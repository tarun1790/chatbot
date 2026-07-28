import pytest
from backend.services.sql_security_gateway import SQLSecurityGateway

def test_safe_select_query():
    gateway = SQLSecurityGateway()
    result = gateway.validate_sql("SELECT * FROM users WHERE age > 18")
    assert result["is_safe"] is True
    # The gateway automatically appends LIMIT if missing
    assert "LIMIT" in result["sanitized_sql"].upper()

def test_reject_drop_table():
    gateway = SQLSecurityGateway()
    result = gateway.validate_sql("DROP TABLE users")
    assert result["is_safe"] is False
    assert "not allowed" in result["violations"]

def test_reject_insert():
    gateway = SQLSecurityGateway()
    result = gateway.validate_sql("INSERT INTO users (name) VALUES ('John')")
    assert result["is_safe"] is False
    assert "not allowed" in result["violations"]

def test_reject_multiple_statements():
    gateway = SQLSecurityGateway()
    result = gateway.validate_sql("SELECT * FROM users; DROP TABLE users;")
    assert result["is_safe"] is False
    assert "Multiple statements" in result["violations"][0]
