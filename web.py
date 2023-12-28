import streamlit as st
from languages import supported_languages
from abc import ABC, abstractmethod
from deep_translator import GoogleTranslator
import speech_recognition as sr
import cython
import whisper
from st_audiorec import st_audiorec

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

# if center_column.button("Click and say sth......"):
#     stream_params = StreamParams()
#     recorder = Recorder(stream_params)
#     recorder.record(5, "audio.wav")
    
# if center_column.button("Translate"):
#     model = whisper.load_model("base")
#     transcription = model.transcribe("audio.wav")
#     st.markdown(transcription["text"])
#     st.markdown(TranslateWords(transcription["text"], supported_languages[destination_language]).getResult())

# st.sidebar.header("Play Original Audio File")
# st.sidebar.audio("audio.wav")
import multiprocessing
 
def write_chunk_to_file(args):
    filename, chunk = args
    with open(filename, "ab") as file:
        file.write(chunk)
 
def write_large_data_to_file_parallel(filename, data, num_processes=40):
    pool = multiprocessing.Pool(processes=num_processes)
    chunk_size = len(data) // num_processes
    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    args_list = [(filename, chunk) for chunk in chunked_data]
    pool.map(write_chunk_to_file, args_list)
    pool.close()
    pool.join()

wav_audio_data = st_audiorec()
from scipy.io.wavfile import write
import numpy as np

if wav_audio_data is not None:
    f = open('audio.wav', 'r+')
    f.truncate(0)
    samplerate = 44100; fs = 100
    t = np.linspace(0., 1., samplerate)
    amplitude = np.iinfo(np.int16).max
    data = amplitude * np.sin(2. * np.pi * fs * t)
    write("audio.wav", samplerate, data.astype(np.int16))
    # st.audio(wav_audio_data, format='audio/wav')
    # write_large_data_to_file_parallel("audio.wav", wav_audio_data)
    # with open('audio.wav', mode='wb') as f:
    #     f.write(wav_audio_data)

if center_column.button("Translate"):
    model = whisper.load_model("base")
    # audio = torch.from_numpy(wav_audio_data)
    transcription = model.transcribe('audio.wav')
    st.markdown("Captured text:\n"+transcription["text"])
    st.markdown("\n\nTranslated text:\n"+TranslateWords(transcription["text"], supported_languages[destination_language]).getResult())