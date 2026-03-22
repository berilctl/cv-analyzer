"""
CV Parser modülü.
PDF dosyasından metin çıkarır.
"""

from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_file) -> str:
    """
    Yüklenen PDF dosyasından tüm sayfaların metnini çıkarır.

    Args:
        pdf_file: Streamlit'in file_uploader'ından gelen dosya objesi

    Returns:
        PDF'deki tüm metnin birleştirilmiş hali
    """
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()
