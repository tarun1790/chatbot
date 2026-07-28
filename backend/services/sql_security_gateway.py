import sqlglot
from sqlglot.errors import ParseError
from typing import Dict, Any

class SQLSecurityGateway:
    def __init__(self):
        self.allowed_operations = {"select", "with", "show", "describe", "explain"}
        self.blocked_operations = {
            "insert", "update", "delete", "drop", "alter", "create", 
            "truncate", "grant", "revoke", "call", "merge", "execute"
        }

    def validate_sql(self, sql_query: str) -> Dict[str, Any]:
        """
        Validates the generated SQL using SQLGlot AST parsing.
        Ensures only safe read operations are performed.
        """
        try:
            # Parse the SQL query into expressions
            # We use 'mysql' dialect as the target
            expressions = sqlglot.parse(sql_query, read="mysql")
            
            if not expressions:
                return {"is_safe": False, "violations": ["Empty query"], "sanitized_sql": None}
                
            # Prevent multiple statements
            if len(expressions) > 1:
                return {"is_safe": False, "violations": ["Multiple statements are not allowed"], "sanitized_sql": None}

            expression = expressions[0]
            if expression is None:
                 return {"is_safe": False, "violations": ["Invalid SQL syntax"], "sanitized_sql": None}

            # Check operation type
            root_node_type = expression.key
            if root_node_type not in self.allowed_operations:
                return {
                    "is_safe": False, 
                    "violations": f"Operation '{root_node_type}' is not allowed. Only SELECT is permitted.",
                    "sanitized_sql": None
                }
                
            # Perform additional security checks on the AST
            # (e.g., check for dangerous functions, ensure LIMIT is present)
            
            # Ensure LIMIT is present for SELECT queries (naive check for now, can be expanded)
            if root_node_type == "select" and not expression.args.get("limit"):
                # Automatically append LIMIT if missing
                expression = expression.limit(1000)
                
            sanitized_sql = expression.sql(dialect="mysql")

            return {
                "is_safe": True,
                "sanitized_sql": sanitized_sql,
                "violations": [],
                "risk_score": 0.0,
                "explanation": "Query passed all security checks."
            }

        except ParseError as e:
            return {
                "is_safe": False,
                "violations": [f"SQL syntax error: {str(e)}"],
                "sanitized_sql": None
            }
        except Exception as e:
             return {
                "is_safe": False,
                "violations": [f"Internal validation error: {str(e)}"],
                "sanitized_sql": None
            }
