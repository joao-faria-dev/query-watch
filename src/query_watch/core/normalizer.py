import re


def normalize_sql(sql: str) -> str:
    if not sql:
        return ""

    # replace string literals
    sql = re.sub(r"'([^'']|'')*'", "?", sql)
    sql = re.sub(r'"([^"]|"")*"', "?", sql)

    # replace numerals
    sql = re.sub(r"-?\d+\.?\d*(?:[eE][+-]?\d+)?", "?", sql)

    # normalize whitespace
    sql = re.sub(r"\s+", " ", sql)

    # trim whitespace
    sql = sql.strip()

    return sql


def normalize_sql_advanced(sql: str) -> str:
    if not sql:
        return ""

    sql = normalize_sql(sql)

    # normalize IN queries
    sql = re.sub(r"IN\s*\(\s*\?(\s*,\s*\?)+\s*\)", "IN (?)", sql, flags=re.IGNORECASE)

    return sql
