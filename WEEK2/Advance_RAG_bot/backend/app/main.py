from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import base64
import json
from typing import List, Optional
import logging
import traceback

# Configure logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenTelemetry imports (optional)
try:
    import opentelemetry
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
    OPENTELEMETRY_AVAILABLE = True
    logger.info("OpenTelemetry available - observability features enabled")
except ImportError:
    OPENTELEMETRY_AVAILABLE = False
    logger.warning("OpenTelemetry not available - observability features disabled")

from models.models import ChatMessage, ChatResponse, ConfigUpdate, RAGVariant, UploadResponse, DocumentInfo, LLMProvider, DocumentType, MemoryMessage
from services.llm_service import LLMService, InternetSearchService
from services.rag_service import RAGFactory
from services.guardrails import EnhancedGuardrailsService
from services.memory import ConversationMemory
from services.document_processor import DocumentProcessor
from config import settings

# Initialize OpenTelemetry (if available)
def setup_observability():
    """Setup OpenTelemetry tracing"""
    if not OPENTELEMETRY_AVAILABLE:
        logger.info("OpenTelemetry not available - skipping observability setup")
        return
        
    try:
        # Set up the tracer provider
        trace.set_tracer_provider(TracerProvider())
        tracer = trace.get_tracer(__name__)
        
        # Configure OTLP exporter
        if settings.OPIK_API_KEY and settings.OPIK_ENDPOINT:
            otlp_exporter = OTLPSpanExporter(
                endpoint=settings.OPIK_ENDPOINT,
                headers={"Authorization": f"Bearer {settings.OPIK_API_KEY}"}
            )
            
            # Add batch span processor
            span_processor = BatchSpanProcessor(otlp_exporter)
            trace.get_tracer_provider().add_span_processor(span_processor)
            
            logger.info("OpenTelemetry tracing configured successfully")
        else:
            logger.warning("OpenTelemetry not configured - missing API key or endpoint")
            
    except Exception as e:
        logger.error(f"Failed to setup observability: {e}")

# Setup observability
setup_observability()

# Initialize services
llm_service = LLMService()
search_service = InternetSearchService()
guardrails = EnhancedGuardrailsService()
memory = ConversationMemory()
document_processor = DocumentProcessor()

# Global configuration
current_config = ConfigUpdate(
    selected_llm=settings.AVAILABLE_LLMS[0] if settings.AVAILABLE_LLMS else "gemini:gemini-2.0-flash",
    selected_rag_variant=RAGVariant.BASIC,
    selected_documents=[],
    enable_internet_search=False
)

rag_service = RAGFactory.create_rag(current_config.selected_rag_variant, search_service)

app = FastAPI(title="Enhanced Multi-modal RAG Chatbot", version="2.0.0")

# Instrument FastAPI with OpenTelemetry (if available)
if OPENTELEMETRY_AVAILABLE:
    try:
        FastAPIInstrumentor.instrument_app(app)
        RequestsInstrumentor().instrument()
        HTTPXClientInstrumentor().instrument()
        logger.info("FastAPI instrumented with OpenTelemetry")
    except Exception as e:
        logger.warning(f"Failed to instrument FastAPI: {e}")
else:
    logger.info("OpenTelemetry not available - skipping instrumentation")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Enhanced Multi-modal RAG Chatbot API"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "backend": "running",
        "llm_available": bool(settings.GEMINI_API_KEY or settings.GROQ_API_KEY or settings.COHERE_API_KEY)
    }

@app.get("/config/llms")
async def get_available_llms():
    return {"llms": settings.AVAILABLE_LLMS}

@app.get("/config/rag-variants")
async def get_rag_variants():
    return {"variants": settings.RAG_VARIANTS}

@app.post("/config/update")
async def update_config(config: ConfigUpdate):
    global current_config, rag_service
    try:
        current_config = config
        rag_service = RAGFactory.create_rag(config.selected_rag_variant, search_service)
        logger.info(f"Configuration updated: LLM={config.selected_llm}, RAG={config.selected_rag_variant}")
        return {"status": "configuration updated"}
    except Exception as e:
        logger.error(f"Config update error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Configuration update failed: {str(e)}")

