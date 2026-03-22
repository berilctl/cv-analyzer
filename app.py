"""
CV Analyzer — Streamlit arayüzü.
CV'nizi yükleyin, iş ilanını yapıştırın, uyumluluk analizini görün.
"""

import streamlit as st
from dotenv import load_dotenv
import os

from cv_parser import extract_text_from_pdf
from analyzer import analyze_cv

# .env dosyasından API key'i yükle
load_dotenv()

# --- Sayfa ayarları ---
st.set_page_config(page_title="CV Analyzer", page_icon="📄", layout="centered")

# --- Özel CSS ile tema ---
st.markdown("""
<style>
    /* Ana arka plan: krem */
    .stApp {
        background-color: #FAF6F0;
    }

    /* Başlık ve metin renkleri: lacivert */
    h1, h2, h3, h4, .stMarkdown p, .stMarkdown li, label, .stFileUploader label, .stTextArea label {
        color: #1B2A4A !important;
    }

    /* Atatürk alıntı kutusu */
    .quote-box {
        background-color: #1B2A4A;
        color: #FAF6F0;
        padding: 20px 28px;
        border-radius: 10px;
        margin-bottom: 30px;
        text-align: center;
        font-size: 15px;
        line-height: 1.7;
        font-style: italic;
        border-left: 5px solid #C8A96E;
    }
    .quote-box .author {
        font-style: normal;
        font-weight: 600;
        margin-top: 8px;
        color: #C8A96E;
    }

    /* Buton: lacivert arka plan */
    .stButton > button {
        background-color: #1B2A4A !important;
        color: #FAF6F0 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }
    .stButton > button:hover {
        background-color: #2C3E6B !important;
    }

    /* Progress bar rengi */
    .stProgress > div > div > div {
        background-color: #1B2A4A !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background-color: #EDE8DF !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    [data-testid="stFileUploaderDropzone"] {
        background-color: #E8E2D8 !important;
        border-color: #1B2A4A !important;
        color: #1B2A4A !important;
    }
    [data-testid="stFileUploaderDropzone"] small,
    [data-testid="stFileUploaderDropzone"] span,
    [data-testid="stFileUploaderDropzone"] div {
        color: #1B2A4A !important;
    }
    [data-testid="stFileUploaderDropzone"] button {
        background-color: #1B2A4A !important;
        color: #FAF6F0 !important;
        border: none !important;
    }
    [data-testid="stFileUploaderDropzone"] svg {
        fill: #1B2A4A !important;
        stroke: #1B2A4A !important;
    }

    /* Text area */
    .stTextArea textarea {
        background-color: #EDE8DF !important;
        border-color: #1B2A4A !important;
        color: #1B2A4A !important;
        border-radius: 10px !important;
    }
    .stTextArea textarea::placeholder {
        color: #7A7062 !important;
    }
    .stTextArea label {
        color: #1B2A4A !important;
    }

    /* Sonuç kartları */
    .result-card {
        background-color: #FFFFFF;
        border: 1px solid #E0D8CC;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 16px;
    }
    .result-card h4 {
        margin-top: 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #1B2A4A;
    }

    /* Skor kutusu */
    .score-box {
        background-color: #1B2A4A;
        color: #FAF6F0;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 16px;
    }
    .score-box .score-number {
        font-size: 48px;
        font-weight: 700;
    }
    .score-box .score-label {
        font-size: 16px;
        margin-top: 4px;
    }

    /* Divider rengi */
    hr {
        border-color: #C8A96E !important;
    }

    /* Sidebar ve header gizle (daha temiz görünüm) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Atatürk Alıntısı ---
st.markdown("""
<div class="quote-box">
    "Umutsuz durumlar yoktur, umutsuz insanlar vardır.
    Ben hiçbir zaman umudumu yitirmedim."
    <div class="author">— Mustafa Kemal Atatürk</div>
</div>
""", unsafe_allow_html=True)

# --- Başlık ---
st.title("CV Analyzer")
st.markdown("CV'nizi yükleyin, iş ilanını yapıştırın — ne kadar uyumlu olduğunuzu öğrenin.")

# --- API Key ---
# Önce Streamlit secrets'dan, sonra .env'den, yoksa kullanıcıdan iste
api_key = st.secrets.get("OPENAI_API_KEY", "") if hasattr(st, "secrets") and "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY", "")
if not api_key or api_key == "buraya_kendi_api_keyinizi_yazin":
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")

# --- CV Yükleme ---
st.subheader("1. CV'nizi Yükleyin (PDF)")
uploaded_file = st.file_uploader("PDF dosyası seçin", type=["pdf"])

# --- İş İlanı ---
st.subheader("2. İş İlanını Yapıştırın")
job_description = st.text_area(
    "İş ilanı metni",
    height=200,
    placeholder="İş ilanındaki gereksinimleri buraya yapıştırın...",
)

# --- Analiz Butonu ---
if st.button("Analiz Et", use_container_width=True):
    # Validasyonlar
    if not api_key:
        st.error("Lütfen OpenAI API Key giriniz.")
    elif not uploaded_file:
        st.error("Lütfen bir CV yükleyiniz.")
    elif not job_description.strip():
        st.error("Lütfen iş ilanı metnini giriniz.")
    else:
        # PDF'den metin çıkar
        with st.spinner("CV okunuyor..."):
            cv_text = extract_text_from_pdf(uploaded_file)

        if not cv_text:
            st.error("PDF'den metin çıkarılamadı. Lütfen metin tabanlı bir PDF yükleyin.")
        else:
            # Analiz yap
            with st.spinner("CV analiz ediliyor..."):
                try:
                    result = analyze_cv(cv_text, job_description, api_key)
                except Exception as e:
                    st.error(f"Analiz sırasında hata oluştu: {e}")
                    st.stop()

            # --- Sonuçları Göster ---
            st.divider()
            st.subheader("Analiz Sonuclari")

            # Uyumluluk skoru
            score = result["score"]
            if score >= 70:
                score_label = "Yüksek Uyumluluk"
            elif score >= 40:
                score_label = "Orta Uyumluluk"
            else:
                score_label = "Düşük Uyumluluk"

            st.markdown(f"""
            <div class="score-box">
                <div class="score-number">{score}/100</div>
                <div class="score-label">{score_label}</div>
            </div>
            """, unsafe_allow_html=True)

            st.progress(score / 100)

            # Güçlü yönler ve eksikler yan yana
            col1, col2 = st.columns(2)

            with col1:
                strengths_html = "".join(f"<li>{item}</li>" for item in result["strengths"])
                st.markdown(f"""
                <div class="result-card">
                    <h4>Güçlü Yönler</h4>
                    <ul>{strengths_html}</ul>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                weaknesses_html = "".join(f"<li>{item}</li>" for item in result["weaknesses"])
                st.markdown(f"""
                <div class="result-card">
                    <h4>Eksikler</h4>
                    <ul>{weaknesses_html}</ul>
                </div>
                """, unsafe_allow_html=True)

            # Öneriler
            suggestions_html = "".join(f"<li>{item}</li>" for item in result["suggestions"])
            st.markdown(f"""
            <div class="result-card">
                <h4>Öneriler</h4>
                <ul>{suggestions_html}</ul>
                <p style="margin-top: 16px; padding-top: 12px; border-top: 1px solid #E0D8CC;
                   color: #1B2A4A; font-style: italic; text-align: center;">
                    İş arama yolculuğunda size bol şans diliyoruz! Doğru pozisyon sizi bekliyor.
                </p>
            </div>
            """, unsafe_allow_html=True)
