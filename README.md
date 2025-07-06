# 📚 Reading Teacher 2.0

An advanced AI-powered reading assistant designed specifically for 5-year-old children learning to read English. This comprehensive system combines story generation, speech recognition, adaptive learning, and detailed assessment to create a personalized reading experience.

## 🌟 Advanced Features

### 📖 AI Story Generation
- **Personalized Stories**: Generate 15-page stories with controlled vocabulary
- **AI Illustrations**: DALL-E 3 generated child-friendly illustrations for each page
- **Adaptive Content**: Stories adjust based on child's reading level and word mastery
- **Multiple Themes**: Adventure, animals, space, fairy tales, nature, friendship

### 🎤 Speech Recognition & Word Highlighting
- **Real-time Listening**: Advanced speech recognition using Whisper and Google STT
- **Word-level Tracking**: Highlight words as child reads them aloud
- **Performance Analysis**: Track accuracy, speed, and fluency in real-time
- **Gentle Corrections**: Provide encouraging feedback on mistakes

### 🧠 Adaptive Learning Engine
- **Word Mastery Tracking**: Monitor individual word performance over time
- **Personalized Difficulty**: Adjust story vocabulary based on mastered/tricky words
- **Progress Optimization**: Gradually introduce new words while reinforcing difficult ones
- **Learning Paths**: Create customized reading journeys for each child

### 📊 Comprehensive Assessment
- **Reading Performance Analysis**: Accuracy, fluency, speed, and comprehension metrics
- **Word Mastery Reports**: Detailed tracking of individual word progress
- **Progress Visualization**: Interactive charts showing improvement over time
- **Reading Level Estimation**: Automatic assessment of current reading level

### 🎮 Gamified Learning Experience
- **Reward System**: Stars, badges, and streaks for motivation
- **Interactive UI**: Child-friendly interface with large buttons and clear navigation
- **Progress Tracking**: Visual progress indicators and achievement celebrations
- **Engagement Features**: Audio pronunciation and interactive word games

### 👨‍👩‍👧‍👦 Parent Dashboard
- **Comprehensive Reports**: Detailed analysis of child's reading progress
- **Progress Charts**: Visual representation of improvement over time
- **Recommendations**: AI-generated suggestions for supporting reading development
- **Performance Metrics**: Accuracy, speed, fluency, and word mastery statistics

## 🏗️ System Architecture

### Frontend (Streamlit Web App)
```
📱 Child Interface
├── Storybook Viewer (text + illustrations)
├── Speech Input & Word Highlighting
├── Gamified UI with rewards
└── Progress Tracking

👨‍👩‍👧‍👦 Parent Dashboard
├── Reading Reports & Analytics
├── Progress Visualization
├── Recommendations Engine
└── Performance Metrics
```

### Backend Services
```
🤖 AI Services
├── Story Generator (GPT-4)
├── Illustration Generator (DALL-E 3)
├── Speech Recognition (Whisper + Google STT)
└── Assessment Engine

📊 Data Processing
├── Word-level Alignment
├── Performance Analysis
├── Adaptive Learning Logic
└── Report Generation

💾 Data Storage
├── Session State Management
├── Progress Tracking
├── Word Mastery Database
└── Assessment History
```

## 🚀 Implementation Phases

### Phase 1: MVP Storybook ✅
- [x] Basic frontend with text + illustration display
- [x] Story + illustration generation pipeline
- [x] Manual page navigation
- [x] Child-friendly UI design

### Phase 2: Speech Listening & Highlighting ✅
- [x] Speech recognition integration
- [x] Word-level alignment for highlighting
- [x] Real-time performance tracking
- [x] Gentle correction prompts

### Phase 3: Adaptive Engine ✅
- [x] Word mastery tracking system
- [x] Adaptive story vocabulary logic
- [x] Personalized difficulty adjustment
- [x] Progress optimization algorithms

### Phase 4: Reading Assessment ✅
- [x] Comprehensive performance analysis
- [x] Progress visualization charts
- [x] Parent dashboard with reports
- [x] Reading level estimation

### Phase 5: Engagement & Gamification ✅
- [x] Reward system (stars, badges, streaks)
- [x] Interactive word games
- [x] Progress celebrations
- [x] Audio pronunciation features

### Phase 6: Deployment & Testing 🔄
- [ ] Private beta testing with families
- [ ] User feedback integration
- [ ] Speech model optimization for child voices
- [ ] Performance optimization

## 🛠️ Technical Stack

### AI & Machine Learning
- **OpenAI GPT-4**: Story generation and content personalization
- **DALL-E 3**: Child-friendly illustration generation
- **Whisper**: Advanced speech recognition
- **Google Speech-to-Text**: Backup speech recognition

### Web Framework
- **Streamlit**: Interactive web application
- **Plotly**: Data visualization and charts
- **Pandas**: Data processing and analysis

### Audio Processing
- **SpeechRecognition**: Speech input handling
- **PyAudio**: Audio capture and processing
- **NumPy**: Audio data manipulation

### Data Management
- **Session State**: Real-time data persistence
- **JSON**: Data serialization and storage
- **Pandas**: Progress tracking and analysis

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Microphone access for speech recognition

### Installation

1. **Clone the repository** and navigate to the reading_teacher_2 directory:
   ```sh
   cd reading_teacher_2
   ```

