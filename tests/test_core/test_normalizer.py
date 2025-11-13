from query_watch.core.normalizer import normalize_sql, normalize_sql_advanced


def test_normalize_sql_empty_string():
    assert normalize_sql("") == ""
    assert normalize_sql("   ") == ""


def test_normalize_sql_string_literals():
    assert (
        normalize_sql("SELECT * FROM users WHERE name = 'John'")
        == "SELECT * FROM users WHERE name = ?"
    )
    assert (
        normalize_sql('SELECT * FROM users WHERE name = "John"')
        == "SELECT * FROM users WHERE name = ?"
    )
    assert (
        normalize_sql("SELECT * FROM users WHERE name = 'John''s'")
        == "SELECT * FROM users WHERE name = ?"
    )
    assert (
        normalize_sql(
            "SELECT * FROM users WHERE name = 'John' AND email = 'test@example.com'"
        )
        == "SELECT * FROM users WHERE name = ? AND email = ?"
    )


def test_normalize_sql_numeric_literals():
    assert (
        normalize_sql("SELECT * FROM users WHERE id = 123")
        == "SELECT * FROM users WHERE id = ?"
    )
    assert (
        normalize_sql("SELECT * FROM users WHERE id = 123.45")
        == "SELECT * FROM users WHERE id = ?"
    )
    assert (
        normalize_sql("SELECT * FROM users WHERE id = -123")
        == "SELECT * FROM users WHERE id = ?"
    )
    assert (
        normalize_sql("SELECT * FROM users WHERE id = 1e10")
        == "SELECT * FROM users WHERE id = ?"
    )
    assert (
        normalize_sql("SELECT * FROM users WHERE id = 123 AND age = 25")
        == "SELECT * FROM users WHERE id = ? AND age = ?"
    )


def test_normalize_sql_whitespace():
    assert normalize_sql("SELECT   *   FROM   users") == "SELECT * FROM users"
    assert normalize_sql("SELECT\t*\tFROM\tusers") == "SELECT * FROM users"
    assert normalize_sql("SELECT\n*\nFROM\nusers") == "SELECT * FROM users"
    assert (
        normalize_sql("SELECT  *  FROM  users  WHERE  id  =  123")
        == "SELECT * FROM users WHERE id = ?"
    )
    assert normalize_sql("  SELECT * FROM users  ") == "SELECT * FROM users"


def test_normalize_sql_complex_query():
    sql = """
        SELECT u.id, u.name, u.email
        FROM users u
        WHERE u.id = 123
        AND u.name = 'John'
        AND u.age > 18
        ORDER BY u.name
        LIMIT 10
    """
    expected = "SELECT u.id, u.name, u.email FROM users u WHERE u.id = ? AND u.name = ? AND u.age > ? ORDER BY u.name LIMIT ?"
    assert normalize_sql(sql) == expected


def test_normalize_sql_update_statement():
    assert (
        normalize_sql("UPDATE users SET name = 'John', age = 25 WHERE id = 123")
        == "UPDATE users SET name = ?, age = ? WHERE id = ?"
    )


def test_normalize_sql_delete_statement():
    assert (
        normalize_sql("DELETE FROM users WHERE id = 123")
        == "DELETE FROM users WHERE id = ?"
    )


def test_normalize_sql_insert_statement():
    assert (
        normalize_sql("INSERT INTO users (id, name) VALUES (123, 'John')")
        == "INSERT INTO users (id, name) VALUES (?, ?)"
    )


def test_normalize_sql_with_in_clause():
    sql = "SELECT * FROM users WHERE id IN (1, 2, 3)"
    normalized = normalize_sql(sql)
    assert "IN" in normalized
    assert normalized.count("?") == 3


def test_normalize_sql_no_literals():
    sql = "SELECT * FROM users WHERE active = true"
    assert normalize_sql(sql) == "SELECT * FROM users WHERE active = true"


def test_normalize_sql_special_characters():
    sql = "SELECT * FROM users WHERE name LIKE '%test%'"
    normalized = normalize_sql(sql)
    assert "LIKE" in normalized
    assert normalized.count("?") >= 1


def test_normalize_sql_advanced_in_clause():
    sql = "SELECT * FROM users WHERE id IN (1, 2, 3, 4, 5)"
    basic = normalize_sql(sql)
    assert basic.count("?") == 5

    advanced = normalize_sql_advanced(sql)
    assert "IN" in advanced
