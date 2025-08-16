"""
GraphQL Practice Tool Backend

This Flask app provides three distinct endpoints for different purposes:

1. /content (GraphQL) - Serves lesson content, concepts, and exercises
2. /sandbox (GraphQL) - Interactive GraphQL playground for hands-on practice
3. /log (REST) - Simple logging endpoint for tracking user interactions and system responses

Why three endpoints instead of one GraphQL endpoint?
- /content and /sandbox serve different learning purposes (content vs. practice)
- /log is simple logging that doesn't benefit from GraphQL complexity
- Clear separation makes the API easier to understand and maintain
- This architecture serves our learning goals better despite abandoning GraphQL orthodoxy re: a single endpoint
"""

from flask import Flask
from flask_cors import CORS
import os

# Import our modular endpoints
from src.content.content import handle_content_request
from src.sandbox.sandbox import handle_sandbox_request
from src.logging.logger import handle_log_request


# === FLASK APP SETUP ===
app = Flask(__name__)

# === CORS CONFIGURATION ===
origins = os.getenv("CORS_ORIGINS", "").split(",")  # Get CORS origins from environment variable
CORS(app, origins=origins, supports_credentials=True)

# === GRAPHQL LESSON ENDPOINT ===
@app.route('/content', methods=['GET','POST'])
def graphql_content():
    """GraphQL endpoint for lesson content and the dual-graph learning system"""
    return handle_content_request()

# === GRAPHQL PRACTICE ENDPOINT ===
@app.route('/sandbox', methods=['GET','POST'])
def graphql_sandbox():
    """GraphQL endpoint for interactive GraphQL practice and learning"""
    return handle_sandbox_request()

# === REST LOGGING ENDPOINT ===
@app.route('/log', methods=['POST'])
def log_entry():
    """REST endpoint for logging user queries and system responses"""
    return handle_log_request()

# === MAIN EXECUTION ===
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)


