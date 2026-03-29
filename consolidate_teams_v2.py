"""
Consolidador inteligente de dados Betfair + FootyStats
Mapeia nomes de times e faz merge por Date + Home/Away
"""

from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd


def similarity_ratio(a, b):
    """Calcula similaridade entre strings (0 a 1)"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def load_data():
    """Carrega dados das duas fontes"""
    data_dir = Path(__file__).parent / "data_total"

    # Betfair não tem data, então vamos extrair dos nomes dos jogos
    betfair = pd.read_csv(data_dir / "dados_betfair_atualizado.csv", delimiter=";")
    footystats = pd.read_csv(data_dir / "dados_footystats.csv", delimiter=";")

    print(f"Betfair: {betfair.shape}")
    print(f"FootyStats: {footystats.shape}")

    return betfair, footystats


def build_team_mapping():
    """
    Cria mapeamento manual de times entre FootyStats e Betfair
    FootyStats => Betfair
    """
    mapping = {
        # Times brasileiros comuns
        "Botafogo": "Botafogo RJ",
        "Botafogo FR": "Botafogo RJ",
        "Atletico Mineiro": "Atlético Mineiro",
        "CA Mineiro": "Atlético Mineiro",
        "Atlético Mineiro": "Atlético Mineiro",
        "CR Flamengo": "Flamengo",
        "Flamengo": "Flamengo",
        "SC Internacional": "Internacional",
        "Internacional": "Internacional",
        "São Paulo": "São Paulo",
        "Sao Paulo": "São Paulo",
        "Sao Paulo FC": "São Paulo",
        "Corinthians": "Corinthians",
        "Corinthians SP": "Corinthians",
        "Santos": "Santos",
        "Santos FC": "Santos",
        "Palmeiras": "Palmeiras",
        "Palmeiras SP": "Palmeiras",
        "Gremio": "Grêmio",
        "Gremio FBPA": "Grêmio",
        "Grêmio": "Grêmio",
        "Cruzeiro": "Cruzeiro",
        "Cruzeiro EC": "Cruzeiro",
        "Cebolinha": "Cebolinha",
        "Vasco": "Vasco",
        "Vasco da Gama": "Vasco",
        "CR Vasco da Gama": "Vasco",
        "Bahia": "Bahia",
        "Bahia EC": "Bahia",
        "Paysandu": "Paysandu",
        "Paysandu PA": "Paysandu",
        "Goias": "Goiás",
        "Goias EC": "Goiás",
        "Atlético Goianiense": "Atlético Goianiense",
        "Atletico Goianiense": "Atlético Goianiense",
        "Atletico GO": "Atlético Goianiense",
        "Vitoria": "Vitória",
        "Vitoria BA": "Vitória",
        "EC Vitoria": "Vitória",
        "Fortaleza": "Fortaleza",
        "Fortaleza CE": "Fortaleza",
        "RB Bragantino": "Red Bull Bragantino",
        "Red Bull Bragantino": "Red Bull Bragantino",
        "Bragantino": "Red Bull Bragantino",
        "Chapecoense": "Chapecoense",
        "Chapecoense AF": "Chapecoense",
        "Avai": "Avaí",
        "Avai FC": "Avaí",
        "Avaí FC": "Avaí",
        "Coritiba": "Coritiba",
        "Coritiba PR": "Coritiba",
        "Parana": "Paraná",
        "Parana Clube": "Paraná",
        "Paranense": "Paranense",
        "Paranense PR": "Paranense",
        "Ponte Preta": "Ponte Preta",
        "Ponte Preta SP": "Ponte Preta",
        "Guarani": "Guarani",
        "Guarani SP": "Guarani",
        "Atletico Paranaense": "Athletico Paranaense",
        "Atletico PR": "Athletico Paranaense",
        "Athletico Paranaense": "Athletico Paranaense",
        "Athletico PR": "Athletico Paranaense",
        "Atletico-PR": "Athletico Paranaense",
        "Santa Cruz": "Santa Cruz",
        "Santa Cruz PE": "Santa Cruz",
        "Sport": "Sport",
        "Sport PE": "Sport",
        "Sport Recife": "Sport",
        "Nautico": "Náutico",
        "Nautico PE": "Náutico",
        "Náutico PE": "Náutico",
        "Ceara": "Ceará",
        "Ceara SC": "Ceará",
        "Ceará SC": "Ceará",
        "Mariliense": "Mariliense",
        "Marilia": "Mariliense",
        "Ituano": "Ituano",
        "Ituano FC": "Ituano",
        "Vasco da Gama": "Vasco",
        "Consadole": "Consadole",
        "Sagan Tosu": "Sagan Tosu",
        "Kashiwa Reysol": "Kashiwa Reysol",
        "Nagoya Grampus": "Nagoya Grampus",
        "Jeonbuk Hyundai Motors": "Jeonbuk Hyundai Motors",
        "Ulsan Hyundai": "Ulsan Hyundai",
        "Al Shabab": "Al Shabab",
        "Al Hilal": "Al Hilal",
        "Al Nassr": "Al Nassr",
        "Al Ahli": "Al Ahli",
    }
    return mapping


def find_team_match(footystats_team, betfair_teams, mapping, threshold=0.75):
    """
    Encontra o time do Betfair correspondente ao FootyStats
    Usa mapping manual primeiro, depois similaridade
    """
    # Tenta mapping direto
    if footystats_team in mapping:
        return mapping[footystats_team]

    # Tenta similaridade com cada time do Betfair
    best_match = None
    best_ratio = threshold

    for betfair_team in betfair_teams:
        ratio = similarity_ratio(footystats_team, betfair_team)
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = betfair_team

    return best_match


def extract_date_from_betfair(home, away, footystats_df):
    """
    Tenta encontrar a data de um jogo Betfair nos dados FootyStats
    Procura por Home/Away match
    """
    matches = footystats_df[((footystats_df["Home"] == home) & (footystats_df["Away"] == away))]

    if len(matches) > 0:
        # Retorna a data mais recente se houver múltiplos matches
        return matches.iloc[-1]["Date"]

    return None


def consolidate_data():
    """
    Principal: consolida Betfair + FootyStats
    """
    betfair, footystats = load_data()

    print("\n=== INICIANDO CONSOLIDAÇÃO ===")

    # Cria mapping de times
    team_mapping = build_team_mapping()
    betfair_teams = set(betfair["Home"].unique()) | set(betfair["Away"].unique())

    print(f"\nTimes Betfair únicos: {len(betfair_teams)}")
    print(f"Amostra: {sorted(list(betfair_teams))[:15]}")

    # Cria nova coluna de Home/Away mapeados no FootyStats
    footystats_copy = footystats.copy()
    footystats_copy["Home_Mapped"] = footystats_copy["Home"].map(lambda x: find_team_match(x, betfair_teams, team_mapping))
    footystats_copy["Away_Mapped"] = footystats_copy["Away"].map(lambda x: find_team_match(x, betfair_teams, team_mapping))

    # Remove jogos que não foram mapeados
    footystats_mapped = footystats_copy[(footystats_copy["Home_Mapped"].notna()) & (footystats_copy["Away_Mapped"].notna())].copy()

    print(f"\nFootyStats games mapeados: {len(footystats_mapped)} / {len(footystats)}")
    print(f"Taxa de mapeamento: {100 * len(footystats_mapped) / len(footystats):.1f}%")

    # Agora faz merge entre Betfair e FootyStats mapeado
    consolidated_records = []
    matched_count = 0

    for idx, betfair_row in betfair.iterrows():
        home_betfair = betfair_row["Home"]
        away_betfair = betfair_row["Away"]

        # Procura correspondências no FootyStats mapeado
        footystats_match = footystats_mapped[(footystats_mapped["Home_Mapped"] == home_betfair) & (footystats_mapped["Away_Mapped"] == away_betfair)]

        if len(footystats_match) > 0:
            # Usa o match mais recente
            fs_row = footystats_match.iloc[-1]

            # Combina dados de ambas as fontes
            record = {
                "Date": fs_row["Date"],
                "Home": home_betfair,
                "Away": away_betfair,
                "League": fs_row["League"],
                "Season": fs_row["Season"],
                # Dados de gols
                "Goals_H_FT": fs_row["Goals_H_FT"],
                "Goals_A_FT": fs_row["Goals_A_FT"],
                "Goals_H_HT": fs_row["Goals_H_HT"],
                "Goals_A_HT": fs_row["Goals_A_HT"],
                # xG
                "xG_H": fs_row["xG_H"],
                "xG_A": fs_row["xG_A"],
                "xG_H_Pre": fs_row["xG_H_Pre"],
                "xG_A_Pre": fs_row["xG_A_Pre"],
                # Odds Betfair
                "Odd_H_Back": betfair_row["Odd_H_Back"],
                "Odd_A_Back": betfair_row["Odd_A_Back"],
                "Odd_D_Back": betfair_row["Odd_D_Back"],
                "Odd_CS_0x1_Lay": betfair_row["Odd_CS_0x1_Lay"],
                # Possessão e Ataques
                "Possession_H": fs_row["Possession_H"],
                "Possession_A": fs_row["Possession_A"],
                "Attacks_H": fs_row["Attacks_H"],
                "Attacks_A": fs_row["Attacks_A"],
                "DangerousAttacks_H": fs_row["DangerousAttacks_H"],
                "DangerousAttacks_A": fs_row["DangerousAttacks_A"],
                # Chutes
                "Shots_H": fs_row["Shots_H"],
                "Shots_A": fs_row["Shots_A"],
                "ShotsOnTarget_H": fs_row["ShotsOnTarget_H"],
                "ShotsOnTarget_A": fs_row["ShotsOnTarget_A"],
                # Estatísticas adicionais
                "Fouls_H": fs_row["Fouls_H"],
                "Fouls_A": fs_row["Fouls_A"],
                "Yellow_Cards_H": fs_row["Yellow_Cards_H"],
                "Yellow_Cards_A": fs_row["Yellow_Cards_A"],
                "Red_Cards_H": fs_row["Red_Cards_H"],
                "Red_Cards_A": fs_row["Red_Cards_A"],
                "Offsides_H": fs_row["Offsides_H"],
                "Offsides_A": fs_row["Offsides_A"],
                # Cantos
                "Corners_H": fs_row["Corners_H"] if "Corners_H" in fs_row.index else 0,
                "Corners_A": fs_row["Corners_A"] if "Corners_A" in fs_row.index else 0,
                # Dados de histórico
                "PPG_H_Pre": fs_row["PPG_H_Pre"],
                "PPG_A_Pre": fs_row["PPG_A_Pre"],
                "PPG_H_Geral_Pre": fs_row["PPG_H_Geral_Pre"],
                "PPG_A_Geral_Pre": fs_row["PPG_A_Geral_Pre"],
                # Resultado Lay 0x1
                "Lay_0x1_Outcome": 1 if fs_row["Goals_A_FT"] == 0 else 0,
                "Profit_Lay_0x1": betfair_row["Profit_Lay_0x1"] if "Profit_Lay_0x1" in betfair_row.index else 0.96,
            }

            consolidated_records.append(record)
            matched_count += 1

    # Cria DataFrame consolidado
    consolidated = pd.DataFrame(consolidated_records)

    print("\n=== RESULTADO ===")
    print(f"Registros consolidados: {len(consolidated)}")
    print(f"Taxa de consolidação: {100 * len(consolidated) / len(betfair):.1f}%")

    # Salva arquivo consolidado
    output_path = Path(__file__).parent / "data_total" / "dados_consolidado_v2.csv"
    consolidated.to_csv(output_path, sep=";", index=False)
    print(f"\nArquivo salvo: {output_path}")

    # Mostra estatísticas
    print(f"\nData range: {consolidated['Date'].min()} a {consolidated['Date'].max()}")
    print(f"Ligas: {consolidated['League'].unique()}")
    print("\nPrimeiras 5 linhas:")
    print(consolidated[["Date", "Home", "Away", "Goals_H_FT", "Goals_A_FT", "xG_H", "xG_A", "Odd_A_Back"]].head())

    return consolidated


if __name__ == "__main__":
    consolidated = consolidate_data()
