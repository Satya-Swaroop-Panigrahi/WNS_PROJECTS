from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from typing import Dict, Any, List
import re
import logging
import torch

class EnhancedGuardrailsService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize toxicity classifier with better model
        try:
            self.toxicity_classifier = pipeline(
                "text-classification",
                model="unitary/toxic-bert",
                tokenizer="unitary/toxic-bert",
                device=0 if torch.cuda.is_available() else -1
            )
            self.logger.info("Toxicity classifier initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize toxicity classifier: {e}")
            self.toxicity_classifier = None
        
        # Initialize NSFW content detector
        try:
            self.nsfw_classifier = pipeline(
                "text-classification",
                model="microsoft/DialoGPT-medium",
                device=0 if torch.cuda.is_available() else -1
            )
            self.logger.info("NSFW classifier initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize NSFW classifier: {e}")
            self.nsfw_classifier = None
        
        # Document type patterns for relevance checking
        self.document_categories = {
            "medical": [
                'medical', 'health', 'patient', 'diagnosis', 'treatment', 
                'prescription', 'symptoms', 'doctor', 'hospital', 'clinical',
                'medicine', 'healthcare', 'report', 'test results'
            ],
            "legal": [
                'legal', 'law', 'contract', 'agreement', 'lawsuit', 'court',
                'attorney', 'legal document', 'clause', 'jurisdiction'
            ],
            "financial": [
                'financial', 'bank', 'loan', 'investment', 'tax', 'revenue',
                'profit', 'loss', 'balance sheet', 'income statement'
            ],
            "technical": [
                'technical', 'code', 'programming', 'software', 'hardware',
                'system', 'network', 'database', 'algorithm'
            ]
        }
    
    def check_toxicity(self, text: str) -> Dict[str, Any]:
        """Check if text contains toxic content with enhanced detection"""
        if not self.toxicity_classifier:
            return {"is_toxic": False, "score": 0.0, "safe": True}
        
        try:
            # Truncate text to avoid token limits
            text_to_check = text[:512]
            results = self.toxicity_classifier(text_to_check)
            
            # Extract toxic labels and their scores
            toxic_labels = ['toxic', 'obscene', 'insult', 'threat', 'identity_hate']
            toxic_score = 0.0
            
            for result in results:
                if result['label'] in toxic_labels:
                    toxic_score = max(toxic_score, result['score'])
            
            # Enhanced threshold for better detection
            is_toxic = toxic_score > 0.6
            
            self.logger.info(f"Toxicity check - Score: {toxic_score:.3f}, Toxic: {is_toxic}")
            
            return {
                "is_toxic": is_toxic,
                "score": toxic_score,
                "safe": not is_toxic,
                "details": results
            }
        except Exception as e:
            self.logger.error(f"Toxicity check failed: {e}")
            return {"is_toxic": False, "score": 0.0, "safe": True}
    
    def check_nsfw_request(self, text: str, images: List[str] = None) -> Dict[str, Any]:
        """Enhanced NSFW content detection"""
        # Extended NSFW keywords list
        nsfw_keywords = [
            'porn', 'nude', 'sexual', 'explicit', 'adult content',
            'nsfw', 'not safe for work', 'erotic', 'xxx', 'pornography',
            'naked', 'nude', 'sex', 'porn', 'adult', 'mature content',
            'inappropriate', 'lewd', 'vulgar', 'obscene'
        ]
        
        text_lower = text.lower()
        detected_keywords = []
        
        for keyword in nsfw_keywords:
            if keyword in text_lower:
                detected_keywords.append(keyword)
        
        # Use ML model for additional NSFW detection if available
        ml_nsfw_score = 0.0
        if self.nsfw_classifier and detected_keywords:
            try:
                results = self.nsfw_classifier(text[:256])
                ml_nsfw_score = max([result['score'] for result in results if 'nsfw' in result['label'].lower()])
            except Exception as e:
                self.logger.warning(f"ML NSFW detection failed: {e}")
        
        is_nsfw = len(detected_keywords) > 0 or ml_nsfw_score > 0.7
        
        self.logger.info(f"NSFW check - Keywords: {detected_keywords}, ML Score: {ml_nsfw_score:.3f}, NSFW: {is_nsfw}")
        
        return {
            "is_nsfw": is_nsfw,
            "detected_keywords": detected_keywords,
            "ml_score": ml_nsfw_score,
            "safe": not is_nsfw
        }
    
    def check_document_relevance(self, user_question: str, document_context: List[str]) -> Dict[str, Any]:
        """Check if user question is relevant to uploaded documents"""
        try:
            if not document_context:
                return {
                    "is_relevant": True, 
                    "reason": "No documents uploaded",
                    "document_topics": [],
                    "question_topics": []
                }
            
            # Extract document topics
            document_topics = self._extract_document_topics(document_context)
            question_topics = self._extract_question_topics(user_question)
            
            # Check relevance
            is_relevant = self._check_topic_relevance(question_topics, document_topics)
            
            return {
                "is_relevant": is_relevant,
                "document_topics": document_topics,
                "question_topics": question_topics,
                "reason": "Question is outside document scope" if not is_relevant else "Question is relevant to documents"
            }
        except Exception as e:
            self.logger.error(f"Error in document relevance check: {e}")
            return {
                "is_relevant": True,
                "document_topics": [],
                "question_topics": [],
                "reason": "Error in relevance check, allowing question"
            }
    
    def _extract_document_topics(self, document_context: List[str]) -> List[str]:
        """Extract main topics from document context"""
        topics = []
        full_text = " ".join(document_context).lower()
        
        for category, keywords in self.document_categories.items():
            for keyword in keywords:
                if keyword in full_text:
                    topics.append(category)
                    break  # Add category only once
        
        return list(set(topics))
    
    def _extract_question_topics(self, question: str) -> List[str]:
        """Extract topics from user question"""
        topics = []
        question_lower = question.lower()
        
        for category, keywords in self.document_categories.items():
            for keyword in keywords:
                if keyword in question_lower:
                    topics.append(category)
                    break
        
        return topics
    
    def _check_topic_relevance(self, question_topics: List[str], document_topics: List[str]) -> bool:
        """Check if question topics are relevant to document topics"""
        if not document_topics:  # No specific topics detected in documents
            return True
        
        if not question_topics:  # No specific topics in question
            return True
        
        # Check if any question topic matches document topics
        return any(topic in document_topics for topic in question_topics)
    
    def validate_request(self, message: str, images: List[str] = None, document_context: List[str] = None) -> Dict[str, Any]:
        """Enhanced validation with comprehensive safety checks"""
        self.logger.info(f"Validating request: {message[:50]}...")
        
        # Basic safety checks
        toxicity_check = self.check_toxicity(message)
        nsfw_check = self.check_nsfw_request(message, images)
        
        # Document relevance check
        relevance_check = self.check_document_relevance(message, document_context or [])
        
        # Determine overall safety
        is_safe = (
            toxicity_check["safe"] and 
            nsfw_check["safe"] and 
            relevance_check["is_relevant"]
        )
        
        # Generate detailed rejection reason
        rejection_reason = None
        if not is_safe:
            reasons = []
            if not toxicity_check["safe"]:
                reasons.append(f"Toxic content detected (score: {toxicity_check['score']:.3f})")
            if not nsfw_check["safe"]:
                reasons.append(f"NSFW content detected (keywords: {', '.join(nsfw_check['detected_keywords'])})")
            if not relevance_check["is_relevant"]:
                reasons.append(f"Question not relevant to documents (topics: {', '.join(relevance_check['document_topics'])})")
            
            rejection_reason = "; ".join(reasons)
        
        self.logger.info(f"Validation result - Safe: {is_safe}, Reason: {rejection_reason}")
        
        return {
            "safe": is_safe,
            "toxicity_score": toxicity_check["score"],
            "is_nsfw": nsfw_check["is_nsfw"],
            "nsfw_keywords": nsfw_check["detected_keywords"],
            "is_relevant": relevance_check["is_relevant"],
            "document_topics": relevance_check["document_topics"],
            "question_topics": relevance_check["question_topics"],
            "rejection_reason": rejection_reason,
            "validation_details": {
                "toxicity": toxicity_check,
                "nsfw": nsfw_check,
                "relevance": relevance_check
            }
        }