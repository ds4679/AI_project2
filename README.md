# AI Translator with OCR & Voice Input

This project leverages the power of Google Translate, Optical Character Recognition (OCR), and speech recognition to create an AI-driven translation tool with both text and voice input. The app is built using Python and Streamlit, and supports translation of text, images (via OCR), and voice input in real-time. The translations are also spoken aloud using text-to-speech.

## Features

- **Text Translation**: Translate text from any language to any other supported language using Google Translate API.
- **OCR**: Extract text from uploaded images using Optical Character Recognition (OCR) with Tesseract.
- **Voice Input**: Capture voice input and translate it to a selected target language.
- **Speech Output**: Convert translated text into speech using Google Text-to-Speech (gTTS) or pyttsx3.
- **Language Detection**: Automatically detect the language of the input text.
- **Translation History**: Keep a history of translated text and display them when requested.
- **User Ratings**: Allow users to rate the translation quality.

## Requirements

- Python 3.7+
- Streamlit
- Googletrans
- gTTS
- Pyttsx3
- pytesseract
- Pillow
- SpeechRecognition

