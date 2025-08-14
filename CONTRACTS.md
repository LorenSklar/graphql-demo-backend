# ------------------------
# ENUMS
# ------------------------
enum ResourceType {
  ARTICLE
  VIDEO
  TUTORIAL
  DOCUMENTATION
}

enum HintType {
  """
  A prompt or suggestion that nudges the learner forward.
  Not tied to a specific wrong answer.
  Required.
  Example: "Remember that queries always start with query or mutation."
  """
  GENERAL_HINT


  """
  Tied to a specific error often in syntax.
  Used to provide targeted feedback for mistakes.
  Optional.
  Example: forgetting braces, requesting a non-existent field, or querying a scalar when a list is expected.
  """
  COMMON_ERROR
  

  """
  Tied to a specific misconception about the concept.
  Triggered when a learner demonstrates an incomplete or alternative understanding.
  Optional.
  Example: requesting a subfield without first querying the parent field, demonstrating a misunderstanding of GraphQL schema structure.
  """
  COMMON_MISCONCEPTION

  """
  TODO: Future versions of hints should adapt dynamically based on learner's exploration readiness or cognitive engagement.
  High readiness → more exploratory hints
  Medium readiness → reinforcing hints that expand understanding
  Low readiness → hints that focus on core concepts and direct guidance
}


# ------------------------
# DOMAIN
# ------------------------
type Domain {
  id: ID!                  # UUID
  type: String!            # "Domain"
  name: String!            # Short descriptive name e.g., "Queries"
  inquiry: String!         # Learner facing question, e.g., "How do I ask for information?"
  clusterIds: [ID!]        # Child clusters, e.g., [UUID1, UUID2]
  recommendedOrder: Int    # Optional advisory sequence, e.g., 1
}

# ------------------------
# CLUSTER
# ------------------------
type Cluster {
  id: ID!
  type: String!
  name: String!
  domainId: ID!            # Parent domain
  conceptIds: [ID!]!       # Concepts under this cluster
  recommendedOrder: Int
}

# ------------------------
# CONCEPT
# ------------------------
type Concept {
  id: ID!
  type: String!
  name: String!
  inquiry: String!
  objective: String!
  foundationIds: [ID!]     # Prerequisite concepts
  extensionIds: [ID!]      # Follow-up concepts
  exerciseIds: [ID!]       # Exercises attached
  resourceIds: [ID!]
}

# ------------------------
# EXERCISE
# ------------------------
type Exercise {
  id: ID!
  type: String!
  inquiry: String!                      # The exercise question
  generalHints: [Hint!]!                # Required nudges for thinking
  optionalHints: [Hint!]                # Common misconceptions and errors, matched by pattern
  solution: [String!]!                  # Step-by-step solutions from starter to full
  minimalAnswerPattern: String!         # Minimal regex to validate core expected structure
  difficultyScore: Int                  # To be implemented based on learner performance
  suggestedNextExerciseIds: [ID!]       # Adaptive branching
  suggestedPrevExerciseIds: [ID!]       # Adaptive branching
}

# ------------------------
# HINT
# ------------------------
type Hint {
  id: ID!
  text: String!         # Hint message
  type: HintType!       # GENERAL_HINT | COMMON_MISCONCEPTION | COMMON_ERROR
  tag: String           # Optional categorization, e.g., 'syntax', 'field', 'logic'
}

# ------------------------
# RESOURCE
# ------------------------
type Resource {
  id: ID!                  # UUID
  type: String!            # "Resource"
  title: String!           # Title of the resource
  typeEnum: ResourceType!  # Category
  url: String!             # URL to the resource
}
