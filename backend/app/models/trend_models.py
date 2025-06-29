"""
Modelos de datos para el análisis de tendencias
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class TrendDirection(str, Enum):
    """Dirección de la tendencia"""
    RISING = "rising"
    FALLING = "falling"
    STABLE = "stable"
    VOLATILE = "volatile"

class CategoryType(str, Enum):
    """Tipos de categorías de productos"""
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    HOME = "home"
    BEAUTY = "beauty"
    SPORTS = "sports"
    BOOKS = "books"
    FOOD = "food"
    OTHER = "other"

class SentimentScore(str, Enum):
    """Puntuaciones de sentimiento"""
    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"

class TrendAnalysisRequest(BaseModel):
    """Solicitud de análisis de tendencias"""
    categories: List[str] = Field(..., description="Categorías a analizar")
    start_date: Optional[str] = Field(None, description="Fecha de inicio (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="Fecha de fin (YYYY-MM-DD)")
    include_sentiment: bool = Field(True, description="Incluir análisis de sentimientos")
    include_predictions: bool = Field(True, description="Incluir predicciones futuras")
    prediction_days: int = Field(30, description="Días para predecir")
    
    class Config:
        schema_extra = {
            "example": {
                "categories": ["electronics", "clothing"],
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
                "include_sentiment": True,
                "include_predictions": True,
                "prediction_days": 30
            }
        }

class TrendData(BaseModel):
    """Datos de una tendencia específica"""
    product_id: str = Field(..., description="ID del producto")
    product_name: str = Field(..., description="Nombre del producto")
    category: str = Field(..., description="Categoría del producto")
    current_trend: TrendDirection = Field(..., description="Dirección actual de la tendencia")
    trend_score: float = Field(..., description="Puntuación de la tendencia (0-100)")
    growth_rate: float = Field(..., description="Tasa de crecimiento (%)")
    search_volume: int = Field(..., description="Volumen de búsquedas")
    sentiment_score: Optional[float] = Field(None, description="Puntuación de sentimiento")
    price_trend: Optional[float] = Field(None, description="Tendencia de precios")
    last_updated: datetime = Field(..., description="Última actualización")

class TrendAnalysisResponse(BaseModel):
    """Respuesta del análisis de tendencias"""
    analysis_id: str = Field(..., description="ID único del análisis")
    request: TrendAnalysisRequest = Field(..., description="Solicitud original")
    trends: List[TrendData] = Field(..., description="Lista de tendencias encontradas")
    summary: Dict[str, Any] = Field(..., description="Resumen del análisis")
    predictions: Optional[List[Dict[str, Any]]] = Field(None, description="Predicciones futuras")
    generated_at: datetime = Field(..., description="Fecha de generación")
    
    class Config:
        schema_extra = {
            "example": {
                "analysis_id": "trend_12345",
                "request": {
                    "categories": ["electronics"],
                    "include_sentiment": True
                },
                "trends": [
                    {
                        "product_id": "prod_001",
                        "product_name": "Smartphone XYZ",
                        "category": "electronics",
                        "current_trend": "rising",
                        "trend_score": 85.5,
                        "growth_rate": 12.3,
                        "search_volume": 15000,
                        "sentiment_score": 0.75,
                        "price_trend": 5.2,
                        "last_updated": "2024-01-15T10:30:00Z"
                    }
                ],
                "summary": {
                    "total_products": 50,
                    "rising_trends": 30,
                    "falling_trends": 10,
                    "stable_trends": 10
                },
                "generated_at": "2024-01-15T10:30:00Z"
            }
        }

class ProductRecommendation(BaseModel):
    """Recomendación de producto"""
    product_id: str = Field(..., description="ID del producto")
    product_name: str = Field(..., description="Nombre del producto")
    category: str = Field(..., description="Categoría del producto")
    recommendation_score: float = Field(..., description="Puntuación de recomendación (0-100)")
    confidence_level: float = Field(..., description="Nivel de confianza (0-1)")
    reasoning: List[str] = Field(..., description="Razones de la recomendación")
    expected_growth: float = Field(..., description="Crecimiento esperado (%)")
    optimal_price: Optional[float] = Field(None, description="Precio óptimo sugerido")
    promotion_suggestions: List[str] = Field(..., description="Sugerencias de promoción")
    
    class Config:
        schema_extra = {
            "example": {
                "product_id": "prod_001",
                "product_name": "Smartphone XYZ",
                "category": "electronics",
                "recommendation_score": 92.5,
                "confidence_level": 0.85,
                "reasoning": [
                    "Alta tendencia de búsqueda",
                    "Sentimiento positivo en reseñas",
                    "Crecimiento sostenido en ventas"
                ],
                "expected_growth": 15.3,
                "optimal_price": 299.99,
                "promotion_suggestions": [
                    "Descuento del 10% en fin de semana",
                    "Promoción en redes sociales",
                    "Bundle con accesorios"
                ]
            }
        }

class PromotionStrategy(BaseModel):
    """Estrategia de promoción"""
    strategy_id: str = Field(..., description="ID de la estrategia")
    name: str = Field(..., description="Nombre de la estrategia")
    description: str = Field(..., description="Descripción de la estrategia")
    target_categories: List[str] = Field(..., description="Categorías objetivo")
    budget_required: float = Field(..., description="Presupuesto requerido")
    expected_roi: float = Field(..., description="ROI esperado (%)")
    duration_days: int = Field(..., description="Duración en días")
    implementation_steps: List[str] = Field(..., description="Pasos de implementación")
    risk_level: str = Field(..., description="Nivel de riesgo")
    success_metrics: List[str] = Field(..., description="Métricas de éxito")
    
    class Config:
        schema_extra = {
            "example": {
                "strategy_id": "promo_001",
                "name": "Descuentos Flash de Fin de Semana",
                "description": "Descuentos del 20-30% en productos de alta tendencia",
                "target_categories": ["electronics", "clothing"],
                "budget_required": 5000.0,
                "expected_roi": 150.0,
                "duration_days": 3,
                "implementation_steps": [
                    "Identificar productos con mayor tendencia",
                    "Configurar descuentos automáticos",
                    "Lanzar campaña en redes sociales"
                ],
                "risk_level": "medium",
                "success_metrics": [
                    "Incremento en ventas del 40%",
                    "Nuevos clientes adquiridos",
                    "Engagement en redes sociales"
                ]
            }
        }

class SalesMetrics(BaseModel):
    """Métricas de ventas"""
    period_start: datetime = Field(..., description="Inicio del período")
    period_end: datetime = Field(..., description="Fin del período")
    total_sales: float = Field(..., description="Ventas totales")
    total_orders: int = Field(..., description="Total de pedidos")
    average_order_value: float = Field(..., description="Valor promedio por pedido")
    sales_by_category: Dict[str, float] = Field(..., description="Ventas por categoría")
    top_products: List[Dict[str, Any]] = Field(..., description="Productos más vendidos")
    growth_rate: float = Field(..., description="Tasa de crecimiento vs período anterior")
    conversion_rate: float = Field(..., description="Tasa de conversión")
    
    class Config:
        schema_extra = {
            "example": {
                "period_start": "2024-01-01T00:00:00Z",
                "period_end": "2024-01-31T23:59:59Z",
                "total_sales": 125000.0,
                "total_orders": 1250,
                "average_order_value": 100.0,
                "sales_by_category": {
                    "electronics": 50000.0,
                    "clothing": 40000.0,
                    "home": 35000.0
                },
                "top_products": [
                    {
                        "product_id": "prod_001",
                        "product_name": "Smartphone XYZ",
                        "units_sold": 150,
                        "revenue": 45000.0
                    }
                ],
                "growth_rate": 12.5,
                "conversion_rate": 3.2
            }
        }

class SentimentAnalysis(BaseModel):
    """Análisis de sentimiento"""
    product_id: Optional[str] = Field(None, description="ID del producto")
    category: Optional[str] = Field(None, description="Categoría")
    overall_sentiment: SentimentScore = Field(..., description="Sentimiento general")
    sentiment_score: float = Field(..., description="Puntuación de sentimiento (-1 a 1)")
    total_reviews: int = Field(..., description="Total de reseñas analizadas")
    positive_reviews: int = Field(..., description="Reseñas positivas")
    negative_reviews: int = Field(..., description="Reseñas negativas")
    neutral_reviews: int = Field(..., description="Reseñas neutrales")
    common_keywords: List[str] = Field(..., description="Palabras clave comunes")
    sentiment_trend: TrendDirection = Field(..., description="Tendencia del sentimiento")
    last_updated: datetime = Field(..., description="Última actualización")
    
    class Config:
        schema_extra = {
            "example": {
                "product_id": "prod_001",
                "category": "electronics",
                "overall_sentiment": "positive",
                "sentiment_score": 0.75,
                "total_reviews": 500,
                "positive_reviews": 375,
                "negative_reviews": 50,
                "neutral_reviews": 75,
                "common_keywords": ["excelente", "calidad", "rápido", "recomiendo"],
                "sentiment_trend": "rising",
                "last_updated": "2024-01-15T10:30:00Z"
            }
        } 