import streamlit as st
from groq import Groq


client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)


def ask_gemini(question):

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer the user's question accurately. "
                    "Do not invent facts. "
                    "If you are uncertain, clearly say so."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content