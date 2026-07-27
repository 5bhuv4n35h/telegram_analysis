"""
Enhanced interactive visualizations using Plotly.
"""

import os
import pandas as pd
import logging
from typing import List

try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

class EnhancedVisualizer:
    """Generates interactive visualizations using Plotly"""
    
    def __init__(self, df: pd.DataFrame, output_dir: str):
        self.df = df
        self.output_dir = os.path.join(output_dir, 'interactive')
        self.logger = logging.getLogger(__name__)
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_all_visualizations(self) -> List[str]:
        """Generate all available interactive visualizations"""
        if not PLOTLY_AVAILABLE:
            self.logger.warning("Plotly is not installed. Skipping interactive visualizations.")
            return []
            
        successful_viz = []
        
        try:
            if self.generate_sentiment_timeline_interactive():
                successful_viz.append('sentiment_timeline_interactive.html')
                
            if self.generate_user_activity_interactive():
                successful_viz.append('user_activity_interactive.html')
                
            if self.generate_hourly_distribution_interactive():
                successful_viz.append('hourly_distribution_interactive.html')
                
            self.logger.info(f"Generated {len(successful_viz)} interactive visualizations")
            return successful_viz
            
        except Exception as e:
            self.logger.error(f"Error generating interactive visualizations: {str(e)}")
            return successful_viz

    def generate_sentiment_timeline_interactive(self) -> bool:
        """Generate interactive sentiment timeline"""
        try:
            # Resample by day
            daily_sentiment = self.df.set_index('date').resample('D')['sentiment'].mean().reset_index()
            
            fig = px.line(daily_sentiment, x='date', y='sentiment', 
                          title='Interactive Emotional Pulse Timeline',
                          template='plotly_dark',
                          color_discrete_sequence=['#0088cc'])
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            output_path = os.path.join(self.output_dir, 'sentiment_timeline_interactive.html')
            fig.write_html(output_path)
            return True
        except Exception as e:
            self.logger.error(f"Error generating interactive sentiment timeline: {str(e)}")
            return False

    def generate_user_activity_interactive(self) -> bool:
        """Generate interactive user activity treemap"""
        try:
            user_counts = self.df['from'].value_counts().reset_index()
            user_counts.columns = ['user', 'messages']
            
            fig = px.treemap(user_counts, path=['user'], values='messages',
                             title='User Contribution Hierarchy',
                             template='plotly_dark',
                             color='messages',
                             color_continuous_scale='Blues')
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            output_path = os.path.join(self.output_dir, 'user_activity_interactive.html')
            fig.write_html(output_path)
            return True
        except Exception as e:
            self.logger.error(f"Error generating interactive user activity: {str(e)}")
            return False

    def generate_hourly_distribution_interactive(self) -> bool:
        """Generate interactive hourly distribution radar chart"""
        try:
            self.df['hour'] = self.df['date'].dt.hour
            hourly_counts = self.df['hour'].value_counts().sort_index().reset_index()
            hourly_counts.columns = ['hour', 'messages']
            
            fig = go.Figure(data=go.Scatterpolar(
                r=hourly_counts['messages'],
                theta=[f"{h}:00" for h in hourly_counts['hour']],
                fill='toself',
                line_color='#00c6ff'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, side='counterclockwise'),
                    bgcolor='rgba(0,0,0,0)'
                ),
                showlegend=False,
                title='24-Hour Activity Radar',
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            output_path = os.path.join(self.output_dir, 'hourly_distribution_interactive.html')
            fig.write_html(output_path)
            return True
        except Exception as e:
            self.logger.error(f"Error generating interactive hourly distribution: {str(e)}")
            return False
