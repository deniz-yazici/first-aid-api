from flask import Flask, request, jsonify
import google.generativeai as genai
import os

# API anahtarını ortam değişkeninden al (önce sistem değişkenine tanımlamalısın)
genai.configure(api_key=os.getenv("AIzaSyBZ3tKkSsmW3klBZpGe4KoYoZUiMIsBMPU"))

# Gemini Pro modeli ile oluştur
model = genai.GenerativeModel("Gemini 1.5 Flash")

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    yas = request.form.get('yas')
    cinsiyet = request.form.get('cinsiyet')
    kaza = request.form.get('kaza')
    semptom = request.form.get('semptom')
    gorsel_base64 = request.form.get('gorsel_base64')

    print("➡️ Veri alındı:")
    print("Yaş:", yas)
    print("Cinsiyet:", cinsiyet)
    print("Kaza:", kaza)
    print("Semptom:", semptom)
    print("Görsel Base64 uzunluğu:", len(gorsel_base64 or ""))

    # Prompta anlamlı bir cümle kur
    prompt = f"""
    {yas} yaşında bir {cinsiyet}, '{kaza}' kazası geçirmiş ve şu semptomları gösteriyor: '{semptom}'.
    Bu durumda yapılması gereken ilk yardım adımları nelerdir? 
    Kısa ve anlaşılır bir şekilde ilk yardım önerisi sun.
    """

    try:
        response = model.generate_content(prompt)
        cevap = response.text
    except Exception as e:
        cevap = f"Hata oluştu: {str(e)}"

    return jsonify({
        "cevap": cevap,
        "animasyon": None  # Daha sonra görsel analiz yapılacaksa kullanılabilir
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
