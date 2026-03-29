"""
Lay 0x1 Strategy V4
Versão final usando dados consolidados de Betfair + FootyStats
Baseado em: https://www.youtube.com/watch?v=5Tm7tQvxgJQ
"""

from pathlib import Path
from typing import Dict, Optional

import pandas as pd


class Lay0x1StrategyV4:
    """
    Estratégia de Lay 0x1 (para 0 gols do visitante)
    Usa dados consolidados como principal, fallback para FootyStats, depois hardcoded
    """

    def __init__(self):
        self.data_dir = Path(__file__).parent / "data_total"
        self.consolidated_data = None
        self.footystats_data = None
        self.team_stats = {}

        self._load_data()

    def _load_data(self):
        """Carrega dados consolidados e FootyStats como fallback"""
        # Consolidado (principal)
        consolidated_path = self.data_dir / "dados_consolidado_v2.csv"
        if consolidated_path.exists():
            self.consolidated_data = pd.read_csv(consolidated_path, sep=";")
            print(f"✓ Dados consolidados carregados: {len(self.consolidated_data)} registros")

        # FootyStats (fallback)
        footystats_path = self.data_dir / "dados_footystats.csv"
        if footystats_path.exists():
            self.footystats_data = pd.read_csv(footystats_path, sep=";")
            print(f"✓ FootyStats carregado: {len(self.footystats_data)} registros")

        # Calcula estatísticas por time
        self._calculate_team_stats()

    def _calculate_team_stats(self):
        """Calcula estatísticas agregadas por time a partir dos dados consolidados"""
        if self.consolidated_data is None:
            return

        df = self.consolidated_data

        # Para cada time, calcula estatísticas como home e away
        all_teams = set(df["Home"].unique()) | set(df["Away"].unique())

        for team in all_teams:
            home_games = df[df["Home"] == team]
            away_games = df[df["Away"] == team]

            self.team_stats[team] = {
                "home": {
                    "matches": len(home_games),
                    "xG_avg": home_games["xG_H"].mean() if len(home_games) > 0 else 0.8,
                    "goals_avg": home_games["Goals_H_FT"].mean() if len(home_games) > 0 else 1.2,
                    "possession_avg": home_games["Possession_H"].mean() if len(home_games) > 0 else 50,
                    "shots_avg": home_games["Shots_H"].mean() if len(home_games) > 0 else 12,
                },
                "away": {
                    "matches": len(away_games),
                    "xG_avg": away_games["xG_A"].mean() if len(away_games) > 0 else 0.8,
                    "goals_avg": away_games["Goals_A_FT"].mean() if len(away_games) > 0 else 1.0,
                    "possession_avg": away_games["Possession_A"].mean() if len(away_games) > 0 else 50,
                    "shots_avg": away_games["Shots_A"].mean() if len(away_games) > 0 else 10,
                },
            }

    def get_team_stats(self, team: str, position: str = "away") -> Dict:
        """Retorna estatísticas do time, com fallback para valores padrão"""
        if team in self.team_stats:
            return self.team_stats[team][position]

        # Fallback: valores padrão
        return {
            "matches": 0,
            "xG_avg": 0.8,
            "goals_avg": 1.0 if position == "away" else 1.2,
            "possession_avg": 50,
            "shots_avg": 10 if position == "away" else 12,
        }

    def evaluate_score(self, home: str, away: str, odd_away: float, odd_0x1_lay: float) -> Dict:
        """
        Avalia um jogo e retorna score de confiança (0-110)

        Fatores:
        1. Odd do visitante (40 pontos) - odds altas = menos favorável
        2. xG do visitante (40 pontos) - xG baixo = favorável
        3. Eficiência defensiva (30 pontos) - defesa forte = favorável

        Estratégia de Lay 0x1:
        - Apostamos que o visitante NÃO marca (0 gols)
        - Quanto menor xG do visitante, melhor
        - Quanto maior odd da aposta, menos favorável
        """

        away_stats = self.get_team_stats(away, position="away")

        # xG do visitante (quanto menor, melhor para lay)
        xg_away = away_stats["xG_avg"]

        # Eficiência defensiva do mandante (inverso dos gols sofridos)
        home_stats = self.get_team_stats(home, position="home")

        # Calcula componentes de score

        # 1. COMPONENTE ODD (0-40)
        # Odds altas = visitante menos favorito = melhor para lay
        if odd_away > 5.0:
            odd_score = 40
        elif odd_away > 3.5:
            odd_score = 30
        elif odd_away > 2.5:
            odd_score = 15
        else:
            odd_score = 5

        # 2. COMPONENTE xG DO VISITANTE (0-40)
        # xG baixo = chance baixa de gol = bom para lay 0x1
        if xg_away < 0.5:
            xg_score = 40
        elif xg_away < 1.0:
            xg_score = 30
        elif xg_away < 1.5:
            xg_score = 15
        else:
            xg_score = 5

        # 3. COMPONENTE EFICIÊNCIA DEFENSIVA (0-30)
        # Calcula "eficiência defensiva" como quantidade de shots sofridos vs gols
        shots_conceded_avg = away_stats["shots_avg"]

        # Razão de eficiência: quanto maior, menos gols por shot
        if shots_conceded_avg < 8:
            defense_score = 30
        elif shots_conceded_avg < 12:
            defense_score = 20
        elif shots_conceded_avg < 15:
            defense_score = 10
        else:
            defense_score = 0

        # Score total (0-110)
        total_score = odd_score + xg_score + defense_score

        # Recomendação
        if total_score >= 90:
            recommendation = "CONFIANÇA"
            risk = "Baixo"
        elif total_score >= 70:
            recommendation = "CUIDADO"
            risk = "Médio"
        else:
            recommendation = "EVITAR"
            risk = "Alto"

        return {
            "home": home,
            "away": away,
            "odd_away": odd_away,
            "odd_0x1_lay": odd_0x1_lay,
            "xg_away": xg_away,
            "shots_away_avg": shots_conceded_avg,
            "odd_score": odd_score,
            "xg_score": xg_score,
            "defense_score": defense_score,
            "total_score": total_score,
            "recommendation": recommendation,
            "risk": risk,
            "rationale": self._generate_rationale(total_score, xg_away, odd_away, home, away),
        }

    def _generate_rationale(self, score: int, xg_away: float, odd_away: float, home: str, away: str) -> str:
        """Gera explicação textual da recomendação"""

        factors = []

        # Fator 1: xG
        if xg_away < 0.8:
            factors.append(f"{away} com xG baixo ({xg_away:.2f})")
        elif xg_away > 1.5:
            factors.append(f"{away} com xG elevado ({xg_away:.2f})")

        # Fator 2: Odd
        if odd_away > 4.0:
            factors.append(f"Odd desfavorável ao visitante ({odd_away:.2f})")
        elif odd_away < 2.5:
            factors.append(f"Odd favorável ao visitante ({odd_away:.2f})")

        # Fator 3: Recomendação geral
        if score >= 90:
            factors.append("Visitante com baixas chances de marcar")
        elif score < 70:
            factors.append("Risco elevado de gol do visitante")

        return " | ".join(factors) if factors else "Análise neutral"

    def analyze_daily_games(self, date: Optional[str] = None) -> pd.DataFrame:
        """
        Analisa todos os jogos de um dia específico da pasta data_day
        Se date=None, retorna todos os jogos
        """
        data_day_dir = Path(__file__).parent / "data_day"

        if not data_day_dir.exists():
            return pd.DataFrame()

        # Carrega arquivos CSV do dia especificado ou todos
        results = []

        for csv_file in data_day_dir.glob("*.csv"):
            try:
                df = pd.read_csv(csv_file, sep=";")

                # Filtra por data se especificada
                if date and "Date" in df.columns:
                    df = df[df["Date"] == date]

                if len(df) == 0:
                    continue

                # Analisa cada jogo
                for idx, row in df.iterrows():
                    try:
                        score = self.evaluate_score(home=row["Home"], away=row["Away"], odd_away=row.get("Odd_A_Back", 2.0), odd_0x1_lay=row.get("Odd_CS_0x1_Lay", 11.0))
                        score["source_file"] = csv_file.name
                        results.append(score)
                    except Exception as e:
                        print(f"Erro ao analisar {row.get('Home')} vs {row.get('Away')}: {e}")
                        continue
            except Exception as e:
                print(f"Erro ao carregar {csv_file}: {e}")
                continue

        return pd.DataFrame(results)

    def get_historical_stats(self) -> Dict:
        """Retorna estatísticas históricas da estratégia nos dados consolidados"""
        if self.consolidated_data is None:
            return {}

        df = self.consolidated_data

        # Por faixa de odd
        by_odd_range: Dict[str, Dict] = {}
        for min_odd, max_odd in [(0, 2.5), (2.5, 3.5), (3.5, 5.0), (5.0, 10.0)]:
            subset = df[(df["Odd_A_Back"] >= min_odd) & (df["Odd_A_Back"] < max_odd)]
            if len(subset) > 0:
                by_odd_range[f"{min_odd:.1f}-{max_odd:.1f}"] = {
                    "count": len(subset),
                    "winrate": float(subset["Lay_0x1_Outcome"].mean()) * 100,
                    "profit": float(subset["Profit_Lay_0x1"].sum()),
                }

        # Calcula estatísticas por faixa de odd
        stats = {
            "total_games": len(df),
            "lay_0x1_wins": int(df["Lay_0x1_Outcome"].sum()),
            "lay_0x1_winrate": float(df["Lay_0x1_Outcome"].mean()) * 100,
            "total_profit": float(df["Profit_Lay_0x1"].sum()),
            "avg_profit": float(df["Profit_Lay_0x1"].mean()),
            "by_odd_range": by_odd_range,
        }

        return stats


if __name__ == "__main__":
    # Teste
    strategy = Lay0x1StrategyV4()

    # Testa scoring em um jogo
    result = strategy.evaluate_score(home="Osasuna", away="Real Madrid", odd_away=1.58, odd_0x1_lay=8.6)

    print("\n=== TESTE DE AVALIAÇÃO ===")
    for key, value in result.items():
        print(f"{key}: {value}")

    # Estatísticas históricas
    print("\n=== ESTATÍSTICAS HISTÓRICAS ===")
    stats = strategy.get_historical_stats()
    for key, value in stats.items():
        if key != "by_odd_range":
            print(f"{key}: {value}")
        else:
            print("\nPor faixa de odd:")
            for odd_range, data in value.items():
                print(f"  {odd_range}: {data['count']} jogos, {data['winrate']:.1f}% win rate, {data['profit']:.2f} profit")
