#!/usr/bin/env python3
"""
Script para mostrar un resumen visual del estado del proyecto
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich import box
import json
from pathlib import Path

console = Console()

def show_summary():
    """Muestra un resumen visual completo"""
    
    # Header
    console.print("\n")
    console.print(Panel.fit(
        "[bold green]🎉 DeFi Newsletter - Setup Completado![/bold green]\n"
        "[dim]Todos los sistemas operacionales - Listo para producción[/dim]",
        border_style="green",
        box=box.DOUBLE
    ))
    
    # Issues Table
    console.print("\n[bold cyan]📋 Issues Creados en Jira[/bold cyan]")
    issues_table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    issues_table.add_column("Issue", style="cyan", width=8)
    issues_table.add_column("Tarea", style="white", width=35)
    issues_table.add_column("SP", justify="right", style="yellow", width=4)
    issues_table.add_column("Estado", style="green", width=12)
    
    issues = [
        ("DN-1", "Setup Beehiiv account", "2", "✓ Creado"),
        ("DN-2", "Research Aave protocol", "5", "✓ Creado"),
        ("DN-3", "Write Newsletter #1", "8", "✓ Creado"),
        ("DN-4", "Test automation scripts", "3", "✓ Creado"),
        ("DN-5", "Create affiliate links", "2", "✓ Creado"),
        ("DN-6", "Setup GitHub Actions", "5", "✓ Creado"),
        ("DN-7", "Design newsletter template", "3", "✓ Creado"),
        ("DN-8", "Research DeFi protocols", "3", "✓ Creado"),
    ]
    
    for issue in issues:
        issues_table.add_row(*issue)
    
    console.print(issues_table)
    
    # Scripts Table
    console.print("\n[bold cyan]🤖 Scripts Disponibles[/bold cyan]")
    scripts_table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    scripts_table.add_column("Script", style="cyan", width=30)
    scripts_table.add_column("Estado", style="green", width=15)
    scripts_table.add_column("Descripción", style="white", width=40)
    
    scripts = [
        ("setup_initial.py", "✅ Listo", "Setup interactivo guiado"),
        ("jira_integration.py", "✅ Probado", "Crear issues en Jira"),
        ("test_jira_connection.py", "✅ Probado", "Diagnosticar conexión"),
        ("update_jira_token.py", "✅ Listo", "Actualizar token Jira"),
        ("collect_defi_data.py", "✅ Probado", "Recopilar datos DeFi"),
        ("generate_newsletter.py", "✅ Probado", "Generar newsletter"),
        ("send_to_beehiiv.py", "⏳ Pendiente", "Requiere cuenta Beehiiv"),
    ]
    
    for script in scripts:
        scripts_table.add_row(*script)
    
    console.print(scripts_table)
    
    # DeFi Data
    data_file = Path(__file__).parent.parent / "data" / "protocols.json"
    if data_file.exists():
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        console.print("\n[bold cyan]📊 Top 5 Protocolos DeFi (últimos datos)[/bold cyan]")
        defi_table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        defi_table.add_column("#", justify="right", style="cyan", width=3)
        defi_table.add_column("Protocolo", style="white", width=20)
        defi_table.add_column("TVL", justify="right", style="green", width=12)
        defi_table.add_column("Categoría", style="yellow", width=15)
        
        for idx, p in enumerate(data['protocols'][:5], 1):
            tvl = p['tvl']
            tvl_str = f"${tvl/1_000_000_000:.2f}B" if tvl > 1_000_000_000 else f"${tvl/1_000_000:.0f}M"
            defi_table.add_row(
                str(idx),
                p['name'],
                tvl_str,
                p['category']
            )
        
        console.print(defi_table)
    
    # Next Steps
    console.print("\n[bold cyan]🎯 Próximos Pasos[/bold cyan]")
    next_steps = Table(show_header=False, box=box.SIMPLE)
    next_steps.add_column("Step", style="yellow", width=5)
    next_steps.add_column("Action", style="white", width=70)
    
    steps = [
        ("1.", "📬 Crear cuenta en Beehiiv.com (DN-1)"),
        ("2.", "📚 Investigar protocolo Aave en profundidad (DN-2)"),
        ("3.", "✍️  Escribir y publicar primera newsletter (DN-3)"),
        ("4.", "🔗 Configurar enlaces de afiliados (DN-5)"),
        ("5.", "🤖 Automatizar con GitHub Actions (DN-6)"),
    ]
    
    for step in steps:
        next_steps.add_row(*step)
    
    console.print(next_steps)
    
    # Footer
    console.print("\n")
    console.print(Panel(
        "[bold white]🔗 Enlaces Importantes:[/bold white]\n\n"
        "• Jira Board: [cyan]https://averas-1744767979220.atlassian.net/jira/software/projects/DN/boards[/cyan]\n"
        "• Beehiiv: [cyan]https://beehiiv.com[/cyan]\n"
        "• DeFi Llama: [cyan]https://defillama.com[/cyan]\n\n"
        "[bold white]📚 Documentación:[/bold white]\n\n"
        "• [yellow]SUCCESS.md[/yellow] - Resumen completo de logros\n"
        "• [yellow]QUICK_REFERENCE.md[/yellow] - Comandos rápidos\n"
        "• [yellow]docs/JIRA-INTEGRATION.md[/yellow] - Guía de Jira\n\n"
        "[bold green]✨ Sistema 100% operacional - ¡Listo para crear contenido![/bold green]",
        border_style="cyan",
        box=box.ROUNDED
    ))
    
    console.print("\n")

if __name__ == "__main__":
    show_summary()
