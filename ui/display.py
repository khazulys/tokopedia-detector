from typing import Dict, List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

class DisplayManager:
    def __init__(self, console: Console):
        self.console = console
    
    def display_results(self, product_info: Dict, fake_score: float, patterns: Dict, 
                       buyers: Dict, ratings: Dict, time_data: Dict, 
                       rating_topics: Optional[Dict] = None, variants: Optional[Dict] = None):
        self.console.clear()
        
        header_panel = Panel.fit(
            Text(f"Tokopedia Fake Review Detection System", style="bold cyan"),
            border_style="cyan"
        )
        self.console.print(header_panel)
        
        if product_info and product_info.get('product'):
            product = product_info['product']
            product_table = Table(title="Product Information", show_header=True, header_style="bold magenta")
            product_table.add_column("Field", style="cyan")
            product_table.add_column("Value", style="white")
            
            product_table.add_row("Name", product.get('name', 'N/A'))
            product_table.add_row("Price", product.get('priceFmt', 'N/A'))
            product_table.add_row("Stock", str(product.get('stock', 'N/A')))
            product_table.add_row("Status", product.get('status', 'N/A'))
            
            self.console.print(product_table)
        
        risk_color = "red" if fake_score > 70 else "yellow" if fake_score > 40 else "green"
        risk_level = "HIGH" if fake_score > 70 else "MEDIUM" if fake_score > 40 else "LOW"
        
        score_panel = Panel(
            Text(f"Fake Detection Score: {fake_score:.1f}%\nRisk Level: {risk_level}", style=f"bold {risk_color}"),
            title="Analysis Result",
            border_style=risk_color
        )
        self.console.print(score_panel)
        
        self._display_findings(patterns, buyers, ratings, time_data, variants)
        self._display_rating_details(rating_topics, ratings)
        
        if variants and variants.get('variant_distribution'):
            self._display_variant_analysis(variants)
        
        if buyers.get('labeled_users'):
            self._display_user_labels(buyers)
    
    def _display_findings(self, patterns: Dict, buyers: Dict, ratings: Dict, 
                         time_data: Dict, variants: Optional[Dict]):
        findings_table = Table(title="Detection Findings", show_header=True, header_style="bold yellow")
        findings_table.add_column("Category", style="cyan")
        findings_table.add_column("Finding", style="white")
        findings_table.add_column("Severity", style="red")
        
        if patterns['generic_reviews'] > 5:
            findings_table.add_row("Review Pattern", f"{patterns['generic_reviews']} generic reviews", "Medium")
        
        if len(patterns['suspiciously_similar']) > 0:
            findings_table.add_row("Review Pattern", f"{len(patterns['suspiciously_similar'])} similar reviews", "High")
        
        if patterns['keyword_stuffing'] > 3:
            findings_table.add_row("Review Pattern", f"{patterns['keyword_stuffing']} keyword stuffing cases", "Medium")
        
        if buyers['anonymous_percentage'] > 30:
            findings_table.add_row("Buyer Analysis", f"{buyers['anonymous_percentage']:.1f}% anonymous buyers", "Medium")
        
        if len(buyers['burst_reviewers']) > 0:
            findings_table.add_row("Buyer Analysis", f"{len(buyers['burst_reviewers'])} burst reviewers", "High")
        
        if ratings['all_same_rating']:
            findings_table.add_row("Rating Analysis", "All reviews have same rating", "High")
        elif ratings['suspicious_pattern']:
            findings_table.add_row("Rating Analysis", "Suspicious rating pattern detected", "Medium")
        
        if len(ratings['sudden_influx']) > 0:
            for date, count in ratings['sudden_influx'][:3]:
                findings_table.add_row("Time Pattern", f"{count} reviews on {date}", "Medium")
        
        if time_data['night_reviews'] > 20:
            findings_table.add_row("Time Pattern", f"{time_data['night_reviews']:.1f}% reviews at night", "Low")
        
        if variants:
            if variants.get('single_variant_dominance'):
                findings_table.add_row("Variant Analysis", "Single variant dominates (>80%)", "High")
            
            if variants.get('variant_count', 0) == 1:
                findings_table.add_row("Variant Analysis", "Only one variant reviewed", "Medium")
        
        if buyers.get('verified_buyers', 0) < 20:
            findings_table.add_row("Buyer Verification", f"Only {buyers.get('verified_buyers', 0):.1f}% verified buyers", "Medium")
        
        self.console.print(findings_table)
    
    def _display_rating_details(self, rating_topics: Optional[Dict], ratings: Dict):
        if rating_topics and rating_topics.get('rating'):
            comprehensive_rating = rating_topics['rating']
            
            rating_summary_table = Table(title="Comprehensive Rating Analysis", show_header=True, header_style="bold magenta")
            rating_summary_table.add_column("Metric", style="cyan")
            rating_summary_table.add_column("Value", style="white")
            
            rating_score = comprehensive_rating.get('ratingScore', 0)
            try:
                rating_score = float(rating_score) if rating_score else 0.0
            except (ValueError, TypeError):
                rating_score = 0.0
            rating_summary_table.add_row("Overall Rating", f"{rating_score:.1f}/5.0")
            rating_summary_table.add_row("Total Reviews", str(comprehensive_rating.get('totalRating', 0)))
            rating_summary_table.add_row("Reviews with Images", str(comprehensive_rating.get('totalRatingWithImage', 0)))
            rating_summary_table.add_row("Positive Percentage", comprehensive_rating.get('positivePercentageFmt', 'N/A'))
            
            self.console.print(rating_summary_table)
            
            if comprehensive_rating.get('detail'):
                rating_dist_table = Table(title="Detailed Rating Distribution", show_header=True, header_style="bold cyan")
                rating_dist_table.add_column("Rating", style="yellow")
                rating_dist_table.add_column("Count", style="white")
                rating_dist_table.add_column("Percentage", style="green")
                rating_dist_table.add_column("Bar", style="blue")
                
                for detail in sorted(comprehensive_rating['detail'], key=lambda x: x.get('rate', 0), reverse=True):
                    rate = detail.get('rate', 0)
                    total_reviews = detail.get('totalReviews', 0)
                    percentage = detail.get('percentageFloat', 0)
                    bar_length = int(percentage / 5)
                    bar = "█" * bar_length + "░" * (20 - bar_length)
                    
                    rating_dist_table.add_row(
                        f"{rate} ⭐",
                        str(total_reviews),
                        f"{percentage:.1f}%",
                        bar
                    )
                
                self.console.print(rating_dist_table)
            
            if rating_topics.get('topics') and len(rating_topics['topics']) > 0:
                topics_table = Table(title="Review Topics", show_header=True, header_style="bold yellow")
                topics_table.add_column("Topic", style="cyan")
                topics_table.add_column("Count", style="white")
                topics_table.add_column("Rating", style="green")
                
                for topic in rating_topics['topics'][:10]:
                    if topic.get('show'):
                        topics_table.add_row(
                            topic.get('formatted', 'N/A'),
                            topic.get('reviewCountFmt', '0'),
                            topic.get('ratingFmt', 'N/A')
                        )
                
                if topics_table.row_count > 0:
                    self.console.print(topics_table)
            
            if rating_topics.get('keywords') and len(rating_topics['keywords']) > 0:
                keywords_table = Table(title="Frequent Keywords", show_header=True, header_style="bold green")
                keywords_table.add_column("Keyword", style="cyan")
                keywords_table.add_column("Count", style="white")
                
                for keyword in rating_topics['keywords'][:15]:
                    keywords_table.add_row(
                        keyword.get('text', ''),
                        str(keyword.get('count', 0))
                    )
                
                if keywords_table.row_count > 0:
                    self.console.print(keywords_table)
        else:
            rating_dist_table = Table(title="Rating Distribution", show_header=True, header_style="bold cyan")
            rating_dist_table.add_column("Rating", style="yellow")
            rating_dist_table.add_column("Count", style="white")
            rating_dist_table.add_column("Percentage", style="green")
            
            total_ratings = sum(ratings['distribution'].values()) if ratings['distribution'] else 1
            for rating in range(5, 0, -1):
                count = ratings['distribution'].get(rating, 0)
                percentage = (count / total_ratings * 100) if total_ratings > 0 else 0
                rating_dist_table.add_row(f"{rating} ⭐", str(count), f"{percentage:.1f}%")
            
            self.console.print(rating_dist_table)
    
    def _display_variant_analysis(self, variants: Dict):
        variant_table = Table(title="Variant Analysis", show_header=True, header_style="bold yellow")
        variant_table.add_column("Variant", style="cyan")
        variant_table.add_column("Reviews", style="white")
        variant_table.add_column("Percentage", style="green")
        
        total_variant_reviews = sum(variants['variant_distribution'].values())
        for variant_name, count in sorted(variants['variant_distribution'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_variant_reviews * 100) if total_variant_reviews > 0 else 0
            variant_table.add_row(variant_name[:50], str(count), f"{percentage:.1f}%")
        
        self.console.print(variant_table)
    
    def _display_user_labels(self, buyers: Dict):
        if buyers.get('labeled_users'):
            user_labels_table = Table(title="User Labels", show_header=True, header_style="bold green")
            user_labels_table.add_column("Label", style="cyan")
            user_labels_table.add_column("Count", style="white")
            
            for label, count in buyers['labeled_users'].items():
                user_labels_table.add_row(label, str(count))
            
            self.console.print(user_labels_table)
    
    def display_trusted_sellers(self, trusted_sellers: List[Dict]):
        if not trusted_sellers:
            self.console.print("\n[yellow]No alternative trusted sellers found[/yellow]")
            return
        
        recommendations_panel = Panel.fit(
            Text("Recommended Trusted Sellers", style="bold green"),
            border_style="green"
        )
        self.console.print("\n", recommendations_panel)
        
        for idx, seller in enumerate(trusted_sellers, 1):
            trust = seller['trust_analysis']
            
            seller_table = Table(title=f"#{idx}. {seller['shop_name']}", show_header=True, header_style="bold cyan")
            seller_table.add_column("Metric", style="cyan")
            seller_table.add_column("Value", style="white")
            
            trust_color = "green" if trust['trust_score'] >= 70 else "yellow" if trust['trust_score'] >= 50 else "red"
            seller_table.add_row("Trust Score", f"[{trust_color}]{trust['trust_score']}%[/{trust_color}]")
            seller_table.add_row("Shop Score", f"{trust['shop_score']}%")
            
            if trust.get('shop_rating', 0) > 0:
                seller_table.add_row("Shop Rating", f"{trust['shop_rating']:.1f}/5.0 ({trust.get('total_reviews', 0):,} reviews)")
            
            badges = []
            if trust['is_official']:
                badges.append("[green]Official Store[/green]")
            if trust['is_gold']:
                badges.append("[yellow]Gold Merchant[/yellow]")
            if badges:
                seller_table.add_row("Badges", " ".join(badges))
            
            if trust['shop_age']:
                seller_table.add_row("Store Since", trust['shop_age'])
            
            seller_table.add_row("Total Favorites", f"{trust['total_favorites']:,}")
            seller_table.add_row("Product", seller['product_name'][:60] + "..." if len(seller['product_name']) > 60 else seller['product_name'])
            seller_table.add_row("Price", seller['product_price'])
            
            if seller['product_rating']:
                rating_float = 0.0
                try:
                    rating_float = float(seller['product_rating'])
                except:
                    pass
                seller_table.add_row("Product Rating", f"{rating_float:.1f}/5.0")
            
            self.console.print(seller_table)
            
            if trust['reasons']:
                reasons_text = Text("Trust Factors:", style="bold")
                self.console.print(reasons_text)
                for reason in trust['reasons']:
                    self.console.print(f"  • {reason}")
            
            self.console.print()
