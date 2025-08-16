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
  Example: "Replace the word inside curly brackets."
  """
  GENERAL_HINT


  """
  Tied to a specific error often in syntax.
  Used to provide targeted feedback for mistakes.
  Optional.
  Example: forgetting braces, requesting a non-existent field, etc.
  """
  COMMON_ERROR
  

  """
  Tied to a specific misconception.
  Triggered when a learner demonstrates an incomplete or inaccurate understanding.
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
  generalHints: [Hint!]    # To clarify instructions or nudge thinking
                           # I moved hints to the concept level rather than exercises.
                           # Pros: Avoids repeating syntax hints across multiple exercises.
                           # Cons: Forces all exercises under this concept to share the same hints
                           # Felt cute. May delete later 😎

  optionalHints: [Hint!]   # Common misconceptions and errors identified by tags or triggerPattern
  reflectionPrompts: [String!]!  # Questions or cues presented to the learner to encourage reflection on the concept.
  reflectionTargets: [String!]!  # Key points or insights the reflection is intended to elicit or focus on.
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
  prefill: Boolean!                     # Does this exercise replace previous text in editor?
  prefillText: String!                  # The initial code shown in the editor if prefill is true. Use "" to clear existing code from editor.
  solutions: [String!]!                 # Solutions progressing from partial hints to full answer.
  minimalAnswerPattern: String!         # Minimal regex to validate core expected structure
  difficultyScore: Int                  # To be implemented based on actual learner performance
  suggestedNextExerciseIds: [ID!]       # Adaptive branching
  suggestedPrevExerciseIds: [ID!]       # Adaptive branching
}

# ------------------------
# HINT
# ------------------------
type Hint {
  id: ID!
  text: String!             # Hint message
  type: HintType!           # GENERAL_HINT | COMMON_MISCONCEPTION | COMMON_ERROR
  tags: [String!]           # Optional categorizations, e.g., 'syntax', 'field', 'logic'
  triggerPattern: String    # Optional regex pattern for recognizing syntax errors
}

# ------------------------
# RESOURCE
# ------------------------
type Resource {
  id: ID!                  # UUID
  type: String!            # "Resource"
  typeEnum: ResourceType!  # Category
  title: String!           # Title of the resource
  url: String!             # URL to the resource
}
