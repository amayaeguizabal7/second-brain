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
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# Configuración
BASE_URL = os.environ.get("BASE_URL", "https://app-gpt-s9jl.onrender.com")
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


def create_simple_card_html(tasks: List[Dict[str, Any]]) -> str:
    """Crea una card HTML simple y minimalista con las tareas"""
    incomplete = sum(1 for t in tasks if not t["completed"])
    completed = sum(1 for t in tasks if t["completed"])
    
    # Generar items de tareas
    task_items = ""
    for task in tasks[:5]:  # Solo mostrar las primeras 5
        status = "✅" if task["completed"] else "⬜"
        priority_color = {"high": "#ef4444", "medium": "#f59e0b", "low": "#10b981"}.get(task["priority"], "#6b7280")
        opacity = "0.6" if task["completed"] else "1"
        text_decoration = "line-through" if task["completed"] else "none"
        
        task_items += f"""
        <div style="display: flex; align-items: start; gap: 8px; padding: 8px; border-left: 3px solid {priority_color}; background: rgba(0,0,0,0.02); border-radius: 4px; margin-bottom: 8px; opacity: {opacity};">
            <span style="font-size: 16px;">{status}</span>
            <div style="flex: 1;">
                <div style="font-weight: 600; color: #1f2937; text-decoration: {text_decoration};">{task['title']}</div>
                {f"<div style='font-size: 13px; color: #6b7280; margin-top: 2px;'>{task.get('description', '')}</div>" if task.get('description') else ""}
                {f"<div style='font-size: 12px; color: #9ca3af; margin-top: 4px;'>📅 {task.get('dueDate', '')}</div>" if task.get('dueDate') else ""}
            </div>
        </div>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Task Summary</title>
    </head>
    <body style="margin: 0; padding: 16px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <div style="max-width: 500px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 20px; border: 1px solid #e5e7eb;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <h2 style="margin: 0; font-size: 20px; color: #111827;">📋 Mis Tareas</h2>
                <div style="display: flex; gap: 12px; font-size: 14px;">
                    <span style="background: #fef3c7; color: #92400e; padding: 4px 10px; border-radius: 12px; font-weight: 600;">⬜ {incomplete}</span>
                    <span style="background: #d1fae5; color: #065f46; padding: 4px 10px; border-radius: 12px; font-weight: 600;">✅ {completed}</span>
                </div>
            </div>
            <div style="margin-top: 16px;">
                {task_items}
            </div>
            <div style="margin-top: 16px; padding-top: 16px; border-top: 1px solid #e5e7eb; text-align: center;">
                <a href="{BASE_URL}/widget" target="_blank" style="color: #2563eb; text-decoration: none; font-size: 14px; font-weight: 500;">🔗 Ver widget completo →</a>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html


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

# Montar directorio de assets estáticos
if ASSETS_DIR.exists():
    assets_path = ASSETS_DIR / "assets"
    if assets_path.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_path)), name="assets")


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


@app.get("/card", response_class=HTMLResponse)
async def get_card():
    """Obtener una card HTML simple con las tareas"""
    card_html = create_simple_card_html(tasks_db)
    return HTMLResponse(content=card_html)


# Endpoints compatibles con MCP (simplificados pero correctos)
@app.post("/mcp")
async def mcp_handler(request: Dict[str, Any]):
    """
    Manejador principal MCP - Compatible con ChatGPT
    Recibe mensajes en formato JSON-RPC 2.0
    """
    method = request.get("method", "")
    params = request.get("params", {})
    request_id = request.get("id")
    
    # Initialize
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "Task Manager MCP Server",
                    "version": "1.0.0"
                }
            }
        }
    
    # List Tools
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
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
                                "description": {"type": "string", "description": "Descripción detallada"},
                                "dueDate": {"type": "string", "description": "Fecha YYYY-MM-DD"},
                                "priority": {"type": "string", "enum": ["low", "medium", "high"], "default": "medium"},
                            },
                            "required": ["title"],
                        }
                    },
                    {
                        "name": "update_task_status",
                        "description": "Actualiza el estado de una tarea",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "task_id": {"type": "string", "description": "ID de la tarea"},
                                "completed": {"type": "boolean", "description": "Estado completado"},
                            },
                            "required": ["task_id", "completed"],
                        }
                    }
                ]
            }
        }
    
    # Call Tool
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "get_tasks":
            incomplete = sum(1 for t in tasks_db if not t["completed"])
            completed = sum(1 for t in tasks_db if t["completed"])
            
            # Crear lista formateada de tareas
            tasks_text = f"📋 **Resumen de Tareas**\n\n"
            tasks_text += f"⬜ Pendientes: **{incomplete}** | ✅ Completadas: **{completed}**\n\n"
            
            if incomplete > 0:
                tasks_text += "**Tareas Pendientes:**\n"
                for task in [t for t in tasks_db if not t["completed"]]:
                    priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task["priority"], "⚪")
                    tasks_text += f"\n{priority_emoji} **{task['title']}**"
                    if task.get("description"):
                        tasks_text += f"\n   _{task['description']}_"
                    if task.get("dueDate"):
                        tasks_text += f"\n   📅 {task['dueDate']}"
                    tasks_text += "\n"
            
            if completed > 0:
                tasks_text += "\n**Tareas Completadas:**\n"
                for task in [t for t in tasks_db if t["completed"]]:
                    tasks_text += f"\n✅ ~~{task['title']}~~"
            
            tasks_text += f"\n\n🎨 **[Ver widget interactivo]({BASE_URL}/card)** con diseño completo"
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": tasks_text
                        }
                    ]
                }
            }
        
        elif tool_name == "create_task":
            new_task = {
                "id": str(len(tasks_db) + 1),
                "title": arguments.get("title", "Nueva tarea"),
                "description": arguments.get("description"),
                "dueDate": arguments.get("dueDate"),
                "completed": False,
                "priority": arguments.get("priority", "medium"),
            }
            tasks_db.append(new_task)
            
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(new_task["priority"], "⚪")
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"✓ Tarea creada: {priority_emoji} **{new_task['title']}**\n\n🔗 Ver todas las tareas: {BASE_URL}/widget"
                        }
                    ]
                }
            }
        
        elif tool_name == "update_task_status":
            task_id = arguments.get("task_id")
            completed = arguments.get("completed")
            task = next((t for t in tasks_db if t["id"] == task_id), None)
            
            if not task:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32602,
                        "message": f"Tarea {task_id} no encontrada"
                    }
                }
            
            task["completed"] = completed
            status_emoji = "✅" if completed else "⬜"
            status_text = "completada" if completed else "pendiente"
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"{status_emoji} Tarea marcada como {status_text}: **{task['title']}**\n\n🔗 Ver todas las tareas: {BASE_URL}/widget"
                        }
                    ]
                }
            }
    
    # Método no soportado
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": -32601,
            "message": f"Método no soportado: {method}"
        }
    }


@app.options("/mcp")
async def mcp_options():
    """CORS preflight para MCP"""
    return {}


# Endpoint GET para testing/debugging (opcional)
@app.get("/mcp/tools")
async def list_tools_get():
    """Lista las herramientas disponibles (para debugging)"""
    return {
        "tools": ["get_tasks", "create_task", "update_task_status"],
        "note": "Use POST /mcp with JSON-RPC 2.0 format for actual MCP communication"
    }


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
