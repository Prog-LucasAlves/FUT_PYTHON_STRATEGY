"""
Lay 0x1 Strategy V3 - Usando dados consolidados
Integra Betfair + FootyStats em um único arquivo
"""

from typing import Dict, Optional

import numpy as np
import pandas as pd


class Lay0x1StrategyV3:
    """Estratégia Lay 0x1 com dados consolidados Betfair + FootyStats"""

    def __init__(self):
        """Inicializa com dados consolidados"""
        try:
            # Tentar carregar dados consolidados (novo)
            self.df = pd.read_csv("data_total/dados_consolidado_betfair_footystats.csv", sep=";")
            self.source = "CONSOLIDADO"
            print(f"✓ Carregado: dados_consolidado_betfair_footystats.csv ({len(self.df)} jogos)")
        except FileNotFoundError:
            # Fallback para FootyStats
            self.df = pd.read_csv("data_total/dados_footystats.csv", sep=";")
            self.source = "FOOTYSTATS"
            print(f"✓ Fallback: dados_footystats.csv ({len(self.df)} jogos)")

        # Construir estatísticas por time
        self._build_team_statistics()

    def _build_team_statistics(self):
        """Calcula estatísticas por time como visitante"""
        self.team_stats = {}

        df = self.df

        # Agrupar por time como visitante
        for team in df["Away"].unique():
            away_matches = df[df["Away"] == team].copy()

            if len(away_matches) > 0:
                xg_away = away_matches["xG_A"].mean() if "xG_A" in away_matches.columns else 0.8
                goals_away = away_matches["Goals_A_FT"].sum() if "Goals_A_FT" in away_matches.columns else 0

                # Eficiência
                if xg_away > 0:
                    efficiency = (goals_away / (xg_away * len(away_matches))) * 100
                else:
                    efficiency = 100

                # Cálculo de minuto de gol (média)
                goal_minute = 45  # Default

                self.team_stats[team] = {
                    "xG_Away": xg_away,
                    "Goals_Away": goals_away,
                    "Efficiency": efficiency,
                    "Matches": len(away_matches),
                    "Attacks": away_matches.get("Attacks_A", pd.Series([np.nan])).mean() if "Attacks_A" in away_matches.columns else 100,
                    "ShotsOnTarget": away_matches.get("ShotsOnTarget_A", pd.Series([np.nan])).mean() if "ShotsOnTarget_A" in away_matches.columns else 5,
                    "DangerousAttacks": away_matches.get("DangerousAttacks_A", pd.Series([np.nan])).mean() if "DangerousAttacks_A" in away_matches.columns else 30,
                    "Goal_Timing": goal_minute,
                }

    def get_team_xg(self, team: str) -> float:
        """Obtém xG real do time como visitante"""
        if team in self.team_stats:
            return self.team_stats[team]["xG_Away"]
        # Fallback: média geral
        if self.team_stats:
            return np.mean([s["xG_Away"] for s in self.team_stats.values()])
        return 0.8

    def get_team_efficiency(self, team: str) -> float:
        """Obtém eficiência real"""
        if team in self.team_stats:
            return self.team_stats[team]["Efficiency"]
        if self.team_stats:
            return np.mean([s["Efficiency"] for s in self.team_stats.values()])
        return 100.0

    def get_goal_timing(self, team: str) -> float:
        """Minuto médio de gol"""
        if team in self.team_stats:
            return self.team_stats[team]["Goal_Timing"]
        return 45.0

    def evaluate_score(
        self,
        home: str,
        away: str,
        odd_away: float,
        xg_away: Optional[float] = None,
        efficiency_away: Optional[float] = None,
        goal_timing: Optional[float] = None,
    ) -> Dict:
        """Calcula score da entrada (0-110)"""

        # Usar valores reais se não fornecidos
        if xg_away is None:
            xg_away = self.get_team_xg(away)
        if efficiency_away is None:
            efficiency_away = self.get_team_efficiency(away)
        if goal_timing is None:
            goal_timing = self.get_goal_timing(away)

        scores = {}

        # 1. ODD (0-40)
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

        # 2. xG (0-40)
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

        # 3. EFFICIENCY (0-30)
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

        # Total
        total_score = scores["odd"] + scores["xg"] + scores["eff"]

        # Recomendação
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
            "source": self.source,
        }

    def get_team_info(self, team: str) -> Dict:
        """Informações completas do time"""
        if team in self.team_stats:
            return self.team_stats[team]
        return {}


if __name__ == "__main__":
    strategy = Lay0x1StrategyV3()

    print("=" * 80)
    print("LAY 0x1 STRATEGY V3 - TESTE")
    print("=" * 80)

    # Teste com jogo real
    result = strategy.evaluate_score(
        home="Athletico-PR",
        away="Botafogo FR",
        odd_away=4.3,
    )

    print(f"\nJogo: {result['home']} x {result['away']}")
    print(f"Odd: {result['odd_away']}")
    print("\nAnálise:")
    print(f"  xG Away: {result['xg_away']} ({result['xg_cat']}) = {result['xg_score']} pts")
    print(f"  Eficiência: {result['efficiency_away']}% ({result['eff_cat']}) = {result['eff_score']} pts")
    print(f"  Odd: ({result['odd_cat']}) = {result['odd_score']} pts")
    print(f"\nScore Total: {result['total_score']}/110")
    print(f"Recomendação: {result['color']} {result['recommendation']}")
    print(f"Confiança: {result['confidence']:.1f}%")
    print(f"Fonte de dados: {result['source']}")
