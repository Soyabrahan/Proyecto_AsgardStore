# Asgard Store Frontend

Tienda de ropa con análisis predictivo de tendencias usando machine learning.

## 🚀 Despliegue en Vercel

### Configuración Automática

Este proyecto está configurado para desplegarse automáticamente en Vercel. Solo necesitas:

1. **Conectar tu repositorio** a Vercel
2. **Configurar el Root Directory** como: `Proyecto_AsgardStore/frontend`
3. **Hacer clic en Deploy**

### Configuración Manual

Si necesitas configurar manualmente:

| Campo | Valor |
|-------|-------|
| **Framework Preset** | `Next.js` |
| **Root Directory** | `Proyecto_AsgardStore/frontend` |
| **Build Command** | `npm run build` |
| **Output Directory** | `.next` |
| **Install Command** | `npm install` |

## 🛠️ Desarrollo Local

```bash
# Instalar dependencias
npm install

# Ejecutar en desarrollo
npm run dev

# Construir para producción
npm run build

# Iniciar servidor de producción
npm run start
```

## 📁 Estructura del Proyecto

```
frontend/
├── app/                    # App Router (Next.js 13+)
│   ├── layout.tsx         # Layout principal
│   ├── page.tsx           # Página principal
│   └── globals.css        # Estilos globales
├── components/            # Componentes React
│   ├── ui/               # Componentes de UI
│   └── PredictiveTrends.tsx # Componente de análisis
├── pages/                # Pages Router
│   └── api/              # API Routes
│       └── predictive-trends.ts
├── scripts/              # Scripts Python
│   └── predictive_trends.py
└── public/               # Archivos estáticos
```

## 🔧 Tecnologías

- **Next.js 15** - Framework de React
- **TypeScript** - Tipado estático
- **Tailwind CSS** - Framework de CSS
- **Radix UI** - Componentes de UI
- **Python** - Análisis predictivo (desarrollo local)

## 🌐 URLs

- **Desarrollo**: `http://localhost:3000`
- **API Endpoint**: `http://localhost:3000/api/predictive-trends`
- **Producción**: `https://tu-proyecto.vercel.app`

## 📊 Funcionalidades

### ✅ Desarrollo Local
- Script Python se ejecuta realmente
- Datos reales del análisis predictivo
- API endpoint funcional

### ✅ Producción (Vercel)
- Datos simulados que imitan la salida del script Python
- Misma interfaz visual y funcionalidad
- Nota informativa sobre datos simulados

## 🚨 Solución de Problemas

### Error: "Build Failed"
1. Verifica que estés en el directorio correcto
2. Ejecuta `npm run build` localmente
3. Revisa los logs en Vercel Dashboard

### Error: "Page Not Found"
1. Asegúrate de que el Root Directory sea: `Proyecto_AsgardStore/frontend`
2. Verifica que el archivo `package.json` esté en ese directorio

### Error: "API Route Not Found"
1. Verifica que el archivo esté en `pages/api/predictive-trends.ts`
2. Asegúrate de que el método sea GET

## 📈 Monitoreo

- **Vercel Dashboard**: Monitorea el rendimiento y errores
- **Analytics**: Ve las visitas y comportamiento de usuarios
- **Logs**: Revisa los logs de la aplicación en tiempo real

## 🔄 Actualizaciones

Los cambios se despliegan automáticamente al hacer push a GitHub.

---

**Estado**: ✅ Listo para despliegue
**Framework**: Next.js 15
**Node.js**: >=18.0.0
