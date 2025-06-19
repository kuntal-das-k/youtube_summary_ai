Here's a clean and professional `README.md` file for your **YouTube Transcript Summarization API using Gemini Flash**, assuming it's a backend-only project with FastAPI and no frontend:

---

## 📽️ YouTube Transcript Summarizer API (Gemini Flash)

This project provides a simple REST API that accepts a YouTube video URL, extracts its transcript using the YouTube Transcript API, and summarizes it using Google's **Gemini 1.5 Flash** model.

### 🚀 Features

* ✅ Accepts any valid YouTube video URL.
* 📜 Automatically fetches the transcript.
* 🧠 Summarizes it using Gemini 1.5 Flash.
* 📦 Clean JSON output with `topic` and `summary`.

---

### 📂 Tech Stack

* **FastAPI** – Lightweight web framework for building APIs
* **Gemini (GenerativeAI)** – Google's large language model
* **YouTube Transcript API** – For transcript extraction
* **Python 3.9+**

---

### 📦 Installation

1. **Clone the repo**:

```bash
git clone https://github.com/yourusername/youtube-gemini-summarizer.git
cd youtube-gemini-summarizer
```

2. **Create a virtual environment (optional)**:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Set up your Gemini API key**:

Open the Python file (`app.py`) and add your Gemini API key here:

```python
genai.configure(api_key="YOUR_GEMINI_API_KEY")
```

---

### ▶️ Run the API

```bash
uvicorn app:app --reload
```

API will be available at: `http://127.0.0.1:8000/summarize`

---

### 📥 API Usage

**Endpoint:**

```
GET /summarize?video_url=https://www.youtube.com/watch?v=VIDEO_ID
```

**Response Example:**

```json
{
  "topic": "AI in Education",
  "summary": "The video discusses how AI is transforming teaching and learning, including personalized tools and automation."
}
```

---

### ❗ Error Responses

* `400`: Invalid YouTube URL
* `404`: Transcript could not be fetched
* `502`: Gemini API failed to respond
* `500`: Gemini response was not valid JSON

---

### 🛠 Dependencies (`requirements.txt`)

```
fastapi
uvicorn
google-generativeai
youtube-transcript-api
```

---

### 📌 Notes

* This project only works for videos with available auto-captions or transcripts.
* For very long transcripts, Gemini may truncate input. You can add chunking logic if needed.

---

### 👨‍💻 Author

**Kuntal Das**
🔗 [LinkedIn](https://www.linkedin.com/in/kuntal-das-271805287/)
🌐 [Portfolio](https://kuntalportfolio-a86e8.web.app)
