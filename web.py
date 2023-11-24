import streamlit as st
from languages import supported_languages
from abc import ABC, abstractmethod
from deep_translator import GoogleTranslator
import speech_recognition as sr
import cython

class ITranslateWords(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def getResult(self) -> str:
        pass

class TranslateWords(ITranslateWords):
    def __init__(self, text_to_translate: str, language_to_translate_to: str):
        super().__init__()
        self.text_to_translate = text_to_translate
        self.language_to_translate_to = language_to_translate_to
        self.result = GoogleTranslator(source='auto', 
                                target=self.language_to_translate_to).translate(self.text_to_translate)
    def getResult(self) -> str:
        return self.result

st.set_page_config(page_title="Speech_Translator_Option.ai", page_icon=":studio_microphone:")

main_container = st.container()
_, center_column, _ = main_container.columns([1, 5, 1])

center_column.title("Speech Translator Option")

destination_language = center_column.selectbox(
        "Select Language",
        sorted(list(supported_languages.keys())[1:]),
        key="target_lang",
        label_visibility="hidden",
)

if center_column.button("Click and say sth......"):
    r = sr.Recognizer()
    st.success("Transcribing Speech")
    with sr.Microphone() as source:
        audio_data = r.record(source, duration=5)
        print("Recognizing...")
        text = r.recognize_google(audio_data)
    st.text(f"Translated text:\n{TranslateWords(text, supported_languages[destination_language]).getResult()}")

