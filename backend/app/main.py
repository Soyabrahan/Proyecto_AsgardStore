"""
Backend Principal - Análisis Predictivo de Tendencias con IA
AsgardStore
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import logging

# Importar modelos y servicios
from .models.trend_models import (
    TrendAnalysisRequest, 
    TrendAnalysisResponse,
    ProductRecommendation,
    PromotionStrategy,
    SalesMetrics,
    SentimentAnalysis
)
from .services.trend_analyzer import TrendAnalyzer
from .services.sentiment_analyzer import SentimentAnalyzer
from .services.prediction_engine import PredictionEngine
from .services.recommendation_system import RecommendationSystem

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="AsgardStore - Análisis Predictivo de Tendencias",
    description="Sistema de IA para análisis predictivo de tendencias y recomendaciones estratégicas",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar servicios
trend_analyzer = TrendAnalyzer()
sentiment_analyzer = SentimentAnalyzer()
prediction_engine = PredictionEngine()
recommendation_system = RecommendationSystem()

@app.get("/")
async def root():
    """Endpoint raíz con información del sistema"""
    return {
        "message": "AsgardStore - Análisis Predictivo de Tendencias con IA",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "trends": "/api/trends",
            "recommendations": "/api/recommendations", 
            "metrics": "/api/metrics",
            "reports": "/api/reports"
        }
    }

@app.get("/health")
async def health_check():
    """Verificación de salud del sistema"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "trend_analyzer": "active",
            "sentiment_analyzer": "active", 
            "prediction_engine": "active",
            "recommendation_system": "active"
        }
    }

# ==================== ENDPOINTS DE TENDENCIAS ====================

@app.get("/api/trends/current", response_model=List[Dict[str, Any]])
async def get_current_trends(
    category: Optional[str] = None,
    limit: int = 10
):
    """
    Obtener tendencias actuales del mercado
    """
    try:
        trends = await trend_analyzer.get_current_trends(category, limit)
        return trends
    except Exception as e:
        logger.error(f"Error obteniendo tendencias actuales: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trends/prediction", response_model=List[Dict[str, Any]])
async def get_trend_predictions(
    days_ahead: int = 30,
    category: Optional[str] = None
):
    """
    Obtener predicciones de tendencias futuras
    """
    try:
        predictions = await prediction_engine.predict_trends(days_ahead, category)
        return predictions
    except Exception as e:
        logger.error(f"Error obteniendo predicciones: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/trends/analyze", response_model=TrendAnalysisResponse)
async def analyze_trends(request: TrendAnalysisRequest):
    """
    Análisis personalizado de tendencias
    """
    try:
        analysis = await trend_analyzer.analyze_custom_trends(request)
        return analysis
    except Exception as e:
        logger.error(f"Error en análisis de tendencias: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ENDPOINTS DE RECOMENDACIONES ====================

@app.get("/api/recommendations/products", response_model=List[ProductRecommendation])
async def get_product_recommendations(
    category: Optional[str] = None,
    limit: int = 10
):
    """
    Obtener recomendaciones de productos basadas en tendencias
    """
    try:
        recommendations = await recommendation_system.get_product_recommendations(
            category, limit
        )
        return recommendations
    except Exception as e:
        logger.error(f"Error obteniendo recomendaciones de productos: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recommendations/promotions", response_model=List[PromotionStrategy])
async def get_promotion_strategies(
    budget: Optional[float] = None,
    target_category: Optional[str] = None
):
    """
    Obtener estrategias de promoción recomendadas
    """
    try:
        strategies = await recommendation_system.get_promotion_strategies(
            budget, target_category
        )
        return strategies
    except Exception as e:
        logger.error(f"Error obteniendo estrategias de promoción: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recommendations/custom", response_model=Dict[str, Any])
async def get_custom_recommendations(
    categories: List[str],
    budget: float,
    timeframe: int = 30
):
    """
    Obtener recomendaciones personalizadas
    """
    try:
        recommendations = await recommendation_system.get_custom_recommendations(
            categories, budget, timeframe
        )
        return recommendations
    except Exception as e:
        logger.error(f"Error obteniendo recomendaciones personalizadas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ENDPOINTS DE MÉTRICAS ====================

@app.get("/api/metrics/sales", response_model=SalesMetrics)
async def get_sales_metrics(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    category: Optional[str] = None
):
    """
    Obtener métricas de ventas
    """
    try:
        metrics = await trend_analyzer.get_sales_metrics(start_date, end_date, category)
        return metrics
    except Exception as e:
        logger.error(f"Error obteniendo métricas de ventas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/metrics/sentiment", response_model=List[SentimentAnalysis])
async def get_sentiment_metrics(
    product_id: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 20
):
    """
    Obtener análisis de sentimientos
    """
    try:
        sentiment_data = await sentiment_analyzer.get_sentiment_metrics(
            product_id, category, limit
        )
        return sentiment_data
    except Exception as e:
        logger.error(f"Error obteniendo métricas de sentimiento: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ENDPOINTS DE REPORTES ====================

@app.get("/api/reports/trends")
async def generate_trends_report(
    format: str = "json",
    include_predictions: bool = True
):
    """
    Generar reporte completo de tendencias
    """
    try:
        report = await trend_analyzer.generate_trends_report(format, include_predictions)
        return report
    except Exception as e:
        logger.error(f"Error generando reporte de tendencias: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports/competition")
async def generate_competition_report(
    competitors: List[str],
    metrics: List[str] = ["price", "trends", "sentiment"]
):
    """
    Generar reporte de análisis competitivo
    """
    try:
        report = await trend_analyzer.generate_competition_report(competitors, metrics)
        return report
    except Exception as e:
        logger.error(f"Error generando reporte de competencia: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== MANEJO DE ERRORES ====================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Manejador global de excepciones"""
    logger.error(f"Error no manejado: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Error interno del servidor",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 