from flask import Flask, render_template, request, jsonify
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from googletrans import Translator

app = Flask(__name__, template_folder='templates', static_folder='static')

# Load model directly
tokenizer = AutoTokenizer.from_pretrained("EngTig/llama-2-7b-Car-maintenance")
model = AutoModelForCausalLM.from_pretrained("EngTig/llama-2-7b-Car-maintenance")

# Initialize the translator
translator = Translator()

# Define the text generation pipeline
text_generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

@app.route('/')
def index():
    return render_template('index.html')

def text2Text(text):
    print(text)

    # Translate to English
    translation_to_english = translator.translate(text, src='ar', dest='en')
    eng_text = translation_to_english.text
    print(eng_text)

    # Generate text
    generated_text = text_generator(eng_text, max_length=512, num_return_sequences=1)
    final_generated_text = generated_text[0]['generated_text']
    print(final_generated_text)

    # Translate to Arabic
    translation_to_arabic = translator.translate(final_generated_text, src='en', dest='ar')
    arab_text = translation_to_arabic.text
    return arab_text

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    input_text = data['text']
    generated_text = text2Text(input_text)
    return jsonify({'generated_text': generated_text})

if __name__ == '__main__':
    app.run(debug=True)