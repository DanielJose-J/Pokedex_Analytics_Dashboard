
import duckdb

# Connect to a database stored on disk
conn = duckdb.connect("data/pokedex.duckdb")

# Create the RAW schema
conn.execute("CREATE SCHEMA IF NOT EXISTS raw")

# Create the Pokemon RAW table
conn.execute("""
    CREATE OR REPLACE TABLE raw.pokemon AS
    SELECT *
    FROM read_json_auto('data/raw/pokemon.json')
""")
# create the species RAW table
conn.execute("""
   CREATE OR REPLACE TABLE raw.species AS
    SELECT *
    FROM read_json_auto('data/raw/species.json')
    """)

# Validate the record count
validation = conn.execute("""
    SELECT
        'pokemon' AS table_name
        ,COUNT(*) AS row_count
        ,COUNT(DISTINCT id) AS unique_ids
        ,MIN(id) AS min_id
        ,MAX(id) AS max_id
    FROM raw.pokemon

    UNION ALL

    SELECT
        'species'
        ,COUNT(*)
        ,COUNT(DISTINCT id)
        ,MIN(id)
        ,MAX(id)
    FROM raw.species
""")

print(validation.fetchall())


## Validating the grain
grain_validation = conn.execute("""
                                SELECT
    id AS Pokemon_ID
    ,name AS Pokemon_Name
    ,generation.name AS Generation_Name
    ,is_legendary AS Is_Legendary
    ,is_mythical AS Is_Mythical
    ,is_baby AS Is_Baby
FROM raw.species
WHERE id = 1;""")


print(grain_validation.fetchall())


conn.close()



