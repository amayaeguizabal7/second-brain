# Guía de Contribución

¡Gracias por tu interés en contribuir a este proyecto! 🎉

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [¿Cómo Puedo Contribuir?](#cómo-puedo-contribuir)
- [Configuración de Desarrollo](#configuración-de-desarrollo)
- [Proceso de Pull Request](#proceso-de-pull-request)
- [Guías de Estilo](#guías-de-estilo)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Mejoras](#sugerir-mejoras)

---

## 📜 Código de Conducta

Este proyecto se adhiere a un código de conducta basado en respeto y colaboración:

- ✅ Sé respetuoso y considerado
- ✅ Acepta críticas constructivas
- ✅ Enfócate en lo que es mejor para la comunidad
- ✅ Muestra empatía hacia otros miembros

---

## 🤝 ¿Cómo Puedo Contribuir?

### Tipos de Contribuciones

1. **🐛 Reportar Bugs** - Encuentra y reporta problemas
2. **✨ Sugerir Features** - Propón nuevas características
3. **📝 Mejorar Documentación** - Corrige typos, añade ejemplos
4. **💻 Contribuir Código** - Implementa features o fixes
5. **🎨 Diseño UI/UX** - Mejora la interfaz del widget
6. **🧪 Testing** - Añade o mejora tests

---

## 🛠️ Configuración de Desarrollo

### Requisitos

- Node.js 18+
- Python 3.10+
- Git
- Un editor (recomendamos VS Code)

### Configuración Inicial

1. **Fork el repositorio**

Haz click en "Fork" en la esquina superior derecha de GitHub.

2. **Clona tu fork**

```bash
git clone https://github.com/TU-USUARIO/app-GPT.git
cd app-GPT
```

3. **Añade el repositorio original como remote**

```bash
git remote add upstream https://github.com/Raul-Marin/app-GPT.git
```

4. **Instala dependencias**

```bash
# Node.js
npm install

# Python
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r server_python/requirements.txt
```

5. **Crea una rama para tu feature**

```bash
git checkout -b feature/mi-nueva-feature
# o
git checkout -b fix/correccion-de-bug
```

### Desarrollo Local

```bash
# Opción 1: Script automático
./start-dev.sh  # macOS/Linux
.\start-dev.ps1  # Windows

# Opción 2: Manual
# Terminal 1
npm run build && npm run serve

# Terminal 2
source .venv/bin/activate
npm run server:python
```

---

## 🔄 Proceso de Pull Request

### Antes de Crear un PR

1. ✅ Asegúrate de que tu código funciona
2. ✅ Ejecuta `npm run build` sin errores
3. ✅ Prueba el servidor MCP localmente
4. ✅ Actualiza la documentación si es necesario
5. ✅ Mantén los commits limpios y descriptivos

### Crear el Pull Request

1. **Haz commit de tus cambios**

```bash
git add .
git commit -m "feat: Añade nueva funcionalidad X"
```

**Formato de commits:** Usamos [Conventional Commits](https://www.conventionalcommits.org/)

```
feat: Nueva característica
fix: Corrección de bug
docs: Cambios en documentación
style: Formato, sin cambios de código
refactor: Refactorización de código
test: Añadir o actualizar tests
chore: Tareas de mantenimiento
```

2. **Push a tu fork**

```bash
git push origin feature/mi-nueva-feature
```

3. **Abre un Pull Request**

Ve a GitHub y haz click en "Compare & pull request".

### Template de Pull Request

```markdown
## Descripción

Breve descripción de los cambios.

## Tipo de Cambio

- [ ] 🐛 Bug fix
- [ ] ✨ Nueva feature
- [ ] 📝 Documentación
- [ ] 🎨 Estilos/UI
- [ ] ♻️ Refactorización

## ¿Cómo ha sido probado?

Describe cómo has probado los cambios.

## Checklist

- [ ] Mi código sigue las guías de estilo
- [ ] He actualizado la documentación
- [ ] He probado los cambios localmente
- [ ] He revisado el código antes de hacer commit
```

---

## 📐 Guías de Estilo

### TypeScript/React

```typescript
// ✅ Bueno: Componentes funcionales con tipos
interface TaskProps {
  task: Task;
  onToggle: (id: string) => void;
}

export function TaskCard({ task, onToggle }: TaskProps) {
  return (
    <div className="rounded-xl border border-subtle">
      {/* contenido */}
    </div>
  );
}

// ❌ Malo: Sin tipos, sintaxis antigua
export default function TaskCard(props) {
  return <div>{/* contenido */}</div>
}
```

### Python/FastAPI

```python
# ✅ Bueno: Type hints, nombres descriptivos
from typing import List, Dict, Any
from pydantic import BaseModel

class Task(BaseModel):
    id: str
    title: str
    completed: bool

def get_tasks() -> List[Task]:
    """Obtiene todas las tareas."""
    return tasks_db

# ❌ Malo: Sin tipos, sin docstrings
def get_tasks():
    return tasks_db
```

### CSS/Tailwind

```tsx
// ✅ Bueno: Clases Tailwind semánticas
<div className="rounded-xl border border-subtle bg-default p-4 hover:shadow-md">
  <h3 className="heading-lg text-primary">Título</h3>
</div>

// ❌ Malo: Estilos inline
<div style={{ borderRadius: '12px', padding: '16px' }}>
  <h3 style={{ fontSize: '20px' }}>Título</h3>
</div>
```

### Estructura de Archivos

```
src/
├── component-name/
│   ├── index.html         # HTML base
│   ├── main.tsx           # Entry point
│   ├── App.tsx            # Componente principal
│   ├── main.css           # Estilos
│   └── types.ts           # (opcional) Tipos
```

---

## 🐛 Reportar Bugs

### Antes de Reportar

1. ✅ Busca en [Issues existentes](https://github.com/Raul-Marin/app-GPT/issues)
2. ✅ Verifica que sea un bug real (no comportamiento esperado)
3. ✅ Prueba con la última versión

### Template de Bug Report

```markdown
## Descripción del Bug

Descripción clara y concisa del problema.

## Pasos para Reproducir

1. Ve a '...'
2. Click en '...'
3. Observa el error

## Comportamiento Esperado

Qué debería suceder.

## Comportamiento Actual

Qué sucede realmente.

## Screenshots

Si aplica, añade screenshots.

## Entorno

- OS: [macOS 14, Windows 11, Ubuntu 22.04]
- Node.js: [v18.x, v20.x]
- Python: [v3.10, v3.11]
- Browser: [Chrome 120, Firefox 121]

## Información Adicional

Cualquier otro contexto relevante.
```

---

## 💡 Sugerir Mejoras

### Template de Feature Request

```markdown
## Descripción de la Feature

Descripción clara de la nueva funcionalidad.

## Problema que Resuelve

¿Qué problema resuelve esta feature?

## Solución Propuesta

Cómo debería funcionar.

## Alternativas Consideradas

Otras soluciones que consideraste.

## Impacto

- ¿Afecta a usuarios existentes?
- ¿Requiere cambios en la API?
- ¿Requiere cambios en la documentación?
```

---

## 🧪 Testing

### Testing Manual

1. **Build del widget**
```bash
npm run build
```

2. **Inicia el servidor**
```bash
./start-dev.sh
```

3. **Prueba el widget**
- Navega a http://localhost:8000/widget
- Verifica que se renderice correctamente

4. **Prueba el MCP endpoint**
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
  }'
```

### Testing en ChatGPT

1. Usa ngrok para exponer tu servidor local
2. Configura el connector en ChatGPT
3. Prueba los comandos en una conversación

---

## 📚 Recursos Útiles

- [OpenAI Apps SDK Examples](https://github.com/openai/openai-apps-sdk-examples)
- [Apps SDK UI](https://github.com/openai/apps-sdk-ui)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [Tailwind CSS Docs](https://tailwindcss.com/)

---

## ❓ Preguntas

Si tienes preguntas, puedes:

1. **Abrir una [Discussion](https://github.com/Raul-Marin/app-GPT/discussions)**
2. **Revisar la [documentación del proyecto](./README.md)**
3. **Abrir un [Issue](https://github.com/Raul-Marin/app-GPT/issues)** (para bugs específicos)

---

## 🎉 ¡Gracias por Contribuir!

Tu contribución hace que este proyecto sea mejor para todos. ¡Gracias! 🙏

---

**Mantenedor:** [@Raul-Marin](https://github.com/Raul-Marin)

