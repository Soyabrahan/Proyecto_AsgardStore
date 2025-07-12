# Integración del Script Python con el Frontend

Este documento explica cómo se ha integrado el script `predictive_trends.py` con el frontend de Next.js.

## Arquitectura

### 1. Endpoint API (`/pages/api/predictive-trends.ts`)
- **Ubicación**: `frontend/pages/api/predictive-trends.ts`
- **Función**: Ejecuta el script Python y devuelve los resultados como JSON
- **Método**: GET
- **URL**: `http://localhost:3000/api/predictive-trends`

### 2. Componente Frontend (`PredictiveTrends.tsx`)
- **Ubicación**: `frontend/components/PredictiveTrends.tsx`
- **Función**: Consume el endpoint API y muestra los resultados de forma visual
- **Características**:
  - Carga automática de datos al montar
  - Estados de carga y error
  - Botón para actualizar datos
  - Visualización estructurada de resultados

### 3. Script Python (`predictive_trends.py`)
- **Ubicación**: `frontend/scripts/predictive_trends.py`
- **Función**: Análisis predictivo de tendencias usando regresión lineal
- **Dependencias**: numpy, scikit-learn

## Cómo Funciona

### Flujo de Datos
1. El frontend hace una petición GET a `/api/predictive-trends`
2. El endpoint API ejecuta el script Python usando `child_process.spawn`
3. Se captura la salida del script (stdout y stderr)
4. Se procesa la salida para extraer información estructurada
5. Se devuelve una respuesta JSON con los resultados
6. El frontend recibe los datos y los muestra en la interfaz

### Estructura de la Respuesta API
```json
{
  "success": true,
  "output": "Salida completa del script Python",
  "results": {
    "summary": {
      "dataPoints": 100,
      "trainingSize": 80,
      "testSize": 20
    },
    "modelInfo": {
      "slope": 2.15,
      "intercept": 10.23,
      "mse": 225.67
    },
    "predictions": [
      {
        "time": 101,
        "predictedValue": 227.38
      },
      // ... más predicciones
    ]
  }
}
```

## Requisitos

### Software Necesario
- **Python 3.x** con las siguientes librerías:
  - numpy
  - scikit-learn
- **Node.js** (ya incluido en el proyecto)
- **Next.js** (ya configurado)

### Instalación de Dependencias Python
```bash
pip install numpy scikit-learn
```

## Uso

### 1. Ejecutar el Proyecto
```bash
cd frontend
npm run dev
```

### 2. Acceder a la Funcionalidad
- Navega a `http://localhost:3000`
- Desplázate hacia abajo hasta la sección "Análisis Predictivo de Tendencias"
- Los datos se cargan automáticamente
- Usa el botón "Actualizar" para ejecutar el análisis nuevamente

### 3. Probar el Endpoint Directamente
```bash
curl http://localhost:3000/api/predictive-trends
```

## Características del Componente

### Estados Visuales
- **Cargando**: Muestra un spinner mientras ejecuta el script
- **Error**: Muestra mensaje de error con botón para reintentar
- **Éxito**: Muestra los resultados organizados en tarjetas

### Información Mostrada
1. **Resumen del Modelo**: Puntos de datos, muestras de entrenamiento y prueba
2. **Información del Modelo**: Pendiente, intercepción y error cuadrático medio
3. **Predicciones Futuras**: Valores predichos para los próximos 10 períodos
4. **Salida Completa**: Texto completo generado por el script Python

## Personalización

### Modificar el Script Python
- Edita `frontend/scripts/predictive_trends.py`
- Ajusta los parámetros del modelo
- Cambia la cantidad de datos generados
- Modifica las predicciones futuras

### Modificar el Procesamiento
- Edita la función `parsePythonOutput` en el endpoint API
- Ajusta las expresiones regulares para extraer datos
- Agrega nuevos campos a la respuesta

### Modificar la Interfaz
- Edita `frontend/components/PredictiveTrends.tsx`
- Cambia el diseño de las tarjetas
- Agrega nuevas visualizaciones
- Modifica los colores y estilos

## Solución de Problemas

### Error: "python no se reconoce como comando"
- Asegúrate de que Python esté instalado y en el PATH
- En Windows, usa `python` o `python3`
- En Linux/Mac, usa `python3`

### Error: "ModuleNotFoundError"
- Instala las dependencias Python: `pip install numpy scikit-learn`
- Verifica que estés usando el entorno Python correcto

### Error: "Cannot find module 'next'"
- Instala las dependencias Node.js: `npm install`
- Verifica que estés en el directorio correcto

### El componente no se muestra
- Verifica que el servidor esté corriendo en `http://localhost:3000`
- Revisa la consola del navegador para errores
- Verifica que el endpoint API responda correctamente

## Seguridad

### Consideraciones
- El script Python se ejecuta en el servidor, no en el cliente
- Los errores del script se capturan y no exponen información sensible
- El endpoint solo acepta peticiones GET

### Mejoras Futuras
- Agregar autenticación al endpoint
- Implementar rate limiting
- Validar parámetros de entrada
- Cachear resultados para mejorar rendimiento

## Extensibilidad

### Agregar Nuevos Scripts
1. Crea un nuevo script Python en `frontend/scripts/`
2. Crea un nuevo endpoint API en `frontend/pages/api/`
3. Crea un nuevo componente React
4. Integra el componente en la página principal

### Agregar Parámetros
1. Modifica el endpoint para aceptar parámetros de query
2. Pasa los parámetros al script Python
3. Actualiza el componente para enviar parámetros
4. Agrega controles en la interfaz

## Contribución

Para contribuir a esta integración:
1. Mantén la compatibilidad con el script Python existente
2. Documenta cualquier cambio en la API
3. Prueba tanto el endpoint como el componente
4. Sigue las convenciones de código del proyecto 