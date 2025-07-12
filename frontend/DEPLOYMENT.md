# Guía de Despliegue en Vercel

## Configuración Actual

El proyecto está configurado para desplegarse correctamente en Vercel con las siguientes características:

### ✅ Configuraciones Implementadas

1. **API Routes Funcionales**: El endpoint `/api/predictive-trends` funciona tanto en desarrollo como en producción
2. **Datos Simulados en Producción**: En Vercel (producción) se usan datos simulados ya que Python no está disponible
3. **Configuración de Next.js**: Optimizada para Vercel sin exportación estática
4. **Archivo vercel.json**: Configuración específica para Vercel

### 🔧 Archivos de Configuración

#### `next.config.mjs`
```javascript
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  // Removido output: "export" para permitir API routes
};
```

#### `vercel.json`
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "installCommand": "npm install",
  "devCommand": "npm run dev",
  "functions": {
    "pages/api/**/*.ts": {
      "runtime": "nodejs18.x"
    }
  },
  "env": {
    "NODE_ENV": "production"
  }
}
```

## Pasos para Desplegar

### 1. Preparar el Repositorio
```bash
# Asegúrate de que todos los cambios estén commitados
git add .
git commit -m "Configuración para despliegue en Vercel"
git push origin main
```

### 2. Conectar con Vercel
1. Ve a [vercel.com](https://vercel.com)
2. Inicia sesión con tu cuenta de GitHub
3. Haz clic en "New Project"
4. Importa tu repositorio de GitHub
5. Configura el proyecto:
   - **Framework Preset**: Next.js
   - **Root Directory**: `Proyecto_AsgardStore/frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Install Command**: `npm install`

### 3. Variables de Entorno (Opcional)
Si necesitas variables de entorno específicas:
- Ve a Settings > Environment Variables
- Agrega cualquier variable necesaria

### 4. Desplegar
- Haz clic en "Deploy"
- Vercel construirá y desplegará automáticamente

## Funcionalidades en Producción

### ✅ Lo que Funciona
- **Página principal**: Diseño completo con animaciones
- **API Endpoint**: `/api/predictive-trends` con datos simulados
- **Componente Predictivo**: Muestra resultados del análisis
- **Responsive Design**: Funciona en móvil y desktop

### ⚠️ Limitaciones en Producción
- **Script Python**: No disponible en Vercel (entorno serverless)
- **Datos Simulados**: Se usan datos predefinidos en lugar del script real
- **Nota Informativa**: Se muestra una nota indicando que son datos simulados

## Solución de Problemas

### Error: "Build Failed"
1. Verifica que todas las dependencias estén en `package.json`
2. Revisa los logs de build en Vercel
3. Asegúrate de que no haya errores de TypeScript

### Error: "API Route Not Found"
1. Verifica que el archivo esté en `pages/api/`
2. Asegúrate de que la ruta sea correcta
3. Revisa que el método HTTP sea GET

### Error: "Component Not Loading"
1. Verifica la consola del navegador
2. Revisa que las importaciones sean correctas
3. Asegúrate de que el componente esté exportado correctamente

## Desarrollo Local vs Producción

### Desarrollo Local
- Script Python se ejecuta realmente
- Datos reales del análisis predictivo
- Sin nota de datos simulados

### Producción (Vercel)
- Datos simulados predefinidos
- Nota informativa sobre datos simulados
- Misma interfaz visual

## Actualizaciones

Para actualizar el despliegue:
1. Haz cambios en tu código local
2. Commit y push a GitHub
3. Vercel desplegará automáticamente

## Monitoreo

- **Vercel Dashboard**: Monitorea el rendimiento y errores
- **Analytics**: Ve las visitas y comportamiento de usuarios
- **Logs**: Revisa los logs de la aplicación en tiempo real

## Optimizaciones Futuras

### Posibles Mejoras
1. **Backend Separado**: Usar un servicio como Railway o Heroku para el script Python
2. **Base de Datos**: Integrar una base de datos para almacenar resultados
3. **Cache**: Implementar cache para mejorar rendimiento
4. **Autenticación**: Agregar sistema de usuarios

### Integración con Python Real
Para usar el script Python real en producción:
1. Crear un backend separado (Node.js/Python)
2. Modificar el endpoint para hacer peticiones al backend
3. Configurar CORS apropiadamente
4. Usar variables de entorno para las URLs

## Contacto

Si tienes problemas con el despliegue:
1. Revisa los logs en Vercel Dashboard
2. Verifica la configuración de archivos
3. Asegúrate de que el repositorio esté actualizado 