#!/usr/bin/env python3
"""
🚀 Script de Setup Inicial para DeFi Monitor
Guía interactiva para configurar el proyecto por primera vez.
"""

import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from dotenv import load_dotenv, set_key

console = Console()

def print_header():
    """Muestra el header del setup."""
    console.print(Panel.fit(
        "[bold cyan]🚀 DeFi Monitor - Setup Inicial[/bold cyan]\n"
        "[dim]Configuración automatizada del proyecto[/dim]",
        border_style="cyan"
    ))

def check_env_file():
    """Verifica si existe el archivo .env."""
    env_path = Path(".env")
    
    if not env_path.exists():
        console.print("\n[yellow]⚠️  Archivo .env no encontrado[/yellow]")
        if Confirm.ask("¿Quieres crearlo ahora?", default=True):
            import shutil
            shutil.copy(".env.example", ".env")
            console.print("[green]✅ Archivo .env creado[/green]")
        else:
            console.print("[red]❌ No se puede continuar sin .env[/red]")
            sys.exit(1)
    else:
        console.print("\n[green]✅ Archivo .env encontrado[/green]")

def setup_jira():
    """Configura las credenciales de Jira."""
    console.print("\n[bold cyan]📋 Configuración de Jira[/bold cyan]")
    
    load_dotenv()
    env_path = Path(".env")
    
    # Verificar configuración actual
    jira_email = os.getenv('JIRA_EMAIL')
    jira_token = os.getenv('JIRA_API_TOKEN')
    
    if jira_email and jira_email != 'tu_email@ejemplo.com':
        console.print(f"[dim]Email actual: {jira_email}[/dim]")
        if not Confirm.ask("¿Quieres cambiar el email?", default=False):
            jira_email = None  # No cambiar
    
    if jira_email is None or jira_email == 'tu_email@ejemplo.com':
        console.print("\n[yellow]Necesitas configurar tu email de Jira[/yellow]")
        jira_email = Prompt.ask("Ingresa tu email de Atlassian")
        set_key(env_path, 'JIRA_EMAIL', jira_email)
        console.print("[green]✅ Email guardado[/green]")
    
    if not jira_token or jira_token == 'your_jira_api_token_here':
        console.print("\n[yellow]Necesitas un API Token de Jira[/yellow]")
        console.print("\n📝 Para obtenerlo:")
        console.print("   1. Ve a: [link]https://id.atlassian.com/manage-profile/security/api-tokens[/link]")
        console.print("   2. Click en 'Create API token'")
        console.print("   3. Dale un nombre (ej: 'DeFi Monitor')")
        console.print("   4. Copia el token\n")
        
        jira_token = Prompt.ask("Ingresa tu API Token", password=True)
        set_key(env_path, 'JIRA_API_TOKEN', jira_token)
        console.print("[green]✅ Token guardado[/green]")

def setup_beehiiv():
    """Configura las credenciales de Beehiiv (opcional por ahora)."""
    console.print("\n[bold cyan]📬 Configuración de Beehiiv (Opcional)[/bold cyan]")
    
    if not Confirm.ask("¿Ya tienes cuenta en Beehiiv?", default=False):
        console.print("\n[dim]No te preocupes, puedes configurarlo después.[/dim]")
        console.print("[dim]Primero enfócate en la configuración de Jira.[/dim]")
        return
    
    load_dotenv()
    env_path = Path(".env")
    
    api_key = Prompt.ask("Ingresa tu Beehiiv API Key (o presiona Enter para omitir)", default="")
    if api_key:
        set_key(env_path, 'BEEHIIV_API_KEY', api_key)
        
        pub_id = Prompt.ask("Ingresa tu Publication ID", default="")
        if pub_id:
            set_key(env_path, 'BEEHIIV_PUBLICATION_ID', pub_id)
            console.print("[green]✅ Beehiiv configurado[/green]")

def create_jira_issues():
    """Pregunta si quiere crear los issues en Jira."""
    console.print("\n[bold cyan]🎯 Crear Issues en Jira[/bold cyan]")
    
    if Confirm.ask("¿Quieres crear los issues iniciales en Jira ahora?", default=True):
        console.print("\n[dim]Ejecutando script de integración...[/dim]")
        import subprocess
        result = subprocess.run(
            [sys.executable, "scripts/jira_integration.py"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            console.print(result.stdout)
            console.print("\n[green]✅ Issues creados exitosamente[/green]")
        else:
            console.print(f"\n[red]❌ Error: {result.stderr}[/red]")
            console.print("\n[yellow]Puedes intentar de nuevo más tarde con:[/yellow]")
            console.print("[dim]python scripts/jira_integration.py[/dim]")
    else:
        console.print("\n[dim]Puedes crear los issues después con:[/dim]")
        console.print("[dim]python scripts/jira_integration.py[/dim]")

def show_next_steps():
    """Muestra los próximos pasos."""
    console.print("\n" + "="*60)
    console.print(Panel.fit(
        "[bold green]🎉 ¡Setup Completado![/bold green]\n\n"
        "[bold]Próximos Pasos:[/bold]\n"
        "1. 📋 Ve a tu Jira board:\n"
        "   [link]https://averas-1744767979220.atlassian.net/jira/software/projects/DN/boards/133[/link]\n\n"
        "2. 🎯 Comienza con el primer issue (DN-001)\n\n"
        "3. 📝 Lee la documentación:\n"
        "   • docs/JIRA-INTEGRATION.md\n"
        "   • docs/ROADMAP.md\n\n"
        "4. 🚀 Ejecuta tus primeros scripts:\n"
        "   • python scripts/collect_defi_data.py\n"
        "   • python scripts/generate_dashboard.py",
        border_style="green"
    ))

def main():
    """Función principal del setup."""
    print_header()
    
    # Paso 1: Verificar .env
    check_env_file()
    
    # Paso 2: Configurar Jira
    setup_jira()
    
    # Paso 3: Configurar Beehiiv (opcional)
    setup_beehiiv()
    
    # Paso 4: Crear issues en Jira
    create_jira_issues()
    
    # Paso 5: Mostrar próximos pasos
    show_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Setup cancelado por el usuario[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]❌ Error inesperado: {e}[/red]")
        sys.exit(1)
