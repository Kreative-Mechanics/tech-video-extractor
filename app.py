import streamlit as st
from moviepy.editor import VideoFileClip
import whisper
import os
import re

# Function to convert video to audio
def convert_video_to_audio(video_path):
    try:
        # Load video file
        video = VideoFileClip(video_path)
        
        # Path to save the extracted audio
        audio_path = "temp_audio.wav"
        
        # Extract audio
        st.write("Converting video to audio...")
        video.audio.write_audiofile(audio_path, codec='pcm_s16le')
        
        return audio_path
    except Exception as e:
        st.error(f"Error during video to audio conversion: {e}")
        return None

# Function to transcribe audio using Whisper
def transcribe_audio(audio_path):
    try:
        model = whisper.load_model("base")
        st.write("Transcribing audio...")
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        st.error(f"Error during audio transcription: {e}")
        return None

# Function to extract insights from the transcription
def extract_insights(transcription):
    st.write("Extracting insights...")
    
    # Regex for extracting years of experience (basic example)
    experience_pattern = r"(\d{1,2})\s*years of experience"
    experience_match = re.search(experience_pattern, transcription.lower())
    years_of_experience = experience_match.group(1) if experience_match else "Not mentioned"
    
    # Tech stack (list of common programming languages and tools)
    tech_stack_keywords = ["python", "java", "sql", "javascript", "c++", "html", "css", "docker", "kubernetes", "aws", "azure"]
    tech_stack = [tech for tech in tech_stack_keywords if tech in transcription.lower()]
    
    # Extracting industry information (basic example)
    industry_keywords = ["banking", "finance", "healthcare", "education", "retail", "technology"]
    industry = [ind for ind in industry_keywords if ind in transcription.lower()]
    
    # Projects worked on (for simplicity, we'll look for the keyword "project")
    project_pattern = r"project[s]?"
    projects_worked_on = "Mentioned" if re.search(project_pattern, transcription.lower()) else "Not mentioned"
    
    # Compile the extracted insights
    insights = {
        "Years of Experience": years_of_experience,
        "Tech Stack": tech_stack,
        "Industry": industry if industry else "Not mentioned",
        "Projects": projects_worked_on
    }
    
    return insights

# Main Streamlit App Logic
def main():
    st.title("Tech Profile Video Analyzer")
    
    # Upload video file
    tfile = st.file_uploader("Upload your tech profile video", type=['mp4', 'mov', 'avi'])
    
    if tfile:
        # Save the uploaded video temporarily
        video_path = tfile.name
        with open(video_path, "wb") as f:
            f.write(tfile.read())
        
        # Convert video to audio
        audio_path = convert_video_to_audio(video_path)
        
        if audio_path:
            # Transcribe the audio
            transcription = transcribe_audio(audio_path)
            
            if transcription:
                st.write("Transcription")
                st.text(transcription)
                
                # Extract insights from the transcription
                insights = extract_insights(transcription)
                
                # Display insights
                st.write("Profile Analysis")
                st.write(f"Years of Experience: {insights['Years of Experience']}")
                st.write(f"Tech Stack: {', '.join(insights['Tech Stack'])}")
                st.write(f"Industry: {', '.join(insights['Industry'])}")
                st.write(f"Projects Worked On: {insights['Projects']}")
                
                # Clean up temporary files
                os.remove(audio_path)
                os.remove(video_path)
            else:
                st.error("Transcription failed.")
        else:
            st.error("Audio extraction failed.")

if __name__ == "__main__":
    main()
