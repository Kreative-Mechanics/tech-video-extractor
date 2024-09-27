import streamlit as st
import whisper
import re
import os

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
    
    # Regex for extracting years of experience
    experience_pattern = r"(\d{1,2})\s*years of experience"
    experience_match = re.search(experience_pattern, transcription.lower())
    years_of_experience = experience_match.group(1) if experience_match else "Not mentioned"
    
    # Tech stack (list of common programming languages and tools)
    tech_stack_keywords = ["python", "java", "sql", "javascript", "c++", "html", "css", "docker", "kubernetes", "aws", "azure"]
    tech_stack = [tech for tech in tech_stack_keywords if tech in transcription.lower()]
    
    # Extracting industry information
    industry_keywords = ["banking", "finance", "healthcare", "education", "retail", "technology"]
    industry = [ind for ind in industry_keywords if ind in transcription.lower()]
    
    # Projects worked on (basic check for the keyword "project")
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
    st.title("Tech Profile Audio Analyzer")
    
    # Upload audio file
    audio_file = st.file_uploader("Upload your tech profile audio", type=['wav', 'mp3'])
    
    if audio_file:
        # Save the uploaded audio temporarily
        audio_path = audio_file.name
        with open(audio_path, "wb") as f:
            f.write(audio_file.read())
        
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
        else:
            st.error("Transcription failed.")

if __name__ == "__main__":
    main()
