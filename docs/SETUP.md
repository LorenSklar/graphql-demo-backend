# Setup Guide

This document covers setup for both local development and production deployment.

## Local Development Setup

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Virtual Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Verify activation (should show venv path)
which python  # macOS/Linux
where python  # Windows
```

### Install Dependencies
```bash
# Make sure virtual environment is activated
pip install -r requirements.txt

# Verify installation
pip list
```

### Run Locally
```bash
# Start Flask development server
python app.py

# Server will be available at:
# http://localhost:8000
# http://127.0.0.1:8000
```

### Test Endpoints
```bash
# Test GraphQL endpoints with curl
curl -X POST http://localhost:8000/content \
  -H "Content-Type: application/json" \
  -d '{"query": "{ ping marco field }"}'

curl -X POST http://localhost:8000/sandbox \
  -H "Content-Type: application/json" \
  -d '{"query": "{ ping }"}'

# Test logging endpoint
curl -X POST http://localhost:8000/log \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "response": "success", "success": true}'
```

### Development Features
- **Auto-reload**: Flask debug mode enabled
- **CORS**: Allows localhost:5173 and localhost:3000
- **Error handling**: Detailed error messages in development

## Production Deployment (Render)

### Environment Variables

Set these in your Render app dashboard:

#### Required Variables
```
ALLOWED_ORIGINS=https://your-frontend.vercel.app
FLASK_ENV=production
FLASK_DEBUG=false
```

#### Optional Variables
```
PORT=8000
HOST=0.0.0.0
```

### CORS Configuration

The `ALLOWED_ORIGINS` variable controls which frontend domains can access your backend:

- **Single domain**: `https://your-frontend.vercel.app`
- **Multiple domains**: `https://domain1.com,https://domain2.com`
- **Development**: Automatically allows localhost:5173 and localhost:3000

### Build Commands

#### Build Command
```bash
pip install -r requirements.txt
```

#### Start Command
```bash
python app.py
```

### Render Settings

#### Build & Deploy
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`

#### Environment
- **Python Version**: 3.11 or higher
- **Port**: 8000 (or use `$PORT` environment variable)

### Health Check

Your app will be available at:
- **Health Check URL**: `https://your-app.onrender.com/`
- **GraphQL Endpoints**: 
  - `/content` (POST)
  - `/sandbox` (POST)
  - `/log` (POST)

## Frontend Integration

### Local Development
- **Backend URL**: `http://localhost:8000`
- **CORS**: Automatically configured for localhost

### Production
- **Backend URL**: `https://your-app.onrender.com`
- **CORS**: Ensure your Vercel domain is in `ALLOWED_ORIGINS`

## Troubleshooting

### Local Development Issues

#### Virtual Environment Problems
```bash
# If venv activation fails
python -m venv --clear venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

#### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or change port in app.py
```

#### Import Errors
```bash
# Ensure virtual environment is activated
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Production Issues

#### CORS Errors
- Verify `ALLOWED_ORIGINS` is set correctly
- Check that your frontend domain is included
- Ensure no trailing slashes in domain URLs

#### Port Issues
- Ensure `HOST=0.0.0.0` and `PORT=8000`
- Render may override with `$PORT` environment variable

#### Build Failures
- Check Python version compatibility
- Verify all dependencies are in requirements.txt
- Check Render logs for detailed error messages

### Debug Mode

#### Local Development
- Debug mode is automatically enabled
- Detailed error messages and stack traces
- Auto-reload on code changes

#### Production
- Set `FLASK_DEBUG=true` temporarily for debugging
- Check Render logs for detailed error messages
- **Remember to set back to `false` after debugging**

## Security Notes

- Never commit `.env` files to version control
- Use Render's environment variable system for production
- Restrict `ALLOWED_ORIGINS` to only necessary domains
- Keep `FLASK_DEBUG=false` in production
- Virtual environment keeps dependencies isolated locally

## File Structure

```
graphql-demo-backend/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── SETUP.md              # This setup guide
├── README.md             # Project overview
├── CONTRACTS.md          # Data contracts
├── breadcrumbs.md        # Development progress (gitignored)
├── reflections.md         # Development insights (gitignored)
└── venv/                 # Virtual environment (gitignored)
```
