"""
DocuMind AI - Minimal Version for Render Deployment
This version completely avoids Pinecone imports to prevent package conflicts
"""

import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    """Create the DocuMind AI application"""
    app = FastAPI(
        title="DocuMind AI - Advanced Document Intelligence",
        description="Advanced Document Intelligence System with cloud vector database, reranking, and citations",
        version="2.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Root endpoint - serve React app
    @app.api_route("/", methods=["GET", "HEAD"])
    async def root():
        try:
            with open("frontend/build/index.html", "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
        except FileNotFoundError:
            # Fallback to development mode
            return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>DocuMind AI - Document Intelligence</title>
    <style>
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; text-align: center; }
        h1 { color: #2c3e50; margin-bottom: 20px; }
        .info { background: #e8f4f8; padding: 20px; border-radius: 10px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 DocuMind AI</h1>
        <div class="info">
            <h3>React Frontend Not Built</h3>
            <p>To enable the React frontend, run:</p>
            <code>cd frontend && npm install && npm run build</code>
            <p>Then redeploy the application.</p>
        </div>
        <p><a href="/api/">Go to API endpoints</a></p>
    </div>
</body>
</html>
            """)
        except Exception as e:
            return HTMLResponse(content=f"<h1>Error loading frontend</h1><p>{str(e)}</p>", status_code=500)
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "system": "documind_ai",
            "message": "Service is running",
            "version": "2.0.0",
            "mode": "minimal"
        }
    
    # Favicon endpoint to prevent 404 errors
    @app.get("/favicon.ico")
    async def favicon():
        from fastapi.responses import Response
        return Response(content="", media_type="image/x-icon")
    
    # Serve frontend HTML file directly
    @app.api_route("/api/", methods=["GET", "HEAD"])
    async def serve_frontend():
        try:
            print("🔍 Serving frontend/index.html directly...")
            with open("frontend/index.html", "r", encoding="utf-8") as f:
                content = f.read()
                print(f"✅ Frontend file served successfully, length: {len(content)} characters")
                return HTMLResponse(content=content)
        except FileNotFoundError as e:
            print(f"❌ Frontend file not found: {e}")
            return HTMLResponse(content="<h1>Frontend not found</h1><p>File: frontend/index.html</p>", status_code=404)
        except Exception as e:
            print(f"❌ Error serving frontend: {e}")
            return HTMLResponse(content=f"<h1>Error loading frontend</h1><p>{str(e)}</p>", status_code=500)
    
    # Serve React build assets
    try:
        from fastapi.staticfiles import StaticFiles
        app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")
        print("✅ React static assets mounted")
    except Exception as e:
        print(f"⚠️ Could not mount React static assets: {e}")

    # API endpoint for testing
    @app.get("/api")
    async def api_info():
        return {
            "message": "DocuMind AI API",
            "status": "running",
            "frontend": "React app at root URL",
            "endpoints": {
                "health": "/health",
                "test": "/api/test",
                "upload": "/api/upload",
                "query": "/api/query"
            }
        }
    
    # Basic API endpoints (after frontend mounting)
    @app.get("/api/health")
    async def api_health():
        return {
            "status": "healthy",
            "message": "API is running",
            "mode": "minimal"
        }
    
    @app.get("/api/test")
    async def test_endpoint():
        return {
            "message": "DocuMind AI is working!",
            "status": "success",
            "mode": "minimal",
            "note": "Running in minimal mode - full services require API keys and proper package installation"
        }
    
    @app.get("/api/debug")
    async def debug_endpoint():
        import os
        try:
            # Check if frontend directory exists
            frontend_exists = os.path.exists("frontend")
            index_exists = os.path.exists("frontend/index.html")
            
            # Get file size if it exists
            file_size = 0
            if index_exists:
                file_size = os.path.getsize("frontend/index.html")
            
            return {
                "frontend_directory_exists": frontend_exists,
                "index_html_exists": index_exists,
                "file_size_bytes": file_size,
                "current_directory": os.getcwd(),
                "directory_contents": os.listdir(".") if os.path.exists(".") else "Directory not found"
            }
        except Exception as e:
            return {"error": str(e)}
    
    @app.post("/api/upload")
    async def upload_endpoint():
        return {
            "message": "Upload endpoint ready",
            "status": "minimal_mode",
            "note": "Full upload functionality requires API keys and vector database configuration"
        }
    
    @app.post("/api/query")
    async def query_endpoint():
        return {
            "message": "Query endpoint ready",
            "status": "minimal_mode",
            "note": "Full query functionality requires API keys and vector database configuration"
        }
    
    return app

# Create the DocuMind AI application
app = create_app()
print("🏆 Starting DocuMind AI - Minimal Version")

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "false").lower() == "true"
    
    print(f"🌐 Server starting on {host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔗 DocuMind Frontend: http://{host}:{port}/api/")
    print(f"❤️ Health Check: http://{host}:{port}/health")
    
    try:
        uvicorn.run(
            "minimal_main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        exit(1)
