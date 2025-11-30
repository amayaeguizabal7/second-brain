"""
Servidor de ejemplo para Second Brain
API REST simple que sirve el widget de notas y conocimiento
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
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")
ASSETS_DIR = Path(__file__).parent.parent / "dist"

# Base de datos simple en memoria
notes_db = [
    {
        "id": "1",
        "title": "Ideas sobre arquitectura de software",
        "description": "Reflexiones sobre patrones de diseño y arquitectura limpia",
        "createdAt": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
        "category": "technology",
        "tags": ["arquitectura", "patrones"],
    },
    {
        "id": "2",
        "title": "Notas de lectura: Clean Code",
        "description": "Principios clave sobre escribir código limpio y mantenible",
        "createdAt": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "category": "learning",
        "tags": ["programación", "libros"],
    },
    {
        "id": "3",
        "title": "Ideas para proyecto personal",
        "description": "Brainstorming de características para nueva aplicación",
        "createdAt": datetime.now().strftime("%Y-%m-%d"),
        "category": "ideas",
        "tags": ["proyecto", "innovación"],
    },
]


# Modelos de datos
class Note(BaseModel):
    id: Optional[str] = None
    title: str = Field(..., description="Título de la nota")
    description: Optional[str] = Field(None, description="Contenido detallado de la nota")
    createdAt: Optional[str] = Field(None, description="Fecha de creación (YYYY-MM-DD)")
    category: str = Field("general", description="Categoría: general, technology, learning, ideas, etc.")
    tags: List[str] = Field(default_factory=list, description="Lista de etiquetas")


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


def create_widget_html(notes: List[Dict[str, Any]]) -> str:
    """Crea el HTML del widget con los datos de las notas"""
    html_template = load_widget_html("second-brain")
    
    # Inyectar datos de notas en el HTML en el head, antes de los scripts de React
    notes_json = json.dumps(notes)
    
    # Insertar script en el head para que esté disponible antes de que React cargue
    # Incluir también un script inline para asegurar que los datos estén disponibles
    head_injection = f"""
    <script>
        // Asegurar que los datos estén disponibles antes de que React se monte
        window.__NOTES_DATA__ = {notes_json};
        console.log('Second Brain: Notes data loaded', window.__NOTES_DATA__);
    </script>
    """
    html_template = html_template.replace('</head>', head_injection + '</head>')
    
    return html_template


def create_simple_card_html(notes: List[Dict[str, Any]]) -> str:
    """Crea una card HTML simple y minimalista con las notas"""
    total_notes = len(notes)
    
    # Generar items de notas
    note_items = ""
    for note in notes[:5]:  # Solo mostrar las primeras 5
        category_color = {
            "technology": "#3b82f6",
            "learning": "#10b981",
            "ideas": "#f59e0b",
            "general": "#6b7280"
        }.get(note.get("category", "general"), "#6b7280")
        
        tags_html = ""
        if note.get("tags"):
            tags_html = f"<div style='font-size: 11px; color: #9ca3af; margin-top: 4px;'>🏷️ {', '.join(note['tags'][:3])}</div>"
        
        note_items += f"""
        <div style="display: flex; align-items: start; gap: 8px; padding: 8px; border-left: 3px solid {category_color}; background: rgba(0,0,0,0.02); border-radius: 4px; margin-bottom: 8px;">
            <div style="flex: 1;">
                <div style="font-weight: 600; color: #1f2937;">{note['title']}</div>
                {f"<div style='font-size: 13px; color: #6b7280; margin-top: 2px;'>{note.get('description', '')}</div>" if note.get('description') else ""}
                {f"<div style='font-size: 12px; color: #9ca3af; margin-top: 4px;'>📅 {note.get('createdAt', '')}</div>" if note.get('createdAt') else ""}
                {tags_html}
            </div>
        </div>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Second Brain Summary</title>
    </head>
    <body style="margin: 0; padding: 16px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <div style="max-width: 500px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 20px; border: 1px solid #e5e7eb;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <h2 style="margin: 0; font-size: 20px; color: #111827;">🧠 Second Brain</h2>
                <div style="display: flex; gap: 12px; font-size: 14px;">
                    <span style="background: #dbeafe; color: #1e40af; padding: 4px 10px; border-radius: 12px; font-weight: 600;">📝 {total_notes}</span>
                </div>
            </div>
            <div style="margin-top: 16px;">
                {note_items}
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
    title="Second Brain Server",
    description="Servidor para Second Brain - gestión de notas y conocimiento personal",
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
        "name": "Second Brain Server",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "notes": "/notes",
            "widget": "/widget",
            "mcp_tools": "/mcp/tools",
            "mcp_call": "/mcp/call"
        }
    }


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy", "notes_count": len(notes_db)}


@app.get("/notes", response_model=List[Note])
async def get_notes():
    """Obtener todas las notas"""
    return notes_db


@app.post("/notes", response_model=Note)
async def create_note(note: Note):
    """Crear una nueva nota"""
    note.id = str(len(notes_db) + 1)
    if not note.createdAt:
        note.createdAt = datetime.now().strftime("%Y-%m-%d")
    note_dict = note.model_dump()
    notes_db.append(note_dict)
    return note_dict


