"""
Content Endpoint Module

Handles the /content GraphQL endpoint for lesson content, concepts, and exercises.
This serves the actual curriculum data from separate YAML files.
"""

from ariadne import make_executable_schema, QueryType, graphql_sync
from flask import request, jsonify
import yaml
import os
import glob


# === CONTENT GRAPHQL SCHEMA ===
content_type_defs = """
    type Hint {
        id: ID!
        text: String!
        type: String!
        tag: String
        triggerPattern: String
    }
    
    type Exercise {
        id: ID!
        type: String!
        inquiry: String!
        prefillEditor: Boolean
        prefillEditorText: String
        solutions: [String!]
        solution: [String!]
        minimalAnswerPattern: String
        difficultyScore: Int
        suggestedNextExerciseIds: [ID!]
        suggestedPrevExerciseIds: [ID!]
    }
    
    type Concept {
        id: ID!
        type: String!
        name: String!
        inquiry: String!
        objective: String!
        generalHints: [Hint!]
        optionalHints: [Hint!]
        reflectionPrompts: [String!]!
        reflectionTargets: [String!]!
        foundationIds: [ID!]
        extensionIds: [ID!]
        exerciseIds: [ID!]
        resourceIds: [ID!]
    }
    
    type Cluster {
        id: ID!
        type: String!
        name: String!
        domainId: ID!
        conceptIds: [ID!]!
        inquiry: String!
    }
    
    type Domain {
        id: ID!
        type: String!
        name: String!
        inquiry: String!
        clusterIds: [ID!]!
        recommendedOrder: Int
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
        lesson(id: String!): Concept
        lessonsByCluster(clusterId: ID!): [Concept!]!
    }
"""

# === CONTENT RESOLVERS ===
content_query = QueryType()

@content_query.field("domains")
def resolve_domains(*_):
    """Get all domains"""
    domains_data = load_yaml_file('domains.yaml')
    return domains_data.get('domains', [])

@content_query.field("clusters")
def resolve_clusters(*_):
    """Get all clusters"""
    clusters_data = load_yaml_file('clusters.yaml')
    return clusters_data.get('clusters', [])

@content_query.field("concepts")
def resolve_concepts(*_):
    """Get all concepts from all lesson files"""
    all_concepts = []
    lesson_files = get_lesson_files()
    
    for lesson_file in lesson_files:
        lesson_data = load_yaml_file(lesson_file)
        concepts = lesson_data.get('concepts', [])
        all_concepts.extend(concepts)
    
    return all_concepts

@content_query.field("exercises")
def resolve_exercises(*_):
    """Get all exercises from all lesson files"""
    all_exercises = []
    lesson_files = get_lesson_files()
    
    for lesson_file in lesson_files:
        lesson_data = load_yaml_file(lesson_file)
        exercises = lesson_data.get('exercises', [])
        all_exercises.extend(exercises)
    
    return all_exercises

@content_query.field("domain")
def resolve_domain(*_, id):
    """Get a specific domain by ID"""
    domains_data = load_yaml_file('domains.yaml')
    domains = domains_data.get('domains', [])
    return next((d for d in domains if d['id'] == id), None)

@content_query.field("cluster")
def resolve_cluster(*_, id):
    """Get a specific cluster by ID"""
    clusters_data = load_yaml_file('clusters.yaml')
    clusters = clusters_data.get('clusters', [])
    return next((c for c in clusters if c['id'] == id), None)

@content_query.field("concept")
def resolve_concept(*_, id):
    """Get a specific concept by ID"""
    lesson_files = get_lesson_files()
    
    for lesson_file in lesson_files:
        lesson_data = load_yaml_file(lesson_file)
        concepts = lesson_data.get('concepts', [])
        concept = next((c for c in concepts if c['id'] == id), None)
        if concept:
            return concept
    
    return None

@content_query.field("exercise")
def resolve_exercise(*_, id):
    """Get a specific exercise by ID"""
    lesson_files = get_lesson_files()
    
    for lesson_file in lesson_files:
        lesson_data = load_yaml_file(lesson_file)
        exercises = lesson_data.get('exercises', [])
        exercise = next((e for e in exercises if e['id'] == id), None)
        if exercise:
            return exercise
    
    return None

@content_query.field("lesson")
def resolve_lesson(*_, id):
    """Get a lesson by its filename (e.g., 'lesson-1a1')"""
    lesson_file = f"{id}.yaml"
    lesson_data = load_yaml_file(lesson_file)
    concepts = lesson_data.get('concepts', [])
    return concepts[0] if concepts else None

@content_query.field("lessonsByCluster")
def resolve_lessons_by_cluster(*_, clusterId):
    """Get all concepts for a specific cluster"""
    # First get the cluster to see what concept IDs it contains
    cluster = resolve_cluster(None, id=clusterId)
    if not cluster:
        return []
    
    concept_ids = cluster.get('conceptIds', [])
    all_concepts = resolve_concepts(None)
    
    # Filter concepts by the cluster's concept IDs
    return [c for c in all_concepts if c['id'] in concept_ids]

# === CREATE CONTENT SCHEMA ===
content_schema = make_executable_schema(content_type_defs, content_query)


def get_lesson_files():
    """Get all lesson YAML files"""
    lessons_dir = os.path.join(os.path.dirname(__file__), '..', 'lessons')
    lesson_pattern = os.path.join(lessons_dir, 'lesson-*.yaml')
    return glob.glob(lesson_pattern)

def load_yaml_file(filename):
    """Load data from a specific YAML file"""
    try:
        lessons_dir = os.path.join(os.path.dirname(__file__), '..', 'lessons')
        file_path = os.path.join(lessons_dir, filename)
        
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        else:
            print(f"File not found: {file_path}")
            return {}
            
    except Exception as e:
        print(f"Error loading {filename}: {e}")
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
