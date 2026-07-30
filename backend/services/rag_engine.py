from typing import Dict, Any, List
from backend.services.vector_store import VectorStoreService

class RAGEngine:
    """
    Orchestrates Retrieval-Augmented Generation (RAG) across schema,
    golden SQL few-shot examples, and entity resolution namespaces.
    """
    def __init__(self, vector_store: VectorStoreService):
        self.vector_store = vector_store

    def retrieve_relevant_schema_context(self, user_query: str) -> List[Dict[str, Any]]:
        """Retrieves semantically matching schema tables and columns."""
        return self.vector_store.search(namespace="schema", query=user_query, top_k=4, min_score=0.1)

    def retrieve_few_shot_examples(self, user_query: str) -> List[Dict[str, Any]]:
        """Retrieves top similar verified Golden SQL examples."""
        return self.vector_store.search(namespace="golden_sql", query=user_query, top_k=2, min_score=0.1)

    def resolve_entity_values(self, user_query: str) -> List[Dict[str, Any]]:
        """Resolves abbreviations, aliases, and categorical entity values."""
        return self.vector_store.search(namespace="entities", query=user_query, top_k=2, min_score=0.1)

    def retrieve_business_terms(self, user_query: str) -> List[Dict[str, Any]]:
        """Retrieves business metric definitions."""
        return self.vector_store.search(namespace="business_terms", query=user_query, top_k=2, min_score=0.1)

    def build_augmented_context(self, user_query: str) -> Dict[str, Any]:
        """
        Builds a comprehensive augmented context payload for LLM prompt construction
        and UI transparency panel streaming.
        """
        schema_matches = self.retrieve_relevant_schema_context(user_query)
        golden_sql_matches = self.retrieve_few_shot_examples(user_query)
        entity_matches = self.resolve_entity_values(user_query)
        business_terms = self.retrieve_business_terms(user_query)

        return {
            "query": user_query,
            "schema_context": schema_matches,
            "golden_sql_examples": golden_sql_matches,
            "resolved_entities": entity_matches,
            "business_terms": business_terms,
            "rag_summary": {
                "tables_found": list(set([m.get("table") for m in schema_matches if m.get("table")])),
                "golden_examples_count": len(golden_sql_matches),
                "entities_resolved": len(entity_matches)
            }
        }
