import streamlit as st
import os
from openai import OpenAI
import json
from typing import List, Dict, Tuple
import base64
from PIL import Image
import io
from dotenv import load_dotenv
import requests
import re

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
    
    def generate_story_outline(self, reading_level: str, theme: str = "adventure", genre: str = None, user_outline: str = None) -> Dict | None:
        """Generate a story outline with controlled vocabulary"""
        # Check if API key is set
        if not self.openai_api_key:
            st.error("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
            return None
            
        level_words = self.vocabulary_levels[reading_level]
        
        genre_str = f"- Genre: {genre or ''}" if genre else ""
        user_outline_str = f"- User outline: {user_outline or ''}" if user_outline else ""
        
        prompt = f"""
        Create a short story outline for a 5-year-old child at {reading_level} reading level.
        
        Requirements:
        - Use primarily these words: {', '.join(level_words[:10])}
        - Theme: {theme}
        {genre_str}
        {user_outline_str}
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
    
    def save_story_to_file(self, story: Dict):
        """Save the story as a JSON file in the 'stories' folder, named after the story title."""
        if not os.path.exists('stories'):
            os.makedirs('stories')
        title = story.get('title', 'untitled_story')
        # Sanitize filename
        filename = ''.join(c for c in title if c.isalnum() or c in (' ', '_', '-'))
        filename = filename.replace(' ', '_').lower() + '.json'
        filepath = os.path.join('stories', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(story, f, ensure_ascii=False, indent=2)

    def extract_main_character_and_style(self, story_outline: Dict) -> str:
        """Extract or synthesize a main character and style description for illustration consistency."""
        title = story_outline.get('title', '')
        theme = story_outline.get('theme', '')
        first_page = story_outline.get('pages', [{}])[0]
        first_text = first_page.get('text', '')
        # Synthesize a consistent style/character description
        desc = f"The main character(s) and style should be consistent across all images. If the story is about a specific animal, child, or object, use the same appearance, color palette, and style throughout. For example, if the story is about a cat, use the same cat in every image.\nStory Title: {title}\nTheme: {theme}\nFirst Page: {first_text}"
        return desc

    def create_complete_story(self, reading_level: str, theme: str = "adventure", genre: str = "", user_outline: str = "") -> Dict | None:
        """Generate a complete story with illustrations and save images locally"""
        st.info("🎨 Creating your special story...")
        # Generate story outline
        with st.spinner("📝 Writing your story..."):
            story_outline = self.generate_story_outline(reading_level, theme, genre or "", user_outline or "")
            if not story_outline:
                return None
        # Save story before generating images
        self.save_story_to_file(story_outline)
        # Prepare image save directory
        title = story_outline.get('title', 'untitled_story')
        story_dir = os.path.join('stories', ''.join(c for c in title if c.isalnum() or c in (' ', '_', '-')).replace(' ', '_').lower())
        if not os.path.exists(story_dir):
            os.makedirs(story_dir)
        # Extract main character/style description for consistency
        style_desc = self.extract_main_character_and_style(story_outline)
        # Generate illustrations for each page and save locally
        with st.spinner("🎨 Creating beautiful illustrations..."):
            for page in story_outline["pages"]:
                # Prepend style/character description to each prompt
                illustration_prompt = f"{style_desc}\nPage Description: {page['illustration_prompt']}"
                illustration_url = self.generate_illustration(
                    illustration_prompt,
                    page["page_number"]
                )
                page["illustration_url"] = illustration_url
                # Download and save image
                if illustration_url:
                    img_path = os.path.join(story_dir, f"page_{page['page_number']}.png")
                    try:
                        response = requests.get(illustration_url)
                        if response.status_code == 200:
                            with open(img_path, 'wb') as img_file:
                                img_file.write(response.content)
                            # Update the page to point to the local image
                            page["illustration_url"] = img_path
                    except Exception as e:
                        st.warning(f"Could not save image for page {page['page_number']}: {e}")
        # Save updated story with local image paths
        self.save_story_to_file(story_outline)
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
    
    def get_story_page(self, page_number: int) -> Dict | None:
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

    def load_story_from_file(self, filename: str) -> Dict | None:
        """Load a story from a JSON file in the 'stories' folder."""
        filepath = os.path.join('stories', filename)
        if not os.path.exists(filepath):
            st.error(f"Story file '{filename}' not found.")
            return None
        with open(filepath, 'r', encoding='utf-8') as f:
            story = json.load(f)
        return story

    def regenerate_images_for_story(self, story: Dict) -> Dict:
        """Regenerate images for the story, saving them as a new version in the story's directory."""
        title = story.get('title', 'untitled_story')
        story_dir = os.path.join('stories', ''.join(c for c in title if c.isalnum() or c in (' ', '_', '-')).replace(' ', '_').lower())
        # Find next version number
        existing_versions = [d for d in os.listdir(story_dir) if re.match(r'^v\\d+$', d)] if os.path.exists(story_dir) else []
        if existing_versions:
            next_version = max([int(d[1:]) for d in existing_versions]) + 1
        else:
            next_version = 2
        version_dir = os.path.join(story_dir, f'v{next_version}')
        os.makedirs(version_dir, exist_ok=True)
        # Extract main character/style description for consistency
        style_desc = self.extract_main_character_and_style(story)
        # Generate new images and update illustration_url
        for page in story["pages"]:
            illustration_prompt = f"{style_desc}\nPage Description: {page['illustration_prompt']}"
            illustration_url = self.generate_illustration(
                illustration_prompt,
                page["page_number"]
            )
            # Download and save image
            img_path = os.path.join(version_dir, f"page_{page['page_number']}.png")
            if illustration_url:
                try:
                    response = requests.get(illustration_url)
                    if response.status_code == 200:
                        with open(img_path, 'wb') as img_file:
                            img_file.write(response.content)
                        page["illustration_url"] = img_path
                except Exception as e:
                    st.warning(f"Could not save image for page {page['page_number']}: {e}")
        # Save updated story as a new versioned JSON file
        versioned_json = os.path.join(story_dir, f'story_v{next_version}.json')
        with open(versioned_json, 'w', encoding='utf-8') as f:
            json.dump(story, f, ensure_ascii=False, indent=2)
        return story

if __name__ == "__main__":
    # Test the story generator
    generator = StoryGenerator()
    story = generator.create_complete_story("beginner", "space adventure")
    if story:
        print(f"Generated story: {story['title']}")
        print(f"Pages: {len(story['pages'])}") 