@app.get("/config/current")
async def get_current_config():
    return current_config

@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        
        # Validate file size
        if len(contents) > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")
        
        # Process document
        result = await document_processor.process_uploaded_file(contents, file.filename)
        
        if result["success"]:
            logger.info(f"Document uploaded: {file.filename}")
            return UploadResponse(
                success=True,
                document_id=result["document_id"],
                filename=result["filename"],
                message=result["message"],
                document_type=result["document_type"]
            )
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Upload failed"))
            
    except Exception as e:
        logger.error(f"Document upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/documents/upload-multiple")
async def upload_multiple_documents(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        try:
            contents = await file.read()
            result = await document_processor.process_uploaded_file(contents, file.filename)
            results.append(result)
        except Exception as e:
            results.append({
                "success": False,
                "filename": file.filename,
                "error": str(e)
            })
    
    return {"results": results}

@app.get("/documents/list")
async def list_documents():
    documents = document_processor.get_all_documents()
    return {"documents": documents}

@app.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    success = document_processor.delete_document(document_id)
    return {"success": success}

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    try:
        logger.info(f"Chat request received: {chat_message.message[:100]}...")
        
        # Get document context if documents are selected
        document_context = []
        if chat_message.document_ids:
            document_context = document_processor.get_document_content(chat_message.document_ids)
            logger.info(f"Using {len(document_context)} document contexts")
        
        # Enhanced validation with document relevance
        safety_check = guardrails.validate_request(
            chat_message.message, 
            chat_message.images, 
            document_context
        )
        
        if not safety_check["safe"]:
            logger.warning(f"Request rejected: {safety_check['rejection_reason']}")
            return JSONResponse(
                status_code=400,
                content={
                    "response": f"Request rejected: {safety_check['rejection_reason']}",
                    "sources": [],
                    "session_id": chat_message.session_id,
                    "is_relevant": safety_check["is_relevant"],
                    "rejection_reason": safety_check["rejection_reason"]
                }
            )
        
        # Add user message to memory with document context
        memory.add_message(
            session_id=chat_message.session_id,
            role="user", 
            content=chat_message.message,
            document_context=document_context
        )
        
        # Get conversation context
        context = memory.get_context_string(chat_message.session_id)
        logger.info(f"Conversation context length: {len(context)} characters")
        
        # Perform RAG search
        rag_results = []
        if current_config.selected_documents or current_config.enable_internet_search:
            try:
                if current_config.selected_rag_variant == "hybrid":
                    rag_results = await rag_service.search(chat_message.message)
                else:
                    rag_results = rag_service.search(chat_message.message)
                logger.info(f"RAG search returned {len(rag_results)} results")
            except Exception as e:
                logger.warning(f"RAG search failed: {str(e)}")
                rag_results = []
        
        # Prepare context for LLM
        context_text = "\n".join([result.get("content", "") for result in rag_results]) if rag_results else ""
        
        # Generate response
        llm_response = await llm_service.generate_response(
            current_config.selected_llm,
            chat_message.message,
            chat_message.images,
            context_text,
            document_context
        )
        
        # Add assistant response to memory
        memory.add_message(
            session_id=chat_message.session_id,
            role="assistant", 
            content=llm_response["content"],
            document_context=document_context
        )
        
        logger.info(f"Chat response generated successfully. Tokens used: {llm_response.get('tokens_used', 0)}")
        
        return ChatResponse(
            response=llm_response["content"],
            sources=rag_results,
            session_id=chat_message.session_id,
            tokens_used=llm_response.get("tokens_used", 0),
            is_relevant=True
        )
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")

@app.get("/memory/{session_id}")
async def get_conversation_memory(session_id: str):
    history = memory.get_conversation_history(session_id)
    return {"session_id": session_id, "history": history}

@app.delete("/memory/{session_id}")
async def clear_memory(session_id: str):
    memory.clear_memory(session_id)
    return {"status": "memory cleared"}

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)



