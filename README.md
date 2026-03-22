# CV Analyzer

CV'nizi yükleyin, iş ilanını yapıştırın — ne kadar uyumlu olduğunuzu öğrenin.

## Özellikler

- PDF formatında CV yükleme (Türkçe / İngilizce)
- İş ilanı metni ile karşılaştırma
- Uyumluluk skoru (0-100)
- Güçlü yönler, eksikler ve öneriler

## Teknolojiler

- Python
- Streamlit
- OpenAI API (GPT-4o-mini)
- PyPDF2

## Kurulum

```bash
git clone https://github.com/berilctl/cv-analyzer.git
cd cv-analyzer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Kullanım

`.env` dosyası oluşturup OpenAI API key'inizi ekleyin:

```
OPENAI_API_KEY=sk-...
```

Uygulamayı başlatın:

```bash
streamlit run app.py
```
