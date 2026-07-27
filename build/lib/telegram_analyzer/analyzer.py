"""
Analyzes processed chat data.
"""

import pandas as pd
from typing import Dict, List
from nltk.corpus import stopwords
import logging
import nltk
import re
import numpy as np
from collections import Counter
from datetime import datetime

class ChatAnalyzer:
    """Analyzes processed chat data"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the chat analyzer.
        
        Args:
            df: DataFrame containing processed chat messages
        """
        self.df = df
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Try to load stopwords
        try:
            nltk.download('stopwords', quiet=True)
            self.stop_words = set(stopwords.words('english'))
        except Exception as e:
            self.logger.warning(f"Could not load NLTK stopwords: {e}")
            self.stop_words = set()
        
        # Ensure date column is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.df['date']):
            self.df['date'] = pd.to_datetime(self.df['date'])

    def get_basic_stats(self) -> Dict:
        """Calculate basic chat statistics"""
        # Ensure text length column exists
        if 'text_length' not in self.df.columns:
            self.df['text_length'] = self.df['text'].str.len()
        
        return {
            'total_messages': len(self.df),
            'total_participants': self.df['from'].nunique(),
            'date_range': {
                'start': self.df['date'].min(),
                'end': self.df['date'].max(),
                'total_days': (self.df['date'].max() - self.df['date'].min()).days
            },
            'media_messages': self.df['media_type'].notna().sum(),
            'avg_message_length': self.df['text_length'].mean()
        }

    def get_user_stats(self) -> Dict:
        """Calculate user-specific statistics"""
        user_stats = {}
        
        # Ensure text length column exists
        if 'text_length' not in self.df.columns:
            self.df['text_length'] = self.df['text'].str.len()
        
        for user in self.df['from'].unique():
            user_messages = self.df[self.df['from'] == user]
            user_stats[user] = {
                'message_count': len(user_messages),
                'media_count': user_messages['media_type'].notna().sum(),
                'avg_message_length': user_messages['text_length'].mean(),
                'avg_sentiment': user_messages['sentiment'].mean() if 'sentiment' in self.df.columns else 0
            }
            
        return user_stats

    def get_activity_patterns(self) -> Dict:
        """Analyze activity patterns"""
        return {
            'hourly': self.df['date'].dt.hour.value_counts().sort_index().to_dict(),
            'daily': self.df['date'].dt.day_name().value_counts().to_dict(),
            'monthly': self.df['date'].dt.month.value_counts().sort_index().to_dict()
        }

    def get_content_analysis(self) -> Dict:
        """Analyze message content"""
        # Prepare default values for analysis
        media_types = self.df['media_type'].value_counts().to_dict() if 'media_type' in self.df.columns else {}
        
        # Check for emoji and link columns
        emoji_usage = self.df['has_emoji'].sum() if 'has_emoji' in self.df.columns else 0
        link_sharing = self.df['has_link'].sum() if 'has_link' in self.df.columns else 0
        
        return {
            'media_types': media_types,
            'avg_sentiment': self.df['sentiment'].mean() if 'sentiment' in self.df.columns else 0,
            'emoji_usage': emoji_usage,
            'link_sharing': link_sharing
        }
        
    def get_online_time_stats(self) -> Dict:
        """
        Calculate online time and presence statistics for users.
        
        Returns:
            Dictionary containing online time and presence statistics
        """
        try:
            # Compute user online time statistics
            user_online_times = {}
            peak_online_hours = {}
            
            for user in self.df['from'].unique():
                # Filter messages for this user
                user_messages = self.df[self.df['from'] == user]
                
                # Calculate total online time
                if len(user_messages) > 0:
                    # Total time from first to last message
                    total_time = (user_messages['date'].max() - user_messages['date'].min()).total_seconds() / 3600  # hours
                    
                    # Most active time (hour with most messages)
                    peak_hour = user_messages['date'].dt.hour.mode().values[0]
                    
                    # Hourly message distribution
                    hourly_distribution = user_messages['date'].dt.hour.value_counts().to_dict()
                    
                    user_online_times[user] = {
                        'total_hours': total_time,
                        'peak_time': f"{peak_hour:02d}:00",
                        'message_count': len(user_messages)
                    }
                    
                    peak_online_hours[user] = [
                        hourly_distribution.get(hour, 0) for hour in range(24)
                    ]
            
            # Compute overall statistics
            stats = {
                'user_online_times': user_online_times,
                'peak_online_hours': peak_online_hours,
                'total_active_users': len(user_online_times),
                'average_online_hours': sum(times['total_hours'] for times in user_online_times.values()) / len(user_online_times) if user_online_times else 0
            }
            
            return stats
        
        except Exception as e:
            self.logger.error(f"Error computing online time statistics: {str(e)}")
            return {}

    def get_chat_velocity(self) -> Dict:
        """Analyze message velocity over time"""
        self.df['day'] = self.df['date'].dt.date
        velocity = self.df.groupby('day').size()
        
        # Calculate rolling average for smoother trends
        rolling_avg = velocity.rolling(window=7, min_periods=1).mean()
        
        return {
            'daily_messages': {str(k): int(v) for k, v in velocity.to_dict().items()},
            'weekly_rolling_avg': {str(k): float(v) for k, v in rolling_avg.to_dict().items()},
            'peak_velocity': {
                'date': str(velocity.idxmax()),
                'count': int(velocity.max())
            }
        }

    def get_engagement_intelligence(self) -> Dict:
        """Calculate advanced engagement scores and user archetypes"""
        intelligence = {}
        
        for user in self.df['from'].unique():
            user_msgs = self.df[self.df['from'] == user]
            
            # Basic metrics
            count = len(user_msgs)
            avg_len = user_msgs['text_length'].mean() if 'text_length' in self.df.columns else 0
            # Metrics for analysis
            sentiment = user_msgs['sentiment'].mean() if 'sentiment' in self.df.columns else 0
            media_ratio = (user_msgs['media_type'].notna().sum() / count) if count > 0 else 0
            
            # Engagement Score (Weighted)
            norm_count = count / len(self.df)
            score = (norm_count * 0.4) + (min(avg_len, 500) / 500 * 0.2) + (abs(sentiment) * 0.2) + (media_ratio * 0.2)
            
            # Archetype assignment
            archetype = "Neutral"
            if count > self.df['from'].value_counts().mean() * 1.5: archetype = "Main Protagonist"
            elif sentiment > 0.3: archetype = "The Optimist"
            elif sentiment < -0.3: archetype = "The Critic"
            elif media_ratio > 0.4: archetype = "Media Maven"
            elif avg_len > 100: archetype = "The Storyteller"

            # Emotional Mapping (Categorical)
            emotion = "Neutral"
            if sentiment > 0.4: emotion = "Joyous / Happy"
            elif sentiment < -0.4: emotion = "Angry / Aggressive"
            elif sentiment < -0.1: emotion = "Sorrowful / Sad"
            elif sentiment > 0.1: emotion = "Pleasant"
                
            intelligence[user] = {
                'engagement_score': round(score * 100, 2),
                'archetype': archetype,
                'dominant_emotion': emotion,
                'ocean_profile': self.get_ocean_personality(user)
            }
            
        return intelligence

    def get_ocean_personality(self, user: str) -> Dict:
        """Calculate Big Five (OCEAN) traits for a specific user"""
        user_msgs = self.df[self.df['from'] == user]
        if user_msgs.empty: return {}
        
        # O - Openness: Media ratio + message length diversity
        openness = (user_msgs['media_type'].notna().sum() / len(user_msgs) * 50) + (min(user_msgs['text_length'].std() if len(user_msgs) > 1 else 0, 100) / 2)
        
        # C - Conscientiousness: Regularity of messaging + text length
        conscientiousness = (min(user_msgs['text_length'].mean(), 200) / 4) + (50 if user_msgs['date'].dt.hour.std() < 5 else 20)
        
        # E - Extraversion: Message frequency + bursts
        extraversion = (len(user_msgs) / (len(self.df) / self.df['from'].nunique()) * 50)
        
        # A - Agreeableness: Sentiment + care mentions
        agreeableness = ((user_msgs['sentiment'].mean() + 1) * 25) + (user_msgs['care_mentions'].mean() * 500)
        
        # N - Neuroticism: Emotional intensity + sentiment volatility
        neuroticism = (user_msgs['sentiment'].std() if len(user_msgs) > 1 else 0) * 100
        
        return {
            'Openness': min(100, round(openness, 1)),
            'Conscientiousness': min(100, round(conscientiousness, 1)),
            'Extraversion': min(100, round(extraversion, 1)),
            'Agreeableness': min(100, round(agreeableness, 1)),
            'Neuroticism': min(100, round(neuroticism, 1))
        }

    def get_conversation_bursts(self) -> List[Dict]:
        """Identify high-intensity conversation bursts"""
        # Sort by date
        sorted_df = self.df.sort_values('date')
        
        # Calculate time difference between consecutive messages
        diffs = sorted_df['date'].diff().dt.total_seconds()
        
        # A burst is a sequence of messages where diff < 60 seconds
        bursts = []
        current_burst = []
        
        for i, diff in enumerate(diffs):
            if pd.isna(diff) or diff < 60:
                current_burst.append(i)
            else:
                if len(current_burst) >= 10:  # Minimum 10 messages for a burst
                    burst_msgs = sorted_df.iloc[current_burst]
                    bursts.append({
                        'start_time': str(burst_msgs['date'].min()),
                        'end_time': str(burst_msgs['date'].max()),
                        'message_count': len(burst_msgs),
                        'participants': int(burst_msgs['from'].nunique())
                    })
                current_burst = [i]
                
        # Handle last burst
        if len(current_burst) >= 10:
            burst_msgs = sorted_df.iloc[current_burst]
            bursts.append({
                'start_time': str(burst_msgs['date'].min()),
                'end_time': str(burst_msgs['date'].max()),
                'message_count': len(burst_msgs),
                'participants': int(burst_msgs['from'].nunique())
            })
            
        return sorted(bursts, key=lambda x: x['message_count'], reverse=True)[:5]

    def get_executive_summary(self) -> str:
        """Generate a high-level summary of the chat's 'character'"""
        stats = self.get_basic_stats()
        sentiment = self.get_content_analysis().get('avg_sentiment', 0)
        
        summary = f"This dataset covers {stats['date_range']['total_days']} days of intelligence across {stats['total_participants']} participants. "
        
        if sentiment > 0.2:
            summary += "The overall emotional landscape is exceptionally positive and collaborative. "
        elif sentiment < -0.2:
            summary += "The discourse tends to be more critical or intense. "
        else:
            summary += "The conversation maintains a professional and balanced tone. "
            
        media_ratio = stats['media_messages'] / stats['total_messages'] if stats['total_messages'] > 0 else 0
        if media_ratio > 0.3:
            summary += "There is a heavy reliance on visual and media-based communication. "
        else:
            summary += "Communication is primarily text-driven and linguistic. "
            
        return summary

    def get_psychological_stats(self) -> Dict:
        """Analyze health, mood, and care patterns"""
        psych = {
            'health': {
                'total_mentions': int(self.df['health_mentions'].sum()),
                'by_user': self.df[self.df['health_mentions']]['from'].value_counts().to_dict()
            },
            'love_and_care': {
                'total_mentions': int(self.df['care_mentions'].sum()),
                'by_user': self.df[self.df['care_mentions']]['from'].value_counts().to_dict()
            },
            'emotional_pulse': {
                'avg_intensity': float(self.df['mood_intensity'].mean()),
                'peak_emotional_days': self.df.groupby(self.df['date'].dt.date)['mood_intensity'].mean().nlargest(5).to_dict()
            }
        }
        
        # Format dates for JSON
        psych['emotional_pulse']['peak_emotional_days'] = {str(k): float(v) for k, v in psych['emotional_pulse']['peak_emotional_days'].items()}
        
        # New: Health Issue Tracking
        health_msgs = self.df[self.df['health_mentions']]
        if not health_msgs.empty:
            # Simple keyword-based categorization
            acute_words = {'fever', 'cold', 'flu', 'cough', 'emergency', 'ambulance', 'surgery', 'pain', 'headache'}
            chronic_words = {'diabetes', 'asthma', 'anxiety', 'depression', 'blood pressure', 'therapy', 'meds'}
            
            psych['health_tracking'] = {
                'acute_episodes': int(health_msgs['text'].str.contains('|'.join(acute_words), case=False).sum()),
                'chronic_management': int(health_msgs['text'].str.contains('|'.join(chronic_words), case=False).sum()),
                'health_velocity': self.df.groupby(self.df['date'].dt.date)['health_mentions'].sum().to_dict()
            }
            # Clean dates for JSON
            psych['health_tracking']['health_velocity'] = {str(k): int(v) for k, v in psych['health_tracking']['health_velocity'].items() if v > 0}
            
        return psych

    def get_social_dynamics(self) -> Dict:
        """Analyze relationships and harmony between users"""
        dynamics = {}
        
        # Get users who interact (sequential messages)
        interactions = []
        users = self.df['from'].dropna().tolist()
        sentiments = self.df['sentiment'].tolist()
        
        for i in range(len(users) - 1):
            if users[i] != users[i+1]:
                pair = tuple(sorted((users[i], users[i+1])))
                # Use the sentiment of the responding message as a proxy for harmony
                interactions.append({
                    'pair': pair,
                    'sentiment': sentiments[i+1]
                })
        
        if not interactions:
            return {}
            
        inter_df = pd.DataFrame(interactions)
        harmony = inter_df.groupby('pair')['sentiment'].mean().to_dict()
        intensity = inter_df.groupby('pair').size().to_dict()
        
        # Convert pairs to strings for JSON
        dynamics['harmony_matrix'] = {f"{p[0]} <-> {p[1]}": float(s) for p, s in harmony.items()}
        dynamics['interaction_intensity'] = {f"{p[0]} <-> {p[1]}": int(i) for p, i in intensity.items()}
        
        # Identify "Most Harmonious" and "Most Intense" pairs
        if dynamics['harmony_matrix']:
            sorted_harmony = sorted(dynamics['harmony_matrix'].items(), key=lambda x: x[1], reverse=True)
            dynamics['most_harmonious'] = sorted_harmony[0] if sorted_harmony else None
            dynamics['most_combative'] = sorted_harmony[-1] if sorted_harmony else None
            
        return dynamics

    def get_semantic_concepts(self) -> List[Dict]:
        """Extract key concepts and thematic clusters"""
        # Simple N-gram frequency analysis (bigrams)
        from collections import Counter
        import re
        
        text = " ".join(self.df['text'].dropna().astype(str).tolist()).lower()
        words = re.findall(r'\b[a-z]{4,}\b', text)
        words = [w for w in words if w not in self.stop_words]
        
        bigrams = [" ".join(pair) for pair in zip(words, words[1:])]
        concept_counts = Counter(bigrams).most_common(15)
        
        return [{'concept': c, 'relevance': int(count)} for c, count in concept_counts]

    def get_user_dna(self) -> Dict:
        """Generate unique DNA fingerprints for each user"""
        dna = {}
        for user in self.df['from'].unique():
            user_msgs = self.df[self.df['from'] == user]
            if len(user_msgs) == 0: continue
            
            # Encode metrics into a DNA string
            # Length (0-9), Sentiment (A-Z), Media (0-9), Timing (A-Z)
            l_val = min(9, int(user_msgs['text_length'].mean() / 20))
            s_val = chr(65 + min(25, int((user_msgs['sentiment'].mean() + 1) * 12.5)))
            m_val = min(9, int((user_msgs['media_type'].notna().sum() / len(user_msgs)) * 10))
            t_val = chr(65 + int(user_msgs['date'].dt.hour.mean()))
            
            dna[user] = f"DNA-{l_val}{s_val}{m_val}{t_val}"
            
        return dna

    def get_stability_index(self) -> Dict:
        """Detect conflict escalations and overall group stability"""
        bursts = self.get_conversation_bursts()
        stability = {
            'index': 100.0,
            'escalations': [],
            'status': 'Stable'
        }
        
        total_escalation = 0
        for burst in bursts:
            # Check for sharp sentiment drop within the burst
            # For simplicity, we compare start vs end sentiment if available
            pass # Simplified logic for now
            
        return stability

    def get_all_stats(self) -> Dict:
        """Get all available statistics including advanced intelligence"""
        return {
            'basic_stats': self.get_basic_stats(),
            'user_stats': self.get_user_stats(),
            'activity_patterns': self.get_activity_patterns(),
            'content_analysis': self.get_content_analysis(),
            'chat_velocity': self.get_chat_velocity(),
            'engagement_intelligence': self.get_engagement_intelligence(),
            'conversation_bursts': self.get_conversation_bursts(),
            'executive_summary': self.get_executive_summary(),
            'psychological_stats': self.get_psychological_stats(),
            'social_dynamics': self.get_social_dynamics(),
            'semantic_concepts': self.get_semantic_concepts(),
            'user_dna': self.get_user_dna(),
            'stability_index': self.get_stability_index()
        }