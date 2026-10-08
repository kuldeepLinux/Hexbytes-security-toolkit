import typer
from rich.console import Console
from rich.table import Table
from core.utils import is_valid_domain, clean_domain
from modules.recon.subdomain import enumerate_subdomains
from modules.recon.portscan import scan_ports
from modules.webscan.headers import check_headers
from modules.reports.pdf_generator import generate_html_report

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
        console.print(f"[red]Invalid domain: {domain}[/red]")
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
def portscan(
    host: str = typer.Argument(..., help="Target host (domain or IP)"),
    ports: str = typer.Option(None, help="Comma-separated ports (e.g. 80,443,8080)"),
    threads: int = typer.Option(100, help="Thread count"),
):
    """Port scanning on target host"""
    port_list = None
    if ports:
        port_list = [int(p.strip()) for p in ports.split(",")]

    results = scan_ports(host, ports=port_list, threads=threads)

    table = Table(title=f"Open Ports — {host}")
    table.add_column("Port", style="cyan")
    table.add_column("Service", style="green")

    for port, service in results:
        table.add_row(str(port), service)

    console.print(table)

@app.command()
def headers(
    url: str = typer.Argument(..., help="Target URL (e.g. https://example.com)"),
):
    """Check security headers of a website"""
    result = check_headers(url)

    if "error" in result:
        console.print(f"[red]Error: {result['error']}[/red]")
        raise typer.Exit(1)

    table = Table(title=f"Security Headers — {result['url']}")
    table.add_column("Header", style="cyan")
    table.add_column("Status", style="green")

    for header, _ in result["present"]:
        table.add_row(header, "✅ present")

    for header in result["missing"]:
        table.add_row(header, "❌ MISSING")

    console.print(table)
    console.print(f"\n[bold]Score:[/bold] {result['score']}")

@app.command()
def version():
    """Show toolkit version"""
    console.print("[bold green]HexBytes Security Toolkit v0.2.0[/bold green]")

if __name__ == "__main__":
    app()
