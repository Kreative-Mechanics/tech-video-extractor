import streamlit as st
import whisper
import spacy
import tempfile
import os

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to extract and transcribe using Whisper
def transcribe_video_whisper(video_path):
    model = whisper.load_model("large")  # Use "base" model for performance, "large" for better accuracy
    result = model.transcribe(video_path)
    return result['text']

# Extract key information from transcription using spaCy
def extract_profile_info(transcription):
    doc = nlp(transcription)
    
    years_of_experience = []
    industries = []
    tech_stack = ["Python", "JavaScript", "AWS", "React", "SQL", "Docker", "Kubernetes", "Machine Learning", "Data Science"]
    skills = ["communication", "leadership", "problem-solving", "teamwork"]
    projects = []

    for ent in doc.ents:
        if ent.label_ == "DATE" and "year" in ent.text.lower():
            years_of_experience.append(ent.text)
        if ent.label_ == "ORG":
            industries.append(ent.text)
    
    detected_tech_stack = [tech for tech in tech_stack if tech.lower() in transcription.lower()]
    detected_skills = [skill for skill in skills if skill.lower() in transcription.lower()]
    
    if "project" in transcription.lower():
        projects.append("Project mentioned")

    return {
        "years_of_experience": years_of_experience,
        "industries": industries,
        "tech_stack": detected_tech_stack,
        "skills": detected_skills,
        "projects": projects
    }

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
    
    # Transcribe the video using Whisper
    st.write("Extracting and transcribing audio from the video...")
    transcription = transcribe_video_whisper(tfile.name)
    
    # Display the transcription
    st.subheader("Transcription")
    st.write(transcription)
    
    # Extract profile information using NLP
    profile_info = extract_profile_info(transcription)
    
    # Display extracted profile information
    st.subheader("Profile Analysis")
    
    st.write("**Years of Experience:**")
    st.write(", ".join(profile_info['years_of_experience']) if profile_info['years_of_experience'] else "Not mentioned")
    
    st.write("**Industries Mentioned:**")
    st.write(", ".join(profile_info['industries']) if profile_info['industries'] else "Not mentioned")
    
    st.write("**Tech Stack Mentioned:**")
    st.write(", ".join(profile_info['tech_stack']) if profile_info['tech_stack'] else "Not mentioned")
    
    st.write("**Skills Mentioned:**")
    st.write(", ".join(profile_info['skills']) if profile_info['skills'] else "Not mentioned")
    
    st.write("**Projects Mentioned:**")
    st.write(", ".join(profile_info['projects']) if profile_info['projects'] else "Not mentioned")
