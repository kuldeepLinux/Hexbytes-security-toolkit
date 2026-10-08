import typer
from rich.console import Console
from rich.table import Table
from core.logger import log
from core.utils import is_valid_domain, clean_domain
from modules.recon.subdomain import enumerate_subdomains

app = typer.Typer(help="HexBytes Security Toolkit — Authorized testing only")
console = Console()

@app.command()
def recon(
    domain: str = typer.Argument(..., help="Target domain (e.g. example.com)"),
    live: bool = typer.Option(True, "--live/--no-live", help="Check live status"),
    threads: int = typer.Option(20, help="Thread count"),
):
    """Subdomain enumeration using crt.sh"""
    domain = clean_domain(domain)
    if not is_valid_domain(domain):
        log.error(f"Invalid domain: {domain}")
        raise typer.Exit(1)

    results = enumerate_subdomains(domain, check_live=live, threads=threads)

    table = Table(title=f"Subdomains — {domain}")
    table.add_column("Subdomain", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("HTTP", style="yellow")

    for sub, alive, code in results:
        status = "LIVE" if alive else ("dead" if alive is False else "-")
        table.add_row(sub, status, str(code) if code else "-")

    console.print(table)

@app.command()
def version():
    """Show toolkit version"""
    console.print("[bold green]HexBytes Security Toolkit v0.1.0[/bold green]")

if __name__ == "__main__":
    app()
