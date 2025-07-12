import { NextApiRequest, NextApiResponse } from 'next';
import { spawn } from 'child_process';
import path from 'path';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // En producción (Vercel), usar datos simulados ya que Python no está disponible
    if (process.env.NODE_ENV === 'production') {
      const simulatedResults = generateSimulatedResults();
      
      res.status(200).json({
        success: true,
        output: simulatedResults.output,
        results: simulatedResults.results,
        note: "Datos simulados - Python no disponible en producción"
      });
      return;
    }

    // En desarrollo, ejecutar el script Python
    const scriptPath = path.join(process.cwd(), 'scripts', 'predictive_trends.py');
    
    // Ejecutar el script Python
    const pythonProcess = spawn('python', [scriptPath]);
    
    let output = '';
    let errorOutput = '';

    // Capturar la salida estándar
    pythonProcess.stdout.on('data', (data: Buffer) => {
      output += data.toString();
    });

    // Capturar errores
    pythonProcess.stderr.on('data', (data: Buffer) => {
      errorOutput += data.toString();
    });

    // Esperar a que termine el proceso
    return new Promise<void>((resolve) => {
      pythonProcess.on('close', (code: number) => {
        if (code !== 0) {
          console.error('Error ejecutando script Python:', errorOutput);
          res.status(500).json({ 
            error: 'Error ejecutando el análisis predictivo',
            details: errorOutput 
          });
          resolve();
        } else {
          // Procesar la salida para extraer información estructurada
          const results = parsePythonOutput(output);
          
          res.status(200).json({
            success: true,
            output: output,
            results: results
          });
          resolve();
        }
      });
    });

  } catch (error) {
    console.error('Error en el endpoint:', error);
    res.status(500).json({ 
      error: 'Error interno del servidor',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}

function parsePythonOutput(output: string) {
  const lines = output.split('\n');
  const results: any = {
    summary: {},
    predictions: [],
    modelInfo: {}
  };

  for (const line of lines) {
    // Extraer información del modelo
    if (line.includes('Coeficiente (pendiente):')) {
      const match = line.match(/Coeficiente \(pendiente\): ([\d.-]+)/);
      if (match) results.modelInfo.slope = parseFloat(match[1]);
    }
    
    if (line.includes('Intercepción:')) {
      const match = line.match(/Intercepción: ([\d.-]+)/);
      if (match) results.modelInfo.intercept = parseFloat(match[1]);
    }
    
    if (line.includes('Error cuadrático medio (MSE):')) {
      const match = line.match(/Error cuadrático medio \(MSE\) en el conjunto de prueba: ([\d.-]+)/);
      if (match) results.modelInfo.mse = parseFloat(match[1]);
    }
    
    // Extraer predicciones futuras
    if (line.includes('Tiempo') && line.includes('Tendencia predicha =')) {
      const match = line.match(/Tiempo (\d+): Tendencia predicha = ([\d.-]+)/);
      if (match) {
        results.predictions.push({
          time: parseInt(match[1]),
          predictedValue: parseFloat(match[2])
        });
      }
    }
    
    // Extraer información de datos
    if (line.includes('Datos generados:')) {
      const match = line.match(/Datos generados: (\d+) puntos de tiempo/);
      if (match) results.summary.dataPoints = parseInt(match[1]);
    }
    
    if (line.includes('Tamaño del conjunto de entrenamiento:')) {
      const match = line.match(/Tamaño del conjunto de entrenamiento: (\d+) muestras/);
      if (match) results.summary.trainingSize = parseInt(match[1]);
    }
    
    if (line.includes('Tamaño del conjunto de prueba:')) {
      const match = line.match(/Tamaño del conjunto de prueba: (\d+) muestras/);
      if (match) results.summary.testSize = parseInt(match[1]);
    }
  }

  return results;
}

function generateSimulatedResults() {
  // Generar datos simulados que imiten la salida del script Python
  const output = `Iniciando análisis predictivo de tendencias...
Datos generados: 100 puntos de tiempo.
Primeros 5 puntos de tiempo: [1 2 3 4 5]
Primeros 5 valores de tendencia: [12.5 14.8 17.2 19.1 21.3]
Tamaño del conjunto de entrenamiento: 80 muestras
Tamaño del conjunto de prueba: 20 muestras

Modelo de regresión lineal entrenado.
Coeficiente (pendiente): 2.15
Intercepción: 10.23

Error cuadrático medio (MSE) en el conjunto de prueba: 225.67

Predicciones de tendencias futuras:
Tiempo 101: Tendencia predicha = 227.38
Tiempo 102: Tendencia predicha = 229.53
Tiempo 103: Tendencia predicha = 231.68
Tiempo 104: Tendencia predicha = 233.83
Tiempo 105: Tendencia predicha = 235.98
Tiempo 106: Tendencia predicha = 238.13
Tiempo 107: Tendencia predicha = 240.28
Tiempo 108: Tendencia predicha = 242.43
Tiempo 109: Tendencia predicha = 244.58
Tiempo 110: Tendencia predicha = 246.73

Análisis predictivo completado.`;

  const results = {
    summary: {
      dataPoints: 100,
      trainingSize: 80,
      testSize: 20
    },
    modelInfo: {
      slope: 2.15,
      intercept: 10.23,
      mse: 225.67
    },
    predictions: [
      { time: 101, predictedValue: 227.38 },
      { time: 102, predictedValue: 229.53 },
      { time: 103, predictedValue: 231.68 },
      { time: 104, predictedValue: 233.83 },
      { time: 105, predictedValue: 235.98 },
      { time: 106, predictedValue: 238.13 },
      { time: 107, predictedValue: 240.28 },
      { time: 108, predictedValue: 242.43 },
      { time: 109, predictedValue: 244.58 },
      { time: 110, predictedValue: 246.73 }
    ]
  };

  return { output, results };
} 