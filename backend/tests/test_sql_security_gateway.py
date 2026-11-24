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
    assert isinstance(result["violations"], list)
    assert any("not allowed" in v for v in result["violations"])

def test_reject_insert():
    gateway = SQLSecurityGateway()
    result = gateway.validate_sql("INSERT INTO users (name) VALUES ('John')")
    assert result["is_safe"] is False
    assert isinstance(result["violations"], list)
    assert any("not allowed" in v for v in result["violations"])

def test_reject_multiple_statements():
    gateway = SQLSecurityGateway()
    result = gateway.validate_sql("SELECT * FROM users; DROP TABLE users;")
    assert result["is_safe"] is False
    assert isinstance(result["violations"], list)
    assert "Multiple statements" in result["violations"][0]

def test_allow_union_query():
    gateway = SQLSecurityGateway()
    result = gateway.validate_sql("SELECT id, name FROM users UNION SELECT id, name FROM archived_users")
    assert result["is_safe"] is True
    assert "LIMIT" in result["sanitized_sql"].upper()

def test_allow_cte_with_query():
    gateway = SQLSecurityGateway()
    result = gateway.validate_sql("WITH active_users AS (SELECT * FROM users WHERE active = 1) SELECT * FROM active_users")
    assert result["is_safe"] is True
    assert "LIMIT" in result["sanitized_sql"].upper()

def test_violations_consistently_list():
    gateway = SQLSecurityGateway()
    # Test empty query
    empty_res = gateway.validate_sql("")
    assert isinstance(empty_res["violations"], list)
    # Test invalid syntax
    syntax_res = gateway.validate_sql("SELECT * FROM")
    assert isinstance(syntax_res["violations"], list)
    # Test blocked operation
    blocked_res = gateway.validate_sql("DELETE FROM orders")
    assert isinstance(blocked_res["violations"], list)

