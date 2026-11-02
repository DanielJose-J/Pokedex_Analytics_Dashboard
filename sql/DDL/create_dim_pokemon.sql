CREATE SCHEMA IF NOT EXISTS model;

-- Grain: one row per default Pokémon variety.
CREATE OR REPLACE TABLE model.DimPokemon (
    Pokemon_ID BIGINT PRIMARY KEY  -- Unique Pokémon identifier from PokéAPI
    ,Pokemon_Name VARCHAR         -- Pokémon name from the API
    ,Species_ID BIGINT            -- Species referenced by this Pokémon
    ,Generation_ID INTEGER        -- References DimGeneration; species' debut generation
    ,Is_Legendary BOOLEAN         -- TRUE if the species is Legendary
    ,Is_Mythical BOOLEAN          -- TRUE if the species is Mythical
    ,Is_Baby BOOLEAN              -- TRUE if the species is classified as a baby Pokémon
    ,Height_M DOUBLE              -- Height in meters; source height divided by 10
    ,Weight_KG DOUBLE             -- Weight in kilograms; source weight divided by 10
    ,Sprite_URL VARCHAR           -- Default front sprite URL for the Pokémon gallery
    ,Artwork_URL VARCHAR          -- Official artwork URL for the Pokémon profile
);

