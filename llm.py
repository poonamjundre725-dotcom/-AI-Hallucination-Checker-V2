import os
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_gemini(question):

    response = client.chat.completions.create(
        # Updated to the current active Groq model
        model="gpt-oss-20b", 
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content