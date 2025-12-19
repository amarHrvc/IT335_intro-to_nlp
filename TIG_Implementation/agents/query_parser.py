"""
Query Parser Agent
Extracts structured information from natural language travel queries
"""

import spacy
from typing import Dict, List, Optional, Tuple, Any
import re
import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QueryParser:
    """
    Two-stage query parser:
    Stage 1: Extract entities with spaCy (fast)
    Stage 2: Structure with LLM (smart)
    """
    
    def __init__(self, use_llm: bool = True, model_name: str = os.getenv("OPENAI_MODEL") or "gpt-3.5-turbo"):
        """
        Initialize spaCy model and optional LLM

        Args:
            use_llm: Whether to use LLM for structuring
            model_name: OpenAI model to use
        """
        logger.info("Loading spaCy model...")
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.info("Downloading en_core_web_sm...")
            from spacy.cli import download
            download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
            
        self.use_llm = use_llm
        self.model_name = model_name
        self.llm_client = None
        
        if use_llm:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                self.llm_client = OpenAI(api_key=api_key)
                logger.info("✓ LLM enabled")
            else:
                logger.warning("⚠ No API key found, falling back to rule-based only")
                self.use_llm = False
        
        logger.info("✓ Query Parser ready")

    def parse(self, query: str) -> Dict[str, Any]:
        """
        Main parsing function
        
        Args:
            query: Natural language query
            
        Returns:
            Structured query dictionary
        """
        logger.info(f"Parsing query: {query}")

        # Stage 1: Extract entities
        entities = self._extract_entities(query)
        
        # Stage 2: Structure
        structured = self._structure_query(query, entities)
        
        return structured
    
    def _extract_entities(self, query: str) -> Dict[str, List[str]]:
        """
        Stage 1: Extract entities using spaCy
        
        We look for:
        - GPE: Cities, countries (destination/origin)
        - DATE: Dates and durations
        - MONEY: Budget amounts
        - CARDINAL: Numbers (days, people)
        """
        doc = self.nlp(query)
        
        entities = {
            'cities': [],
            'dates': [],
            'money': [],
            'numbers': [],
            'raw_text': [query] # Keep as list for consistency or just str? Original was str but dict type hint says List[str] usually.
                                # Actually original code had 'raw_text': query. Let's keep it simple but fix type hint if needed.
                                # The return type hint says Dict[str, List[str]], but raw_text is str.
                                # Let's adjust return type hint to Dict[str, Any] to be safe.
        }
        entities['raw_text'] = query # Restore original behavior

        # Extract named entities
        for ent in doc.ents:
            if ent.label_ == 'GPE':  # Geopolitical entity (cities)
                entities['cities'].append(ent.text)
            elif ent.label_ == 'DATE':
                entities['dates'].append(ent.text)
            elif ent.label_ == 'MONEY':
                entities['money'].append(ent.text)
            elif ent.label_ == 'CARDINAL':  # Numbers
                entities['numbers'].append(ent.text)
        
        logger.debug(f"[Stage 1] Entities extracted: {entities}")
        return entities
    
    def _structure_query(self, query: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        """
        Stage 2: Structure with LLM (if available) or rules
        """
        if self.use_llm and self.llm_client:
            return self._structure_with_llm(query, entities)
        else:
            return self._structure_with_rules(query, entities)
    
    def _structure_with_rules(self, query: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        """
        Stage 2: Structure entities into query format (Rule-based)
        """
        structured = {
            'origin': None,
            'destination': None,
            'duration': None,
            'budget': None,
            'people_number': 1,  # Default
            'interests': [],
            'constraints': {}
        }
        
        # Destination (assume last city mentioned)
        if entities['cities']:
            structured['destination'] = entities['cities'][-1]
            if len(entities['cities']) > 1:
                structured['origin'] = entities['cities'][0]
        
        # Duration (look for "X day" or "X-day")
        duration_match = re.search(r'(\d+)[\s-]day', query.lower())
        if duration_match:
            structured['duration'] = int(duration_match.group(1))
        elif entities['numbers']:
            # Try to find a number that looks like duration if not found by regex
            # This is a naive fallback
            try:
                structured['duration'] = int(entities['numbers'][0])
            except ValueError:
                pass
        
        # Budget (extract number from money)
        # IMPROVED REGEX: Require currency symbol or keyword
        if entities['money']:
            money_str = entities['money'][0]
            # Extract just the number
            budget_match = re.search(r'[\$€£]?([\d,]+)', money_str)
            if budget_match:
                budget_num = budget_match.group(1).replace(',', '')
                try:
                    structured['budget'] = int(budget_num)
                except ValueError:
                    pass
        else:
            # Fallback: Look for "budget X" or "X euros" patterns in text if spaCy missed it
            # Stricter regex to avoid matching years
            budget_pattern = r'(?:budget|cost|spend)[\s\w]*?[\$€£]?\s*([\d,]+)|([\d,]+)\s*(?:euros?|dollars?|usd|eur)'
            budget_match = re.search(budget_pattern, query.lower())
            if budget_match:
                # Group 1 is from "budget X", Group 2 is from "X euros"
                val = budget_match.group(1) or budget_match.group(2)
                if val:
                    try:
                        structured['budget'] = int(val.replace(',', ''))
                    except ValueError:
                        pass


        people_patterns = [
            r'for\s+(\d+)\s+(?:people|persons|travelers|guests)',
            r'(\d+)\s+(?:people|persons|travelers|guests)',
            r'group\s+of\s+(\d+)',
            r'party\s+of\s+(\d+)'
        ]

        for pattern in people_patterns:
            people_match = re.search(pattern, query.lower())
            if people_match:
                try:
                    structured['people_number'] = int(people_match.group(1))
                    break
                except ValueError:
                    pass

        # Interests (simple keyword matching)
        interest_keywords = [
            'sightseeing', 'culture', 'food', 'museums', 
            'beach', 'hiking', 'shopping', 'nightlife'
        ]
        query_lower = query.lower()
        structured['interests'] = [
            interest for interest in interest_keywords 
            if interest in query_lower
        ]
        
        logger.info(f"[Stage 2] Structured query (Rule-based): {structured}")
        return structured

    def _structure_with_llm(self, query: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        """
        LLM-based structuring - smarter!
        
        Uses GPT to understand context and fill gaps
        """
        logger.info("[Stage 2] Using LLM for structuring...")

        prompt = f"""Extract travel query details from this request:

Query: "{query}"

Extracted entities:
- Cities: {entities['cities']}
- Dates: {entities['dates']}
- Money: {entities['money']}
- Numbers: {entities['numbers']}

Output JSON with these fields:
{{
    "origin": "departure city or null",
    "destination": "destination city (required)",
    "duration": "trip length in days (required)",
    "budget": "budget as integer or null",
    "people_number": "number of travelers (default 1)",
    "interests": ["list", "of", "interests"],
    "constraints": {{"key": "value"}}
}}

Rules:
- If multiple cities mentioned, first is origin, last is destination
- Duration can be from "X day" or "X-day" pattern
- Interests are activities mentioned (sightseeing, food, culture, etc.)
- Return ONLY valid JSON, no explanation
"""
        
        try:
            response = self.llm_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a travel query parser. Output only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Low temp for consistent output
                max_tokens=300
            )
            
            result_text = response.choices[0].message.content
            print(f"LLM response: {result_text}")
            logger.debug(f"LLM response: {result_text}")

            # Parse JSON
            import json
            structured = json.loads(result_text)
            
            print("\n[Stage 2] LLM structured query:")
            for key, value in structured.items():
                print(f"  {key}: {value}")
            logger.info(f"[Stage 2] LLM structured query: {structured}")

            return structured
            
        except Exception as e:
            print(f"⚠ LLM structuring failed: {e}")
            print("Falling back to rule-based...")
            logger.error(f"⚠ LLM structuring failed: {e}")
            logger.info("Falling back to rule-based...")
            return self._structure_with_rules(query, entities)
    
    def validate_query(self, structured: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Check if we have minimum required information
        
        Returns:
            (is_valid, missing_fields)
        """
        required = ['destination', 'duration']
        missing = [
            field for field in required 
            if not structured.get(field)
        ]
        
        is_valid = len(missing) == 0
        return is_valid, missing
