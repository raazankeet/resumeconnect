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
RESUME_PATH = r"static/Ankit-Raj-Resume.pdf"   # local file path
LINKEDIN_URL = "https://www.linkedin.com/in/raazankeet/"
GITHUB_URL="https://github.com/raazankeet" # GitHub URL
EMAIL="raazankeet@gmail.com"               # Email address
AVATAR_PATH = "static/avatar.png"  # Add your avatar image path here


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

# Compact sidebar with integrated download button and avatar
def create_sidebar_html():
    # Check if resume file exists for download button
    download_button_html = ""
    if os.path.exists(RESUME_PATH):
        # Create a download link that works in HTML with PDF icon
        download_button_html = f"""
        <div style="margin-bottom: 0.6rem; display: flex; justify-content: center;">
            <a href="data:application/pdf;base64,{get_resume_base64()}" 
               download="Ankit-Raj-Resume.pdf" 
               style="text-decoration: none; width: 75%;">
                <button style="background: linear-gradient(135deg, #6366f1, #8b5cf6, #d946ef); 
                               color: #ffffff; font-weight: 600; padding: 0.6rem 0.6rem; 
                               border-radius: 10px; border: none; font-size: 0.8rem; 
                               width: 100%; cursor: pointer; display: flex; align-items: center; 
                               justify-content: center; gap: 0.5rem;
                               transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                               box-shadow: 0 3px 10px rgba(99, 102, 241, 0.3);
                               position: relative; overflow: hidden;"
                        onmouseover="this.style.background='linear-gradient(135deg, #7c3aed, #a855f7, #ec4899)'; this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(124, 58, 237, 0.4)';"
                        onmouseout="this.style.background='linear-gradient(135deg, #6366f1, #8b5cf6, #d946ef)'; this.style.transform='translateY(0)'; this.style.boxShadow='0 3px 10px rgba(99, 102, 241, 0.3)';">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
                    </svg>
                    Download Resume
                </button>
            </a>
        </div>
        """
    else:
        download_button_html = f"""
        <div style="text-align: center; padding: 0.6rem; background: #fca5a5; color: #991b1b; 
                    border-radius: 10px; font-size: 0.8rem; margin-bottom: 0.6rem;">
            Resume file not found
        </div>
        """
    
    # Avatar handling - check if avatar exists with smaller green dot
    avatar_html = ""
    if os.path.exists(AVATAR_PATH):
        avatar_base64 = get_avatar_base64()
        avatar_html = f"""
        <div style="text-align: center; margin-bottom: 0.4rem;">
            <div style="position: relative; display: inline-block;">
                <img src="data:image/jpeg;base64,{avatar_base64}" 
                     alt="Ankit Raj" 
                     style="width: 70px; height: 70px; border-radius: 50%; 
                            border: 3px solid #10b981; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
                            object-fit: cover;">
                <div style="position: absolute; bottom: 2px; right: 2px; 
                           width: 12px; height: 12px; background: #10b981; 
                           border: 2px solid white; border-radius: 50%;
                           box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div>
            </div>
        </div>
        """
    else:
        # Fallback avatar with initials and smaller green dot
        avatar_html = """
        <div style="text-align: center; margin-bottom: 0.4rem;">
            <div style="position: relative; display: inline-block;">
                <div style="width: 70px; height: 70px; border-radius: 50%; 
                           background: linear-gradient(135deg, #10b981, #059669); 
                           display: flex; align-items: center; justify-content: center;
                           color: white; font-weight: 700; font-size: 1.4rem;
                           border: 3px solid #10b981; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);">
                    AR
                </div>
                <div style="position: absolute; bottom: 2px; right: 2px; 
                           width: 12px; height: 12px; background: #10b981; 
                           border: 2px solid white; border-radius: 50%;
                           box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div>
            </div>
        </div>
        """
    
    return f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
  * {{ font-family: 'Inter', sans-serif; }}
  
  #sidebar {{
    position: sticky;
    top: 0px;
    align-self: flex-start;
    max-width: 100%;
    height: fit-content;
    max-height: 80vh;
    overflow: visible;
  }}

  .professional-card {{
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 50%, #e2e8f0 100%);
    border: 1px solid #cbd5e1;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08), 0 1px 3px rgba(0, 0, 0, 0.1);
    border-radius: 16px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(10px);
  }}
  
  .professional-card:hover {{
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12), 0 4px 10px rgba(0, 0, 0, 0.08);
    transform: translateY(-2px);
  }}
  
  /* Ultra compact skill pills with diverse color schemes */
  .skills-container {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.2rem;
    align-items: flex-start;
  }}
  
  .skill-pill {{
    padding: 0.25rem 0.5rem;
    font-size: 0.6rem;
    border-radius: 14px;
    font-weight: 700;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    cursor: pointer;
    white-space: nowrap;
    line-height: 1.3;
    color: #ffffff !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    position: relative;
    overflow: hidden;
    transform: translateZ(0);
    letter-spacing: 0.02em;
    border: 1px solid rgba(255,255,255,0.2);
  }}
  
  .skill-pill::before {{
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    transition: left 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  }}
  
  .skill-pill:hover::before {{
    left: 100%;
  }}
  
  .skill-pill:hover {{
    transform: translateY(-1px) scale(1.05) translateZ(0);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    filter: brightness(1.1) saturate(1.1);
  }}
  
  /* Diverse gradient color schemes */
  .skill-purple {{ background: linear-gradient(135deg, #8b5cf6, #7c3aed); }}
  .skill-green {{ background: linear-gradient(135deg, #10b981, #059669); }}
  .skill-orange {{ background: linear-gradient(135deg, #f59e0b, #d97706); }}
  .skill-pink {{ background: linear-gradient(135deg, #ec4899, #db2777); }}
  .skill-cyan {{ background: linear-gradient(135deg, #06b6d4, #0891b2); }}
  .skill-red {{ background: linear-gradient(135deg, #ef4444, #dc2626); }}
  .skill-emerald {{ background: linear-gradient(135deg, #34d399, #10b981); }}
  .skill-violet {{ background: linear-gradient(135deg, #a78bfa, #8b5cf6); }}
  .skill-rose {{ background: linear-gradient(135deg, #fb7185, #f43f5e); }}
  .skill-amber {{ background: linear-gradient(135deg, #fbbf24, #f59e0b); }}
  .skill-teal {{ background: linear-gradient(135deg, #2dd4bf, #14b8a6); }}
  .skill-slate {{ background: linear-gradient(135deg, #64748b, #475569); }}
  .skill-indigo {{ background: linear-gradient(135deg, #6366f1, #4f46e5); }}
  .skill-lime {{ background: linear-gradient(135deg, #84cc16, #65a30d); }}
  .skill-fuchsia {{ background: linear-gradient(135deg, #d946ef, #c026d3); }}
  .skill-sky {{ background: linear-gradient(135deg, #38bdf8, #0ea5e9); }}
  
  .social-link {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 2rem;
    height: 2rem;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.8);
    border: 1px solid rgba(148, 163, 184, 0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    text-decoration: none;
    backdrop-filter: blur(5px);
  }}
  
  .social-link:hover {{
    transform: translateY(-2px) scale(1.08);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
  }}
  
  .social-linkedin:hover {{ background: #0077b5; border-color: #0077b5; }}
  .social-github:hover {{ background: #333; border-color: #333; }}
  .social-email:hover {{ background: #ea4335; border-color: #ea4335; }}
  
  .social-link:hover img {{ filter: brightness(0) invert(1); }}
  
  /* Smaller status indicator */
  .status-dot {{
    width: 4px;
    height: 4px;
    background: #10b981;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 2s ease-in-out infinite;
    box-shadow: 0 0 4px rgba(16, 185, 129, 0.5);
  }}
  
  @keyframes pulse {{
    0%, 100% {{ 
      opacity: 1; 
      transform: scale(1);
      box-shadow: 0 0 4px rgba(16, 185, 129, 0.5);
    }}
    50% {{ 
      opacity: 0.7; 
      transform: scale(1.2);
      box-shadow: 0 0 6px rgba(16, 185, 129, 0.8);
    }}
  }}
  
  /* Enhanced typography */
  .text-primary {{ color: #1f2937; }}
  .text-secondary {{ color: #374151; }}
  .section-title {{ 
    color: #1f2937; 
    font-weight: 700; 
    font-size: 0.75rem; 
    margin-bottom: 0.4rem;
    display: block;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }}
    
.section-divider {{
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(16, 185, 129, 0.9),   /* emerald green */
    rgba(59, 130, 246, 0.9),   /* vibrant blue */
    transparent
  );
  margin: 0.5rem 0;
  border-radius: 2px;
  box-shadow: 0 0 6px rgba(59, 130, 246, 0.4);
}}
</style>

<div id="sidebar">
  <div class="professional-card" style="padding: 0.7rem;">
    
    <!-- Avatar -->
    {avatar_html}
    
    <!-- Enhanced Profile Header -->
    <div style="text-align: center; border-bottom: 1px solid rgba(148, 163, 184, 0.3); 
                padding-bottom: 0.6rem; margin-bottom: 0.6rem;">
      <h2 style="margin: 0 0 0.3rem 0; font-size: 1rem; font-weight: 800; color: #1f2937;">Ankit Raj</h2>
      <div style="display: flex; align-items: center; justify-content: center; gap: 0.4rem; 
                  background: linear-gradient(135deg, #10b981, #059669); 
                  color: white; padding: 0.25rem 0.6rem; border-radius: 14px; 
                  font-size: 0.7rem; font-weight: 700; box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
                  margin: 0 auto; width: fit-content; text-align: center; white-space: nowrap;">
        <span class="status-dot"></span>
        <div style="display:flex;text-align:center; justify-content:center; align-items:center;">
  <span style="line-height:1;text-align:center; display:inline-block;">Senior Architect</span>
</div>
      </div>
      
      <p style="margin: 0.3rem 0 0 0; font-size: 0.75rem; color: #6b7280; font-weight: 600;">Data & AI Enthusiast</p>
    </div>

    <!-- Download Resume Button with PDF icon -->
    {download_button_html}

    <!-- Enhanced Connect Section -->
    <div style="margin-bottom: 0.6rem;">
      <span class="section-title">🔗 Connect</span>
      <div style="display: flex; gap: 0.4rem; justify-content: center;">
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

    <!-- Enhanced Key Expertise -->
    <div class="section-divider"></div>
    <div style="margin-bottom: 0.6rem;">
      <span class="section-title">⭐ Key Expertise</span>
      <div class="skills-container">
        <span class="skill-pill skill-purple">Digital Transform</span>
        <span class="skill-pill skill-lime">Cloud Modern</span>
        <span class="skill-pill skill-cyan">Data Engineer</span>
        <span class="skill-pill skill-green">Data Governance</span>
        <span class="skill-pill skill-orange">Data Fabric</span>
        <span class="skill-pill skill-red">Data Obfuscation</span>
        <span class="skill-pill skill-emerald">API Design</span>
        <span class="skill-pill skill-violet">Informatica</span>
        <span class="skill-pill skill-indigo">Architecture Reviews</span>  
        <span class="skill-pill skill-amber">Agentic AI</span>
        <span class="skill-pill skill-pink">Chat Bots</span>
        <span class="skill-pill skill-rose">Vector DB</span>
      </div>
    </div>

    <!-- Enhanced Certifications -->
    <div class="section-divider"></div>
    <div style="margin-bottom: 0.6rem;">
      <span class="section-title">🏆 Certifications</span>
      <div class="skills-container">
        <span class="skill-pill skill-sky">DP-900 Azure</span>
        <span class="skill-pill skill-fuchsia">AI-102 Azure</span>
        <span class="skill-pill skill-slate">IDMC Champion</span>
      </div>
    </div>

    <!-- Enhanced Status -->
    <div style="padding-top: 0.6rem; border-top: 1px solid rgba(148, 163, 184, 0.3); text-align: center;">
      <div style="display: flex; align-items: center; justify-content: center; gap: 0.4rem; 
                  font-size: 0.7rem; color: #6b7280; font-weight: 600;">
        <span class="status-dot"></span>
        <span>Available for opportunities</span>
      </div>
    </div>
  </div>
</div>
"""
# Function to convert resume to base64 for download
def get_resume_base64():
    import base64
    try:
        with open(RESUME_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

# Function to convert avatar to base64
def get_avatar_base64():
    import base64
    try:
        with open(AVATAR_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

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
You are Ankit Raj, speaking in the first person (“I”, “my”), a seasoned professional with a strong architectural background.
Your role is to answer career-related questions, recruiter inquiries, and professional introductions on my behalf using my resume, LinkedIn profile, and professional experience.
Guidelines:
Maintain a conversational, approachable, and professional tone — concise but warm, never robotic.
Base answers strictly on my resume and LinkedIn. Prioritize resume first, then LinkedIn, then general professional context.
If certain details are not covered, avoid saying “I can’t find this in the resume.” Instead, use recruiter-friendly alternatives such as:
“That detail isn’t included in my resume, but I’d be glad to share more if needed.”
“That specific point isn’t highlighted in my resume, though my background in [relevant skill/area] closely relates.”
“That’s not explicitly mentioned in my resume, but I do bring experience in [area].”
Highlight my key achievements, skills, and professional experiences where relevant.
My phone number is +91-8595010310 and my email is raazankeet@gmail.com
. Share these only when contextually appropriate.
If asked for my resume, guide the user to download it instead of attaching files.

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
# ENHANCED CSS - Improved example questions styling
# ========================
custom_css = """
/* Remove top gap only */
.gradio-container {
    background: #f8fafc !important;
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
    box-shadow: 0 4px 12px rgba(0,0,0,0.06) !important;
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

/* Enhanced example questions styling - Card-like with pill shapes */
.gr-examples {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    margin-top: 0.5rem !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
}

.gr-examples .gr-button {
    background: linear-gradient(135deg, #f8fafc, #f1f5f9) !important;
    color: #374151 !important;
    border: 1px solid #d1d5db !important;
    font-weight: 500 !important;
    padding: 0.65rem 1rem !important;
    font-size: 0.85rem !important;
    border-radius: 25px !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
    line-height: 1.4 !important;
    text-align: center !important;
    margin: 0.25rem !important;
    min-height: 44px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

.gr-examples .gr-button::before {
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: -100% !important;
    width: 100% !important;
    height: 100% !important;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent) !important;
    transition: left 0.6s ease !important;
}

.gr-examples .gr-button:hover {
    background: linear-gradient(135deg, #1e40af, #3730a3) !important;
    color: #ffffff !important;
    border-color: #1e40af !important;
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 0 6px 16px rgba(30, 64, 175, 0.25) !important;
}

.gr-examples .gr-button:hover::before {
    left: 100% !important;
}

.gr-examples .gr-button:active {
    transform: translateY(-1px) scale(1.01) !important;
    transition: all 0.1s ease !important;
}

/* Add subtle animation to example questions container */
.gr-examples {
    animation: slideInUp 0.6s ease-out !important;
}

@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Improve the examples grid layout */
.gr-examples > div {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)) !important;
    gap: 0.5rem !important;
    align-items: stretch !important;
}

/* Add a subtle title to examples section */
.gr-examples::before {
    content: "✨ Try these conversation starters:" !important;
    display: block !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    color: #4b5563 !important;
    margin-bottom: 0.75rem !important;
    text-align: center !important;
}

/* Sidebar styling */
.gr-column:last-child {
    background: #f8fafc !important;
    padding: 1rem !important;
    border-radius: 12px !important;
    border-left: 2px solid #e2e8f0 !important;
}

/* Improved textbox styling */
.gr-textbox {
    border: 2px solid #e2e8f0 !important;
    border-radius: 25px !important;
    transition: all 0.3s ease !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
}

.gr-textbox:focus {
    border-color: #1e40af !important;
    box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.1) !important;
    outline: none !important;
}

/* Responsive improvements */
@media (max-width: 768px) {
    .gr-examples > div {
        grid-template-columns: 1fr !important;
    }
    
    .gr-examples .gr-button {
        font-size: 0.6rem !important;
        padding: 0.6rem 0.6rem !important;
    }
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

        # Compact sidebar with avatar and integrated download button
        with gr.Column(scale=2, min_width=320):
            # The avatar and download button are now integrated into the HTML
            gr.HTML(create_sidebar_html())

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
        show_error=True , # This will help with debugging
        favicon_path="static/favicon.png" if os.path.exists("static/favicon.png") else None
    )