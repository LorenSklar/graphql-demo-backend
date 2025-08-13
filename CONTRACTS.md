type Concept {
  concept_id: ID!
  concept_inquiry: String!                # The open-ended question or challenge
  concept_objective: String!              # The specific skill or outcome expected
  concept_foundations: [ID!]              # Concepts to review if stuck (prerequisites)
  concept_extensions: [ID!]               # Concepts to advance to if proficient (follow-ups)
  exercise_ids: [ID!]!                    # Exercises associated with this concept
  resource_ids: [ID!]!                    # Resources associated with this concept
}

enum ResourceType {
  ARTICLE
  VIDEO
  TUTORIAL
  DOCUMENTATION
}

type Resource {
  resource_id: ID!
  title: String!
  url: String!
  type: ResourceType!                    # Fixed type to help categorize resource
  # Optional fields for future use
  # level: String                        # e.g., Beginner, Intermediate, Advanced
  # tags: [String!]                     # Keywords or categories for filtering/search
  # thumbsUpCount: Int                  # For user rating or usefulness metrics
}


enum HintType {
  STARTER_CODE
  COMMON_MISCONCEPTION
  COMMON_ERROR
  GENERAL_HINT
}


type Hint {
  text: String!
  type: HintType!
  stepNumber: Int    # optional, for ordered steps in starter code
}


type Exercise {
  exercise_id: ID!
  inquiry: String!
  hints: [Hint]!
  solution: [String!]
  minimalAnswerPattern: String
  difficultyScore: Int          # 1 (easy) to 5 (hard) generated from actual usage
  suggestedNextExerciseIds: [ID!]
  suggestedPrevExerciseIds: [ID!]
}




