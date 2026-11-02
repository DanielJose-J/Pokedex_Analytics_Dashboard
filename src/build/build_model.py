from pathlib import Path
import sys
import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SETUP = "--setup" in sys.argv

TABLES = [
    "dim_generation",
    "dim_pokemon",
    "dim_type",
    "bridge_pokemon_type",
]

conn = duckdb.connect(str(PROJECT_ROOT / "data/pokedex.duckdb"))

try:
    conn.execute("BEGIN TRANSACTION")

    # Create or recreate tables only during setup.
    if SETUP:
        for table in TABLES:
            path = PROJECT_ROOT / "sql/ddl" / f"create_{table}.sql"
            conn.execute(path.read_text())

    # Load generation first, then Pokémon.
    for table in TABLES:
        path = PROJECT_ROOT / "sql/loads" / f"load_{table}.sql"
        conn.execute(path.read_text())

    # Ensure every Pokémon references an existing generation.
    missing_matches = conn.execute("""
        SELECT COUNT(*)
        FROM model.DimPokemon AS p
        LEFT JOIN model.DimGeneration AS g
            ON p.Generation_ID = g.Generation_ID
        WHERE g.Generation_ID IS NULL
    """).fetchone()[0]

    if missing_matches > 0:
        raise ValueError(
            f"{missing_matches} Pokémon have no matching generation"
        )

    counts = conn.execute("""
        SELECT
            Generation_ID
            ,COUNT(*) AS Pokemon_Count
        FROM model.DimPokemon
        GROUP BY Generation_ID
        ORDER BY Generation_ID
    """).fetchall()

    conn.execute("COMMIT")

    print("Pokémon loaded by generation:", counts)
    print("Missing generation matches:", missing_matches)

except Exception:
    conn.execute("ROLLBACK")
    raise

finally:
    conn.close()