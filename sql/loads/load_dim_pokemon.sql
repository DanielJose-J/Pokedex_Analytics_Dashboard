-- Full refresh: remove existing records before inserting fresh data.
-- The Python runner will execute this load within a transaction.

DELETE FROM model.DimPokemon;

INSERT INTO model.DimPokemon (
    Pokemon_ID
    ,Pokemon_Name
    ,Species_ID
    ,Generation_ID
    ,Is_Legendary
    ,Is_Mythical
    ,Is_Baby
    ,Height_M
    ,Weight_KG
    ,Sprite_URL
    ,Artwork_URL
    ,HP
    ,Attack
    ,Defense
    ,Special_Attack
    ,Special_Defense
    ,Speed
    ,Base_Stat_Total
)

WITH CTE_POKEMON AS (
    SELECT
        id AS Pokemon_ID
        ,name AS Pokemon_Name
        ,CAST(
            regexp_extract(species.url, '/([0-9]+)/$', 1)
            AS BIGINT
        ) AS Species_ID
        ,height / 10.0 AS Height_M
        ,weight / 10.0 AS Weight_KG
        ,sprites.front_default AS Sprite_URL
        ,sprites.other."official-artwork".front_default AS Artwork_URL
    FROM raw.pokemon
    WHERE is_default = TRUE
)

-- Expand the stats list into one row per Pokémon per stat.
,CTE_STATS_EXPANDED AS (
    SELECT
        id AS Pokemon_ID
        ,UNNEST(stats) AS Stat_Entry
    FROM raw.pokemon
    WHERE is_default = TRUE
)

-- Turn the six stat rows into six columns per Pokémon.
,CTE_STATS AS (
    SELECT
        Pokemon_ID
        ,MAX(CASE WHEN Stat_Entry.stat.name = 'hp'
            THEN Stat_Entry.base_stat END) AS HP
        ,MAX(CASE WHEN Stat_Entry.stat.name = 'attack'
            THEN Stat_Entry.base_stat END) AS Attack
        ,MAX(CASE WHEN Stat_Entry.stat.name = 'defense'
            THEN Stat_Entry.base_stat END) AS Defense
        ,MAX(CASE WHEN Stat_Entry.stat.name = 'special-attack'
            THEN Stat_Entry.base_stat END) AS Special_Attack
        ,MAX(CASE WHEN Stat_Entry.stat.name = 'special-defense'
            THEN Stat_Entry.base_stat END) AS Special_Defense
        ,MAX(CASE WHEN Stat_Entry.stat.name = 'speed'
            THEN Stat_Entry.base_stat END) AS Speed
    FROM CTE_STATS_EXPANDED
    GROUP BY Pokemon_ID
)

SELECT
    p.Pokemon_ID
    ,p.Pokemon_Name
    ,p.Species_ID
    ,CAST(
        regexp_extract(s.generation.url, '/([0-9]+)/$', 1)
        AS INTEGER
    ) AS Generation_ID
    ,s.is_legendary
    ,s.is_mythical
    ,s.is_baby
    ,p.Height_M
    ,p.Weight_KG
    ,p.Sprite_URL
    ,p.Artwork_URL
    ,st.HP
    ,st.Attack
    ,st.Defense
    ,st.Special_Attack
    ,st.Special_Defense
    ,st.Speed
    ,st.HP + st.Attack + st.Defense
        + st.Special_Attack + st.Special_Defense
        + st.Speed AS Base_Stat_Total
FROM CTE_POKEMON AS p
LEFT JOIN raw.species AS s
    ON p.Species_ID = s.id
LEFT JOIN CTE_STATS AS st
    ON p.Pokemon_ID = st.Pokemon_ID;