"""
Script de Validação de Entrada para Estratégia Lay 0x1
Valida se um jogo do dia atende aos critérios da estratégia
"""

from typing import Dict, Optional, Tuple

import numpy as np
import pandas as pd


class Lay0x1Validator:
    """Validador de entradas para estratégia Lay 0x1"""

    def __init__(self):
        """Inicializa validador com dados históricos"""
        self.df = pd.read_csv("data_total/dados_betfair_atualizado.csv", sep=";")

        # Calcular estatísticas de xG e eficiência por time (como visitante)
        self._build_team_stats()

        # Critérios conservadores baseados em análise
        self.criteria = {
            "odds_excelente": (5.0, 999.0),  # >5.0
            "odds_bom": (3.5, 5.0),  # 3.5-5.0
            "odds_moderado": (2.5, 3.5),  # 2.5-3.5
            "odds_fraco": (0, 2.5),  # <2.5
            "xg_excelente": (0, 0.5),  # <0.5
            "xg_bom": (0.5, 1.0),  # 0.5-1.0
            "xg_moderado": (1.0, 1.5),  # 1.0-1.5
            "xg_fraco": (1.5, 999.0),  # >1.5
            "efficiency_excelente": (0, 100),  # <100%
            "efficiency_bom": (100, 150),  # 100-150%
            "efficiency_moderado": (150, 200),  # 150-200%
            "efficiency_fraco": (200, 999),  # >200%
        }

        # Scores para cada critério
        self.scores = {
            "odds_excelente": 40,
            "odds_bom": 30,
            "odds_moderado": 15,
            "odds_fraco": 5,
            "xg_excelente": 40,
            "xg_bom": 30,
            "xg_moderado": 15,
            "xg_fraco": 5,
            "efficiency_excelente": 30,
            "efficiency_bom": 20,
            "efficiency_moderado": 10,
            "efficiency_fraco": 0,
        }

    def _build_team_stats(self):
        """Calcula estatísticas históricas por time como visitante"""
        self.team_away_stats = {}

        if "Away" in self.df.columns and "xG_Away" in self.df.columns:
            for team in self.df["Away"].unique():
                team_matches = self.df[self.df["Away"] == team]

                # xG médio
                avg_xg = team_matches["xG_Away"].mean() if len(team_matches) > 0 else 0.8

                # Eficiência (gols / xG)
                total_goals = team_matches["Goals_A_FT"].sum() if "Goals_A_FT" in self.df.columns else 0
                total_xg = team_matches["xG_Away"].sum()
                efficiency = (total_goals / total_xg * 100) if total_xg > 0 else 100

                self.team_away_stats[team] = {"avg_xg": avg_xg, "efficiency": efficiency, "matches": len(team_matches)}

    def get_team_xg_estimate(self, team: str, fallback_xg: Optional[float] = None) -> float:
        """Obtém xG estimado do time baseado no histórico"""
        if team in self.team_away_stats:
            return self.team_away_stats[team]["avg_xg"]

        # Se time não encontrado, usar média geral
        if len(self.team_away_stats) > 0:
            all_xg = [stats["avg_xg"] for stats in self.team_away_stats.values()]
            return np.mean(all_xg)

        return fallback_xg if fallback_xg else 0.8

    def get_team_efficiency_estimate(self, team: str, fallback_eff: Optional[float] = None) -> float:
        """Obtém eficiência estimada do time baseada no histórico"""
        if team in self.team_away_stats:
            return self.team_away_stats[team]["efficiency"]

        # Se time não encontrado, usar média geral
        if len(self.team_away_stats) > 0:
            all_eff = [stats["efficiency"] for stats in self.team_away_stats.values()]
            return np.mean(all_eff)

        return fallback_eff if fallback_eff else 100.0

    def evaluate_odds(self, odd: float) -> Tuple[str, int]:
        """
        Avalia a odd do visitante

        Args:
            odd: Odd de vitória simples do visitante

        Returns:
            Tupla (categoria, score)
        """
        if odd >= self.criteria["odds_excelente"][0]:
            return "Excelente (>5.0)", self.scores["odds_excelente"]
        elif odd >= self.criteria["odds_bom"][0]:
            return "Bom (3.5-5.0)", self.scores["odds_bom"]
        elif odd >= self.criteria["odds_moderado"][0]:
            return "Moderado (2.5-3.5)", self.scores["odds_moderado"]
        else:
            return "Fraco (<2.5)", self.scores["odds_fraco"]

    def evaluate_xg(self, xg: float) -> Tuple[str, int]:
        """
        Avalia o xG do visitante

        Args:
            xg: Expected Goals do visitante

        Returns:
            Tupla (categoria, score)
        """
        if xg < self.criteria["xg_excelente"][1]:
            return "Excelente (<0.5)", self.scores["xg_excelente"]
        elif xg < self.criteria["xg_bom"][1]:
            return "Bom (0.5-1.0)", self.scores["xg_bom"]
        elif xg < self.criteria["xg_moderado"][1]:
            return "Moderado (1.0-1.5)", self.scores["xg_moderado"]
        else:
            return "Fraco (>1.5)", self.scores["xg_fraco"]

    def evaluate_efficiency(self, efficiency: float) -> Tuple[str, int]:
        """
        Avalia a eficiência de conversão do visitante

        Args:
            efficiency: Percentual de conversão (gols/xG * 100)

        Returns:
            Tupla (categoria, score)
        """
        if efficiency == 0:
            return "Excelente (0%)", self.scores["efficiency_excelente"]
        elif efficiency < self.criteria["efficiency_bom"][1]:
            return "Bom (100-150%)", self.scores["efficiency_bom"]
        elif efficiency < self.criteria["efficiency_moderado"][1]:
            return "Moderado (150-200%)", self.scores["efficiency_moderado"]
        else:
            return "Fraco (>200%)", self.scores["efficiency_fraco"]

    def validate_match(
        self,
        home: str,
        away: str,
        odd_away: float,
        xg_away: float,
        efficiency_away: Optional[float] = None,
    ) -> Dict:
        """
        Valida um jogo contra os critérios da estratégia

        Args:
            home: Nome do time mandante
            away: Nome do time visitante
            odd_away: Odd de vitória simples do visitante
            xg_away: Expected Goals do visitante
            efficiency_away: Eficiência de conversão (opcional)

        Returns:
            Dicionário com análise completa
        """

        # Avaliar cada critério
        odds_categoria, odds_score = self.evaluate_odds(odd_away)
        xg_categoria, xg_score = self.evaluate_xg(xg_away)

        if efficiency_away is None:
            efficiency_away = 100.0  # Default neutro

        eff_categoria, eff_score = self.evaluate_efficiency(efficiency_away)

        # Calcular score total (máximo 110)
        total_score = odds_score + xg_score + eff_score

        # Determinar recomendação
        if total_score >= 90:
            recommendation = "[ENTRAR COM CONFIANCA]"
            recommendation_color = "green"
        elif total_score >= 70:
            recommendation = "[ENTRAR COM CUIDADO]"
            recommendation_color = "yellow"
        elif total_score >= 50:
            recommendation = "[CONSIDERAR COM CAUTELA]"
            recommendation_color = "orange"
        else:
            recommendation = "[EVITAR]"
            recommendation_color = "red"

        # Buscar histórico similar
        similar = self.df[(self.df["Odd_A_Back"].between(odd_away - 0.5, odd_away + 0.5)) & (self.df["xG_Away"].between(xg_away - 0.3, xg_away + 0.3))]

        historical_wr = None
        historical_profit = None
        if len(similar) > 0:
            historical_wr = (similar["Lay_0x1_Result"] == "WIN").sum() / len(similar) * 100
            historical_profit = similar["Lay_0x1_Profit"].mean()

        return {
            "home": home,
            "away": away,
            "odd_away": odd_away,
            "xg_away": xg_away,
            "efficiency_away": efficiency_away,
            "analysis": {"odds": {"value": odd_away, "categoria": odds_categoria, "score": odds_score}, "xg": {"value": xg_away, "categoria": xg_categoria, "score": xg_score}, "efficiency": {"value": efficiency_away, "categoria": eff_categoria, "score": eff_score}},
            "total_score": total_score,
            "recommendation": recommendation,
            "recommendation_color": recommendation_color,
            "historical": {"similar_matches": len(similar), "win_rate": historical_wr, "avg_profit": historical_profit},
        }

    def print_validation(self, result: Dict) -> None:
        """Imprime resultado da validação de forma legível"""

        print("\n" + "=" * 80)
        print(f"VALIDACAO LAY 0x1: {result['home']} vs {result['away']}")
        print("=" * 80)

        print("\n[DADOS DO JOGO]")
        print(f"  Visitante (Away): {result['away']}")
        print(f"  Odd Visitante: {result['odd_away']:.2f}")
        print(f"  xG Visitante: {result['xg_away']:.2f}")
        print(f"  Eficiencia Visitante: {result['efficiency_away']:.1f}%")

        print("\n[ANALISE POR CRITERIO]")

        print(f"\n  1. ODDS DO VISITANTE: {result['analysis']['odds']['categoria']}")
        print(f"     Score: {result['analysis']['odds']['score']}/40")

        print(f"\n  2. xG DO VISITANTE: {result['analysis']['xg']['categoria']}")
        print(f"     Score: {result['analysis']['xg']['score']}/40")

        print(f"\n  3. EFICIENCIA: {result['analysis']['efficiency']['categoria']}")
        print(f"     Score: {result['analysis']['efficiency']['score']}/30")

        print(f"\n[SCORE TOTAL] {result['total_score']}/110")
        print(f"\n{result['recommendation']}")

        if result["historical"]["similar_matches"] > 0:
            print(f"\n[HISTORICO SEMELHANTE] ({result['historical']['similar_matches']} jogos):")
            print(f"  Win Rate: {result['historical']['win_rate']:.1f}%")
            print(f"  Lucro Medio: {result['historical']['avg_profit']:.2f}")

        print("\n" + "=" * 80)


if __name__ == "__main__":
    # Exemplo de uso
    validator = Lay0x1Validator()

    # Exemplo 1: Jogo com odds altas e xG baixo (excelente)
    result1 = validator.validate_match(home="Manchester United", away="Leicester City", odd_away=6.5, xg_away=0.3, efficiency_away=120.0)
    validator.print_validation(result1)

    # Exemplo 2: Jogo com odds baixas e xG alto (ruim)
    result2 = validator.validate_match(home="Barcelona", away="Real Madrid", odd_away=1.8, xg_away=2.5, efficiency_away=180.0)
    validator.print_validation(result2)

    # Exemplo 3: Jogo moderado
    result3 = validator.validate_match(home="Liverpool", away="Arsenal", odd_away=3.2, xg_away=1.1, efficiency_away=140.0)
    validator.print_validation(result3)
