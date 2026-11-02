-- Grain: one row per Pokémon–type assignment.
CREATE OR REPLACE TABLE model.BridgePokemonType (
    Pokemon_ID BIGINT          -- References DimPokemon
    ,Type_ID INTEGER           -- References DimType
    ,Type_Slot INTEGER         -- First or second type
    ,PRIMARY KEY (Pokemon_ID, Type_ID)
);