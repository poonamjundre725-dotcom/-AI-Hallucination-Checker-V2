import os
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_gemini(question):

    response = client.chat.completions.create(
        # Updated to a highly reliable and widely available Groq model ID
        model="llama3-8b-8192", 
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content