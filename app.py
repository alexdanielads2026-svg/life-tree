import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as fgo
from datetime import datetime

# Configuração da página para modo QueryOtimizado para TV de 43
st.set_page_config(
    page_title="TI Árvore Líquida - LIFE TREE",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Estilização CSS para visualização em modo quiosque (Full Screen)
st.markdown(
    """
    <style>
        @import url('https://googleapis.com');
        .main { background-color: #0e1117; color: #ffffff; }
        .block-container { padding-top: 2rem; padding-bottom: 1rem; }
        .metric-box {
            background-color: #1f2937;
            padding: 15px;
            border-radius: 8px;
            border-left: 5px solid #10b981;
            margin-bottom: 10px;
        }
        .metric-val { font-family: 'Share Tech Mono', monospace; font-size: 24px; color: #10b981; }
        .footer-text { font-size: 12px; color: #6b7280; font-family: monospace; }
    </style>
    """,
    unsafe_allow_html=True,
)


# --- SIMULAÇÃO DE LEITURA DE DADOS (Substituir pela sua query Influx/Postgres) ---
@st.cache_data(ttl=1)
def ler_dados_sensores():
    # Simulando dados que o Node-RED inseriu no banco
    agora = datetime.now()
    co2_in = float(np.random.normal(450, 15))
    eficiencia_simulada = 0.25  # 25% de redução biológica
    co2_out = co2_in * (1 - eficiencia_simulada)

    dados_atuais = {
        "timestamp": agora,
        "co2_in": co2_in,
        "co2_out": co2_out,
        "pm1": float(np.random.normal(5, 1)),
        "pm25": float(np.random.normal(12, 2)),
        "pm10": float(np.random.normal(25, 4)),
        "no2": 0.02,
        "so2": 0.01,
        "o3": 0.03,
        "ch4": 1.8,
        "h2s": 0.002,
        "voc": 0.15,
        "o2_out": 21.2,
        "temp": 24.5,
        "umi": 62.0,
    }
    return dados_atuais


dados = ler_dados_sensores()

# --- CÁLCULOS DO PROJETO (Conforme Seção 6) ---
co2_retirado = dados["co2_in"] - dados["co2_out"]
eficiencia = (co2_retirado / dados["co2_in"]) * 100

# ==================== CABEÇALHO TÉCNICO ====================
st.title("🌲 TI ÁRVORE LÍQUIDA - LIFE TREE")
st.subheader("Sistema Biotecnológico de Monitoramento Ambiental em Tempo Real")
st.markdown("---")

# ==================== BLOCO DE DESEMPENHO CENTRAL ====================
st.markdown("### 📊 DESEMPENHO CENTRAL DA LIFE TREE")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(
        f"<div class='metric-box'><b>CO₂ Entrada</b><br><span class='metric-val'>{dados['co2_in']:.1f} ppm</span></div>",
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f"<div class='metric-box' style='border-left-color: #ef4444;'><b>CO₂ Saída</b><br><span class='metric-val'>{dados['co2_out']:.1f} ppm</span></div>",
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        f"<div class='metric-box' style='border-left-color: #3b82f6;'><b>CO₂ Retirado</b><br><span class='metric-val'>{co2_retirado:.1f} ppm</span></div>",
        unsafe_allow_html=True,
    )
with col4:
    st.markdown(
        f"<div class='metric-box' style='border-left-color: #f59e0b;'><b>Eficiência</b><br><span class='metric-val'>{eficiencia:.2f} %</span></div>",
        unsafe_allow_html=True,
    )
with col5:
    st.markdown(
        f"<div class='metric-box'><b>O₂ Saída</b><br><span class='metric-val'>{dados['o2_out']:.1f} %</span></div>",
        unsafe_allow_html=True,
    )

st.markdown("---")

# ==================== BLOCOS LATERAIS (ENTRADA vs SAÍDA) ====================
col_esquerda, col_direita = st.columns(2)

with col_esquerda:
    st.markdown("### 🌬️ Bloco Entrada – Ar Ambiente")
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        st.metric("Material Particulado PM1", f"{dados['pm1']:.1f} µg/m³")
        st.metric("Material Particulado PM2.5", f"{dados['pm25']:.1f} µg/m³")
        st.metric("Material Particulado PM10", f"{dados['pm10']:.1f} µg/m³")
        st.metric("Temperatura / Umidade", f"{dados['temp']}°C / {dados['umi']}%")
    with sub_col2:
        st.metric("Dióxido de Nitrogênio (NO₂)", f"{dados['no2']} ppm")
        st.metric("Dióxido de Enxofre (SO₂)", f"{dados['so2']} ppm")
        st.metric("Ozônio (O₃)", f"{dados['o3']} ppm")
        st.metric("Gases (CH₄ / H₂S / VOC)", f"{dados['ch4']} / {dados['voc']} ppm")

with col_direita:
    st.markdown("### 🍃 Bloco Saída – Ar Após Processo")
    # Geração do gráfico histórico em tempo real
    st.markdown("Tendência Temporal de Carbono (Últimos minutos)")

    # Simulação de histórico para o gráfico Plotly
    df_historico = pd.DataFrame(
        {
            "Tempo": pd.date_range(end=datetime.now(), periods=20, freq="min"),
            "CO2_Entrada": np.random.normal(450, 10, 20),
            "CO2_Saída": np.random.normal(337, 8, 20),
        }
    )

    fig = fgo.Figure()
    fig.add_trace(
        fgo.Scatter(
            x=df_historico["Tempo"],
            y=df_historico["CO2_Entrada"],
            name="Entrada (Ar Ambiente)",
            line=dict(color="#10b981", width=3),
        )
    )
    fig.add_trace(
        fgo.Scatter(
            x=df_historico["Tempo"],
            y=df_historico["CO2_Saída"],
            name="Saída (Tratado)",
            line=dict(color="#ef4444", width=3, dash="dash"),
        )
    )

    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=20, r=20, t=20, b=20),
        height=280,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)

# ==================== RODAPÉ TÉCNICO & STATUS (Seção 9) ====================
st.markdown("---")
rf1, rf2, rf3, rf4 = st.columns(4)
with rf1:
    st.markdown(
        "<p class='footer-text'>🖥️ <b>Mini PC:</b> Intel Core i3 | RAM 16GB</p>",
        unsafe_allow_html=True,
    )
with rf2:
    st.markdown(
        "<p class='footer-text'>🤖 <b>Controlador de Campo:</b> ESP32-S3 (W5500 Ethernet)</p>",
        unsafe_allow_html=True,
    )
with rf3:
    st.markdown(
        "<p class='footer-text'>⛓️ <b>Rede / Protocolo:</b> Modbus RS485 Local OK</p>",
        unsafe_allow_html=True,
    )
with rf4:
    st.markdown(
        "<p class='footer-text'>📸 <b>Câmera IP PoE:</b> Conectada (RTSP Stream Ativo)</p>",
        unsafe_allow_html=True,
    )