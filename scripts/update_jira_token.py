#!/usr/bin/env python3
"""
Script simple para actualizar el JIRA_API_TOKEN en el archivo .env
"""

import os
import sys
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from dotenv import load_dotenv, set_key

console = Console()

def update_jira_token():
    """Actualiza el JIRA_API_TOKEN en .env"""
    
    console.print("\n[bold cyan]🔑 Actualizar JIRA API Token[/bold cyan]\n")
    
    env_path = Path(".env")
    
    if not env_path.exists():
        console.print("[red]❌ Archivo .env no encontrado[/red]")
        console.print("[dim]Ejecuta primero: python3 scripts/setup_initial.py[/dim]")
        return
    
    load_dotenv()
    
    # Mostrar instrucciones
    console.print("[yellow]📝 Pasos para obtener el API Token:[/yellow]\n")
    console.print("1. Ve a: [link]https://id.atlassian.com/manage-profile/security/api-tokens[/link]")
    console.print("2. Click en [bold]'Create API token'[/bold]")
    console.print("3. Dale un nombre: [cyan]'DeFi Monitor'[/cyan]")
    console.print("4. [bold]Copia[/bold] el token (solo se muestra una vez)")
    console.print("5. Pégalo aquí abajo\n")
    
    # Solicitar token
    token = Prompt.ask("🔐 Ingresa tu JIRA API Token", password=True)
    
    if not token:
        console.print("\n[red]❌ Token vacío, cancelando...[/red]")
        return
    
    # Guardar en .env
    try:
        set_key(env_path, 'JIRA_API_TOKEN', token)
        
        # También limpiar las comillas del email si existen
        email = os.getenv('JIRA_EMAIL', '').strip("'\"")
        if email:
            set_key(env_path, 'JIRA_EMAIL', email)
        
        console.print("\n[green]✅ Token guardado exitosamente[/green]")
        
        # Verificar
        console.print("\n[cyan]🔍 Verificando conexión...[/cyan]")
        import subprocess
        result = subprocess.run(
            [sys.executable, "scripts/test_jira_connection.py"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        
        if result.returncode == 0:
            console.print("\n[bold green]🎉 ¡Todo listo![/bold green]")
            console.print("\n[cyan]Próximo paso:[/cyan]")
            console.print("  python3 scripts/jira_integration.py")
        
    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]")

if __name__ == "__main__":
    update_jira_token()
