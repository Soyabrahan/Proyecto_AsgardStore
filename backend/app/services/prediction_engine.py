"""
Motor de Predicciones
Implementa algoritmos de machine learning para predecir tendencias futuras
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import uuid

logger = logging.getLogger(__name__)

class PredictionEngine:
    """Motor de predicciones con algoritmos de ML"""
    
    def __init__(self):
        self.models = {
            'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'gradient_boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'linear_regression': LinearRegression()
        }
        self.scaler = StandardScaler()
        self.trained_models = {}
        self.sample_data = self._generate_sample_data()
        
    def _generate_sample_data(self) -> pd.DataFrame:
        """Generar datos de ejemplo para entrenamiento"""
        np.random.seed(42)
        
        # Generar datos históricos más complejos
        data = []
        base_date = datetime.now() - timedelta(days=730)  # 2 años de datos
        
        # Productos de ejemplo
        products = [
            "Smartphone Galaxy S24", "iPhone 15 Pro", "Laptop Dell XPS", 
            "Nike Air Max", "Adidas Ultraboost", "Samsung TV 4K",
            "Sony Headphones", "MacBook Pro", "iPad Air", "Apple Watch"
        ]
        
        categories = ["electronics"] * 6 + ["sports"] * 4
        
        for i, (product, category) in enumerate(zip(products, categories)):
            # Generar datos históricos para cada producto
            for day in range(730):
                date = base_date + timedelta(days=day)
                
                # Factores que influyen en las ventas
                day_of_week = date.weekday()
                month = date.month
                day_of_year = date.timetuple().tm_yday
                
                # Tendencia base
                base_trend = 1 + 0.05 * (day / 730)  # Tendencia general creciente
                
                # Estacionalidad
                seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * day_of_year / 365)
                
                # Patrones semanales
                weekly_pattern = 1 + 0.2 * np.sin(2 * np.pi * day_of_week / 7)
                
                # Patrones por categoría
                if category == "electronics":
                    tech_cycle = 1 + 0.15 * np.sin(2 * np.pi * day / 90)  # Ciclos de 3 meses
                    base_sales = 100 + i * 15
                    price_factor = 1 + 0.1 * np.sin(2 * np.pi * day / 180)  # Cambios de precio
                else:  # sports
                    sports_season = 1 + 0.4 * np.sin(2 * np.pi * day_of_year / 365)
                    base_sales = 80 + i * 12
                    price_factor = 1 + 0.05 * np.sin(2 * np.pi * day / 120)
                
                # Eventos especiales (simulados)
                event_factor = 1.0
                if month == 12:  # Navidad
                    event_factor = 1.5
                elif month == 11:  # Black Friday
                    event_factor = 1.8
                elif month == 6:  # Verano
                    event_factor = 1.2
                
                # Ruido aleatorio
                noise = np.random.normal(0, 0.1)
                
                # Calcular ventas finales
                if category == "electronics":
                    sales = int(base_sales * base_trend * seasonal_factor * weekly_pattern * 
                               tech_cycle * price_factor * event_factor * (1 + noise))
                else:
                    sales = int(base_sales * base_trend * seasonal_factor * weekly_pattern * 
                               sports_season * price_factor * event_factor * (1 + noise))
                
                # Otras métricas
                search_volume = int(sales * np.random.uniform(8, 40))
                price = np.random.uniform(50, 800)
                sentiment = np.random.uniform(-0.3, 0.7)
                competitor_price = price * np.random.uniform(0.8, 1.2)
                marketing_spend = np.random.uniform(100, 1000)
                
                # Features para ML
                data.append({
                    'date': date,
                    'product_id': f'prod_{i:03d}',
                    'product_name': product,
                    'category': category,
                    'sales': max(0, sales),
                    'search_volume': max(0, search_volume),
                    'price': price,
                    'sentiment_score': sentiment,
                    'competitor_price': competitor_price,
                    'marketing_spend': marketing_spend,
                    'day_of_week': day_of_week,
                    'month': month,
                    'day_of_year': day_of_year,
                    'is_weekend': 1 if day_of_week >= 5 else 0,
                    'is_holiday': 1 if month in [12, 11, 6] else 0,
                    'price_competitiveness': price / competitor_price,
                    'search_to_sales_ratio': search_volume / max(1, sales)
                })
        
        return pd.DataFrame(data)
    
    async def predict_trends(self, days_ahead: int = 30, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Predecir tendencias futuras"""
        try:
            # Filtrar datos por categoría si se especifica
            if category:
                data = self.sample_data[self.sample_data['category'] == category].copy()
            else:
                data = self.sample_data.copy()
            
            predictions = []
            
            # Predecir para cada producto
            for product_id in data['product_id'].unique():
                product_data = data[data['product_id'] == product_id]
                
                if len(product_data) < 60:  # Necesitamos al menos 2 meses de datos
                    continue
                
                # Entrenar modelo para este producto
                model = await self._train_product_model(product_data)
                
                if model is None:
                    continue
                
                # Generar features para predicción
                future_features = self._generate_future_features(product_data, days_ahead)
                
                # Hacer predicciones
                predicted_sales = model.predict(future_features)
                
                # Calcular métricas de confianza
                confidence = self._calculate_prediction_confidence(model, product_data)
                
                # Generar análisis de la predicción
                prediction_analysis = self._analyze_prediction(product_data, predicted_sales, days_ahead)
                
                product_info = product_data.iloc[0]
                
                predictions.append({
                    'product_id': product_id,
                    'product_name': product_info['product_name'],
                    'category': product_info['category'],
                    'prediction_period': days_ahead,
                    'predicted_sales': [max(0, int(sale)) for sale in predicted_sales],
                    'confidence_level': round(confidence, 3),
                    'predicted_growth': round(prediction_analysis['growth_rate'], 2),
                    'trend_direction': prediction_analysis['trend_direction'],
                    'seasonal_factors': prediction_analysis['seasonal_factors'],
                    'risk_factors': prediction_analysis['risk_factors'],
                    'recommendations': prediction_analysis['recommendations'],
                    'model_used': model.__class__.__name__,
                    'prediction_date': datetime.now().isoformat()
                })
            
            # Ordenar por confianza y crecimiento esperado
            predictions.sort(key=lambda x: (x['confidence_level'], x['predicted_growth']), reverse=True)
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error prediciendo tendencias: {e}")
            raise
    
    async def predict_demand(self, product_id: str, days_ahead: int = 30) -> Dict[str, Any]:
        """Predecir demanda específica para un producto"""
        try:
            product_data = self.sample_data[self.sample_data['product_id'] == product_id].copy()
            
            if product_data.empty:
                raise ValueError(f"No se encontraron datos para el producto {product_id}")
            
            if len(product_data) < 30:
                raise ValueError("Se necesitan al menos 30 días de datos históricos")
            
            # Entrenar modelo específico
            model = await self._train_product_model(product_data)
            
            if model is None:
                raise ValueError("No se pudo entrenar el modelo para este producto")
            
            # Generar features futuras
            future_features = self._generate_future_features(product_data, days_ahead)
            
            # Predicciones
            predicted_sales = model.predict(future_features)
            predicted_sales = [max(0, int(sale)) for sale in predicted_sales]
            
            # Análisis detallado
            analysis = self._analyze_demand_prediction(product_data, predicted_sales, days_ahead)
            
            # Calcular intervalos de confianza
            confidence_intervals = self._calculate_confidence_intervals(predicted_sales, model, product_data)
            
            product_info = product_data.iloc[0]
            
            return {
                'product_id': product_id,
                'product_name': product_info['product_name'],
                'category': product_info['category'],
                'prediction_period': days_ahead,
                'predicted_demand': predicted_sales,
                'total_predicted_sales': sum(predicted_sales),
                'average_daily_demand': round(np.mean(predicted_sales), 2),
                'peak_demand_day': np.argmax(predicted_sales) + 1,
                'peak_demand_value': max(predicted_sales),
                'confidence_intervals': confidence_intervals,
                'trend_analysis': analysis['trend_analysis'],
                'seasonal_patterns': analysis['seasonal_patterns'],
                'risk_assessment': analysis['risk_assessment'],
                'inventory_recommendations': analysis['inventory_recommendations'],
                'model_performance': analysis['model_performance'],
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error prediciendo demanda: {e}")
            raise
    
    async def predict_market_trends(self, category: str, months_ahead: int = 6) -> Dict[str, Any]:
        """Predecir tendencias del mercado para una categoría"""
        try:
            category_data = self.sample_data[self.sample_data['category'] == category].copy()
            
            if category_data.empty:
                raise ValueError(f"No se encontraron datos para la categoría {category}")
            
            # Agregar datos por día para toda la categoría
            daily_data = category_data.groupby('date').agg({
                'sales': 'sum',
                'search_volume': 'sum',
                'price': 'mean',
                'sentiment_score': 'mean',
                'marketing_spend': 'sum'
            }).reset_index()
            
            # Entrenar modelo para la categoría
            model = await self._train_category_model(daily_data)
            
            if model is None:
                raise ValueError("No se pudo entrenar el modelo para esta categoría")
            
            # Generar predicciones
            days_ahead = months_ahead * 30
            future_features = self._generate_category_future_features(daily_data, days_ahead)
            predicted_sales = model.predict(future_features)
            
            # Análisis de mercado
            market_analysis = self._analyze_market_prediction(daily_data, predicted_sales, months_ahead)
            
            return {
                'category': category,
                'prediction_period_months': months_ahead,
                'predicted_market_sales': [max(0, int(sale)) for sale in predicted_sales],
                'total_predicted_market_size': sum(predicted_sales),
                'market_growth_rate': round(market_analysis['growth_rate'], 2),
                'market_trend': market_analysis['trend'],
                'seasonal_forecast': market_analysis['seasonal_forecast'],
                'competitive_analysis': market_analysis['competitive_analysis'],
                'opportunity_areas': market_analysis['opportunity_areas'],
                'risk_factors': market_analysis['risk_factors'],
                'strategic_recommendations': market_analysis['recommendations'],
                'model_confidence': round(market_analysis['confidence'], 3),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error prediciendo tendencias de mercado: {e}")
            raise
    
    async def _train_product_model(self, product_data: pd.DataFrame) -> Optional[object]:
        """Entrenar modelo para un producto específico"""
        try:
            # Preparar features
            features = [
                'day_of_week', 'month', 'day_of_year', 'is_weekend', 'is_holiday',
                'price', 'sentiment_score', 'search_volume', 'competitor_price',
                'marketing_spend', 'price_competitiveness', 'search_to_sales_ratio'
            ]
            
            X = product_data[features].values
            y = product_data['sales'].values
            
            # Dividir datos
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Escalar features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Entrenar múltiples modelos y seleccionar el mejor
            best_model = None
            best_score = -float('inf')
            
            for name, model in self.models.items():
                model.fit(X_train_scaled, y_train)
                score = model.score(X_test_scaled, y_test)
                
                if score > best_score:
                    best_score = score
                    best_model = model
            
            # Guardar el mejor modelo
            product_id = product_data['product_id'].iloc[0]
            self.trained_models[product_id] = {
                'model': best_model,
                'scaler': self.scaler,
                'features': features,
                'score': best_score
            }
            
            return best_model
            
        except Exception as e:
            logger.error(f"Error entrenando modelo para producto: {e}")
            return None
    
    async def _train_category_model(self, category_data: pd.DataFrame) -> Optional[object]:
        """Entrenar modelo para una categoría"""
        try:
            # Features para categoría
            features = [
                'day_of_week', 'month', 'day_of_year', 'is_weekend', 'is_holiday',
                'price', 'sentiment_score', 'search_volume', 'marketing_spend'
            ]
            
            X = category_data[features].values
            y = category_data['sales'].values
            
            # Dividir y escalar
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Usar Random Forest para categorías
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train_scaled, y_train)
            
            return model
            
        except Exception as e:
            logger.error(f"Error entrenando modelo para categoría: {e}")
            return None
    
    def _generate_future_features(self, product_data: pd.DataFrame, days_ahead: int) -> np.ndarray:
        """Generar features para predicciones futuras"""
        last_date = product_data['date'].max()
        features = []
        
        for day in range(1, days_ahead + 1):
            future_date = last_date + timedelta(days=day)
            
            # Calcular features para la fecha futura
            day_of_week = future_date.weekday()
            month = future_date.month
            day_of_year = future_date.timetuple().tm_yday
            
            # Usar valores promedio del producto para features que no cambian
            avg_price = product_data['price'].mean()
            avg_sentiment = product_data['sentiment_score'].mean()
            avg_search = product_data['search_volume'].mean()
            avg_competitor_price = product_data['competitor_price'].mean()
            avg_marketing = product_data['marketing_spend'].mean()
            
            feature_vector = [
                day_of_week, month, day_of_year,
                1 if day_of_week >= 5 else 0,  # is_weekend
                1 if month in [12, 11, 6] else 0,  # is_holiday
                avg_price, avg_sentiment, avg_search, avg_competitor_price,
                avg_marketing, avg_price / avg_competitor_price, avg_search / 100
            ]
            
            features.append(feature_vector)
        
        return np.array(features)
    
    def _generate_category_future_features(self, category_data: pd.DataFrame, days_ahead: int) -> np.ndarray:
        """Generar features futuras para categoría"""
        last_date = category_data['date'].max()
        features = []
        
        for day in range(1, days_ahead + 1):
            future_date = last_date + timedelta(days=day)
            
            day_of_week = future_date.weekday()
            month = future_date.month
            day_of_year = future_date.timetuple().tm_yday
            
            # Valores promedio de la categoría
            avg_price = category_data['price'].mean()
            avg_sentiment = category_data['sentiment_score'].mean()
            avg_search = category_data['search_volume'].mean()
            avg_marketing = category_data['marketing_spend'].mean()
            
            feature_vector = [
                day_of_week, month, day_of_year,
                1 if day_of_week >= 5 else 0,
                1 if month in [12, 11, 6] else 0,
                avg_price, avg_sentiment, avg_search, avg_marketing
            ]
            
            features.append(feature_vector)
        
        return np.array(features)
    
    def _calculate_prediction_confidence(self, model: object, product_data: pd.DataFrame) -> float:
        """Calcular nivel de confianza de la predicción"""
        try:
            # Usar R² score como base de confianza
            features = [
                'day_of_week', 'month', 'day_of_year', 'is_weekend', 'is_holiday',
                'price', 'sentiment_score', 'search_volume', 'competitor_price',
                'marketing_spend', 'price_competitiveness', 'search_to_sales_ratio'
            ]
            
            X = product_data[features].values
            y = product_data['sales'].values
            
            # Escalar features
            X_scaled = self.scaler.transform(X)
            
            # Calcular R²
            r2 = model.score(X_scaled, y)
            
            # Ajustar confianza basada en cantidad de datos
            data_factor = min(1.0, len(product_data) / 365)  # Más datos = más confianza
            
            # Ajustar por estabilidad de datos
            sales_std = product_data['sales'].std()
            sales_mean = product_data['sales'].mean()
            stability_factor = 1.0 / (1.0 + sales_std / max(1, sales_mean))
            
            confidence = r2 * data_factor * stability_factor
            
            return max(0.1, min(0.95, confidence))  # Limitar entre 0.1 y 0.95
            
        except Exception as e:
            logger.error(f"Error calculando confianza: {e}")
            return 0.5  # Confianza por defecto
    
    def _analyze_prediction(self, product_data: pd.DataFrame, predicted_sales: np.ndarray, days_ahead: int) -> Dict[str, Any]:
        """Analizar predicción y generar insights"""
        try:
            # Calcular crecimiento
            recent_sales = product_data['sales'].tail(30).mean()
            predicted_avg = np.mean(predicted_sales)
            growth_rate = ((predicted_avg - recent_sales) / recent_sales * 100) if recent_sales > 0 else 0
            
            # Determinar dirección de tendencia
            if growth_rate > 5:
                trend_direction = "rising"
            elif growth_rate < -5:
                trend_direction = "falling"
            else:
                trend_direction = "stable"
            
            # Análisis estacional
            seasonal_factors = self._analyze_seasonal_factors(predicted_sales, days_ahead)
            
            # Factores de riesgo
            risk_factors = self._identify_risk_factors(product_data, predicted_sales)
            
            # Recomendaciones
            recommendations = self._generate_prediction_recommendations(
                product_data, predicted_sales, growth_rate, trend_direction
            )
            
            return {
                'growth_rate': growth_rate,
                'trend_direction': trend_direction,
                'seasonal_factors': seasonal_factors,
                'risk_factors': risk_factors,
                'recommendations': recommendations
            }
            
        except Exception as e:
            logger.error(f"Error analizando predicción: {e}")
            return {
                'growth_rate': 0,
                'trend_direction': "stable",
                'seasonal_factors': [],
                'risk_factors': [],
                'recommendations': []
            }
    
    def _analyze_seasonal_factors(self, predicted_sales: np.ndarray, days_ahead: int) -> List[Dict[str, Any]]:
        """Analizar factores estacionales en las predicciones"""
        seasonal_factors = []
        
        # Identificar picos y valles
        peak_day = np.argmax(predicted_sales) + 1
        valley_day = np.argmin(predicted_sales) + 1
        
        # Calcular variabilidad estacional
        sales_std = np.std(predicted_sales)
        sales_mean = np.mean(predicted_sales)
        variability = sales_std / max(1, sales_mean)
        
        seasonal_factors.append({
            'peak_day': peak_day,
            'peak_value': int(max(predicted_sales)),
            'valley_day': valley_day,
            'valley_value': int(min(predicted_sales)),
            'seasonal_variability': round(variability, 3),
            'seasonal_strength': 'high' if variability > 0.3 else 'medium' if variability > 0.1 else 'low'
        })
        
        return seasonal_factors
    
    def _identify_risk_factors(self, product_data: pd.DataFrame, predicted_sales: np.ndarray) -> List[str]:
        """Identificar factores de riesgo en las predicciones"""
        risk_factors = []
        
        # Riesgo por alta variabilidad
        sales_std = np.std(predicted_sales)
        if sales_std > np.mean(predicted_sales) * 0.5:
            risk_factors.append("Alta variabilidad en predicciones")
        
        # Riesgo por tendencia negativa
        if np.mean(predicted_sales) < product_data['sales'].tail(30).mean() * 0.8:
            risk_factors.append("Tendencia de ventas decreciente")
        
        # Riesgo por estacionalidad extrema
        if max(predicted_sales) > min(predicted_sales) * 3:
            risk_factors.append("Patrón estacional muy marcado")
        
        # Riesgo por datos insuficientes
        if len(product_data) < 90:
            risk_factors.append("Datos históricos limitados")
        
        return risk_factors
    
    def _generate_prediction_recommendations(self, product_data: pd.DataFrame, 
                                           predicted_sales: np.ndarray, 
                                           growth_rate: float, 
                                           trend_direction: str) -> List[str]:
        """Generar recomendaciones basadas en predicciones"""
        recommendations = []
        
        if trend_direction == "rising":
            recommendations.extend([
                "Incrementar inventario para aprovechar la tendencia positiva",
                "Considerar aumentar el presupuesto de marketing",
                "Evaluar oportunidades de expansión de línea"
            ])
        elif trend_direction == "falling":
            recommendations.extend([
                "Revisar estrategia de precios y promociones",
                "Analizar cambios en preferencias del consumidor",
                "Considerar reposicionamiento del producto"
            ])
        else:
            recommendations.extend([
                "Mantener estrategia actual",
                "Monitorear indicadores de mercado",
                "Optimizar mix de productos"
            ])
        
        # Recomendaciones específicas por crecimiento
        if growth_rate > 20:
            recommendations.append("Preparar para crecimiento acelerado")
        elif growth_rate < -20:
            recommendations.append("Implementar medidas correctivas urgentes")
        
        return recommendations
    
    def _analyze_demand_prediction(self, product_data: pd.DataFrame, 
                                 predicted_sales: List[int], 
                                 days_ahead: int) -> Dict[str, Any]:
        """Análisis detallado de predicción de demanda"""
        try:
            # Análisis de tendencia
            recent_avg = product_data['sales'].tail(30).mean()
            predicted_avg = np.mean(predicted_sales)
            growth_rate = ((predicted_avg - recent_avg) / recent_avg * 100) if recent_avg > 0 else 0
            
            trend_analysis = {
                'current_average': round(recent_avg, 2),
                'predicted_average': round(predicted_avg, 2),
                'growth_rate': round(growth_rate, 2),
                'trend_strength': 'strong' if abs(growth_rate) > 15 else 'moderate' if abs(growth_rate) > 5 else 'weak'
            }
            
            # Patrones estacionales
            seasonal_patterns = self._analyze_seasonal_patterns(predicted_sales, days_ahead)
            
            # Evaluación de riesgos
            risk_assessment = self._assess_demand_risks(product_data, predicted_sales)
            
            # Recomendaciones de inventario
            inventory_recommendations = self._generate_inventory_recommendations(predicted_sales)
            
            # Rendimiento del modelo
            model_performance = self._evaluate_model_performance(product_data)
            
            return {
                'trend_analysis': trend_analysis,
                'seasonal_patterns': seasonal_patterns,
                'risk_assessment': risk_assessment,
                'inventory_recommendations': inventory_recommendations,
                'model_performance': model_performance
            }
            
        except Exception as e:
            logger.error(f"Error analizando predicción de demanda: {e}")
            return {}
    
    def _analyze_seasonal_patterns(self, predicted_sales: List[int], days_ahead: int) -> Dict[str, Any]:
        """Analizar patrones estacionales en las predicciones"""
        # Identificar ciclos semanales
        weekly_pattern = []
        for i in range(0, min(days_ahead, 7)):
            week_days = predicted_sales[i::7]
            weekly_pattern.append({
                'day_of_week': i + 1,
                'average_sales': round(np.mean(week_days), 2),
                'peak_day': i + 1 if np.mean(week_days) == max(weekly_pattern) else None
            })
        
        # Identificar tendencias dentro del período
        trend_slope = np.polyfit(range(len(predicted_sales)), predicted_sales, 1)[0]
        
        return {
            'weekly_pattern': weekly_pattern,
            'trend_slope': round(trend_slope, 3),
            'seasonal_strength': 'high' if np.std(predicted_sales) > np.mean(predicted_sales) * 0.3 else 'low'
        }
    
    def _assess_demand_risks(self, product_data: pd.DataFrame, predicted_sales: List[int]) -> Dict[str, Any]:
        """Evaluar riesgos en la predicción de demanda"""
        risks = {
            'high_variability': np.std(predicted_sales) > np.mean(predicted_sales) * 0.5,
            'declining_trend': np.mean(predicted_sales) < product_data['sales'].tail(30).mean() * 0.8,
            'insufficient_data': len(product_data) < 90,
            'high_uncertainty': len(predicted_sales) > 30 and np.std(predicted_sales[-30:]) > np.mean(predicted_sales[-30:]) * 0.4
        }
        
        risk_level = sum(risks.values())
        risk_score = 'high' if risk_level >= 3 else 'medium' if risk_level >= 1 else 'low'
        
        return {
            'risk_factors': risks,
            'risk_level': risk_score,
            'risk_score': risk_level
        }
    
    def _generate_inventory_recommendations(self, predicted_sales: List[int]) -> List[str]:
        """Generar recomendaciones de inventario basadas en predicciones"""
        recommendations = []
        
        avg_demand = np.mean(predicted_sales)
        max_demand = max(predicted_sales)
        min_demand = min(predicted_sales)
        
        # Recomendación de inventario base
        safety_stock = max_demand * 0.2  # 20% de stock de seguridad
        recommended_inventory = avg_demand * 7 + safety_stock  # 1 semana + seguridad
        
        recommendations.append(f"Mantener inventario de {int(recommended_inventory)} unidades")
        
        # Recomendaciones específicas
        if max_demand > avg_demand * 2:
            recommendations.append("Preparar para picos de demanda estacional")
        
        if min_demand < avg_demand * 0.5:
            recommendations.append("Planificar para períodos de baja demanda")
        
        if np.std(predicted_sales) > avg_demand * 0.3:
            recommendations.append("Implementar sistema de inventario flexible")
        
        return recommendations
    
    def _evaluate_model_performance(self, product_data: pd.DataFrame) -> Dict[str, Any]:
        """Evaluar rendimiento del modelo"""
        try:
            product_id = product_data['product_id'].iloc[0]
            
            if product_id in self.trained_models:
                model_info = self.trained_models[product_id]
                return {
                    'model_type': model_info['model'].__class__.__name__,
                    'r2_score': round(model_info['score'], 3),
                    'performance_rating': 'excellent' if model_info['score'] > 0.8 else 'good' if model_info['score'] > 0.6 else 'fair',
                    'features_used': len(model_info['features']),
                    'training_data_points': len(product_data)
                }
            else:
                return {
                    'model_type': 'unknown',
                    'r2_score': 0.0,
                    'performance_rating': 'unknown',
                    'features_used': 0,
                    'training_data_points': len(product_data)
                }
                
        except Exception as e:
            logger.error(f"Error evaluando rendimiento del modelo: {e}")
            return {}
    
    def _calculate_confidence_intervals(self, predicted_sales: List[int], 
                                      model: object, 
                                      product_data: pd.DataFrame) -> Dict[str, List[float]]:
        """Calcular intervalos de confianza para las predicciones"""
        try:
            # Simular múltiples predicciones para calcular intervalos
            n_simulations = 100
            all_predictions = []
            
            for _ in range(n_simulations):
                # Añadir ruido a los datos de entrenamiento
                noisy_data = product_data.copy()
                noise = np.random.normal(0, product_data['sales'].std() * 0.1, len(product_data))
                noisy_data['sales'] = noisy_data['sales'] + noise
                
                # Reentrenar modelo con datos ruidosos
                features = [
                    'day_of_week', 'month', 'day_of_year', 'is_weekend', 'is_holiday',
                    'price', 'sentiment_score', 'search_volume', 'competitor_price',
                    'marketing_spend', 'price_competitiveness', 'search_to_sales_ratio'
                ]
                
                X = noisy_data[features].values
                y = noisy_data['sales'].values
                
                temp_model = RandomForestRegressor(n_estimators=50, random_state=42)
                temp_model.fit(X, y)
                
                # Generar predicciones
                future_features = self._generate_future_features(noisy_data, len(predicted_sales))
                temp_predictions = temp_model.predict(future_features)
                all_predictions.append(temp_predictions)
            
            # Calcular intervalos de confianza
            all_predictions = np.array(all_predictions)
            lower_bound = np.percentile(all_predictions, 5, axis=0)  # 5% inferior
            upper_bound = np.percentile(all_predictions, 95, axis=0)  # 95% superior
            
            return {
                'lower_bound': [max(0, int(val)) for val in lower_bound],
                'upper_bound': [max(0, int(val)) for val in upper_bound],
                'confidence_level': 0.90
            }
            
        except Exception as e:
            logger.error(f"Error calculando intervalos de confianza: {e}")
            return {
                'lower_bound': [max(0, int(sale * 0.8)) for sale in predicted_sales],
                'upper_bound': [max(0, int(sale * 1.2)) for sale in predicted_sales],
                'confidence_level': 0.80
            }
    
    def _analyze_market_prediction(self, category_data: pd.DataFrame, 
                                 predicted_sales: np.ndarray, 
                                 months_ahead: int) -> Dict[str, Any]:
        """Analizar predicción de mercado"""
        try:
            # Cálculo de crecimiento del mercado
            recent_market_sales = category_data['sales'].tail(90).mean()  # Últimos 3 meses
            predicted_market_avg = np.mean(predicted_sales)
            market_growth = ((predicted_market_avg - recent_market_sales) / recent_market_sales * 100) if recent_market_sales > 0 else 0
            
            # Análisis de tendencia del mercado
            if market_growth > 10:
                market_trend = "expanding"
            elif market_growth > -5:
                market_trend = "stable"
            else:
                market_trend = "contracting"
            
            # Pronóstico estacional
            seasonal_forecast = self._generate_seasonal_forecast(predicted_sales, months_ahead)
            
            # Análisis competitivo
            competitive_analysis = self._analyze_competitive_position(category_data)
            
            # Áreas de oportunidad
            opportunity_areas = self._identify_opportunity_areas(category_data, predicted_sales)
            
            # Factores de riesgo del mercado
            risk_factors = self._identify_market_risks(category_data, predicted_sales)
            
            # Recomendaciones estratégicas
            recommendations = self._generate_market_recommendations(
                market_growth, market_trend, opportunity_areas, risk_factors
            )
            
            # Calcular confianza del modelo
            confidence = self._calculate_market_confidence(category_data, predicted_sales)
            
            return {
                'growth_rate': market_growth,
                'trend': market_trend,
                'seasonal_forecast': seasonal_forecast,
                'competitive_analysis': competitive_analysis,
                'opportunity_areas': opportunity_areas,
                'risk_factors': risk_factors,
                'recommendations': recommendations,
                'confidence': confidence
            }
            
        except Exception as e:
            logger.error(f"Error analizando predicción de mercado: {e}")
            return {}
    
    def _generate_seasonal_forecast(self, predicted_sales: np.ndarray, months_ahead: int) -> Dict[str, Any]:
        """Generar pronóstico estacional"""
        # Identificar patrones estacionales
        monthly_sales = []
        for month in range(1, months_ahead + 1):
            start_idx = (month - 1) * 30
            end_idx = min(month * 30, len(predicted_sales))
            month_sales = predicted_sales[start_idx:end_idx]
            monthly_sales.append({
                'month': month,
                'total_sales': int(sum(month_sales)),
                'average_daily_sales': round(np.mean(month_sales), 2),
                'peak_day': int(np.argmax(month_sales)) + 1
            })
        
        return {
            'monthly_breakdown': monthly_sales,
            'peak_month': max(monthly_sales, key=lambda x: x['total_sales'])['month'],
            'lowest_month': min(monthly_sales, key=lambda x: x['total_sales'])['month']
        }
    
    def _analyze_competitive_position(self, category_data: pd.DataFrame) -> Dict[str, Any]:
        """Analizar posición competitiva"""
        # Simular análisis competitivo
        return {
            'market_share': round(np.random.uniform(15, 35), 1),
            'competitive_advantage': 'innovation',
            'price_position': 'competitive',
            'brand_strength': 'strong',
            'customer_loyalty': 'high'
        }
    
    def _identify_opportunity_areas(self, category_data: pd.DataFrame, predicted_sales: np.ndarray) -> List[str]:
        """Identificar áreas de oportunidad"""
        opportunities = []
        
        # Oportunidades basadas en crecimiento
        if np.mean(predicted_sales) > category_data['sales'].tail(30).mean() * 1.2:
            opportunities.append("Expansión de mercado")
        
        # Oportunidades por estacionalidad
        if np.std(predicted_sales) > np.mean(predicted_sales) * 0.3:
            opportunities.append("Optimización de inventario estacional")
        
        # Oportunidades por sentimiento
        if category_data['sentiment_score'].mean() > 0.5:
            opportunities.append("Desarrollo de productos premium")
        
        return opportunities
    
    def _identify_market_risks(self, category_data: pd.DataFrame, predicted_sales: np.ndarray) -> List[str]:
        """Identificar riesgos del mercado"""
        risks = []
        
        # Riesgos por declive
        if np.mean(predicted_sales) < category_data['sales'].tail(30).mean() * 0.8:
            risks.append("Declive del mercado")
        
        # Riesgos por alta volatilidad
        if np.std(predicted_sales) > np.mean(predicted_sales) * 0.5:
            risks.append("Alta volatilidad del mercado")
        
        # Riesgos por sentimiento negativo
        if category_data['sentiment_score'].mean() < -0.2:
            risks.append("Sentimiento negativo del consumidor")
        
        return risks
    
    def _generate_market_recommendations(self, growth_rate: float, trend: str, 
                                       opportunities: List[str], risks: List[str]) -> List[str]:
        """Generar recomendaciones estratégicas para el mercado"""
        recommendations = []
        
        if trend == "expanding":
            recommendations.extend([
                "Incrementar inversión en marketing",
                "Expandir gama de productos",
                "Explorar nuevos canales de distribución"
            ])
        elif trend == "contracting":
            recommendations.extend([
                "Optimizar costos operativos",
                "Enfocar en productos core",
                "Diversificar a mercados relacionados"
            ])
        
        # Recomendaciones específicas por oportunidades
        for opportunity in opportunities:
            if "Expansión" in opportunity:
                recommendations.append("Desarrollar estrategia de expansión")
            elif "Optimización" in opportunity:
                recommendations.append("Implementar sistema de gestión de inventario")
        
        # Recomendaciones por riesgos
        for risk in risks:
            if "Declive" in risk:
                recommendations.append("Desarrollar estrategia de defensa")
            elif "Volatilidad" in risk:
                recommendations.append("Implementar estrategias de mitigación de riesgo")
        
        return recommendations
    
    def _calculate_market_confidence(self, category_data: pd.DataFrame, predicted_sales: np.ndarray) -> float:
        """Calcular confianza en la predicción del mercado"""
        try:
            # Factores que afectan la confianza
            data_quality = min(1.0, len(category_data) / 365)  # Más datos = más confianza
            trend_stability = 1.0 / (1.0 + category_data['sales'].std() / max(1, category_data['sales'].mean()))
            prediction_consistency = 1.0 / (1.0 + np.std(predicted_sales) / max(1, np.mean(predicted_sales)))
            
            confidence = (data_quality + trend_stability + prediction_consistency) / 3
            
            return max(0.1, min(0.95, confidence))
            
        except Exception as e:
            logger.error(f"Error calculando confianza del mercado: {e}")
            return 0.5 