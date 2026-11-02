CREATE SCHEMA IF NOT EXISTS model;

-- Grain: one row per generation.
CREATE OR REPLACE TABLE model.DimGeneration (
    Generation_ID INTEGER PRIMARY KEY  -- Numeric generation identifier
    ,Generation_Name VARCHAR           -- API name, such as generation-i
);