"""
Sistema de Recomendaciones con IA
Implementa algoritmos de recomendación personalizada y estrategias de promoción
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import json
import uuid

from ..models.trend_models import (
    ProductRecommendation,
    PromotionStrategy
)

logger = logging.getLogger(__name__)

class RecommendationSystem:
    """Sistema de recomendaciones con algoritmos de IA"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.clustering_model = KMeans(n_clusters=8, random_state=42)
        self.sample_data = self._generate_sample_data()
        self.user_profiles = self._generate_user_profiles()
        
    def _generate_sample_data(self) -> pd.DataFrame:
        """Generar datos de ejemplo para el sistema de recomendaciones"""
        np.random.seed(42)
        
        # Productos con características detalladas
        products = [
            {
                'id': 'prod_001', 'name': 'Smartphone Galaxy S24', 'category': 'electronics',
                'price': 899.99, 'rating': 4.5, 'features': '5G, 128GB, Android, Camera 108MP',
                'tags': 'smartphone, android, samsung, 5g, camera'
            },
            {
                'id': 'prod_002', 'name': 'iPhone 15 Pro', 'category': 'electronics',
                'price': 999.99, 'rating': 4.7, 'features': '5G, 256GB, iOS, Camera 48MP',
                'tags': 'smartphone, ios, apple, 5g, camera, premium'
            },
            {
                'id': 'prod_003', 'name': 'Laptop Dell XPS 13', 'category': 'electronics',
                'price': 1299.99, 'rating': 4.6, 'features': 'Intel i7, 16GB RAM, 512GB SSD',
                'tags': 'laptop, dell, intel, premium, business'
            },
            {
                'id': 'prod_004', 'name': 'Nike Air Max 270', 'category': 'sports',
                'price': 129.99, 'rating': 4.4, 'features': 'Air Max, Comfortable, Stylish',
                'tags': 'shoes, nike, running, comfortable, stylish'
            },
            {
                'id': 'prod_005', 'name': 'Adidas Ultraboost 22', 'category': 'sports',
                'price': 179.99, 'rating': 4.5, 'features': 'Boost Technology, Lightweight',
                'tags': 'shoes, adidas, running, boost, lightweight'
            },
            {
                'id': 'prod_006', 'name': 'Samsung TV 4K 55"', 'category': 'electronics',
                'price': 699.99, 'rating': 4.3, 'features': '4K UHD, Smart TV, HDR',
                'tags': 'tv, samsung, 4k, smart, entertainment'
            },
            {
                'id': 'prod_007', 'name': 'Sony WH-1000XM4', 'category': 'electronics',
                'price': 349.99, 'rating': 4.8, 'features': 'Noise Cancelling, 30h Battery',
                'tags': 'headphones, sony, noise-cancelling, wireless, premium'
            },
            {
                'id': 'prod_008', 'name': 'MacBook Pro 14"', 'category': 'electronics',
                'price': 1999.99, 'rating': 4.9, 'features': 'M2 Pro, 16GB RAM, 512GB SSD',
                'tags': 'laptop, macbook, apple, m2, premium, professional'
            },
            {
                'id': 'prod_009', 'name': 'iPad Air 5th Gen', 'category': 'electronics',
                'price': 599.99, 'rating': 4.6, 'features': 'M1 Chip, 10.9", 64GB',
                'tags': 'tablet, ipad, apple, m1, portable'
            },
            {
                'id': 'prod_010', 'name': 'Apple Watch Series 9', 'category': 'electronics',
                'price': 399.99, 'rating': 4.7, 'features': 'GPS, Heart Rate, Fitness',
                'tags': 'watch, apple, fitness, health, smartwatch'
            },
            {
                'id': 'prod_011', 'name': 'Nike Running Shoes', 'category': 'sports',
                'price': 89.99, 'rating': 4.3, 'features': 'Lightweight, Breathable',
                'tags': 'shoes, nike, running, lightweight, breathable'
            },
            {
                'id': 'prod_012', 'name': 'Adidas Soccer Ball', 'category': 'sports',
                'price': 49.99, 'rating': 4.2, 'features': 'Professional, FIFA Approved',
                'tags': 'soccer, ball, adidas, professional, sports'
            },
            {
                'id': 'prod_013', 'name': 'Basketball Nike Elite', 'category': 'sports',
                'price': 69.99, 'rating': 4.4, 'features': 'Indoor/Outdoor, Official Size',
                'tags': 'basketball, nike, sports, indoor, outdoor'
            },
            {
                'id': 'prod_014', 'name': 'Yoga Mat Premium', 'category': 'sports',
                'price': 39.99, 'rating': 4.1, 'features': 'Non-slip, Eco-friendly',
                'tags': 'yoga, mat, fitness, eco-friendly, non-slip'
            },
            {
                'id': 'prod_015', 'name': 'Dumbbells Set 20kg', 'category': 'sports',
                'price': 79.99, 'rating': 4.0, 'features': 'Adjustable, Rubber Coated',
                'tags': 'dumbbells, fitness, strength, adjustable, rubber'
            },
            {
                'id': 'prod_016', 'name': 'Treadmill Pro', 'category': 'sports',
                'price': 899.99, 'rating': 4.2, 'features': 'Motorized, 12 Programs',
                'tags': 'treadmill, fitness, cardio, motorized, home-gym'
            },
            {
                'id': 'prod_017', 'name': 'Makeup Palette Pro', 'category': 'beauty',
                'price': 49.99, 'rating': 4.3, 'features': '18 Colors, Long-lasting',
                'tags': 'makeup, palette, colors, long-lasting, beauty'
            },
            {
                'id': 'prod_018', 'name': 'Skincare Set Complete', 'category': 'beauty',
                'price': 89.99, 'rating': 4.5, 'features': 'Cleanser, Toner, Moisturizer',
                'tags': 'skincare, beauty, cleanser, toner, moisturizer'
            },
            {
                'id': 'prod_019', 'name': 'Hair Dryer Professional', 'category': 'beauty',
                'price': 129.99, 'rating': 4.4, 'features': '2000W, Ionic Technology',
                'tags': 'hair-dryer, beauty, professional, ionic, 2000w'
            },
            {
                'id': 'prod_020', 'name': 'Perfume Luxury Collection', 'category': 'beauty',
                'price': 199.99, 'rating': 4.6, 'features': 'Long-lasting, Unique Scent',
                'tags': 'perfume, luxury, beauty, long-lasting, unique'
            }
        ]
        
        # Convertir a DataFrame
        df = pd.DataFrame(products)
        
        # Agregar métricas de ventas y tendencias
        df['sales_volume'] = np.random.randint(100, 1000, len(df))
        df['trend_score'] = np.random.uniform(0.3, 0.9, len(df))
        df['profit_margin'] = np.random.uniform(0.15, 0.45, len(df))
        df['stock_level'] = np.random.randint(10, 100, len(df))
        
        return df
    
    def _generate_user_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Generar perfiles de usuario para recomendaciones personalizadas"""
        profiles = {
            'tech_enthusiast': {
                'interests': ['electronics', 'gadgets', 'technology'],
                'price_range': (500, 2000),
                'preferred_brands': ['Apple', 'Samsung', 'Sony'],
                'purchase_frequency': 'high'
            },
            'fitness_fanatic': {
                'interests': ['sports', 'fitness', 'health'],
                'price_range': (50, 300),
                'preferred_brands': ['Nike', 'Adidas'],
                'purchase_frequency': 'medium'
            },
            'beauty_lover': {
                'interests': ['beauty', 'skincare', 'makeup'],
                'price_range': (30, 200),
                'preferred_brands': ['Luxury', 'Professional'],
                'purchase_frequency': 'high'
            },
            'budget_conscious': {
                'interests': ['electronics', 'sports', 'beauty'],
                'price_range': (20, 150),
                'preferred_brands': ['Generic', 'Budget'],
                'purchase_frequency': 'low'
            },
            'premium_buyer': {
                'interests': ['electronics', 'luxury', 'premium'],
                'price_range': (500, 3000),
                'preferred_brands': ['Apple', 'Premium', 'Luxury'],
                'purchase_frequency': 'medium'
            }
        }
        return profiles
    
    async def get_product_recommendations(self, category: Optional[str] = None, limit: int = 10) -> List[ProductRecommendation]:
        """Obtener recomendaciones de productos basadas en tendencias y análisis de IA"""
        try:
            # Filtrar por categoría si se especifica
            if category:
                data = self.sample_data[self.sample_data['category'] == category].copy()
            else:
                data = self.sample_data.copy()
            
            # Calcular puntuación de recomendación para cada producto
            recommendations = []
            for _, product in data.iterrows():
                # Calcular puntuación basada en múltiples factores
                recommendation_score = self._calculate_recommendation_score(product)
                
                # Generar razones de recomendación
                reasons = self._generate_recommendation_reasons(product)
                
                # Crear objeto de recomendación
                recommendation = ProductRecommendation(
                    product_id=product['id'],
                    product_name=product['name'],
                    category=product['category'],
                    price=product['price'],
                    recommendation_score=round(recommendation_score, 2),
                    reasons=reasons,
                    estimated_demand=round(product['sales_volume'] * (1 + product['trend_score']), 0),
                    profit_potential=round(product['price'] * product['profit_margin'], 2),
                    stock_status=self._get_stock_status(product['stock_level']),
                    last_updated=datetime.now().isoformat()
                )
                
                recommendations.append(recommendation)
            
            # Ordenar por puntuación de recomendación y limitar resultados
            recommendations.sort(key=lambda x: x.recommendation_score, reverse=True)
            return recommendations[:limit]
            
        except Exception as e:
            logger.error(f"Error obteniendo recomendaciones de productos: {e}")
            raise
    
    async def get_promotion_strategies(self, budget: Optional[float] = None, target_category: Optional[str] = None) -> List[PromotionStrategy]:
        """Obtener estrategias de promoción recomendadas basadas en análisis de IA"""
        try:
            # Filtrar productos por categoría si se especifica
            if target_category:
                data = self.sample_data[self.sample_data['category'] == target_category].copy()
            else:
                data = self.sample_data.copy()
            
            # Si no se especifica presupuesto, usar uno por defecto
            if not budget:
                budget = 5000.0
            
            strategies = []
            
            # Estrategia 1: Descuentos por volumen
            volume_discount_strategy = self._create_volume_discount_strategy(data, budget)
            strategies.append(volume_discount_strategy)
            
            # Estrategia 2: Bundle de productos
            bundle_strategy = self._create_bundle_strategy(data, budget)
            strategies.append(bundle_strategy)
            
            # Estrategia 3: Descuentos por categoría
            category_discount_strategy = self._create_category_discount_strategy(data, budget)
            strategies.append(category_discount_strategy)
            
            # Estrategia 4: Promoción de productos en tendencia
            trending_strategy = self._create_trending_promotion_strategy(data, budget)
            strategies.append(trending_strategy)
            
            # Estrategia 5: Liquidación de inventario
            clearance_strategy = self._create_clearance_strategy(data, budget)
            strategies.append(clearance_strategy)
            
            return strategies
            
        except Exception as e:
            logger.error(f"Error obteniendo estrategias de promoción: {e}")
            raise
    
    async def get_custom_recommendations(self, categories: List[str], budget: float, timeframe: int = 30) -> Dict[str, Any]:
        """Obtener recomendaciones personalizadas basadas en categorías y presupuesto"""
        try:
            # Filtrar productos por categorías especificadas
            data = self.sample_data[self.sample_data['category'].isin(categories)].copy()
            
            # Analizar productos por categoría
            category_analysis = {}
            for category in categories:
                category_data = data[data['category'] == category]
                if not category_data.empty:
                    category_analysis[category] = {
                        'product_count': len(category_data),
                        'avg_price': category_data['price'].mean(),
                        'total_value': category_data['price'].sum(),
                        'trending_products': self._get_trending_products(category_data, 3)
                    }
            
            # Generar recomendaciones de inversión
            investment_recommendations = self._generate_investment_recommendations(data, budget, timeframe)
            
            # Generar estrategias de marketing
            marketing_strategies = self._generate_marketing_strategies(categories, budget)
            
            # Calcular ROI estimado
            estimated_roi = self._calculate_estimated_roi(data, budget, timeframe)
            
            return {
                'categories_analysis': category_analysis,
                'investment_recommendations': investment_recommendations,
                'marketing_strategies': marketing_strategies,
                'estimated_roi': estimated_roi,
                'budget_allocation': self._allocate_budget(data, budget),
                'risk_assessment': self._assess_risk(data, categories),
                'timeline_recommendations': self._generate_timeline_recommendations(timeframe),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo recomendaciones personalizadas: {e}")
            raise
    
    def _calculate_recommendation_score(self, product: pd.Series) -> float:
        """Calcular puntuación de recomendación basada en múltiples factores"""
        # Factores de puntuación
        sales_factor = min(product['sales_volume'] / 1000, 1.0)  # Normalizar ventas
        trend_factor = product['trend_score']
        rating_factor = product['rating'] / 5.0
        profit_factor = product['profit_margin']
        stock_factor = min(product['stock_level'] / 100, 1.0)  # Normalizar stock
        
        # Ponderación de factores
        weights = {
            'sales': 0.25,
            'trend': 0.30,
            'rating': 0.20,
            'profit': 0.15,
            'stock': 0.10
        }
        
        score = (
            sales_factor * weights['sales'] +
            trend_factor * weights['trend'] +
            rating_factor * weights['rating'] +
            profit_factor * weights['profit'] +
            stock_factor * weights['stock']
        )
        
        return score
    
    def _generate_recommendation_reasons(self, product: pd.Series) -> List[str]:
        """Generar razones para la recomendación del producto"""
        reasons = []
        
        if product['trend_score'] > 0.7:
            reasons.append("Producto en tendencia ascendente")
        
        if product['rating'] >= 4.5:
            reasons.append("Excelente calificación de clientes")
        
        if product['profit_margin'] > 0.3:
            reasons.append("Alto margen de ganancia")
        
        if product['sales_volume'] > 500:
            reasons.append("Alto volumen de ventas")
        
        if product['stock_level'] < 30:
            reasons.append("Stock limitado - oportunidad única")
        
        if len(reasons) == 0:
            reasons.append("Producto con buen balance de características")
        
        return reasons
    
    def _get_stock_status(self, stock_level: int) -> str:
        """Determinar el estado del stock"""
        if stock_level < 20:
            return "low"
        elif stock_level < 50:
            return "medium"
        else:
            return "high"
    
    def _create_volume_discount_strategy(self, data: pd.DataFrame, budget: float) -> PromotionStrategy:
        """Crear estrategia de descuentos por volumen"""
        # Seleccionar productos con alto stock
        high_stock_products = data[data['stock_level'] > 50].copy()
        
        if high_stock_products.empty:
            high_stock_products = data.head(5)
        
        discount_products = []
        total_cost = 0
        
        for _, product in high_stock_products.head(3).iterrows():
            discount_amount = product['price'] * 0.15  # 15% de descuento
            cost = discount_amount * 10  # Aplicar a 10 unidades
            
            if total_cost + cost <= budget * 0.3:  # Usar 30% del presupuesto
                discount_products.append({
                    'product_id': product['id'],
                    'product_name': product['name'],
                    'discount_percentage': 15,
                    'units_affected': 10,
                    'cost': cost
                })
                total_cost += cost
        
        return PromotionStrategy(
            strategy_id=f"vol_disc_{uuid.uuid4().hex[:8]}",
            strategy_name="Descuentos por Volumen",
            strategy_type="volume_discount",
            description="Descuentos del 15% en compras de 10+ unidades",
            target_products=discount_products,
            estimated_cost=total_cost,
            expected_revenue=total_cost * 1.8,  # 80% de ganancia
            duration_days=14,
            success_probability=0.75,
            risk_level="low",
            created_at=datetime.now().isoformat()
        )
    
    def _create_bundle_strategy(self, data: pd.DataFrame, budget: float) -> PromotionStrategy:
        """Crear estrategia de bundle de productos"""
        # Agrupar productos por categoría
        categories = data['category'].unique()
        bundle_products = []
        total_cost = 0
        
        for category in categories[:2]:  # Máximo 2 categorías
            category_products = data[data['category'] == category].head(2)
            
            for _, product in category_products.iterrows():
                bundle_discount = product['price'] * 0.20  # 20% de descuento en bundle
                cost = bundle_discount * 5  # Aplicar a 5 bundles
                
                if total_cost + cost <= budget * 0.25:  # Usar 25% del presupuesto
                    bundle_products.append({
                        'product_id': product['id'],
                        'product_name': product['name'],
                        'discount_percentage': 20,
                        'bundle_size': 2,
                        'cost': cost
                    })
                    total_cost += cost
        
        return PromotionStrategy(
            strategy_id=f"bundle_{uuid.uuid4().hex[:8]}",
            strategy_name="Bundles de Productos",
            strategy_type="product_bundle",
            description="20% de descuento en compras de 2 productos de la misma categoría",
            target_products=bundle_products,
            estimated_cost=total_cost,
            expected_revenue=total_cost * 2.0,  # 100% de ganancia
            duration_days=21,
            success_probability=0.70,
            risk_level="medium",
            created_at=datetime.now().isoformat()
        )
    
    def _create_category_discount_strategy(self, data: pd.DataFrame, budget: float) -> PromotionStrategy:
        """Crear estrategia de descuentos por categoría"""
        # Encontrar categoría con más productos
        category_counts = data['category'].value_counts()
        target_category = category_counts.index[0]
        
        category_products = data[data['category'] == target_category]
        discount_products = []
        total_cost = 0
        
        for _, product in category_products.head(5).iterrows():
            discount_amount = product['price'] * 0.10  # 10% de descuento
            cost = discount_amount * 15  # Aplicar a 15 unidades
            
            if total_cost + cost <= budget * 0.25:  # Usar 25% del presupuesto
                discount_products.append({
                    'product_id': product['id'],
                    'product_name': product['name'],
                    'discount_percentage': 10,
                    'units_affected': 15,
                    'cost': cost
                })
                total_cost += cost
        
        return PromotionStrategy(
            strategy_id=f"cat_disc_{uuid.uuid4().hex[:8]}",
            strategy_name=f"Descuentos en {target_category.title()}",
            strategy_type="category_discount",
            description=f"10% de descuento en toda la categoría {target_category}",
            target_products=discount_products,
            estimated_cost=total_cost,
            expected_revenue=total_cost * 1.6,  # 60% de ganancia
            duration_days=10,
            success_probability=0.80,
            risk_level="low",
            created_at=datetime.now().isoformat()
        )
    
    def _create_trending_promotion_strategy(self, data: pd.DataFrame, budget: float) -> PromotionStrategy:
        """Crear estrategia de promoción de productos en tendencia"""
        # Seleccionar productos con alta tendencia
        trending_products = data[data['trend_score'] > 0.7].copy()
        
        if trending_products.empty:
            trending_products = data.nlargest(3, 'trend_score')
        
        discount_products = []
        total_cost = 0
        
        for _, product in trending_products.head(3).iterrows():
            discount_amount = product['price'] * 0.05  # 5% de descuento (productos ya populares)
            cost = discount_amount * 20  # Aplicar a 20 unidades
            
            if total_cost + cost <= budget * 0.15:  # Usar 15% del presupuesto
                discount_products.append({
                    'product_id': product['id'],
                    'product_name': product['name'],
                    'discount_percentage': 5,
                    'units_affected': 20,
                    'cost': cost
                })
                total_cost += cost
        
        return PromotionStrategy(
            strategy_id=f"trend_{uuid.uuid4().hex[:8]}",
            strategy_name="Promoción de Productos en Tendencia",
            strategy_type="trending_promotion",
            description="5% de descuento en productos con alta tendencia",
            target_products=discount_products,
            estimated_cost=total_cost,
            expected_revenue=total_cost * 1.4,  # 40% de ganancia
            duration_days=7,
            success_probability=0.85,
            risk_level="very_low",
            created_at=datetime.now().isoformat()
        )
    
    def _create_clearance_strategy(self, data: pd.DataFrame, budget: float) -> PromotionStrategy:
        """Crear estrategia de liquidación de inventario"""
        # Seleccionar productos con bajo stock y baja tendencia
        clearance_products = data[
            (data['stock_level'] < 30) & 
            (data['trend_score'] < 0.5)
        ].copy()
        
        if clearance_products.empty:
            clearance_products = data.nsmallest(3, 'stock_level')
        
        discount_products = []
        total_cost = 0
        
        for _, product in clearance_products.head(3).iterrows():
            discount_amount = product['price'] * 0.30  # 30% de descuento para liquidación
            cost = discount_amount * product['stock_level']  # Aplicar a todo el stock
            
            if total_cost + cost <= budget * 0.05:  # Usar 5% del presupuesto
                discount_products.append({
                    'product_id': product['id'],
                    'product_name': product['name'],
                    'discount_percentage': 30,
                    'units_affected': product['stock_level'],
                    'cost': cost
                })
                total_cost += cost
        
        return PromotionStrategy(
            strategy_id=f"clear_{uuid.uuid4().hex[:8]}",
            strategy_name="Liquidación de Inventario",
            strategy_type="clearance",
            description="30% de descuento en productos con stock limitado",
            target_products=discount_products,
            estimated_cost=total_cost,
            expected_revenue=total_cost * 1.2,  # 20% de ganancia
            duration_days=5,
            success_probability=0.90,
            risk_level="very_low",
            created_at=datetime.now().isoformat()
        )
    
    def _get_trending_products(self, data: pd.DataFrame, limit: int) -> List[Dict[str, Any]]:
        """Obtener productos en tendencia de una categoría"""
        trending = data.nlargest(limit, 'trend_score')
        return [
            {
                'product_id': row['id'],
                'product_name': row['name'],
                'trend_score': round(row['trend_score'], 2),
                'price': row['price']
            }
            for _, row in trending.iterrows()
        ]
    
    def _generate_investment_recommendations(self, data: pd.DataFrame, budget: float, timeframe: int) -> List[Dict[str, Any]]:
        """Generar recomendaciones de inversión"""
        recommendations = []
        
        # Recomendación 1: Invertir en productos en tendencia
        trending_products = data[data['trend_score'] > 0.7]
        if not trending_products.empty:
            trending_investment = min(budget * 0.4, trending_products['price'].sum() * 0.3)
            recommendations.append({
                'type': 'trending_investment',
                'description': 'Invertir en productos con alta tendencia',
                'amount': round(trending_investment, 2),
                'expected_return': round(trending_investment * 1.5, 2),
                'risk_level': 'medium'
            })
        
        # Recomendación 2: Diversificar categorías
        category_diversity = data['category'].nunique()
        if category_diversity >= 3:
            diversity_investment = budget * 0.3
            recommendations.append({
                'type': 'category_diversification',
                'description': 'Diversificar inversión entre categorías',
                'amount': round(diversity_investment, 2),
                'expected_return': round(diversity_investment * 1.3, 2),
                'risk_level': 'low'
            })
        
        # Recomendación 3: Productos de alto margen
        high_margin_products = data[data['profit_margin'] > 0.3]
        if not high_margin_products.empty:
            margin_investment = min(budget * 0.3, high_margin_products['price'].sum() * 0.2)
            recommendations.append({
                'type': 'high_margin_investment',
                'description': 'Invertir en productos con alto margen de ganancia',
                'amount': round(margin_investment, 2),
                'expected_return': round(margin_investment * 1.4, 2),
                'risk_level': 'medium'
            })
        
        return recommendations
    
    def _generate_marketing_strategies(self, categories: List[str], budget: float) -> List[Dict[str, Any]]:
        """Generar estrategias de marketing"""
        strategies = []
        
        # Estrategia 1: Marketing digital
        digital_marketing = {
            'type': 'digital_marketing',
            'description': 'Campañas en redes sociales y Google Ads',
            'budget_allocation': round(budget * 0.4, 2),
            'channels': ['Instagram', 'Facebook', 'Google Ads'],
            'expected_reach': '10,000-50,000 personas',
            'duration': '30 días'
        }
        strategies.append(digital_marketing)
        
        # Estrategia 2: Email marketing
        email_marketing = {
            'type': 'email_marketing',
            'description': 'Campañas de email personalizadas',
            'budget_allocation': round(budget * 0.2, 2),
            'channels': ['Email'],
            'expected_reach': '5,000-15,000 suscriptores',
            'duration': '15 días'
        }
        strategies.append(email_marketing)
        
        # Estrategia 3: Influencer marketing
        influencer_marketing = {
            'type': 'influencer_marketing',
            'description': 'Colaboraciones con influencers del sector',
            'budget_allocation': round(budget * 0.3, 2),
            'channels': ['Instagram', 'YouTube', 'TikTok'],
            'expected_reach': '20,000-100,000 personas',
            'duration': '45 días'
        }
        strategies.append(influencer_marketing)
        
        # Estrategia 4: SEO y contenido
        seo_content = {
            'type': 'seo_content',
            'description': 'Optimización SEO y contenido de valor',
            'budget_allocation': round(budget * 0.1, 2),
            'channels': ['Blog', 'Website', 'YouTube'],
            'expected_reach': '2,000-10,000 personas',
            'duration': '60 días'
        }
        strategies.append(seo_content)
        
        return strategies
    
    def _calculate_estimated_roi(self, data: pd.DataFrame, budget: float, timeframe: int) -> Dict[str, Any]:
        """Calcular ROI estimado"""
        # Calcular métricas base
        avg_profit_margin = data['profit_margin'].mean()
        avg_trend_score = data['trend_score'].mean()
        
        # Factores de ajuste
        trend_factor = 1 + (avg_trend_score - 0.5) * 0.4  # ±20% basado en tendencia
        timeframe_factor = 1 + (timeframe - 30) / 100  # ±15% basado en timeframe
        
        # ROI base
        base_roi = avg_profit_margin * trend_factor * timeframe_factor
        
        # Escenarios
        conservative_roi = base_roi * 0.8
        expected_roi = base_roi
        optimistic_roi = base_roi * 1.3
        
        return {
            'conservative': round(conservative_roi * 100, 1),
            'expected': round(expected_roi * 100, 1),
            'optimistic': round(optimistic_roi * 100, 1),
            'break_even_days': round(30 / expected_roi, 0),
            'confidence_level': 'medium'
        }
    
    def _allocate_budget(self, data: pd.DataFrame, budget: float) -> Dict[str, float]:
        """Asignar presupuesto por categoría"""
        category_totals = data.groupby('category')['price'].sum()
        total_value = category_totals.sum()
        
        allocation = {}
        for category, value in category_totals.items():
            allocation[category] = round((value / total_value) * budget, 2)
        
        return allocation
    
    def _assess_risk(self, data: pd.DataFrame, categories: List[str]) -> Dict[str, Any]:
        """Evaluar nivel de riesgo de la inversión"""
        # Factores de riesgo
        category_diversity = len(categories)
        avg_trend_score = data['trend_score'].mean()
        avg_profit_margin = data['profit_margin'].mean()
        stock_variability = data['stock_level'].std() / data['stock_level'].mean()
        
        # Calcular puntuación de riesgo (0-100, menor es mejor)
        risk_score = 0
        
        # Riesgo por diversificación
        if category_diversity < 2:
            risk_score += 30
        elif category_diversity < 3:
            risk_score += 15
        
        # Riesgo por tendencia
        if avg_trend_score < 0.4:
            risk_score += 25
        elif avg_trend_score < 0.6:
            risk_score += 10
        
        # Riesgo por margen
        if avg_profit_margin < 0.2:
            risk_score += 20
        elif avg_profit_margin < 0.3:
            risk_score += 10
        
        # Riesgo por stock
        if stock_variability > 0.5:
            risk_score += 15
        
        # Determinar nivel de riesgo
        if risk_score < 20:
            risk_level = "very_low"
        elif risk_score < 40:
            risk_level = "low"
        elif risk_score < 60:
            risk_level = "medium"
        elif risk_score < 80:
            risk_level = "high"
        else:
            risk_level = "very_high"
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'factors': {
                'category_diversity': category_diversity,
                'avg_trend_score': round(avg_trend_score, 2),
                'avg_profit_margin': round(avg_profit_margin, 2),
                'stock_variability': round(stock_variability, 2)
            },
            'mitigation_strategies': self._generate_risk_mitigation_strategies(risk_score)
        }
    
    def _generate_risk_mitigation_strategies(self, risk_score: float) -> List[str]:
        """Generar estrategias de mitigación de riesgo"""
        strategies = []
        
        if risk_score > 50:
            strategies.append("Diversificar inversión en más categorías")
            strategies.append("Implementar estrategias de descuento agresivas")
            strategies.append("Monitorear tendencias diariamente")
        
        if risk_score > 30:
            strategies.append("Mantener inventario flexible")
            strategies.append("Establecer alertas de precio")
        
        strategies.append("Realizar análisis de mercado semanal")
        strategies.append("Mantener comunicación con proveedores")
        
        return strategies
    
    def _generate_timeline_recommendations(self, timeframe: int) -> List[Dict[str, Any]]:
        """Generar recomendaciones de timeline"""
        recommendations = []
        
        if timeframe <= 7:
            recommendations.append({
                'phase': 'Inmediato (1-7 días)',
                'actions': [
                    'Implementar descuentos flash',
                    'Optimizar precios de productos en tendencia',
                    'Preparar campañas de email marketing'
                ]
            })
        elif timeframe <= 30:
            recommendations.append({
                'phase': 'Corto plazo (1-4 semanas)',
                'actions': [
                    'Lanzar campañas de redes sociales',
                    'Implementar estrategias de bundle',
                    'Optimizar SEO para productos clave'
                ]
            })
        else:
            recommendations.append({
                'phase': 'Mediano plazo (1-3 meses)',
                'actions': [
                    'Desarrollar contenido de marketing',
                    'Establecer alianzas con influencers',
                    'Implementar programa de fidelización'
                ]
            })
        
        return recommendations 