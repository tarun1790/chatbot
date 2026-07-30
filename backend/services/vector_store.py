import math
import re
from typing import List, Dict, Any, Optional

def _tokenize(text: str) -> List[str]:
    """Helper tokenizer converting string to lowercase word tokens."""
    return re.findall(r'\w+', text.lower())

def _cosine_similarity(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
    """Computes cosine similarity between two term-frequency vector dictionaries."""
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    return float(numerator) / denominator

class VectorStoreService:
    """
    Lightweight in-memory vector store service utilizing Term-Frequency vectors
    and cosine similarity matching across separate metadata namespaces.
    """
    def __init__(self):
        # Dictionary structure: { namespace: [ { "id": str, "text": str, "metadata": dict, "vector": dict } ] }
        self.store: Dict[str, List[Dict[str, Any]]] = {
            "schema": [],
            "golden_sql": [],
            "entities": [],
            "business_terms": []
        }
        self._initialize_default_indexes()

    def add_documents(self, namespace: str, documents: List[Dict[str, Any]]) -> None:
        """Adds documents with automatic TF vector computation."""
        if namespace not in self.store:
            self.store[namespace] = []

        for doc in documents:
            tokens = _tokenize(doc["text"])
            tf: Dict[str, float] = {}
            for token in tokens:
                tf[token] = tf.get(token, 0.0) + 1.0
            
            # Normalize vector
            length = math.sqrt(sum(v * v for v in tf.values())) or 1.0
            norm_tf = {k: v / length for k, v in tf.items()}

            entry = {
                "id": doc.get("id", str(len(self.store[namespace]))),
                "text": doc["text"],
                "metadata": doc.get("metadata", {}),
                "vector": norm_tf
            }
            self.store[namespace].append(entry)

    def search(
        self,
        namespace: str,
        query: str,
        top_k: int = 5,
        min_score: float = 0.15
    ) -> List[Dict[str, Any]]:
        """Searches documents in a given namespace by cosine similarity."""
        if namespace not in self.store or not self.store[namespace]:
            return []

        query_tokens = _tokenize(query)
        tf: Dict[str, float] = {}
        for token in query_tokens:
            tf[token] = tf.get(token, 0.0) + 1.0
        
        length = math.sqrt(sum(v * v for v in tf.values())) or 1.0
        query_vector = {k: v / length for k, v in tf.items()}

        results = []
        for doc in self.store[namespace]:
            score = _cosine_similarity(query_vector, doc["vector"])
            if score >= min_score:
                item = dict(doc["metadata"])
                item["similarity_score"] = round(score, 2)
                item["text"] = doc["text"]
                results.append(item)

        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:top_k]

    def clear_namespace(self, namespace: str) -> None:
        self.store[namespace] = []

    def _initialize_default_indexes(self):
        """Populate initial domain documents for demo enterprise database."""
        # 1. Schema Docs
        schema_docs = [
            {
                "id": "customers_table",
                "text": "Table customers. Stores customer details, names, cities, emails, and account registration dates.",
                "metadata": {"table": "customers", "type": "table", "description": "Customer demographics and account data"}
            },
            {
                "id": "orders_table",
                "text": "Table orders. Stores sales transactions, order totals, amounts, status, and dates linked to customer_id.",
                "metadata": {"table": "orders", "type": "table", "description": "Sales transactions and order totals"}
            },
            {
                "id": "employees_table",
                "text": "Table employees. Internal staff records, employee names, departments, salary, and hire dates.",
                "metadata": {"table": "employees", "type": "table", "description": "Internal staff and employee information"}
            },
            {
                "id": "col_customers_city",
                "text": "Column customers.city. Customer location, city, state, or address region.",
                "metadata": {"table": "customers", "column": "city", "description": "Customer location/city"}
            },
            {
                "id": "col_orders_amount",
                "text": "Column orders.amount total order amount revenue revenue sales value.",
                "metadata": {"table": "orders", "column": "amount", "description": "Order sales revenue value"}
            }
        ]
        self.add_documents("schema", schema_docs)

        # 2. Golden SQL Examples
        golden_sql_docs = [
            {
                "id": "gsql_1",
                "text": "Show top revenue customers by total sales order amount",
                "metadata": {
                    "question": "Show top revenue customers",
                    "sql": "SELECT c.name, SUM(o.amount) AS total_revenue FROM customers c JOIN orders o ON c.id = o.customer_id GROUP BY c.name ORDER BY total_revenue DESC LIMIT 10;"
                }
            },
            {
                "id": "gsql_2",
                "text": "List employees in a specific city or department",
                "metadata": {
                    "question": "Which employees work in Hyderabad?",
                    "sql": "SELECT name, department, hire_date FROM employees WHERE city = 'Hyderabad' LIMIT 50;"
                }
            },
            {
                "id": "gsql_3",
                "text": "Show monthly sales total revenue trend orders",
                "metadata": {
                    "question": "Monthly sales trend",
                    "sql": "SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, SUM(amount) AS monthly_sales FROM orders GROUP BY month ORDER BY month ASC;"
                }
            }
        ]
        self.add_documents("golden_sql", golden_sql_docs)

        # 3. Entity Aliases
        entity_docs = [
            {
                "id": "ent_hyd",
                "text": "Hyd HYD Cyberabad Secunderabad Hyderabad customer employee location city",
                "metadata": {
                    "input": "Hyd",
                    "resolved_value": "Hyderabad",
                    "field": "customers.city",
                    "canonical_name": "Hyderabad"
                }
            },
            {
                "id": "ent_blr",
                "text": "Blr BLR Bengaluru Bangalore location city",
                "metadata": {
                    "input": "Blr",
                    "resolved_value": "Bangalore",
                    "field": "customers.city",
                    "canonical_name": "Bangalore"
                }
            }
        ]
        self.add_documents("entities", entity_docs)

        # 4. Business Terms
        term_docs = [
            {
                "id": "term_revenue",
                "text": "Revenue Total Sales Gross Amount Income Earnings",
                "metadata": {
                    "term": "Revenue",
                    "definition": "SUM(orders.amount) for completed transactions"
                }
            }
        ]
        self.add_documents("business_terms", term_docs)
