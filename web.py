import wave
from dataclasses import dataclass, asdict

import pyaudio


@dataclass
class StreamParams:
    format: int = pyaudio.paInt16
    channels: int = 2
    rate: int = 44100
    frames_per_buffer: int = 1024
    input: bool = True
    output: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


class Recorder:
    """Recorder uses the blocking I/O facility from pyaudio to record sound
    from mic.

    Attributes:
        - stream_params: StreamParams object with values for pyaudio Stream
            object
    """
    def __init__(self, stream_params: StreamParams) -> None:
        self.stream_params = stream_params
        self._pyaudio = None
        self._stream = None
        self._wav_file = None

    def record(self, duration: int, save_path: str) -> None:
        """Record sound from mic for a given amount of seconds.

        :param duration: Number of seconds we want to record for
        :param save_path: Where to store recording
        """
        print("Start recording...")
        self._create_recording_resources(save_path)
        self._write_wav_file_reading_from_stream(duration)
        self._close_recording_resources()
        print("Stop recording")

    def _create_recording_resources(self, save_path: str) -> None:
        self._pyaudio = pyaudio.PyAudio()
        self._stream = self._pyaudio.open(**self.stream_params.to_dict())
        self._create_wav_file(save_path)

    def _create_wav_file(self, save_path: str):
        self._wav_file = wave.open(save_path, "wb")
        self._wav_file.setnchannels(self.stream_params.channels)
        self._wav_file.setsampwidth(self._pyaudio.get_sample_size(self.stream_params.format))
        self._wav_file.setframerate(self.stream_params.rate)

    def _write_wav_file_reading_from_stream(self, duration: int) -> None:
        for _ in range(int(self.stream_params.rate * duration / self.stream_params.frames_per_buffer)):
            audio_data = self._stream.read(self.stream_params.frames_per_buffer)
            self._wav_file.writeframes(audio_data)

    def _close_recording_resources(self) -> None:
        self._wav_file.close()
        self._stream.close()
        self._pyaudio.terminate()

# import streamlit as st
# from bokeh.models.widgets import Button
# from bokeh.models import CustomJS

# text = st.text_input("Say what ?")

# tts_button = Button(label="Speak", width=100)

# tts_button.js_on_event("button_click", CustomJS(code=f"""
#     var u = new SpeechSynthesisUtterance();
#     u.text = "{text}";
#     u.lang = 'en-US';

#     speechSynthesis.speak(u);
#     """))

# st.bokeh_chart(tts_button)

import streamlit as st
from languages import supported_languages
from abc import ABC, abstractmethod
from deep_translator import GoogleTranslator
import speech_recognition as sr
import cython
import whisper

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
    stream_params = StreamParams()
    recorder = Recorder(stream_params)
    recorder.record(5, "audio.wav")
    
if center_column.button("Click and say sth......"):
    model = whisper.load_model("base")
    transcription = model.transcribe("audio.wav")
    st.markdown(transcription["text"])
    st.markdown(TranslateWords(transcription["text"], supported_languages[destination_language]).getResult())

st.sidebar.header("Play Original Audio File")
st.sidebar.audio("audio.wav")