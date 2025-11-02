#!/usr/bin/env python3
"""
Script para recopilar datos de protocolos DeFi desde DeFi Llama API
"""

import requests
import json
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

def fetch_top_protocols(limit=10):
    """Obtiene los top protocolos DeFi por TVL"""
    try:
        url = "https://api.llama.fi/protocols"
        response = requests.get(url)
        response.raise_for_status()
        
        protocols = response.json()
        # Ordenar por TVL y tomar los top N
        top_protocols = sorted(protocols, key=lambda x: x.get('tvl', 0), reverse=True)[:limit]
        
        return top_protocols
    except Exception as e:
        console.print(f"[red]Error fetching protocols: {e}[/red]")
        return []

def save_protocols_data(protocols):
    """Guarda los datos de protocolos en JSON"""
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    output_file = data_dir / "protocols.json"
    
    # Preparar datos para guardar
    protocols_data = {
        "last_updated": datetime.now().isoformat(),
        "protocols": [
            {
                "name": p.get("name"),
                "tvl": p.get("tvl"),
                "chain": p.get("chain", "Multi-chain"),
                "category": p.get("category", "Unknown"),
                "change_1d": p.get("change_1d", 0)
            }
            for p in protocols
        ]
    }
    
    with open(output_file, 'w') as f:
        json.dump(protocols_data, f, indent=2)
    
    console.print(f"[green]✓ Datos guardados en {output_file}[/green]")
    return protocols_data

def display_protocols_table(protocols):
    """Muestra los protocolos en una tabla bonita"""
    table = Table(title="📊 Top 10 Protocolos DeFi por TVL")
    
    table.add_column("#", style="cyan", justify="right")
    table.add_column("Protocolo", style="magenta")
    table.add_column("TVL", justify="right", style="green")
    table.add_column("Chain", style="blue")
    table.add_column("Categoría", style="yellow")
    
    for idx, p in enumerate(protocols, 1):
        tvl = p.get("tvl", 0)
        tvl_formatted = f"${tvl/1_000_000_000:.2f}B" if tvl > 1_000_000_000 else f"${tvl/1_000_000:.0f}M"
        
        table.add_row(
            str(idx),
            p.get("name", "Unknown"),
            tvl_formatted,
            p.get("chain", "Multi-chain"),
            p.get("category", "Unknown")
        )
    
    console.print(table)

def main():
    """Función principal"""
    console.print("[bold blue]🔍 Recopilando datos de DeFi Llama...[/bold blue]\n")
    
    # Obtener datos
    protocols = fetch_top_protocols(10)
    
    if not protocols:
        console.print("[red]No se pudieron obtener datos[/red]")
        return
    
    # Mostrar tabla
    display_protocols_table(protocols)
    
    # Guardar datos
    console.print()
    save_protocols_data(protocols)
    
    console.print("\n[bold green]✓ Proceso completado![/bold green]")

if __name__ == "__main__":
    main()
