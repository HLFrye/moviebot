"""
This module contains SQL queries used by the bot
"""

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
SELECT s.name, s.show_id
FROM shows s
JOIN votes v ON v.show_id = s.show_id AND interested
GROUP BY 1, 2
HAVING array_agg(v.user_id) @> ($1)
AND array_agg(v.user_id) <@ ($1)
"""

CHOOSE_SHOW_SQL_WITH_EXCLUDES = """
SELECT s.name, s.show_id
FROM shows s
JOIN votes v ON v.show_id = s.show_id AND interested
WHERE NOT s.show_id = any($2::int[])
GROUP BY 1, 2
HAVING array_agg(v.user_id) @> ($1)
AND array_agg(v.user_id) <@ ($1)
"""

SAVE_RECOMMENDATION_SQL = """
INSERT INTO recommendation
(message_id, user_ids, show_id, rejected, parent_message_id)
VALUES
($1, $2, $3, False, $4)
"""

GET_RECOMMENDATION_SQL = """
SELECT user_ids, show_id
FROM recommendation
WHERE message_id = $1
"""

SET_REJECTED_SQL = """
UPDATE recommendation
SET rejected = True
WHERE message_id = $1
"""

GET_PARENT_SQL = """
SELECT 
    message_id,
    show_id,
    parent_message_id,
    user_ids
FROM recommendation
WHERE message_id = $1
"""

SEARCH_SHOW_SQL = """
SELECT
    show_id,
    name
FROM shows
WHERE name ILIKE $1
"""

MARK_SHOW_REMOVED = """
UPDATE shows
SET
    removed = true
WHERE show_id = $1
"""
