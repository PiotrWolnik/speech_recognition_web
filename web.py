import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

stt_button = Button(label="Speak", width=100)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))
# import streamlit as st
# from languages import supported_languages
# from abc import ABC, abstractmethod
# from deep_translator import GoogleTranslator
# import speech_recognition as sr
# import cython

# class ITranslateWords(ABC):
#     def __init__(self):
#         super().__init__()

#     @abstractmethod
#     def getResult(self) -> str:
#         pass

# class TranslateWords(ITranslateWords):
#     def __init__(self, text_to_translate: str, language_to_translate_to: str):
#         super().__init__()
#         self.text_to_translate = text_to_translate
#         self.language_to_translate_to = language_to_translate_to
#         self.result = GoogleTranslator(source='auto', 
#                                 target=self.language_to_translate_to).translate(self.text_to_translate)
#     def getResult(self) -> str:
#         return self.result

# st.set_page_config(page_title="Speech_Translator_Option.ai", page_icon=":studio_microphone:")

# main_container = st.container()
# _, center_column, _ = main_container.columns([1, 5, 1])

# center_column.title("Speech Translator Option")

# destination_language = center_column.selectbox(
#         "Select Language",
#         sorted(list(supported_languages.keys())[1:]),
#         key="target_lang",
#         label_visibility="hidden",
# )

# if center_column.button("Click and say sth......"):
#     r = sr.Recognizer()
#     st.success("Transcribing Speech")
#     with sr.Microphone() as source:
#         audio_data = r.record(source, duration=5)
#         print("Recognizing...")
#         text = r.recognize_google(audio_data)
#     st.text(f"Translated text:\n{TranslateWords(text, supported_languages[destination_language]).getResult()}")

