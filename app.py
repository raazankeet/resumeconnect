import os
import logging
import gradio as gr
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# ========================
# 🔑 Configurable Variables
# ========================
RESUME_PATH = r"Ankit-Resume.pdf"   # local file path
LINKEDIN_URL = "https://www.linkedin.com/in/raazankeet/"
LINKEDIN_LOGO = r"linkedinlogo.png"        # local PNG file
GITHUB_URL="https://github.com/raazankeet" # GitHub URL
EMAIL="raazankeet@gmail.com"               # Email address


if os.getenv("ENVIRONMENT") != "production":
    from dotenv import load_dotenv
    load_dotenv()


# Compact professional header with reduced margin
markdown_content = """
<div style="background: linear-gradient(90deg, #1e40af 0%, #3730a3 100%); 
            padding: 0.5rem 1.5rem; border-radius: 12px; margin: 0; 
            box-shadow: 0 4px 12px rgba(30,64,175,0.15);">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div>
            <h1 style="font-size: 1.5em; margin: 0; font-weight: 700; 
                       color: #ffffff; display: inline-block;">
                ResumeConnect
            </h1>
            <span style="color: #c7d2fe; font-size: 0.9em; margin-left: 1rem; font-weight: 500;">
                Explore Ankit Raj's Professional Journey
            </span>
        </div>
        <div style="color: #e0e7ff; font-size: 0.85em; font-weight: 500;">
            🚀 AI-Powered Resume Assistant
        </div>
    </div>
</div>
"""

