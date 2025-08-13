# GraphQL Practice Tool Backend

A Python-based GraphQL API backend that provides the core functionality for an interactive GraphQL learning platform. This backend serves lesson content, handles interactive query execution, and logs user interactions for a hands-on GraphQL learning experience.

## Architecture

- **Hosting**: Render (Python backend)
- **Frontend**: Separate Vercel deployment (consumes this API)
- **Data**: File-based storage (no database for MVP)
- **Authentication**: None (public learning tool)

## API Endpoints

### `/content` (GraphQL)
Main GraphQL endpoint that serves:
- Lesson content and objectives
- Interactive query execution
- Sample data and schemas
- Success/error feedback

### `/log` (REST)
Tracks user interactions and system responses:
- User query submissions
- GraphQL query results
- Error responses
- User progress through lessons

### `/sandbox` (GraphQL)
Interactive playground endpoint for hands-on GraphQL practice:
- Simple queries to build confidence
- Progressive complexity for skill development
- Real GraphQL execution and error handling

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Run tests
python -m pytest
```

## Project Structure

```
graphql-demo-backend/
├── app.py                 # Main Flask application
├── schema/               # GraphQL schema definitions
├── resolvers/            # GraphQL resolver functions
├── lessons/              # Lesson content and data
├── sandbox/              # Sandbox endpoint logic
├── logging/              # Logging utilities
└── requirements.txt      # Python dependencies
```

## Key Features

- **Real-time GraphQL execution**: Live query processing with immediate feedback
- **Structured lesson system**: Progressive learning through predefined exercises
- **Interactive sandbox**: Hands-on GraphQL practice environment
- **Comprehensive logging**: Track user behavior and system performance
- **File-based data**: No database setup required for MVP

## MVP Scope

- ✅ Core GraphQL API with basic lesson content
- ✅ Interactive sandbox with simple queries
- ✅ User interaction logging
- ✅ File-based data storage
- 🔄 Complete single lesson end-to-end
- 🔄 Multiple lessons and progression
- 🔄 User progress tracking (v2)
- 🔄 Reflection storage (v2)
- 🔄 Authentication system (v2)
- 🔄 Database persistence (v2)

## Version Roadmap

### MVP (v1.0) - 2-4 weeks
**Goal**: Single lesson working end-to-end
- Core GraphQL API with one complete lesson
- Basic sandbox for GraphQL practice
- File-based data storage
- Simple logging system
- Frontend integration working

### Enhanced MVP (v2.0) - 2-3 months
**Goal**: Multiple lessons and basic progression
- Multiple lesson content
- Simple lesson sequencing
- User progress tracking
- Enhanced logging and analytics

### Learning System (v3.0) - 4-6 months
**Goal**: Advanced learning features
- Concept relationships and prerequisites
- Exercise difficulty adaptation
- User reflection and feedback
- Basic analytics dashboard

## Deployment
The backend is designed to deploy to Render with minimal configuration. All data is file-based, making it stateless and easy to scale.
