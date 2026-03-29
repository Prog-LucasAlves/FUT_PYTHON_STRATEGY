import ast
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Lay 0x1 Strategy Dashboard", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv("data_total/dados_betfair_atualizado.csv", sep=";")
    return df


@st.cache_data
def load_analysis():
    try:
        odds_analysis = pd.read_csv("data_total/analise_faixas_odds.csv", index_col=0)
        xg_analysis = pd.read_csv("data_total/analise_faixas_xg.csv", index_col=0)
        eff_analysis = pd.read_csv("data_total/analise_faixas_efficiency.csv", index_col=0)
        combinada = pd.read_csv("data_total/analise_combinada.csv", index_col=[0, 1])
        return odds_analysis, xg_analysis, eff_analysis, combinada
    except:
        return None, None, None, None


def parse_goals_minutes(min_goals_str):
    if isinstance(min_goals_str, str) and min_goals_str.strip() != "[]":
        try:
            return ast.literal_eval(min_goals_str)
        except:
            return []
    return []


# Carregar dados
df = load_data()
odds_analysis, xg_analysis, eff_analysis, combinada = load_analysis()

# ===== HEADER =====
st.title("⚽ Lay 0x1 Strategy Dashboard")
st.markdown("**Estratégia de apostas contra o resultado 0x1 (visitante vitória por 1 gol)**")

# ===== KPIs PRINCIPAIS =====
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_jogos = len(df)
    st.metric("Total de Jogos", total_jogos)

with col2:
    win_rate = (df["Lay_0x1_Result"] == "WIN").sum() / len(df) * 100
    st.metric("Win Rate", f"{win_rate:.1f}%", delta="Target: 70%+")

with col3:
    lucro_total = df["Lay_0x1_Profit"].sum()
    st.metric("Lucro Total", f"{lucro_total:.2f}", delta=f"ROI: {lucro_total / len(df):.2f}")

with col4:
    lucratividade = (df["Lay_0x1_Profit"] > 0).sum() / len(df) * 100
    st.metric("Jogos Lucrativos", f"{lucratividade:.1f}%")

with col5:
    avg_odd_away = df["Odd_A_Back"].mean()
    st.metric("Odd Média (Away)", f"{avg_odd_away:.2f}")

st.divider()

# ===== TABS =====
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Dashboard Principal", "📈 Análise por Faixas", "🎯 Estratégia Recomendada", "💰 Detalhes de Jogos", "🔍 Análise Avançada", "🎮 Validador - Jogos do Dia"])

