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
    
    # Root endpoint - redirect to frontend
    @app.api_route("/", methods=["GET", "HEAD"])
    async def root():
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/api/")
    
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
    
    # Serve embedded frontend HTML directly
    @app.api_route("/api/", methods=["GET", "HEAD"])
    async def serve_frontend():
        print("🔍 Serving embedded frontend HTML...")
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DocuMind AI Professional</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: white;
        }
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        .upload-section, .query-section {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        .section-title {
            font-size: 1.3rem;
            margin-bottom: 20px;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        .upload-area {
            border: 3px dashed #bdc3c7;
            border-radius: 10px;
            padding: 40px 20px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            margin-bottom: 20px;
        }
        .upload-area:hover {
            border-color: #3498db;
            background-color: #f8f9fa;
        }
        .upload-icon {
            font-size: 3rem;
            color: #bdc3c7;
            margin-bottom: 15px;
        }
        .upload-text {
            color: #7f8c8d;
            font-size: 1.1rem;
        }
        .text-input {
            width: 100%;
            min-height: 150px;
            padding: 15px;
            border: 2px solid #ecf0f1;
            border-radius: 10px;
            font-size: 1rem;
            resize: vertical;
            font-family: inherit;
        }
        .text-input:focus {
            outline: none;
            border-color: #3498db;
        }
        .query-input {
            width: 100%;
            padding: 15px;
            border: 2px solid #ecf0f1;
            border-radius: 10px;
            font-size: 1rem;
            margin-bottom: 15px;
        }
        .query-input:focus {
            outline: none;
            border-color: #3498db;
        }
        .btn {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-right: 10px;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
        }
        .results-section {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .answer {
            background: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 0 10px 10px 0;
        }
        .answer-text {
            font-size: 1.1rem;
            line-height: 1.8;
            margin-bottom: 15px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.9;
        }
        .error {
            background: #e74c3c;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .success {
            background: #27ae60;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            .header h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 DocuMind AI</h1>
            <p>Professional Document Intelligence System</p>
        </div>

        <div class="main-content">
            <div class="upload-section">
                <h2 class="section-title">📄 Document Upload</h2>
                
                <div class="upload-area" onclick="alert('Upload functionality requires API keys configuration')">
                    <div class="upload-icon">📁</div>
                    <div class="upload-text">
                        <strong>Click to upload</strong> or drag and drop<br>
                        <small>Supports PDF, DOCX, TXT, and more</small>
                    </div>
                </div>

                <div class="section-title">📝 Or Paste Text</div>
                <textarea 
                    class="text-input" 
                    placeholder="Paste your document text here..."
                ></textarea>
                
                <button class="btn" onclick="alert('Upload functionality requires API keys configuration')">Upload Document</button>
                <button class="btn" onclick="document.querySelector('.text-input').value=''">Clear</button>
            </div>

            <div class="query-section">
                <h2 class="section-title">❓ Ask Questions</h2>
                
                <input 
                    type="text" 
                    class="query-input" 
                    placeholder="What would you like to know about the document?"
                >
                
                <button class="btn" onclick="alert('Query functionality requires API keys configuration')">Ask Question</button>
                <button class="btn" onclick="document.querySelector('.query-input').value=''">Clear Query</button>
            </div>
        </div>

        <div class="results-section" style="display: none;">
            <h2 class="section-title">💡 Answer</h2>
            <div class="answer">
                <div class="answer-text">Full functionality requires API keys configuration.</div>
            </div>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">✅</div>
                <div class="stat-label">System Running</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">Minimal</div>
                <div class="stat-label">Mode</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">Ready</div>
                <div class="stat-label">Status</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">API Keys</div>
                <div class="stat-label">Required</div>
            </div>
        </div>
    </div>

    <script>
        console.log('DocuMind AI Frontend loaded successfully!');
        console.log('To enable full functionality, configure API keys in Render dashboard.');
    </script>
</body>
</html>
        """
        print(f"✅ Serving embedded frontend HTML, length: {len(html_content)} characters")
        return HTMLResponse(content=html_content)
    
    # Also serve frontend at root /api path
    @app.api_route("/api", methods=["GET", "HEAD"])
    async def serve_frontend_root():
        print("🔍 Serving embedded frontend HTML from /api...")
        # Same HTML content as above
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DocuMind AI Professional</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 30px; color: white; }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .header p { font-size: 1.1rem; opacity: 0.9; }
        .main-content { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 30px; }
        .upload-section, .query-section { background: white; border-radius: 15px; padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        .section-title { font-size: 1.3rem; margin-bottom: 20px; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        .upload-area { border: 3px dashed #bdc3c7; border-radius: 10px; padding: 40px 20px; text-align: center; transition: all 0.3s ease; cursor: pointer; margin-bottom: 20px; }
        .upload-area:hover { border-color: #3498db; background-color: #f8f9fa; }
        .upload-icon { font-size: 3rem; color: #bdc3c7; margin-bottom: 15px; }
        .upload-text { color: #7f8c8d; font-size: 1.1rem; }
        .text-input { width: 100%; min-height: 150px; padding: 15px; border: 2px solid #ecf0f1; border-radius: 10px; font-size: 1rem; resize: vertical; font-family: inherit; }
        .text-input:focus { outline: none; border-color: #3498db; }
        .query-input { width: 100%; padding: 15px; border: 2px solid #ecf0f1; border-radius: 10px; font-size: 1rem; margin-bottom: 15px; }
        .query-input:focus { outline: none; border-color: #3498db; }
        .btn { background: linear-gradient(135deg, #3498db, #2980b9); color: white; border: none; padding: 12px 25px; border-radius: 8px; font-size: 1rem; cursor: pointer; transition: all 0.3s ease; margin-right: 10px; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4); }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 20px; }
        .stat-card { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 10px; text-align: center; }
        .stat-value { font-size: 2rem; font-weight: bold; margin-bottom: 5px; }
        .stat-label { font-size: 0.9rem; opacity: 0.9; }
        @media (max-width: 768px) { .main-content { grid-template-columns: 1fr; } .header h1 { font-size: 2rem; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 DocuMind AI</h1>
            <p>Professional Document Intelligence System</p>
        </div>
        <div class="main-content">
            <div class="upload-section">
                <h2 class="section-title">📄 Document Upload</h2>
                <div class="upload-area" onclick="alert('Upload functionality requires API keys configuration')">
                    <div class="upload-icon">📁</div>
                    <div class="upload-text"><strong>Click to upload</strong> or drag and drop<br><small>Supports PDF, DOCX, TXT, and more</small></div>
                </div>
                <div class="section-title">📝 Or Paste Text</div>
                <textarea class="text-input" placeholder="Paste your document text here..."></textarea>
                <button class="btn" onclick="alert('Upload functionality requires API keys configuration')">Upload Document</button>
                <button class="btn" onclick="document.querySelector('.text-input').value=''">Clear</button>
            </div>
            <div class="query-section">
                <h2 class="section-title">❓ Ask Questions</h2>
                <input type="text" class="query-input" placeholder="What would you like to know about the document?">
                <button class="btn" onclick="alert('Query functionality requires API keys configuration')">Ask Question</button>
                <button class="btn" onclick="document.querySelector('.query-input').value=''">Clear Query</button>
            </div>
        </div>
        <div class="stats">
            <div class="stat-card"><div class="stat-value">✅</div><div class="stat-label">System Running</div></div>
            <div class="stat-card"><div class="stat-value">Minimal</div><div class="stat-label">Mode</div></div>
            <div class="stat-card"><div class="stat-value">Ready</div><div class="stat-label">Status</div></div>
            <div class="stat-card"><div class="stat-value">API Keys</div><div class="stat-label">Required</div></div>
        </div>
    </div>
    <script>console.log('DocuMind AI Frontend loaded successfully!');</script>
</body>
</html>
        """
        print(f"✅ Serving embedded frontend HTML from /api, length: {len(html_content)} characters")
        return HTMLResponse(content=html_content)
    
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