# Compact sidebar with smaller fonts and diverse pill colors
SIDEBAR_HTML = f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
  * {{ font-family: 'Inter', sans-serif; }}
  
  #sidebar {{
    position: sticky;
    top: 0px;
    align-self: flex-start;
    max-width: 100%;
    height: fit-content;
  }}

  .professional-card {{
    background: #B8BFC4;
    border: 1px solid #d1d5db;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    border-radius: 10px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }}
  
  .professional-card:hover {{
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
    transform: translateY(-1px);
  }}
  
  /* Compact skill pills with diverse colors */
  .skills-container {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
    align-items: flex-start;
  }}
  
  .skill-pill {{
    padding: 0.25rem 0.6rem;
    font-size: 0.65rem;
    border-radius: 20px;
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    cursor: pointer;
    white-space: nowrap;
    line-height: 1.2;
    color: #ffffff !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    position: relative;
    overflow: hidden;
    transform: translateZ(0);
  }}
  
  .skill-pill::before {{
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  }}
  
  .skill-pill:hover::before {{
    left: 100%;
  }}
  
  .skill-pill:hover {{
    transform: translateY(-2px) scale(1.05) translateZ(0);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
    filter: brightness(1.1);
  }}
  
  .skill-pill:active {{
    transform: translateY(-1px) scale(1.02) translateZ(0);
    transition: all 0.1s cubic-bezier(0.4, 0, 0.2, 1);
  }}
  
  /* Diverse color schemes for pills */
  .skill-blue {{ background: linear-gradient(135deg, #1e40af, #3730a3); }}
  .skill-purple {{ background: linear-gradient(135deg, #7c3aed, #5b21b6); }}
  .skill-green {{ background: linear-gradient(135deg, #059669, #047857); }}
  .skill-red {{ background: linear-gradient(135deg, #dc2626, #b91c1c); }}
  .skill-cyan {{ background: linear-gradient(135deg, #0891b2, #0e7490); }}
  .skill-indigo {{ background: linear-gradient(135deg, #4f46e5, #4338ca); }}
  .skill-orange {{ background: linear-gradient(135deg, #ea580c, #c2410c); }}
  .skill-pink {{ background: linear-gradient(135deg, #db2777, #be185d); }}
  .skill-emerald {{ background: linear-gradient(135deg, #10b981, #059669); }}
  .skill-violet {{ background: linear-gradient(135deg, #8b5cf6, #7c3aed); }}
  .skill-rose {{ background: linear-gradient(135deg, #f43f5e, #e11d48); }}
  .skill-amber {{ background: linear-gradient(135deg, #f59e0b, #d97706); }}
  .skill-teal {{ background: linear-gradient(135deg, #14b8a6, #0d9488); }}
  .skill-slate {{ background: linear-gradient(135deg, #64748b, #475569); }}

.skill-yellow {{ background: linear-gradient(135deg, #eab308, #ca8a04); }}
.skill-lime   {{ background: linear-gradient(135deg, #65a30d, #4d7c0f); }}
.skill-brown  {{ background: linear-gradient(135deg, #92400e, #78350f); }}
.skill-stone  {{ background: linear-gradient(135deg, #78716c, #57534e); }}
.skill-zinc   {{ background: linear-gradient(135deg, #71717a, #52525b); }}
.skill-neutral {{ background: linear-gradient(135deg, #737373, #404040); }}
.skill-fuchsia {{ background: linear-gradient(135deg, #c026d3, #86198f); }}
.skill-sky     {{ background: linear-gradient(135deg, #0ea5e9, #0369a1); }}
.skill-light   {{ background: linear-gradient(135deg, #f3f4f6, #d1d5db); }}
.skill-dark    {{ background: linear-gradient(135deg, #1f2937, #111827); }}
  
  .social-link {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 2rem;
    height: 2rem;
    border-radius: 8px;
    background: #e5e7eb;
    border: 1px solid #d1d5db;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    text-decoration: none;
  }}
  
  .social-link:hover {{
    background: #d1d5db;
    border-color: #9ca3af;
    transform: translateY(-2px) scale(1.05);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }}
  
  .social-linkedin:hover {{ background: #0077b5; border-color: #0077b5; }}
  .social-github:hover {{ background: #333; border-color: #333; }}
  .social-email:hover {{ background: #ea4335; border-color: #ea4335; }}
  
  .social-link:hover img {{ filter: brightness(0) invert(1); }}
  
  /* Compact status indicator */
  .status-dot {{
    width: 6px;
    height: 6px;
    background: #10b981;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 2s ease-in-out infinite;
    box-shadow: 0 0 6px rgba(16, 185, 129, 0.5);
  }}
  
  @keyframes pulse {{
    0%, 100% {{ 
      opacity: 1; 
      transform: scale(1);
      box-shadow: 0 0 6px rgba(16, 185, 129, 0.5);
    }}
    50% {{ 
      opacity: 0.7; 
      transform: scale(1.1);
      box-shadow: 0 0 8px rgba(16, 185, 129, 0.8);
    }}
  }}
  
  /* Compact typography */
  .text-primary {{ color: #1f2937; }}
  .text-secondary {{ color: #4b5563; }}
  .section-title {{ 
    color: #1f2937; 
    font-weight: 600; 
    font-size: 0.75rem; 
    margin-bottom: 0.4rem;
    display: block;
  }}
  
  /* Compact download button */
  .download-btn {{
    display: block;
    width: 100%;
    text-align: center;
    background: linear-gradient(135deg, #1e40af, #3730a3);
    color: #ffffff !important;
    font-weight: 600;
    padding: 0.6rem;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    margin-bottom: 0.8rem;
    font-size: 0.8rem;
    border: none;
    text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    position: relative;
    overflow: hidden;
  }}

  a.download-btn,
  a.download-btn:visited,
  a.download-btn:hover,
  a.download-btn:active {{
    text-decoration: none !important;
  }}
  
  .download-btn::before {{
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  }}
  
  .download-btn:hover::before {{
    left: 100%;
  }}
  
  .download-btn:hover {{
    background: linear-gradient(135deg, #1d4ed8, #4338ca);
    color: #ffffff !important;
    text-decoration: none;
    transform: translateY(-2px);
    box-shadow: 0 6px 14px rgba(30, 64, 175, 0.4);
    filter: brightness(1.05);
  }}
  
  .download-btn:active {{
    transform: translateY(0);
    transition: all 0.1s cubic-bezier(0.4, 0, 0.2, 1);
  }}

    
  .section-divider {{
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.6), rgba(118, 75, 162, 0.6), rgba(240, 147, 251, 0.6), transparent);
    margin: 1.2rem 0;
    border-radius: 1px;
    position: relative;
    overflow: hidden;
  }}

    .section-divider::after {{
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent);
    animation: dividerSlide 3s ease-in-out infinite;
  }}
</style>

<div id="sidebar">
  <div class="professional-card" style="padding: 0.9rem;">
    
    <!-- Compact Profile Header -->
    <div style="text-align: center; border-bottom: 1px solid #d1d5db; padding-bottom: 0.7rem; margin-bottom: 0.7rem;">
      <h2 style="margin: 0 0 0.3rem 0; font-size: 1rem; font-weight: 700; color: #1f2937;">Ankit Raj</h2>
      <div style="display: inline-flex; align-items: center; gap: 0.4rem; background: linear-gradient(135deg, #1e40af, #3730a3); 
                  color: white; padding: 0.25rem 0.6rem; border-radius: 16px; font-size: 0.7rem; font-weight: 600;">
        <span class="status-dot"></span>
        Senior Architect
      </div>
      <p style="margin: 0.3rem 0 0 0; font-size: 0.75rem; color: #4b5563; font-weight: 500;">Cloud & AI Enthusiast</p>
    </div>

    <!-- Compact Download Resume Button -->
    <a href="{RESUME_PATH}" download class="download-btn">
      📄 Download Resume
    </a>

    <!-- Compact Connect Section -->
    <div style="margin-bottom: 0.8rem;">
      <span class="section-title">🔗 Connect</span>
      <div style="display: flex; gap: 0.4rem; justify-content: flex-start;">
        <a href="{LINKEDIN_URL}" target="_blank" title="LinkedIn" class="social-link social-linkedin">
          <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" 
               alt="LinkedIn" style="width: 14px; height: 14px;">
        </a>
        <a href="{GITHUB_URL}" target="_blank" title="GitHub" class="social-link social-github">
          <img src="https://cdn-icons-png.flaticon.com/512/733/733609.png" 
               alt="GitHub" style="width: 14px; height: 14px;">
        </a>
        <a href="mailto:{EMAIL}" title="Email" class="social-link social-email">
          <img src="https://cdn-icons-png.flaticon.com/512/732/732200.png" 
               alt="Email" style="width: 14px; height: 14px;">
        </a>
      </div>
    </div>

    <!-- Compact Key Expertise with diverse colors -->
     <div class="section-divider"></div>
    <div style="margin-bottom: 0.8rem;">
      <span class="section-title">⭐ Key Expertise</span>
      <div class="skills-container">
        <span class="skill-pill skill-blue">Digital Transformation</span>
        <span class="skill-pill skill-lime">Cloud Modernization</span>
        <span class="skill-pill skill-purple">Data Engineering</span>
        <span class="skill-pill skill-green">Data Governance</span>
        <span class="skill-pill skill-cyan">Data Fabric</span>
        <span class="skill-pill skill-red">Data Obfuscation</span>
        
        <span class="skill-pill skill-indigo">Architecture Reviews</span>  
        <span class="skill-pill skill-orange">Agentic AI</span>
        <span class="skill-pill skill-pink">Chat Bots</span>
        <span class="skill-pill skill-emerald">API Design</span>
        <span class="skill-pill skill-violet">Informatica Cloud</span>
        <span class="skill-pill skill-rose">Vector DB</span>
      </div>
    </div>

    <!-- Compact Certifications with unique colors -->
     <div class="section-divider"></div>
    <div style="margin-bottom: 0.8rem;">
      <span class="section-title">🏆 Certifications</span>
      <div class="skills-container">
        <span class="skill-pill skill-amber">DP-900 Azure Data</span>
        <span class="skill-pill skill-teal">AI-102 Azure AI Engineer</span>
        <span class="skill-pill skill-slate">IDMC Champion</span>
      </div>
    </div>

    <!-- Compact Status -->
    <div style="padding-top: 0.7rem; border-top: 1px solid #d1d5db; text-align: center;">
      <div style="display: flex; align-items: center; justify-content: center; gap: 0.4rem; 
                  font-size: 0.7rem; color: #4b5563; font-weight: 500;">
        <span class="status-dot"></span>
        <span>Available for opportunities</span>
      </div>
    </div>
  </div>
</div>
"""

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========================
# Profile Data Loader
# ========================
class ProfileDataLoader:
    def extract_resume_text(self, resume_path: str) -> str:
        if not os.path.exists(resume_path):
            raise FileNotFoundError(f"Resume file not found at {resume_path}")

        text_chunks = []
        with open(resume_path, "rb") as f:
            pdf = PdfReader(f)
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_chunks.append(text.strip())

        resume_text = "\n".join(text_chunks)
        logger.info(f"Extracted {len(resume_text)} characters from resume")
        return resume_text

    def load_data(self, resume_path: str, linkedin_url: str):
        resume_text = self.extract_resume_text(resume_path)
        return {
            "resume_text": resume_text,
            "resume_path": resume_path,
            "linkedin_url": linkedin_url
        }

# ========================
# Personal Assistant
# ========================
class PersonalAssistant:
    def __init__(self, resume_path: str, linkedin_url: str):
        self.data_loader = ProfileDataLoader()
        self.conversation_history = []

        # ✅ Gemini embeddings + LLM
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
        self.llm = ChatOpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url=os.getenv("GEMINI_BASE_URL"),
            model="gemini-1.5-flash",
            temperature=0.3,
            max_tokens=5000,
            top_p=0.8
        )

        self.profile_data = self.data_loader.load_data(resume_path, linkedin_url)

    def answer_question(self, message: str, history) -> str:
        prompt = f"""
You are a helpful assistant speaking as Ankit Raj in the first person ('I', 'my'), a seasoned professional with a strong architectural background.
Your role is to answer questions on my behalf based on my resume, LinkedIn profile, and professional experience.
Guidelines for Responses:
Maintain a conversational, approachable, and professional tone.
Provide accurate and relevant answers strictly from the given context.
If certain details are not available in the context, politely acknowledge it.
When relevant, highlight my key achievements, skills, and professional experiences to add depth.
Keep answers clear, focused, and concise.
I value integrity and transparency; avoid fabricating information.
My phone number is +91-8595010310 and my email is raazankeet@gmail.com.
For resume download requests, guide the user to download my resume.

Resume Data:
{self.profile_data['resume_text']}

Question: {message}
"""
        try:
            response = self.llm.invoke(prompt)
            return response.content.strip()
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return "Sorry, I had trouble generating an answer."

# ========================
# Initialize Assistant
# ========================
assistant = PersonalAssistant(resume_path=RESUME_PATH, linkedin_url=LINKEDIN_URL)

# ========================
# MINIMAL CSS - Only fix top gap and basic alignment
# ========================
custom_css = """
/* Remove top gap only */
.gradio-container {
    background: #f1f5f9 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    padding-top: 0.5rem !important;
}

/* Hide footer */
footer { visibility: hidden !important; }

/* Basic chat styling */
.gr-chatbot {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
    height: 600px !important;
}

.chatbot .message.user {
    background: #1e40af !important;
    color: white !important;
}

.chatbot .message.bot {
    background: #f8fafc !important;
    color: #111827 !important;
}

/* Example buttons */
.gr-examples .gr-button {
    background: #AEC9FF !important;
    color: #374151 !important;
    border: 1px solid #d1d5db !important;
    font-weight: 500 !important;
    padding: 0.4rem 0.6rem !important;
    font-size: 0.8rem !important;
    border-radius: 20px !important;
}

.gr-examples .gr-button:hover {
    background: #e5e7eb !important;
    color: #111827 !important;
    border-color: #9ca3af !important;
    transform: translateY(-1px) scale(1.02) !important;
}

/* Sidebar styling */
.gr-column:last-child {
    background: #f3f4f6 !important;
    padding: 1.2rem !important;
    border-radius: 12px !important;
    border-left: 2px solid #d1d5db !important;
}
"""

with gr.Blocks(
    css=custom_css,
    title="ResumeConnect - Ankit Raj",
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="gray",
        neutral_hue="slate",
        font=gr.themes.GoogleFont("Inter"),
        spacing_size="sm",
        radius_size="md"
    )
) as demo:
    gr.Markdown(markdown_content)
    
    with gr.Row():
        # Adjusted column scales - wider sidebar
        with gr.Column(scale=5):
            gr.ChatInterface(
                fn=assistant.answer_question,
                type="messages",
                chatbot=gr.Chatbot(
                    height=530, 
                    label="Chat with Ankit's AI Assistant",
                    show_label=True,
                    container=True,
                    
                ),
                textbox=gr.Textbox(
                    placeholder="Ask me about my experience, skills, projects, or anything else! 🚀",
                    container=False,
                    scale=7
                ),
                title="",
                description="",
                examples=[
                    "Tell me about your cloud architecture experience",
                    "What AI projects have you worked on?",
                    "How can you help with digital transformation?",
                    "What's your approach to data governance?",
                    "Tell me about your leadership experience"
                ]
            )

        # Wider sidebar
        with gr.Column(scale=2, min_width=350):
            gr.HTML(SIDEBAR_HTML)

# Launch with enhanced configuration
import os

if __name__ == "__main__":
    # Azure Web Apps typically use port 8000, but check multiple env vars
    port = int(os.getenv("PORT") or os.getenv("WEBSITES_PORT") or 8000)
    
    # Always bind to 0.0.0.0 for containerized deployments
    server_name = "0.0.0.0"
    
    print(f"Starting server on {server_name}:{port}")
    print(f"Environment PORT: {os.getenv('PORT')}")
    print(f"Environment WEBSITES_PORT: {os.getenv('WEBSITES_PORT')}")
    
    demo.launch(
        share=False,
        server_name=server_name,
        server_port=port,
        show_error=True  # This will help with debugging
    )
