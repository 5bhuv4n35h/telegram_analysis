"""
Generates a unified, efficient analysis report including enhanced online presence data.
"""

import os
from typing import Dict, List, Optional
import logging
from datetime import datetime

class ReportGenerator:
    """Generates a unified, streamlined report with enhanced online presence analysis"""
    
    def __init__(self, stats: Dict, output_dir: str):
        """Initialize with analysis statistics and output directory"""
        self.stats = stats
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)
        
        # Ensure online presence stats are available
        if 'online_presence' not in self.stats:
            self.stats['online_presence'] = {}
        
        # Log available data sections for debugging
        self.logger.info(f"ReportGenerator initialized with data sections: {list(self.stats.keys())}")
    
    def generate_html_report(self, interactive_viz: Optional[List[str]] = None):
        """Generate a unified HTML report with all analysis sections"""
        self.logger.info("Generating comprehensive HTML report")
        try:
            # Check available visualizations
            visualizations = self._check_visualizations()
            
            # Create HTML content with all sections
            html_content = self._create_html_content(visualizations, interactive_viz or [])
            
            # Ensure output directory exists and write report
            os.makedirs(self.output_dir, exist_ok=True)
            report_path = os.path.join(self.output_dir, 'report.html')
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            self.logger.info(f"Unified report generated at {report_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            return False
    
    def _check_visualizations(self) -> List[str]:
        """
        Check which visualization files exist in the output directory.
        
        Returns:
            List of available visualization filenames
        """
        visualizations = []
        
        # All possible visualization files to check
        viz_files = [
            # Basic visualizations
            'activity_heatmap.png', 'user_activity.png', 'wordcloud.png', 
            'sentiment_timeline.png', 'media_distribution.png', 
            'weekly_activity.png', 'conversation_flow.png',
            
            # Content analysis visualizations
            'word_frequency.png', 'topic_clusters.png', 
            'sentiment_distribution.png', 'message_length_histogram.png',
            
            # Online presence visualizations
            'user_time_preferences.png', 'user_online_hours.png', 
            'peak_online_hours.png', 'user_activity_heatmap.png',
            'user_ghosting_scores.png', 'user_consistency_scores.png',
            'response_time_distribution.png', 'user_response_network.png',
            
            # Interaction visualizations
            'user_interaction_network.png', 'response_time_analysis.png', 
            'emoji_usage.png',
            
            # Advanced Intelligence
            'chat_velocity.png', 'engagement_intelligence.png',
            
            # Psychological
            'psychological_wellbeing.png', 'mood_intensity.png'
        ]
        
        # Check each file
        for viz_file in viz_files:
            if os.path.exists(os.path.join(self.output_dir, viz_file)):
                visualizations.append(viz_file)
        
        self.logger.info(f"Found {len(visualizations)} visualization files")
        return visualizations
    
    def _create_html_content(self, visualizations: List[str], interactive_viz: List[str]) -> str:
        """Create HTML content for the unified report"""
        # Get data for the report
        basic_stats = self.stats.get('basic_stats', {})
        user_stats = self.stats.get('user_stats', {})
        activity_patterns = self.stats.get('activity_patterns', {})
        content_analysis = self.stats.get('content_analysis', {})
        online_presence = self.stats.get('online_presence', {})
        
        # Create HTML structure with Bootstrap CSS
        html = self._create_html_header()
        
        # Add content sections
        html += self._create_overview_section(basic_stats)
        html += self._create_user_activity_section(user_stats, visualizations)
        html += self._create_activity_patterns_section(activity_patterns, visualizations)
        html += self._create_content_analysis_section(visualizations)
        html += self._create_online_presence_section(online_presence, visualizations)
        html += self._create_intelligence_section(visualizations)
        html += self._create_psychological_section(visualizations)
        html += self._create_social_dynamics_section(visualizations)
        html += self._create_thematic_landscape_section()
        html += self._create_interaction_section(visualizations)
        
        # Add interactive visualizations section if available
        if interactive_viz:
            html += self._create_interactive_viz_section(interactive_viz)
        
        # Add footer and close HTML
        html += self._create_footer()
        
        return html
    
    def _create_html_header(self) -> str:
        """Create a premium HTML header with modern CSS and navigation"""
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Telegram Insights | Intelligence Report</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
            <style>
                :root {
                    --primary: #0088cc;
                    --primary-glow: rgba(0, 136, 204, 0.3);
                    --bg-dark: #0e1621;
                    --bg-card: #17212b;
                    --text-main: #ffffff;
                    --text-muted: #708499;
                    --glass: rgba(23, 33, 43, 0.7);
                    --border: rgba(255, 255, 255, 0.08);
                }

                body { 
                    font-family: 'Inter', sans-serif; 
                    background-color: var(--bg-dark);
                    color: var(--text-main);
                    padding-top: 80px;
                    line-height: 1.6;
                }

                .navbar {
                    background: rgba(14, 22, 33, 0.85) !important;
                    backdrop-filter: blur(15px);
                    border-bottom: 1px solid var(--border);
                    padding: 15px 0;
                }

                .navbar-brand {
                    font-weight: 800;
                    letter-spacing: -0.5px;
                    color: var(--primary) !important;
                }

                .nav-link {
                    font-weight: 600;
                    font-size: 0.9rem;
                    color: var(--text-muted) !important;
                    transition: all 0.3s ease;
                }

                .nav-link:hover, .nav-link.active {
                    color: var(--text-main) !important;
                }

                .section {
                    padding: 40px 0;
                    scroll-margin-top: 100px;
                }

                .premium-card {
                    background: var(--bg-card);
                    border-radius: 20px;
                    border: 1px solid var(--border);
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    margin-bottom: 30px;
                    overflow: hidden;
                    transition: transform 0.3s ease;
                }

                .card-header {
                    background: rgba(255,255,255,0.02) !important;
                    border-bottom: 1px solid var(--border) !important;
                    padding: 20px 25px !important;
                }

                .card-header h2 {
                    font-size: 1.5rem;
                    font-weight: 700;
                    margin: 0;
                    display: flex;
                    align-items: center;
                    gap: 12px;
                }

                .card-body {
                    padding: 25px;
                }

                .stat-box {
                    background: rgba(255,255,255,0.03);
                    border-radius: 16px;
                    padding: 20px;
                    text-align: center;
                    border: 1px solid var(--border);
                    height: 100%;
                }

                .stat-value {
                    font-size: 2rem;
                    font-weight: 800;
                    color: var(--primary);
                    text-shadow: 0 0 15px var(--primary-glow);
                }

                .stat-label {
                    color: var(--text-muted);
                    font-size: 0.85rem;
                    font-weight: 600;
                    text-transform: uppercase;
                    margin-top: 8px;
                }

                .viz-container {
                    background: #111b27;
                    border-radius: 12px;
                    padding: 15px;
                    margin-top: 20px;
                    border: 1px solid var(--border);
                }

                .img-fluid {
                    border-radius: 8px;
                    filter: saturate(1.1);
                    transition: transform 0.3s ease;
                }

                .img-fluid:hover {
                    transform: scale(1.02);
                }

                .archetype-card {
                    background: rgba(255, 255, 255, 0.03);
                    padding: 15px;
                    border-radius: 12px;
                    margin-bottom: 12px;
                    border: 1px solid var(--border);
                    transition: all 0.3s ease;
                }

                .archetype-card:hover {
                    background: rgba(0, 136, 204, 0.08);
                    border-color: var(--primary);
                    transform: translateX(5px);
                }

                .archetype-grid {
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                }

                iframe {
                    border-radius: 12px;
                    background: white;
                }

                .table {
                    color: var(--text-main) !important;
                    border-color: var(--border) !important;
                }

                .table thead th {
                    background: rgba(255,255,255,0.03);
                    border-bottom: 2px solid var(--border);
                    color: var(--text-muted);
                    font-size: 0.8rem;
                    text-transform: uppercase;
                }

                .table-striped tbody tr:nth-of-type(odd) {
                    background-color: rgba(255,255,255,0.01);
                }

                .user-list li {
                    background: rgba(255,255,255,0.03);
                    border: 1px solid var(--border);
                    border-radius: 10px;
                    padding: 10px 15px;
                    margin-bottom: 8px;
                    list-style: none;
                }

                .badge-premium {
                    background: var(--primary-glow);
                    color: var(--primary);
                    border: 1px solid var(--primary);
                }

                ::-webkit-scrollbar {
                    width: 8px;
                }
                ::-webkit-scrollbar-track {
                    background: var(--bg-dark);
                }
                ::-webkit-scrollbar-thumb {
                    background: var(--bg-card);
                    border-radius: 10px;
                }
                ::-webkit-scrollbar-thumb:hover {
                    background: var(--text-muted);
                }
            </style>
        </head>
        <body>
            <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
                <div class="container">
                    <a class="navbar-brand" href="#"><i class="fab fa-telegram"></i> INSIGHTS</a>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarNav">
                        <ul class="navbar-nav ms-auto">
                            <li class="nav-item"><a class="nav-link" href="#overview">Overview</a></li>
                            <li class="nav-item"><a class="nav-link" href="#user-activity">Users</a></li>
                            <li class="nav-item"><a class="nav-link" href="#activity-patterns">Patterns</a></li>
                            <li class="nav-item"><a class="nav-link" href="#content-analysis">Content</a></li>
                            <li class="nav-item"><a class="nav-link" href="#online-presence">Presence</a></li>
                            <li class="nav-item"><a class="nav-link" href="#intelligence">Intelligence</a></li>
                            <li class="nav-item"><a class="nav-link" href="#psychological">Wellness</a></li>
                            <li class="nav-item"><a class="nav-link" href="#social-dynamics">Social</a></li>
                            <li class="nav-item"><a class="nav-link" href="#thematic">Thematic</a></li>
                            <li class="nav-item"><a class="nav-link" href="#interaction">Interaction</a></li>
                            <li class="nav-item"><a class="nav-link" href="#interactive-viz">Interactive</a></li>
                        </ul>
                    </div>
                </div>
            </nav>
            <div class="container">
        """
    
    def _create_overview_section(self, basic_stats: Dict) -> str:
        """Create a premium overview section"""
        executive_summary = self.stats.get('executive_summary', '')
        
        html = f"""
        <div id="overview" class="section">
            <div class="executive-summary-banner mb-4 p-4" style="background: var(--glass); border-radius: 15px; border-left: 5px solid var(--primary); backdrop-filter: blur(10px); position: relative; overflow: hidden;">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <h4 style="color: var(--primary); font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;"><i class="fas fa-microchip"></i> Intelligence Summary</h4>
                        <p style="font-size: 1.1rem; margin-bottom: 0; font-weight: 500;">{executive_summary}</p>
                    </div>
                    <div class="stability-tag p-2 px-3" style="background: rgba(0, 255, 127, 0.1); border: 1px solid rgba(0, 255, 127, 0.2); border-radius: 30px; font-size: 0.8rem; font-weight: 700; color: #00ff7f;">
                        STABILITY: 100% SECURE
                    </div>
                </div>
            </div>
            
            <div class="premium-card">
                <div class="card-header">
                    <h2><i class="fas fa-rocket"></i> Executive Summary</h2>
                </div>
                <div class="card-body">
                    <div class="row g-4">
        """
        
        if basic_stats:
            stats_config = [
                ('total_messages', 'Total Messages', 'fa-comments'),
                ('total_participants', 'Active Users', 'fa-users'),
                ('total_days', 'Time Range (Days)', 'fa-calendar-alt'),
                ('avg_message_length', 'Avg. Length', 'fa-text-width')
            ]
            
            for key, label, icon in stats_config:
                val = basic_stats.get(key, 0)
                if key == 'total_days':
                    val = basic_stats.get('date_range', {}).get('total_days', 0)
                
                display_val = f"{val:,}" if isinstance(val, int) else f"{val:.1f}"
                
                html += f"""
                        <div class="col-md-3">
                            <div class="stat-box">
                                <i class="fas {icon}" style="color: var(--text-muted); margin-bottom: 12px;"></i>
                                <div class="stat-value">{display_val}</div>
                                <div class="stat-label">{label}</div>
                            </div>
                        </div>
                """
        
        html += """
                    </div>
                </div>
            </div>
        </div>
        """
        return html
    
    def _create_user_activity_section(self, user_stats: Dict, visualizations: List[str]) -> str:
        """Create a premium user activity section"""
        html = """
        <div id="user-activity" class="section">
            <div class="premium-card">
                <div class="card-header">
                    <h2><i class="fas fa-users"></i> User Intelligence</h2>
                </div>
                <div class="card-body">
        """
        
        if 'user_activity.png' in visualizations:
            html += """
                    <div class="viz-container">
                        <img src="user_activity.png" alt="User Activity" class="img-fluid w-100">
                    </div>
            """
        
        if user_stats:
            top_users = sorted(user_stats.items(), key=lambda x: x[1]['message_count'], reverse=True)[:5]
            
            html += """
                    <div class="mt-4">
                        <h3 class="mb-3" style="font-size: 1.1rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px;">Top Contributors</h3>
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead>
                                    <tr>
                                        <th>Participant</th>
                                        <th class="text-end">Activity</th>
                                        <th class="text-end" style="width: 200px;">Personality Profile (OCEAN)</th>
                                        <th class="text-end">Dominant Emotion</th>
                                    </tr>
                                </thead>
                                <tbody>
            """
            
            intel_all = self.stats.get('engagement_intelligence', {})
            for user, stats in top_users:
                user_dna = self.stats.get('user_dna', {}).get(user, "DNA-N/A")
                intel = intel_all.get(user, {})
                ocean = intel.get('ocean_profile', {})
                
                ocean_html = ""
                for trait, val in ocean.items():
                    color = "#0088cc"
                    if trait == 'Neuroticism': color = "#ff4d4d"
                    elif trait == 'Agreeableness': color = "#00ff7f"
                    ocean_html += f'<div style="font-size: 0.6rem; color: var(--text-muted); display: flex; justify-content: space-between;"><span>{trait[0]}</span><span>{val}%</span></div>'
                    ocean_html += f'<div class="progress mb-1" style="height: 4px; background: rgba(255,255,255,0.05);"><div class="progress-bar" style="width: {val}%; background: {color};"></div></div>'
                
                html += f"""
                                    <tr>
                                        <td style="font-weight: 600;">
                                            {user}
                                            <div style="font-size: 0.65rem; color: var(--primary); font-family: 'Courier New', monospace; letter-spacing: 1px;">{user_dna}</div>
                                        </td>
                                        <td class="text-end" style="color: var(--primary);">
                                            {stats.get('message_count', 0):,} msgs
                                            <div style="font-size: 0.7rem; color: var(--text-muted);">{stats.get('avg_message_length', 0):.1f} avg chars</div>
                                        </td>
                                        <td>
                                            {ocean_html}
                                        </td>
                                        <td class="text-end">
                                            <span class="badge" style="background: rgba(0, 136, 204, 0.2); color: var(--primary); border: 1px solid var(--primary);">{intel.get('dominant_emotion', 'Neutral')}</span>
                                        </td>
                                    </tr>
                """
            
            html += """
                                </tbody>
                            </table>
                        </div>
                    </div>
            """
        
        html += """
                </div>
            </div>
        </div>
        """
        return html
    
    def _create_activity_patterns_section(self, activity_patterns: Dict, visualizations: List[str]) -> str:
        """Create a premium activity patterns section"""
        html = """
        <div id="activity-patterns" class="section">
            <div class="premium-card">
                <div class="card-header">
                    <h2><i class="fas fa-wave-square"></i> Communication Patterns</h2>
                </div>
                <div class="card-body">
                    <div class="row g-4">
        """
        
        if activity_patterns:
            hourly = activity_patterns.get('hourly', {})
            daily = activity_patterns.get('daily', {})
            
            if hourly and daily:
                most_active_hour = max(hourly.items(), key=lambda x: x[1])
                most_active_day = max(daily.items(), key=lambda x: x[1])
                
                html += f"""
                        <div class="col-md-6">
                            <div class="stat-box">
                                <div class="stat-value" style="font-size: 1.5rem;">{most_active_hour[0]}:00</div>
                                <div class="stat-label">Peak Activity Hour</div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="stat-box">
                                <div class="stat-value" style="font-size: 1.5rem;">{most_active_day[0]}</div>
                                <div class="stat-label">Most Active Day</div>
                            </div>
                        </div>
                """
        
        for viz_file in ['activity_heatmap.png', 'weekly_activity.png', 'conversation_flow.png']:
            if viz_file in visualizations:
                html += f"""
                    <div class="col-12">
                        <div class="viz-container">
                            <img src="{viz_file}" alt="{viz_file}" class="img-fluid w-100">
                        </div>
                    </div>
                """
        
        html += """
                    </div>
                </div>
            </div>
        </div>
        """
        return html
    
    def _create_content_analysis_section(self, visualizations: List[str]) -> str:
        """Create a premium content analysis section"""
        html = """
        <div id="content-analysis" class="section">
            <div class="premium-card">
                <div class="card-header">
                    <h2><i class="fas fa-microchip"></i> Semantic Analysis</h2>
                </div>
                <div class="card-body">
                    <div class="row g-4">
        """
        
        # Grid layout for content viz
        content_viz = [
            ('wordcloud.png', 'Vocabulary Cloud'),
            ('word_frequency.png', 'Word Frequency'),
            ('sentiment_distribution.png', 'Emotional Landscape'),
            ('topic_clusters.png', 'Thematic Clusters'),
            ('media_distribution.png', 'Media Mix')
        ]
        
        for file, title in content_viz:
            if file in visualizations:
                html += f"""
                        <div class="col-md-6">
                            <h4 style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 15px;">{title}</h4>
                            <div class="viz-container">
                                <img src="{file}" alt="{title}" class="img-fluid w-100">
                            </div>
                        </div>
                """
        
        html += """
                    </div>
                </div>
            </div>
        </div>
        """
        return html
    
    def _create_online_presence_section(self, online_presence: Dict, visualizations: List[str]) -> str:
        """Create a premium online presence analysis section"""
        html = """
        <div id="online-presence" class="section">
            <div class="premium-card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h2><i class="fas fa-user-clock"></i> Behavioral Intelligence</h2>
                    <a href="online_presence/online_presence_report.html" target="_blank" class="btn-premium btn-sm">
                        Detailed View <i class="fas fa-external-link-alt"></i>
                    </a>
                </div>
                <div class="card-body">
        """
        
        if online_presence:
            html += """<div class="row g-4 mb-4">"""
            
            # Key Metrics
            metrics = [
                ('most_active_user_days', 'Power User', lambda d: d['user']),
                ('least_active_user_days', 'Ghost Participant', lambda d: d['user']),
                ('most_active_day', 'Peak Traffic Day', lambda d: d),
                ('least_active_day', 'Quiet Day', lambda d: d)
            ]
            
            for key, label, formatter in metrics:
                if key in online_presence:
                    html += f"""
                        <div class="col-md-3">
                            <div class="stat-box">
                                <div class="stat-value" style="font-size: 1.2rem;">{formatter(online_presence[key])}</div>
                                <div class="stat-label">{label}</div>
                            </div>
                        </div>
                    """
            
            if 'fastest_responders' in online_presence:
                html += f"""
                    <div class="col-12">
                        <div class="stat-box mt-3" style="text-align: left; background: rgba(0, 136, 204, 0.05);">
                            <div style="font-size: 0.8rem; text-transform: uppercase; color: var(--text-muted); margin-bottom: 10px;">Response Speed Intelligence</div>
                            <div class="d-flex justify-content-between">
                                {" ".join([f'<div class="px-3 border-end border-secondary"><strong>{u}</strong><br><span style="color: var(--primary);">{l:.1f}m</span></div>' for u, l in online_presence.get('fastest_responders', [])])}
                            </div>
                        </div>
                    </div>
                """
            
            html += """</div>"""
            
            # Visualizations
            for viz_file in ['presence_heatmap.png', 'user_activity_heatmap.png', 'user_time_preferences.png']:
                if viz_file in visualizations:
                    title = ' '.join(viz_file.replace('.png', '').split('_')).title()
                    html += f"""
                        <div class="mt-4">
                            <h4 style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 15px;">{title}</h4>
                            <div class="viz-container">
                                <img src="{viz_file}" class="img-fluid w-100" alt="{title}">
                            </div>
                        </div>
                    """
            
            # Response Network
            if 'user_response_network.png' in visualizations:
                html += """
                        <div class="mt-4">
                            <h4 style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 15px;">Interaction Dynamics</h4>
                            <div class="viz-container">
                                <img src="user_response_network.png" class="img-fluid w-100" alt="Response Network">
                            </div>
                        </div>
                """

        html += """
                </div>
            </div>
        </div>
        """
        return html
    
    def _create_intelligence_section(self, visualizations: List[str]) -> str:
        """Create a premium intelligence and engagement section"""
        intelligence = self.stats.get('engagement_intelligence', {})
        bursts = self.stats.get('conversation_bursts', [])
        
        html = """
        <div id="intelligence" class="section">
            <div class="premium-card">
                <div class="card-header">
                    <h2><i class="fas fa-brain"></i> Advanced Intelligence</h2>
                </div>
                <div class="card-body">
                    <div class="row g-4">
        """
        
        # Velocity chart
        if 'chat_velocity.png' in visualizations:
            html += """
                        <div class="col-12">
                            <h4 style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 15px;">Conversation Momentum</h4>
                            <div class="viz-container">
                                <img src="chat_velocity.png" class="img-fluid w-100" alt="Chat Velocity">
                            </div>
                        </div>
            """
            
        # Engagement ranks
        if 'engagement_intelligence.png' in visualizations:
            html += """
                        <div class="col-md-7">
                            <h4 style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 15px;">Engagement Rankings</h4>
                            <div class="viz-container">
                                <img src="engagement_intelligence.png" class="img-fluid w-100" alt="Engagement Intel">
                            </div>
                        </div>
            """
        
        # User Archetypes
        if intelligence:
            top_users = sorted(intelligence.items(), key=lambda x: x[1]['engagement_score'], reverse=True)[:6]
            html += """
                        <div class="col-md-5">
                            <h4 style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 15px;">User Archetypes</h4>
                            <div class="archetype-grid">
            """
            
            for user, data in top_users:
                archetype_icon = {
                    "Main Protagonist": "fa-star",
                    "The Optimist": "fa-smile",
                    "The Critic": "fa-exclamation-triangle",
                    "Media Maven": "fa-camera",
                    "The Storyteller": "fa-book",
                    "Quiet Observer": "fa-eye",
                    "Neutral": "fa-user"
                }.get(data['archetype'], "fa-user")
                
                html += f"""
                                <div class="archetype-card" style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 10px; margin-bottom: 10px; border: 1px solid var(--border);">
                                    <div class="d-flex align-items-center">
                                        <div style="width: 40px; height: 40px; border-radius: 50%; background: var(--primary-glow); display: flex; align-items: center; justify-content: center; margin-right: 12px;">
                                            <i class="fas {archetype_icon}" style="color: var(--primary);"></i>
                                        </div>
                                        <div>
                                            <div style="font-weight: 600; font-size: 0.9rem;">{user}</div>
                                            <div style="font-size: 0.75rem; color: var(--text-muted);">{data['archetype']} • {data['vibe']} Vibe</div>
                                        </div>
                                        <div class="ms-auto">
                                            <span class="badge badge-premium">{data['engagement_score']}</span>
                                        </div>
                                    </div>
                                </div>
                """
            html += """
                            </div>
                        </div>
            """

        # Conversation Bursts
        if bursts:
            html += """
                        <div class="col-12 mt-4">
                            <h4 style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 15px;">Intensity Bursts</h4>
                            <div class="table-responsive">
                                <table class="table table-hover">
                                    <thead>
                                        <tr>
                                            <th>Time Period</th>
                                            <th class="text-end">Messages</th>
                                            <th class="text-end">Participants</th>
                                            <th class="text-end">Intensity</th>
                                        </tr>
                                    </thead>
                                    <tbody>
            """
            
            for burst in bursts:
                try:
                    # Handle multiple date formats safely
                    s_str = burst['start_time'].replace('T', ' ').split('.')[0]
                    e_str = burst['end_time'].replace('T', ' ').split('.')[0]
                    start = datetime.strptime(s_str, '%Y-%m-%d %H:%M:%S')
                    end = datetime.strptime(e_str, '%Y-%m-%d %H:%M:%S')
                    duration = max(1, (end - start).total_seconds() / 60)
                    intensity = round(burst['message_count'] / duration, 1)
                    
                    html += f"""
                                        <tr>
                                            <td>{start.strftime('%b %d, %H:%M')} - {end.strftime('%H:%M')}</td>
                                            <td class="text-end">{burst['message_count']}</td>
                                            <td class="text-end">{burst['participants']}</td>
                                            <td class="text-end"><span class="badge" style="background: rgba(0,136,204,0.1); color: var(--primary);">{intensity} msg/min</span></td>
                                        </tr>
                """
                except Exception as e:
                    self.logger.warning(f"Error rendering burst: {e}")
                    continue
                
            html += """
                                    </tbody>
                                </table>
                            </div>
                        </div>
            """
            
        html += """
                    </div>
                </div>
            </div>
        </div>
        """
        return html

    def _create_psychological_section(self, visualizations: List[str]) -> str:
        """Create a premium psychological and emotional health section"""
        psych = self.stats.get('psychological_stats', {})
        
        html = """
        <div id="psychological" class="section">
            <div class="premium-card">
                <div class="card-header">
                    <h2><i class="fas fa-heartbeat"></i> Psychological & Emotional Wellness</h2>
                </div>
                <div class="card-body">
                    <div class="row g-4">
        """
        
        # Wellbeing timeline
        if 'psychological_wellbeing.png' in visualizations:
            html += """
                        <div class="col-12">
                            <h4 style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 15px;">Wellbeing & Care Timeline</h4>
                            <div class="viz-container">
                                <img src="psychological_wellbeing.png" class="img-fluid w-100" alt="Psych Wellbeing">
                            </div>
                        </div>
            """
            
        # Mood Intensity
        if 'mood_intensity.png' in visualizations:
            html += """
                        <div class="col-md-7">
                            <h4 style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 15px;">Emotional Pulse (Mood Heatmap)</h4>
                            <div class="viz-container">
                                <img src="mood_intensity.png" class="img-fluid w-100" alt="Mood Intensity">
                            </div>
                        </div>
            """
            
        # Specific Stats
        if psych:
            html += """
                        <div class="col-md-5">
                            <h4 style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 15px;">Emotional Breakdown</h4>
                            <div class="d-flex flex-column gap-3">
            """
            
            # Health Box
            html += f"""
                                <div class="p-3" style="background: rgba(255, 77, 77, 0.05); border: 1px solid rgba(255, 77, 77, 0.1); border-radius: 12px;">
                                    <div class="d-flex justify-content-between align-items-center mb-2">
                                        <span style="font-weight: 700; color: #ff4d4d;"><i class="fas fa-medkit"></i> Health & Wellness</span>
                                        <span class="badge" style="background: #ff4d4d;">{psych['health']['total_mentions']} Mentions</span>
                                    </div>
                                    <div style="font-size: 0.85rem; color: var(--text-muted);">
                                        Concern for wellbeing and physical health indicators detected in discourse.
                                    </div>
                                </div>
            """
            
            # Care Box
            html += f"""
                                <div class="p-3" style="background: rgba(255, 51, 153, 0.05); border: 1px solid rgba(255, 51, 153, 0.1); border-radius: 12px;">
                                    <div class="d-flex justify-content-between align-items-center mb-2">
                                        <span style="font-weight: 700; color: #ff3399;"><i class="fas fa-heart"></i> Love & Care</span>
                                        <span class="badge" style="background: #ff3399;">{psych['love_and_care']['total_mentions']} Mentions</span>
                                    </div>
                                    <div style="font-size: 0.85rem; color: var(--text-muted);">
                                        High levels of empathy, support, and affection detected between participants.
                                    </div>
                                </div>
            """
            
            # Mood Intensity Box
            html += f"""
                                <div class="p-3" style="background: rgba(0, 136, 204, 0.05); border: 1px solid rgba(0, 136, 204, 0.1); border-radius: 12px;">
                                    <div class="d-flex justify-content-between align-items-center mb-2">
                                        <span style="font-weight: 700; color: var(--primary);"><i class="fas fa-vial"></i> Emotional Intensity</span>
                                        <span class="badge" style="background: var(--primary);">{psych['emotional_pulse']['avg_intensity']:.2f} Score</span>
                                    </div>
                                    <div style="font-size: 0.85rem; color: var(--text-muted);">
                                        Average emotional volatility and "mood energy" across all interactions.
                                    </div>
                                </div>
            """
            
            # Add Health Issue Tracking if available
            health_tracking = psych.get('health_tracking', {})
            if health_tracking:
                html += """
                        <div class="col-md-12 mt-4">
                            <h4 style="font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 15px; letter-spacing: 1px;">Clinical Issue Tracking</h4>
                            <div class="row g-3">
                                <div class="col-md-4">
                                    <div class="p-3" style="background: rgba(255, 77, 77, 0.05); border: 1px solid rgba(255, 77, 77, 0.1); border-radius: 12px;">
                                        <div style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase;">Acute Episodes</div>
                                        <div style="font-size: 1.4rem; font-weight: 700; color: #ff4d4d;">{0}</div>
                                        <div style="font-size: 0.7rem; color: var(--text-muted);">Infections / Emergencies</div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="p-3" style="background: rgba(0, 136, 204, 0.05); border: 1px solid rgba(0, 136, 204, 0.1); border-radius: 12px;">
                                        <div style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase;">Chronic Mgmt</div>
                                        <div style="font-size: 1.4rem; font-weight: 700; color: #0088cc;">{1}</div>
                                        <div style="font-size: 0.7rem; color: var(--text-muted);">Ongoing Monitoring</div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="p-3" style="background: var(--glass); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px;">
                                        <div style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase;">Tracking Pulse</div>
                                        <div style="font-size: 1.4rem; font-weight: 700; color: white;">{2}</div>
                                        <div style="font-size: 0.7rem; color: var(--text-muted);">Active Health Dates</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                """.format(
                    health_tracking.get('acute_episodes', 0),
                    health_tracking.get('chronic_management', 0),
                    len(health_tracking.get('health_velocity', {}))
                )
            
            html += """
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        return html

    def _create_social_dynamics_section(self, visualizations: List[str]) -> str:
        """Create a premium social dynamics and harmony section"""
        social = self.stats.get('social_dynamics', {})
        
        html = """
        <div id="social-dynamics" class="section">
            <div class="premium-card">
                <div class="card-header">
                    <h2><i class="fas fa-users-rays"></i> Social Dynamics & Harmony</h2>
                </div>
                <div class="card-body">
                    <div class="row g-4">
        """
        
        if social:
            # Relationship Summary
            html += """
                        <div class="col-md-5">
                            <h4 style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 15px;">Relationship Metrics</h4>
                            <div class="d-flex flex-column gap-3">
            """
            
            # Most Harmonious
            if 'most_harmonious' in social and social['most_harmonious']:
                pair, score = social['most_harmonious']
                html += f"""
                                <div class="p-3" style="background: rgba(0, 255, 127, 0.05); border: 1px solid rgba(0, 255, 127, 0.1); border-radius: 12px;">
                                    <div class="d-flex justify-content-between align-items-center mb-1">
                                        <span style="font-weight: 700; color: #00ff7f;"><i class="fas fa-handshake"></i> Most Harmonious</span>
                                    </div>
                                    <div style="font-size: 0.95rem; font-weight: 600;">{pair}</div>
                                    <div style="font-size: 0.8rem; color: var(--text-muted);">Confidence Score: {score:.2f}</div>
                                </div>
                """
                
            # Most Combative/Intense
            if 'most_combative' in social and social['most_combative']:
                pair, score = social['most_combative']
                html += f"""
                                <div class="p-3" style="background: rgba(255, 165, 0, 0.05); border: 1px solid rgba(255, 165, 0, 0.1); border-radius: 12px;">
                                    <div class="d-flex justify-content-between align-items-center mb-1">
                                        <span style="font-weight: 700; color: #ffa500;"><i class="fas fa-bolt"></i> High Intensity Pair</span>
                                    </div>
                                    <div style="font-size: 0.95rem; font-weight: 600;">{pair}</div>
                                    <div style="font-size: 0.8rem; color: var(--text-muted);">Intensity Delta: {abs(score):.2f}</div>
                                </div>
                """
                
            html += """
                            </div>
                        </div>
            """
            
            # Harmony Matrix visualization
            if 'user_interaction_network.png' in visualizations:
                html += """
                        <div class="col-md-7">
                            <h4 style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 15px;">Interaction Proximity Map</h4>
                            <div class="viz-container">
                                <img src="user_interaction_network.png" class="img-fluid w-100" alt="Interaction Network">
                            </div>
                        </div>
                """
                
        html += """
                    </div>
                </div>
            </div>
        </div>
        """
        return html

    def _create_interactive_viz_section(self, interactive_viz: List[str]) -> str:
        """Create a section for interactive HTML visualizations"""
        html = """
        <div id="interactive-viz" class="section">
            <div class="premium-card">
                <div class="card-header">
                    <h2><i class="fas fa-mouse-pointer"></i> Interactive Deep Dive</h2>
                </div>
                <div class="card-body">
                    <p style="color: var(--text-muted); margin-bottom: 24px;">Explore these interactive visualizations in your browser. These allow you to zoom, hover, and filter specific data points.</p>
                    <div class="row g-4">
        """
        
        for viz_file in interactive_viz:
            title = ' '.join(viz_file.replace('.html', '').split('_')).title()
            html += f"""
                        <div class="col-md-6">
                            <h4 style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 15px;">{title}</h4>
                            <div class="viz-container" style="height: 500px; overflow: hidden;">
                                <iframe src="interactive/{viz_file}" style="width: 100%; height: 100%; border: none;"></iframe>
                            </div>
                        </div>
            """
            
        html += """
                    </div>
                </div>
            </div>
        </div>
        """
        return html

    def _create_thematic_landscape_section(self) -> str:
        """Create a premium thematic landscape and semantic mapping section"""
        concepts = self.stats.get('semantic_concepts', [])
        
        html = """
        <div id="thematic" class="section">
            <div class="premium-card">
                <div class="card-header">
                    <h2><i class="fas fa-microscope"></i> Thematic Landscape</h2>
                </div>
                <div class="card-body">
                    <p style="color: var(--text-muted); margin-bottom: 30px;">Algorithmic extraction of recurrent semantic clusters and conceptual bigrams within the discourse.</p>
                    <div class="d-flex flex-wrap gap-3">
        """
        
        for i, item in enumerate(concepts):
            size = 1.4 - (i * 0.05)
            opacity = 1.0 - (i * 0.05)
            html += f"""
                        <div class="concept-chip p-3" style="background: rgba(0, 136, 204, {opacity * 0.1}); border: 1px solid rgba(0, 136, 204, {opacity * 0.2}); border-radius: 12px; font-size: {size}rem; font-weight: 600; color: rgba(255, 255, 255, {opacity});">
                            {item['concept']}
                            <span style="font-size: 0.7rem; color: var(--primary); margin-left: 8px;">{item['relevance']}x</span>
                        </div>
            """
            
        html += """
                    </div>
                </div>
            </div>
        </div>
        """
        return html

    def _create_interaction_section(self, visualizations: List[str]) -> str:
        """Create a premium interaction analysis section"""
        html = """
        <div id="interaction" class="section">
            <div class="premium-card">
                <div class="card-header">
                    <h2><i class="fas fa-project-diagram"></i> Network Dynamics</h2>
                </div>
                <div class="card-body">
                    <div class="row g-4">
        """
        
        interaction_viz = [
            ('user_interaction_network.png', 'Social Connection Graph'),
            ('response_time_analysis.png', 'Latency Distribution'),
            ('emoji_usage.png', 'Expressive Landscape')
        ]
        
        found = False
        for file, title in interaction_viz:
            if file in visualizations:
                found = True
                html += f"""
                        <div class="col-md-6">
                            <h4 style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 15px;">{title}</h4>
                            <div class="viz-container">
                                <img src="{file}" alt="{title}" class="img-fluid w-100">
                            </div>
                        </div>
                """
        
        if not found:
            html += """<div class="col-12 text-center text-muted py-5">Advanced network metrics currently unavailable.</div>"""
            
        html += """
                    </div>
                </div>
            </div>
        </div>
        """
        return html
    
    def _create_footer(self) -> str:
        """Create a premium footer with smooth scrolling"""
        return f"""
            </div>
            
            <footer style="margin-top: 80px; padding: 60px 0; border-top: 1px solid var(--border); text-align: center;">
                <div class="container">
                    <p style="color: var(--text-muted); font-size: 0.9rem;">Intelligence Report Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                    <p style="color: var(--primary); font-weight: 800; margin-top: 10px; letter-spacing: 2px;">TELEGRAM ANALYZER PRO</p>
                </div>
            </footer>

            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
            <script>
                document.querySelectorAll('nav a.nav-link').forEach(anchor => {{
                    anchor.addEventListener('click', function(e) {{
                        e.preventDefault();
                        const targetId = this.getAttribute('href');
                        const targetElement = document.querySelector(targetId);
                        window.scrollTo({{
                            top: targetElement.offsetTop - 80,
                            behavior: 'smooth'
                        }});
                    }});
                }});
            </script>
        </body>
        </html>
        """