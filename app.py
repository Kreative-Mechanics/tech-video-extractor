import streamlit as st
import speech_recognition as sr
import moviepy.editor as mp
import tempfile
import os


# Function to extract audio from video and transcribe using SpeechRecognition
def transcribe_video(video_path):
    recognizer = sr.Recognizer()

    # Extract audio from video using moviepy
    video = mp.VideoFileClip(video_path)
    audio_path = "audio.wav"
    video.audio.write_audiofile(audio_path)

    # Load the audio for speech recognition
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            # Transcribe the audio to text
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            text = "Sorry, couldn't understand the audio."
        except sr.RequestError:
            text = "Request failed; please check your internet connection."

    # Remove the audio file to clean up
    os.remove(audio_path)

    return text


# Streamlit app layout
st.title("Tech Profile Video Reviewer")
st.write("Upload a video with your tech profile, and we'll extract and analyze the content.")

# Upload video file
uploaded_video = st.file_uploader("Choose a video...", type=["mp4", "mov", "avi"])

if uploaded_video is not None:
    # Save video to a temporary location
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_video.read())

    # Display the uploaded video
    st.video(tfile.name)

    # Transcribe the video
    st.write("Extracting and transcribing audio from the video...")
    transcription = transcribe_video(tfile.name)

    # Display the transcription
    st.subheader("Transcription")
    st.write(transcription)

    # Analyze the transcription for keywords
    st.subheader("Profile Analysis")

    tech_keywords = ["Python", "JavaScript", "AWS", "React", "SQL", "Docker", "Kubernetes", "Machine Learning",
                     "Data Science"]
    skills_keywords = ["communication", "leadership", "problem-solving", "teamwork"]
    experiences_keywords = ["years", "project", "company", "internship", "freelance", "product"]

    # Display detected tech stack
    st.write("**Tech Stack Mentioned:**")
    for keyword in tech_keywords:
        if keyword.lower() in transcription.lower():
            st.write(f"- {keyword}")

    # Display detected skills
    st.write("**Skills Mentioned:**")
    for skill in skills_keywords:
        if skill.lower() in transcription.lower():
            st.write(f"- {skill}")

    # Display detected experiences
    st.write("**Experiences Mentioned:**")
    for experience in experiences_keywords:
        if experience.lower() in transcription.lower():
            st.write(f"- {experience}")
