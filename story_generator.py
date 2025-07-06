import streamlit as st
import os
from openai import OpenAI
import json
from typing import List, Dict, Tuple
import base64
from PIL import Image
import io
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class StoryGenerator:
    def __init__(self):
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        if not self.openai_api_key:
            st.error("Please set your OpenAI API key as an environment variable: OPENAI_API_KEY")
            st.stop()
        
        self.client = OpenAI(api_key=self.openai_api_key)
        
        # Age-appropriate vocabulary levels
        self.vocabulary_levels = {
            "beginner": ["cat", "dog", "hat", "run", "big", "red", "sun", "fun", "map", "top", "see", "the", "a", "is", "in", "on", "at", "to", "and", "of"],
            "intermediate": ["house", "tree", "book", "play", "walk", "jump", "sing", "read", "write", "draw", "happy", "sad", "good", "bad", "fast", "slow", "hot", "cold", "new", "old"],
            "advanced": ["beautiful", "wonderful", "amazing", "exciting", "adventure", "journey", "discover", "explore", "imagine", "create", "celebrate", "friendship", "kindness", "bravery", "wisdom"]
        }
    
    def generate_story_outline(self, reading_level: str, theme: str = "adventure") -> Dict | None:
        """Generate a story outline with controlled vocabulary"""
        # Check if API key is set
        if not self.openai_api_key:
            st.error("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
            return None
            
        level_words = self.vocabulary_levels[reading_level]
        
        prompt = f"""
        Create a short story outline for a 5-year-old child at {reading_level} reading level.
        
        Requirements:
        - Use primarily these words: {', '.join(level_words[:10])}
        - Theme: {theme}
        - Story should be about 15 pages long
        - Each page should have 1-2 simple sentences
        - Include repetition of key words for practice
        - Make it engaging and fun
        
        Return the outline as JSON with this structure:
        {{
            "title": "Story Title",
            "theme": "{theme}",
            "reading_level": "{reading_level}",
            "pages": [
                {{
                    "page_number": 1,
                    "text": "Simple sentence here.",
                    "key_words": ["word1", "word2"],
                    "illustration_prompt": "Description for DALL-E to create child-friendly illustration"
                }}
            ]
        }}
        
        IMPORTANT: Return ONLY valid JSON, no additional text or explanations.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Get the response content
            response_content = response.choices[0].message.content.strip()
            
            # Debug: Print the response to see what we're getting
            # st.write("Debug - API Response:", response_content)
            
            # Check if response is empty
            if not response_content:
                st.error("Received empty response from OpenAI API")
                return None
            
            # Try to parse JSON
            try:
                # First, try to parse as-is
                story_outline = json.loads(response_content)
                return story_outline
            except json.JSONDecodeError:
                # If that fails, try to extract JSON from markdown code blocks
                try:
                    # Remove markdown code block formatting
                    if response_content.startswith('```json'):
                        response_content = response_content[7:]  # Remove ```json
                    if response_content.startswith('```'):
                        response_content = response_content[3:]  # Remove ```
                    if response_content.endswith('```'):
                        response_content = response_content[:-3]  # Remove trailing ```
                    
                    # Clean up any extra whitespace
                    response_content = response_content.strip()
                    
                    # Try parsing again
                    story_outline = json.loads(response_content)
                    return story_outline
                except json.JSONDecodeError as json_error:
                    st.error(f"Invalid JSON response: {json_error}")
                    st.write("Raw response:", response_content)
                    return None
            
        except Exception as e:
            st.error(f"Error generating story outline: {e}")
            st.write("Full error details:", str(e))
            return None
    
    def generate_illustration(self, prompt: str, page_number: int) -> str | None:
        """Generate a child-friendly illustration for a story page"""
        enhanced_prompt = f"""
        Create a child-friendly, colorful illustration for a children's book page.
        
        Scene: {prompt}
        
        Style requirements:
        - Bright, cheerful colors
        - Simple, clear shapes
        - Cute, friendly characters
        - Safe, age-appropriate content
        - Storybook illustration style
        - No text or words in the image
        - Suitable for 5-year-old children
        
        Make it engaging and fun!
        """
        
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=enhanced_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url
            return image_url
            
        except Exception as e:
            st.error(f"Error generating illustration: {e}")
            return None
    
    def create_complete_story(self, reading_level: str, theme: str = "adventure") -> Dict | None:
        """Generate a complete story with illustrations"""
        st.info("🎨 Creating your special story...")
        
        # Generate story outline
        with st.spinner("📝 Writing your story..."):
            story_outline = self.generate_story_outline(reading_level, theme)
            if not story_outline:
                return None
        
        # Generate illustrations for each page
        with st.spinner("🎨 Creating beautiful illustrations..."):
            for page in story_outline["pages"]:
                illustration_url = self.generate_illustration(
                    page["illustration_prompt"], 
                    page["page_number"]
                )
                page["illustration_url"] = illustration_url
        
        return story_outline
    
    def save_story_to_session(self, story: Dict):
        """Save the generated story to session state"""
        st.session_state["current_story"] = story
        st.session_state["current_page"] = 0
        st.session_state["story_progress"] = {
            "words_read": {},
            "mistakes": [],
            "reading_time": 0,
            "completed": False
        }
    
    def get_story_page(self, page_number: int) -> Dict:
        """Get a specific page from the current story"""
        if "current_story" not in st.session_state:
            return None
        
        story = st.session_state["current_story"]
        if 0 <= page_number < len(story["pages"]):
            return story["pages"][page_number]
        return None
    
    def get_total_pages(self) -> int:
        """Get the total number of pages in the current story"""
        if "current_story" not in st.session_state:
            return 0
        return len(st.session_state["current_story"]["pages"])

if __name__ == "__main__":
    # Test the story generator
    generator = StoryGenerator()
    story = generator.create_complete_story("beginner", "space adventure")
    if story:
        print(f"Generated story: {story['title']}")
        print(f"Pages: {len(story['pages'])}") 