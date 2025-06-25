CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 1. users
CREATE TABLE users (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    mail TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL, 
    avatar TEXT
);
/*
password will be stored as hashed with pgcrypto
Example:
INSERT INTO users (name, mail, password)
VALUES ('Alice', 'alice@example.com', crypt('securePassword123', gen_salt('bf')));
*/

-- 2. book
CREATE TABLE book (
    id UUID PRIMARY KEY,
    author TEXT,
    title TEXT NOT NULL,
    language TEXT,
    description TEXT,
    cover TEXT
);

-- 3. tag
CREATE TABLE tag (
    id UUID PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);

-- 4. book_tag (Many-to-Many)
CREATE TABLE book_tag (
    tag_id UUID NOT NULL,
    book_id UUID NOT NULL,
    PRIMARY KEY (tag_id, book_id),
    FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES book(id) ON DELETE CASCADE
);

-- 5. collection
CREATE TABLE collection (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    user_id UUID NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    description TEXT,
    cover TEXT,
    is_private BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. collection_item
CREATE TABLE collection_item (
    collection_id UUID NOT NULL,
    book_id UUID NOT NULL,
    content_type TEXT,
    PRIMARY KEY (collection_id, book_id),
    FOREIGN KEY (collection_id) REFERENCES collection(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES book(id) ON DELETE CASCADE
);

-- 7. review
CREATE TABLE review (
    user_id UUID NOT NULL,
    book_id UUID NOT NULL,
    rate INTEGER CHECK (rate BETWEEN 0 AND 10),
    text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, book_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES book(id) ON DELETE CASCADE
);

-- 8. note
CREATE TABLE note (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    book_id UUID REFERENCES book(id) ON DELETE CASCADE,
    text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. user_book
CREATE TABLE user_book (
    user_id UUID NOT NULL,
    book_id UUID NOT NULL,
    start_date DATE,
    end_date DATE,
    status TEXT CHECK (status IN ('want to read', 'reading now', 'have read')),
    PRIMARY KEY (user_id, book_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES book(id) ON DELETE CASCADE
);

-- 10. streak
CREATE TABLE streak (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    start_date DATE,
    end_date DATE
);

-- 11. subscription
CREATE TABLE subscription (
    follower_id UUID NOT NULL,
    subscribed_id UUID NOT NULL,
    PRIMARY KEY (follower_id, subscribed_id),
    FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (subscribed_id) REFERENCES users(id) ON DELETE CASCADE
);
