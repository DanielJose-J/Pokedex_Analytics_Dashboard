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

    print("\n--- Sample Pokémon type assignments ---")

    conn.sql("""
        SELECT
            p.Pokemon_ID
            ,p.Pokemon_Name
            ,t.Type_Name
            ,b.Type_Slot
        FROM model.BridgePokemonType AS b
        LEFT JOIN model.DimPokemon AS p
            ON b.Pokemon_ID = p.Pokemon_ID
        LEFT JOIN model.DimType AS t
            ON b.Type_ID = t.Type_ID
        WHERE b.Pokemon_ID IN (1, 4, 7)
        ORDER BY b.Pokemon_ID, b.Type_Slot
    """).show()

    print("\n--- Bridge records with missing dimension matches ---")

    conn.sql("""
        SELECT COUNT(*) AS Missing_Matches
        FROM model.BridgePokemonType AS b
        LEFT JOIN model.DimPokemon AS p
            ON b.Pokemon_ID = p.Pokemon_ID
        LEFT JOIN model.DimType AS t
            ON b.Type_ID = t.Type_ID
        WHERE p.Pokemon_ID IS NULL
            OR t.Type_ID IS NULL
    """).show()

finally:
    conn.close()