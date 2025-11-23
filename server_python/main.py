"""
Servidor de ejemplo para Task Manager
API REST simple que sirve el widget de tareas
"""

import os
import json
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

# Configuración
BASE_URL = os.environ.get("BASE_URL", "http://localhost:4444")
ASSETS_DIR = Path(__file__).parent.parent / "dist"

# Base de datos simple en memoria
tasks_db = [
    {
        "id": "1",
        "title": "Revisar propuesta de diseño",
        "description": "Analizar mockups del nuevo dashboard",
        "dueDate": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        "completed": False,
        "priority": "high",
    },
    {
        "id": "2",
        "title": "Actualizar documentación",
        "description": "Añadir ejemplos de uso del API",
        "dueDate": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "completed": False,
        "priority": "medium",
    },
    {
        "id": "3",
        "title": "Reunión de equipo",
        "description": "Sprint planning Q1 2026",
        "dueDate": datetime.now().strftime("%Y-%m-%d"),
        "completed": True,
        "priority": "low",
    },
]


# Modelos de datos
class Task(BaseModel):
    id: Optional[str] = None
    title: str = Field(..., description="Título de la tarea")
    description: Optional[str] = Field(None, description="Descripción detallada")
    dueDate: Optional[str] = Field(None, description="Fecha de vencimiento (YYYY-MM-DD)")
    priority: str = Field("medium", description="Prioridad: low, medium, high")
    completed: bool = Field(False, description="Estado de completado")


class TaskUpdate(BaseModel):
    completed: bool = Field(..., description="Estado de completado")


@lru_cache(maxsize=10)
def load_widget_html(widget_name: str) -> str:
    """Carga el HTML del widget desde los assets compilados"""
    # Buscar en directorios comunes donde puede estar el widget
    possible_paths = [
        ASSETS_DIR / f"{widget_name}.html",
        ASSETS_DIR / widget_name / "index.html",
        ASSETS_DIR / "src" / widget_name / "index.html",
    ]
    
    # También buscar recursivamente por si está en otra ubicación
    html_files = list(ASSETS_DIR.glob(f"**/*{widget_name}*/index.html"))
    possible_paths.extend(html_files)
    
    # Buscar archivos que contengan el nombre del widget
    html_files_by_name = list(ASSETS_DIR.glob(f"**/{widget_name}*.html"))
    possible_paths.extend(html_files_by_name)
    
    # Encontrar el primer archivo que existe
    html_file = None
    for path in possible_paths:
        if path.exists() and path.is_file():
            html_file = path
            break
    
    if not html_file:
        # Mostrar rutas para debug
        all_html = list(ASSETS_DIR.glob("**/*.html"))
        error_msg = f"""
        <div style="padding: 20px; font-family: monospace; background: #fee; border: 2px solid #f00; border-radius: 8px;">
            <h3>❌ Widget '{widget_name}' no encontrado</h3>
            <p><strong>Directorio base:</strong> {ASSETS_DIR}</p>
            <p><strong>Rutas buscadas:</strong></p>
            <ul style="background: #fff; padding: 10px; border-radius: 4px;">
                {''.join(f'<li>{p}</li>' for p in possible_paths[:3])}
            </ul>
            <p><strong>Archivos HTML disponibles:</strong></p>
            <ul style="background: #fff; padding: 10px; border-radius: 4px;">
                {''.join(f'<li>{f.relative_to(ASSETS_DIR)}</li>' for f in all_html) if all_html else '<li>Ninguno encontrado</li>'}
            </ul>
            <p><strong>✅ Solución:</strong> Ejecuta <code>npm run build</code></p>
        </div>
        """
        return error_msg
    
    html_content = html_file.read_text()
    
    # Reemplazar rutas relativas con la URL base
    html_content = html_content.replace('="/assets/', f'="{BASE_URL}/assets/')
    html_content = html_content.replace("'/assets/", f"'{BASE_URL}/assets/")
    html_content = html_content.replace('="./assets/', f'="{BASE_URL}/assets/')
    html_content = html_content.replace("'./assets/", f"'{BASE_URL}/assets/")
    
    return html_content


def create_widget_html(tasks: List[Dict[str, Any]]) -> str:
    """Crea el HTML del widget con los datos de las tareas"""
    html_template = load_widget_html("task-manager")
    
    # Inyectar datos de tareas en el HTML
    tasks_json = json.dumps(tasks)
    
    # Insertar script antes del cierre de body
    injection = f"""
    <script>
        window.__TASK_DATA__ = {tasks_json};
    </script>
    </body>
    """
    html_template = html_template.replace("</body>", injection)
    
    return html_template


