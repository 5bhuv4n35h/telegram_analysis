#!/usr/bin/env python3
"""
Telegram HTML Format Specific Converter

This script is tailored specifically for the Telegram HTML export format
with proper handling of date formats and message structures.
Optimized to handle very large chats with 10,000+ messages.

Usage:
    python telegram_html_to_json.py /path/to/folder -o output.json -c -v -f
    
The script will process all HTML files in the specified folder and save
a combined JSON file to the output path.
"""

import os
import re
import json
import argparse
import logging
import sys
import tempfile
import shutil
import traceback
import gc
from typing import Dict, List, Optional, Tuple, Generator, Iterator
from datetime import datetime
from bs4 import BeautifulSoup, Tag
from glob import glob

# Add main execution code
def process_folder(folder_path: str, output_path: str, combine: bool = False, 
                  force: bool = False, verbose: bool = False) -> None:
    """
    Process all HTML files in a folder.
    
    Args:
        folder_path: Path to folder containing HTML files
        output_path: Path to save JSON output
        combine: Whether to combine all files into one JSON
        force: Whether to overwrite existing files
        verbose: Whether to enable verbose logging
    """
    # Set log level
    if verbose:
        logger.setLevel(logging.DEBUG)
    
    try:
        # Make sure the folder exists
        if not os.path.isdir(folder_path):
            logger.error(f"Folder not found: {folder_path}")
            raise
        
