-- Refresh the generation records.
DELETE FROM model.DimGeneration;

INSERT INTO model.DimGeneration (
    Generation_ID
    ,Generation_Name
)
SELECT DISTINCT
    CAST(
        regexp_extract(generation.url, '/([0-9]+)/$', 1)
        AS INTEGER
    ) AS Generation_ID
    ,generation.name AS Generation_Name
FROM raw.species;