CREATE TABLE Users (
    user_id bigint PRIMARY KEY,
    avatar_url text,
    display_name text,
    avatar text,
    default_avatar text,
    default_avatar_url text,
    guild text,
    name text,
    nick text    
);

CREATE TABLE Shows (
    show_id SERIAL PRIMARY KEY,
    name text,
    show_image_url text,
    removed boolean DEFAULT FALSE
);

CREATE TABLE Votes (
    user_id bigint REFERENCES Users(user_id),
    show_id int REFERENCES Shows(show_id),
    interested boolean
);

CREATE TABLE IF NOT EXISTS Token(
    token text,
    guild text
);

GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO moviebot;