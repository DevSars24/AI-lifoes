from typing import Dict, Any
import google.generativeai as genai
from app.core.config import config
from loguru import logger
import re

# Configure Gemini API
genai.configure(api_key=config.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

class GeminiService:

    @staticmethod
    async def generate_learning_suggestion(user_input: str) -> Dict[str, Any]:
        """
        Generate a complete learning suggestion with everything in one field.
        """
        try:
            prompt = (
                f"""You are a Go learning expert. Create a complete learning suggestion for: "{user_input}"

Include:
- Topic name  
- Detailed explanation (why important, key concepts)
- 2-3 YouTube video resources WITH DIRECT LINKS

Format as clean Markdown:
---
## Learning Topic: [Name]

### Explanation:
[Detailed explanation...]

### Video Resources:
1. **[Title]**
   https://www.youtube.com/watch?v=VIDEO_ID
   
2. **[Title]**
   https://www.youtube.com/watch?v=VIDEO_ID
   
3. **[Title]**
   https://www.youtube.com/watch?v=VIDEO_ID
---
"""
            )
            
            response = model.generate_content(prompt)
            result_text = response.text.strip() if response.text else ""
            
            # Extract VALID YouTube links
            youtube_links = extract_youtube_links(result_text)
            logger.info(f"Found {len(youtube_links)} valid YouTube links")
            
            # Add links to the suggestion (for display)
            if youtube_links:
                links_section = "\n\n### Extracted Links:\n" + "\n".join([f"- {link}" for link in youtube_links[:3]])
                result_text += links_section
            
            return {"suggestion": result_text, "resources": youtube_links}

        except Exception as e:
            logger.error(f"Gemini generate_learning_suggestion failed: {e}")
            return {"suggestion": "", "resources": []}


def extract_youtube_links(text: str) -> list[str]:
    """Extract VALID YouTube links from text"""
    links = []
    
    # Pattern 1: Full YouTube URLs
    full_urls = re.findall(r'https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})', text)
    for video_id in full_urls:
        links.append(f"https://www.youtube.com/watch?v={video_id}")
    
    # Pattern 2: Links after "Link:" or standalone URLs
    link_texts = re.findall(r'(?:Link:\s*|https?://[^\s\n]+)', text, re.IGNORECASE)
    for link_text in link_texts:
        # Fix common issues
        fixed_link = link_text.strip().replace('https//', 'https://')
        
        # Validate YouTube URL
        if re.match(r'https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[a-zA-Z0-9_-]{11}', fixed_link):
            links.append(fixed_link)
    
    # Remove duplicates and limit to 3
    unique_links = list(dict.fromkeys(links))[:3]
    
    return unique_links

gemini_service = GeminiService()