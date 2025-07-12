'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';

interface Prediction {
  time: number;
  predictedValue: number;
}

interface ModelInfo {
  slope: number;
  intercept: number;
  mse: number;
}

interface Summary {
  dataPoints: number;
  trainingSize: number;
  testSize: number;
}

interface ApiResponse {
  success: boolean;
  output: string;
  results: {
    summary: Summary;
    predictions: Prediction[];
    modelInfo: ModelInfo;
  };
}

export default function PredictiveTrends() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchPredictiveData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/predictive-trends');
      const result = await response.json();
      
      if (response.ok) {
        setData(result);
      } else {
        setError(result.error || 'Error al obtener datos predictivos');
      }
    } catch (err) {
      setError('Error de conexión');
      console.error('Error fetching predictive data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Cargar datos automáticamente al montar el componente
    fetchPredictiveData();
  }, []);

  if (loading) {
    return (
      <Card className="w-full">
        <CardHeader>
          <CardTitle>Análisis Predictivo de Tendencias</CardTitle>
          <CardDescription>Ejecutando análisis...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="w-full">
        <CardHeader>
          <CardTitle>Análisis Predictivo de Tendencias</CardTitle>
          <CardDescription>Error en el análisis</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-red-600 mb-4">{error}</div>
          <Button onClick={fetchPredictiveData} className="border border-input bg-background hover:bg-accent hover:text-accent-foreground">
            Reintentar
          </Button>
        </CardContent>
      </Card>
    );
  }

  if (!data) {
    return null;
  }

  const { results } = data;

  return (
    <div className="space-y-6">
      <Card className="w-full">
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            Análisis Predictivo de Tendencias
            <Button onClick={fetchPredictiveData} className="border border-input bg-background hover:bg-accent hover:text-accent-foreground h-9 rounded-md px-3">
              Actualizar
            </Button>
          </CardTitle>
          <CardDescription>
            Modelo de regresión lineal para predecir tendencias futuras
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Resumen del modelo */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <CardContent className="pt-6">
                <div className="text-2xl font-bold">{results.summary.dataPoints}</div>
                <p className="text-xs text-muted-foreground">Puntos de datos</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-2xl font-bold">{results.summary.trainingSize}</div>
                <p className="text-xs text-muted-foreground">Muestras de entrenamiento</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-2xl font-bold">{results.summary.testSize}</div>
                <p className="text-xs text-muted-foreground">Muestras de prueba</p>
              </CardContent>
            </Card>
          </div>

          {/* Información del modelo */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Información del Modelo</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <p className="text-sm font-medium">Pendiente (Coeficiente)</p>
                  <p className="text-2xl font-bold text-blue-600">
                    {results.modelInfo.slope?.toFixed(2) || 'N/A'}
                  </p>
                </div>
                <div>
                  <p className="text-sm font-medium">Intercepción</p>
                  <p className="text-2xl font-bold text-green-600">
                    {results.modelInfo.intercept?.toFixed(2) || 'N/A'}
                  </p>
                </div>
                <div>
                  <p className="text-sm font-medium">Error Cuadrático Medio (MSE)</p>
                  <p className="text-2xl font-bold text-orange-600">
                    {results.modelInfo.mse?.toFixed(2) || 'N/A'}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Predicciones futuras */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Predicciones Futuras</CardTitle>
              <CardDescription>
                Valores predichos para los próximos 10 períodos
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                {results.predictions.map((prediction, index) => (
                  <div key={index} className="text-center p-3 border rounded-lg">
                    <div className="text-sm text-muted-foreground">Tiempo {prediction.time}</div>
                    <div className="text-lg font-bold text-purple-600">
                      {prediction.predictedValue.toFixed(1)}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Salida completa del script */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Salida Completa del Script</CardTitle>
            </CardHeader>
            <CardContent>
              <pre className="bg-gray-100 p-4 rounded-lg text-sm overflow-x-auto">
                {data.output}
              </pre>
            </CardContent>
          </Card>
        </CardContent>
      </Card>
    </div>
  );
} 