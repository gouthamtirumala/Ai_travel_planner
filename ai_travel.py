import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

# Set page config
st.set_page_config(page_title="AI Powered Travel Planner", layout="centered", page_icon="✈")

st.title("🌍Ai Travel planner ✈")
st.write("Plan your journey in style! 🚀 Enter your details and discover travel cost estimates for every adventure.✨")

# User Inputs
source = st.text_input("📍 Source:")
destination = st.text_input("🎯 Destination:")

# Optional: Basic gradient background (works only for small sections, not full app)
st.markdown(
    """
    <style>
        .st-emotion-cache-1y4p8pa {
            background: linear-gradient(to right, #4facfe, #00f2fe);
            padding: 15px;
            border-radius: 10px;
            color: white;
            text-align: center;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

if st.button("Get Travel Plan"):
    if source and destination:
        with st.spinner("Fetching all travel options..."):
            # Define prompt template
            chat_template = ChatPromptTemplate.from_messages([
                ("system", """
                You are an AI-powered travel assistant designed to help users find the best travel options between a given source and destination.
                Upon receiving the source and destination, generate a list of travel options, including cab, bus, train, and flight choices. 
                For each option, provide the following details:
                - Mode of Transport (e.g., Bus: AC Sleeper, Non-AC Sleeper, etc.)
                - Estimated Price (in INR)
                - Travel Time
                - Distance (in km)

                Focus on accuracy, cost-effectiveness, and convenience, ensuring the user can make an informed decision.

                Conclude with:
                - Recommended Travel Mode
                - Best Time to Travel
                """),
                ("human", "Find travel options from {source} to {destination} along with estimated costs.")
            ])

            # Initialize the Google GenAI chat model (no API key in constructor, it reads from env variable)
            chat_model = ChatGoogleGenerativeAI(api_key="AIzaSyDLQ_21-2FgM1-qsKaFI7sfWCC8YdE9qtM", model="gemini-2.0-flash-exp")

            # Define parser to parse output as plain text
            parser = StrOutputParser()

            # Create chain (Prompt -> Model -> Output Parser)
            chain = chat_template | chat_model | parser

            # Prepare input and invoke chain
            raw_input = {"source": source, "destination": destination}
            response = chain.invoke(raw_input)

            # Display result
            st.success("Possible Travel Routes and Budget Breakdown", icon="🔍")

            # Render each line separately
            travel_modes = response.split("\n")
            for mode in travel_modes:
                if mode.strip():
                    st.markdown(f"✅ {mode}")

    else:
        st.error("Error! Please enter both source and destination.")