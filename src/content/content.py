"""
Content Endpoint Module

Handles the /content GraphQL endpoint for lesson content, concepts, and exercises.
This serves the actual curriculum data from YAML files.
"""

from ariadne import make_executable_schema, QueryType, graphql_sync
from flask import request, jsonify
import yaml
import os


# === CONTENT GRAPHQL SCHEMA ===
content_type_defs = """
    type Domain {
        id: ID!
        type: String!
        name: String!
        inquiry: String!
        clusterIds: [ID!]!
        recommendedOrder: Int
    }
    
    type Cluster {
        id: ID!
        type: String!
        name: String!
        domainId: ID!
        conceptIds: [ID!]!
        recommendedOrder: Int
    }
    
    type Concept {
        id: ID!
        type: String!
        name: String!
        inquiry: String!
        objective: String!
        generalHints: [String!]
        optionalHints: [String!]
        reflectionPrompts: [String!]!
        reflectionTargets: [String!]!
        foundationIds: [ID!]
        extensionIds: [ID!]
        exerciseIds: [ID!]
        resourceIds: [ID!]
    }
    
    type Exercise {
        id: ID!
        type: String!
        inquiry: String!
        objective: String!
        successCriteria: [String!]!
        hints: [String!]
        solution: String!
        explanation: String!
        difficulty: String!
        timeEstimate: Int
        conceptIds: [ID!]!
    }
    
    type Query {
        domains: [Domain!]!
        clusters: [Cluster!]!
        concepts: [Concept!]!
        exercises: [Exercise!]!
        domain(id: ID!): Domain
        cluster(id: ID!): Cluster
        concept(id: ID!): Concept
        exercise(id: ID!): Exercise
    }
"""

# === CONTENT RESOLVERS ===
content_query = QueryType()

@content_query.field("domains")
def resolve_domains(*_):
    """Get all domains"""
    curriculum = load_curriculum()
    return curriculum.get('domains', [])

@content_query.field("clusters")
def resolve_clusters(*_):
    """Get all clusters"""
    curriculum = load_curriculum()
    return curriculum.get('clusters', [])

@content_query.field("concepts")
def resolve_concepts(*_):
    """Get all concepts"""
    curriculum = load_curriculum()
    return curriculum.get('concepts', [])

@content_query.field("exercises")
def resolve_exercises(*_):
    """Get all exercises"""
    curriculum = load_curriculum()
    return curriculum.get('exercises', [])

@content_query.field("domain")
def resolve_domain(*_, id):
    """Get a specific domain by ID"""
    curriculum = load_curriculum()
    domains = curriculum.get('domains', [])
    return next((d for d in domains if d['id'] == id), None)

@content_query.field("cluster")
def resolve_cluster(*_, id):
    """Get a specific cluster by ID"""
    curriculum = load_curriculum()
    clusters = curriculum.get('clusters', [])
    return next((c for c in clusters if c['id'] == id), None)

@content_query.field("concept")
def resolve_concept(*_, id):
    """Get a specific concept by ID"""
    curriculum = load_curriculum()
    concepts = curriculum.get('concepts', [])
    return next((c for c in concepts if c['id'] == id), None)

@content_query.field("exercise")
def resolve_exercise(*_, id):
    """Get a specific exercise by ID"""
    curriculum = load_curriculum()
    exercises = curriculum.get('exercises', [])
    return next((e for e in exercises if e['id'] == id), None)

# === CREATE CONTENT SCHEMA ===
content_schema = make_executable_schema(content_type_defs, content_query)


def load_curriculum():
    """Load curriculum data from YAML file"""
    try:
        curriculum_path = os.path.join(os.path.dirname(__file__), '..', 'lessons', 'CURRICULUM.yaml')
        with open(curriculum_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading curriculum: {e}")
        return {}


def handle_content_request():
    """Handle GraphQL requests for lesson content"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        variables = data.get('variables', {})
        
        success, result = graphql_sync(content_schema, {"query": query, "variables": variables})
        
        if success:
            return jsonify(result)
        else:
            return jsonify({"errors": result}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400
