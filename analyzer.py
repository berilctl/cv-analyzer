"""
Analyzer modülü.
OpenAI API kullanarak CV'yi iş ilanına göre analiz eder.
"""

import json
from openai import OpenAI


def analyze_cv(cv_text: str, job_description: str, api_key: str) -> dict:
    """
    CV metnini iş ilanıyla karşılaştırıp analiz eder.

    Args:
        cv_text: PDF'den çıkarılan CV metni
        job_description: Kullanıcının girdiği iş ilanı metni
        api_key: OpenAI API anahtarı

    Returns:
        Analiz sonuçlarını içeren dict:
        {
            "score": 0-100 arası uyumluluk skoru,
            "strengths": ["güçlü yön 1", ...],
            "weaknesses": ["eksik 1", ...],
            "suggestions": ["öneri 1", ...]
        }
    """
    client = OpenAI(api_key=api_key)

    prompt = f"""Sen bir İK uzmanısın. Sana bir CV metni ve bir iş ilanı vereceğim.
CV'yi iş ilanına göre analiz et.

Yanıtını SADECE aşağıdaki JSON formatında ver, başka hiçbir şey yazma:
{{
    "score": <0-100 arası uyumluluk puanı>,
    "strengths": ["güçlü yön 1", "güçlü yön 2", ...],
    "weaknesses": ["eksik 1", "eksik 2", ...],
    "suggestions": ["öneri 1", "öneri 2", ...]
}}

Kurallar:
- score: CV'nin iş ilanına ne kadar uyduğunu 0-100 arasında puanla
- strengths: İş ilanıyla eşleşen beceriler ve deneyimler (en az 2 madde)
- weaknesses: İş ilanının isteyip CV'de olmayan beceriler/deneyimler (en az 2 madde)
- suggestions: CV'yi bu iş için güçlendirmek adına somut öneriler (en az 2 madde)
- CV ve iş ilanı hangi dilde ise o dilde yanıt ver

--- CV METNİ ---
{cv_text}

--- İŞ İLANI ---
{job_description}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    result_text = response.choices[0].message.content.strip()

    # JSON bloğunu temizle (bazen ```json ... ``` içinde gelebiliyor)
    if result_text.startswith("```"):
        result_text = result_text.split("```")[1]
        if result_text.startswith("json"):
            result_text = result_text[4:]
        result_text = result_text.strip()

    return json.loads(result_text)
