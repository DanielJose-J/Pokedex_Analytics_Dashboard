-- Full refresh of Pokémon-to-type assignments.
DELETE FROM model.BridgePokemonType;

INSERT INTO model.BridgePokemonType (
    Pokemon_ID
    ,Type_ID
    ,Type_Slot
)

-- Expand each Pokémon's type list into separate rows.
WITH CTE_TYPES AS (
    SELECT
        id AS Pokemon_ID
        ,UNNEST(types) AS Type_Entry
    FROM raw.pokemon
    WHERE is_default = TRUE
)

SELECT
    Pokemon_ID

    -- Extract the numeric type ID from its API URL.
    ,CAST(
        regexp_extract(Type_Entry.type.url, '/([0-9]+)/$', 1)
        AS INTEGER
    ) AS Type_ID

    -- Preserve whether this is the first or second type.
    ,Type_Entry.slot AS Type_Slot
FROM CTE_TYPES;