2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key** (see SETUP.md for detailed instructions):
   ```sh
   export OPENAI_API_KEY="your-openai-api-key"
   ```
   
   Or create a `.env` file:
   ```sh
   echo 'OPENAI_API_KEY=your-openai-api-key' > .env
   ```

4. **Run the application**:
   ```sh
   streamlit run main_app.py
   ```

## 🎯 Usage Guide

### For Children (5-year-olds)
1. **Start Reading**: Click "New Story" to generate a personalized story
2. **Read Aloud**: Use the microphone to read the story aloud
3. **Track Progress**: Watch your stars and badges grow
4. **Play Games**: Practice with interactive word games
5. **See Progress**: Check your reading improvement over time

### For Parents
1. **Switch to Parent Mode**: Select "parent" in the user type dropdown
2. **View Reports**: See comprehensive reading progress analysis
3. **Track Performance**: Monitor accuracy, speed, and fluency metrics
4. **Get Recommendations**: Receive AI-generated suggestions for supporting reading
5. **Monitor Progress**: View detailed charts and word mastery reports

## 🎨 Design Philosophy

### Child-Centric Design
- **Large, clear buttons** for easy navigation
- **Colorful, engaging visuals** with emojis and illustrations
- **Positive reinforcement** throughout the experience
- **Simple, intuitive interface** appropriate for 5-year-olds

### Educational Excellence
- **Evidence-based approach** to reading instruction
- **Phonics-based learning** with sound-it-out guidance
- **Progressive difficulty** matching learning pace
- **Comprehensive assessment** for personalized instruction

### Safety & Privacy
- **No personal data collection** beyond reading progress
- **Age-appropriate content** filtering
- **Parental oversight** with comprehensive dashboard
- **Secure data handling** with local session storage

## 🔧 Advanced Features

### Speech Recognition Capabilities
- **Multi-model approach** using Whisper and Google STT
- **Child voice optimization** for better accuracy
- **Real-time word alignment** for precise tracking
- **Noise cancellation** for better recognition

### Adaptive Learning Intelligence
- **Word mastery algorithms** for personalized content
- **Difficulty progression** based on performance
- **Content personalization** using reading history
- **Learning path optimization** for maximum effectiveness

### Assessment & Analytics
- **Comprehensive metrics** including accuracy, speed, and fluency
- **Progress visualization** with interactive charts
- **Word-level analysis** for targeted improvement
- **Reading level estimation** for appropriate content selection

## 🎉 Impact & Benefits

### For Children
- **Personalized learning** experience tailored to individual needs
- **Engaging content** that makes reading fun and exciting
- **Immediate feedback** for continuous improvement
- **Confidence building** through positive reinforcement

### For Parents
- **Detailed insights** into child's reading development
- **Actionable recommendations** for supporting learning
- **Progress tracking** to monitor improvement over time
- **Peace of mind** knowing their child is learning effectively

### For Educators
- **Data-driven insights** for personalized instruction
- **Comprehensive assessment** tools for reading evaluation
- **Progress monitoring** for intervention planning
- **Evidence-based recommendations** for teaching strategies

## 🤝 Contributing

This project is designed for educational use. Feel free to:
- Report bugs and issues
- Suggest improvements
- Contribute to the codebase
- Share feedback from children and parents

## 📄 License

This project is open source and available under the MIT License.

---

**Empowering young readers, one story at a time! 📚✨** 

## 🔧 Troubleshooting

### Common Issues

**"No module named 'speech_recognition'"**
- Solution: `pip install SpeechRecognition`

**"Could not find PyAudio; check installation"**
- Solution: `pip install --only-binary=all pyaudio`

**"Invalid JSON response" when generating stories**
- Solution: Make sure your OpenAI API key is set correctly
- Check that you have sufficient API credits

**NumPy compatibility warnings**
- Solution: The requirements.txt already includes `numpy<2` for compatibility

### API Key Setup
See `SETUP.md` for detailed instructions on setting up your OpenAI API key.

## 🎨 Design Philosophy

### Child-Centric Design
- **Large, clear buttons** for easy navigation
- **Colorful, engaging visuals** with emojis and illustrations
- **Positive reinforcement** throughout the experience
- **Simple, intuitive interface** appropriate for 5-year-olds

### Educational Excellence
- **Evidence-based approach** to reading instruction
- **Phonics-based learning** with sound-it-out guidance
- **Progressive difficulty** matching learning pace
- **Comprehensive assessment** for personalized instruction

## 📁 Project Structure

```
reading_teacher_2/
├── main_app.py              # Main Streamlit application
├── story_generator.py       # AI story and illustration generation
├── speech_engine.py         # Speech recognition and word highlighting
├── assessment_engine.py     # Reading performance analysis
├── requirements.txt         # Python dependencies
├── SETUP.md                # Detailed setup instructions
└── README.md               # This file
```

## 🚀 Current Status

✅ **Completed Features:**
- AI story generation with DALL-E 3 illustrations
- Speech recognition with word highlighting
- Adaptive learning engine
- Comprehensive assessment system
- Gamified UI with rewards
- Parent dashboard with analytics
- All import and dependency issues resolved

🔄 **Ready for Use:**
- All core functionality implemented
- Error handling and debugging added
- Setup instructions provided
- Ready for testing and deployment

## 🤝 Contributing

This project is designed for educational use. Feel free to:
- Report bugs and issues
- Suggest improvements
- Contribute to the codebase
- Share feedback from children and parents

## 📄 License

This project is open source and available under the MIT License. 