# AsgardStore Frontend

Frontend moderno para AsgardStore construido con Next.js 15, TypeScript, Tailwind CSS v4 y Framer Motion.

## 🚀 Características

- **Next.js 15** con App Router
- **TypeScript** con configuración estricta
- **Tailwind CSS v4** con variables CSS modernas
- **Framer Motion v11** para animaciones fluidas
- **shadcn/ui** para componentes UI consistentes
- **Axios** para integración con API
- **Lucide React** para iconos
- **Responsive Design** optimizado para móviles

## 📦 Dependencias Principales

```json
{
  "@radix-ui/react-label": "^2.1.7",
  "@radix-ui/react-slot": "^1.2.3",
  "axios": "^1.10.0",
  "class-variance-authority": "^0.7.1",
  "clsx": "^2.1.1",
  "framer-motion": "^11.0.0",
  "lucide-react": "^0.523.0",
  "next": "15.3.4",
  "react": "^19.0.0",
  "tailwind-merge": "^3.3.1"
}
```

## 🏗️ Estructura del Proyecto

```
frontend/
├── src/
│   ├── app/
│   │   ├── dashboard/
│   │   │   └── page.tsx          # Página del dashboard
│   │   ├── globals.css           # Estilos globales con Tailwind v4
│   │   ├── layout.tsx            # Layout principal
│   │   └── page.tsx              # Página principal
│   ├── components/
│   │   ├── animations.tsx        # Componentes de animación con Framer Motion
│   │   ├── AsgardDashboard.tsx   # Dashboard principal
│   │   └── ui/                   # Componentes UI de shadcn/ui
│   │       ├── badge.tsx
│   │       ├── button.tsx
│   │       ├── card.tsx
│   │       └── input.tsx
│   ├── hooks/
│   │   └── useInView.ts          # Hook para detectar elementos en viewport
│   ├── lib/
│   │   ├── api.ts                # Configuración de Axios y funciones API
│   │   └── utils.ts              # Utilidades (función cn)
│   └── utils/                    # Utilidades adicionales
├── components.json               # Configuración de shadcn/ui
├── tailwind.config.ts            # Configuración de Tailwind CSS v4
├── postcss.config.mjs            # Configuración de PostCSS
└── package.json
```

## 🎨 Configuración de Estilos

### Tailwind CSS v4

- Uso de `@import "tailwindcss"` en lugar de directivas
- Variables CSS modernas con `oklch()`
- Configuración con `@theme inline`
- Soporte para modo oscuro automático

### Componentes UI

- **shadcn/ui** con estilo "new-york"
- Componentes accesibles y consistentes
- Variantes usando `class-variance-authority`
- Integración con sistema de colores

## 🎭 Animaciones

### Framer Motion v11

- Tipado explícito con `HTMLMotionProps`
- Variantes de animación reutilizables
- Animaciones de scroll optimizadas
- Hooks personalizados para animaciones

### Componentes de Animación

- `AnimatedDiv`: Componente base para animaciones
- `StaggerContainer`: Contenedor con animaciones escalonadas
- `useScrollAnimation`: Hook para animaciones de scroll
- Variantes predefinidas: `fadeInUp`, `fadeInDown`, `scaleIn`, etc.

## 🔌 Integración con API

### Axios Configuration

- Interceptores para autenticación
- Manejo global de errores
- Timeout configurado
- Headers automáticos

### Funciones API

- `productAPI`: Gestión de productos
- `authAPI`: Autenticación de usuarios
- `orderAPI`: Gestión de órdenes

## 🚀 Scripts Disponibles

```bash
# Desarrollo
npm run dev

# Construcción
npm run build

# Producción
npm run start

# Linting
npm run lint
```

## 📱 Responsive Design

- Diseño mobile-first
- Breakpoints optimizados
- Animaciones adaptadas para móviles
- Performance optimizada para dispositivos móviles

## 🎯 Puntos Clave

1. **Configuración Moderna**: Tailwind CSS v4 con variables CSS modernas
2. **Animaciones Fluidas**: Framer Motion v11 con tipado explícito
3. **Componentes Reutilizables**: shadcn/ui con variantes consistentes
4. **API Integration**: Axios con interceptores y manejo de errores
5. **Performance**: Optimizaciones para móviles y accesibilidad
6. **TypeScript**: Configuración estricta con paths aliases

## 🔧 Configuración de Desarrollo

1. Instalar dependencias: `npm install`
2. Configurar variables de entorno (si es necesario)
3. Ejecutar en desarrollo: `npm run dev`
4. Acceder a `http://localhost:3000`

## 📄 Licencia

Este proyecto es parte de AsgardStore y sigue las mejores prácticas de desarrollo moderno.