# Configurar FastAPI
app = FastAPI(
    title="Task Manager Demo Server",
    description="Servidor de ejemplo para gestión de tareas con widget interactivo",
    version="1.0.0",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Endpoint de información"""
    return {
        "name": "Task Manager Demo Server",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "tasks": "/tasks",
            "widget": "/widget",
            "mcp_tools": "/mcp/tools",
            "mcp_call": "/mcp/call"
        }
    }


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy", "tasks_count": len(tasks_db)}


@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    """Obtener todas las tareas"""
    return tasks_db


@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    """Crear una nueva tarea"""
    task.id = str(len(tasks_db) + 1)
    task_dict = task.model_dump()
    tasks_db.append(task_dict)
    return task_dict


@app.patch("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task_update: TaskUpdate):
    """Actualizar el estado de una tarea"""
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    task["completed"] = task_update.completed
    return task


@app.get("/widget", response_class=HTMLResponse)
async def get_widget():
    """Obtener el widget HTML con los datos actuales"""
    widget_html = create_widget_html(tasks_db)
    return HTMLResponse(content=widget_html)


# Endpoints compatibles con MCP (simplificados)
@app.get("/mcp")
async def mcp_info():
    """Información del servidor MCP - Compatible con ChatGPT"""
    # Devolver las herramientas disponibles directamente
    return {
        "tools": [
            {
                "name": "get_tasks",
                "description": "Obtiene todas las tareas del usuario con un widget interactivo",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                }
            },
            {
                "name": "create_task",
                "description": "Crea una nueva tarea",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Título de la tarea"},
                        "description": {"type": "string", "description": "Descripción detallada (opcional)"},
                        "dueDate": {"type": "string", "description": "Fecha de vencimiento en formato YYYY-MM-DD (opcional)"},
                        "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "Prioridad de la tarea", "default": "medium"},
                    },
                    "required": ["title"],
                }
            },
            {
                "name": "update_task_status",
                "description": "Actualiza el estado de completado de una tarea",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "ID de la tarea a actualizar"},
                        "completed": {"type": "boolean", "description": "Nuevo estado de completado"},
                    },
                    "required": ["task_id", "completed"],
                }
            }
        ]
    }


@app.options("/mcp")
async def mcp_options():
    """CORS preflight para MCP"""
    return {}


@app.get("/mcp/tools")
async def list_mcp_tools():
    """Lista las herramientas disponibles (formato MCP simplificado)"""
    return {
        "tools": [
            {
                "name": "get_tasks",
                "description": "Obtiene todas las tareas del usuario con un widget interactivo",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                }
            },
            {
                "name": "create_task",
                "description": "Crea una nueva tarea",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Título de la tarea",
                        },
                        "description": {
                            "type": "string",
                            "description": "Descripción detallada (opcional)",
                        },
                        "dueDate": {
                            "type": "string",
                            "description": "Fecha de vencimiento en formato YYYY-MM-DD (opcional)",
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high"],
                            "description": "Prioridad de la tarea",
                            "default": "medium",
                        },
                    },
                    "required": ["title"],
                }
            },
            {
                "name": "update_task_status",
                "description": "Actualiza el estado de completado de una tarea",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "ID de la tarea a actualizar",
                        },
                        "completed": {
                            "type": "boolean",
                            "description": "Nuevo estado de completado",
                        },
                    },
                    "required": ["task_id", "completed"],
                }
            }
        ]
    }


@app.post("/mcp/call")
async def call_mcp_tool(request: Dict[str, Any]):
    """Ejecuta una herramienta MCP (formato simplificado)"""
    tool_name = request.get("name")
    arguments = request.get("arguments", {})
    
    if tool_name == "get_tasks":
        widget_html = create_widget_html(tasks_db)
        incomplete_count = sum(1 for t in tasks_db if not t["completed"])
        completed_count = sum(1 for t in tasks_db if t["completed"])
        
        return {
            "result": {
                "text": f"Tienes {incomplete_count} tarea(s) pendiente(s) y {completed_count} completada(s).",
                "widget": widget_html
            }
        }
    
    elif tool_name == "create_task":
        new_task = {
            "id": str(len(tasks_db) + 1),
            "title": arguments["title"],
            "description": arguments.get("description"),
            "dueDate": arguments.get("dueDate"),
            "completed": False,
            "priority": arguments.get("priority", "medium"),
        }
        tasks_db.append(new_task)
        
        widget_html = create_widget_html(tasks_db)
        
        return {
            "result": {
                "text": f"✓ Tarea creada: {new_task['title']}",
                "widget": widget_html
            }
        }
    
    elif tool_name == "update_task_status":
        task_id = arguments["task_id"]
        completed = arguments["completed"]
        
        task = next((t for t in tasks_db if t["id"] == task_id), None)
        if not task:
            return {
                "error": f"Tarea con ID {task_id} no encontrada"
            }
        
        task["completed"] = completed
        status_text = "completada" if completed else "pendiente"
        
        widget_html = create_widget_html(tasks_db)
        
        return {
            "result": {
                "text": f"✓ Tarea marcada como {status_text}: {task['title']}",
                "widget": widget_html
            }
        }
    
    return {
        "error": f"Herramienta '{tool_name}' no reconocida"
    }


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
