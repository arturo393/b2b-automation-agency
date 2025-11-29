#!/usr/bin/env python3
"""
Script para preparar newsletter para Substack
Substack es 100% GRATIS con suscriptores ILIMITADOS
"""

from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()

def get_latest_newsletter():
    """Obtiene la última newsletter generada"""
    newsletters_dir = Path(__file__).parent.parent / "content" / "newsletters"
    newsletters = [f for f in sorted(newsletters_dir.glob("*.md"), reverse=True) 
                   if f.name != 'template.md']
    
    if not newsletters:
        console.print("[red]❌ No hay newsletters[/red]")
        console.print("[yellow]Ejecuta: python3 scripts/generate_newsletter.py[/yellow]")
        return None
    
    return newsletters[0]

def main():
    console.print("\n")
    console.print(Panel.fit(
        "[bold green]📬 Publicar en Substack (100% GRATIS)[/bold green]\n"
        "[cyan]✅ Suscriptores ilimitados[/cyan]\n"
        "[cyan]✅ Emails ilimitados[/cyan]\n"
        "[cyan]✅ Sin costos ocultos[/cyan]",
        border_style="green"
    ))
    
    newsletter = get_latest_newsletter()
    if not newsletter:
        return
    
    with open(newsletter, 'r') as f:
        content = f.read()
    
    console.print(f"\n[green]✅ Newsletter:[/green] [cyan]{newsletter.name}[/cyan]\n")
    
    # Previsualización
    lines = content.split('\n')
    console.print("[bold]📋 Primeras 20 líneas:[/bold]")
    console.print("─" * 70)
    for line in lines[:20]:
        console.print(line)
    console.print(f"[dim]... {len(lines) - 20} líneas más[/dim]")
    console.print("─" * 70)
    
    # Instrucciones
    console.print("\n[bold yellow]🚀 Cómo publicar en Substack (2 minutos):[/bold yellow]\n")
    console.print("1. Ve a: [cyan]https://substack.com/signin[/cyan]\n")
    console.print("2. Click en [bold]'New post'[/bold]\n")
    console.print("3. Título: Copia desde la línea 1 de tu newsletter\n")
    console.print("4. Contenido: Copia todo el resto\n")
    console.print("5. Click en [bold]'Publish'[/bold] 🎉\n")
    
    console.print("[green]💡 Substack acepta Markdown directamente![/green]\n")
    
    # Opciones
    console.print("[yellow]Opciones:[/yellow]")
    console.print("1. 📂 Abrir archivo")
    console.print("2. 📄 Ver contenido completo")
    console.print("3. 🌐 Abrir Substack")
    console.print("4. ❌ Salir\n")
    
    choice = input("Elige (1/2/3/4): ")
    
    if choice == '1':
        import subprocess
        subprocess.run(['open', str(newsletter)])
        console.print(f"\n[green]✅ Abierto: {newsletter.name}[/green]")
    elif choice == '2':
        console.print("\n[bold]📄 Contenido completo:[/bold]\n")
        console.print(content)
    elif choice == '3':
        import subprocess
        subprocess.run(['open', 'https://substack.com/signin'])
        console.print("\n[green]✅ Substack abierto en navegador[/green]")
    
    console.print(f"\n[dim]📍 Newsletter: {newsletter}[/dim]")
    console.print("\n[bold green]✨ ¡Substack es GRATIS para siempre![/bold green]\n")

if __name__ == "__main__":
    main()
