import time
import random
from typing import List, Dict, Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..api import APIFetcher
from ..analysis import (
    PatternAnalyzer, BuyerAnalyzer, RatingAnalyzer,
    TimeAnalyzer, VariantAnalyzer, TrustAnalyzer, FakeScorer
)
from ..ui import DisplayManager

class TokopediaFakeDetector:
    def __init__(self):
        self.console = Console()
        self.api = APIFetcher()
        self.display = DisplayManager(self.console)
        self.pattern_analyzer = PatternAnalyzer()
        self.buyer_analyzer = BuyerAnalyzer()
        self.rating_analyzer = RatingAnalyzer()
        self.time_analyzer = TimeAnalyzer()
        self.variant_analyzer = VariantAnalyzer()
        self.trust_analyzer = TrustAnalyzer()
        self.scorer = FakeScorer()
        self.fake_indicators = {}
        self.trusted_sellers = []
    
    def run(self, product_url: str):
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True,
            refresh_per_second=10,
        ) as progress:
            
            task = progress.add_task("[cyan]Fetching product information...", total=None)
            product_info = self.api.fetch_product_info(product_url)
            
            if not product_info or not product_info.get('product'):
                progress.stop()
                self.console.print("[red]Failed to fetch product information[/red]")
                return
            
            progress.update(task, description="[cyan]Fetching comprehensive rating data...")
            rating_topics = self.api.fetch_rating_and_topics(product_url)
            
            all_reviews = []
            variant_data = None
            for page in range(1, 6):
                progress.update(task, description=f"[cyan]Fetching reviews (page {page})...")
                review_data = self.api.fetch_reviews(product_url, page=page, limit=20)
                if review_data and review_data.get('list'):
                    all_reviews.extend(review_data['list'])
                    if not variant_data and review_data.get('variantFilter'):
                        variant_data = review_data['variantFilter']
                    if not review_data.get('hasNext'):
                        break
                else:
                    break
            
            if not all_reviews:
                progress.stop()
                self.console.print("[yellow]No reviews found for this product[/yellow]")
                return
            
            progress.update(task, description="[cyan]Analyzing review patterns...")
            patterns = self.pattern_analyzer.analyze(all_reviews)
            
            progress.update(task, description="[cyan]Analyzing buyer behavior...")
            buyers = self.buyer_analyzer.analyze(all_reviews)
            
            progress.update(task, description="[cyan]Analyzing rating distribution...")
            ratings = self.rating_analyzer.analyze(all_reviews)
            
            progress.update(task, description="[cyan]Analyzing time patterns...")
            time_data = self.time_analyzer.analyze(all_reviews)
            
            progress.update(task, description="[cyan]Analyzing variant patterns...")
            variants = self.variant_analyzer.analyze(all_reviews)
            
            progress.update(task, description="[cyan]Calculating fake score...")
            fake_score = self.scorer.calculate(patterns, buyers, ratings, time_data, rating_topics, variants)
            
            trusted_sellers = []
            if fake_score > 30:
                progress.update(task, description="[cyan]Searching for trusted sellers...")
                product_name = product_info['product'].get('name', '')
                shop_url = product_url.split('/')[3] if len(product_url.split('/')) > 3 else None
                trusted_sellers = self.find_trusted_sellers(product_name, shop_url)
        
        self.display.display_results(product_info, fake_score, patterns, buyers, ratings, time_data, rating_topics, variants)
        
        if trusted_sellers:
            self.display.display_trusted_sellers(trusted_sellers)
        
        self.fake_indicators = {
            'review_patterns': patterns,
            'suspicious_buyers': buyers,
            'rating_anomalies': ratings,
            'time_patterns': time_data,
            'rating_topics': rating_topics,
            'variants': variants,
            'fake_score': fake_score,
            'trusted_sellers': trusted_sellers if fake_score > 30 else []
        }
    
    def find_trusted_sellers(self, product_name: str, current_shop: Optional[str] = None) -> List[Dict]:
        query = ' '.join(product_name.split()[:5])
        
        search_results = self.api.search_products(query, page=1, rows=20)
        
        if not search_results or not search_results.get('data'):
            return []
        
        products = search_results['data'].get('products', [])
        shop_scores = []
        
        for product in products[:10]:
            if not product.get('shop'):
                continue
            
            shop = product['shop']
            shop_domain = shop.get('url', '').split('/')[-1]
            
            if shop_domain and shop_domain != current_shop:
                shop_detail = self.api.fetch_shop_detail(shop_domain)
                
                if shop_detail:
                    shop_id = str(shop_detail.get('shopCore', {}).get('shopID', ''))
                    shop_rating = None
                    
                    if shop_id:
                        shop_rating = self.api.fetch_shop_rating(shop_id)
                    
                    trust_analysis = self.trust_analyzer.analyze(shop_detail, shop_rating)
                    
                    shop_scores.append({
                        'shop_name': shop.get('name', ''),
                        'shop_domain': shop_domain,
                        'shop_tier': shop.get('tier', 0),
                        'product_name': product.get('name', ''),
                        'product_url': product.get('url', ''),
                        'product_price': product.get('price', {}).get('text', ''),
                        'product_rating': product.get('rating', 0),
                        'trust_analysis': trust_analysis
                    })
                
                time.sleep(random.uniform(0.3, 0.8))
        
        shop_scores.sort(key=lambda x: x['trust_analysis']['trust_score'], reverse=True)
        
        return shop_scores[:5]
    
    def quick_analyze(self, product_url: str):
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True,
            refresh_per_second=10,
        ) as progress:
            task = progress.add_task("[cyan]Fetching product information...", total=None)
            product_info = self.api.fetch_product_info(product_url)
            
            if not product_info or not product_info.get('product'):
                progress.stop()
                self.console.print("[red]Failed to fetch product information[/red]")
                return
            
            progress.update(task, description="[cyan]Analyzing reviews...")
            rating_topics = self.api.fetch_rating_and_topics(product_url)
            
            all_reviews = []
            for page in range(1, 3):
                progress.update(task, description=f"[cyan]Fetching reviews (page {page})...")
                review_data = self.api.fetch_reviews(product_url, page=page, limit=20)
                if review_data and review_data.get('list'):
                    all_reviews.extend(review_data['list'])
                    if not review_data.get('hasNext'):
                        break
                else:
                    break
            
            if not all_reviews:
                progress.stop()
                self.console.print("[yellow]No reviews found[/yellow]")
                return
            
            progress.update(task, description="[cyan]Analyzing patterns...")
            patterns = self.pattern_analyzer.analyze(all_reviews)
            buyers = self.buyer_analyzer.analyze(all_reviews)
            ratings = self.rating_analyzer.analyze(all_reviews)
            time_data = self.time_analyzer.analyze(all_reviews)
            variants = self.variant_analyzer.analyze(all_reviews)
            fake_score = self.scorer.calculate(patterns, buyers, ratings, time_data, rating_topics, variants)
        
        self.display.display_results(product_info, fake_score, patterns, buyers, ratings, time_data, rating_topics, variants)
