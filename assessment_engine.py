import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Tuple
import json
from datetime import datetime, timedelta
import numpy as np

class AssessmentEngine:
    def __init__(self):
        self.assessment_data = {
            "reading_sessions": [],
            "word_mastery": {},
            "progress_over_time": [],
            "recommendations": []
        }
    
    def analyze_reading_session(self, session_data: Dict) -> Dict:
        """Analyze a single reading session"""
        analysis = {
            "session_id": session_data.get("session_id", datetime.now().isoformat()),
            "timestamp": session_data.get("timestamp", datetime.now().isoformat()),
            "reading_level": session_data.get("reading_level", "beginner"),
            "story_title": session_data.get("story_title", "Unknown"),
            "performance_metrics": {},
            "word_analysis": {},
            "recommendations": []
        }
        
        # Analyze performance metrics
        performance = session_data.get("performance", {})
        analysis["performance_metrics"] = {
            "accuracy": performance.get("accuracy", 0),
            "words_per_minute": performance.get("words_per_minute", 0),
            "fluency_score": performance.get("fluency_score", 0),
            "total_words": performance.get("total_words", 0),
            "mistakes": performance.get("mistakes", 0),
            "missed_words": performance.get("missed_words", 0)
        }
        
        # Analyze word mastery
        words_read = session_data.get("words_read", {})
        analysis["word_analysis"] = {
            "words_attempted": len(words_read),
            "words_mastered": len([w for w, stats in words_read.items() if stats.get("mastery_level", 0) >= 90]),
            "words_needing_practice": len([w for w, stats in words_read.items() if stats.get("mastery_level", 0) < 70]),
            "average_mastery": np.mean([stats.get("mastery_level", 0) for stats in words_read.values()]) if words_read else 0
        }
        
        # Generate session-specific recommendations
        analysis["recommendations"] = self.generate_session_recommendations(analysis)
        
        return analysis
    
    def generate_session_recommendations(self, analysis: Dict) -> List[str]:
        """Generate recommendations based on session analysis"""
        recommendations = []
        
        # Accuracy-based recommendations
        accuracy = analysis["performance_metrics"]["accuracy"]
        if accuracy < 70:
            recommendations.append("Focus on word recognition and phonics practice")
        elif accuracy < 85:
            recommendations.append("Continue practicing challenging words")
        else:
            recommendations.append("Great accuracy! Ready for more complex texts")
        
        # Speed-based recommendations
        wpm = analysis["performance_metrics"]["words_per_minute"]
        if wpm < 20:
            recommendations.append("Practice reading aloud to improve speed")
        elif wpm > 50:
            recommendations.append("Excellent reading speed! Focus on comprehension")
        
        # Fluency-based recommendations
        fluency = analysis["performance_metrics"]["fluency_score"]
        if fluency < 60:
            recommendations.append("Practice reading with expression and rhythm")
        elif fluency < 80:
            recommendations.append("Good fluency! Continue regular practice")
        
        # Word mastery recommendations
        words_needing_practice = analysis["word_analysis"]["words_needing_practice"]
        if words_needing_practice > 5:
            recommendations.append(f"Focus on practicing {words_needing_practice} words that need more work")
        
        return recommendations
    
    def track_progress_over_time(self, session_analysis: Dict):
        """Track reading progress over time"""
        progress_point = {
            "date": session_analysis["timestamp"][:10],  # Just the date part
            "accuracy": session_analysis["performance_metrics"]["accuracy"],
            "words_per_minute": session_analysis["performance_metrics"]["words_per_minute"],
            "fluency_score": session_analysis["performance_metrics"]["fluency_score"],
            "words_mastered": session_analysis["word_analysis"]["words_mastered"],
            "average_mastery": session_analysis["word_analysis"]["average_mastery"]
        }
        
        self.assessment_data["progress_over_time"].append(progress_point)
    
    def generate_progress_charts(self) -> Dict:
        """Generate progress visualization charts"""
        if not self.assessment_data["progress_over_time"]:
            return {}
        
        df = pd.DataFrame(self.assessment_data["progress_over_time"])
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        charts = {}
        
        # Accuracy over time
        fig_accuracy = px.line(df, x='date', y='accuracy', 
                              title='Reading Accuracy Over Time',
                              labels={'accuracy': 'Accuracy (%)', 'date': 'Date'})
        fig_accuracy.update_layout(yaxis_range=[0, 100])
        charts['accuracy'] = fig_accuracy
        
        # Words per minute over time
        fig_wpm = px.line(df, x='date', y='words_per_minute',
                         title='Reading Speed Over Time',
                         labels={'words_per_minute': 'Words per Minute', 'date': 'Date'})
        charts['wpm'] = fig_wpm
        
        # Fluency score over time
        fig_fluency = px.line(df, x='date', y='fluency_score',
                             title='Fluency Score Over Time',
                             labels={'fluency_score': 'Fluency Score (%)', 'date': 'Date'})
        fig_fluency.update_layout(yaxis_range=[0, 100])
        charts['fluency'] = fig_fluency
        
        # Words mastered over time
        fig_mastered = px.bar(df, x='date', y='words_mastered',
                             title='Words Mastered Over Time',
                             labels={'words_mastered': 'Words Mastered', 'date': 'Date'})
        charts['mastered'] = fig_mastered
        
        return charts
    
    def generate_word_mastery_report(self) -> Dict:
        """Generate detailed word mastery report"""
        all_words = {}
        
        # Aggregate word mastery data from all sessions
        for session in self.assessment_data["reading_sessions"]:
            words_read = session.get("words_read", {})
            for word, stats in words_read.items():
                if word not in all_words:
                    all_words[word] = {
                        "correct_count": 0,
                        "total_count": 0,
                        "mastery_level": 0,
                        "first_seen": session.get("timestamp", ""),
                        "last_seen": session.get("timestamp", "")
                    }
                
                all_words[word]["correct_count"] += stats.get("correct_count", 0)
                all_words[word]["total_count"] += stats.get("total_count", 0)
                all_words[word]["last_seen"] = session.get("timestamp", "")
        
        # Calculate mastery levels
        for word, stats in all_words.items():
            if stats["total_count"] > 0:
                stats["mastery_level"] = (stats["correct_count"] / stats["total_count"]) * 100
        
        # Categorize words
        mastered_words = {word: stats for word, stats in all_words.items() if stats["mastery_level"] >= 90}
        needs_practice = {word: stats for word, stats in all_words.items() if stats["mastery_level"] < 70}
        improving_words = {word: stats for word, stats in all_words.items() if 70 <= stats["mastery_level"] < 90}
        
        return {
            "total_words": len(all_words),
            "mastered_words": len(mastered_words),
            "needs_practice": len(needs_practice),
            "improving_words": len(improving_words),
            "word_details": {
                "mastered": mastered_words,
                "needs_practice": needs_practice,
                "improving": improving_words
            }
        }
    
    def estimate_reading_level(self) -> str:
        """Estimate current reading level based on performance"""
        if not self.assessment_data["progress_over_time"]:
            return "beginner"
        
        # Get recent performance (last 5 sessions)
        recent_sessions = self.assessment_data["progress_over_time"][-5:]
        
        avg_accuracy = np.mean([s["accuracy"] for s in recent_sessions])
        avg_wpm = np.mean([s["words_per_minute"] for s in recent_sessions])
        avg_fluency = np.mean([s["fluency_score"] for s in recent_sessions])
        
        # Reading level criteria
        if avg_accuracy >= 90 and avg_wpm >= 40 and avg_fluency >= 80:
            return "advanced"
        elif avg_accuracy >= 80 and avg_wpm >= 25 and avg_fluency >= 60:
            return "intermediate"
        else:
            return "beginner"
    
    def generate_parent_report(self) -> Dict:
        """Generate comprehensive report for parents"""
        if not self.assessment_data["reading_sessions"]:
            return {"message": "No reading sessions available for report generation"}
        
        # Calculate overall statistics
        total_sessions = len(self.assessment_data["reading_sessions"])
        avg_accuracy = np.mean([s["performance_metrics"]["accuracy"] for s in self.assessment_data["reading_sessions"]])
        avg_wpm = np.mean([s["performance_metrics"]["words_per_minute"] for s in self.assessment_data["reading_sessions"]])
        avg_fluency = np.mean([s["performance_metrics"]["fluency_score"] for s in self.assessment_data["reading_sessions"]])
        
        # Word mastery report
        word_report = self.generate_word_mastery_report()
        
        # Current reading level
        current_level = self.estimate_reading_level()
        
        # Generate charts
        charts = self.generate_progress_charts()
        
        # Overall recommendations
        overall_recommendations = self.generate_overall_recommendations()
        
        report = {
            "summary": {
                "total_sessions": total_sessions,
                "current_reading_level": current_level,
                "average_accuracy": round(avg_accuracy, 1),
                "average_speed": round(avg_wpm, 1),
                "average_fluency": round(avg_fluency, 1)
            },
            "word_mastery": word_report,
            "recommendations": overall_recommendations,
            "charts": charts,
            "generated_date": datetime.now().isoformat()
        }
        
        return report
    
    def generate_overall_recommendations(self) -> List[str]:
        """Generate overall recommendations based on all sessions"""
        recommendations = []
        
        if not self.assessment_data["reading_sessions"]:
            return ["Start with regular reading sessions to build a foundation"]
        
        # Analyze recent performance
        recent_sessions = self.assessment_data["reading_sessions"][-3:]
        recent_accuracy = np.mean([s["performance_metrics"]["accuracy"] for s in recent_sessions])
        recent_wpm = np.mean([s["performance_metrics"]["words_per_minute"] for s in recent_sessions])
        
        # Frequency recommendations
        total_sessions = len(self.assessment_data["reading_sessions"])
        if total_sessions < 5:
            recommendations.append("Increase reading frequency to at least 3-4 sessions per week")
        elif total_sessions < 10:
            recommendations.append("Good reading frequency! Continue with regular practice")
        else:
            recommendations.append("Excellent reading consistency! Consider more challenging texts")
        
        # Performance-based recommendations
        if recent_accuracy < 75:
            recommendations.append("Focus on accuracy over speed - practice difficult words")
        elif recent_accuracy > 90:
            recommendations.append("Excellent accuracy! Ready for more complex vocabulary")
        
        if recent_wpm < 20:
            recommendations.append("Practice reading aloud to improve reading speed")
        elif recent_wpm > 45:
            recommendations.append("Great reading speed! Focus on comprehension and expression")
        
        # Word mastery recommendations
        word_report = self.generate_word_mastery_report()
        if word_report["needs_practice"] > 10:
            recommendations.append(f"Focus on practicing {word_report['needs_practice']} words that need more work")
        
        return recommendations
    
    def save_assessment_data(self):
        """Save assessment data to session state"""
        st.session_state["assessment_data"] = self.assessment_data
    
    def load_assessment_data(self):
        """Load assessment data from session state"""
        if "assessment_data" in st.session_state:
            self.assessment_data = st.session_state["assessment_data"]

if __name__ == "__main__":
    # Test the assessment engine
    engine = AssessmentEngine()
    print("Assessment engine initialized") 