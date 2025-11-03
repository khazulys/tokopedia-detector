import time
import sys
import os

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import tokped_detector
    from tokped_detector.core import TokopediaFakeDetector
    from tokped_detector.ui import MenuManager
else:
    from .core import TokopediaFakeDetector
    from .ui import MenuManager

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

def main():
    console = Console()
    detector = TokopediaFakeDetector()
    menu = MenuManager(console)
    
    while True:
        choice = menu.display_menu()
        
        if choice == "0":
            console.print("\n[green]Thank you for using Tokopedia Fake Review Detector![/green]")
            break
        
        elif choice == "1":
            console.print("\n[bold cyan]Product Review Analysis[/bold cyan]")
            url = menu.get_product_url()
            if url:
                try:
                    detector.run(url)
                    menu.wait_for_continue()
                except Exception as e:
                    console.print(f"[red]Error: {str(e)}[/red]")
                    time.sleep(2)
        
        elif choice == "2":
            console.print("\n[bold cyan]Find Trusted Sellers[/bold cyan]")
            query = menu.get_search_query()
            if query:
                try:
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        console=console,
                        transient=True
                    ) as progress:
                        task = progress.add_task("[cyan]Searching for trusted sellers...", total=None)
                        trusted = detector.find_trusted_sellers(query, None)
                    
                    if trusted:
                        detector.display.display_trusted_sellers(trusted)
                    else:
                        console.print("[yellow]No sellers found for this search[/yellow]")
                    menu.wait_for_continue()
                except Exception as e:
                    console.print(f"[red]Error: {str(e)}[/red]")
                    time.sleep(2)
        
        elif choice == "3":
            console.print("\n[bold cyan]Quick Analysis (No Recommendations)[/bold cyan]")
            url = menu.get_product_url()
            if url:
                try:
                    detector.quick_analyze(url)
                    menu.wait_for_continue()
                except Exception as e:
                    console.print(f"[red]Error: {str(e)}[/red]")
                    time.sleep(2)
        
        elif choice == "4":
            console.print("\n[bold cyan]Batch Analysis[/bold cyan]")
            urls = menu.get_batch_urls()
            
            if urls:
                console.print(f"\n[green]Analyzing {len(urls)} products...[/green]")
                for i, url in enumerate(urls, 1):
                    console.print(f"\n[bold cyan]Product {i}/{len(urls)}[/bold cyan]")
                    try:
                        detector.run(url)
                    except Exception as e:
                        console.print(f"[red]Error: {str(e)}[/red]")
                    if i < len(urls):
                        console.print("\n[dim]---[/dim]\n")
                menu.wait_for_continue()
            else:
                console.print("[yellow]No valid URLs provided[/yellow]")
                time.sleep(2)
        
        elif choice == "5":
            menu.show_about()
        
        else:
            console.print("[red]Invalid option. Please select 0-5[/red]")
            time.sleep(1)

if __name__ == "__main__":
    main()
