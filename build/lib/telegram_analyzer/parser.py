"""
Parser for Telegram export JSON data.
"""

import json
import pandas as pd
import logging
from typing import Dict
from tqdm import tqdm
from nltk.sentiment import SentimentIntensityAnalyzer
from .utils import extract_text_from_message, has_emoji, has_link
import re

class TelegramDataParser:
    """Parser for Telegram export JSON data"""
    
    def __init__(self, json_file: str):
        self.logger = logging.getLogger(__name__)
        self.json_file = json_file
        self.raw_data = self._load_json()
        self.chat_info = self._extract_chat_info()
        
        # Pre-compile regex for performance with expanded medical lexicon
        self.health_pattern = re.compile(
            r'\b(sick|pain|doctor|medicine|exercise|sleep|hospital|fever|cold|workout|diet|gym|wellness|ill|ache|clinic|therapy|'
            r'headache|nausea|fatigue|cough|dizzy|blood pressure|diabetes|asthma|anxiety|depression|insomnia|'
            r'surgery|emergency|ambulance|rehab|symptom|prescription|meds|dose|vaccine|allergy|injury|fracture|sprain|'
            r'covid|flu|virus|infection|biopsy|scan|xray|mri|consultation|specialist|pharmacy)\b', 
            re.IGNORECASE
        )
        self.care_pattern = re.compile(
            r'\b(love|care|miss|hug|kiss|dear|sweet|heart|help|support|honey|darling|adore|cherish|grateful|appreciate|respect|kind|'
            r'stay strong|take care|get well|healing|praying|thinking of you|here for you|comfort|sympathy|empathy|solidarity)\b', 
            re.IGNORECASE
        )

    def _load_json(self) -> Dict:
        """Load and validate JSON data"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self._validate_json_structure(data)
            return data
        except Exception as e:
            self.logger.error(f"Error loading JSON file: {str(e)}")
            raise

    def _validate_json_structure(self, data: Dict):
        """Validate the JSON structure meets Telegram export format"""
        required_fields = ['name', 'type', 'id', 'messages']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Invalid JSON structure: missing '{field}' field")

    def _extract_chat_info(self) -> Dict:
        """Extract chat metadata"""
        return {
            'name': self.raw_data['name'],
            'type': self.raw_data['type'],
            'id': self.raw_data['id'],
            'messages_count': len(self.raw_data['messages'])
        }

    def process_messages(self) -> pd.DataFrame:
        """Process all messages and convert to DataFrame"""
        messages_list = []
        
        try:
            for msg in tqdm(self.raw_data['messages'], desc="Processing messages"):
                if not isinstance(msg, dict):
                    continue
                    
                processed_msg = self._process_single_message(msg)
                if processed_msg:
                    messages_list.append(processed_msg)
            
            df = pd.DataFrame(messages_list)
            
            # Convert date strings to datetime objects
            df['date'] = pd.to_datetime(df['date'])
            
            # Add sentiment analysis
            sia = SentimentIntensityAnalyzer()
            df['sentiment_scores'] = df['text'].apply(
                lambda x: sia.polarity_scores(str(x)) if pd.notnull(x) else None
            )
            df['sentiment'] = df['sentiment_scores'].apply(
                lambda x: x['compound'] if x is not None else None
            )
            
            # Add detailed emotional categories (Vectorized or optimized)
            df['health_mentions'] = df['text'].apply(lambda x: bool(self.health_pattern.search(str(x))) if pd.notnull(x) else False)
            df['care_mentions'] = df['text'].apply(lambda x: bool(self.care_pattern.search(str(x))) if pd.notnull(x) else False)
            df['mood_intensity'] = df['sentiment_scores'].apply(lambda x: (x['pos'] + x['neg']) if x is not None else 0)
            
            # Sort by date and reset index
            df = df.sort_values('date').reset_index(drop=True)
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error processing messages: {str(e)}")
            raise

    def _detect_category(self, text: str, pattern: re.Pattern) -> bool:
        """Detect if text contains any keywords from a category pattern"""
        if not text or text == 'None':
            return False
        return bool(pattern.search(text))

    def _process_single_message(self, msg: Dict) -> Dict:
        """Process a single message and extract relevant information"""
        try:
            # Extract basic message info
            processed = {
                'message_id': msg.get('id', None),
                'date': msg.get('date', None),
                'from': msg.get('from', None),
                'type': msg.get('type', None),
                'text': extract_text_from_message(msg),
                'media_type': msg.get('media_type', None),
                'file': msg.get('file', None),
                'reply_to_message_id': msg.get('reply_to_message_id', None),
                'forwarded_from': msg.get('forwarded_from', None),
            }

            text = extract_text_from_message(msg)
            if text:
                processed.update({
                    'text_length': len(text),
                    'word_count': len(text.split()),
                    'has_emoji': has_emoji(text),
                    'has_link': has_link(text)
                })

            return processed

        except Exception as e:
            self.logger.warning(f"Error processing message: {str(e)}")
            return None
