"""
Sandbox Endpoint Module

Handles the /sandbox GraphQL endpoint for interactive GraphQL practice and learning.
This is the hands-on playground for users to experiment with GraphQL queries.
"""

from ariadne import make_executable_schema, QueryType, graphql_sync
from flask import request, jsonify


# === SANDBOX GRAPHQL SCHEMA ===
sandbox_type_defs = """
    type Query {
        ping: String!
        marco: String!
        field: String!
        # TODO: Add practice data types
        # users: [User!]!
        # posts: [Post!]!
        # comments: [Comment!]!
    }
"""

# === SANDBOX RESOLVERS ===
sandbox_query = QueryType()

@sandbox_query.field("ping")
def resolve_sandbox_ping(*_):
    return "sandbox-pong"

@sandbox_query.field("marco")
def resolve_sandbox_marco(*_):
    return "sandbox-polo"

@sandbox_query.field("field")
def resolve_sandbox_field(*_):
    return "sandbox-value"

# === CREATE SANDBOX SCHEMA ===
sandbox_schema = make_executable_schema(sandbox_type_defs, sandbox_query)


def handle_sandbox_request():
    """Handle GraphQL requests for sandbox practice"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        variables = data.get('variables', {})
        
        success, result = graphql_sync(sandbox_schema, {"query": query, "variables": variables})
        
        if success:
            return jsonify(result)
        else:
            return jsonify({"errors": result}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400
