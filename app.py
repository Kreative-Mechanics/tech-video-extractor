import streamlit as st
import re

def extract_insights(transcription):
    # Initialize a dictionary to hold extracted insights
    insights = {
        "years_of_experience": None,
        "industries": [],
        "tech_stack": [],
        "skills": [],
        "projects": []
    }
    
    # Regex patterns for extracting information
    years_pattern = r'(\d+)\s+years?\s+of\s+experience'
    industries_pattern = r'(banking|inventory|software|technology|finance|healthcare|education|retail|manufacturing)'  # Add more industries as needed
    tech_stack_pattern = r'\b(SQL|Python|Java|JavaScript|C#|HTML|CSS|React|Node.js|Django|Flask|Swift|Kotlin)\b'  # Extend as needed
    skills_pattern = r'\b(skill1|skill2|skill3|skill4)\b'  # Replace with actual skill names
    projects_pattern = r'\b(project1|project2|project3|project4)\b'  # Replace with actual project names

    # Extract years of experience
    years_match = re.search(years_pattern, transcription)
    if years_match:
        insights["years_of_experience"] = years_match.group(1)

    # Extract industries
    industries_matches = re.findall(industries_pattern, transcription, re.IGNORECASE)
    insights["industries"] = list(set(industries_matches))

    # Extract tech stack
    tech_stack_matches = re.findall(tech_stack_pattern, transcription)
    insights["tech_stack"] = list(set(tech_stack_matches))

    # Extract skills
    skills_matches = re.findall(skills_pattern, transcription)
    insights["skills"] = list(set(skills_matches))

    # Extract projects
    projects_matches = re.findall(projects_pattern, transcription)
    insights["projects"] = list(set(projects_matches))

    return insights

# Streamlit app
st.title("Text Analysis for Tech Profiles")

# Text input for transcription
transcription = st.text_area("Paste the transcription text here:", height=300)

if st.button("Analyze"):
    if transcription:
        insights = extract_insights(transcription)

        # Display extracted insights
        st.write("Extracted Insights:")
        st.write(f"Years of Experience: {insights['years_of_experience']}")
        st.write(f"Industries Worked In: {', '.join(insights['industries']) if insights['industries'] else 'None'}")
        st.write(f"Tech Stack: {', '.join(insights['tech_stack']) if insights['tech_stack'] else 'None'}")
        st.write(f"Skills: {', '.join(insights['skills']) if insights['skills'] else 'None'}")
        st.write(f"Projects Worked On: {', '.join(insights['projects']) if insights['projects'] else 'None'}")
    else:
        st.warning("Please enter the transcription text for analysis.")
