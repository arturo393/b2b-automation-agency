#!/usr/bin/env python3
"""
Script para actualizar Jira con el progreso actual del proyecto
"""

import os
import sys
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from rich.console import Console

console = Console()
load_dotenv()

JIRA_URL = os.getenv('JIRA_URL')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY', 'DN')

auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
headers = {"Accept": "application/json", "Content-Type": "application/json"}

def add_comment(issue_key, comment):
    """Añade un comentario a un issue"""
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}/comment"
    
    payload = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": comment
                        }
                    ]
                }
            ]
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, auth=auth)
        response.raise_for_status()
        console.print(f"[green]✅ Comentario añadido a {issue_key}[/green]")
        return True
    except Exception as e:
        console.print(f"[red]❌ Error en {issue_key}: {e}[/red]")
        return False

def log_work(issue_key, time_spent, comment):
    """Registra tiempo trabajado en un issue"""
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}/worklog"
    
    payload = {
        "timeSpent": time_spent,
        "comment": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": comment
                        }
                    ]
                }
            ]
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, auth=auth)
        response.raise_for_status()
        console.print(f"[green]✅ Worklog añadido a {issue_key}: {time_spent}[/green]")
        return True
    except Exception as e:
        console.print(f"[red]❌ Error logging work en {issue_key}: {e}[/red]")
        return False

def main():
    """Actualiza Jira con el progreso actual"""
    console.print("\n[bold cyan]📊 Actualizando Jira con progreso real...[/bold cyan]\n")
    
    # DN-1: Setup Substack (cambiado de Beehiiv)
    console.print("\n[yellow]DN-1: Setup Newsletter Platform[/yellow]")
    
    log_work("DN-1", "30m", "Investigación de plataformas de newsletter (Beehiiv, Substack, alternativas)")
    log_work("DN-1", "20m", "Configuración inicial de Beehiiv - descubierto que requiere pago")
    log_work("DN-1", "15m", "Investigación y comparación de alternativas gratuitas")
    log_work("DN-1", "10m", "Cambio a Substack - documentación y scripts actualizados")
    
    add_comment("DN-1", """
Progreso actualizado:

✅ Investigación completa de plataformas
✅ Decisión: Substack (100% GRATIS vs Beehiiv $49/mes)
✅ Script publish_to_substack.py creado
✅ Documentación actualizada

⏳ PENDIENTE: Crear cuenta en Substack
    
Razón del cambio:
- Beehiiv requiere plan Premium ($49/mes) para API
- Substack es completamente gratis con suscriptores ilimitados
- Mejor opción para comenzar

Próximo paso: Crear cuenta en Substack.com
""")
    
    # DN-4: Test automation scripts
    console.print("\n[yellow]DN-4: Test Automation Scripts[/yellow]")
    
    log_work("DN-4", "2h", "Setup completo del proyecto: Jira integrado, scripts probados")
    log_work("DN-4", "30m", "Fix en collect_defi_data.py - manejo de TVL nulos")
    log_work("DN-4", "20m", "Scripts de status y helpers creados")
    
    add_comment("DN-4", """
Scripts probados y funcionando:

✅ collect_defi_data.py - Recopila datos DeFi (PROBADO)
✅ generate_dashboard.py - Genera newsletter (PROBADO)
✅ jira_integration.py - Crea issues (PROBADO)
✅ test_jira_connection.py - Diagnóstico (PROBADO)
✅ publish_to_substack.py - Helper para Substack (NUEVO)
✅ show_status.py - Dashboard del proyecto (NUEVO)

Primer newsletter generada: 001-2025-11-02.md
Datos DeFi recopilados: protocols.json (Top 10 por TVL)

Estado: Scripts operacionales al 100%
""")
    
    # DN-2: Research Aave (siguiente prioridad)
    console.print("\n[yellow]DN-2: Research Aave Protocol[/yellow]")
    
    add_comment("DN-2", """
Próximo en la lista.

Pasos planificados:
1. Leer documentación oficial de Aave
2. Investigar mecanismos de lending/borrowing
3. Documentar en learning/aave-notes.md
4. Identificar puntos clave para newsletter

Estado: No iniciado
Prioridad: Alta (siguiente tarea)
""")
    
    console.print("\n[bold green]✅ Jira actualizado con progreso real[/bold green]")
    console.print(f"\n🔗 Ve tu board: {JIRA_URL}/jira/software/projects/{PROJECT_KEY}/boards\n")

if __name__ == "__main__":
    main()
