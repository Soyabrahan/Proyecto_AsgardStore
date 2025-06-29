"""
Servicio de Análisis de Tendencias
Implementa algoritmos de IA para identificar y analizar tendencias del mercado
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
import json
import uuid

from models.trend_models import (
    TrendAnalysisRequest, 
    TrendAnalysisResponse, 
    TrendData, 
    TrendDirection,
    SalesMetrics
)

logger = logging.getLogger(__name__)

class TrendAnalyzer:
    """Analizador de tendencias con algoritmos de IA"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.trend_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.clustering_model = KMeans(n_clusters=5, random_state=42)
        self.sample_data = self._generate_sample_data()
        
    def _generate_sample_data(self) -> pd.DataFrame:
        """Generar datos de ejemplo para demostración"""
        np.random.seed(42)
        
        # Generar datos de productos
        products = [
            "Smartphone Galaxy S24", "iPhone 15 Pro", "Laptop Dell XPS", 
            "Nike Air Max", "Adidas Ultraboost", "Samsung TV 4K",
            "Sony Headphones", "MacBook Pro", "iPad Air", "Apple Watch",
            "Nike Running Shoes", "Adidas Soccer Ball", "Basketball Nike",
            "Yoga Mat Premium", "Dumbbells Set", "Treadmill Pro",
            "Makeup Palette", "Skincare Set", "Hair Dryer", "Perfume Luxury"
        ]
        
        categories = ["electronics"] * 10 + ["sports"] * 6 + ["beauty"] * 4
        
        data = []
        base_date = datetime.now() - timedelta(days=365)
        
        for i, (product, category) in enumerate(zip(products, categories)):
            # Generar datos históricos para cada producto
            for day in range(365):
                date = base_date + timedelta(days=day)
                
                # Simular tendencias estacionales y cíclicas
                seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * day / 365)
                trend_factor = 1 + 0.1 * (day / 365)  # Tendencia general
                noise = np.random.normal(0, 0.1)
                
                # Simular diferentes patrones por categoría
                if category == "electronics":
                    tech_trend = 1 + 0.2 * np.sin(2 * np.pi * day / 90)  # Ciclos de 3 meses
                    base_sales = 100 + i * 10
                elif category == "sports":
                    sports_trend = 1 + 0.4 * np.sin(2 * np.pi * day / 180)  # Ciclos de 6 meses
                    base_sales = 80 + i * 8
                else:  # beauty
                    beauty_trend = 1 + 0.25 * np.sin(2 * np.pi * day / 120)  # Ciclos de 4 meses
                    base_sales = 60 + i * 6
                
                # Calcular ventas con todos los factores
                if category == "electronics":
                    sales = int(base_sales * seasonal_factor * trend_factor * tech_trend * (1 + noise))
                elif category == "sports":
                    sales = int(base_sales * seasonal_factor * trend_factor * sports_trend * (1 + noise))
                else:
                    sales = int(base_sales * seasonal_factor * trend_factor * beauty_trend * (1 + noise))
                
                # Simular otros métricas
                search_volume = int(sales * np.random.uniform(10, 50))
                price = np.random.uniform(50, 500)
                sentiment = np.random.uniform(-0.2, 0.8)
                
                data.append({
                    'date': date,
                    'product_id': f'prod_{i:03d}',
                    'product_name': product,
                    'category': category,
                    'sales': max(0, sales),
                    'search_volume': max(0, search_volume),
                    'price': price,
                    'sentiment_score': sentiment,
                    'reviews_count': int(sales * np.random.uniform(0.1, 0.3))
                })
        
        return pd.DataFrame(data)
    
    async def get_current_trends(self, category: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtener tendencias actuales del mercado"""
        try:
            # Filtrar datos por categoría si se especifica
            if category:
                data = self.sample_data[self.sample_data['category'] == category].copy()
            else:
                data = self.sample_data.copy()
            
            # Calcular tendencias para los últimos 30 días
            recent_data = data[data['date'] >= datetime.now() - timedelta(days=30)]
            
            # Agrupar por producto y calcular métricas de tendencia
            trends = []
            for product_id in recent_data['product_id'].unique():
                product_data = recent_data[recent_data['product_id'] == product_id]
                
                if len(product_data) < 7:  # Necesitamos al menos una semana de datos
                    continue
                
                # Calcular métricas de tendencia
                sales_trend = self._calculate_trend(product_data['sales'].values)
                search_trend = self._calculate_trend(product_data['search_volume'].values)
                sentiment_avg = product_data['sentiment_score'].mean()
                
                # Determinar dirección de la tendencia
                trend_direction = self._determine_trend_direction(sales_trend, search_trend)
                
                # Calcular puntuación de tendencia (0-100)
                trend_score = self._calculate_trend_score(sales_trend, search_trend, sentiment_avg)
                
                # Obtener información del producto
                product_info = product_data.iloc[0]
                
                trends.append({
                    'product_id': product_id,
                    'product_name': product_info['product_name'],
                    'category': product_info['category'],
                    'current_trend': trend_direction,
                    'trend_score': round(trend_score, 2),
                    'growth_rate': round(sales_trend * 100, 2),
                    'search_volume': int(product_data['search_volume'].mean()),
                    'sentiment_score': round(sentiment_avg, 3),
                    'price_trend': round(self._calculate_price_trend(product_data['price'].values), 2),
                    'last_updated': datetime.now().isoformat()
                })
            
            # Ordenar por puntuación de tendencia y limitar resultados
            trends.sort(key=lambda x: x['trend_score'], reverse=True)
            return trends[:limit]
            
        except Exception as e:
            logger.error(f"Error obteniendo tendencias actuales: {e}")
            raise
    
    async def analyze_custom_trends(self, request: TrendAnalysisRequest) -> TrendAnalysisResponse:
        """Análisis personalizado de tendencias"""
        try:
            # Filtrar datos según la solicitud
            data = self.sample_data.copy()
            
            if request.categories:
                data = data[data['category'].isin(request.categories)]
            
            if request.start_date:
                start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
                data = data[data['date'] >= start_date]
            
            if request.end_date:
                end_date = datetime.strptime(request.end_date, "%Y-%m-%d")
                data = data[data['date'] <= end_date]
            
            # Analizar tendencias
            trends = []
            for product_id in data['product_id'].unique():
                product_data = data[data['product_id'] == product_id]
                
                if len(product_data) < 14:  # Necesitamos al menos 2 semanas de datos
                    continue
                
                # Calcular métricas
                sales_trend = self._calculate_trend(product_data['sales'].values)
                search_trend = self._calculate_trend(product_data['search_volume'].values)
                sentiment_avg = product_data['sentiment_score'].mean()
                
                trend_direction = self._determine_trend_direction(sales_trend, search_trend)
                trend_score = self._calculate_trend_score(sales_trend, search_trend, sentiment_avg)
                
                product_info = product_data.iloc[0]
                
                trend_data = TrendData(
                    product_id=product_id,
                    product_name=product_info['product_name'],
                    category=product_info['category'],
                    current_trend=trend_direction,
                    trend_score=round(trend_score, 2),
                    growth_rate=round(sales_trend * 100, 2),
                    search_volume=int(product_data['search_volume'].mean()),
                    sentiment_score=round(sentiment_avg, 3) if request.include_sentiment else None,
                    price_trend=round(self._calculate_price_trend(product_data['price'].values), 2),
                    last_updated=datetime.now()
                )
                trends.append(trend_data)
            
            # Generar resumen
            summary = self._generate_analysis_summary(trends)
            
            # Generar predicciones si se solicita
            predictions = None
            if request.include_predictions:
                predictions = await self._generate_predictions(data, request.prediction_days)
            
            return TrendAnalysisResponse(
                analysis_id=str(uuid.uuid4()),
                request=request,
                trends=trends,
                summary=summary,
                predictions=predictions,
                generated_at=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error en análisis personalizado: {e}")
            raise
    
    async def get_sales_metrics(self, start_date: Optional[str] = None, 
                               end_date: Optional[str] = None, 
                               category: Optional[str] = None) -> SalesMetrics:
        """Obtener métricas de ventas"""
        try:
            data = self.sample_data.copy()
            
            # Aplicar filtros
            if start_date:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                data = data[data['date'] >= start]
            
            if end_date:
                end = datetime.strptime(end_date, "%Y-%m-%d")
                data = data[data['date'] <= end]
            
            if category:
                data = data[data['category'] == category]
            
            if data.empty:
                raise ValueError("No hay datos disponibles para los filtros especificados")
            
            # Calcular métricas
            total_sales = data['sales'].sum()
            total_orders = len(data)
            average_order_value = total_sales / total_orders if total_orders > 0 else 0
            
            # Ventas por categoría
            sales_by_category = data.groupby('category')['sales'].sum().to_dict()
            
            # Productos más vendidos
            top_products = data.groupby(['product_id', 'product_name']).agg({
                'sales': 'sum'
            }).reset_index().nlargest(10, 'sales')
            
            top_products_list = []
            for _, row in top_products.iterrows():
                top_products_list.append({
                    'product_id': row['product_id'],
                    'product_name': row['product_name'],
                    'units_sold': int(row['sales']),
                    'revenue': float(row['sales'] * data[data['product_id'] == row['product_id']]['price'].mean())
                })
            
            # Calcular crecimiento vs período anterior
            period_start = data['date'].min()
            period_end = data['date'].max()
            
            # Período anterior de la misma duración
            period_duration = period_end - period_start
            previous_start = period_start - period_duration
            previous_end = period_start
            
            previous_data = self.sample_data[
                (self.sample_data['date'] >= previous_start) & 
                (self.sample_data['date'] < previous_end)
            ]
            
            if category:
                previous_data = previous_data[previous_data['category'] == category]
            
            previous_sales = previous_data['sales'].sum()
            growth_rate = ((total_sales - previous_sales) / previous_sales * 100) if previous_sales > 0 else 0
            
            # Tasa de conversión (simulada)
            conversion_rate = np.random.uniform(2.0, 5.0)
            
            return SalesMetrics(
                period_start=period_start,
                period_end=period_end,
                total_sales=float(total_sales),
                total_orders=int(total_orders),
                average_order_value=float(average_order_value),
                sales_by_category=sales_by_category,
                top_products=top_products_list,
                growth_rate=round(growth_rate, 2),
                conversion_rate=round(conversion_rate, 2)
            )
            
        except Exception as e:
            logger.error(f"Error obteniendo métricas de ventas: {e}")
            raise
    
    async def generate_trends_report(self, format: str = "json", include_predictions: bool = True) -> Dict[str, Any]:
        """Generar reporte completo de tendencias"""
        try:
            # Obtener tendencias actuales
            current_trends = await self.get_current_trends(limit=50)
            
            # Análisis por categoría
            category_analysis = {}
            for trend in current_trends:
                category = trend['category']
                if category not in category_analysis:
                    category_analysis[category] = {
                        'total_products': 0,
                        'rising_trends': 0,
                        'falling_trends': 0,
                        'stable_trends': 0,
                        'avg_trend_score': 0,
                        'top_products': []
                    }
                
                category_analysis[category]['total_products'] += 1
                category_analysis[category]['avg_trend_score'] += trend['trend_score']
                
                if trend['current_trend'] == TrendDirection.RISING:
                    category_analysis[category]['rising_trends'] += 1
                elif trend['current_trend'] == TrendDirection.FALLING:
                    category_analysis[category]['falling_trends'] += 1
                else:
                    category_analysis[category]['stable_trends'] += 1
                
                # Mantener top 5 productos por categoría
                category_analysis[category]['top_products'].append({
                    'product_name': trend['product_name'],
                    'trend_score': trend['trend_score'],
                    'growth_rate': trend['growth_rate']
                })
            
            # Calcular promedios y ordenar top productos
            for category in category_analysis:
                total = category_analysis[category]['total_products']
                if total > 0:
                    category_analysis[category]['avg_trend_score'] /= total
                
                # Ordenar top productos por puntuación de tendencia
                category_analysis[category]['top_products'].sort(
                    key=lambda x: x['trend_score'], reverse=True
                )
                category_analysis[category]['top_products'] = category_analysis[category]['top_products'][:5]
            
            # Generar predicciones si se solicita
            predictions = None
            if include_predictions:
                predictions = await self._generate_predictions(self.sample_data, 30)
            
            report = {
                'report_id': str(uuid.uuid4()),
                'generated_at': datetime.now().isoformat(),
                'summary': {
                    'total_products_analyzed': len(current_trends),
                    'categories_analyzed': list(category_analysis.keys()),
                    'overall_trend': self._determine_overall_trend(current_trends)
                },
                'category_analysis': category_analysis,
                'top_trending_products': current_trends[:10],
                'predictions': predictions,
                'recommendations': self._generate_strategic_recommendations(current_trends, category_analysis)
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generando reporte de tendencias: {e}")
            raise
    
    async def generate_competition_report(self, competitors: List[str], metrics: List[str]) -> Dict[str, Any]:
        """Generar reporte de análisis competitivo"""
        try:
            # Simular datos de competencia
            competition_data = {}
            
            for competitor in competitors:
                competition_data[competitor] = {
                    'market_share': np.random.uniform(5, 25),
                    'price_competitiveness': np.random.uniform(0.8, 1.2),
                    'trend_alignment': np.random.uniform(0.6, 0.95),
                    'customer_satisfaction': np.random.uniform(3.5, 4.8),
                    'product_range': np.random.uniform(50, 200),
                    'strengths': self._generate_competitor_strengths(),
                    'weaknesses': self._generate_competitor_weaknesses(),
                    'threat_level': self._assess_threat_level()
                }
            
            # Análisis comparativo
            comparative_analysis = {
                'market_position': self._analyze_market_position(competition_data),
                'price_analysis': self._analyze_price_competitiveness(competition_data),
                'trend_analysis': self._analyze_trend_alignment(competition_data),
                'opportunities': self._identify_opportunities(competition_data),
                'threats': self._identify_threats(competition_data)
            }
            
            return {
                'report_id': str(uuid.uuid4()),
                'generated_at': datetime.now().isoformat(),
                'competitors_analyzed': competitors,
                'metrics_analyzed': metrics,
                'competition_data': competition_data,
                'comparative_analysis': comparative_analysis,
                'strategic_recommendations': self._generate_competitive_recommendations(competition_data)
            }
            
        except Exception as e:
            logger.error(f"Error generando reporte de competencia: {e}")
            raise
    
    def _calculate_trend(self, values: np.ndarray) -> float:
        """Calcular tendencia usando regresión lineal"""
        if len(values) < 2:
            return 0.0
        
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        # Normalizar la tendencia
        if np.mean(values) > 0:
            return slope / np.mean(values)
        return 0.0
    
    def _determine_trend_direction(self, sales_trend: float, search_trend: float) -> TrendDirection:
        """Determinar dirección de la tendencia"""
        combined_trend = (sales_trend + search_trend) / 2
        
        if combined_trend > 0.05:
            return TrendDirection.RISING
        elif combined_trend < -0.05:
            return TrendDirection.FALLING
        elif abs(combined_trend) < 0.02:
            return TrendDirection.STABLE
        else:
            return TrendDirection.VOLATILE
    
    def _calculate_trend_score(self, sales_trend: float, search_trend: float, sentiment: float) -> float:
        """Calcular puntuación de tendencia (0-100)"""
        # Normalizar tendencias
        sales_score = min(100, max(0, (sales_trend + 0.1) * 500))
        search_score = min(100, max(0, (search_trend + 0.1) * 500))
        sentiment_score = min(100, max(0, (sentiment + 0.2) * 125))
        
        # Ponderación: ventas 40%, búsquedas 35%, sentimiento 25%
        final_score = (sales_score * 0.4 + search_score * 0.35 + sentiment_score * 0.25)
        
        return min(100, max(0, final_score))
    
    def _calculate_price_trend(self, prices: np.ndarray) -> float:
        """Calcular tendencia de precios"""
        if len(prices) < 2:
            return 0.0
        
        return self._calculate_trend(prices)
    
    def _generate_analysis_summary(self, trends: List[TrendData]) -> Dict[str, Any]:
        """Generar resumen del análisis"""
        total_products = len(trends)
        rising_trends = sum(1 for t in trends if t.current_trend == TrendDirection.RISING)
        falling_trends = sum(1 for t in trends if t.current_trend == TrendDirection.FALLING)
        stable_trends = sum(1 for t in trends if t.current_trend == TrendDirection.STABLE)
        
        avg_trend_score = sum(t.trend_score for t in trends) / total_products if total_products > 0 else 0
        
        return {
            'total_products': total_products,
            'rising_trends': rising_trends,
            'falling_trends': falling_trends,
            'stable_trends': stable_trends,
            'avg_trend_score': round(avg_trend_score, 2),
            'trend_distribution': {
                'rising_percentage': round(rising_trends / total_products * 100, 1) if total_products > 0 else 0,
                'falling_percentage': round(falling_trends / total_products * 100, 1) if total_products > 0 else 0,
                'stable_percentage': round(stable_trends / total_products * 100, 1) if total_products > 0 else 0
            }
        }
    
    async def _generate_predictions(self, data: pd.DataFrame, days_ahead: int) -> List[Dict[str, Any]]:
        """Generar predicciones futuras"""
        # Simular predicciones usando datos históricos
        predictions = []
        
        for product_id in data['product_id'].unique()[:10]:  # Limitar a 10 productos
            product_data = data[data['product_id'] == product_id]
            
            if len(product_data) < 30:  # Necesitamos suficientes datos históricos
                continue
            
            # Simular predicción usando tendencia histórica
            recent_sales = product_data['sales'].tail(30).values
            trend = self._calculate_trend(recent_sales)
            
            # Proyectar ventas futuras
            base_sales = recent_sales[-1]
            predicted_sales = []
            
            for day in range(days_ahead):
                # Aplicar tendencia y estacionalidad
                seasonal_factor = 1 + 0.1 * np.sin(2 * np.pi * day / 7)  # Ciclo semanal
                predicted = base_sales * (1 + trend * (day + 1)) * seasonal_factor
                predicted_sales.append(max(0, int(predicted)))
            
            product_info = product_data.iloc[0]
            
            predictions.append({
                'product_id': product_id,
                'product_name': product_info['product_name'],
                'category': product_info['category'],
                'current_trend': self._determine_trend_direction(trend, trend),
                'predicted_growth': round(trend * 100, 2),
                'confidence_level': round(np.random.uniform(0.6, 0.9), 2),
                'predicted_sales': predicted_sales,
                'recommendations': self._generate_product_recommendations(trend, product_info['category'])
            })
        
        return predictions
    
    def _determine_overall_trend(self, trends: List[Dict[str, Any]]) -> str:
        """Determinar tendencia general del mercado"""
        rising_count = sum(1 for t in trends if t['current_trend'] == TrendDirection.RISING)
        falling_count = sum(1 for t in trends if t['current_trend'] == TrendDirection.FALLING)
        
        total = len(trends)
        if total == 0:
            return "neutral"
        
        rising_percentage = rising_count / total
        falling_percentage = falling_count / total
        
        if rising_percentage > 0.6:
            return "bullish"
        elif falling_percentage > 0.6:
            return "bearish"
        else:
            return "neutral"
    
    def _generate_strategic_recommendations(self, trends: List[Dict[str, Any]], 
                                          category_analysis: Dict[str, Any]) -> List[str]:
        """Generar recomendaciones estratégicas"""
        recommendations = []
        
        # Analizar categorías con mejor rendimiento
        best_categories = sorted(
            category_analysis.items(),
            key=lambda x: x[1]['avg_trend_score'],
            reverse=True
        )[:3]
        
        recommendations.append(f"Enfocar recursos en categorías con mejor tendencia: {', '.join([cat for cat, _ in best_categories])}")
        
        # Identificar productos con mayor potencial
        top_trending = [t for t in trends if t['trend_score'] > 80]
        if top_trending:
            recommendations.append(f"Promocionar productos de alta tendencia: {len(top_trending)} productos identificados")
        
        # Recomendaciones por categoría
        for category, analysis in category_analysis.items():
            if analysis['rising_trends'] > analysis['falling_trends']:
                recommendations.append(f"Incrementar inventario en {category} - tendencia positiva")
            else:
                recommendations.append(f"Revisar estrategia de {category} - tendencia negativa")
        
        return recommendations
    
    def _generate_competitor_strengths(self) -> List[str]:
        """Generar fortalezas de competidores"""
        strengths = [
            "Amplia gama de productos",
            "Precios competitivos",
            "Servicio al cliente excepcional",
            "Presencia en múltiples canales",
            "Innovación tecnológica",
            "Logística eficiente",
            "Marca reconocida",
            "Experiencia de usuario superior"
        ]
        return np.random.choice(strengths, size=np.random.randint(2, 5), replace=False).tolist()
    
    def _generate_competitor_weaknesses(self) -> List[str]:
        """Generar debilidades de competidores"""
        weaknesses = [
            "Precios altos",
            "Gama limitada de productos",
            "Servicio al cliente deficiente",
            "Logística lenta",
            "Falta de innovación",
            "Experiencia de usuario pobre",
            "Presencia limitada en canales",
            "Marca poco conocida"
        ]
        return np.random.choice(weaknesses, size=np.random.randint(1, 4), replace=False).tolist()
    
    def _assess_threat_level(self) -> str:
        """Evaluar nivel de amenaza"""
        threat_levels = ["low", "medium", "high"]
        return np.random.choice(threat_levels, p=[0.3, 0.5, 0.2])
    
    def _analyze_market_position(self, competition_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analizar posición en el mercado"""
        return {
            "our_market_share": np.random.uniform(15, 35),
            "competitive_advantage": "Innovación y experiencia de usuario",
            "market_position": "Líder en innovación",
            "growth_potential": "Alto"
        }
    
    def _analyze_price_competitiveness(self, competition_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analizar competitividad de precios"""
        return {
            "price_position": "Competitivo",
            "price_elasticity": "Media",
            "opportunity_for_premium": "Limitada",
            "recommendation": "Mantener precios actuales"
        }
    
    def _analyze_trend_alignment(self, competition_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analizar alineación de tendencias"""
        return {
            "trend_alignment": "Alto",
            "innovation_gap": "Favorable",
            "market_timing": "Óptimo",
            "recommendation": "Acelerar lanzamientos"
        }
    
    def _identify_opportunities(self, competition_data: Dict[str, Any]) -> List[str]:
        """Identificar oportunidades"""
        return [
            "Expansión a nuevos mercados",
            "Desarrollo de productos premium",
            "Mejora de la experiencia digital",
            "Alianzas estratégicas"
        ]
    
    def _identify_threats(self, competition_data: Dict[str, Any]) -> List[str]:
        """Identificar amenazas"""
        return [
            "Entrada de nuevos competidores",
            "Cambios en preferencias del consumidor",
            "Presión de precios",
            "Disrupción tecnológica"
        ]
    
    def _generate_competitive_recommendations(self, competition_data: Dict[str, Any]) -> List[str]:
        """Generar recomendaciones competitivas"""
        return [
            "Fortalecer diferenciación por innovación",
            "Mejorar experiencia del cliente",
            "Optimizar cadena de suministro",
            "Desarrollar productos únicos",
            "Invertir en marketing digital"
        ]
    
    def _generate_product_recommendations(self, trend: float, category: str) -> List[str]:
        """Generar recomendaciones específicas para productos"""
        recommendations = []
        
        if trend > 0.1:
            recommendations.extend([
                "Incrementar inventario",
                "Promocionar en canales principales",
                "Considerar expansión de línea"
            ])
        elif trend < -0.1:
            recommendations.extend([
                "Revisar estrategia de precios",
                "Evaluar reposicionamiento",
                "Considerar descuentos selectivos"
            ])
        else:
            recommendations.extend([
                "Mantener estrategia actual",
                "Monitorear tendencias de mercado",
                "Optimizar mix de productos"
            ])
        
        return recommendations 