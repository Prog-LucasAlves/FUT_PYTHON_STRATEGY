#!/usr/bin/env python
"""
Setup e instalação de dependências para Lay 0x1 Strategy
Execute este script uma única vez para configurar o ambiente
"""

import subprocess
import sys


def install_requirements():
    """Instala as dependências necessárias"""

    packages = {
        "streamlit": "streamlit>=1.28.0",
        "pandas": "pandas>=2.0.0",
        "numpy": "numpy>=1.24.0",
        "plotly": "plotly>=5.17.0",
    }

    print("=" * 80)
    print("INSTALACAO DE DEPENDENCIAS - LAY 0x1 STRATEGY")
    print("=" * 80)

    print("\nVerificando e instalando pacotes necessarios...")

    for name, package in packages.items():
        try:
            print(f"\n[{name.upper()}] Verificando...")
            __import__(name)
            print(f"  ✅ {name} já instalado")
        except ImportError:
            print(f"  📦 Instalando {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"  ✅ {name} instalado com sucesso")

    print("\n" + "=" * 80)
    print("INSTALACAO CONCLUIDA")
    print("=" * 80)

    print("\nProximos passos:")
    print("\n1. INICIAR DASHBOARD:")
    print("   streamlit run app_lay_0x1.py")

    print("\n2. VALIDAR UM JOGO:")
    print("   python -c \"from validate_entry import Lay0x1Validator; v = Lay0x1Validator(); print(v.validate_match('A', 'B', 4.5, 0.8))\"")

    print("\n3. LER DOCUMENTACAO:")
    print("   - README_ESTRATEGIA.md")
    print("   - QUICKSTART.md")
    print("   - IMPLEMENTACAO_COMPLETA.txt")


if __name__ == "__main__":
    install_requirements()
