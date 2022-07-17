CREATE_MEMBER_SQL = """
INSERT INTO Users (
    user_id, 
    display_name, 
    guild, 
    name, 
    nick
)
VALUES (
    $1, 
    $2, 
    $3, 
    $4, 
    $5
)
ON CONFLICT(user_id) DO UPDATE
SET
    user_id = EXCLUDED.user_id,
    display_name = EXCLUDED.display_name,
    guild = EXCLUDED.guild,
    name = EXCLUDED.name,
    nick = EXCLUDED.nick
"""    

CREATE_SHOW_SQL = """
INSERT INTO Shows (name) VALUES ($1) 
ON CONFLICT DO NOTHING 
RETURNING show_id
"""

ADD_VOTE_SQL = """
INSERT INTO votes (
    user_id, 
    show_id, 
    interested
) 
VALUES (
    $1, 
    $2, 
    $3
)
ON CONFLICT (user_id, show_id) DO UPDATE
SET
    interested = EXCLUDED.interested
"""

CHOOSE_SHOW_SQL = """
SELECT s.name
FROM shows s
JOIN votes v ON v.show_id = s.show_id AND interested
GROUP BY 1
HAVING array_agg(v.user_id) @> ($1)
AND array_agg(v.user_id) <@ ($1)
"""