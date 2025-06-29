# Backend - Análisis Predictivo de Tendencias con IA

## ¿Qué hace este sistema?

Este backend implementa un **Sistema de Análisis Predictivo de Tendencias con Inteligencia Artificial** para AsgardStore. Su función principal es:

### 🎯 **Identificación de Tendencias**
- Analiza datos históricos de ventas, búsquedas y comportamiento del usuario
- Identifica qué productos o estilos están en tendencia ascendente
- Detecta patrones estacionales y ciclos de popularidad

### 📊 **Predicción de Demanda**
- Utiliza algoritmos de machine learning para predecir futuras tendencias
- Analiza sentimientos en redes sociales y reseñas de productos
- Proporciona recomendaciones basadas en datos para optimizar inventario

### 💡 **Sugerencias Estratégicas**
- Sugiere al negocio qué productos promocionar en cada temporada
- Recomienda estrategias de precios basadas en tendencias
- Identifica oportunidades de mercado emergentes

## Características Principales

### 🤖 **Algoritmos de IA Implementados**
- **Análisis de Series Temporales**: Predicción de tendencias usando LSTM y Prophet
- **Análisis de Sentimientos**: Procesamiento de lenguaje natural para reseñas
- **Clustering de Productos**: Agrupación inteligente por características similares
- **Recomendación Personalizada**: Sistema de recomendaciones basado en colaboración

### 📈 **Métricas Analizadas**
- Volumen de ventas por categoría
- Tendencias de búsqueda en tiempo real
- Sentimiento de reseñas de clientes
- Patrones estacionales y cíclicos
- Competencia y precios del mercado

### 🔮 **Predicciones Generadas**
- Productos con mayor potencial de crecimiento
- Temporadas óptimas para lanzamientos
- Precios recomendados basados en elasticidad
- Estrategias de marketing personalizadas

## Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # API FastAPI principal
│   ├── models/                 # Modelos de datos Pydantic
│   ├── services/               # Lógica de negocio
│   │   ├── trend_analyzer.py   # Análisis de tendencias
│   │   ├── sentiment_analyzer.py # Análisis de sentimientos
│   │   ├── prediction_engine.py # Motor de predicciones
│   │   └── recommendation_system.py # Sistema de recomendaciones
│   ├── utils/                  # Utilidades y helpers
│   └── data/                   # Datos de ejemplo y modelos entrenados
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Este archivo
└── .env.example               # Variables de entorno de ejemplo
```

## Instalación y Uso

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

### 3. Ejecutar el servidor
```bash
uvicorn app.main:app --reload
```

### 4. Acceder a la documentación
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints Principales

### 📊 **Análisis de Tendencias**
- `GET /api/trends/current` - Tendencias actuales
- `GET /api/trends/prediction` - Predicciones futuras
- `POST /api/trends/analyze` - Análisis personalizado

### 🎯 **Recomendaciones**
- `GET /api/recommendations/products` - Productos recomendados
- `GET /api/recommendations/promotions` - Estrategias de promoción
- `POST /api/recommendations/custom` - Recomendaciones personalizadas

### 📈 **Métricas y Reportes**
- `GET /api/metrics/sales` - Métricas de ventas
- `GET /api/metrics/sentiment` - Análisis de sentimientos
- `GET /api/reports/trends` - Reportes de tendencias

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido
- **TensorFlow/PyTorch**: Deep Learning para predicciones
- **Scikit-learn**: Machine Learning tradicional
- **Pandas/Numpy**: Manipulación y análisis de datos
- **NLTK/Transformers**: Procesamiento de lenguaje natural
- **Plotly/Matplotlib**: Visualización de datos
- **Prophet**: Análisis de series temporales

## Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 