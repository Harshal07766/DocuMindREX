"""
DocuMind AI API Routes
FastAPI routes for the DocuMind AI system
"""

import os
import uuid
from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

from services.api_service import get_api_service

# Initialize router
router = APIRouter(prefix="/api", tags=["DocuMind AI"])

# Pydantic models
class QueryRequest(BaseModel):
    document_id: str
    question: str
    top_k: Optional[int] = 10

class TextUploadRequest(BaseModel):
    text: str
    title: Optional[str] = ""
    source: Optional[str] = "text_input"

class SystemInfoResponse(BaseModel):
    vector_database: dict
    chunking: dict
    reranker: dict
    documents_uploaded: int
    total_chunks: int

# Initialize API service
api_service = get_api_service()

@router.get("/", response_class=HTMLResponse)
async def get_frontend():
    """Serve the frontend interface"""
    try:
        with open("frontend/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Frontend not found</h1>", status_code=404)

@router.post("/upload")
async def upload_document(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    title: Optional[str] = Form(""),
    source: Optional[str] = Form("")
):
    """
    Upload a document (file or text)
    """
    try:
        if file and file.filename:
            # Handle file upload
            content = await file.read()
            
            # Extract text based on file type
            if file.filename.endswith('.txt'):
                content_str = content.decode('utf-8')
            elif file.filename.endswith('.md'):
                content_str = content.decode('utf-8')
            elif file.filename.endswith('.pdf'):
                # Use PyMuPDF for PDF processing
                import fitz
                doc = fitz.open(stream=content, filetype="pdf")
                content_str = ""
                for page in doc:
                    content_str += page.get_text()
                doc.close()
            elif file.filename.endswith('.docx'):
                # Use python-docx for DOCX processing
                from docx import Document
                import io
                doc = Document(io.BytesIO(content))
                content_str = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            else:
                # For other file types, try to decode as text
                content_str = content.decode('utf-8', errors='ignore')
            
            result = await api_service.upload_document(
                content=content_str,
                source=source or file.filename,
                title=title or file.filename,
                doc_type=file.filename.split('.')[-1] if '.' in file.filename else 'unknown'
            )
            
        elif text:
            # Handle text upload
            result = await api_service.upload_document(
                content=text,
                source=source or "text_input",
                title=title or "Text Document",
                doc_type="text"
            )
        else:
            raise HTTPException(status_code=400, detail="Either file or text must be provided")
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query")
async def query_document(request: QueryRequest):
    """
    Query a document with a question
    """
    try:
        result = await api_service.query_document(
            document_id=request.document_id,
            question=request.question,
            top_k=request.top_k
        )
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents")
async def list_documents():
    """
    List all uploaded documents
    """
    try:
        documents = api_service.list_documents()
        return {"documents": documents}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/{document_id}")
async def get_document_info(document_id: str):
    """
    Get information about a specific document
    """
    try:
        doc_info = api_service.get_document_info(document_id)
        if not doc_info:
            raise HTTPException(status_code=404, detail="Document not found")
        return doc_info
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/system")
async def get_system_info():
    """
    Get system configuration and status
    """
    try:
        info = api_service.get_system_info()
        return info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """
    Delete a document and its chunks
    """
    try:
        if document_id not in api_service.documents:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Remove from memory
        del api_service.documents[document_id]
        if document_id in api_service.document_chunks:
            del api_service.document_chunks[document_id]
        
        return {"success": True, "message": "Document deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    try:
        system_info = api_service.get_system_info()
        return {
            "status": "healthy",
            "message": "Track B Mini RAG API is operational",
            "system_info": system_info
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"System error: {str(e)}"
        }

# Additional utility endpoints for Track B compliance

@router.get("/chunking-params")
async def get_chunking_parameters():
    """
    Get current chunking parameters
    """
    try:
        params = api_service.chunker.get_chunking_parameters()
        return params
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reranker-info")
async def get_reranker_info():
    """
    Get reranker configuration information
    """
    try:
        info = api_service.reranker.get_reranker_info()
        return info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/vector-db-info")
async def get_vector_db_info():
    """
    Get vector database configuration information
    """
    try:
        info = {
            "provider": api_service.vector_db.provider,
            "collection_name": "hackrx_documents",
            "embedding_dimension": 3072,
            "base_url": api_service.vector_db.base_url,
            "api_configured": bool(api_service.vector_db.api_key)
        }
        return info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Evaluation endpoint for Track B compliance
@router.post("/evaluate")
async def evaluate_system(document_id: Optional[str] = None):
    """
    Run evaluation with 5 Q&A pairs (Track B requirement)
    """
    try:
        from evaluation.track_b_evaluation import get_track_b_evaluation
        
        if not document_id:
            # Return evaluation framework info
            evaluation = get_track_b_evaluation()
            return {
                "evaluation_questions": [
                    {
                        "id": q.id,
                        "question": q.question,
                        "category": q.category,
                        "difficulty": q.difficulty
                    }
                    for q in evaluation.evaluation_questions
                ],
                "message": "Evaluation framework ready. Provide document_id to run evaluation.",
                "note": "This endpoint provides the evaluation structure required for Track B compliance"
            }
        
        # Run actual evaluation
        evaluation = get_track_b_evaluation()
        results = await evaluation.evaluate_document(api_service, document_id)
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evaluate/{document_id}")
async def evaluate_document(document_id: str):
    """
    Evaluate a specific document with 5 Q&A pairs
    """
    try:
        from evaluation.track_b_evaluation import get_track_b_evaluation
        
        evaluation = get_track_b_evaluation()
        results = await evaluation.evaluate_document(api_service, document_id)
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
