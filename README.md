# Asgard Store

Asgard Store es una tienda online inspirada en la cultura Geek, donde puedes encontrar ropa y accesorios únicos para expresar tu estilo. El proyecto está dividido en dos partes principales: **frontend** y **backend**.

---

## Frontend

El frontend está desarrollado con Next.js, Tailwind CSS y componentes modernos para una experiencia visual atractiva y responsiva.

### Tecnologías principales
- **Next.js** (App Router)
- **React**
- **Tailwind CSS**
- **shadcn/ui** (componentes UI)
- **TypeScript**
- **pnpm** (gestor de paquetes)

### Características
- Página de inicio con animaciones y diseño responsivo
- Secciones de colecciones populares y nuevos lanzamientos
- Búsqueda y navegación optimizadas
- Estilos modernos y personalizables

### Instalación local del frontend

1. Clona el repositorio:
   ```bash
   git clone https://github.com/Soyabrahan/Proyecto_AsgardStore.git
   cd Proyecto_AsgardStore/frontend
   ```
2. Instala las dependencias:
   ```bash
   pnpm install
   # o
   npm install
   ```
3. Corre el servidor de desarrollo:
   ```bash
   pnpm run dev
   # o
   npm run dev
   ```
4. Abre [http://localhost:3000](http://localhost:3000) en tu navegador.

### Despliegue en producción

El frontend está desplegado en Render y puedes verlo en:

👉 [https://proyecto-asgardstore.onrender.com](https://proyecto-asgardstore.onrender.com)

---

## Backend

El backend está pensado para gestionar la lógica de negocio, la autenticación, la base de datos y la API que consume el frontend.

### Tecnologías principales
- **Python**
- **FastAPI** (o Flask/Django, según tu implementación)
- **Base de datos relacional** (por ejemplo, PostgreSQL o MySQL)
- **ORM** (por ejemplo, SQLAlchemy)
- **Autenticación y autorización**
- **Despliegue preparado para Render o cualquier servicio compatible con Python**

### Características
- Endpoints RESTful para productos, usuarios, pedidos, etc.
- Gestión de usuarios y autenticación segura
- Integración con base de datos
- Documentación automática de la API (por ejemplo, Swagger con FastAPI)
- Preparado para despliegue en la nube

### Instalación local del backend

1. Entra a la carpeta backend:
   ```bash
   cd Proyecto_AsgardStore/backend
   ```
2. Crea un entorno virtual e instala las dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Corre el servidor de desarrollo:
   ```bash
   uvicorn app.main:app --reload
   ```
   (Ajusta el comando según tu estructura de archivos.)

4. La API estará disponible en [http://localhost:8000](http://localhost:8000)

---

## Autores

- Abrahan Ramirez
- Richard Suarez
- Alberto Williams
- Jesus Merlin

---

## Licencia

Este proyecto es solo para fines educativos y de demostración.
