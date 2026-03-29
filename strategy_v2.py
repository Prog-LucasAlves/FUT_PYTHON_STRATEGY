"""
Script de Estratégia Lay 0x1 Reformulado
Baseado em análise de xG real, minuto de gol e padrões de eficiência
Integra dados de footystats com informações detalhadas
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple


class Lay0x1StrategyV2:
    """Validador de entradas para estratégia Lay 0x1 - Versão 2 com dados reais"""

    def __init__(self):
        """Inicializa estratégia com dados históricos"""
        try:
            self.df_footystats = pd.read_csv("data_total/dados_footystats.csv", sep=";")
            self.has_footystats = True
        except:
            self.df_footystats = None
            self.has_footystats = False

        try:
            self.df_betfair = pd.read_csv("data_total/dados_betfair_atualizado.csv", sep=";")
            self.has_betfair = True
        except:
            self.df_betfair = None
            self.has_betfair = False

        # Construir estatísticas por time
        self._build_team_statistics()

    def _build_team_statistics(self):
        """Constrói estatísticas detalhadas por time (visitante)"""
        self.team_stats = {}

        if self.has_footystats:
            df = self.df_footystats

            # Agrupar por time como visitante
            for team in df["Away"].unique():
                away_matches = df[df["Away"] == team].copy()

                if len(away_matches) > 0:
                    self.team_stats[team] = {
                        "xG_Away": away_matches["xG_A"].mean(),
                        "Goals_Away": away_matches["Goals_A_FT"].sum(),
                        "Efficiency": (
                            away_matches["Goals_A_FT"].sum()
                            / away_matches["xG_A"].sum()
                            * 100
                            if away_matches["xG_A"].sum() > 0
                            else 100
                        ),
                        "Matches": len(away_matches),
                        "Attacks": away_matches["Attacks_A"].mean(),
                        "DangerousAttacks": away_matches["DangerousAttacks_A"].mean(),
                        "ShotsOnTarget": away_matches["ShotsOnTarget_A"].mean(),
                        "Goals_Min_Avg": self._calculate_goal_minute(
                            away_matches
                        ),  # Minuto médio de gol
                    }

    def _calculate_goal_minute(self, matches_df: pd.DataFrame) -> float:
        """Calcula minuto médio de gol sofrido como visitante (para Lay 0x1)"""
        total_minutes = 0
        total_goals = 0

        if "Goals_A_Min" in matches_df.columns:
            for minutes_str in matches_df["Goals_A_Min"]:
                if pd.notna(minutes_str) and minutes_str != "":
                    try:
                        # Converter string de minutos em lista
                        minutes = [
                            int(m.strip()) for m in str(minutes_str).split(",") if m.strip()
                        ]
                        total_minutes += sum(minutes)
                        total_goals += len(minutes)
                    except:
                        pass

        return total_minutes / total_goals if total_goals > 0 else 45  # Padrão: meio do jogo

    def get_team_xg(self, team: str) -> float:
        """Obtém xG real do time como visitante"""
        if team in self.team_stats:
            return self.team_stats[team]["xG_Away"]
        # Fallback: média geral
        if self.team_stats:
            return np.mean([s["xG_Away"] for s in self.team_stats.values()])
        return 0.8  # Padrão

    def get_team_efficiency(self, team: str) -> float:
        """Obtém eficiência real do time como visitante (gols/xG)"""
        if team in self.team_stats:
            return self.team_stats[team]["Efficiency"]
        # Fallback: média geral
        if self.team_stats:
            return np.mean([s["Efficiency"] for s in self.team_stats.values()])
        return 100.0  # Padrão

    def get_goal_timing(self, team: str) -> float:
        """Obtém minuto médio de gol sofrido como visitante"""
        if team in self.team_stats:
            return self.team_stats[team]["Goals_Min_Avg"]
        # Fallback: média geral
        if self.team_stats:
            return np.mean([s["Goals_Min_Avg"] for s in self.team_stats.values()])
        return 45  # Padrão: metade do jogo

    def evaluate_score(
        self,
        home: str,
        away: str,
        odd_away: float,
        xg_away: Optional[float] = None,
        efficiency_away: Optional[float] = None,
        goal_timing: Optional[float] = None,
    ) -> Dict:
        """
        Avalia entrada para Lay 0x1

        Critérios:
        1. ODD: Maior odd = melhor (visitante é azarão)
        2. xG: Menor xG = melhor (menos chances)
        3. Eficiência: Maior eficiência (>150%) = pior (converte bem)
        4. Timing: Gols tardios (>50 min) = melhor para Lay

        Fórmula de Score (0-110):
        - Odds: 0-40
        - xG: 0-40
        - Efficiency: 0-30
        """

        # Usar valores reais se não fornecidos
        if xg_away is None:
            xg_away = self.get_team_xg(away)
        if efficiency_away is None:
            efficiency_away = self.get_team_efficiency(away)
        if goal_timing is None:
            goal_timing = self.get_goal_timing(away)

        # Scores por critério
        scores = {}

        # 1. ODD (0-40): Maior = melhor
        if odd_away >= 5.0:
            scores["odd"] = 40
            scores["odd_cat"] = "Excelente (>5.0)"
        elif odd_away >= 3.5:
            scores["odd"] = 30
            scores["odd_cat"] = "Bom (3.5-5.0)"
        elif odd_away >= 2.5:
            scores["odd"] = 15
            scores["odd_cat"] = "Moderado (2.5-3.5)"
        else:
            scores["odd"] = 5
            scores["odd_cat"] = "Fraco (<2.5)"

        # 2. xG (0-40): Menor = melhor
        if xg_away < 0.5:
            scores["xg"] = 40
            scores["xg_cat"] = "Excelente (<0.5)"
        elif xg_away < 1.0:
            scores["xg"] = 30
            scores["xg_cat"] = "Bom (0.5-1.0)"
        elif xg_away < 1.5:
            scores["xg"] = 15
            scores["xg_cat"] = "Moderado (1.0-1.5)"
        else:
            scores["xg"] = 5
            scores["xg_cat"] = "Fraco (>1.5)"

        # 3. EFFICIENCY (0-30): Menor = melhor (não converte bem)
        if efficiency_away < 100:
            scores["eff"] = 30
            scores["eff_cat"] = "Excelente (<100%)"
        elif efficiency_away < 150:
            scores["eff"] = 20
            scores["eff_cat"] = "Bom (100-150%)"
        elif efficiency_away < 200:
            scores["eff"] = 10
            scores["eff_cat"] = "Moderado (150-200%)"
        else:
            scores["eff"] = 0
            scores["eff_cat"] = "Fraco (>200%)"

        # Calcular total
        total_score = scores["odd"] + scores["xg"] + scores["eff"]

        # Recomendação baseada em score
        if total_score >= 90:
            recommendation = "ENTRAR COM CONFIANCA"
            color = "🟢"
        elif total_score >= 70:
            recommendation = "ENTRAR COM CUIDADO"
            color = "🟡"
        else:
            recommendation = "EVITAR"
            color = "🔴"

        return {
            "home": home,
            "away": away,
            "odd_away": odd_away,
            "xg_away": round(xg_away, 3),
            "efficiency_away": round(efficiency_away, 1),
            "goal_timing": round(goal_timing, 1),
            "odd_score": scores["odd"],
            "odd_cat": scores["odd_cat"],
            "xg_score": scores["xg"],
            "xg_cat": scores["xg_cat"],
            "eff_score": scores["eff"],
            "eff_cat": scores["eff_cat"],
            "total_score": total_score,
            "recommendation": recommendation,
            "color": color,
            "confidence": total_score / 110 * 100,
        }

    def get_team_info(self, team: str) -> Dict:
        """Obtém informações detalhadas do time"""
        if team in self.team_stats:
            return self.team_stats[team]
        return {}


if __name__ == "__main__":
    strategy = Lay0x1StrategyV2()

    # Teste
    print("=" * 80)
    print("TESTE - LAY 0X1 STRATEGY V2")
    print("=" * 80)

    result = strategy.evaluate_score(
        home="Athletico-PR",
        away="Botafogo FR",
        odd_away=4.3,
    )

    print(f"\nJogo: {result['home']} x {result['away']}")
    print(f"Odd: {result['odd_away']}")
    print(f"\nAnálise:")
    print(f"  xG Away: {result['xg_away']} ({result['xg_cat']}) = {result['xg_score']} pts")
    print(f"  Eficiência: {result['efficiency_away']}% ({result['eff_cat']}) = {result['eff_score']} pts")
    print(f"  Odd: ({result['odd_cat']}) = {result['odd_score']} pts")
    print(f"  Minuto médio de gol: {result['goal_timing']} min")
    print(f"\nScore Total: {result['total_score']}/110")
    print(f"Recomendação: {result['color']} {result['recommendation']}")
    print(f"Confiança: {result['confidence']:.1f}%")
