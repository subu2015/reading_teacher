import streamlit as st
import os
from datetime import datetime
import json
from story_generator import StoryGenerator
from speech_engine import SpeechRecognitionEngine, WordHighlighter
from assessment_engine import AssessmentEngine
import glob

class ReadingTeacherApp:
    def __init__(self):
        st.set_page_config(
            page_title="Reading Teacher",
            page_icon="📚",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Initialize components
        self.story_generator = StoryGenerator()
        self.speech_engine = SpeechRecognitionEngine()
        self.word_highlighter = WordHighlighter()
        self.assessment_engine = AssessmentEngine()
        
        # Initialize session state
        self.initialize_session_state()
        
        # Load assessment data
        self.assessment_engine.load_assessment_data()
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if "current_story" not in st.session_state:
            st.session_state.current_story = None
        if "current_page" not in st.session_state:
            st.session_state.current_page = 0
        if "reading_mode" not in st.session_state:
            st.session_state.reading_mode = "manual"  # manual, speech
        if "user_type" not in st.session_state:
            st.session_state.user_type = "child"  # child, parent
        if "reading_level" not in st.session_state:
            st.session_state.reading_level = "beginner"
        if "session_id" not in st.session_state:
            st.session_state.session_id = datetime.now().isoformat()
        if "rewards" not in st.session_state:
            st.session_state.rewards = {
                "stars": 0,
                "badges": [],
                "streak": 0
            }
    
    def main(self):
        """Main application interface"""
        # Header
        st.title("📚 Reading Teacher")
        st.markdown("### Your AI-powered reading adventure! 🚀")
        
        # User type selector
        col1, col2 = st.columns([1, 4])
        with col1:
            user_type = st.selectbox(
                "I am a:",
                ["child", "parent"],
                index=0 if st.session_state.user_type == "child" else 1
            )
            st.session_state.user_type = user_type
        
        # Show pending story editor if needed
        if st.session_state.get("show_pending_story_editor", False):
            self.pending_story_line_editor()
            return
        
        # Main content based on user type
        if user_type == "child":
            self.child_interface()
        else:
            self.parent_interface()
    
    def child_interface(self):
        """Child-friendly reading interface"""
        # Sidebar for child
        with st.sidebar:
            st.header("🎯 My Reading Journey")
            
            # Reading level
            level = st.selectbox(
                "Reading Level:",
                ["beginner", "intermediate", "advanced"],
                index=["beginner", "intermediate", "advanced"].index(st.session_state.reading_level)
            )
            st.session_state.reading_level = level
            
            # Rewards display
            st.subheader("🏆 My Rewards")
            st.metric("⭐ Stars", st.session_state.rewards["stars"])
            st.metric("🔥 Streak", st.session_state.rewards["streak"])
            
            if st.session_state.rewards["badges"]:
                st.write("🏅 Badges:")
                for badge in st.session_state.rewards["badges"]:
                    st.write(f"  {badge}")
            
            # Quick actions
            st.subheader("🎮 Quick Actions")
            if st.button("🎨 New Story"):
                st.session_state.show_new_story_form = True
            
            # Load existing story
            story_files = glob.glob('stories/*.json')
            story_files = [os.path.basename(f) for f in story_files]
            if story_files:
                selected_story = st.selectbox("📂 Load Existing Story:", ["(Select a story)"] + story_files)
                if selected_story != "(Select a story)":
                    if st.button("📖 Load Story"):
                        story = self.story_generator.load_story_from_file(selected_story)
                        if story:
                            self.story_generator.save_story_to_session(story)
                            st.success(f"Loaded story: {story['title']}")
                            st.rerun()
            
            if st.button("📊 My Progress"):
                st.session_state.show_progress = True
        
        # Show new story form if requested
        if st.session_state.get("show_new_story_form", False):
            self.new_story_form()
            return
        
        # Main content tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📖 Read Story", "🎮 Word Games", "📊 My Progress", "🏠 Home"])
        
        with tab1:
            self.story_reading_interface()
        
        with tab2:
            self.word_games_interface()
        
        with tab3:
            self.child_progress_interface()
        
        with tab4:
            self.home_interface()
    
    def story_reading_interface(self):
        """Story reading interface with speech recognition"""
        st.header("�� Read Your Story")
        # Story Line Editor button
        if st.button("✏️ Edit Story Lines"):
            st.session_state.show_story_editor = True
        if st.session_state.get("show_story_editor", False):
            self.story_line_editor()
            return
        if not st.session_state.current_story:
            st.info("🎨 Click 'New Story' in the sidebar to start your reading adventure!")
            return
        
        story = st.session_state.current_story
        current_page = st.session_state.current_page
        total_pages = len(story["pages"])
        
        if current_page >= total_pages:
            st.success("🎉 Congratulations! You finished the story!")
            self.complete_story_session()
            return
        
        # Get current page
        page = story["pages"][current_page]
        
        # Story page display
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Story illustration
            if page.get("illustration_url"):
                illustration_url = page["illustration_url"]
                if os.path.exists(illustration_url):
                    st.image(illustration_url, use_container_width=True)
                else:
                    st.image(illustration_url, use_container_width=True)
            else:
                st.info("🎨 Illustration loading...")
        
        with col2:
            # Story text with word highlighting
            st.subheader(f"Page {current_page + 1} of {total_pages}")
            
            # Display text with word highlighting
            text = page["text"]
            highlighted_text = self.word_highlighter.highlight_word_in_text(text, -1)  # No highlighting initially
            st.markdown(f"<div style='font-size: 24px; line-height: 1.5;'>{highlighted_text}</div>", unsafe_allow_html=True)
            
            # Reading controls
            st.subheader("🎤 Reading Options")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🎤 Start Reading", type="primary"):
                    self.start_speech_reading(text)
            
            with col_b:
                if st.button("🔊 Hear Word"):
                    self.play_word_pronunciation(text)
            
            # Navigation
            st.subheader("📄 Navigation")
            nav_col1, nav_col2, nav_col3 = st.columns(3)
            
            with nav_col1:
                if st.button("⬅️ Previous") and current_page > 0:
                    st.session_state.current_page -= 1
                    st.rerun()
            
            with nav_col2:
                st.write(f"Page {current_page + 1}")
            
            with nav_col3:
                if st.button("➡️ Next") and current_page < total_pages - 1:
                    st.session_state.current_page += 1
                    st.rerun()
    
    def start_speech_reading(self, text: str):
        """Start speech recognition for reading"""
        st.info("🎤 Listening... Read the text aloud!")
        
        # Adjust for ambient noise
        self.speech_engine.adjust_for_ambient_noise()
        
        # Listen for speech
        audio = self.speech_engine.listen_for_speech(timeout=10)
        
        if audio:
            # Transcribe audio
            spoken_text = self.speech_engine.transcribe_audio(audio)
            
            if spoken_text:
                st.success(f"🎤 You said: '{spoken_text}'")
                
                # Analyze reading performance
                alignment = self.speech_engine.align_words_with_text(spoken_text, text)
                performance = self.speech_engine.analyze_reading_performance(alignment, 10.0)  # Assume 10 seconds
                
                # Track word mastery
                self.speech_engine.track_word_mastery(alignment)
                
                # Display results
                self.display_reading_results(performance, alignment)
                
                # Award points
                self.award_points(performance["accuracy"])
            else:
                st.error("😕 I couldn't hear you clearly. Try again!")
        else:
            st.warning("⏰ No speech detected. Try reading aloud!")
    
    def display_reading_results(self, performance: dict, alignment: dict):
        """Display reading performance results"""
        st.subheader("📊 Reading Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Accuracy", f"{performance['accuracy']:.1f}%")
        
        with col2:
            st.metric("Speed", f"{performance['words_per_minute']:.1f} WPM")
        
        with col3:
            st.metric("Fluency", f"{performance['fluency_score']:.1f}%")
        
        # Show mistakes if any
        if alignment["incorrect_words"]:
            st.warning("📝 Words to practice:")
            for mistake in alignment["incorrect_words"]:
                st.write(f"  • '{mistake['word']}' (you said: '{mistake['spoken']}')")
        
        # Encouragement
        if performance["accuracy"] >= 90:
            st.success("🌟 Excellent reading! You're doing amazing!")
            st.balloons()
        elif performance["accuracy"] >= 70:
            st.info("👍 Good job! Keep practicing!")
        else:
            st.info("💪 Keep trying! Reading takes practice!")
    
    def award_points(self, accuracy: float):
        """Award points based on reading performance"""
        points = int(accuracy / 10)  # 1 point per 10% accuracy
        st.session_state.rewards["stars"] += points
        st.session_state.rewards["streak"] += 1
        
        st.success(f"⭐ You earned {points} stars! Total: {st.session_state.rewards['stars']}")
    
    def play_word_pronunciation(self, text: str):
        """Play word pronunciation (placeholder)"""
        st.info("🔊 Word pronunciation feature coming soon!")
    
    def create_new_story(self):
        """Create a new story"""
        st.info("🎨 Creating your special story...")
        
        # Story theme selection
        theme = st.selectbox(
            "Choose a story theme:",
            ["adventure", "animals", "space", "fairy tale", "nature", "friendship"]
        )
        
        # Generate story
        story = self.story_generator.create_complete_story(st.session_state.reading_level, theme)
        
        if story:
            self.story_generator.save_story_to_session(story)
            st.success(f"🎉 Your story '{story['title']}' is ready!")
            st.rerun()
        else:
            st.error("😕 Sorry, I couldn't create a story right now. Try again!")
    
    def word_games_interface(self):
        """Word games interface"""
        st.header("🎮 Word Games")
        st.info("🎮 Word games coming soon! Practice your reading skills with fun games!")
    
    def child_progress_interface(self):
        """Child-friendly progress interface"""
        st.header("📊 My Reading Progress")
        
        if "reading_performance" in st.session_state:
            performance = st.session_state.reading_performance
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Words Mastered", len(performance.get("words_read", {})))
            
            with col2:
                st.metric("Reading Sessions", len(self.assessment_engine.assessment_data["reading_sessions"]))
            
            with col3:
                st.metric("Current Streak", st.session_state.rewards["streak"])
        else:
            st.info("📚 Start reading to see your progress!")
    
    def home_interface(self):
        """Home interface for children"""
        st.header("🏠 Welcome to Reading Teacher!")
        
        st.markdown("""
        ### 👋 Hello, young reader!
        
        I'm here to help you become an amazing reader! Here's what we can do together:
        
        📖 **Read Stories** - Beautiful stories with pictures just for you!
        🎮 **Play Games** - Fun word games to practice reading
        📊 **See Progress** - Watch yourself get better at reading
        🏆 **Earn Rewards** - Collect stars and badges for your hard work!
        
        ### 🎯 Ready to start?
        Click on "Read Story" to begin your reading adventure!
        """)
        
        if st.session_state.rewards["stars"] > 0:
            st.success(f"🌟 You have {st.session_state.rewards['stars']} stars! Keep up the great work!")
    
    def parent_interface(self):
        """Parent dashboard interface"""
        st.header("👨‍👩‍👧‍👦 Parent Dashboard")
        
        # Generate parent report
        report = self.assessment_engine.generate_parent_report()
        
        if "message" in report:
            st.info(report["message"])
            return
        
        # Summary metrics
        st.subheader("📊 Reading Summary")
        summary = report["summary"]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Sessions", summary["total_sessions"])
        
        with col2:
            st.metric("Reading Level", summary["current_reading_level"].title())
        
        with col3:
            st.metric("Average Accuracy", f"{summary['average_accuracy']}%")
        
        with col4:
            st.metric("Average Speed", f"{summary['average_speed']} WPM")
        
        # Progress charts
        st.subheader("📈 Progress Over Time")
        charts = report["charts"]
        
        if charts:
            tab1, tab2, tab3, tab4 = st.tabs(["Accuracy", "Speed", "Fluency", "Words Mastered"])
            
            with tab1:
                st.plotly_chart(charts["accuracy"], use_container_width=True)
            
            with tab2:
                st.plotly_chart(charts["wpm"], use_container_width=True)
            
            with tab3:
                st.plotly_chart(charts["fluency"], use_container_width=True)
            
            with tab4:
                st.plotly_chart(charts["mastered"], use_container_width=True)
        
        # Word mastery report
        st.subheader("📚 Word Mastery")
        word_report = report["word_mastery"]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Words", word_report["total_words"])
        
        with col2:
            st.metric("Mastered Words", word_report["mastered_words"])
        
        with col3:
            st.metric("Need Practice", word_report["needs_practice"])
        
        # Recommendations
        st.subheader("💡 Recommendations")
        recommendations = report["recommendations"]
        
        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec}")
    
    def complete_story_session(self):
        """Complete a story reading session"""
        if not st.session_state.current_story:
            return
        
        # Save session data
        session_data = {
            "session_id": st.session_state.session_id,
            "timestamp": datetime.now().isoformat(),
            "reading_level": st.session_state.reading_level,
            "story_title": st.session_state.current_story["title"],
            "performance": self.speech_engine.reading_performance,
            "words_read": self.speech_engine.reading_performance["words_read"]
        }
        
        # Analyze session
        session_analysis = self.assessment_engine.analyze_reading_session(session_data)
        
        # Track progress
        self.assessment_engine.track_progress_over_time(session_analysis)
        
        # Save to session state
        self.assessment_engine.save_assessment_data()
        
        st.success("🎉 Story completed! Great job reading!")
        st.balloons()

    def story_line_editor(self):
        """Show an editor for all story lines and illustration prompts, indexed by page number."""
        story = st.session_state.current_story
        st.subheader("📝 Story Line Editor")
        edited = False
        for i, page in enumerate(story["pages"]):
            st.markdown(f"**Page {i+1}:**")
            new_text = st.text_area(f"Story Text (Page {i+1})", value=page["text"], key=f"edit_text_{i}")
            new_prompt = st.text_area(f"Illustration Prompt (Page {i+1})", value=page.get("illustration_prompt", ""), key=f"edit_prompt_{i}")
            if new_text != page["text"] or new_prompt != page.get("illustration_prompt", ""):
                page["text"] = new_text
                page["illustration_prompt"] = new_prompt
                edited = True
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Edits"):
                self.story_generator.save_story_to_session(story)
                self.story_generator.save_story_to_file(story)
                st.success("Story edits saved!")
                st.session_state.show_story_editor = False
                st.rerun()
        with col2:
            if st.button("🎨 Re-generate Images (New Version)"):
                new_story = self.story_generator.regenerate_images_for_story(story)
                self.story_generator.save_story_to_session(new_story)
                st.success("Images re-generated and saved as a new version!")
                st.session_state.show_story_editor = False
                st.rerun()
        if st.button("❌ Close Editor"):
            st.session_state.show_story_editor = False
            st.rerun()

    def new_story_form(self):
        """Interactive form for new story creation: theme, genre, and custom outline."""
        st.header("🎨 Create a New Story")
        with st.form("new_story_form"):
            themes = ["space", "unicorn", "disney world", "saturn", "number blocks"]
            genres = ["adventure", "mystery", "friendship", "fantasy", "silly", "educational"]
            theme = st.selectbox("Choose a story theme:", themes)
            genre = st.selectbox("Choose a story genre:", genres)
            user_outline = st.text_area("Chat with the AI: What should your story be about? (Optional)", "")
            submitted = st.form_submit_button("Generate Story Outline!")
        if submitted:
            st.session_state.show_new_story_form = False
            # Generate only the outline, not images or saving yet
            outline = self.story_generator.generate_story_outline(
                st.session_state.reading_level,
                theme=theme,
                genre=genre,
                user_outline=user_outline
            )
            if outline:
                st.session_state.pending_story_outline = outline
                st.session_state.show_pending_story_editor = True
                st.rerun()
            else:
                st.error("😕 Sorry, I couldn't create a story outline right now. Try again!")

    def pending_story_line_editor(self):
        """Show the story line editor for a pending new story outline before images are generated."""
        story = st.session_state.pending_story_outline
        st.subheader("📝 Review and Edit Your Story Outline")
        for i, page in enumerate(story["pages"]):
            st.markdown(f"**Page {i+1}:**")
            new_text = st.text_area(f"Story Text (Page {i+1})", value=page["text"], key=f"pending_edit_text_{i}")
            new_prompt = st.text_area(f"Illustration Prompt (Page {i+1})", value=page.get("illustration_prompt", ""), key=f"pending_edit_prompt_{i}")
            page["text"] = new_text
            page["illustration_prompt"] = new_prompt
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Accept and Generate Images"):
                # Now save and generate images
                final_story = self.story_generator.create_complete_story(
                    story["reading_level"],
                    theme=story["theme"],
                    genre=story.get("genre", ""),
                    user_outline=""
                )
                if final_story:
                    self.story_generator.save_story_to_session(final_story)
                    st.success(f"🎉 Your story '{final_story['title']}' is ready!")
                    st.session_state.show_pending_story_editor = False
                    st.session_state.pending_story_outline = None
                    st.rerun()
                else:
                    st.error("😕 Sorry, I couldn't create the full story right now. Try again!")
        with col2:
            if st.button("❌ Cancel"):
                st.session_state.show_pending_story_editor = False
                st.session_state.pending_story_outline = None
                st.rerun()

if __name__ == "__main__":
    app = ReadingTeacherApp()
    app.main() 