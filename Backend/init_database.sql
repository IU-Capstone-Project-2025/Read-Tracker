CREATE EXTENSION IF NOT EXISTS pgcrypto;


-- 1. User Table
CREATE TABLE "User" (
    ID SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    mail TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL, 
    avatar TEXT
);
/*
password will be stored as hashed with pgcrypto
Example: Insert User with Hashed Password
INSERT INTO "User" (name, mail, password)
VALUES ('Alice', 'alice@example.com', crypt('securePassword123', gen_salt('bf')));
*/


-- 2. Book Table
CREATE TABLE Book (
    ID SERIAL PRIMARY KEY,
    author TEXT,
    title TEXT NOT NULL,
    language TEXT,
    description TEXT,
    cover TEXT --book cover
);

-- 3. Tag Table
CREATE TABLE Tag (
    ID SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);

-- 4. BookTag (Many-to-Many)
-- note: a book may have more than one tag
CREATE TABLE BookTag (
    tag_ID INTEGER NOT NULL,
    book_ID INTEGER NOT NULL,
    PRIMARY KEY (tag_ID, book_ID),
    FOREIGN KEY (tag_ID) REFERENCES Tag(ID) ON DELETE CASCADE,
    FOREIGN KEY (book_ID) REFERENCES Book(ID) ON DELETE CASCADE
);

-- 5. Collection Table
CREATE TABLE Collection (
    ID SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    user_ID INTEGER REFERENCES "User"(ID) ON DELETE SET NULL,
    description TEXT,
    cover TEXT,
    is_private BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. CollectionItem (Many-to-Many)
CREATE TABLE CollectionItem (
    collection_ID INTEGER NOT NULL,
    book_ID INTEGER NOT NULL,
    content_type TEXT,
    PRIMARY KEY (collection_ID, book_ID),
    FOREIGN KEY (collection_ID) REFERENCES Collection(ID) ON DELETE CASCADE,
    FOREIGN KEY (book_ID) REFERENCES Book(ID) ON DELETE CASCADE
);

-- 7. Review Table
-- note: a book can only have one review from one user
CREATE TABLE Review (
    user_ID INTEGER NOT NULL,
    book_ID INTEGER NOT NULL,
    rate INTEGER CHECK (rate BETWEEN 0 AND 10),
    text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_ID, book_ID),
    FOREIGN KEY (user_ID) REFERENCES "User"(ID) ON DELETE CASCADE,
    FOREIGN KEY (book_ID) REFERENCES Book(ID) ON DELETE CASCADE
);

-- 8. Note Table
-- note: a book may have several notes from one user
CREATE TABLE Note (
    ID SERIAL PRIMARY KEY,
    user_ID INTEGER REFERENCES "User"(ID) ON DELETE CASCADE,
    book_ID INTEGER REFERENCES Book(ID) ON DELETE CASCADE,
    text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. UserBook Table
CREATE TABLE UserBook (
    user_ID INTEGER NOT NULL,
    book_ID INTEGER NOT NULL,
    start_date DATE,
    end_date DATE,
	status TEXT CHECK (status IN ('want to read', 'reading now', 'have read')),
	PRIMARY KEY (user_ID, book_ID),
    FOREIGN KEY (user_ID) REFERENCES "User"(ID) ON DELETE CASCADE,
    FOREIGN KEY (book_ID) REFERENCES Book(ID) ON DELETE CASCADE
);

-- 10. Streak Table
-- note: streak is the sequence of days user was reading continiously
CREATE TABLE Streak (
    ID SERIAL PRIMARY KEY,
    user_ID INTEGER REFERENCES "User"(ID) ON DELETE CASCADE,
    start_date DATE,
    end_date DATE
);

-- 11. Subscription Table
CREATE TABLE Subscription (
    follower_id INTEGER NOT NULL,
    subscribed_id INTEGER NOT NULL,
    PRIMARY KEY (follower_id, subscribed_id),
    FOREIGN KEY (follower_id) REFERENCES "User"(ID) ON DELETE CASCADE,
    FOREIGN KEY (subscribed_id) REFERENCES "User"(ID) ON DELETE CASCADE
);


