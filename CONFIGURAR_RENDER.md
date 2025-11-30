# 🚀 Configuración de Render para Second Brain

## ✅ Repositorio de GitHub creado
- **URL**: https://github.com/amayaeguizabal7/second-brain
- **Código**: Subido exitosamente ✅

---

## 📋 Pasos para Configurar Render

### Paso 1: Crear un Nuevo Servicio Web en Render

1. Ve a tu dashboard de Render: https://dashboard.render.com/
2. Si ya tienes el servicio "app-GPT", puedes:
   - **Opción A**: Editar el servicio existente y cambiar el repositorio
   - **Opción B**: Crear un nuevo servicio (recomendado)

### Paso 2: Si vas a EDITAR el servicio existente:

En la configuración del servicio "app-GPT":

1. **General**:
   - **Name**: Cambiar a `second-brain`

2. **Build & Deploy**:
   - **Repository**: Cambiar a:
     ```
     https://github.com/amayaeguizabal7/second-brain
     ```
   - **Branch**: `main`
   - **Build Command**: 
     ```
     npm install && npm run build && pip install -r server_python/requirements.txt
     ```
   - **Start Command**: 
     ```
     uvicorn server_python.main:app --host 0.0.0.0 --port $PORT
     ```

3. **Environment** (en el menú lateral izquierdo):
   - Haz clic en "Environment"
   - Agrega una nueva variable:
     - **Key**: `BASE_URL`
     - **Value**: Dejar vacío por ahora (lo actualizaremos después del primer deploy)

4. **Health Checks**:
   - **Health Check Path**: `/health`

5. Haz clic en **"Save Changes"**

### Paso 3: Si vas a CREAR un nuevo servicio:

1. En Render, haz clic en **"New +"** → **"Web Service"**
2. Conecta tu cuenta de GitHub si no lo has hecho
3. Selecciona el repositorio: **`amayaeguizabal7/second-brain`**
4. Configura:
   - **Name**: `second-brain`
   - **Region**: Oregon (US West) o la que prefieras
   - **Branch**: `main`
   - **Root Directory**: (dejar vacío)
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```
     npm install && npm run build && pip install -r server_python/requirements.txt
     ```
   - **Start Command**: 
     ```
     uvicorn server_python.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Instance Type**: Free (para empezar)

5. Haz clic en **"Create Web Service"**

### Paso 4: Configurar Variables de Entorno

1. Una vez creado o actualizado el servicio, ve a **"Environment"** en el menú lateral
2. Haz clic en **"Add Environment Variable"**
3. Agrega:
   - **Key**: `BASE_URL`
   - **Value**: Por ahora déjala vacía o usa: `https://second-brain-XXXXX.onrender.com`
   
   ⚠️ **Nota**: Después del primer deploy, Render te dará la URL real. Actualiza esta variable con la URL completa (ej: `https://second-brain-abc123.onrender.com`)

### Paso 5: Primer Deploy

1. Render detectará automáticamente los cambios y empezará a construir
2. Ve a la pestaña **"Logs"** para ver el progreso
3. El proceso puede tomar 5-10 minutos la primera vez

### Paso 6: Actualizar BASE_URL después del deploy

1. Una vez que el deploy termine exitosamente, Render te dará una URL como:
   ```
   https://second-brain-XXXXX.onrender.com
   ```

2. Ve a **Environment** → Edita la variable `BASE_URL`
3. Pon la URL completa: `https://second-brain-XXXXX.onrender.com`
4. Guarda los cambios
5. Render hará un nuevo deploy automáticamente

---

## ✅ Verificación

Una vez configurado, deberías poder acceder a:

- **Aplicación**: `https://second-brain-XXXXX.onrender.com`
- **Health Check**: `https://second-brain-XXXXX.onrender.com/health`
- **Widget**: `https://second-brain-XXXXX.onrender.com/widget`
- **MCP Endpoint**: `https://second-brain-XXXXX.onrender.com/mcp`

---

## 🔗 Integración con ChatGPT

Una vez que tengas la URL de producción, configura el connector en ChatGPT:

1. **ChatGPT** → **Settings** ⚙️
2. Ve a **Connectors** o **MCP Settings**
3. Agrega:
   - **Name**: `Second Brain`
   - **Type**: `MCP`
   - **URL**: `https://second-brain-XXXXX.onrender.com/mcp`
4. Guarda y actualiza

---

## 📝 Notas Importantes

- El archivo `render.yaml` ya está configurado en el repositorio
- Render puede detectar automáticamente la configuración si usas el archivo `render.yaml`
- El primer deploy puede tardar más tiempo porque instala todas las dependencias
- Asegúrate de que `BASE_URL` esté correctamente configurada después del primer deploy

---

## 🆘 Si algo falla

1. Revisa los logs en Render (pestaña "Logs")
2. Verifica que todas las variables de entorno estén correctas
3. Asegúrate de que el repositorio sea accesible
4. Verifica que los comandos de build y start sean correctos

