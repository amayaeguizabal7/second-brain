# 📝 Instrucciones para Crear el Repositorio en GitHub

## Paso 1: Crear el Repositorio en GitHub

1. Ve a: **https://github.com/new**
2. **Repository name**: `second-brain`
3. **Description** (opcional): `Second Brain - Personal Knowledge Manager integrado con ChatGPT`
4. **Visibility**: Elige Público o Privado (tu preferencia)
5. **IMPORTANTE**: NO marques ninguna de estas opciones:
   - ❌ Add a README file
   - ❌ Add .gitignore
   - ❌ Choose a license
6. Haz clic en **"Create repository"**

## Paso 2: Una vez creado el repositorio

GitHub te mostrará una página con instrucciones. **NO sigas esas instrucciones**. En su lugar, ejecuta estos comandos en tu terminal:

```bash
cd "/Users/amayaeguizabal/Desktop/FORMACION&MAS/SHIFT + R/App Second Brain"

# Cambiar el remoto al nuevo repositorio
git remote set-url origin https://github.com/amayaeguizabal7/second-brain.git

# Verificar que el remoto cambió
git remote -v

# Subir el código
git push -u origin main
```

## Paso 3: Verificar

Después de ejecutar los comandos, ve a:
**https://github.com/amayaeguizabal7/second-brain**

Deberías ver todo tu código allí.

## ¿Listo?

Una vez que hayas creado el repositorio, avísame y te ayudo a configurar Render.

