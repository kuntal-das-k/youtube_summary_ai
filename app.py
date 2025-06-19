from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from typing import Optional
import re
import json
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# ==== FastAPI App Init ====
app = FastAPI()

# ==== Gemini API Key Config ====
genai.configure(api_key="AIzaSyBPYFahsZmYoyAcFvrHYcB9QCaAQX6rx10")  # Replace with your actual key


# ==== Extract YouTube Video ID ====
def extract_video_id(url: str) -> Optional[str]:
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    return match.group(1) if match else None


# ==== Fetch Transcript from YouTube ====
def get_transcript(video_id: str) -> Optional[str]:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript])
    except Exception as e:
        print("❌ Transcript fetch error:", e)
        return None


# ==== Summarize using Gemini ====
def summarize_with_gemini(transcript: str) -> Optional[str]:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
You are a helpful assistant. Summarize the following YouTube transcript in a **very short** format and include a **brief topic name**.

Respond ONLY in the following JSON format:
{{
  "topic": "Short title",
  "summary": "Brief and clear summary."
}}

Transcript:
\"\"\"{transcript}\"\"\"
"""

        response = model.generate_content(prompt)
        print("📤 Gemini raw response:\n", response.text)
        return response.text.strip() if response.text else None

    except Exception as e:
        print("❌ Gemini API error:", e)
        return None


# ==== FastAPI Endpoint ====
@app.get("/summarize")
def summarize(video_url: str = Query(..., alias="video_url")):
    video_id = extract_video_id(video_url)
    if not video_id:
        return JSONResponse(status_code=400, content={"error": "Invalid YouTube URL."})

    transcript = get_transcript(video_id)
    if not transcript:
        return JSONResponse(status_code=404, content={"error": "Transcript fetch failed."})

    print("✅ Transcript length:", len(transcript))

    response_text = summarize_with_gemini(transcript)
    if not response_text:
        return JSONResponse(status_code=502, content={"error": "Gemini summarization failed."})

    try:
        # Clean any markdown/code block formatting from Gemini response
        cleaned_text = response_text.strip("` \n")
        if cleaned_text.lower().startswith("json"):
            cleaned_text = cleaned_text[4:].strip("` \n")

        summary_json = json.loads(cleaned_text)
        return {
            "topic": summary_json.get("topic", "N/A"),
            "summary": summary_json.get("summary", "No summary generated.")
        }
    except json.JSONDecodeError as e:
        return JSONResponse(status_code=500, content={
            "error": f"Gemini response was not valid JSON: {str(e)}",
            "raw_response": response_text
        })
