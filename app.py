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

from ariadne import make_executable_schema, load_schema_from_path, ObjectType, QueryType, graphql_sync
from ariadne.asgi import GraphQL
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import time


# === FLASK APP SETUP ===
app = Flask(__name__)

# === CORS CONFIGURATION ===
origins = os.getenv("CORS_ORIGINS", "").split(",")  # Get CORS origins from environment variable
CORS(app, origins=origins, supports_credentials=True)

# === GRAPHQL SCHEMA DEFINITION ===
type_defs = """
    type Query {
        ping: String!
        marco: String!
        field: String!
    }
"""

# === GRAPHQL RESOLVERS ===
query = QueryType()

@query.field("ping")
def resolve_ping(*_):
    return "pong"

@query.field("marco")
def resolve_marco(*_):
    return "polo"

@query.field("field")
def resolve_field(*_):
    return "value"

# === CREATE EXECUTABLE SCHEMA ===
schema = make_executable_schema(type_defs, query)

# === GRAPHQL LESSON ENDPOINT ===
@app.route('/content', methods=['GET','POST'])
def graphql_content():
    """GraphQL endpoint for lesson content and the dual-graph learning system"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        variables = data.get('variables', {})
        
        success, result = graphql_sync(schema, {"query": query, "variables": variables})
        
        if success:
            return jsonify(result)
        else:
            return jsonify({"errors": result}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# === GRAPHQL PRACTICE ENDPOINT ===
@app.route('/sandbox', methods=['GET','POST'])
def graphql_sandbox():
    """GraphQL endpoint for interactive GraphQL practice and learning"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        variables = data.get('variables', {})
        
        success, result = graphql_sync(schema, {"query": query, "variables": variables})
        
        if success:
            return jsonify(result)
        else:
            return jsonify({"errors": result}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# === REST LOGGING ENDPOINT ===
@app.route('/log', methods=['POST'])
def log_entry():
    """REST endpoint for logging user queries and system responses"""
    try:
        data = request.get_json()
        
        # Simple logging for MVP
        log_entry = {
            'timestamp': time.time(),
            'user_query': data.get('query', ''),
            'response': data.get('response', ''),
            'success': data.get('success', False)
        }
        
        # TODO: Save to file or implement proper logging
        print(f"LOG: {json.dumps(log_entry)}")
        
        return jsonify({'status': 'logged', 'timestamp': log_entry['timestamp']})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# === MAIN EXECUTION ===
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)


