"""
Logging Module

Handles the /log REST endpoint for tracking user interactions and system responses.
Implements file-based logging with rotation for Render deployment.
"""

from flask import request, jsonify
import json
import time
import os
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler


# === LOGGING SETUP ===
def setup_logger():
    """Setup file-based logger with rotation"""
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    # Setup rotating file handler (10MB max, keep 5 backup files)
    log_file = os.path.join(logs_dir, 'app.log')
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    
    # Setup formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    
    # Setup logger
    logger = logging.getLogger('graphql_demo')
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    
    # Also log to stdout (captured by Render)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

# Initialize logger
logger = setup_logger()


def log_user_interaction(data):
    """Log user interaction to file and console"""
    try:
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'user_interaction',
            'user_query': data.get('query', ''),
            'response': data.get('response', ''),
            'success': data.get('success', False),
            'endpoint': data.get('endpoint', 'unknown'),
            'user_id': data.get('user_id', 'anonymous'),
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', 'unknown')
        }
        
        # Log to file and console
        if log_entry['success']:
            logger.info(f"User interaction: {json.dumps(log_entry)}")
        else:
            logger.warning(f"User interaction (failed): {json.dumps(log_entry)}")
            
        return log_entry
        
    except Exception as e:
        logger.error(f"Error logging user interaction: {str(e)}")
        return None


def log_system_event(event_type, details, level='info'):
    """Log system events (errors, warnings, info)"""
    try:
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'system_event',
            'event_type': event_type,
            'details': details,
            'level': level
        }
        
        # Log based on level
        if level == 'error':
            logger.error(f"System event: {json.dumps(log_entry)}")
        elif level == 'warning':
            logger.warning(f"System event: {json.dumps(log_entry)}")
        else:
            logger.info(f"System event: {json.dumps(log_entry)}")
            
        return log_entry
        
    except Exception as e:
        print(f"Error logging system event: {str(e)}")  # Fallback to print
        return None


def handle_log_request():
    """Handle logging requests for user interactions"""
    try:
        data = request.get_json()
        
        # Log the interaction
        log_entry = log_user_interaction(data)
        
        if log_entry:
            return jsonify({
                'status': 'logged', 
                'timestamp': log_entry['timestamp'],
                'message': 'Interaction logged successfully',
                'log_id': f"{int(time.time())}-{hash(str(log_entry))}"
            })
        else:
            return jsonify({'error': 'Failed to log interaction'}), 500
            
    except Exception as e:
        # Log the error itself
        log_system_event('logging_error', str(e), 'error')
        return jsonify({'error': str(e)}), 400


def get_log_stats():
    """Get basic logging statistics"""
    try:
        logs_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
        log_file = os.path.join(logs_dir, 'app.log')
        
        if os.path.exists(log_file):
            file_size = os.path.getsize(log_file)
            file_size_mb = round(file_size / (1024 * 1024), 2)
            last_modified = datetime.fromtimestamp(os.path.getmtime(log_file))
            
            return {
                'log_file_exists': True,
                'file_size_mb': file_size_mb,
                'last_modified': last_modified.isoformat(),
                'logs_directory': logs_dir
            }
        else:
            return {
                'log_file_exists': False,
                'message': 'Log file not found'
            }
            
    except Exception as e:
        return {
            'error': str(e),
            'message': 'Failed to get log stats'
        }
