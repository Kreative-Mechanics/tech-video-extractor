import streamlit as st
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from collections import Counter

# Download necessary NLTK data files
nltk.download('punkt')
nltk.download('stopwords')

def extract_points(text):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    # Remove stop words for better insight extraction
    stop_words = set(stopwords.words('english'))
    words = [word for word in text.split() if word.lower() not in stop_words]
    
    # Count word frequency
    word_freq = Counter(words)

    # Extract key sentences based on word frequency
    key_sentences = sorted(sentences, key=lambda x: sum(word_freq[word] for word in x.split()), reverse=True)

    return key_sentences[:5]  # Return the top 5 sentences

# Streamlit app
st.title("General Text Analysis")

# Text input for transcription
transcription = st.text_area("Paste the transcription text here:", height=300)

if st.button("Analyze"):
    if transcription:
        key_points = extract_points(transcription)

        # Display extracted key points
        st.write("Extracted Key Points:")
        for i, point in enumerate(key_points, 1):
            st.write(f"{i}. {point}")
    else:
        st.warning("Please enter the transcription text for analysis.")
