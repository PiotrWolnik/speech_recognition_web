import streamlit as st
from languages import supported_languages
from abc import ABC, abstractmethod
from deep_translator import GoogleTranslator
import speech_recognition as sr
import cython
import whisper

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
    def __init__(self) -> None:
        pass

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

from audiorecorder import audiorecorder

st.title("Audio Recorder")
audio = audiorecorder("Click to record", "Click to stop recording")

if len(audio) > 0:
    # To play audio in frontend:
    st.audio(audio.export().read())  

    # To save audio to a file, use pydub export method:
    audio.export("audio.wav", format="wav")

if center_column.button("Translate"):
    model = whisper.load_model("base")
    # audio = torch.from_numpy(wav_audio_data)
    transcription = model.transcribe('audio.wav')
    st.markdown("Captured text:\n"+transcription["text"])
    st.markdown("\n\nTranslated text:\n"+TranslateWords(transcription["text"], supported_languages[destination_language]).getResult())