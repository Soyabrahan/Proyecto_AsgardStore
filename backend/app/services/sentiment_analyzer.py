"""
Servicio de Análisis de Sentimientos
Implementa procesamiento de lenguaje natural para analizar sentimientos en reseñas y comentarios
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging
import re
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import uuid

from ..models.trend_models import SentimentAnalysis, SentimentScore

logger = logging.getLogger(__name__)

# Descargar recursos de NLTK (solo una vez)
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

class SentimentAnalyzer:
    """Analizador de sentimientos con NLP"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('spanish') + stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.sample_reviews = self._generate_sample_reviews()
        
    def _generate_sample_reviews(self) -> pd.DataFrame:
        """Generar reseñas de ejemplo para demostración"""
        np.random.seed(42)
        
        # Reseñas positivas
        positive_reviews = [
            "Excelente producto, muy buena calidad y rápido envío. Lo recomiendo totalmente!",
            "Increíble experiencia de compra. El producto superó mis expectativas.",
            "Muy satisfecho con la compra. El servicio al cliente fue excepcional.",
            "Producto de alta calidad, vale cada centavo invertido.",
            "Envío rápido y producto en perfectas condiciones. Muy recomendado.",
            "Excelente relación calidad-precio. Definitivamente volveré a comprar.",
            "El producto llegó antes de lo esperado y en perfecto estado.",
            "Muy buena atención y producto de primera calidad.",
            "Superó todas mis expectativas. Excelente servicio.",
            "Producto fantástico, muy duradero y funcional."
        ]
        
        # Reseñas neutrales
        neutral_reviews = [
            "El producto cumple con lo esperado, nada más que agregar.",
            "Envío normal, producto correcto.",
            "Buen producto, precio razonable.",
            "Cumple su función, sin más comentarios.",
            "Producto estándar, entrega a tiempo.",
            "Calidad aceptable para el precio.",
            "Funciona como se describe, sin sorpresas.",
            "Producto regular, ni muy bueno ni muy malo.",
            "Entrega puntual, producto correcto.",
            "Aceptable para el uso que le doy."
        ]
        
        # Reseñas negativas
        negative_reviews = [
            "Muy decepcionado con la calidad del producto. No lo recomiendo.",
            "Envío tardío y producto defectuoso. Pésimo servicio.",
            "Calidad muy inferior a lo esperado. No vale el precio.",
            "Producto llegó dañado y el servicio al cliente fue terrible.",
            "Muy mala experiencia de compra. No volveré a comprar aquí.",
            "Producto de baja calidad, se rompió en poco tiempo.",
            "Envío muy lento y producto no cumple las expectativas.",
            "Precio alto para la calidad que ofrece. No lo recomiendo.",
            "Mala atención al cliente y producto defectuoso.",
            "Experiencia muy negativa, no recomiendo esta tienda."
        ]
        
        # Generar datos de reseñas
        reviews_data = []
        base_date = datetime.now() - timedelta(days=365)
        
        # Productos de ejemplo
        products = [
            "Smartphone Galaxy S24", "iPhone 15 Pro", "Laptop Dell XPS", 
            "Nike Air Max", "Adidas Ultraboost", "Samsung TV 4K",
            "Sony Headphones", "MacBook Pro", "iPad Air", "Apple Watch"
        ]
        
        categories = ["electronics"] * 6 + ["sports"] * 4
        
        for i, (product, category) in enumerate(zip(products, categories)):
            # Generar múltiples reseñas por producto
            for review_idx in range(20):
                # Distribuir sentimientos: 60% positivas, 25% neutrales, 15% negativas
                sentiment_choice = np.random.choice(['positive', 'neutral', 'negative'], 
                                                   p=[0.6, 0.25, 0.15])
                
                if sentiment_choice == 'positive':
                    review_text = np.random.choice(positive_reviews)
                    base_sentiment = np.random.uniform(0.3, 0.8)
                elif sentiment_choice == 'neutral':
                    review_text = np.random.choice(neutral_reviews)
                    base_sentiment = np.random.uniform(-0.1, 0.3)
                else:
                    review_text = np.random.choice(negative_reviews)
                    base_sentiment = np.random.uniform(-0.8, -0.2)
                
                # Añadir variabilidad
                sentiment_score = base_sentiment + np.random.normal(0, 0.1)
                sentiment_score = max(-1, min(1, sentiment_score))
                
                # Generar fecha aleatoria
                days_ago = np.random.randint(0, 365)
                review_date = base_date + timedelta(days=days_ago)
                
                reviews_data.append({
                    'review_id': f'review_{i:03d}_{review_idx:03d}',
                    'product_id': f'prod_{i:03d}',
                    'product_name': product,
                    'category': category,
                    'review_text': review_text,
                    'sentiment_score': sentiment_score,
                    'rating': self._sentiment_to_rating(sentiment_score),
                    'review_date': review_date,
                    'helpful_votes': np.random.randint(0, 50),
                    'review_length': len(review_text)
                })
        
        return pd.DataFrame(reviews_data)
    
    async def get_sentiment_metrics(self, product_id: Optional[str] = None, 
                                   category: Optional[str] = None, 
                                   limit: int = 20) -> List[SentimentAnalysis]:
        """Obtener métricas de sentimiento"""
        try:
            # Filtrar datos según parámetros
            data = self.sample_reviews.copy()
            
            if product_id:
                data = data[data['product_id'] == product_id]
            
            if category:
                data = data[data['category'] == category]
            
            if data.empty:
                raise ValueError("No hay datos disponibles para los filtros especificados")
            
            # Agrupar por producto si no se especifica uno
            if not product_id:
                sentiment_analyses = []
                
                for product_id in data['product_id'].unique()[:limit]:
                    product_data = data[data['product_id'] == product_id]
                    
                    analysis = self._analyze_product_sentiment(product_data)
                    sentiment_analyses.append(analysis)
                
                return sentiment_analyses
            else:
                # Análisis para un producto específico
                analysis = self._analyze_product_sentiment(data)
                return [analysis]
                
        except Exception as e:
            logger.error(f"Error obteniendo métricas de sentimiento: {e}")
            raise
    
    async def analyze_text_sentiment(self, text: str) -> Dict[str, Any]:
        """Analizar sentimiento de un texto específico"""
        try:
            # Preprocesar texto
            processed_text = self._preprocess_text(text)
            
            # Análisis con TextBlob
            blob = TextBlob(processed_text)
            sentiment_score = blob.sentiment.polarity
            
            # Análisis más detallado
            analysis = {
                'text': text,
                'processed_text': processed_text,
                'sentiment_score': round(sentiment_score, 3),
                'sentiment_label': self._score_to_label(sentiment_score),
                'subjectivity': round(blob.sentiment.subjectivity, 3),
                'word_count': len(text.split()),
                'key_phrases': self._extract_key_phrases(text),
                'emotion_indicators': self._detect_emotions(text),
                'analyzed_at': datetime.now().isoformat()
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analizando sentimiento de texto: {e}")
            raise
    
    async def get_sentiment_trends(self, days: int = 30, category: Optional[str] = None) -> Dict[str, Any]:
        """Obtener tendencias de sentimiento en el tiempo"""
        try:
            data = self.sample_reviews.copy()
            
            if category:
                data = data[data['category'] == category]
            
            # Filtrar por fecha
            cutoff_date = datetime.now() - timedelta(days=days)
            data = data[data['review_date'] >= cutoff_date]
            
            if data.empty:
                raise ValueError("No hay datos disponibles para el período especificado")
            
            # Agrupar por fecha y calcular sentimiento promedio
            daily_sentiment = data.groupby(data['review_date'].dt.date).agg({
                'sentiment_score': ['mean', 'count'],
                'rating': 'mean'
            }).reset_index()
            
            daily_sentiment.columns = ['date', 'avg_sentiment', 'review_count', 'avg_rating']
            
            # Calcular tendencia
            sentiment_trend = self._calculate_sentiment_trend(daily_sentiment['avg_sentiment'].values)
            
            # Análisis por categoría
            category_sentiment = {}
            if not category:
                for cat in data['category'].unique():
                    cat_data = data[data['category'] == cat]
                    category_sentiment[cat] = {
                        'avg_sentiment': round(cat_data['sentiment_score'].mean(), 3),
                        'review_count': len(cat_data),
                        'positive_percentage': round(len(cat_data[cat_data['sentiment_score'] > 0.1]) / len(cat_data) * 100, 1),
                        'negative_percentage': round(len(cat_data[cat_data['sentiment_score'] < -0.1]) / len(cat_data) * 100, 1)
                    }
            
            return {
                'period_days': days,
                'total_reviews': len(data),
                'overall_sentiment': round(data['sentiment_score'].mean(), 3),
                'sentiment_trend': sentiment_trend,
                'daily_data': daily_sentiment.to_dict('records'),
                'category_breakdown': category_sentiment,
                'top_keywords': self._extract_top_keywords(data['review_text'].tolist()),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo tendencias de sentimiento: {e}")
            raise
    
    def _analyze_product_sentiment(self, product_data: pd.DataFrame) -> SentimentAnalysis:
        """Analizar sentimiento de un producto específico"""
        sentiment_scores = product_data['sentiment_score'].values
        total_reviews = len(product_data)
        
        # Calcular métricas
        avg_sentiment = np.mean(sentiment_scores)
        positive_reviews = len(sentiment_scores[sentiment_scores > 0.1])
        negative_reviews = len(sentiment_scores[sentiment_scores < -0.1])
        neutral_reviews = total_reviews - positive_reviews - negative_reviews
        
        # Determinar sentimiento general
        if avg_sentiment > 0.3:
            overall_sentiment = SentimentScore.POSITIVE
        elif avg_sentiment > -0.1:
            overall_sentiment = SentimentScore.NEUTRAL
        else:
            overall_sentiment = SentimentScore.NEGATIVE
        
        # Extraer palabras clave
        all_text = ' '.join(product_data['review_text'].tolist())
        common_keywords = self._extract_key_phrases(all_text)
        
        # Determinar tendencia del sentimiento
        if len(sentiment_scores) >= 7:
            recent_scores = sentiment_scores[-7:]  # Últimos 7 días
            older_scores = sentiment_scores[:-7] if len(sentiment_scores) > 7 else sentiment_scores
            
            recent_avg = np.mean(recent_scores)
            older_avg = np.mean(older_scores)
            
            if recent_avg > older_avg + 0.1:
                sentiment_trend = "rising"
            elif recent_avg < older_avg - 0.1:
                sentiment_trend = "falling"
            else:
                sentiment_trend = "stable"
        else:
            sentiment_trend = "stable"
        
        product_info = product_data.iloc[0]
        
        return SentimentAnalysis(
            product_id=product_info['product_id'],
            category=product_info['category'],
            overall_sentiment=overall_sentiment,
            sentiment_score=round(avg_sentiment, 3),
            total_reviews=total_reviews,
            positive_reviews=positive_reviews,
            negative_reviews=negative_reviews,
            neutral_reviews=neutral_reviews,
            common_keywords=common_keywords[:10],  # Top 10 keywords
            sentiment_trend=sentiment_trend,
            last_updated=datetime.now()
        )
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocesar texto para análisis de sentimientos"""
        # Convertir a minúsculas
        text = text.lower()
        
        # Remover caracteres especiales pero mantener acentos
        text = re.sub(r'[^a-zA-ZáéíóúñÁÉÍÓÚÑ\s]', ' ', text)
        
        # Tokenizar
        tokens = word_tokenize(text)
        
        # Remover stop words y lematizar
        processed_tokens = []
        for token in tokens:
            if token not in self.stop_words and len(token) > 2:
                lemmatized = self.lemmatizer.lemmatize(token)
                processed_tokens.append(lemmatized)
        
        return ' '.join(processed_tokens)
    
    def _score_to_label(self, score: float) -> SentimentScore:
        """Convertir puntuación de sentimiento a etiqueta"""
        if score > 0.3:
            return SentimentScore.POSITIVE
        elif score > -0.1:
            return SentimentScore.NEUTRAL
        else:
            return SentimentScore.NEGATIVE
    
    def _sentiment_to_rating(self, sentiment_score: float) -> int:
        """Convertir sentimiento a calificación de 1-5"""
        if sentiment_score > 0.5:
            return 5
        elif sentiment_score > 0.2:
            return 4
        elif sentiment_score > -0.1:
            return 3
        elif sentiment_score > -0.4:
            return 2
        else:
            return 1
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extraer frases clave del texto"""
        # Palabras positivas y negativas comunes
        positive_words = [
            'excelente', 'increíble', 'fantástico', 'perfecto', 'genial', 'maravilloso',
            'excellent', 'amazing', 'fantastic', 'perfect', 'great', 'wonderful',
            'bueno', 'buena', 'buen', 'good', 'nice', 'quality', 'calidad'
        ]
        
        negative_words = [
            'terrible', 'pésimo', 'malo', 'defectuoso', 'decepcionado', 'horrible',
            'terrible', 'awful', 'bad', 'defective', 'disappointed', 'horrible',
            'mal', 'mala', 'problema', 'problem', 'error', 'falla'
        ]
        
        # Buscar palabras clave
        text_lower = text.lower()
        key_phrases = []
        
        for word in positive_words + negative_words:
            if word in text_lower:
                key_phrases.append(word)
        
        return key_phrases[:10]  # Limitar a 10 frases
    
    def _detect_emotions(self, text: str) -> Dict[str, float]:
        """Detectar emociones en el texto"""
        text_lower = text.lower()
        
        emotions = {
            'joy': 0.0,
            'anger': 0.0,
            'sadness': 0.0,
            'surprise': 0.0,
            'fear': 0.0
        }
        
        # Palabras asociadas con emociones
        emotion_words = {
            'joy': ['feliz', 'contento', 'alegre', 'satisfecho', 'happy', 'joyful', 'pleased'],
            'anger': ['enojado', 'furioso', 'molesto', 'irritado', 'angry', 'furious', 'annoyed'],
            'sadness': ['triste', 'decepcionado', 'desilusionado', 'sad', 'disappointed'],
            'surprise': ['sorprendido', 'asombrado', 'increíble', 'surprised', 'amazed'],
            'fear': ['preocupado', 'nervioso', 'ansioso', 'worried', 'nervous', 'anxious']
        }
        
        for emotion, words in emotion_words.items():
            count = sum(1 for word in words if word in text_lower)
            emotions[emotion] = count / len(words) if words else 0.0
        
        return emotions
    
    def _calculate_sentiment_trend(self, sentiment_values: np.ndarray) -> str:
        """Calcular tendencia del sentimiento"""
        if len(sentiment_values) < 2:
            return "stable"
        
        # Calcular tendencia usando regresión lineal
        x = np.arange(len(sentiment_values))
        slope = np.polyfit(x, sentiment_values, 1)[0]
        
        if slope > 0.01:
            return "rising"
        elif slope < -0.01:
            return "falling"
        else:
            return "stable"
    
    def _extract_top_keywords(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Extraer palabras clave más frecuentes"""
        # Combinar todos los textos
        all_text = ' '.join(texts)
        processed_text = self._preprocess_text(all_text)
        
        # Contar frecuencia de palabras
        words = processed_text.split()
        word_freq = {}
        
        for word in words:
            if len(word) > 3:  # Solo palabras de más de 3 caracteres
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Ordenar por frecuencia
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Retornar top 10 con información adicional
        top_keywords = []
        for word, freq in sorted_words[:10]:
            # Determinar sentimiento de la palabra
            sentiment = self._analyze_word_sentiment(word)
            
            top_keywords.append({
                'word': word,
                'frequency': freq,
                'sentiment': sentiment,
                'percentage': round(freq / len(words) * 100, 2)
            })
        
        return top_keywords
    
    def _analyze_word_sentiment(self, word: str) -> str:
        """Analizar sentimiento de una palabra específica"""
        positive_words = {
            'excelente', 'increíble', 'fantástico', 'perfecto', 'genial', 'maravilloso',
            'bueno', 'buena', 'buen', 'calidad', 'rápido', 'durable', 'funcional',
            'excellent', 'amazing', 'fantastic', 'perfect', 'great', 'wonderful',
            'good', 'quality', 'fast', 'durable', 'functional'
        }
        
        negative_words = {
            'terrible', 'pésimo', 'malo', 'defectuoso', 'decepcionado', 'horrible',
            'mal', 'mala', 'problema', 'error', 'falla', 'lento', 'frágil',
            'terrible', 'awful', 'bad', 'defective', 'disappointed', 'horrible',
            'problem', 'error', 'slow', 'fragile'
        }
        
        if word in positive_words:
            return "positive"
        elif word in negative_words:
            return "negative"
        else:
            return "neutral" 