"""Claude AI integration for resume optimization suggestions"""
import os
from app.core.config import settings

try:
    # On Python 3.14+, older anthropic versions may emit a noisy (but non-fatal)
    # warning about Pydantic v1 compat. This app runs fine in "demo mode" without
    # Claude configured, so we silence that specific warning to avoid confusion.
    import warnings

    warnings.filterwarnings(
        "ignore",
        message=r".*Core Pydantic V1 functionality isn't compatible with Python 3\.14 or greater.*",
        category=UserWarning,
        module=r"anthropic\._compat",
    )
    from anthropic import Anthropic
    CLIENT_AVAILABLE = True
except ImportError:
    CLIENT_AVAILABLE = False

def optimize_resume(resume, jd):
    """Generate AI-powered resume optimization suggestions using Claude"""
    if not CLIENT_AVAILABLE or not settings.CLAUDE_API_KEY:
        return {
            "missing_skills": ["API key not configured - demo mode"],
            "bullet_improvements": ["Enable Claude API to get AI suggestions"],
            "ats_improvements": ["Set CLAUDE_API_KEY environment variable"]
        }
    
    try:
        client = Anthropic(api_key=settings.CLAUDE_API_KEY)
        
        prompt = f"""You are an ATS Resume Optimization Expert.

Resume:
{resume}

Job Description:
{jd}

Provide suggestions in this format:
1. Missing Skills:
2. Bullet Point Improvements (3 examples):
3. ATS Alignment Tips:
"""
        
        response = client.messages.create(
            model=settings.MODEL_NAME,
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    except Exception as e:
        return f"Optimization suggestions unavailable: {str(e)}"