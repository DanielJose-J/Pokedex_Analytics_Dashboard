import duckdb

conn = duckdb.connect("data/pokedex.duckdb", read_only=True)

try:
    result = conn.execute("""
        SELECT stats
        FROM raw.pokemon
        WHERE id = 1
    """).fetchone()

    for stat in result[0]:
        print(stat["stat"]["name"], "→", stat["base_stat"])

finally:
    conn.close()




