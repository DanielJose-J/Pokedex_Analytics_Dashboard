import duckdb

conn = duckdb.connect("data/pokedex.duckdb", read_only=True)

for table in ["raw.pokemon", "raw.species"]:
    print(f"\n{table}")

    columns = conn.execute(f"DESCRIBE {table}").fetchall()

    for column in columns:
        print(column[0], "→", column[1])

conn.close()