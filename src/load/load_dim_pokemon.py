from pathlib import Path
import sys
import duckdb

# Locate files relative to the project folder.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

conn = duckdb.connect(str(PROJECT_ROOT / "data/pokedex.duckdb"))

try:
    conn.execute("BEGIN TRANSACTION")

    # Recreate the table only when --setup is provided.
    if "--setup" in sys.argv:
        ddl_path = PROJECT_ROOT / "sql/ddl/create_dim_pokemon.sql"
        conn.execute(ddl_path.read_text())

    # Refresh the table's records.
    load_path = PROJECT_ROOT / "sql/loads/load_dim_pokemon.sql"
    conn.execute(load_path.read_text())

    # Check the loaded data before committing.
    counts = conn.execute("""
        SELECT
            Generation_ID
            ,COUNT(*) AS Pokemon_Count
        FROM model.DimPokemon
        GROUP BY Generation_ID
        ORDER BY Generation_ID
    """).fetchall()

    missing_matches = conn.execute("""
        SELECT COUNT(*)
        FROM model.DimPokemon
        WHERE Generation_ID IS NULL
    """).fetchone()[0]

    if missing_matches > 0:
        raise ValueError(f"{missing_matches} Pokémon have no generation match")

    conn.execute("COMMIT")

    print("Pokémon loaded by generation:", counts)
    print("Missing generation matches:", missing_matches)

except Exception:
    conn.execute("ROLLBACK")
    raise

finally:
    conn.close()