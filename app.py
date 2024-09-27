import moviepy.editor as mp
import whisper
import os
import math
import tempfile
from pydub import AudioSegment
from pydub.utils import make_chunks

# Load Whisper model
model = whisper.load_model("base")

# Function to transcribe a single audio chunk
def transcribe_audio_chunk(audio_chunk_path):
    result = model.transcribe(audio_chunk_path)
    return result['text']

# Function to split audio into smaller chunks and transcribe each
def transcribe_video_in_chunks(video_path, chunk_length_ms=60000):  # Chunk length in milliseconds
    # Extract audio from the video
    video = mp.VideoFileClip(video_path)
    audio_path = video_path.replace('.mp4', '.wav')
    video.audio.write_audiofile(audio_path)

    # Load the audio file and split into chunks
    audio = AudioSegment.from_wav(audio_path)
    audio_chunks = make_chunks(audio, chunk_length_ms)

    transcription = ""

    # Transcribe each chunk and append to the final transcription
    for i, chunk in enumerate(audio_chunks):
        chunk_name = f"chunk{i}.wav"
        chunk.export(chunk_name, format="wav")

        # Transcribe the chunk
        chunk_transcription = transcribe_audio_chunk(chunk_name)
        transcription += chunk_transcription + " "

        # Remove temporary chunk file
        os.remove(chunk_name)

    # Remove the extracted audio file after transcription
    os.remove(audio_path)

    return transcription

# Streamlit app to handle video upload and transcription
import streamlit as st

st.title("Tech Profile Video Reviewer")

# Upload video file
uploaded_video = st.file_uploader("Choose a video...", type=["mp4", "mov", "avi"])

if uploaded_video is not None:
    # Save the uploaded video to a temporary location
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_video.read())

    # Transcribe the video in chunks
    st.write("Transcribing video in chunks...")
    transcription = transcribe_video_in_chunks(tfile.name)

    # Display the full transcription
    st.subheader("Transcription")
    st.write(transcription)
