from typing import List, Dict, Any, Optional
from collections import deque
import json
import time
import logging
import hashlib

logger = logging.getLogger(__name__)

class ConversationMemory:
    def __init__(self, max_messages: int = 10):
        self.memories: Dict[str, deque] = {}
        self.max_messages = max_messages
        self.conversation_summaries: Dict[str, str] = {}
        self.context_embeddings: Dict[str, List[float]] = {}
        self.logger = logging.getLogger(__name__)
    
    def add_message(self, session_id: str, role: str, content: str, document_context: List[str] = None):
        """Add a message to conversation memory with enhanced context tracking"""
        if session_id not in self.memories:
            self.memories[session_id] = deque(maxlen=self.max_messages)
        
        # Create message with enhanced metadata
        message = {
            "role": role,
            "content": content,
            "timestamp": time.time(),
            "document_context": document_context if document_context else [],
            "message_id": self._generate_message_id(content, role),
            "context_hash": self._generate_context_hash(content, document_context)
        }
        
        self.memories[session_id].append(message)
        
        # Update conversation summary if we have enough messages
        if len(self.memories[session_id]) >= 3:
            self._update_conversation_summary(session_id)
        
        self.logger.info(f"Added {role} message to memory for session {session_id} (total: {len(self.memories[session_id])})")
    
    def get_conversation_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get conversation history for a session"""
        if session_id not in self.memories:
            return []
        return list(self.memories[session_id])
    
    def get_context_string(self, session_id: str, max_messages: int = 5) -> str:
        """Get enhanced conversation context as a string for LLM prompting"""
        history = self.get_conversation_history(session_id)
        context_parts = []
        
        # Add conversation summary if available
        if session_id in self.conversation_summaries:
            context_parts.append(f"CONVERSATION SUMMARY: {self.conversation_summaries[session_id]}")
            context_parts.append("")
        
        # Get last N messages for context with enhanced formatting
        recent_messages = history[-max_messages:]
        for i, msg in enumerate(recent_messages):
            role = "User" if msg["role"] == "user" else "Assistant"
            timestamp = time.strftime("%H:%M", time.localtime(msg["timestamp"]))
            
            # Enhanced message formatting
            message_text = f"[{timestamp}] {role}: {msg['content']}"
            context_parts.append(message_text)
            
            # Include document context if available
            if msg.get("document_context") and msg["document_context"]:
                doc_refs = [doc[:100] + "..." if len(doc) > 100 else doc for doc in msg["document_context"]]
                context_parts.append(f"  📄 Document References: {'; '.join(doc_refs)}")
            
            # Add message ID for tracking
            if msg.get("message_id"):
                context_parts.append(f"  ID: {msg['message_id']}")
        
        return "\n".join(context_parts)
    
    def clear_memory(self, session_id: str):
        """Clear memory for a specific session"""
        if session_id in self.memories:
            del self.memories[session_id]
            logger.info(f"Cleared memory for session {session_id}")
    
    def get_session_count(self, session_id: str) -> int:
        """Get number of messages in a session"""
        if session_id in self.memories:
            return len(self.memories[session_id])
        return 0
    
    def get_all_sessions(self) -> List[str]:
        """Get list of all active session IDs"""
        return list(self.memories.keys())
    
    def _generate_message_id(self, content: str, role: str) -> str:
        """Generate unique message ID"""
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        timestamp = str(int(time.time()))[-6:]
        return f"{role}_{timestamp}_{content_hash}"
    
    def _generate_context_hash(self, content: str, document_context: List[str]) -> str:
        """Generate hash for context tracking"""
        context_str = content + "|" + "|".join(document_context or [])
        return hashlib.md5(context_str.encode()).hexdigest()[:12]
    
    def _update_conversation_summary(self, session_id: str):
        """Update conversation summary based on recent messages"""
        if session_id not in self.memories:
            return
        
        messages = list(self.memories[session_id])
        if len(messages) < 3:
            return
        
        # Extract key topics and themes from recent messages
        topics = []
        for msg in messages[-5:]:  # Last 5 messages
            content = msg["content"].lower()
            if "question" in content or "?" in content:
                topics.append("questioning")
            if "help" in content or "assist" in content:
                topics.append("assistance")
            if "document" in content or "file" in content:
                topics.append("document_analysis")
            if "search" in content or "find" in content:
                topics.append("search")
        
        # Create summary
        unique_topics = list(set(topics))
        if unique_topics:
            self.conversation_summaries[session_id] = f"Recent conversation topics: {', '.join(unique_topics)}"
        else:
            self.conversation_summaries[session_id] = "General conversation in progress"
    
    def get_conversation_summary(self, session_id: str) -> str:
        """Get conversation summary for a session"""
        return self.conversation_summaries.get(session_id, "No summary available")
    
    def get_memory_stats(self, session_id: str) -> Dict[str, Any]:
        """Get memory statistics for a session"""
        if session_id not in self.memories:
            return {"message_count": 0, "has_summary": False, "context_hashes": []}
        
        messages = list(self.memories[session_id])
        context_hashes = [msg.get("context_hash", "") for msg in messages if msg.get("context_hash")]
        
        return {
            "message_count": len(messages),
            "has_summary": session_id in self.conversation_summaries,
            "context_hashes": context_hashes,
            "summary": self.conversation_summaries.get(session_id, ""),
            "last_message_time": messages[-1]["timestamp"] if messages else None
        }