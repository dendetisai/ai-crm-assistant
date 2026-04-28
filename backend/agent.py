import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# -----------------------------
# REAL LLM FUNCTION
# -----------------------------
def run_agent(prompt: str):
    """
    Calls Groq LLM and returns structured response
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant for a pharmaceutical CRM system. Return structured JSON when asked."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# -----------------------------
# TEST BLOCK (OPTIONAL)
# -----------------------------
if __name__ == "__main__":
    result = run_agent("Explain AI in one line")
    print("\n🔹 AI Output:\n")
    print(result)