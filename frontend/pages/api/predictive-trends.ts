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
    // Ruta al script Python
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