@app.get("/notes/{note_id}", response_model=Note)
async def get_note(note_id: str):
    """Obtener una nota específica"""
    note = next((n for n in notes_db if n["id"] == note_id), None)
    if not note:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return note


@app.get("/widget", response_class=HTMLResponse)
async def get_widget():
    """Obtener el widget HTML con los datos actuales"""
    widget_html = create_widget_html(notes_db)
    return HTMLResponse(content=widget_html)


@app.get("/card", response_class=HTMLResponse)
async def get_card():
    """Obtener una card HTML simple con las notas"""
    card_html = create_simple_card_html(notes_db)
    return HTMLResponse(content=card_html)


# Endpoints compatibles con MCP (formato oficial OpenAI)
@app.post("/mcp")
async def mcp_handler(request: Dict[str, Any]):
    """
    Manejador principal MCP - Compatible con ChatGPT
    Recibe mensajes en formato JSON-RPC 2.0
    Formato oficial según la documentación de OpenAI Apps SDK
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
                    "tools": {},
                    "resources": {}
                },
                "serverInfo": {
                    "name": "Second Brain MCP Server",
                    "version": "1.0.0"
                }
            }
        }
    
    # List Resources - CRÍTICO para widgets
    elif method == "resources/list":
        card_html = create_simple_card_html(notes_db)
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "resources": [
                    {
                        "uri": "ui://widget/second-brain.html",
                        "name": "Second Brain Widget",
                        "description": "Widget interactivo para gestionar notas y conocimiento",
                        "mimeType": "text/html+skybridge"
                    }
                ]
            }
        }
    
    # Read Resource - Devuelve el HTML del widget principal de React
    elif method == "resources/read":
        uri = params.get("uri")
        if uri == "ui://widget/second-brain.html":
            widget_html = create_widget_html(notes_db)
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "contents": [
                        {
                            "uri": "ui://widget/second-brain.html",
                            "mimeType": "text/html+skybridge",
                            "text": widget_html,
                            "_meta": {
                                "openai/widgetPrefersBorder": False
                            }
                        }
                    ]
                }
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32602,
                    "message": f"Resource not found: {uri}"
                }
            }
    
    # List Tools - Con metadata oficial de OpenAI
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "get_notes",
                        "description": "Obtiene todas las notas del Second Brain con un widget interactivo",
                        "inputSchema": {
                            "type": "object",
                            "properties": {},
                        },
                        "_meta": {
                            "openai/outputTemplate": "ui://widget/second-brain.html",
                            "openai/toolInvocation/invoking": "Obteniendo notas",
                            "openai/toolInvocation/invoked": "Notas obtenidas"
                        }
                    },
                    {
                        "name": "create_note",
                        "description": "Crea una nueva nota en el Second Brain",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string", "description": "Título de la nota"},
                                "description": {"type": "string", "description": "Contenido detallado de la nota"},
                                "category": {"type": "string", "enum": ["general", "technology", "learning", "ideas"], "default": "general", "description": "Categoría de la nota"},
                                "tags": {"type": "array", "items": {"type": "string"}, "description": "Lista de etiquetas"},
                            },
                            "required": ["title"],
                        },
                        "_meta": {
                            "openai/outputTemplate": "ui://widget/second-brain.html",
                            "openai/toolInvocation/invoking": "Creando nota",
                            "openai/toolInvocation/invoked": "Nota creada"
                        }
                    },
                    {
                        "name": "get_note",
                        "description": "Obtiene una nota específica por su ID",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "note_id": {"type": "string", "description": "ID de la nota"},
                            },
                            "required": ["note_id"],
                        },
                        "_meta": {
                            "openai/outputTemplate": "ui://widget/second-brain.html",
                            "openai/toolInvocation/invoking": "Buscando nota",
                            "openai/toolInvocation/invoked": "Nota encontrada"
                        }
                    }
                ]
            }
        }
    
    # Call Tool
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "get_notes":
            total_notes = len(notes_db)
            
            # Formato oficial OpenAI Apps SDK
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Tienes {total_notes} nota(s) en tu Second Brain."
                        }
                    ],
                    "structuredContent": {
                        "notes": notes_db
                    }
                }
            }
        
        elif tool_name == "create_note":
            new_note = {
                "id": str(len(notes_db) + 1),
                "title": arguments.get("title", "Nueva nota"),
                "description": arguments.get("description"),
                "createdAt": datetime.now().strftime("%Y-%m-%d"),
                "category": arguments.get("category", "general"),
                "tags": arguments.get("tags", []),
            }
            notes_db.append(new_note)
            
            # Formato oficial OpenAI Apps SDK
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Nota creada: \"{new_note['title']}\"."
                        }
                    ],
                    "structuredContent": {
                        "notes": notes_db
                    }
                }
            }
        
        elif tool_name == "get_note":
            note_id = arguments.get("note_id")
            note = next((n for n in notes_db if n["id"] == note_id), None)
            
            if not note:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32602,
                        "message": f"Nota {note_id} no encontrada"
                    }
                }
            
            # Formato oficial OpenAI Apps SDK
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Nota encontrada: \"{note['title']}\"."
                        }
                    ],
                    "structuredContent": {
                        "notes": [note]
                    }
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
        "tools": ["get_notes", "create_note", "get_note"],
        "note": "Use POST /mcp with JSON-RPC 2.0 format for actual MCP communication"
    }


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
