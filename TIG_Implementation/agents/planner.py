"""
Itinerary Planner Agent

Generates travel itineraries using LLM providers (OpenAI or Claude).
Uses few-shot prompting with similar examples from the dataset.
"""

import os
from dotenv import load_dotenv
from typing import Dict, List, Optional
import json
from agents.llm_provider import get_llm_provider, BaseLLMProvider

# Load environment variables
load_dotenv()


class ItineraryPlanner:
    """
    Itinerary Planner using configurable LLM providers.

    Supports OpenAI GPT and Anthropic Claude models.
    """

    def __init__(
        self,
        dataset,
        llm_provider: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        debug: bool = False
    ):
        """
        Initialize the planner with a dataset and LLM provider.

        Args:
            dataset: TravelDataSet instance for retrieving similar examples
            llm_provider: Provider name ('openai' or 'claude').
                         If None, reads from LLM_PROVIDER env var (default: 'openai')
            api_key: API key for the provider (optional, reads from env if not provided)
            model: Model name to use (optional, uses provider default if not provided)
        """
        self.dataset = dataset
        self.debug = debug

        # Initialize LLM provider
        try:
            self.llm_client = get_llm_provider(
                provider_name=llm_provider,
                api_key=api_key,
                model=model
            )
            provider_name = llm_provider or os.getenv("LLM_PROVIDER", "openai")
            print(f"✓ Itinerary Planner initialized with {provider_name} provider")
        except Exception as e:
            print(f"⚠ Warning: Could not initialize LLM provider: {e}")
            print("  Planner will not be able to generate itineraries")
            self.llm_client = None

    def generate_itinerary(self, query: Dict, k: int = 3, debug: bool = None) -> Dict:
        """
        Generate an itinerary based on the user query.

        Args:
            query (Dict): User query containing destination, duration, budget, etc.
            k (int): Number of similar examples to retrieve from the dataset.

        Returns:
            Dict: Generated itinerary plan.
        """

        # Use instance debug setting if not overridden
        if debug is None:
            debug = self.debug

        if not self.llm_client:
            return {
                "error": "LLM provider not initialized",
                "itinerary": "Unable to generate itinerary without LLM provider"
            }


        print(f"\n{'='*60}")
        print("GENERATING ITINERARY")
        print(f"{'='*60}")

        # Retrieve similar examples from the dataset
        examples = self.dataset.find_similar_queries(query, k=k)

        # Generate itinerary using LLM
        itinerary = self._generate_with_llm(query, examples, debug=debug)

        # TODO: ground to dataset (validate against real hotels, restaurants, etc.)

        return itinerary
    
    def _generate_with_llm(self, query: Dict, examples: List[Dict], debug: bool = False) -> Dict:
        """
        Generate itinerary using few-shot prompting.

        Args:
            query (Dict): User query.
            examples (List[Dict]): Similar examples from the dataset.

        Returns:
            Dict: Generated itinerary plan.
        """
        # Construct the prompt with few-shot examples
        # Construct the prompt with few-shot examples
        prompt = self._build_prompt(query, examples)

        if not debug:
            print("\n[LLM Prompt Preview]")
            print(prompt[:500] + "..." if len(prompt) > 500 else prompt)

        # Prepare messages for LLM
        messages = [
            {
                "role": "system",
                "content": "You are a helpful travel planning assistant. Generate detailed day-by-day itineraries. Return ONLY valid JSON, no markdown formatting, no code blocks, no ```json wrapper."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        try:
            if debug:
                # Use debug mode - capture raw response
                response = self.llm_client.generate_with_debug(
                    messages=messages,
                    max_tokens=1500,
                    temperature=0.7
                )

                itinerary_text = response['content']
                raw_response = response['raw_content']

                return {
                    "itinerary": itinerary_text,
                    "parsed_query": query,
                    "debug_info": {
                        "prompt": prompt,
                        "raw_response": raw_response,
                        "processed_response": itinerary_text,
                        "messages": messages
                    }
                }
            else:
                # Normal mode - just get content
                itinerary_text = self.llm_client.generate(
                    messages=messages,
                    max_tokens=1500,
                    temperature=0.7
                )

                print("\n[Generated Itinerary]")
                print(itinerary_text[:300] + "..." if len(itinerary_text) > 300 else itinerary_text)

                return {"itinerary": itinerary_text}

        except Exception as e:
            print(f"\n⚠ Error generating itinerary: {e}")
            result = {
                "error": str(e),
                "itinerary": "Failed to generate itinerary"
            }
            if debug:
                result["debug_info"] = {
                    "prompt": prompt,
                    "error": str(e)
                }
            return result

    def _build_prompt(self, query: Dict, examples: List[Dict]) -> str:
        """
        Build few-shot prompt with examples.

        Args:
            query: User query dictionary
            examples: List of similar example itineraries

        Returns:
            Formatted prompt string
        """
        prompt = "You are an expert travel planner. Based on the following examples, create a detailed itinerary for the given query.\n\n"

        # Add few-shot examples
        if examples:
            prompt += "EXAMPLES:\n"
            prompt += "="*50 + "\n\n"

            for i, ex in enumerate(examples, 1):
                prompt += f"Example {i}:\n"
                prompt += f"Query: {json.dumps(ex.get('query', 'N/A'))}\n"
                prompt += f"Destination: {ex.get('destination', 'N/A')}\n"
                prompt += f"Duration: {ex.get('duration', 'N/A')} days\n"

                # Include plan if available
                if ex.get('plan'):
                    plan_str = json.dumps(ex['plan']) if isinstance(ex['plan'], dict) else str(ex['plan'])
                    prompt += f"Plan: {plan_str[:200]}...\n"  # Truncate long plans

                prompt += "\n"

        # Add the new query
        prompt += "="*50 + "\n"
        prompt += "NEW QUERY:\n"
        prompt += f"Destination: {query.get('destination', 'N/A')}\n"
        prompt += f"Duration: {query.get('duration', 'N/A')} days\n"
        prompt += f"Budget: ${query.get('budget', 'N/A')}\n"
        prompt += f"People: {query.get('people_number', 1)}\n"

        if query.get('interests'):
            prompt += f"Interests: {', '.join(query['interests'])}\n"

        prompt += "\n"
        prompt += "="*50 + "\n"
        prompt += "IMPORTANT REQUIREMENTS:\n"
        prompt += f"1. MUST explicitly mention '{query.get('destination', 'N/A')}' in at least one activity description\n"
        prompt += "2. Return ONLY valid JSON (no markdown, no code blocks, no ```json wrapper)\n"
        prompt += "3. Follow this EXACT format:\n\n"
        prompt += "{\n"
        prompt += '  "Day 1": {\n'
        prompt += '    "Morning": {"time": "09:00", "activity": "...", "cost": "$X"},\n'
        prompt += '    "Lunch": {"time": "12:00", "restaurant": "...", "cost": "$X"},\n'
        prompt += '    "Afternoon": {"time": "14:00", "activity": "...", "cost": "$X"},\n'
        prompt += '    "Dinner": {"time": "19:00", "restaurant": "...", "cost": "$X"},\n'
        prompt += '    "Accommodation": "Hotel Name ($X/night)"\n'
        prompt += '  },\n'
        prompt += '  "Day 2": {...},\n'
        prompt += '  ...\n'
        prompt += '  "Total Cost": "$XXXX"\n'
        prompt += "}\n"
        prompt += "\nProvide a detailed day-by-day itinerary with activities, meals, and accommodations."

        return prompt