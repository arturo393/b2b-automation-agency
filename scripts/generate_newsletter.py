#!/usr/bin/env python3
"""
Script para generar el contenido de la newsletter basado en datos recopilados
"""

import json
from pathlib import Path
from datetime import datetime
from jinja2 import Template

def load_protocols_data():
    """Carga los datos de protocolos"""
    data_file = Path(__file__).parent.parent / "data" / "protocols.json"
    
    if not data_file.exists():
        print("❌ No se encontraron datos. Ejecuta collect_defi_data.py primero")
        return None
    
    with open(data_file, 'r') as f:
        return json.load(f)

def generate_newsletter_content(data):
    """Genera el contenido de la newsletter en Markdown"""
    
    template_str = """
# 📰 DeFi Weekly Report - {{ date }}

¡Hola DeFi enthusiast! 👋

Aquí está tu resumen semanal de los protocolos más importantes del ecosistema DeFi.

## 📊 Top 10 Protocolos por TVL

{% for protocol in protocols[:10] %}
### {{ loop.index }}. {{ protocol.name }}
- 💰 **TVL:** ${{ "%.2f" | format(protocol.tvl / 1000000000) }}B
- ⛓️ **Chain:** {{ protocol.chain }}
- 📁 **Categoría:** {{ protocol.category }}
{% if protocol.change_1d %}
- 📈 **Cambio 24h:** {{ "%.2f" | format(protocol.change_1d) }}%
{% endif %}

{% endfor %}

## 🎓 Lo que aprendí esta semana

_[Aquí agregarás tus aprendizajes sobre DeFi]_

## 💡 Estrategia de la semana

_[Aquí describirás alguna estrategia interesante]_

## 🔗 Enlaces útiles

- [Aave](https://aave.com) - Protocolo de lending
- [Uniswap](https://uniswap.org) - DEX líder
- [Curve](https://curve.fi) - Stablecoin DEX

---

**¿Te gustó esta newsletter?** Compártela con tus amigos interesados en DeFi.

*Última actualización: {{ last_updated }}*
"""
    
    template = Template(template_str)
    
    content = template.render(
        date=datetime.now().strftime("%Y-%m-%d"),
        protocols=data['protocols'],
        last_updated=data['last_updated']
    )
    
    return content

def save_newsletter(content, edition_number=1):
    """Guarda la newsletter en formato Markdown"""
    content_dir = Path(__file__).parent.parent / "content" / "newsletters"
    content_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"{edition_number:03d}-{datetime.now().strftime('%Y-%m-%d')}.md"
    output_file = content_dir / filename
    
    with open(output_file, 'w') as f:
        f.write(content)
    
    print(f"✅ Newsletter guardada en {output_file}")
    return output_file

def main():
    """Función principal"""
    print("🚀 Generando newsletter...\n")
    
    # Cargar datos
    data = load_protocols_data()
    if not data:
        return
    
    # Generar contenido
    content = generate_newsletter_content(data)
    
    # Guardar
    output_file = save_newsletter(content)
    
    print(f"\n✅ Newsletter generada exitosamente!")
    print(f"📄 Archivo: {output_file}")

if __name__ == "__main__":
    main()
