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
  note?: string;
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
      <Card className="w-full bg-[#2e2447] border-[#2e2447] text-white">
        <CardHeader>
          <CardTitle className="text-white">Análisis Predictivo de Tendencias</CardTitle>
          <CardDescription className="text-[#a394c7]">Ejecutando análisis...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#7847eb]"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="w-full bg-[#2e2447] border-[#2e2447] text-white">
        <CardHeader>
          <CardTitle className="text-white">Análisis Predictivo de Tendencias</CardTitle>
          <CardDescription className="text-[#a394c7]">Error en el análisis</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-red-400 mb-4">{error}</div>
          <Button 
            onClick={fetchPredictiveData} 
            className="bg-[#7847eb] hover:bg-[#7847eb]/90 text-white border-[#7847eb]"
          >
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
      <Card className="w-full bg-[#2e2447] border-[#2e2447] text-white">
        <CardHeader>
          <CardTitle className="flex items-center justify-between text-white">
            Análisis Predictivo de Tendencias
            <Button 
              onClick={fetchPredictiveData} 
              className="bg-[#7847eb] hover:bg-[#7847eb]/90 text-white border-[#7847eb] h-9 rounded-md px-3"
            >
              Actualizar
            </Button>
          </CardTitle>
          <CardDescription className="text-[#a394c7]">
            Modelo de regresión lineal para predecir tendencias futuras
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Resumen del modelo */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card className="bg-[#1a1a2e] border-[#2e2447]">
              <CardContent className="pt-6">
                <div className="text-2xl font-bold text-white">{results.summary.dataPoints}</div>
                <p className="text-xs text-[#a394c7]">Puntos de datos</p>
              </CardContent>
            </Card>
            <Card className="bg-[#1a1a2e] border-[#2e2447]">
              <CardContent className="pt-6">
                <div className="text-2xl font-bold text-white">{results.summary.trainingSize}</div>
                <p className="text-xs text-[#a394c7]">Muestras de entrenamiento</p>
              </CardContent>
            </Card>
            <Card className="bg-[#1a1a2e] border-[#2e2447]">
              <CardContent className="pt-6">
                <div className="text-2xl font-bold text-white">{results.summary.testSize}</div>
                <p className="text-xs text-[#a394c7]">Muestras de prueba</p>
              </CardContent>
            </Card>
          </div>

          {/* Información del modelo */}
          <Card className="bg-[#1a1a2e] border-[#2e2447]">
            <CardHeader>
              <CardTitle className="text-lg text-white">Información del Modelo</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <p className="text-sm font-medium text-[#a394c7]">Pendiente (Coeficiente)</p>
                  <p className="text-2xl font-bold text-cyan-400">
                    {results.modelInfo.slope?.toFixed(2) || 'N/A'}
                  </p>
                </div>
                <div>
                  <p className="text-sm font-medium text-[#a394c7]">Intercepción</p>
                  <p className="text-2xl font-bold text-green-400">
                    {results.modelInfo.intercept?.toFixed(2) || 'N/A'}
                  </p>
                </div>
                <div>
                  <p className="text-sm font-medium text-[#a394c7]">Error Cuadrático Medio (MSE)</p>
                  <p className="text-2xl font-bold text-orange-400">
                    {results.modelInfo.mse?.toFixed(2) || 'N/A'}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Predicciones futuras */}
          <Card className="bg-[#1a1a2e] border-[#2e2447]">
            <CardHeader>
              <CardTitle className="text-lg text-white">Predicciones Futuras</CardTitle>
              <CardDescription className="text-[#a394c7]">
                Valores predichos para los próximos 10 períodos
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                {results.predictions.map((prediction, index) => (
                  <div key={index} className="text-center p-3 border border-[#2e2447] rounded-lg bg-[#171221]">
                    <div className="text-sm text-[#a394c7]">Tiempo {prediction.time}</div>
                    <div className="text-lg font-bold text-[#7847eb]">
                      {prediction.predictedValue.toFixed(1)}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Salida completa del script */}
          <Card className="bg-[#1a1a2e] border-[#2e2447]">
            <CardHeader>
              <CardTitle className="text-lg text-white">Salida Completa del Script</CardTitle>
            </CardHeader>
            <CardContent>
              <pre className="bg-[#171221] p-4 rounded-lg text-sm overflow-x-auto text-[#a394c7] border border-[#2e2447]">
                {data.output}
              </pre>
            </CardContent>
          </Card>

          {/* Nota sobre datos simulados */}
          {data.note && (
            <Card className="border-[#7847eb]/30 bg-[#7847eb]/10">
              <CardContent className="pt-6">
                <div className="flex items-center space-x-2 text-[#7847eb]">
                  <div className="w-2 h-2 bg-[#7847eb] rounded-full"></div>
                  <p className="text-sm">{data.note}</p>
                </div>
              </CardContent>
            </Card>
          )}
        </CardContent>
      </Card>
    </div>
  );
} 