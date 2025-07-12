import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def analyze_and_predict_trends():
    """
    Simula el análisis predictivo de tendencias utilizando un modelo de regresión lineal.
    Genera datos de tendencias sintéticos y predice valores futuros.
    """
    print("Iniciando análisis predictivo de tendencias...")

    # 1. Generar datos de tendencias sintéticos
    # Supongamos que 'tiempo' es la variable independiente (ej. días, semanas)
    # y 'tendencia' es la variable dependiente (ej. volumen de ventas, popularidad)
    np.random.seed(42) # Para reproducibilidad
    tiempo = np.arange(1, 101).reshape(-1, 1) # 100 puntos de tiempo
    # Una tendencia general creciente con algo de ruido
    tendencia = 2 * tiempo + 10 + np.random.normal(0, 15, tiempo.shape)

    print(f"Datos generados: {len(tiempo)} puntos de tiempo.")
    print(f"Primeros 5 puntos de tiempo: {tiempo[:5].flatten()}")
    print(f"Primeros 5 valores de tendencia: {tendencia[:5].flatten()}")

    # 2. Dividir los datos en conjuntos de entrenamiento y prueba
    # Usaremos el 80% para entrenar y el 20% para probar
    X_train, X_test, y_train, y_test = train_test_split(tiempo, tendencia, test_size=0.2, random_state=42)

    print(f"Tamaño del conjunto de entrenamiento: {len(X_train)} muestras")
    print(f"Tamaño del conjunto de prueba: {len(X_test)} muestras")

    # 3. Entrenar un modelo de regresión lineal
    model = LinearRegression()
    model.fit(X_train, y_train)

    print("\nModelo de regresión lineal entrenado.")
    print(f"Coeficiente (pendiente): {model.coef_[0][0]:.2f}")
    print(f"Intercepción: {model.intercept_[0]:.2f}")

    # 4. Evaluar el modelo con el conjunto de prueba
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"\nError cuadrático medio (MSE) en el conjunto de prueba: {mse:.2f}")

    # 5. Realizar predicciones para el futuro
    # Predicciones para los próximos 10 puntos de tiempo después de los datos existentes
    futuro_tiempo = np.arange(101, 111).reshape(-1, 1)
    predicciones_futuras = model.predict(futuro_tiempo)

    print("\nPredicciones de tendencias futuras:")
    for i, (tiempo_futuro, prediccion) in enumerate(zip(futuro_tiempo, predicciones_futuras)):
        print(f"Tiempo {tiempo_futuro[0]}: Tendencia predicha = {prediccion[0]:.2f}")

    print("\nAnálisis predictivo completado.")

# Ejecutar la función
if __name__ == "__main__":
    analyze_and_predict_trends()
