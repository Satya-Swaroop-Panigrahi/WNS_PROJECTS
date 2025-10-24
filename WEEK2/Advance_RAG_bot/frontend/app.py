import streamlit as st
import requests
import base64
from PIL import Image
import io
import uuid
import os
import time

# Backend API URL
API_BASE = "http://localhost:8000"

# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="Enhanced Multi-modal RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Enhanced CSS for modern UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);
    }
    
    .main-header h1 {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    .sidebar h3 {
        color: #2d3748;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    /* Metric Cards */
    .stMetric {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .stMetric > div > div > div {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3748;
    }
    
    .stMetric > div > div > div:last-child {
        font-size: 0.875rem;
        color: #718096;
        font-weight: 400;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(102, 126, 234, 0.2);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* File Uploader */
    .stFileUploader {
        border: 2px dashed #cbd5e0;
        border-radius: 0.75rem;
        padding: 1.5rem;
        background: #f8fafc;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #667eea;
        background: #f7fafc;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* Chat Messages */
    .chat-message {
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        border-radius: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        font-family: 'Inter', sans-serif;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
        border-bottom-right-radius: 0.25rem;
    }
    
    .assistant-message {
        background: #f8fafc;
        color: #2d3748;
        margin-right: 20%;
        border-bottom-left-radius: 0.25rem;
        border: 1px solid #e2e8f0;
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: #f0fff4;
        color: #22543d;
        border-radius: 0.5rem;
        font-size: 0.875rem;
        font-weight: 500;
        border: 1px solid #9ae6b4;
    }
    
    .status-indicator.warning {
        background: #fffbeb;
        color: #92400e;
        border-color: #fbbf24;
    }
    
    .status-indicator.error {
        background: #fed7d7;
        color: #c53030;
        border-color: #fc8181;
    }
    
    /* Document Cards */
    .document-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 0.75rem;
        padding: 1rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .document-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Progress Bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: #f0fff4;
        border: 1px solid #9ae6b4;
        color: #22543d;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    .stError {
        background: #fed7d7;
        border: 1px solid #fc8181;
        color: #c53030;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    .stWarning {
        background: #fffbeb;
        border: 1px solid #fbbf24;
        color: #92400e;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    /* Info Boxes */
    .stInfo {
        background: #ebf8ff;
        border: 1px solid #90cdf4;
        color: #2b6cb0;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e0;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a0aec0;
    }
    
    /* Animation for new messages */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .chat-message {
        animation: slideIn 0.3s ease-out;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .user-message, .assistant-message {
            margin-left: 0;
            margin-right: 0;
        }
    }
</style>
""", unsafe_allow_html=True)

def init_session():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    if "uploaded_documents" not in st.session_state:
        st.session_state.uploaded_documents = []
    if "selected_documents" not in st.session_state:
        st.session_state.selected_documents = []
    if "last_config_update" not in st.session_state:
        st.session_state.last_config_update = 0
    if "last_document_update" not in st.session_state:
        st.session_state.last_document_update = 0
    if "current_config" not in st.session_state:
        st.session_state.current_config = {}
    if "refresh_trigger" not in st.session_state:
        st.session_state.refresh_trigger = 0
    
    # Clean up any corrupted session state
    if "llm_selector" in st.session_state and not isinstance(st.session_state.llm_selector, str):
        del st.session_state.llm_selector
    if "rag_selector" in st.session_state and not isinstance(st.session_state.rag_selector, str):
        del st.session_state.rag_selector

def trigger_refresh():
    """Trigger a refresh of the system status"""
    st.session_state.refresh_trigger += 1

def get_available_llms():
    try:
        response = requests.get(f"{API_BASE}/config/llms")
        if response.status_code == 200:
            return response.json()["llms"]
    except:
        pass
    return ["gemini:gemini-2.0-flash"]

def get_rag_variants():
    try:
        response = requests.get(f"{API_BASE}/config/rag-variants")
        if response.status_code == 200:
            return response.json()["variants"]
    except:
        pass
    return ["basic", "knowledge_graph", "hybrid"]

def get_uploaded_documents():
    try:
        response = requests.get(f"{API_BASE}/documents/list")
        if response.status_code == 200:
            return response.json()["documents"]
    except:
        pass
    return []

def get_current_config():
    """Get current configuration from backend with caching"""
    current_time = time.time()
    
    # Cache for 2 seconds to avoid too many API calls
    if (current_time - st.session_state.get('last_config_update', 0) < 2 and 
        st.session_state.get('current_config')):
        return st.session_state.current_config
    
    try:
        response = requests.get(f"{API_BASE}/config/current")
        if response.status_code == 200:
            config = response.json()
            st.session_state.current_config = config
            st.session_state.last_config_update = current_time
            return config
    except Exception as e:
        st.error(f"❌ Cannot connect to backend: {e}")
    
    return {}

def update_config(selected_llm, selected_rag, selected_docs, enable_search):
    config = {
        "selected_llm": selected_llm,
        "selected_rag_variant": selected_rag,
        "selected_documents": selected_docs,
        "enable_internet_search": enable_search
    }
    try:
        response = requests.post(f"{API_BASE}/config/update", json=config)
        if response.status_code == 200:
            # Clear cache to force refresh
            st.session_state.last_config_update = 0
            trigger_refresh()
            return True
        else:
            st.error(f"❌ Backend returned status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        st.error(f"❌ Configuration update failed: {e}")
        return False

def upload_document(file):
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(f"{API_BASE}/documents/upload", files=files)
        if response.status_code == 200:
            # Clear cache to force refresh
            st.session_state.last_document_update = 0
            trigger_refresh()
            return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}
    return {"success": False, "error": "Upload failed"}

def upload_multiple_documents(files):
    results = []
    for file in files:
        result = upload_document(file)
        results.append(result)
    return results

def send_message(message, images, document_ids):
    data = {
        "message": message,
        "images": images,
        "session_id": st.session_state.session_id,
        "document_ids": document_ids
    }
    try:
        response = requests.post(f"{API_BASE}/chat", json=data)
        if response.status_code == 200:
            trigger_refresh()  # Refresh status after chat
            return response.json()
    except Exception as e:
        return {"response": f"Error: {str(e)}", "sources": []}
    return {"response": "Error: Failed to get response", "sources": []}

def display_system_status():
    """Display system status with enhanced styling"""
    st.subheader("📊 System Status")
    
    # Get current configuration
    config = get_current_config()
    
    if config:
        # Display configuration in a nice format
        selected_llm = config.get('selected_llm', 'Not set')
        is_gemini = selected_llm.startswith("gemini:")
        
        # Determine web search status based on model type
        web_search_status = "✅ Enabled (Auto)" if not is_gemini else ("✅ On" if config.get('enable_internet_search') else "❌ Off")

        # Enhanced metrics with better styling
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🤖 LLM Provider", selected_llm.split(':')[0].title() if ':' in selected_llm else selected_llm)
        with col2:
            st.metric("🔍 Internet Search", "Enabled" if "✅" in web_search_status else "Disabled")
        
        # Additional status indicators
        st.markdown("""
        <div class="status-indicator">
            <i class="fas fa-check-circle"></i>
            Backend Connected
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.markdown("""
        <div class="status-indicator error">
            <i class="fas fa-exclamation-circle"></i>
            Backend Disconnected
        </div>
        """, unsafe_allow_html=True)
        st.info("Make sure the backend server is running on http://localhost:8000")

def display_uploaded_documents():
    """Display uploaded documents with enhanced styling"""
    st.subheader("📂 Uploaded Documents")
    
    # Use cached documents or fetch new ones
    current_time = time.time()
    if (current_time - st.session_state.get('last_document_update', 0) > 5 or 
        not st.session_state.get('uploaded_documents')):
        st.session_state.uploaded_documents = get_uploaded_documents()
        st.session_state.last_document_update = current_time
    
    uploaded_docs = st.session_state.uploaded_documents
    
    if uploaded_docs:
        for doc in uploaded_docs:
            # Enhanced document card
            st.markdown(f"""
            <div class="document-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <div>
                        <strong>📄 {doc['name']}</strong>
                        <div style="font-size: 0.75rem; color: #718096; margin-top: 0.25rem;">
                            Type: {doc['type']} | Size: {doc.get('size', 0)} bytes
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([4, 1])
            with col1:
                if doc.get('content_summary'):
                    with st.expander("📖 Preview Content", expanded=False):
                        st.text(doc['content_summary'][:300] + "..." if len(doc['content_summary']) > 300 else doc['content_summary'])
            with col2:
                if st.button("🗑️", key=f"delete_{doc['id']}", help="Delete document"):
                    try:
                        response = requests.delete(f"{API_BASE}/documents/{doc['id']}")
                        if response.status_code == 200:
                            st.success(f"✅ Deleted {doc['name']}")
                            st.session_state.last_document_update = 0
                            trigger_refresh()
                            st.rerun()
                    except:
                        st.error("❌ Failed to delete document")
    else:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #a0aec0;">
            <i class="fas fa-file-alt" style="font-size: 2rem; margin-bottom: 1rem;"></i>
            <p>No documents uploaded yet</p>
            <p style="font-size: 0.875rem;">Upload documents to start chatting with them!</p>
        </div>
        """, unsafe_allow_html=True)
        
    # Refresh button for documents
    if st.button("🔄 Refresh Documents", key="refresh_docs"):
        st.session_state.last_document_update = 0
        trigger_refresh()
        st.rerun()

def display_conversation_memory():
    """Display conversation memory with enhanced styling"""
    st.subheader("🧠 Memory Usage")
    
    # Current memory stats with enhanced metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💬 Messages", len(st.session_state.conversation))
    with col2:
        st.metric("🆔 Session", st.session_state.session_id[:8] + "...")
    
    # Memory status indicator
    memory_status = "🟢 Active" if len(st.session_state.conversation) > 0 else "⚪ Empty"
    st.markdown(f"""
    <div class="status-indicator" style="margin-bottom: 1rem;">
        <i class="fas fa-brain"></i>
        Memory Status: {memory_status}
    </div>
    """, unsafe_allow_html=True)
    
    # Clear memory button
    if st.button("🗑️ Clear Memory", key="clear_memory_main"):
        st.session_state.conversation = []
        trigger_refresh()
        st.success("✅ Memory cleared successfully!")
    
    # Conversation history with enhanced display
    if st.session_state.conversation:
        with st.expander("📜 View Conversation History", expanded=False):
            for i, msg in enumerate(st.session_state.conversation[-10:]):
                role_icon = "👤" if msg['role'] == 'user' else "🤖"
                message_class = "user-message" if msg['role'] == 'user' else "assistant-message"
                
                st.markdown(f"""
                <div class="chat-message {message_class}">
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                        <span>{role_icon}</span>
                        <strong>{msg['role'].title()}</strong>
                    </div>
                    <div>{msg['content']}</div>
                    {"<div style='margin-top: 0.5rem; font-size: 0.875rem; opacity: 0.7;'>📷 Image attached</div>" if "images" in msg and msg["images"] else ""}
                </div>
                """, unsafe_allow_html=True)

def main():
    init_session()
    
    # Modern Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Enhanced Multi-modal Advanced RAG Chatbot</h1>
        <p>Powered by Advanced AI with Multi-modal Support, Internet Search & Enhanced Guardrails</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main chat area - moved outside of sidebar
    st.subheader("💬 Chat Interface")
    
    # Display conversation with enhanced styling
    for msg in st.session_state.conversation:
        role_icon = "👤" if msg['role'] == 'user' else "🤖"
        message_class = "user-message" if msg['role'] == 'user' else "assistant-message"
        
        st.markdown(f"""
        <div class="chat-message {message_class}">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <span>{role_icon}</span>
                <strong>{msg['role'].title()}</strong>
            </div>
            <div>{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if "images" in msg and msg["images"]:
            st.markdown("**📷 Attached Images:**")
            for img_data in msg["images"]:
                try:
                    img_bytes = base64.b64decode(img_data)
                    image = Image.open(io.BytesIO(img_bytes))
                    st.image(image, caption="Uploaded Image", width=200)
                except:
                    st.write("📷 *Image attachment*")
    
    # Image upload section
    st.subheader("📷 Upload Images")
    uploaded_images = st.file_uploader(
        "Upload Images",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        key="image_uploader"
    )
    
    # Convert images to base64
    image_data_list = []
    if uploaded_images:
        for uploaded_image in uploaded_images:
            image_bytes = uploaded_image.read()
            image_b64 = base64.b64encode(image_bytes).decode('utf-8')
            image_data_list.append(image_b64)
            # Display uploaded image
            st.image(image_bytes, caption=uploaded_image.name, width=150)
    
    # Chat input - now completely outside any containers
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add user message to conversation
        st.session_state.conversation.append({
            "role": "user",
            "content": user_input,
            "images": image_data_list
        })
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
            for img_data in image_data_list:
                try:
                    img_bytes = base64.b64decode(img_data)
                    image = Image.open(io.BytesIO(img_bytes))
                    st.image(image, caption="Uploaded Image", width=200)
                except:
                    st.write("📷 *Image attachment*")
        
        # Get AI response with enhanced styling
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                response = send_message(user_input, image_data_list, st.session_state.selected_documents)
                
                if response.get("rejection_reason"):
                    st.markdown(f"""
                    <div class="chat-message assistant-message" style="background: #fed7d7; color: #c53030; border: 1px solid #fc8181;">
                        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                            <span>🚫</span>
                            <strong>Request Rejected</strong>
                        </div>
                        <div>{response['response']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message assistant-message">
                        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                            <span>🤖</span>
                            <strong>Assistant</strong>
                        </div>
                        <div>{response['response']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Display sources with enhanced styling
                if response.get("sources"):
                    st.markdown("""
                    <div class="message-sources">
                        <div class="sources-title">
                            <i class="fas fa-book"></i>
                            Sources & References
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for i, source in enumerate(response["sources"]):
                        source_type = source.get('type', 'unknown')
                        source_icon = "📄" if source_type == 'semantic' else "🌐" if source_type == 'internet' else "📚"
                        
                        st.markdown(f"""
                        <div class="source-item">
                            <div class="source-title">
                                {source_icon} {source.get('title', 'Unknown Source')}
                            </div>
                            <div class="source-snippet">
                                {source.get('snippet', source.get('content', 'No content available'))}
                            </div>
                            {f'<a href="{source.get("link")}" class="source-link" target="_blank">🔗 View Source</a>' if source.get('link') else ''}
                        </div>
                        """, unsafe_allow_html=True)
        
        # Add assistant response to conversation
        if not response.get("rejection_reason"):
            st.session_state.conversation.append({
                "role": "assistant",
                "content": response["response"]
            })
        
        # Force a small refresh to update the status panel
        trigger_refresh()
    
    # Sidebar for configuration - moved after chat input
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Get current config to set defaults
        current_config_data = get_current_config()
        
        # Get available options first
        available_llms = get_available_llms()
        rag_variants = get_rag_variants()
        
        # LLM Selection
        current_llm = current_config_data.get('selected_llm', available_llms[0])
        llm_index = available_llms.index(current_llm) if current_llm in available_llms else 0
        selected_llm = st.selectbox(
            "Select LLM", 
            available_llms, 
            index=llm_index, 
            key="llm_selector"
        )
        
        # RAG Variant Selection
        current_rag = current_config_data.get('selected_rag_variant', rag_variants[0])
        rag_index = rag_variants.index(current_rag) if current_rag in rag_variants else 0
        selected_rag = st.selectbox(
            "RAG Variant", 
            rag_variants, 
            index=rag_index, 
            key="rag_selector"
        )
        
        # Check if selections have changed and update config
        if (selected_llm != current_llm or selected_rag != current_rag):
            try:
                is_gemini = selected_llm.startswith("gemini:")
                enable_search = st.session_state.get('search_toggle', False) if is_gemini else True
                selected_docs = st.session_state.get('selected_documents', [])

                success = update_config(
                    selected_llm,
                    selected_rag,
                    selected_docs,
                    enable_search
                )
                if success:
                    st.success("✅ Configuration updated!")
                    st.rerun()  # Force refresh to show updated values
                else:
                    st.error("❌ Failed to update configuration")
            except Exception as e:
                st.error(f"❌ Configuration error: {str(e)}")
        
        # Document Management
        st.subheader("📁 Document Management")
        
        uploaded_files = st.file_uploader(
            "Upload Documents (Multiple files supported)",
            type=['pdf', 'txt', 'docx', 'doc', 'png', 'jpg', 'jpeg', 'pptx', 'xlsx'],
            accept_multiple_files=True,
            key="multi_file_uploader"
        )
        
        if uploaded_files and st.button("Upload Files", key="upload_files_btn"):
            with st.spinner("Uploading files..."):
                results = upload_multiple_documents(uploaded_files)
                
                success_count = 0
                for i, result in enumerate(results):
                    if result.get("success"):
                        success_count += 1
                        st.success(f"✅ {uploaded_files[i].name} uploaded successfully!")
                    else:
                        st.error(f"❌ Failed to upload {uploaded_files[i].name}: {result.get('error', 'Unknown error')}")
                
                if success_count > 0:
                    # Force refresh of documents list
                    st.session_state.last_document_update = 0
                    trigger_refresh()
        
        # Document selection
        uploaded_docs = get_uploaded_documents()
        if uploaded_docs:
            st.subheader("📄 Select Documents for Chat")
            doc_options = {doc['name']: doc['id'] for doc in uploaded_docs}
            default_selected = [name for name, doc_id in doc_options.items() if doc_id in current_config_data.get('selected_documents', [])]
            
            selected_doc_names = st.multiselect(
                "Choose documents to chat with:",
                options=list(doc_options.keys()),
                default=default_selected,
                key="doc_selector"
            )
            
            # Update selected documents if changed
            selected_doc_ids = [doc_options[name] for name in selected_doc_names if name in doc_options]
            if selected_doc_ids != st.session_state.get('selected_documents', []):
                st.session_state.selected_documents = selected_doc_ids
                try:
                    current_llm = st.session_state.get('llm_selector', available_llms[0])
                    current_rag = st.session_state.get('rag_selector', rag_variants[0])
                    is_gemini = current_llm.startswith("gemini:")
                    enable_search = st.session_state.get('search_toggle', False) if is_gemini else True

                    success = update_config(
                        current_llm,
                        current_rag,
                        selected_doc_ids,
                        enable_search
                    )
                    if success:
                        st.success("✅ Document selection updated!")
                    else:
                        st.error("❌ Failed to update document selection")
                except Exception as e:
                    st.error(f"❌ Document selection error: {str(e)}")
        
        # Internet Search Toggle
        is_gemini_selected = st.session_state.get('llm_selector', '').startswith("gemini:")
        search_value = current_config_data.get('enable_internet_search', False) if is_gemini_selected else True
        search_enabled = st.checkbox(
            "🔍 Enable Internet Search", 
            value=search_value, 
            key="search_toggle", 
            disabled=not is_gemini_selected
        )
        
        # Update search setting if changed
        if search_enabled != current_config_data.get('enable_internet_search', False):
            try:
                current_llm = st.session_state.get('llm_selector', available_llms[0])
                current_rag = st.session_state.get('rag_selector', rag_variants[0])
                selected_docs = st.session_state.get('selected_documents', [])

                success = update_config(
                    current_llm,
                    current_rag,
                    selected_docs,
                    search_enabled
                )
                if success:
                    st.success("✅ Internet search setting updated!")
                else:
                    st.error("❌ Failed to update internet search setting")
            except Exception as e:
                st.error(f"❌ Internet search error: {str(e)}")
        
        st.markdown("---")
        st.subheader("🔧 Debug Info")
        with st.expander("Current Configuration", expanded=False):
            st.json(current_config_data)
            st.write(f"Session State LLM: {st.session_state.get('llm_selector', 'Not set')}")
            st.write(f"Session State RAG: {st.session_state.get('rag_selector', 'Not set')}")
            st.write(f"Session State Docs: {st.session_state.get('selected_documents', [])}")
            st.write(f"Available LLMs: {available_llms}")
            st.write(f"Available RAG Variants: {rag_variants}")
            
            # Session state reset button
            if st.button("🔄 Reset Session State", key="reset_session"):
                # Clear problematic session state keys
                keys_to_clear = ['llm_selector', 'rag_selector', 'doc_selector', 'search_toggle']
                for key in keys_to_clear:
                    if key in st.session_state:
                        del st.session_state[key]
                st.success("✅ Session state reset!")
                st.rerun()
        
        st.markdown("---")
        st.subheader("💬 Conversation Memory")
        if st.button("🗑️ Clear Memory", key="clear_memory_sidebar"):
            st.session_state.conversation = []
            trigger_refresh()
            st.success("Memory cleared!")
        
        st.markdown("---")
        st.subheader("🛡️ Features")
        st.markdown("""
        - **Multi-modal** (Text + Images)
        - **Advanced RAG** variants
        - **Internet search** integration
        - **Enhanced guardrails** with document relevance
        - **Multi-file upload** support
        - **Conversation memory** (10 messages)
        - **Observability** with Opik
        """)
    
        # Manual refresh button
        if st.button("🔄 Refresh All Status", key="refresh_all"):
            st.session_state.last_config_update = 0
            st.session_state.last_document_update = 0
            trigger_refresh()
            st.rerun()

if __name__ == "__main__":
    main()
