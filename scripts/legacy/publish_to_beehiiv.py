#!/usr/bin/env python3
"""
Script para preparar newsletter para publicar en Beehiiv
Nota: La API de envío de posts requiere plan Premium de Beehiiv
"""

import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()

def get_latest_newsletter():
    """Obtiene la última newsletter generada"""
    newsletters_dir = Path(__file__).parent.parent / "content" / "newsletters"
    
    # Obtener archivos excepto template
    newsletters = [f for f in sorted(newsletters_dir.glob("*.md"), reverse=True) 
                   if f.name != 'template.md']
    
    if not newsletters:
        console.print("[red]❌ No hay newsletters para publicar[/red]")
        console.print("[yellow]💡 Ejecuta: python3 scripts/generate_newsletter.py[/yellow]")
        return None
    
    return newsletters[0]

def main():
    """Función principal"""
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]📬 Publicar Newsletter en Beehiiv[/bold cyan]\n"
        "[dim]Plan gratuito: Copia y pega manualmente[/dim]",
        border_style="cyan"
    ))
    
    newsletter = get_latest_newsletter()
    if not newsletter:
        return
    
    # Leer contenido
    with open(newsletter, 'r') as f:
        content = f.read()
    
    console.print(f"\n[green]✅ Newsletter lista:[/green] [cyan]{newsletter.name}[/cyan]\n")
    
    # Mostrar previsualización
    lines = content.split('\n')
    console.print("[bold]📋 Previsualización (primeras 15 líneas):[/bold]")
    console.print("─" * 70)
    for line in lines[:15]:
        console.print(line)
    console.print(f"[dim]... y {len(lines) - 15} líneas más[/dim]")
    console.print("─" * 70)
    
    # Instrucciones
    console.print("\n[bold yellow]📝 Cómo publicar en Beehiiv:[/bold yellow]\n")
    console.print("1. Abre tu dashboard de Beehiiv:")
    console.print("   [cyan]https://app.beehiiv.com/[/cyan]\n")
    console.print("2. Click en [bold]'New Post'[/bold] o [bold]'Create'[/bold]\n")
    console.print("3. Copia el contenido del archivo:")
    console.print(f"   [cyan]{newsletter}[/cyan]\n")
    console.print("4. Pega en el editor de Beehiiv (soporta Markdown)\n")
    console.print("5. Revisa el formato y [bold]publica[/bold] 🚀\n")
    
    # Opciones
    console.print("[yellow]Opciones:[/yellow]")
    console.print("1. Abrir archivo en editor")
    console.print("2. Ver contenido completo")
    console.print("3. Salir\n")
    
    choice = input("Elige (1/2/3): ")
    
    if choice == '1':
        import subprocess
        subprocess.run(['open', str(newsletter)])
        console.print(f"\n[green]✅ Archivo abierto[/green]")
    elif choice == '2':
        console.print("\n[bold]📄 Contenido completo:[/bold]\n")
        console.print(content)
    
    console.print(f"\n[dim]💡 Newsletter ubicada en: {newsletter}[/dim]\n")

if __name__ == "__main__":
    main()
