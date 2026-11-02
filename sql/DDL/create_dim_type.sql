-- Grain: one row per Pokémon type.
CREATE OR REPLACE TABLE model.DimType (
    Type_ID INTEGER PRIMARY KEY  -- Type identifier from PokéAPI
    ,Type_Name VARCHAR           -- Type name, such as water or grass
);