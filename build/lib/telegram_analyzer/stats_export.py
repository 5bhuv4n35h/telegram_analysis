import os
import json
import logging
from datetime import datetime
import numpy as np
import pandas as pd

import datetime as dt

class StatsEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle NumPy types and datetimes"""
    def default(self, obj):
        if isinstance(obj, (np.int64, np.int32, np.integer)):
            return int(obj)
        if isinstance(obj, (np.float64, np.float32, np.floating)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (dt.datetime, dt.date, pd.Timestamp)):
            return obj.isoformat()
        return super(StatsEncoder, self).default(obj)

def export_stats_to_json(stats, output_dir):
    """
    Export analysis statistics to a JSON file.
    
    Args:
        stats: Dictionary containing analysis statistics
        output_dir: Directory to save the JSON file
        
    Returns:
        Path to the saved JSON file or None if export failed
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Make sure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Define output path
        output_path = os.path.join(output_dir, 'stats.json')
        
        # Write JSON to file using custom encoder
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, cls=StatsEncoder, ensure_ascii=False, indent=2)
            
        logger.info(f"Statistics exported to {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Failed to export statistics to JSON: {str(e)}")
        return None
