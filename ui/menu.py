import time
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn

class MenuManager:
    def __init__(self, console: Console):
        self.console = console
    
    def display_menu(self) -> str:
        self.console.clear()
        self.console.print(Panel.fit(
            Text("Tokopedia Fake Review Detector", style="bold cyan"),
            subtitle="Detect fake reviews & find trusted sellers",
            border_style="cyan"
        ))
        
        menu_table = Table(show_header=False, box=None, padding=(0, 2))
        menu_table.add_column("Option", style="cyan", width=3)
        menu_table.add_column("Description", style="white")
        
        menu_table.add_row("1", "Analyze Product Reviews - Detect fake reviews & ratings")
        menu_table.add_row("2", "Find Trusted Sellers - Search for reliable alternatives")
        menu_table.add_row("3", "Quick Analysis - Fast check without recommendations")
        menu_table.add_row("4", "Batch Analysis - Analyze multiple products")
        menu_table.add_row("5", "About - Information about detection methods")
        menu_table.add_row("0", "Exit")
        
        self.console.print("\n[bold yellow]Menu Options:[/bold yellow]")
        self.console.print(menu_table)
        
        try:
            choice = self.console.input("\n[cyan]Select option (0-5): [/cyan]").strip()
            return choice
        except (EOFError, KeyboardInterrupt):
            return "0"
    
    def show_about(self):
        self.console.print("\n[bold cyan]About Fake Review Detection[/bold cyan]\n")
        
        about_text = """This tool analyzes various factors to detect fake reviews:

[bold yellow]Detection Methods:[/bold yellow]
• Review Patterns - Identifies generic, duplicate, and suspicious similarities
• Buyer Analysis - Checks anonymous buyers, burst reviewers, verification status  
• Rating Analysis - Detects unnatural rating distributions and sudden influxes
• Time Patterns - Analyzes posting times and frequency anomalies
• Variant Analysis - Checks product variant review distribution
• Seller Trust Score - Evaluates shop age, ratings, badges, and reputation

[bold yellow]Trust Score Factors:[/bold yellow]
• Official/Gold merchant status
• Shop age and establishment date
• Customer ratings and review count
• Total favorites and engagement
• Product catalog diversity

[bold yellow]Risk Levels:[/bold yellow]
• [green]LOW (0-30%)[/green] - Likely authentic reviews
• [yellow]MEDIUM (31-70%)[/yellow] - Some suspicious patterns detected
• [red]HIGH (71-100%)[/red] - Strong indicators of fake reviews

[bold cyan]Tips:[/bold cyan]
• Always check multiple factors before making decisions
• Look for verified buyers and detailed reviews with images
• Compare prices across trusted sellers
• Check seller ratings and establishment dates"""
        
        self.console.print(about_text)
        self.console.input("\n[dim]Press Enter to continue...[/dim]")
    
    def get_product_url(self) -> Optional[str]:
        try:
            product_url = self.console.input("[cyan]Enter Tokopedia product URL: [/cyan]").strip()
            if product_url and product_url.startswith("https://www.tokopedia.com/"):
                return product_url
            else:
                self.console.print("[red]Invalid URL. Please enter a valid Tokopedia product URL[/red]")
                time.sleep(2)
                return None
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Cancelled[/yellow]")
            return None
    
    def get_search_query(self) -> Optional[str]:
        try:
            query = self.console.input("[cyan]Enter product name to search: [/cyan]").strip()
            if query:
                return query
            else:
                self.console.print("[red]Please enter a product name[/red]")
                time.sleep(2)
                return None
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Cancelled[/yellow]")
            return None
    
    def get_batch_urls(self) -> list:
        self.console.print("[yellow]Enter product URLs (one per line, empty line to finish):[/yellow]")
        urls = []
        while True:
            try:
                url = self.console.input("[cyan]URL: [/cyan]").strip()
                if not url:
                    break
                if url.startswith("https://www.tokopedia.com/"):
                    urls.append(url)
                else:
                    self.console.print("[red]Invalid URL, skipping...[/red]")
            except KeyboardInterrupt:
                break
        return urls
    
    def wait_for_continue(self):
        try:
            self.console.input("\n[dim]Press Enter to continue...[/dim]")
        except KeyboardInterrupt:
            pass
