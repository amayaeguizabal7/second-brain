# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto sigue [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-26

### ✨ Added
- Widget interactivo de React con OpenAI Apps SDK UI
- Servidor MCP completo en Python/FastAPI con JSON-RPC 2.0
- Integración completa con ChatGPT usando Model Context Protocol
- Sistema de recursos MCP con `resources/list` y `resources/read`
- Widget HTML embebible con `text/html+skybridge` MIME type
- Estado dinámico en React con `useState` y `useEffect`
- Escucha de eventos `openai:set_globals` para actualizaciones
- Herramientas MCP: `get_tasks`, `create_task`, `update_task_status`, `delete_task`
- Despliegue en Render con configuración `render.yaml`
- Scripts de desarrollo para macOS/Linux (`start-dev.sh`) y Windows (`start-dev.ps1`)
- Documentación completa: README, QUICKSTART, TUTORIAL, PROJECT_STRUCTURE, etc.
- Componentes UI accesibles: Badge, Button, Icon (Calendar, CheckCircle, Circle)
- Diseño responsive con Tailwind CSS 4
- Servidor de assets estáticos para desarrollo local
- CORS configurado para desarrollo y producción

### 🎨 Design
- Interfaz moderna con design system de OpenAI Apps SDK UI
- Dark mode compatible
- Componentes con animaciones y transiciones suaves
- Layout responsive que se adapta a diferentes tamaños

### 🛠️ Technical
- Build con Vite para compilación ultrarrápida
- TypeScript para type safety
- PostCSS + Tailwind 4 para estilos
- FastAPI + Uvicorn para el backend
- Pydantic para validación de datos
- Protocolo JSON-RPC 2.0 estándar
- Sistema de recursos MCP oficial de OpenAI

### 📚 Documentation
- README.md completamente actualizado
- QUICKSTART.md para empezar en 5 minutos
- TUTORIAL.md con guía paso a paso
- PROJECT_STRUCTURE.md con arquitectura detallada
- DEPLOY_RENDER.md para despliegue en Render
- NGROK_SETUP.md para tunneling local
- EXAMPLES.md con casos de uso
- OPCIONES_CHATGPT.md con opciones de integración

### 🔧 Configuration
- `vite.config.ts` optimizado para múltiples entry points
- `postcss.config.mjs` con Tailwind 4
- `render.yaml` para auto-deploy
- `.gitignore` actualizado
- `requirements.txt` con dependencias Python mínimas

### 🐛 Fixed
- Rutas correctas de assets compilados en producción
- CORS headers para permitir embedding en ChatGPT
- Formato correcto de respuestas MCP JSON-RPC 2.0
- Widget HTML con rutas absolutas de assets
- Inyección correcta de datos con `window.__TASK_DATA__`

### 🚀 Deployment
- Configuración automática de Render
- Variables de entorno (`BASE_URL`) correctamente configuradas
- Build command optimizado: `npm install && npm run build && pip install`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Auto-deploy desde GitHub main branch

## [0.2.0] - 2025-11-25

### Added
- Card HTML simple para testing de widgets
- Test interface local para simular ChatGPT
- Scripts de testing: `test-chatgpt-local.sh`, `test-mcp-protocol.sh`

### Fixed
- Problemas de embedding de HTML en ChatGPT
- Formato de `_meta.openai/outputTemplate`

## [0.1.0] - 2025-11-24

### Added
- Proyecto inicial con Apps SDK de OpenAI
- Estructura básica del proyecto
- Configuración inicial de Node.js y Python
- Primera versión del widget Task Manager
- Servidor MCP básico

---

## Tipos de Cambios

- `Added` - Nuevas características
- `Changed` - Cambios en funcionalidad existente
- `Deprecated` - Características que serán removidas
- `Removed` - Características removidas
- `Fixed` - Corrección de bugs
- `Security` - Correcciones de seguridad

