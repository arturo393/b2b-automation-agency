#!/usr/bin/env python3
"""
DeFi Monitor - Dashboard Data Generator
Genera JSON estructurado para dashboard con yields en tiempo real
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

def load_protocols_data() -> List[Dict[str, Any]]:
    """Carga datos de protocolos desde data/protocols.json"""
    data_path = Path(__file__).parent.parent / "data" / "protocols.json"
    
    if not data_path.exists():
        print(f"⚠️  Advertencia: {data_path} no existe")
        return []
    
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    # Si data es un dict con 'protocols', extraer la lista
    if isinstance(data, dict) and 'protocols' in data:
        return data['protocols']
    # Si ya es una lista, retornarla directamente
    elif isinstance(data, list):
        return data
    else:
        return []

def calculate_summary(protocols: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calcula estadísticas resumen del dashboard"""
    if not protocols:
        return {
            "total_protocols": 0,
            "avg_tvl": 0,
            "total_tvl": 0,
            "avg_apy": 0,
            "max_apy": 0,
        }
    
    tvls = [p.get('tvl', 0) for p in protocols if p.get('tvl')]
    apys = [p.get('apy', 0) for p in protocols if p.get('apy')]
    
    return {
        "total_protocols": len(protocols),
        "avg_tvl": sum(tvls) / len(tvls) if tvls else 0,
        "total_tvl": sum(tvls),
        "avg_apy": sum(apys) / len(apys) if apys else 0,
        "max_apy": max(apys) if apys else 0,
    }

def get_top_protocols(protocols: List[Dict[str, Any]], limit: int = 10) -> List[Dict[str, Any]]:
    """Obtiene top protocolos ordenados por TVL"""
    sorted_protocols = sorted(
        protocols,
        key=lambda x: x.get('tvl', 0),
        reverse=True
    )
    return sorted_protocols[:limit]

def check_alerts(protocols: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Verifica si hay yields que cumplan criterios de alerta"""
    alerts = []
    
    for protocol in protocols:
        apy = protocol.get('apy', 0)
        name = protocol.get('name', 'Unknown')
        
        # Alerta: APY > 50%
        if apy > 50:
            alerts.append({
                "protocol": name,
                "apy": apy,
                "type": "high_yield",
                "severity": "high" if apy > 100 else "medium",
                "message": f"{name} tiene APY de {apy:.2f}% (>50%)",
                "timestamp": datetime.now().isoformat()
            })
    
    return alerts

def generate_dashboard_data() -> Dict[str, Any]:
    """Genera estructura JSON completa para el dashboard"""
    print("📊 Generando datos del dashboard...")
    
    # Cargar datos
    protocols = load_protocols_data()
    
    if not protocols:
        print("❌ No hay datos de protocolos disponibles")
        return None
    
    # Generar estructura del dashboard
    dashboard = {
        "updated_at": datetime.now().isoformat(),
        "version": "1.0",
        "summary": calculate_summary(protocols),
        "top_protocols": get_top_protocols(protocols, limit=10),
        "all_protocols": protocols,
        "alerts": check_alerts(protocols),
        "metadata": {
            "source": "DeFi Llama API",
            "refresh_interval": "6 hours",
            "next_update": "Automated via GitHub Actions"
        }
    }
    
    return dashboard

def save_dashboard(dashboard: Dict[str, Any]) -> Path:
    """Guarda el dashboard en formato JSON"""
    output_dir = Path(__file__).parent.parent / "data"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "dashboard.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dashboard, f, indent=2, ensure_ascii=False)
    
    return output_file

def main():
    """Función principal"""
    print("🚀 DeFi Monitor - Dashboard Generator\n")
    
    try:
        # Generar dashboard
        dashboard = generate_dashboard_data()
        
        if not dashboard:
            print("❌ Error: No se pudo generar el dashboard")
            return
        
        # Guardar archivo
        output_file = save_dashboard(dashboard)
        
        # Mostrar resumen
        print(f"\n✅ Dashboard generado exitosamente!")
        print(f"📄 Archivo: {output_file}")
        print(f"\n📊 Resumen:")
        print(f"  - Protocolos: {dashboard['summary']['total_protocols']}")
        print(f"  - TVL Total: ${dashboard['summary']['total_tvl']:,.0f}")
        print(f"  - APY Promedio: {dashboard['summary']['avg_apy']:.2f}%")
        print(f"  - APY Máximo: {dashboard['summary']['max_apy']:.2f}%")
        print(f"  - Alertas: {len(dashboard['alerts'])}")
        
        if dashboard['alerts']:
            print(f"\n🔔 Alertas activas:")
            for alert in dashboard['alerts'][:3]:  # Mostrar max 3
                print(f"  - {alert['message']}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