# ===== TAB 1: DASHBOARD PRINCIPAL =====
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribuição de Win Rate por Odds")
        odds_winrate = df.groupby("Odds_Away_Range").agg({"Lay_0x1_Result": lambda x: (x == "WIN").sum() / len(x) * 100}).sort_values("Lay_0x1_Result", ascending=False)

        fig_odds = px.bar(odds_winrate.reset_index(), x="Odds_Away_Range", y="Lay_0x1_Result", color="Lay_0x1_Result", title="Win Rate por Faixa de Odds", labels={"Lay_0x1_Result": "Win Rate (%)", "Odds_Away_Range": "Faixa de Odds"}, color_continuous_scale="RdYlGn")
        fig_odds.update_yaxes(title_text="Win Rate (%)")
        st.plotly_chart(fig_odds, use_container_width=True)

    with col2:
        st.subheader("Distribuição de Lucro por Odds")
        lucro_odds = df.groupby("Odds_Away_Range").agg({"Lay_0x1_Profit": "sum"}).sort_values("Lay_0x1_Profit", ascending=False)

        fig_lucro = px.bar(lucro_odds.reset_index(), x="Odds_Away_Range", y="Lay_0x1_Profit", title="Lucro Total por Faixa de Odds", labels={"Lay_0x1_Profit": "Lucro", "Odds_Away_Range": "Faixa de Odds"}, color="Lay_0x1_Profit", color_continuous_scale="Greens")
        st.plotly_chart(fig_lucro, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Distribuição de xG do Visitante")
        fig_xg = go.Figure(data=[go.Histogram(x=df["xG_Away"], nbinsx=30)])
        fig_xg.update_layout(title="Distribuição de xG (Visitante)", xaxis_title="xG", yaxis_title="Frequência")
        st.plotly_chart(fig_xg, use_container_width=True)

    with col4:
        st.subheader("Lucro Acumulado ao Longo do Tempo")
        df_sorted = df.sort_index()
        df_sorted["Lucro_Acumulado"] = df_sorted["Lay_0x1_Profit"].cumsum()

        fig_cumulative = go.Figure()
        fig_cumulative.add_trace(go.Scatter(y=df_sorted["Lucro_Acumulado"], mode="lines", name="Lucro Acumulado", fill="tozeroy"))
        fig_cumulative.update_layout(title="Lucro Acumulado", xaxis_title="Número do Jogo", yaxis_title="Lucro Acumulado", hovermode="x unified")
        st.plotly_chart(fig_cumulative, use_container_width=True)

# ===== TAB 2: ANÁLISE POR FAIXAS =====
with tab2:
    st.subheader("Análise por Faixa de Odds")
    st.dataframe(odds_analysis.style.format("{:.2f}"), use_container_width=True)

    st.subheader("Análise por Faixa de xG")
    st.dataframe(xg_analysis.style.format("{:.2f}"), use_container_width=True)

    st.subheader("Análise por Faixa de Eficiência")
    st.dataframe(eff_analysis.style.format("{:.2f}"), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Heatmap: Odds vs xG (Win Rate %)")
        if combinada is not None and len(combinada) > 0:
            pivot_winrate = combinada["Win_Rate_%"].unstack(fill_value=0)
            fig_heatmap = px.imshow(pivot_winrate, labels=dict(x="xG Range", y="Odds Range", color="Win Rate %"), title="Win Rate por Combinação Odds x xG", color_continuous_scale="RdYlGn", aspect="auto")
            st.plotly_chart(fig_heatmap, use_container_width=True)

    with col2:
        st.subheader("Heatmap: Odds vs xG (Lucro Médio)")
        if combinada is not None and len(combinada) > 0:
            pivot_lucro = combinada["Lucro_Medio"].unstack(fill_value=0)
            fig_heatmap_lucro = px.imshow(pivot_lucro, labels=dict(x="xG Range", y="Odds Range", color="Lucro Médio"), title="Lucro Médio por Combinação Odds x xG", color_continuous_scale="RdYlGn", aspect="auto")
            st.plotly_chart(fig_heatmap_lucro, use_container_width=True)

# ===== TAB 3: ESTRATÉGIA RECOMENDADA =====
with tab3:
    st.subheader("🎯 Critérios de Entrada da Estratégia")

    st.markdown("""
    ### Baseado em Analysis of Lay 0x1 Betting Strategy

    **Odds Altas = Maior Segurança**
    - Visitante com odds > 5.0: Win Rate 96.7% ✅
    - Visitante com odds < 2.0: Win Rate 86.5% ⚠️

    **xG Baixo = Melhor Probabilidade**
    - xG < 0.5 (Muito Baixo): Win Rate 100% ✅
    - xG 1.0-1.5 (Médio): Win Rate 100% ✅
    - xG 0.5-1.0 (Baixo): Win Rate 78.6% ⚠️

    **Eficiência Importa**
    - Sem chances de gol: Win Rate 100% ✅
    - Alta eficiência (150-200%): Win Rate 89.3% ✅
    """)

    st.divider()

    st.subheader("✅ Recomendações de Entrada")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### 🟢 ENTRADAS IDEAIS

        **Prioridade Alta:**
        - Odd (Away) > 5.0 + xG < 1.0
        - Win Rate: 96-100%
        - Lucro Médio: 0.96+

        **Ação:** APOSTAR COM CONFIANÇA
        """)

    with col2:
        st.markdown("""
        ### 🟡 ENTRADAS MODERADAS

        **Considerar:**
        - Odd (Away) 3.5-5.0 + xG < 1.5
        - Win Rate: 90-95%
        - Lucro Médio: 1.84-2.64

        **Ação:** APOSTAR COM CUIDADO
        """)

    with col3:
        st.markdown("""
        ### 🔴 EVITAR

        **Alto Risco:**
        - Odd (Away) < 2.0 + xG 0.5-1.0
        - Win Rate: 78.6%
        - Variação Alta

        **Ação:** EVITAR OU REDUZIR
        """)

    st.divider()

    st.subheader("💡 Dicas de Gerenciamento de Risco")
    st.markdown("""
    1. **Stake Management:** Use flat stake (aposta fixa) de 1.00 unidade
    2. **Bankroll:** Mantenha pelo menos 50 unidades de bankroll
    3. **Drawdown:** Máximo de -10 unidades consecutivas antes de parar
    4. **ROI Target:** 2%+ por jogo (você está tendo média de 2.02)
    5. **Volume:** Mínimo 20-30 jogos por semana para validação
    """)

# ===== TAB 4: DETALHES DE JOGOS =====
with tab4:
    st.subheader("Filtrar Jogos")

    col1, col2, col3 = st.columns(3)

    with col1:
        odds_filter = st.multiselect("Faixa de Odds do Visitante", df["Odds_Away_Range"].unique(), default=df["Odds_Away_Range"].unique())

    with col2:
        xg_filter = st.multiselect("Faixa de xG do Visitante", df["xG_Away_Range"].unique(), default=df["xG_Away_Range"].unique())

    with col3:
        result_filter = st.multiselect("Resultado", ["WIN", "LOSS"], default=["WIN", "LOSS"])

    # Aplicar filtros
    df_filtered = df[(df["Odds_Away_Range"].isin(odds_filter)) & (df["xG_Away_Range"].isin(xg_filter)) & (df["Lay_0x1_Result"].isin(result_filter))]

    st.metric("Jogos após filtro", len(df_filtered))

    # Mostrar detalhes
    display_cols = ["Home", "Away", "Odd_A_Back", "Odd_CS_0x1_Lay", "Goals_H_FT", "Goals_A_FT", "xG_Home", "xG_Away", "Efficiency_Home", "Efficiency_Away", "Lay_0x1_Result", "Profit_Lay_0x1", "Lay_0x1_Profit"]

    st.dataframe(df_filtered[display_cols].style.format("{:.2f}", subset=["Odd_A_Back", "Odd_CS_0x1_Lay"]), use_container_width=True)

    # Download
    csv = df_filtered.to_csv(index=False, sep=";")
    st.download_button(label="Baixar Jogos Filtrados", data=csv, file_name=f"jogos_lay_0x1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", mime="text/csv")

# ===== TAB 5: ANÁLISE AVANÇADA =====
with tab5:
    st.subheader("📊 Análise Estatística Avançada")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Correlações Importantes")

        # Criar coluna numérica para correlação
        df_corr = df.copy()
        df_corr["Lay_0x1_Outcome"] = (df_corr["Lay_0x1_Result"] == "WIN").astype(int)

        correlations = df_corr[["Odd_A_Back", "Odd_CS_0x1_Lay", "Goals_H_FT", "Goals_A_FT", "xG_Home", "xG_Away", "Efficiency_Away", "Luck_Index_Away", "Lay_0x1_Outcome"]].corr()["Lay_0x1_Outcome"].sort_values(ascending=False)

        fig_corr = px.bar(x=correlations.values, y=correlations.index, orientation="h", title="Correlação com Resultado do Lay 0x1", labels={"x": "Correlação", "y": ""})
        st.plotly_chart(fig_corr, use_container_width=True)

    with col2:
        st.markdown("### Estatísticas de Distribuição")

        stats_data = {
            "Métrica": ["Odd Away", "xG Away", "Efficiency Away", "Luck Index Away"],
            "Média": [df["Odd_A_Back"].mean(), df["xG_Away"].mean(), df["Efficiency_Away"].mean(), df["Luck_Index_Away"].mean()],
            "Desvio": [df["Odd_A_Back"].std(), df["xG_Away"].std(), df["Efficiency_Away"].std(), df["Luck_Index_Away"].std()],
            "Min": [df["Odd_A_Back"].min(), df["xG_Away"].min(), df["Efficiency_Away"].min(), df["Luck_Index_Away"].min()],
            "Max": [df["Odd_A_Back"].max(), df["xG_Away"].max(), df["Efficiency_Away"].max(), df["Luck_Index_Away"].max()],
        }

        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df.style.format({col: "{:.2f}" for col in stats_df.columns if col != "Métrica"}), use_container_width=True)

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### Box Plot: xG por Resultado")

        fig_box = go.Figure()
        for result in ["WIN", "LOSS"]:
            fig_box.add_trace(go.Box(y=df[df["Lay_0x1_Result"] == result]["xG_Away"], name=f"{result} (0x1)", boxmean="sd"))

        fig_box.update_layout(title="Distribuição de xG por Resultado")
        st.plotly_chart(fig_box, use_container_width=True)

    with col4:
        st.markdown("### Box Plot: Odd Away por Resultado")

        fig_box_odds = go.Figure()
        for result in ["WIN", "LOSS"]:
            fig_box_odds.add_trace(go.Box(y=df[df["Lay_0x1_Result"] == result]["Odd_A_Back"], name=f"{result} (0x1)", boxmean="sd"))

        fig_box_odds.update_layout(title="Distribuição de Odds por Resultado")
        st.plotly_chart(fig_box_odds, use_container_width=True)

# ===== TAB 6: VALIDADOR DE JOGOS DO DIA =====
with tab6:
    st.subheader("Validador Lay 0x1 - Jogos do Dia")
    st.markdown("""
    Valide seus jogos do dia contra a estratégia Lay 0x1:
    - Score 90+/110 → ENTRAR COM CONFIANÇA
    - Score 70-89 → ENTRAR COM CUIDADO
    - Score <50 → EVITAR
    """)

    # Importar validador
    import glob
    from pathlib import Path

    from validate_entry import Lay0x1Validator

    # Carregar arquivos de jogos do dia
    day_files = sorted(glob.glob("data_day/dados_day_betfair_*.csv"))

    if len(day_files) > 0:
        # Extrair datas disponíveis
        datas_disponiveis = []
        datas_info = {}
        for file in day_files:
            date_str = Path(file).stem.split("_")[-1]
            datas_disponiveis.append(date_str)
            # Contar jogos por data
            try:
                df_temp = pd.read_csv(file, sep=";")
                datas_info[date_str] = len(df_temp)
            except:
                datas_info[date_str] = 0

        # Ordenar datas
        datas_disponiveis = sorted(datas_disponiveis, reverse=True)

        # Mostrar resumo de datas disponíveis
        st.info(f"📅 **{len(datas_disponiveis)} datas disponíveis**")

        # Mostrar últimas 5 datas com resumo
        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]

        for i, data in enumerate(datas_disponiveis[:5]):
            with cols[i]:
                num_jogos = datas_info.get(data, 0)
                st.metric(data, f"{num_jogos} jogos")

        st.divider()
        st.subheader("Selecione a Data")

        # Seletor de data com calendário
        data_selecionada = st.selectbox("Escolha uma data:", datas_disponiveis, index=0, key="data_selector", help="Selecione a data dos jogos que deseja validar")

        # Carregar arquivo da data selecionada
        arquivo_selecionado = f"data_day/dados_day_betfair_{data_selecionada}.csv"

        try:
            df_day = pd.read_csv(arquivo_selecionado, sep=";")
            st.success(f"✅ {len(df_day)} jogo(s) carregado(s) para {data_selecionada}")

            # Inicializar validador
            validator = Lay0x1Validator()

            if len(df_day) > 0:
                # Seletor de jogo
                st.divider()
                st.subheader("Selecione um Jogo")

                # Criar lista de opções
                opcoes_jogos = []
                for idx, row in df_day.iterrows():
                    opcao = f"[{row['Time']}] {row['Home']} vs {row['Away']} ({row['League']})"
                    opcoes_jogos.append((idx, opcao))

                # Seletor
                jogo_selecionado = st.selectbox("Escolha um jogo:", [opt[1] for opt in opcoes_jogos], key="jogo_selector")

                # Encontrar índice do jogo selecionado
                idx_selecionado = None
                for idx, opcao in opcoes_jogos:
                    if opcao == jogo_selecionado:
                        idx_selecionado = idx
                        break

                if idx_selecionado is not None:
                    row = df_day.iloc[idx_selecionado]

                    st.divider()
                    st.subheader("Dados do Jogo")

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric("Horário", row["Time"])

                    with col2:
                        st.metric("Liga", row["League"])

                    with col3:
                        st.metric("Mandante", row["Home"])

                    with col4:
                        st.metric("Visitante", row["Away"])

                    st.divider()
                    st.subheader("Odds e Métricas")

                    # Inputs para validação
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        odd_away = st.number_input("Odd do Visitante (Away Back)", value=float(row["Odd_A_Back"]), min_value=1.0, max_value=100.0, step=0.1, key="odd_away")

                    with col2:
                        odd_cs_0x1 = st.number_input("Odd Lay 0x1 (Back)", value=float(row["Odd_CS_0x1_Back"]) if "Odd_CS_0x1_Back" in row else 15.0, min_value=1.0, max_value=999.0, step=0.5, key="odd_0x1")

                    with col3:
                        st.metric("Odd CS 0x1 Lay", f"{row['Odd_CS_0x1_Lay']:.1f}")

                    # Estimativa de xG baseada em histórico
                    col1, col2, col3 = st.columns(3)

                    # Obter estimativas do histórico
                    team_away = row["Away"]
                    xg_from_history = validator.get_team_xg_estimate(team_away)
                    eff_from_history = validator.get_team_efficiency_estimate(team_away)
                    xg_fallback = min(2.0, round(1.5 / np.sqrt(odd_away), 2))

                    # Verificar se time foi encontrado
                    team_found = team_away in validator.team_away_stats
                    found_marker = "✓ Histórico" if team_found else "⚠ Média Geral"

                    with col1:
                        st.info(f"**xG**: {xg_from_history:.2f} {found_marker}")
                        xg_away_est = st.number_input("xG do Visitante", value=round(xg_from_history, 2), min_value=0.0, max_value=5.0, step=0.1, help=f"Ajuste conforme análise. Fallback (por odds): {xg_fallback}", key="xg_away")

                    with col2:
                        st.info(f"**Eficiência**: {eff_from_history:.1f}% {found_marker}")
                        efficiency_away = st.slider("Eficiência do Visitante (%)", min_value=50, max_value=250, value=int(round(eff_from_history)), step=10, help="Percentual de conversão. Padrão: 100%", key="efficiency")

                    with col3:
                        st.metric("Matches (Away)", f"{validator.team_away_stats.get(team_away, {}).get('matches', '?')}")
                        st.metric("Btts Lay", f"{row.get('Odd_BTTS_Yes_Lay', 'N/A')}")

                    st.divider()
                    st.subheader("Validação Lay 0x1")

                    # Botão de validação
                    if st.button("🎯 Validar Entrada", use_container_width=True, type="primary"):
                        # Validar
                        result = validator.validate_match(home=row["Home"], away=row["Away"], odd_away=odd_away, xg_away=xg_away_est, efficiency_away=efficiency_away)

                        # Exibir resultado
                        st.divider()

                        # Score e recomendação
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            score_color = "green" if result["total_score"] >= 90 else "orange" if result["total_score"] >= 70 else "red"
                            st.markdown(
                                f"""
                            <div style="text-align: center; padding: 20px; background-color: {score_color}40; border-radius: 10px;">
                                <h2 style="margin: 0;">{result["total_score"]}/110</h2>
                                <p style="margin: 5px 0; font-weight: bold;">SCORE FINAL</p>
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )

                        with col2:
                            rec_color = "green" if result["total_score"] >= 90 else "orange" if result["total_score"] >= 70 else "red"
                            st.markdown(
                                f"""
                            <div style="text-align: center; padding: 20px; background-color: {rec_color}40; border-radius: 10px;">
                                <p style="margin: 0; font-size: 14px;">RECOMENDACAO</p>
                                <p style="margin: 5px 0; font-weight: bold;">{result["recommendation"]}</p>
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )

                        with col3:
                            if result["historical"]["similar_matches"] > 0:
                                wr = result["historical"]["win_rate"]
                                st.markdown(
                                    f"""
                                <div style="text-align: center; padding: 20px; background-color: #00800040; border-radius: 10px;">
                                    <p style="margin: 0; font-size: 14px;">WIN RATE SIMILAR</p>
                                    <p style="margin: 5px 0; font-weight: bold;">{wr:.1f}%</p>
                                    <p style="margin: 5px 0; font-size: 12px;">({int(result["historical"]["similar_matches"])} jogos)</p>
                                </div>
                                """,
                                    unsafe_allow_html=True,
                                )

                        st.divider()

                        # Critérios de análise
                        st.subheader("Análise por Critério")

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.markdown(f"""
                            **Odds do Visitante**
                            - Valor: {result["analysis"]["odds"]["value"]:.2f}
                            - Categoria: {result["analysis"]["odds"]["categoria"]}
                            - Score: {result["analysis"]["odds"]["score"]}/40
                            """)

                        with col2:
                            st.markdown(f"""
                            **xG do Visitante**
                            - Valor: {result["analysis"]["xg"]["value"]:.2f}
                            - Categoria: {result["analysis"]["xg"]["categoria"]}
                            - Score: {result["analysis"]["xg"]["score"]}/40
                            """)

                        with col3:
                            st.markdown(f"""
                            **Eficiência**
                            - Valor: {result["analysis"]["efficiency"]["value"]:.1f}%
                            - Categoria: {result["analysis"]["efficiency"]["categoria"]}
                            - Score: {result["analysis"]["efficiency"]["score"]}/30
                            """)

                        st.divider()

                        # Resumo da decisão
                        st.subheader("Resumo da Decisão")

                        if result["total_score"] >= 90:
                            st.success("""
                            ✅ **ENTRAR COM CONFIANÇA**

                            Este jogo atende todos os critérios ideais para Lay 0x1.
                            - Win rate esperado: 96-100%
                            - Lucro esperado: 1.80-2.07 por jogo
                            - Risco: Baixo
                            """)
                        elif result["total_score"] >= 70:
                            st.warning("""
                            🟡 **ENTRAR COM CUIDADO**

                            Este jogo é uma boa oportunidade mas com cuidado.
                            - Win rate esperado: 90-95%
                            - Lucro esperado: 1.84-2.64 por jogo
                            - Risco: Moderado
                            """)
                        elif result["total_score"] >= 50:
                            st.info("""
                            ⚠️ **CONSIDERAR COM CAUTELA**

                            Este jogo pode ser interessante mas requer análise adicional.
                            - Win rate esperado: 80-90%
                            - Stake recomendado: 1% do bankroll
                            """)
                        else:
                            st.error("""
                            🔴 **EVITAR**

                            Este jogo não atende aos critérios mínimos de entrada.
                            - Win rate baixo
                            - Risco elevado
                            - Melhor esperar por melhores oportunidades
                            """)

                        st.divider()

                        # Dicas
                        st.subheader("Dicas para Este Jogo")

                        st.info(
                            """
                        **Informações Úteis:**
                        - Odds Lay 0x1: """
                            + f"{odd_cs_0x1:.1f}"
                            + """
                        - Stake recomendado: 1-2% do bankroll
                        - Lucro em caso de WIN: aproximadamente """
                            + f"{100 * (odd_cs_0x1 - 1) / odd_cs_0x1:.1f}%"
                            + """ da aposta
                        """,
                        )

        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")
    else:
        st.warning("Nenhum arquivo de jogos do dia encontrado em data_day/")
        st.info("Coloque arquivos .csv em data_day/ com padrão: dados_day_betfair_YYYY-MM-DD.csv")

st.divider()
st.markdown(
    """
---
**Lay 0x1 Strategy Dashboard** | Atualizado em: {} | Version 1.0
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
)
