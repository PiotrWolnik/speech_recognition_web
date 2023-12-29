import streamlit as st
from languages import supported_languages
from abc import ABC, abstractmethod
from deep_translator import GoogleTranslator
import speech_recognition as sr
import whisper
from audiorecorder import audiorecorder
import numpy as np

class TranslateWords:
    def __init__(self, text_to_translate: str, language_to_translate_to: str):
        super().__init__()
        self.text_to_translate = text_to_translate
        self.language_to_translate_to = language_to_translate_to
        self.result = GoogleTranslator(source='auto', 
                                target=self.language_to_translate_to).translate(self.text_to_translate)
    def getResult(self) -> str:
        return self.result

class TranslateSpeech:
    def __init__(self, language_to_translate_to: str, audio: np.ndarray) -> None:
        self.language_to_translate_to = language_to_translate_to
        model = whisper.load_model("base")
        self.transcription = model.transcribe(audio)
    
    def translate_speech(self) -> str:
        return TranslateWords(self.transcription["text"], self.language_to_translate_to).getResult()

    def get_transcript_of_speech(self) -> str:
        return self.transcription["text"]


main_container = st.container()
_, center_column, _ = main_container.columns([1, 5, 1])

center_column.title("Speech Translator Option")

destination_language = center_column.selectbox(
        "Select Language",
        sorted(list(supported_languages.keys())[1:]),
        key="target_lang",
        label_visibility="hidden",
)

st.title("Audio Recorder")
audio = audiorecorder("Click to record", "Click to stop recording")

if len(audio) > 0:
    st.audio(audio.export().read())  
    audio.export("audio.wav", format="wav")
if center_column.button("Translate"):
    speech_translator = TranslateSpeech(supported_languages[destination_language], "audio.wav")
    st.markdown("Captured text:\n"+speech_translator.get_transcript_of_speech())
    st.markdown("\n\nTranslated text:\n"+speech_translator.translate_speech())