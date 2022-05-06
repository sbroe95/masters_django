CREATE TABLE IF NOT EXISTS espn (
    -- cut_element TEXT,
    -- cut_score TEXT,
    pos TEXT,
    player TEXT, 
    country_flag_image TEXT,
    link TEXT,
    to_par TEXT,
    today TEXT,
    thru TEXT,
    r1 TEXT,
    r2 TEXT,
    r3 TEXT,
    r4 TEXT,
    tot TEXT
);

CREATE TABLE IF NOT EXISTS players (
    gent TEXT,
    player_1 TEXT,
    player_2 TEXT,
    player_3 TEXT,
    predicted_score INTEGER
);


CREATE VIEW scores AS
WITH cte1 AS (
    SELECT gent,
       player_1,
           e1.to_par::INTEGER AS e1_score,
           CASE
               WHEN e1.thru = 'CUT' THEN 4
               ELSE 0
               END                                                      AS e1_penalty,
       player_2,
           e2.to_par::INTEGER AS e2_score,
           CASE
               WHEN e2.thru = 'CUT' THEN 4
               ELSE 0
               END                                                      AS e2_penalty,
       player_3,
           e3.to_par::INTEGER AS e3_score,
           CASE
               WHEN e3.thru = 'CUT' THEN 4
               ELSE 0
               END                                                      AS e3_penalty,
               predicted_score
    FROM players p
             LEFT JOIN espn e1 ON player_1 = e1.player
             LEFT JOIN espn e2 ON player_2 = e2.player
             LEFT JOIN espn e3 ON player_3 = e3.player

)
SELECT
       gent,
       player_1,
       player_2,
       player_3,
    e1_score + e2_score + e3_score + e1_penalty + e2_penalty + e3_penalty AS score,
    predicted_score
FROM cte1
ORDER BY score
;

