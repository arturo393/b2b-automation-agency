#!/usr/bin/env python3
"""
Script para enviar newsletter a Beehiiv usando su API
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Confirm

console = Console()
load_dotenv()

BEEHIIV_API_KEY = os.getenv('BEEHIIV_API_KEY')
BEEHIIV_PUBLICATION_ID = os.getenv('BEEHIIV_PUBLICATION_ID')
BEEHIIV_API_URL = "https://api.beehiiv.com/v2"

def get_latest_newsletter():
    """Obtiene la última newsletter generada"""
    newsletters_dir = Path(__file__).parent.parent / "content" / "newsletters"
    
    if not newsletters_dir.exists():
        console.print("[red]❌ No se encontró el directorio de newsletters[/red]")
        return None
    
    # Obtener todos los archivos .md
    newsletters = sorted(newsletters_dir.glob("*.md"), reverse=True)
    
    if not newsletters:
        console.print("[red]❌ No hay newsletters para enviar[/red]")
        console.print("[yellow]💡 Ejecuta primero: python3 scripts/generate_newsletter.py[/yellow]")
        return None
    
    latest = newsletters[0]
    console.print(f"[green]✓ Newsletter encontrada: {latest.name}[/green]")
    
    with open(latest, 'r') as f:
        content = f.read()
    
    return {
        'filename': latest.name,
        'content': content
    }

def create_post(subject, content, status='draft'):
    """
    Crea un post en Beehiiv
    
    Args:
        subject: Título del post
        content: Contenido en markdown
        status: 'draft' o 'confirmed' (publicado)
    """
    
    if not BEEHIIV_API_KEY or not BEEHIIV_PUBLICATION_ID:
        console.print("[red]❌ Credenciales de Beehiiv no configuradas[/red]")
        return False
    
    url = f"{BEEHIIV_API_URL}/publications/{BEEHIIV_PUBLICATION_ID}/posts"
    
    headers = {
        "Authorization": f"Bearer {BEEHIIV_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Extraer título del contenido (primera línea con #)
    lines = content.split('\n')
    title = subject
    for line in lines:
        if line.startswith('# '):
            title = line.replace('# ', '').strip()
            break
    
    payload = {
        "title": title,
        "content": content,
        "content_type": "markdown",
        "status": status,
        "platform": "both"  # web + email
    }
    
    try:
        console.print(f"\n[cyan]� Enviando a Beehiiv...[/cyan]")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        post_id = result.get('data', {}).get('id')
        
        console.print(f"[green]✅ Post creado exitosamente![/green]")
        console.print(f"[dim]ID: {post_id}[/dim]")
        console.print(f"[dim]Estado: {status}[/dim]")
        
        if status == 'draft':
            console.print("\n[yellow]💡 El post está en BORRADOR[/yellow]")
            console.print("[yellow]   Ve a Beehiiv para revisarlo y publicarlo[/yellow]")
        else:
            console.print("\n[green]🎉 ¡Newsletter PUBLICADA![/green]")
        
        return True
        
    except requests.exceptions.HTTPError as e:
        console.print(f"[red]❌ Error HTTP: {e}[/red]")
        if hasattr(e.response, 'text'):
            console.print(f"[dim]Detalle: {e.response.text}[/dim]")
        return False
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        return False

def main():
    """Función principal"""
    console.print("\n[bold cyan]📬 Envío de Newsletter a Beehiiv[/bold cyan]\n")
    
    # Obtener última newsletter
    newsletter = get_latest_newsletter()
    if not newsletter:
        return
    
    console.print(f"\n[bold]Newsletter:[/bold] {newsletter['filename']}")
    
    # Previsualizar primeras líneas
    preview_lines = newsletter['content'].split('\n')[:5]
    console.print("\n[dim]Previsualización:[/dim]")
    for line in preview_lines:
        console.print(f"[dim]{line}[/dim]")
    console.print("[dim]...[/dim]\n")
    
    # Preguntar qué hacer
    console.print("[yellow]¿Cómo quieres crear el post?[/yellow]")
    console.print("1. [cyan]Borrador[/cyan] - Para revisar antes de publicar")
    console.print("2. [green]Publicar[/green] - Enviar directamente a suscriptores")
    console.print("3. [red]Cancelar[/red]\n")
    
    choice = console.input("[bold]Elige una opción (1/2/3):[/bold] ")
    
    if choice == '1':
        # Crear como borrador
        subject = f"DeFi Weekly - {datetime.now().strftime('%Y-%m-%d')}"
        create_post(subject, newsletter['content'], status='draft')
        
    elif choice == '2':
        # Publicar directamente
        if Confirm.ask("\n[yellow]⚠️  ¿Estás seguro de publicar directamente?[/yellow]"):
            subject = f"DeFi Weekly - {datetime.now().strftime('%Y-%m-%d')}"
            create_post(subject, newsletter['content'], status='confirmed')
        else:
            console.print("[dim]Cancelado[/dim]")
    else:
        console.print("[dim]Cancelado[/dim]")

if __name__ == "__main__":
    main()

