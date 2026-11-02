from pathlib import Path
import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[2]

conn = duckdb.connect(
    str(PROJECT_ROOT / "data/pokedex.duckdb"),
    read_only=True
)

try:
    print("\n--- DimGeneration ---")
    conn.sql("""
        SELECT *
        FROM model.DimGeneration
        ORDER BY Generation_ID
        LIMIT 5
    """).show()

    print("\n--- DimPokemon ---")
    conn.sql("""
        SELECT
            Pokemon_ID
            ,Pokemon_Name
            ,Generation_ID
            ,Is_Legendary
            ,HP
            ,Attack
            ,Defense
            ,Special_Attack
            ,Special_Defense
            ,Speed
            ,Base_Stat_Total
        FROM model.DimPokemon
        ORDER BY Pokemon_ID
        LIMIT 5
    """).show()

    print("\n--- DimType ---")
    conn.sql("""
        SELECT *
        FROM model.DimType
        ORDER BY Type_ID
        LIMIT 5
    """).show()

finally:
    conn.close()