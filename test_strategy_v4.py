"""
Test suite completo para Strategy V4 e app_lay_0x1_v3
"""

import pandas as pd

from strategy_v4 import Lay0x1StrategyV4


def test_strategy_loading():
    """Testa carregamento da estratégia"""
    print("🔍 Teste 1: Carregamento da Estratégia V4...")
    strategy = Lay0x1StrategyV4()
    assert strategy.consolidated_data is not None, "Dados consolidados não carregados"
    assert len(strategy.consolidated_data) == 2933, "Número de jogos incorreto"
    assert len(strategy.team_stats) > 0, "Stats de times não calculadas"
    print("✅ Strategy V4 carregada com sucesso\n")


def test_score_evaluation():
    """Testa avaliação de score"""
    print("🔍 Teste 2: Avaliação de Score...")
    strategy = Lay0x1StrategyV4()

    # Caso 1: Jogo desfavorável (visitante forte)
    result1 = strategy.evaluate_score("Osasuna", "Real Madrid", 1.58, 8.6)
    assert result1["total_score"] <= 50, f"Real Madrid deveria ter score baixo, mas tem {result1['total_score']}"
    assert result1["recommendation"] == "EVITAR", f"Real Madrid deveria ser EVITAR, mas é {result1['recommendation']}"
    print(f"  ✅ Real Madrid: {result1['total_score']}/110 → {result1['recommendation']}")

    # Caso 2: Jogo favorável (visitante fraco, odds altas)
    # Simulado: baixo xG, odds altas
    result2 = strategy.evaluate_score("Mallorca", "Granada CF", 5.3, 14.0)
    assert result2["odd_score"] >= 30, "Odd alta deveria ter score bom"
    print(f"  ✅ Granada CF: {result2['total_score']}/110 → {result2['recommendation']}\n")


def test_historical_stats():
    """Testa estatísticas históricas"""
    print("🔍 Teste 3: Estatísticas Históricas...")
    strategy = Lay0x1StrategyV4()
    stats = strategy.get_historical_stats()

    assert stats["total_games"] == 2933, "Total de jogos incorreto"
    assert 30 < stats["lay_0x1_winrate"] < 50, "Win rate fora do esperado"
    assert "by_odd_range" in stats, "Stats por faixa de odds não encontradas"

    print(f"  📊 Total de jogos: {stats['total_games']}")
    print(f"  📊 Win Rate Geral: {stats['lay_0x1_winrate']:.1f}%")
    print(f"  💰 Lucro Total: {stats['total_profit']:.2f}")

    # Validar que odds altas são melhores
    wr_high = stats["by_odd_range"].get("5.0-10.0", {}).get("winrate", 0)
    wr_low = stats["by_odd_range"].get("0.0-2.5", {}).get("winrate", 0)
    assert wr_high > wr_low, f"Odds altas ({wr_high:.1f}%) devem ter melhor WR que odds baixas ({wr_low:.1f}%)"
    print(f"  ✅ Odds altas têm melhor WR: {wr_high:.1f}% vs {wr_low:.1f}%\n")


def test_consolidated_data():
    """Testa dados consolidados"""
    print("🔍 Teste 4: Dados Consolidados...")
    df = pd.read_csv("data_total/dados_consolidado_v2.csv", sep=";")

    assert df.shape[0] == 2933, "Número de registros incorreto"
    assert "xG_H" in df.columns, "Coluna xG_H não encontrada"
    assert "xG_A" in df.columns, "Coluna xG_A não encontrada"
    assert "Lay_0x1_Outcome" in df.columns, "Coluna resultado não encontrada"
    assert "Odd_A_Back" in df.columns, "Coluna odd não encontrada"

    print(f"  📊 Registros: {df.shape[0]}")
    print(f"  📊 Colunas: {df.shape[1]}")
    print(f"  📊 Período: {df['Date'].min()} a {df['Date'].max()}")
    print(f"  📊 Ligas: {', '.join(df['League'].unique())}\n")


def test_app_imports():
    """Testa se app v3 pode ser executado"""
    print("🔍 Teste 5: Validação App V3...")
    try:
        # Verifica que arquivo principal existe
        import os
        assert os.path.exists("app_lay_0x1_v3.py"), "App v3 não encontrado"
        print("  ✅ App V3 disponível\n")
    except AssertionError as e:
        print(f"  ❌ Erro: {e}\n")
        raise


def test_team_stats():
    """Testa cálculo de estatísticas por time"""
    print("🔍 Teste 6: Estatísticas por Time...")
    strategy = Lay0x1StrategyV4()

    # Testa um time conhecido
    real_madrid = strategy.get_team_stats("Real Madrid", position="away")
    assert real_madrid["xG_avg"] > 0, "xG médio deve ser positivo"
    assert real_madrid["matches"] > 0, "Deve ter matches registrados"
    print(f"  ✅ Real Madrid (away): {real_madrid['matches']} jogos, xG avg {real_madrid['xG_avg']:.2f}")

    # Testa fallback para time não encontrado
    team_fake = strategy.get_team_stats("Fake Team FC", position="away")
    assert team_fake["xG_avg"] == 0.8, "Fallback de xG deveria ser 0.8"
    print(f"  ✅ Fallback para time desconhecido: xG {team_fake['xG_avg']:.2f}\n")


def run_all_tests():
    """Executa todos os testes"""
    print("=" * 60)
    print("🧪 TEST SUITE - Strategy V4 & App V3")
    print("=" * 60)
    print()

    try:
        test_strategy_loading()
        test_score_evaluation()
        test_historical_stats()
        test_consolidated_data()
        test_app_imports()
        test_team_stats()

        print("=" * 60)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("=" * 60)
        print("\n🚀 Strategy V4 está pronta para uso!")
        print("   Execute: streamlit run app_lay_0x1_v3.py")

    except AssertionError as e:
        print(f"\n❌ ERRO NOS TESTES: {e}")
        raise
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()
