#!/usr/bin/env python3
"""
Script para crear issues iniciales en Jira automáticamente.
Configura el board con las primeras tareas del proyecto.
"""

import os
import sys
from pathlib import Path
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración Jira
JIRA_URL = os.getenv('JIRA_URL')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY', 'DN')

# Validar configuración
if not all([JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN]):
    print("❌ Error: Faltan variables de entorno de Jira")
    print("\nConfigura en tu archivo .env:")
    print("  - JIRA_URL")
    print("  - JIRA_EMAIL")
    print("  - JIRA_API_TOKEN")
    print("\n💡 Para obtener tu API token:")
    print("  1. Ve a: https://id.atlassian.com/manage-profile/security/api-tokens")
    print("  2. Crea un nuevo token")
    print("  3. Cópialo al archivo .env")
    sys.exit(1)

# Headers para autenticación
auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def create_issue(summary, description, issue_type="Task", story_points=None, labels=None):
    """Crea un issue en Jira."""
    url = f"{JIRA_URL}/rest/api/3/issue"
    
    payload = {
        "fields": {
            "project": {
                "key": PROJECT_KEY
            },
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": issue_type
            }
        }
    }
    
    # Añadir labels si se proporcionan
    if labels:
        payload["fields"]["labels"] = labels
    
    # Añadir story points si se proporcionan (requiere campo customizado)
    # Nota: El campo de story points varía por instalación de Jira
    if story_points:
        # Esto es un placeholder - necesitarás el ID correcto del campo
        # payload["fields"]["customfield_10016"] = story_points
        pass
    
    try:
        response = requests.post(url, json=payload, headers=headers, auth=auth)
        response.raise_for_status()
        issue_data = response.json()
        issue_key = issue_data.get('key')
        print(f"✅ Creado: {issue_key} - {summary}")
        return issue_key
    except requests.exceptions.RequestException as e:
        print(f"❌ Error creando '{summary}': {e}")
        if hasattr(e.response, 'text'):
            print(f"   Detalle: {e.response.text}")
        return None

def main():
    """Crea los issues iniciales del proyecto."""
    print("🚀 Creando issues iniciales en Jira...\n")
    
    # Epic 1: Content Production
    issues = [
        {
            "summary": "Setup Beehiiv account",
            "description": "Crear cuenta en Beehiiv y configurar la newsletter inicial. Obtener API key y publication ID.",
            "story_points": 2,
            "labels": ["automation", "setup"]
        },
        {
            "summary": "Research Aave protocol",
            "description": "Investigar el protocolo Aave a fondo: mecanismos de lending/borrowing, tokenomics, governance, y casos de uso. Documentar en learning/aave-notes.md",
            "story_points": 5,
            "labels": ["learning", "research"]
        },
        {
            "summary": "Write Newsletter #1 - Aave Deep Dive",
            "description": "Escribir la primera edición de la newsletter sobre Aave. Incluir: introducción, cómo funciona, estrategias, riesgos, y links de afiliados.",
            "story_points": 8,
            "labels": ["newsletter", "content"]
        },
        {
            "summary": "Test automation scripts",
            "description": "Probar los scripts de collect_defi_data.py y generate_dashboard.py. Asegurar que funcionan correctamente antes de automatizar.",
            "story_points": 3,
            "labels": ["automation", "testing"]
        },
        {
            "summary": "Create affiliate links database",
            "description": "Crear archivo JSON con todos los enlaces de afiliados (Binance, Aave, etc.) y sus respectivos tracking codes.",
            "story_points": 2,
            "labels": ["monetization", "data"]
        },
        {
            "summary": "Setup GitHub Actions workflow",
            "description": "Configurar GitHub Actions para ejecutar automáticamente la generación y envío de newsletter cada lunes a las 9am.",
            "story_points": 5,
            "labels": ["automation", "devops"]
        },
        {
            "summary": "Design newsletter template",
            "description": "Crear template HTML/Markdown para la newsletter con secciones: intro, protocolo destacado, métricas, estrategias, disclaimer.",
            "story_points": 3,
            "labels": ["newsletter", "design"]
        },
        {
            "summary": "Research DeFi protocols for content pipeline",
            "description": "Identificar y listar 10-15 protocolos DeFi interesantes para cubrir en futuras newsletters. Priorizar por TVL y novedad.",
            "story_points": 3,
            "labels": ["learning", "planning"]
        }
    ]
    
    created_count = 0
    for issue in issues:
        if create_issue(
            summary=issue["summary"],
            description=issue["description"],
            story_points=issue.get("story_points"),
            labels=issue.get("labels")
        ):
            created_count += 1
    
    print(f"\n✨ Proceso completado: {created_count}/{len(issues)} issues creados")
    print(f"\n🔗 Ve tu board aquí:")
    print(f"   {JIRA_URL}/jira/software/projects/{PROJECT_KEY}/boards")
    
    if created_count < len(issues):
        print("\n⚠️  Algunos issues no se crearon. Verifica tu configuración de Jira.")

if __name__ == "__main__":
    main()