def main():
    """Main function to handle command line arguments and execute the script"""
    # Create argument parser
    parser = argparse.ArgumentParser(
        description="Convert Telegram HTML exports to JSON format",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Add arguments
    parser.add_argument(
        "folder", 
        help="Path to folder containing HTML files"
    )
    parser.add_argument(
        "-o", "--output", 
        default="output.json", 
        help="Path to save JSON output"
    )
    parser.add_argument(
        "-c", "--combine", 
        action="store_true", 
        help="Combine all files into one JSON"
    )
    parser.add_argument(
        "-f", "--force", 
        action="store_true", 
        help="Force overwrite of existing files"
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Enable verbose logging"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        # Process folder
        process_folder(
            args.folder,
            args.output,
            args.combine,
            args.force,
            args.verbose
        )
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() FileNotFoundError(f"Folder not found: {folder_path}")
        
        # Find all HTML files in the folder
        html_files = glob(os.path.join(folder_path, "*.html"))
        if not html_files:
            logger.error(f"No HTML files found in {folder_path}")
            raise FileNotFoundError(f"No HTML files found in {folder_path}")
        
        logger.info(f"Found {len(html_files)} HTML files to process")
        
        # Check if output file exists and force flag is not set
        if os.path.exists(output_path) and not force:
            logger.error(f"Output file {output_path} already exists. Use -f to overwrite.")
            raise FileExistsError(f"Output file {output_path} already exists")
        
        # Process files
        if combine:
            # Combine all files into one JSON
            logger.info(f"Combining {len(html_files)} files into {output_path}")
            
            # Create combined data structure
            combined_data = {
                'name': "Combined Telegram Export",
                'type': "combined",
                'id': 0,
                'chats': []
            }
            
            # Process each file
            for html_file in html_files:
                logger.info(f"Processing {os.path.basename(html_file)}")
                try:
                    converter = TelegramHTMLConverter(html_file)
                    chat_data = converter.convert_to_dict()
                    combined_data['chats'].append(chat_data)
                except Exception as e:
                    logger.error(f"Error processing {html_file}: {str(e)}")
                    logger.debug(traceback.format_exc())
            
            # Write combined JSON
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(combined_data, f, ensure_ascii=False, indent=2, default=str)
            
            logger.info(f"Successfully combined {len(html_files)} files into {output_path}")
            
        else:
            # Process each file individually
            if len(html_files) > 1 and os.path.splitext(output_path)[1]:
                # If multiple files and output is a single file, append file index
                logger.warning("Multiple HTML files found but output is a single file. Will append index to output files.")
                
                for i, html_file in enumerate(html_files):
                    # Create output path with index
                    base, ext = os.path.splitext(output_path)
                    indexed_output = f"{base}_{i+1}{ext}"
                    
                    logger.info(f"Processing {os.path.basename(html_file)} -> {indexed_output}")
                    try:
                        converter = TelegramHTMLConverter(html_file)
                        converter.convert_to_json(indexed_output)
                    except Exception as e:
                        logger.error(f"Error processing {html_file}: {str(e)}")
                        logger.debug(traceback.format_exc())
            else:
                # Single file or output is a directory
                out_dir = output_path if os.path.isdir(output_path) else os.path.dirname(output_path)
                os.makedirs(out_dir, exist_ok=True)
                
                for html_file in html_files:
                    # Create output file path
                    if os.path.isdir(output_path):
                        base_name = os.path.splitext(os.path.basename(html_file))[0]
                        out_file = os.path.join(output_path, f"{base_name}.json")
                    else:
                        out_file = output_path
                    
                    logger.info(f"Processing {os.path.basename(html_file)} -> {out_file}")
                    try:
                        converter = TelegramHTMLConverter(html_file)
                        converter.convert_to_json(out_file)
                    except Exception as e:
                        logger.error(f"Error processing {html_file}: {str(e)}")
                        logger.debug(traceback.format_exc())
                        
    except Exception as e:
        logger.error(f"Error processing folder: {str(e)}")
        logger.debug(traceback.format_exc())
        raise

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TelegramConverter")

class TelegramHTMLConverter:
    """Converter for Telegram HTML exports in the specific format from the sample"""
    
    # Class variable to cache media files by directory
    _media_cache = {}
    
    def __init__(self, html_file_path: str):
        """
        Initialize the converter with the HTML file.
        
        Args:
            html_file_path: Path to the Telegram HTML export file
        """
        try:
            self.html_file_path = os.path.abspath(html_file_path)
            self.export_dir = os.path.dirname(self.html_file_path)
            logger.info(f"Initializing converter for file: {self.html_file_path}")
            
            # Don't load the entire HTML file into memory at once for large files
            self.soup = None
            self.file_size = os.path.getsize(self.html_file_path)
            if self.file_size > 10 * 1024 * 1024:  # 10 MB threshold
                logger.info(f"Large file detected ({self.file_size / (1024*1024):.2f} MB). Using chunked processing.")
                # We'll load the HTML later in chunks
            else:
                # Small enough file, load normally
                self.soup = self._load_html()
            
            # Initialize media files dictionary - using cache for performance
            self.media_files = self._get_media_files()
            logger.info(f"Found {len(self.media_files)} media files")
        except Exception as e:
            logger.error(f"Error initializing converter: {str(e)}")
            logger.debug(traceback.format_exc())
            raise
    
    def _load_html(self) -> BeautifulSoup:
        """Load HTML content from file and parse it"""
        try:
            with open(self.html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            return BeautifulSoup(html_content, 'html.parser')
        except UnicodeDecodeError:
            # Try with a different encoding if utf-8 fails
            logger.warning("UTF-8 decoding failed, trying with ISO-8859-1 encoding")
            with open(self.html_file_path, 'r', encoding='iso-8859-1') as f:
                html_content = f.read()
            return BeautifulSoup(html_content, 'html.parser')
        except PermissionError:
            logger.error(f"Permission denied when reading {self.html_file_path}. Check file permissions.")
            raise
        except Exception as e:
            logger.error(f"Error loading HTML file: {str(e)}")
            logger.debug(traceback.format_exc())
            raise
    
    def _get_media_files(self) -> Dict[str, str]:
        """
        Get media files in the export directory, using cache if available.
        
        Returns:
            Dictionary mapping relative paths to absolute paths
        """
        try:
            # Check if we already scanned this directory
            if self.export_dir in TelegramHTMLConverter._media_cache:
                logger.debug(f"Using cached media files for {self.export_dir}")
                return TelegramHTMLConverter._media_cache[self.export_dir]
            
            # Otherwise scan the directory and cache the results
            media_files = self._find_media_files()
            TelegramHTMLConverter._media_cache[self.export_dir] = media_files
            return media_files
        except Exception as e:
            logger.warning(f"Error finding media files: {str(e)}. Continuing without media.")
            logger.debug(traceback.format_exc())
            return {}
        
    def _find_media_files(self) -> Dict[str, str]:
        """
        Find media files in the export directory.
        
        Returns:
            Dictionary mapping relative paths to absolute paths
        """
        media_files = {}
        
        # Common media directories in Telegram exports
        media_dirs = [
            os.path.join(self.export_dir, "files"),
            os.path.join(self.export_dir, "photos"),
            os.path.join(self.export_dir, "video_files"),
            os.path.join(self.export_dir, "voice_messages"),
            os.path.join(self.export_dir, "audio_files"),
            os.path.join(self.export_dir, "stickers"),
        ]
        
        # Find all files in media directories
        for media_dir in media_dirs:
            if os.path.isdir(media_dir):
                try:
                    for root, _, files in os.walk(media_dir):
                        for filename in files:
                            file_path = os.path.join(root, filename)
                            
                            # Create relative path for matching with HTML references
                            rel_path = os.path.relpath(file_path, self.export_dir)
                            
                            # Store path mappings
                            media_files[rel_path] = file_path
                            media_files[rel_path.replace('\\', '/')] = file_path
                            media_files[filename] = file_path
                except PermissionError:
                    logger.warning(f"Permission denied when accessing {media_dir}. Skipping.")
                except Exception as e:
                    logger.warning(f"Error accessing {media_dir}: {str(e)}. Skipping.")
        
        return media_files
    
    def _resolve_media_path(self, relative_path: str) -> Optional[str]:
        """
        Resolve relative media path to absolute path if it exists in the media files.
        
        Args:
            relative_path: Relative path from HTML
            
        Returns:
            Absolute path if found, otherwise None
        """
        if not relative_path:
            return None
            
        # Clean up path
        relative_path = relative_path.split('#')[0].split('?')[0]
        
        # Try to find in media files
        if relative_path in self.media_files:
            return self.media_files[relative_path]
        
        # Try with normalized slashes
        normalized_path = relative_path.replace('\\', '/')
        if normalized_path in self.media_files:
            return self.media_files[normalized_path]
        
        # Try with just filename
        filename = os.path.basename(relative_path)
        if filename in self.media_files:
            return self.media_files[filename]
        
        # Check if it's an absolute path that exists
        if os.path.isfile(relative_path):
            return relative_path
            
        # Try checking if file exists relative to export directory
        full_path = os.path.join(self.export_dir, relative_path)
        if os.path.isfile(full_path):
            return full_path
            
        return None
    
    def _parse_date(self, date_str: str, title_str: Optional[str] = None, base_date: Optional[str] = None) -> str:
        """
        Parse date string from the Telegram export.
        
        Args:
            date_str: Date string (like "18:47")
            title_str: Title attribute with full date (like "18.02.2025 18:47:00 UTC+05:30")
            base_date: Base date string (YYYY-MM-DD) to use if only time is available
            
        Returns:
            ISO format date string
        """
        try:
            if title_str:
                # Extract date from title attribute (preferred method)
                match = re.search(r'(\d{2})\.(\d{2})\.(\d{4})\s+(\d{2}):(\d{2}):(\d{2})', title_str)
                if match:
                    day, month, year, hour, minute, second = map(int, match.groups())
                    dt = datetime(year, month, day, hour, minute, second)
                    return dt.isoformat()
            
            # If only the base_date and time are available
            if base_date and date_str:
                match = re.search(r'(\d{2}):(\d{2})', date_str)
                if match:
                    hour, minute = map(int, match.groups())
                    year, month, day = map(int, base_date.split('-'))
                    dt = datetime(year, month, day, hour, minute, 0)
                    return dt.isoformat()
            
            # Fallback: use current time if all parsing fails
            return datetime.now().isoformat()
        except Exception as e:
            logger.warning(f"Error parsing date '{date_str}': {str(e)}. Using current date as fallback.")
            return datetime.now().isoformat()
    
    def _parse_date_from_service_message(self, date_text: str) -> Optional[str]:
        """
        Parse date from service message text.
        
        Args:
            date_text: Text like "18 February 2025"
            
        Returns:
            Date string in YYYY-MM-DD format or None if parsing fails
        """
        try:
            # Try different date formats (adjust as needed based on your samples)
            for fmt in ["%d %B %Y", "%B %d, %Y", "%d %b %Y"]:
                try:
                    message_date = datetime.strptime(date_text, fmt)
                    return message_date.strftime("%Y-%m-%d")
                except ValueError:
                    continue
                    
            # If all formats fail, try a more permissive approach with regex
            match = re.search(r'(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)(?:,)?\s+(\d{4})', date_text)
            if match:
                day, month, year = match.groups()
                month_dict = {
                    'january': 1, 'february': 2, 'march': 3, 'april': 4,
                    'may': 5, 'june': 6, 'july': 7, 'august': 8,
                    'september': 9, 'october': 10, 'november': 11, 'december': 12,
                    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'jun': 6, 'jul': 7,
                    'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
                }
                month_num = month_dict.get(month.lower(), 1)
                dt = datetime(int(year), month_num, int(day))
                return dt.strftime("%Y-%m-%d")
                
        except Exception as e:
            logger.warning(f"Error parsing date '{date_text}': {str(e)}")
            
        return None
    
    def _extract_chat_info(self) -> Dict:
        """Extract chat information from the HTML"""
        info = {
            'name': "Unknown Chat",
            'type': "unknown",
            'id': 0
        }
        
        try:
            # If we haven't loaded the HTML yet, load just the header
            if self.soup is None:
                with open(self.html_file_path, 'r', encoding='utf-8') as f:
                    # Read just the first part of the file to find the header
                    header_html = f.read(50000)
                    header_soup = BeautifulSoup(header_html, 'html.parser')
                    
                    # Extract chat name from the header
                    header_div = header_soup.select_one('.page_header .text.bold')
                    if header_div and header_div.text.strip():
                        info['name'] = header_div.text.strip()
                        
                        # Generate a stable ID from the chat name
                        import hashlib
                        info['id'] = int(hashlib.md5(info['name'].encode('utf-8')).hexdigest(), 16) % 10**9
                        
                        # Determine if it's a private chat or group
                        if "@" in info['name'] or "Chat with" in info['name']:
                            info['type'] = "private"
                        else:
                            info['type'] = "group"
            else:
                # Use the already loaded soup
                header_div = self.soup.select_one('.page_header .text.bold')
                if header_div and header_div.text.strip():
                    info['name'] = header_div.text.strip()
                    
                    # Generate a stable ID from the chat name
                    import hashlib
                    info['id'] = int(hashlib.md5(info['name'].encode('utf-8')).hexdigest(), 16) % 10**9
                    
                    # Determine if it's a private chat or group
                    if "@" in info['name'] or "Chat with" in info['name']:
                        info['type'] = "private"
                    else:
                        info['type'] = "group"
        except Exception as e:
            logger.warning(f"Error extracting chat info: {str(e)}. Using default values.")
            logger.debug(traceback.format_exc())
        
        return info
    
    def _chunk_read_html(self, chunk_size=1024*1024) -> Iterator[str]:
        """
        Read the HTML file in chunks to avoid loading it all into memory at once.
        
        Args:
            chunk_size: Size of each chunk in bytes
            
        Yields:
            Chunks of the HTML file
        """
        try:
            with open(self.html_file_path, 'r', encoding='utf-8') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
        except UnicodeDecodeError:
            # Try with a different encoding if utf-8 fails
            logger.warning("UTF-8 decoding failed for chunked reading, trying with ISO-8859-1 encoding")
            with open(self.html_file_path, 'r', encoding='iso-8859-1') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
    
    def _stream_elements(self, tag_name='div', class_name=None) -> Generator[Tag, None, None]:
        """
        Stream elements from the HTML file without loading the entire file into memory.
        
        Args:
            tag_name: Name of the HTML tag to look for
            class_name: Optional class name to filter by
            
        Yields:
            BeautifulSoup Tag objects matching the criteria
        """
        # If we already have the soup loaded, use it
        if self.soup is not None:
            if class_name:
                for elem in self.soup.find_all(tag_name, class_=class_name):
                    yield elem
            else:
                for elem in self.soup.find_all(tag_name):
                    yield elem
            return
            
        # For large files, use a streaming approach
        from bs4 import BeautifulSoup, SoupStrainer
        
        # Create a filter to only parse the elements we're interested in
        if class_name:
            parse_only = SoupStrainer(tag_name, class_=class_name)
        else:
            parse_only = SoupStrainer(tag_name)
            
        # Read the HTML in chunks
        buffer = ""
        for chunk in self._chunk_read_html(chunk_size=2*1024*1024):  # 2MB chunks
            buffer += chunk
            
            # Try to find complete elements in the buffer
            while True:
                # Find opening tag
                start_idx = buffer.find(f'<{tag_name} ')
                if start_idx == -1:
                    # No more elements in this buffer
                    break
                    
                # Find closing tag
                end_tag = f'</{tag_name}>'
                end_idx = buffer.find(end_tag, start_idx)
                if end_idx == -1:
                    # Element not complete yet, wait for more data
                    break
                    
                # Extract the complete element
                end_idx += len(end_tag)
                element_html = buffer[start_idx:end_idx]
                
                # Parse the element
                element_soup = BeautifulSoup(element_html, 'html.parser', parse_only=parse_only)
                for elem in element_soup.find_all(tag_name):
                    if class_name is None or class_name in elem.get('class', []):
                        yield elem
                
                # Remove the processed element from the buffer
                buffer = buffer[end_idx:]
        
        # Process any remaining elements in the buffer
        if buffer:
            element_soup = BeautifulSoup(buffer, 'html.parser', parse_only=parse_only)
            for elem in element_soup.find_all(tag_name):
                if class_name is None or class_name in elem.get('class', []):
                    yield elem
    
    def _extract_date_markers(self) -> Dict[str, str]:
        """
        Extract date markers from service messages.
        
        Returns:
            Dictionary mapping message IDs to date strings
        """
        date_map = {}
        current_date = None
        
        # Look for service messages with dates
        service_messages = self._stream_elements('div', 'message service')
        for elem in service_messages:
            elem_id = elem.get('id', '')
            
            # Check if it contains a date
            date_div = elem.select_one('.body.details')
            if date_div:
                date_text = date_div.text.strip()
                parsed_date = self._parse_date_from_service_message(date_text)
                
                if parsed_date:
                    current_date = parsed_date
                    logger.debug(f"Found date marker: {date_text} -> {current_date}")
            
            # Associate this element ID with the current date
            if current_date and elem_id:
                date_map[elem_id] = current_date
                
        return date_map
    
    def convert_to_dict(self) -> Dict:
        """
        Convert the HTML export to a Python dictionary.
        
        Returns:
            Dictionary with the JSON data structure
        """
        # Extract chat info
        try:
            chat_info = self._extract_chat_info()
            logger.info(f"Chat name: {chat_info['name']}")
            
            # Extract date markers
            logger.info("Extracting date markers...")
            date_map = self._extract_date_markers()
            
            # If no dates were found, this is a problem
            if not date_map:
                logger.warning("No date markers found in the export! Messages may have incorrect dates.")
            else:
                logger.info(f"Found date markers for {len(set(date_map.values()))} different days")
            
            # Extract messages
            logger.info("Extracting messages...")
            messages = []
            message_count = 0
            
            # Process messages in batches to avoid memory issues
            batch_size = 1000
            current_batch = []
            
            # Extract messages from the HTML
            message_elements = self._stream_elements('div', 'message default')
            for elem in message_elements:
                try:
                    # Get message ID
                    message_id = elem.get('id', '')
                    
                    # Find base date for this message
                    base_date = None
                    
                    # Find the closest date before this message
                    sorted_ids = sorted([msg_id for msg_id in date_map.keys() if msg_id <= message_id])
                    if sorted_ids:
                        closest_id = sorted_ids[-1]
                        base_date = date_map.get(closest_id)
                    
                    # Extract message with the correct base date
                    message = self._extract_message(elem, base_date)
                    if message:
                        current_batch.append(message)
                        message_count += 1
                        
                        # Process in batches to save memory
                        if len(current_batch) >= batch_size:
                            messages.extend(current_batch)
                            logger.debug(f"Processed batch of {len(current_batch)} messages. Total so far: {len(messages)}")
                            current_batch = []
                            
                            # Force garbage collection
                            gc.collect()
                            
                except Exception as e:
                    logger.warning(f"Error processing message {elem.get('id')}: {str(e)}")
                    logger.debug(traceback.format_exc())
            
            # Add any remaining messages
            if current_batch:
                messages.extend(current_batch)
                logger.debug(f"Processed final batch of {len(current_batch)} messages")
            
            logger.info(f"Extracted {len(messages)} messages")
            
            # Sort messages by date
            logger.info("Sorting messages by date...")
            messages.sort(key=lambda x: x.get('date', ''))
            
            # Create final JSON structure
            json_data = {
                'name': chat_info['name'],
                'type': chat_info['type'],
                'id': chat_info['id'],
                'messages': messages
            }
            
            # Analyze date range
            if messages:
                try:
                    dates = sorted([m['date'] for m in messages if m.get('date')])
                    if dates:
                        first_date = dates[0]
                        last_date = dates[-1]
                        json_data['first_date'] = first_date
                        json_data['last_date'] = last_date
                        logger.info(f"Date range: {first_date} to {last_date}")
                        
                        # Check if dates span multiple days
                        first_day = first_date.split('T')[0]
                        last_day = last_date.split('T')[0]
                        
                        if first_day != last_day:
                            days = len(set([d.split('T')[0] for d in dates]))
                            logger.info(f"Messages span {days} days")
                        else:
                            logger.warning("All messages are from the same day. Check if this is expected.")
                except Exception as e:
                    logger.error(f"Error analyzing date range: {str(e)}")
                    logger.debug(traceback.format_exc())
                    
            return json_data
        except Exception as e:
            logger.error(f"Error converting to dictionary: {str(e)}")
            logger.debug(traceback.format_exc())
            # Return a minimal valid structure
            return {
                'name': f"Error processing {os.path.basename(self.html_file_path)}",
                'type': "error",
                'id': 0,
                'messages': [],
                'error': str(e)
            }
    
    def _extract_message(self, msg_div, base_date: Optional[str] = None) -> Dict:
        """
        Extract message data from a message div element.
        
        Args:
            msg_div: BeautifulSoup Tag containing the message
            base_date: Base date string (YYYY-MM-DD) if known
            
        Returns:
            Message data dictionary
        """
        try:
            # Initialize message data
            message = {
                'id': msg_div.get('id', ''),
                'type': 'message',
                'date': None,
                'from': None,
                'text': '',
            }
            
            # Check if it's a joined message (continuation from previous sender)
            is_joined = 'joined' in msg_div.get('class', [])
            
            # Extract sender name (if not joined)
            if not is_joined:
                from_name = msg_div.select_one('.from_name')
                if from_name:
                    message['from'] = from_name.text.strip()
                else:
                    message['from'] = "Unknown User"
            
            # Extract date
            date_div = msg_div.select_one('.date.details')
            if date_div:
                # Get time and full date from title attribute
                time_str = date_div.text.strip()
                title_str = date_div.get('title', '')
                
                # Parse date (now including base_date)
                message['date'] = self._parse_date(time_str, title_str, base_date)
            
            # Extract text content
            text_div = msg_div.select_one('.text')
            if text_div:
                # Get plain text
                message['text'] = text_div.get_text(separator=' ', strip=True)
                
                # Check for media content
                media_wrap = msg_div.select_one('.media_wrap')
                if media_wrap:
                    media_type, file_path = self._extract_media(media_wrap)
                    if media_type:
                        message['media_type'] = media_type
                        if file_path:
                            message['file'] = file_path
                
                # Check for links in text that might be media
                links = text_div.select('a')
                for link in links:
                    href = link.get('href', '')
                    if href and not href.startswith(('http://', 'https://')):
                        file_path = self._resolve_media_path(href)
                        if file_path:
                            # Determine media type from file extension
                            ext = os.path.splitext(file_path)[1].lower()
                            if ext in ['.jpg', '.jpeg', '.png', '.gif']:
                                message['media_type'] = 'photo'
                            elif ext in ['.mp4', '.avi', '.mov', '.webm']:
                                message['media_type'] = 'video'
                            elif ext in ['.mp3', '.ogg', '.m4a', '.wav']:
                                message['media_type'] = 'audio'
                            else:
                                message['media_type'] = 'file'
                            
                            message['file'] = file_path
                            break
            
            # Check for reply
            reply_div = msg_div.select_one('.reply_to.details')
            if reply_div:
                reply_link = reply_div.select_one('a')
                if reply_link and reply_link.get('href', ''):
                    # Extract message ID from the href
                    reply_href = reply_link.get('href', '')
                    match = re.search(r'#go_to_message(\d+)', reply_href)
                    if match:
                        message['reply_to_message_id'] = match.group(1)
            
            return message
        except Exception as e:
            logger.warning(f"Error extracting message data: {str(e)}")
            logger.debug(traceback.format_exc())
            # Return a minimal valid message
            return {
                'id': msg_div.get('id', 'unknown'),
                'type': 'error',
                'date': datetime.now().isoformat(),
                'from': "Error",
                'text': f"Error extracting message: {str(e)}"
            }
    
    def _extract_media(self, media_wrap) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract media type and file path from a media wrap element.
        
        Args:
            media_wrap: BeautifulSoup Tag containing the media
            
        Returns:
            Tuple of (media_type, file_path)
        """
        try:
            # Check different media types
            media_types = {
                '.media_photo': 'photo',
                '.media_file': 'file',
                '.media_voice_message': 'voice',
                '.media_video': 'video',
                '.media_audio_file': 'audio',
                '.media_poll': 'poll',
                '.media_contact': 'contact',
                '.media_location': 'location',
            }
            
            for selector, media_type in media_types.items():
                media_elem = media_wrap.select_one(selector)
                if media_elem:
                    # Found media of this type, now look for the file
                    if media_type == 'photo':
                        img = media_elem.select_one('img')
                        if img and img.get('src'):
                            file_path = self._resolve_media_path(img.get('src'))
                            return media_type, file_path
                    elif media_type in ['file', 'audio', 'voice']:
                        # Get title if available
                        title = media_elem.select_one('.title.bold')
                        if title:
                            return media_type, None  # File not included in export
                        
                        # Try to find a link
                        link = media_elem.select_one('a')
                        if link and link.get('href'):
                            file_path = self._resolve_media_path(link.get('href'))
                            return media_type, file_path
                            
                    return media_type, None
        except Exception as e:
            logger.warning(f"Error extracting media: {str(e)}")
            logger.debug(traceback.format_exc())
            
        return None, None
        
    def convert_to_json(self, output_path: str) -> None:
        """
        Convert the HTML export to JSON format and save it to the specified path.
        
        Args:
            output_path: Path where the JSON file will be saved
        """
        try:
            # Get the JSON data structure
            json_data = self.convert_to_dict()
            
            # Use a temporary file to avoid permission issues
            output_dir = os.path.dirname(os.path.abspath(output_path))
            
            # Create the output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Check if we have write permission to the directory
            if not os.access(output_dir, os.W_OK):
                logger.error(f"No write permission for directory: {output_dir}")
                raise PermissionError(f"No write permission for {output_dir}")
            
            # Use a temporary file for safe writing
            temp_file = os.path.join(output_dir, f"temp_{os.getpid()}_{datetime.now().strftime('%H%M%S')}.json")
            
            # Write messages in chunks to avoid memory issues
            logger.info(f"Writing JSON to {temp_file}...")
            
            with open(temp_file, 'w', encoding='utf-8') as f:
                # Start the JSON object
                f.write('{\n')
                
                # Write metadata
                f.write(f'  "name": {json.dumps(json_data["name"])},\n')
                f.write(f'  "type": {json.dumps(json_data["type"])},\n')
                f.write(f'  "id": {json.dumps(json_data["id"])},\n')
                
                # Add first_date and last_date if available
                if "first_date" in json_data:
                    f.write(f'  "first_date": {json.dumps(json_data["first_date"])},\n')
                if "last_date" in json_data:
                    f.write(f'  "last_date": {json.dumps(json_data["last_date"])},\n')
                
                # Start the messages array
                f.write('  "messages": [\n')
                
                # Write messages in batches
                messages = json_data["messages"]
                for i, message in enumerate(messages):
                    message_json = json.dumps(message, ensure_ascii=False, default=str)
                    if i < len(messages) - 1:
                        f.write(f'    {message_json},\n')
                    else:
                        f.write(f'    {message_json}\n')
                    
                    # Flush every 100 messages to avoid buffering issues
                    if i % 100 == 0:
                        f.flush()
                
                # Close the messages array and JSON object
                f.write('  ]\n')
                f.write('}\n')
            
            # Move the temporary file to the destination
            if os.path.exists(output_path):
                try:
                    # Try to remove existing file if it exists
                    os.remove(output_path)
                except PermissionError:
                    logger.error(f"Cannot overwrite {output_path}. File may be in use by another program.")
                    # Keep the temp file as a fallback
                    alternative_path = f"{output_path}.new"
                    shutil.move(temp_file, alternative_path)
                    logger.info(f"Saved to alternative location: {alternative_path}")
                    return
            
            # Move temp file to final destination
            shutil.move(temp_file, output_path)
            
            logger.info(f"Conversion complete! JSON file created: {output_path}")
            logger.info(f"Total messages in output: {len(json_data['messages'])}")
            
        except PermissionError as e:
            logger.error(f"Permission error: {str(e)}")
            logger.error("Make sure you have write access to the output directory and the file is not open in another program.")
            raise
        except Exception as e:
            logger.error(f"Error converting to JSON: {str(e)}")
            logger.debug(traceback.format_exc())
            raise