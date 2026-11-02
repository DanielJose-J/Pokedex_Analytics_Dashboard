from pathlib import Path
import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[2]

conn = duckdb.connect(
    str(PROJECT_ROOT / "data/pokedex.duckdb"),
    read_only=True
)

try:
    # Check one familiar Pokémon.
    bulbasaur = conn.execute("""
        SELECT
            Pokemon_Name
            ,HP
            ,Attack
            ,Defense
            ,Special_Attack
            ,Special_Defense
            ,Speed
            ,Base_Stat_Total
        FROM model.DimPokemon
        WHERE Pokemon_ID = 1
    """).fetchone()

    print("Bulbasaur:", bulbasaur)

    # Check every Pokémon for missing or inconsistent stats.
    issues = conn.execute("""
        SELECT COUNT(*)
        FROM model.DimPokemon
        WHERE HP IS NULL
            OR Attack IS NULL
            OR Defense IS NULL
            OR Special_Attack IS NULL
            OR Special_Defense IS NULL
            OR Speed IS NULL
            OR Base_Stat_Total IS NULL
            OR Base_Stat_Total <>
                HP + Attack + Defense
                + Special_Attack + Special_Defense + Speed
    """).fetchone()[0]

    print("Pokémon with stat issues:", issues)

finally:
    conn.close()