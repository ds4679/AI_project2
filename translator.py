import streamlit as st
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os
import time
from PIL import Image
import pytesseract
import speech_recognition as sr
import pyttsx3
import tempfile
import threading

# Explicitly set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function for translation using Google Translate API with error handling
def google_translate(text, src_lang, tgt_lang):
    translator = Translator()
    try:
        translation = translator.translate(text, src=src_lang, dest=tgt_lang)
        return translation.text, translation.dest
    except Exception as e:
        st.error(f"Error during translation: {e}")
        return None, None

# Function for speech output using Google Text-to-Speech
def speak_text_gtts(text, lang_code):
    tts = gTTS(text=text, lang=lang_code, slow=False)
    tts.save("output.mp3")
    
    # Play the audio using Streamlit's st.audio()
    with open("output.mp3", "rb") as audio_file:
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")
    
    # Add a small delay to allow the file to finish playing before deletion
    time.sleep(1)
    
    # Remove the audio file after playback
    try:
        os.remove("output.mp3")
    except PermissionError as e:
        st.error(f"Error removing file: {e}")
        # Optionally, you can log the issue or retry the deletion later.

# Function for image to text conversion using pytesseract
def ocr_from_image(image):
    img = Image.open(image)
    text = pytesseract.image_to_string(img)
    return text

# Function to capture voice input from the user and convert it to text
def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak now!")
        try:
            audio = recognizer.listen(source, timeout=5)
            st.success("Audio captured successfully!")
            text = recognizer.recognize_google(audio)
            st.write(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand that.")
            return ""
        except sr.RequestError as e:
            st.error(f"Error with the speech recognition service: {e}")
            return ""

# Function to translate text to a target language
def translate_text(text, target_language='es'):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=target_language)
        st.write(f"Translated Text: {translation.text}")
        return translation.text
    except Exception as e:
        st.error(f"Error in translation: {e}")
        return ""

# Function to convert translated text to speech and save it to a file
def text_to_speech(text):
    def synthesize_speech():
        engine = pyttsx3.init()
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        try:
            engine.save_to_file(text, temp_file.name)
            engine.runAndWait()
            st.success("Speech synthesis completed!")
            st.audio(temp_file.name, format="audio/mp3")
            os.remove(temp_file.name)  # Clean up the temporary file
        except Exception as e:
            st.error(f"Error in speech synthesis: {e}")
    
    # Run the speech synthesis in a separate thread to avoid blocking the Streamlit UI
    thread = threading.Thread(target=synthesize_speech)
    thread.start()

# Streamlit Web Interface
st.title("✨ GEN-AI HACKATHON ✨")
st.title("🌍 AI Translator with OCR & Voice Input 🤖")
st.sidebar.header("🔧 Translation Settings")

# Language selection with all languages supported by Google Translate
lang_codes = list(LANGUAGES.keys())
lang_names = [LANGUAGES[code].capitalize() for code in lang_codes]

# Dropdown for selecting source and target languages
src_lang = st.sidebar.selectbox("🌏 Select Source Language", lang_names)
tgt_lang = st.sidebar.selectbox("🌐 Select Target Language", lang_names)

# Map selected language names to language codes
src_lang_code = lang_codes[lang_names.index(src_lang)]
tgt_lang_code = lang_codes[lang_names.index(tgt_lang)]

# Swap Languages functionality
if st.button("🔄 Swap Languages"):
    src_lang, tgt_lang = tgt_lang, src_lang
    src_lang_code = lang_codes[lang_names.index(src_lang)]
    tgt_lang_code = lang_codes[lang_names.index(tgt_lang)]

# User input text area for text translation
user_input = st.text_area("✍ Enter Text to Translate", height=200)

# Image upload for OCR
image_file = st.file_uploader("📸 Upload Image for OCR", type=["jpg", "jpeg", "png"])

# Detect language of input (for translation)
def detect_language(text):
    translator = Translator()
    lang = translator.detect(text)
    return lang.lang

# Text translation handling (only if user_input is provided)
if user_input:
    detected_lang = detect_language(user_input)
    st.write(f"Detected Language: {LANGUAGES[detected_lang].capitalize()}")

    # Real-time translation
    with st.spinner('Translating...'):
        time.sleep(1)  # Simulate translation time
        translated_text, translated_lang_code = google_translate(user_input, detected_lang, tgt_lang_code)
    
    if translated_text:
        st.text_area("📜 Translated Text", translated_text, height=200, key="translated", disabled=True)

        # Speak the translated text using gTTS
        speak_text_gtts(translated_text, translated_lang_code)

# OCR functionality (image-based processing)
if image_file:
    ocr_text = ocr_from_image(image_file)
    st.write("📝 Extracted Text from Image:")
    st.text_area("OCR Output", ocr_text, height=200, disabled=True)

    if ocr_text:
        st.write("No language detection is performed for OCR text.")

        # Translate OCR text
        with st.spinner('Translating OCR text...'):
            time.sleep(1)  # Simulate translation time
            ocr_translated_text, ocr_translated_lang_code = google_translate(ocr_text, "en", tgt_lang_code)

        if ocr_translated_text:
            st.write("🌟 Translated OCR Text:")
            st.text_area("OCR Translated Text", ocr_translated_text, height=200, disabled=True)

            # Speak the translated OCR text using gTTS
            speak_text_gtts(ocr_translated_text, ocr_translated_lang_code)
        else:
            st.error("Translation failed due to an unsupported source language.")

# Voice input translation feature
st.subheader("🎤 Voice Input Translator")
if st.button("🎙 Start Voice Recording"):
    st.write("🔴 Recording... Please speak.")
    input_text = record_audio()
    if input_text:
        # Show the recognized text
        st.write(f"Recognized Text: {input_text}")
        
        # Translate the recognized text
        translated_text = translate_text(input_text, tgt_lang_code)
        
        if translated_text:
            # Show the translated text
            st.write(f"🌍 Translated Text: {translated_text}")
            
            # Trigger speech synthesis for the translated text
            text_to_speech(translated_text)  # This will speak out the translated text

            # Optionally, you can show the translated text along with audio playback
            speak_text_gtts(translated_text, tgt_lang_code)  # Play audio as well

# Translation history (optional)
if "history" not in st.session_state:
    st.session_state.history = []

if user_input:
    st.session_state.history.append({"src": user_input, "tgt": translated_text})

# Display translation history
if st.button("🕒 Show Translation History"):
    for entry in st.session_state.history:
        st.write(f"📝 Original: {entry['src']} | Translated: {entry['tgt']}")

# Feedback System
rating = st.slider("⭐ Rate the Translation Quality", 1, 5, 3)
if rating:
    st.write(f"User Rating: {rating}/5")

# Custom UI Styling
st.markdown(
    """
    <style>
    body {
        font-family: 'Roboto', sans-serif;
        color: #333;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        padding: 12px 30px;
        font-size: 18px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextArea>div {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        background-color: #f9f9f9;
    }
    </style>
    """, unsafe_allow_html=True
)