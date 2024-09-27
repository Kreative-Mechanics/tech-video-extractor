import streamlit as st
import subprocess
from moviepy.editor import VideoFileClip
import whisper

# Function to check if FFmpeg is installed
def check_ffmpeg_installation():
    try:
        ffmpeg_installed = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return ffmpeg_installed.stdout.decode()
    except FileNotFoundError:
        return None

# Function to extract audio from the video and transcribe it
def transcribe_video_in_chunks(video_path):
    try:
        # Load video file
        video = VideoFileClip(video_path)
        
        # Path to save the extracted audio
        audio_path = "temp_audio.wav"
        
        # Extract audio, explicitly specifying the codec
        st.write("Extracting audio from the video...")
        video.audio.write_audiofile(audio_path, codec='pcm_s16le')
        
        # Now proceed to transcribe the extracted audio
        st.write("Transcribing audio...")
        transcription = transcribe_audio_in_chunks(audio_path)
        return transcription
    except Exception as e:
        st.error(f"Error during video transcription: {e}")
        return None

# Function to transcribe the extracted audio file in chunks
def transcribe_audio_in_chunks(audio_path):
    model = whisper.load_model("base")  # Load the Whisper model
    result = model.transcribe(audio_path)
    return result["text"]

# Main Streamlit App Logic
def main():
    st.title("Tech Profile Video Extractor")
    
    # Display FFmpeg version to check if it's installed
    ffmpeg_version = check_ffmpeg_installation()
    if ffmpeg_version:
        st.write("FFmpeg is installed and available.")
        st.code(ffmpeg_version)
    else:
        st.error("FFmpeg is not installed or not accessible in this environment.")
    
    # Upload video
    tfile = st.file_uploader("Upload your tech profile video", type=['mp4', 'mov', 'avi'])
    
    if tfile:
        # Save the uploaded video temporarily
        with open(tfile.name, "wb") as f:
            f.write(tfile.read())
        
        st.write(f"Processing video: {tfile.name}")
        
        # Transcribe video
        transcription = transcribe_video_in_chunks(tfile.name)
        
        if transcription:
            st.write("Transcription")
            st.text(transcription)
            
            # Further processing for tech stack, experience, etc. can go here
            st.write("Profile Analysis")
            # Example placeholder logic for extracting info (adjust according to your needs)
            tech_stack = ["SQL", "Python", "JavaScript"]  # Placeholder
            experience_years = 5  # Placeholder
            
            st.write(f"Tech Stack Mentioned: {', '.join(tech_stack)}")
            st.write(f"Years of Experience: {experience_years}")
        else:
            st.error("Transcription failed.")
        
if __name__ == "__main__":
    main()
