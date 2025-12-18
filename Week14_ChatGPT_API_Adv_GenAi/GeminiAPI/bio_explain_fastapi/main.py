
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from google import genai
import markdown

app = FastAPI(
    title="BioExplain AI",
    description="Biomedical Text Explanation Chatbot using Gemini",
    version="1.0"
)

templates = Jinja2Templates(directory="templates")

# Initialize Gemini client
client = genai.Client(api_key="AIzaSyCsMjLr0qsYQjIpnp2FY3bsy5TSOAddNbc")

# Create chat session
chat = client.chats.create(
    model="models/gemini-flash-lite-latest"
)

# System instruction (sent once)
chat.send_message(
    "You are a biomedical NLP expert. "
    "Explain biomedical concepts clearly using headings, bullet points, "
    "short paragraphs, and simple language. "
    "Always keep output well structured."
)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/", response_class=HTMLResponse)
def explain_text(request: Request, text: str = Form(...)):

    raw_explanation = chat.send_message(
        f"""
Explain the following biomedical concept in a clean and structured format.

Rules:
- Use headings (##)
- Use bullet points
- Use short paragraphs
- Avoid long blocks of text

Text:
{text}
"""
    ).text

    raw_example = chat.send_message(
        """
Give one real-world or clinical example.
Format it clearly using headings and bullet points.
"""
    ).text

    # Convert Markdown → HTML
    explanation = markdown.markdown(raw_explanation)
    example = markdown.markdown(raw_example)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "explanation": explanation,
            "example": example
        }
    )
