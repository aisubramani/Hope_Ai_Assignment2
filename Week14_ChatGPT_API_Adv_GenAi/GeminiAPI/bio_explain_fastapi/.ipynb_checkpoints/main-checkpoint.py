from fastapi import FastAPI
from pydantic import BaseModel
from google import genai

app = FastAPI(
    title="BioExplain AI",
    description="Biomedical Text Explanation API using Gemini",
    version="1.0"
)

# Gemini client
client = genai.Client(api_key="AIzaSyCsMjLr0qsYQjIpnp2FY3bsy5TSOAddNbc")

# Create chat WITHOUT system_instruction
chat = client.chats.create(
    model="models/gemini-flash-lite-latest"
)

# Send system instruction as first message
chat.send_message(
    "You are a biomedical NLP expert. "
    "Explain biomedical text in simple language "
    "and give real-world or clinical examples."
)

# Request model
class BioTextRequest(BaseModel):
    text: str

# Response model
class BioTextResponse(BaseModel):
    explanation: str
    example: str


@app.post("/explain", response_model=BioTextResponse)
def explain_biomedical_text(request: BioTextRequest):

    explanation = chat.send_message(
        f"Explain the following biomedical text simply:\n{request.text}"
    ).text

    example = chat.send_message(
        "Give one real-world or clinical example related to this."
    ).text

    return {
        "explanation": explanation,
        "example": example
    }


@app.get("/")
def root():
    return {"message": "BioExplain AI is running successfully"}

