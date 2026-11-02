DELETE FROM model.DimType;

INSERT INTO model.DimType (
    Type_ID
    ,Type_Name
)
WITH CTE_TYPES AS (
    SELECT
        UNNEST(types) AS Type_Entry
    FROM raw.pokemon
    WHERE is_default = TRUE
)
SELECT DISTINCT
    CAST(
        regexp_extract(Type_Entry.type.url, '/([0-9]+)/$', 1)
        AS INTEGER
    ) AS Type_ID
    ,Type_Entry.type.name AS Type_Name
FROM CTE_TYPES;