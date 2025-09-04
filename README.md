# ResumeConnect - AI-Powered Resume Assistant

🚀 **ResumeConnect** is an interactive AI-powered assistant that helps
recruiters, colleagues, and hiring managers explore **Ankit Raj's
professional journey** in a conversational way.\
The app uses **Gradio** for the UI, integrates **Google Gemini
embeddings** and **LLMs (OpenAI/Gemini)**, and processes resume data to
answer questions contextually.

------------------------------------------------------------------------

## ✨ Features

-   **Chat with Resume** → Ask questions about Ankit's experience,
    skills, and projects.\
-   **AI-Powered Responses** → Contextual answers from Gemini/OpenAI
    LLMs.\
-   **Interactive Sidebar** → Expertise, certifications, and contact
    links at a glance.\
-   **Download Resume** → Secure access to the PDF resume.\
-   **Modern UI** → Responsive design with clean pill-style highlights.

------------------------------------------------------------------------

## 🛠 Tech Stack

-   **Python 3.9+**
-   [Gradio](https://www.gradio.app/) -- interactive UI
-   [LangChain](https://www.langchain.com/) -- prompt management
-   [PyPDF2](https://pypi.org/project/pypdf2/) -- resume PDF parsing
-   [python-dotenv](https://pypi.org/project/python-dotenv/) --
    environment variable management
-   **Google Gemini Embeddings** (`langchain-google-genai`)
-   **OpenAI/Gemini APIs** for LLM responses

------------------------------------------------------------------------

## 📂 Project Structure

    .
    ├── app.py              # Main application
    ├── requirements.txt    # Python dependencies
    ├── .env                # API keys (ignored in git)
    ├── assets/
    │   ├── Ankit-Resume.pdf
    │   └── linkedinlogo.png
    └── README.md

------------------------------------------------------------------------

## ⚙️ Setup & Installation

1.  **Clone the repo**

    ``` bash
    git clone https://github.com/raazankeet/resumeconnect.git
    cd resumeconnect
    ```

2.  **Create a virtual environment**

    ``` bash
    python -m venv venv
    source venv/bin/activate   # (Linux/Mac)
    venv\Scriptsctivate      # (Windows)
    ```

3.  **Install dependencies**

    ``` bash
    pip install -r requirements.txt
    ```

4.  **Add environment variables** in a `.env` file:

    ``` env
    GEMINI_API_KEY=your_gemini_api_key
    GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai
    OPENAI_API_KEY=your_openai_key   # if using OpenAI
    ```

5.  **Run the app**

    ``` bash
    python app.py
    ```

6.  Open <http://localhost:9876> in your browser.

------------------------------------------------------------------------

## 🔒 Security Notes

-   Do **not** commit `.env` or API keys to GitHub.\
-   `.gitignore` already excludes `.env`, `Ankit-Resume.pdf`, and
    personal logos.\
-   For production, store assets (resume, logos) in **Azure Blob
    Storage**, **AWS S3**, or similar.

------------------------------------------------------------------------

## 📜 License

This project is licensed under the **MIT License**.\
You are free to use, modify, and distribute it with attribution.

------------------------------------------------------------------------

## 👤 Author

**Ankit Raj**\
- [LinkedIn](https://www.linkedin.com/in/raazankeet/)\
- [GitHub](https://github.com/raazankeet)\
- 📧 raazankeet@gmail.com
