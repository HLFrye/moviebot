CREATE TABLE recommendation (
    message_id bigint PRIMARY KEY,
    user_ids bigint[],
    show_id bigint,
    parent_message_id bigint,
    rejected boolean
);

GRANT SELECT, INSERT, UPDATE ON TABLE recommendation TO moviebot;
GRANT SELECT ON TABLE recommendation TO grafana;
