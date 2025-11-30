# 🔧 Solución: Widget no carga en ChatGPT

## Problema Identificado

El widget no se carga en ChatGPT porque:
1. **BASE_URL no está configurada** en Render
2. Las rutas de los assets necesitan URLs absolutas

## ✅ Solución Paso a Paso

### Paso 1: Configurar BASE_URL en Render

1. Ve a tu dashboard de Render: https://dashboard.render.com/
2. Haz clic en tu servicio `second-brain`
3. En el menú lateral izquierdo, haz clic en **"Environment"**
4. Haz clic en **"Add Environment Variable"**
5. Agrega:
   - **Key**: `BASE_URL`
   - **Value**: `https://second-brain-4ijd.onrender.com`
6. Haz clic en **"Save Changes"**
7. Render hará un nuevo deploy automáticamente (puede tomar 2-3 minutos)

### Paso 2: Verificar que los Assets se Sirvan Correctamente

Una vez que el deploy termine, verifica que los assets se puedan cargar:

```bash
# Verificar que el JavaScript se sirve
curl -I https://second-brain-4ijd.onrender.com/assets/second-brain-BIOttPsk.js

# Verificar que el CSS se sirve
curl -I https://second-brain-4ijd.onrender.com/assets/second-brain-B29qkEue.css
```

Deberían devolver `HTTP/2 200`.

### Paso 3: Verificar que el Widget Use URLs Absolutas

Después del deploy, verifica que el widget HTML tenga URLs absolutas:

```bash
curl -s https://second-brain-4ijd.onrender.com/widget | grep "assets"
```

Deberías ver algo como:
```html
<script src="https://second-brain-4ijd.onrender.com/assets/second-brain-BIOttPsk.js"></script>
```

**NO** deberías ver rutas relativas como `/assets/...`.

### Paso 4: Probar el Widget en ChatGPT

1. Espera a que el deploy termine completamente (ve a la pestaña "Logs" en Render)
2. En ChatGPT, prueba:
   ```
   👤 "Muéstrame mis notas"
   ```
3. El widget debería aparecer en la conversación

## 🔍 Debugging

Si el widget aún no carga, verifica:

### 1. Verificar el Endpoint MCP

```bash
curl -X POST https://second-brain-4ijd.onrender.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"resources/read","params":{"uri":"ui://widget/second-brain.html"}}'
```

Debería devolver el HTML del widget con URLs absolutas.

### 2. Verificar en la Consola del Navegador

Si estás probando el widget directamente en el navegador:
- Abre las herramientas de desarrollador (F12)
- Ve a la pestaña "Console"
- Busca errores relacionados con CORS o carga de recursos

### 3. Verificar los Logs de Render

1. En Render, ve a la pestaña **"Logs"**
2. Busca errores durante el build o el runtime
3. Asegúrate de que `npm run build` se ejecutó correctamente

## 📝 Cambios Realizados

He actualizado el código para:
1. Detectar automáticamente `BASE_URL` desde variables de entorno de Render
2. Mejorar el reemplazo de rutas de assets para usar URLs absolutas
3. Hacer el código más robusto

**Importante**: Los cambios ya están en el repositorio, pero necesitas hacer push y que Render los despliegue.

## 🚀 Siguiente Paso

Una vez que configures `BASE_URL` en Render y se complete el deploy, el widget debería funcionar en ChatGPT.

## ⚠️ Nota sobre CORS

Si hay problemas de CORS, el servidor ya tiene CORS configurado para permitir todas las fuentes. Pero si ChatGPT tiene problemas específicos, podríamos necesitar ajustar la configuración de CORS.

