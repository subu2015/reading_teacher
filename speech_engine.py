import streamlit as st
import speech_recognition as sr
import whisper
import time
import json
from typing import List, Dict, Tuple
import threading
import queue
import numpy as np
from datetime import datetime

class SpeechRecognitionEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize Whisper model for better accuracy
        try:
            self.whisper_model = whisper.load_model("base")
        except Exception as e:
            st.warning(f"Whisper model not loaded: {e}")
            self.whisper_model = None
        
        # Reading performance tracking
        self.current_text = ""
        self.words_in_text = []
        self.reading_performance = {
            "words_read": {},
            "mistakes": [],
            "hesitations": [],
            "reading_speed": 0,
            "accuracy": 0,
            "fluency_score": 0
        }
        
        # Audio processing queue
        self.audio_queue = queue.Queue()
        self.is_listening = False
    
    def adjust_for_ambient_noise(self):
        """Adjust microphone for ambient noise"""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
    
    def listen_for_speech(self, timeout=5):
        """Listen for speech input"""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            return audio
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            st.error(f"Error listening for speech: {e}")
            return None
    
    def transcribe_audio(self, audio) -> str:
        """Transcribe audio using multiple methods for better accuracy"""
        transcriptions = []
        
        # Try Google Speech Recognition
        try:
            text = self.recognizer.recognize_google(audio)
            transcriptions.append(text.lower())
        except Exception as e:
            pass
        
        # Try Whisper if available
        if self.whisper_model:
            try:
                # Convert audio to format Whisper can process
                audio_data = np.frombuffer(audio.frame_data, dtype=np.int16)
                result = self.whisper_model.transcribe(audio_data)
                transcriptions.append(result["text"].lower())
            except Exception as e:
                pass
        
        # Return the best transcription
        if transcriptions:
            return transcriptions[0]
        return ""
    
    def align_words_with_text(self, spoken_text: str, target_text: str) -> Dict:
        """Align spoken words with target text for word-level tracking"""
        spoken_words = spoken_text.split()
        target_words = target_text.lower().split()
        
        alignment = {
            "correct_words": [],
            "incorrect_words": [],
            "missed_words": [],
            "extra_words": []
        }
        
        # Simple word-by-word comparison
        for i, target_word in enumerate(target_words):
            if i < len(spoken_words):
                spoken_word = spoken_words[i]
                if spoken_word == target_word:
                    alignment["correct_words"].append({
                        "word": target_word,
                        "position": i,
                        "correct": True
                    })
                else:
                    alignment["incorrect_words"].append({
                        "word": target_word,
                        "spoken": spoken_word,
                        "position": i,
                        "correct": False
                    })
            else:
                alignment["missed_words"].append({
                    "word": target_word,
                    "position": i
                })
        
        # Check for extra words
        if len(spoken_words) > len(target_words):
            for word in spoken_words[len(target_words):]:
                alignment["extra_words"].append(word)
        
        return alignment
    
    def analyze_reading_performance(self, alignment: Dict, reading_time: float) -> Dict:
        """Analyze reading performance based on word alignment"""
        total_words = len(alignment["correct_words"]) + len(alignment["incorrect_words"]) + len(alignment["missed_words"])
        correct_words = len(alignment["correct_words"])
        
        performance = {
            "accuracy": (correct_words / total_words * 100) if total_words > 0 else 0,
            "words_per_minute": (total_words / reading_time * 60) if reading_time > 0 else 0,
            "mistakes": len(alignment["incorrect_words"]),
            "missed_words": len(alignment["missed_words"]),
            "extra_words": len(alignment["extra_words"]),
            "fluency_score": self.calculate_fluency_score(alignment, reading_time),
            "timestamp": datetime.now().isoformat()
        }
        
        return performance
    
    def calculate_fluency_score(self, alignment: Dict, reading_time: float) -> float:
        """Calculate a fluency score based on accuracy and speed"""
        total_words = len(alignment["correct_words"]) + len(alignment["incorrect_words"]) + len(alignment["missed_words"])
        
        if total_words == 0 or reading_time == 0:
            return 0
        
        accuracy = len(alignment["correct_words"]) / total_words
        words_per_minute = total_words / reading_time * 60
        
        # Ideal reading speed for 5-year-olds: 20-40 words per minute
        speed_score = min(words_per_minute / 30, 1.0)  # Normalize to 30 WPM
        
        # Fluency score combines accuracy and speed
        fluency_score = (accuracy * 0.7) + (speed_score * 0.3)
        return fluency_score * 100
    
    def track_word_mastery(self, alignment: Dict):
        """Track individual word mastery for adaptive learning"""
        for word_data in alignment["correct_words"]:
            word = word_data["word"]
            if word not in self.reading_performance["words_read"]:
                self.reading_performance["words_read"][word] = {
                    "correct_count": 0,
                    "total_count": 0,
                    "mastery_level": 0
                }
            
            self.reading_performance["words_read"][word]["correct_count"] += 1
            self.reading_performance["words_read"][word]["total_count"] += 1
            
            # Calculate mastery level (0-100)
            word_stats = self.reading_performance["words_read"][word]
            word_stats["mastery_level"] = (word_stats["correct_count"] / word_stats["total_count"]) * 100
        
        # Track mistakes for words needing more practice
        for mistake in alignment["incorrect_words"]:
            word = mistake["word"]
            if word not in self.reading_performance["words_read"]:
                self.reading_performance["words_read"][word] = {
                    "correct_count": 0,
                    "total_count": 0,
                    "mastery_level": 0
                }
            
            self.reading_performance["words_read"][word]["total_count"] += 1
            word_stats = self.reading_performance["words_read"][word]
            word_stats["mastery_level"] = (word_stats["correct_count"] / word_stats["total_count"]) * 100
    
    def get_words_needing_practice(self, threshold: float = 70.0) -> List[str]:
        """Get words that need more practice based on mastery level"""
        words_needing_practice = []
        
        for word, stats in self.reading_performance["words_read"].items():
            if stats["mastery_level"] < threshold:
                words_needing_practice.append(word)
        
        return words_needing_practice
    
    def get_mastered_words(self, threshold: float = 90.0) -> List[str]:
        """Get words that are mastered based on mastery level"""
        mastered_words = []
        
        for word, stats in self.reading_performance["words_read"].items():
            if stats["mastery_level"] >= threshold:
                mastered_words.append(word)
        
        return mastered_words
    
    def reset_performance_tracking(self):
        """Reset performance tracking for a new reading session"""
        self.reading_performance = {
            "words_read": {},
            "mistakes": [],
            "hesitations": [],
            "reading_speed": 0,
            "accuracy": 0,
            "fluency_score": 0
        }
    
    def save_performance_to_session(self):
        """Save reading performance to session state"""
        if "reading_performance" not in st.session_state:
            st.session_state["reading_performance"] = {}
        
        st.session_state["reading_performance"].update(self.reading_performance)

class WordHighlighter:
    def __init__(self):
        self.current_highlighted_word = -1
        self.highlight_color = "#FFD700"  # Gold color for highlighting
    
    def highlight_word_in_text(self, text: str, word_index: int) -> str:
        """Create HTML with highlighted word"""
        words = text.split()
        
        if word_index >= len(words):
            return text
        
        highlighted_words = []
        for i, word in enumerate(words):
            if i == word_index:
                highlighted_words.append(f'<span style="background-color: {self.highlight_color}; padding: 2px 4px; border-radius: 3px;">{word}</span>')
            else:
                highlighted_words.append(word)
        
        return " ".join(highlighted_words)
    
    def reset_highlight(self):
        """Reset word highlighting"""
        self.current_highlighted_word = -1

if __name__ == "__main__":
    # Test the speech recognition engine
    engine = SpeechRecognitionEngine()
    print("Speech recognition engine initialized") 