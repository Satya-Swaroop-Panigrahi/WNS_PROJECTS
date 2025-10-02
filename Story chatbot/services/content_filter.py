import re
import logging
from typing import List, Set
from config import Config

logger = logging.getLogger(__name__)

class ContentFilter:
    def __init__(self):
        # Sensitive content patterns
        self.sensitive_patterns = [
            r'\b(violence|violent|kill|murder|death|suicide|self-harm)\b',
            r'\b(hate|racist|discrimination|prejudice)\b',
            r'\b(terrorist|terrorism|bomb|weapon)\b',
            r'\b(illegal|drug|addiction|overdose)\b',
            r'\b(explicit|porn|sexual|nude)\b',
            r'\b(harmful|dangerous|toxic|poison)\b'
        ]
        
        # Religion-related bias patterns (to avoid)
        self.bias_patterns = [
            r'\b(religion is|god is|faith is)\s+(bad|evil|wrong|stupid)',
            r'\b(all\s+\w+\s+are)\s+(bad|evil|stupid|inferior)',
            r'\b(only\s+\w+\s+are)\s+(good|superior|better)',
            r'\b(\w+)\s+(people|race|religion)\s+(are|is)\s+(all|always)'
        ]
        
        # Compile patterns for efficiency
        self.sensitive_regex = [re.compile(pattern, re.IGNORECASE) for pattern in self.sensitive_patterns]
        self.bias_regex = [re.compile(pattern, re.IGNORECASE) for pattern in self.bias_patterns]
    
    def is_safe(self, content: str) -> bool:
        """Check if content is safe and doesn't violate guidelines"""
        if not content or not isinstance(content, str):
            return False
        
        content_lower = content.lower()
        
        # Check for sensitive content
        for regex in self.sensitive_regex:
            if regex.search(content):
                logger.warning(f"Sensitive content detected: {content[:100]}...")
                return False
        
        # Check for bias patterns
        for regex in self.bias_regex:
            if regex.search(content):
                logger.warning(f"Bias pattern detected: {content[:100]}...")
                return False
        
        # Check against sensitive keywords
        for keyword in Config.SENSITIVE_KEYWORDS:
            if keyword.lower() in content_lower:
                logger.warning(f"Sensitive keyword detected: {keyword}")
                return False
        
        return True
    
    def is_safe_search(self, query: str) -> bool:
        """Check if search query is safe"""
        if not query or not isinstance(query, str):
            return False
        
        # Additional search-specific filtering
        dangerous_searches = [
            'how to make bomb', 'how to kill', 'suicide methods',
            'illegal drugs', 'hate speech', 'terrorist attacks',
            'violence against', 'child abuse', 'animal cruelty'
        ]
        
        query_lower = query.lower()
        
        for dangerous in dangerous_searches:
            if dangerous in query_lower:
                logger.warning(f"Dangerous search query detected: {query}")
                return False
        
        return self.is_safe(query)
    
    def filter_content(self, content: str) -> str:
        """Filter and clean content"""
        if not self.is_safe(content):
            return "Content filtered for safety reasons."
        
        # Additional content cleaning if needed
        # Remove excessive whitespace
        content = re.sub(r'\s+', ' ', content.strip())
        
        return content
    
    def get_safety_report(self, content: str) -> dict:
        """Get detailed safety report for content"""
        issues = []
        
        for i, regex in enumerate(self.sensitive_regex):
            matches = regex.findall(content)
            if matches:
                issues.append({
                    "type": "sensitive_content",
                    "pattern": self.sensitive_patterns[i],
                    "matches": matches
                })
        
        for i, regex in enumerate(self.bias_regex):
            matches = regex.findall(content)
            if matches:
                issues.append({
                    "type": "bias_pattern",
                    "pattern": self.bias_patterns[i],
                    "matches": matches
                })
        
        return {
            "is_safe": len(issues) == 0,
            "issues": issues,
            "content_length": len(content)
        }
