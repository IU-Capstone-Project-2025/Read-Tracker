### Login page interaction

On the auth page user may register, login or reset password:

#### POST /auth/register

```
{
  "mail": "user@example.com",
  "password": "password"
}
```

Validation Steps:

1. Checks if the email is in a valid format (e.g., user@domain.com).
2. Verifies that the email is not already registered in the system.
3. Ensures the password meets security requirements (e.g., minimum length, special characters).

Possible Responses:

- 200 OK – Registration successful.

```
{
  "status": "success",
  "message": "User registered successfully",
}
```

- 400 Bad Request – Invalid email, weak password, or missing fields.

```
{
  "status": "error",
  "message": "Invalid email format or password requirements not met."
}
```

- 409 Conflict – Email already exists.

```
{
  "status": "error",
  "message": "This email is already registered."
}
```

#### POST /auth/login

Accepts a JSON for authentication:

```
{
  "mail": "user@example.com",
  "password": "password"
}
```

Validation Steps:

1. Checks if the email exists in the system.
2. Verifies the password matches the stored hash.
3. Generates a JWT for authenticated users.

Possible Responses:

- 200 OK – Login successful.
  The route returns JWT with description "User logged in successfully."
  Something like

```
{
    "token": "abc123..."
}
```

- 401 Unauthorized – Invalid credentials.

```
{
  "status": "error",
  "message": "Incorrect email or password."
}
```

- 404 Not Found – Email not registered.

```
{
  "status": "error",
  "message": "No account found with this email."
}
```

#### POST /auth/validate

The route which validates token

Accepts a JSON for validation:

```
{
    "token": "abc123...",
}
```

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Token validated."
}
```

- 404 Not Found

```
{
  "status": "error",
  "message": "User is not found."
}
```

#### POST /auth/refresh

Refreshes the token with new one.
Accepts a JSON with refresh token:

```
{
    "token": "abc123...",
}
```

Possible responses:

- 200 OK - sends back new created token

```
{
    "token": "abc123..."
}
```

- 404 Not Found

```
{
  "status": "error",
  "message": "User is not found."
}
```

### Password Reset Functionality

The reset functionality has two steps: forgot-password and reset-password

#### POST /auth/forgot_password

```
{
  "mail": "user@example.com"
}
```

Validation steps:

1. Email must be valid email address
2. Checks if the email exists in the system.
3. Generates unique token for reset  (e.g., 6-digit numeric or UUID or digits with letters).
4. Sends the link to the email with this format:

https://{read-tracker.com}/auth/reset-password?token=abc123...

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "If the email is registered, a reset link has been sent."
}
```

- 400 Bad Request – Incorrect.

```
{
  "status": "error",
  "message": "Invalid email format."
}
```

- 404 Not Found – Email not registered.

```
{
  "status": "error",
  "message": "No account found with this email."
}
```

#### POST /auth/reset_password

```
{
  "token": "abc123...",
  "new_password": "new_password"
}
```

Validation steps

1. Check if the token exists and is not expired.
2. Validate the password correctness.
3. Find associated user by token.userId.
4. Hash and update the user's password.
5. Invalidate the token after use.

Possible responses:

- 200 OK – Password updated successfully.

```
{
  "status": "success",
  "message": "Password updated successfully."
}
```

- 400 Bad Request – Invalid or expired mail token.

```
{
  "status": "error",
  "message": "Invalid or expired mail token."
}
```

### User profile page

#### GET /auth/profile

Possible responses:

- 200 OK
  Returns the profile schema with name, mail, id and avatarUrl

- 401 Unauthorized

```
{
    "status": "error",
    "message": "Invalid or expired token."
}
```

#### PUT /auth/profile/avatar

The route accepts JSON:

```
{
  "avatarUrl": "https://cdn.example.com/new-avatar.jpg"
}
```

Possible responses:

- 200 OK - avatar updated

```
{
  "status": "success",
  "message": "Avatar updated"
}
```

- 400 Bad Request - Avatar not found or incorrect format

```
{
  "status": "error",
  "message": "Invalid format of avatar"
}
```

- 401 Unauthorized

```
{
    "status": "error",
    "message": "Invalid or expired token."
}
```

#### PUT /auth/profile/password

The route accepts JSON:

```
{
  "curr_password": "password",
  "new_password": "new_password"
}
```

Validation steps:

1. Check the old password correctness
2. Validate new password correctness
3. Hash and update the user's password.

Possible responses:

- 200 OK - Password changed successfully

```
{
  "status": "success",
  "message": "Password changed successfully"
}
```

- 400 Bad Request – Old password or new password is incorrect.

```
{
  "status": "error",
  "message": "Incorrect old or new password"
}
```

- 401 Unauthorized

```
{
    "status": "error",
    "message": "Invalid or expired token."
}
```

### Users streak

#### POST /me/check_in

``` 
{
  "date": date
}
```

If user already has a streak, do nothing. Else create new streak (add create_date)

- 200 OK
```
{
  "status": "success",
  "message": "Successfully marked"
}
```

#### PUT /me/check_in

This place if user forgot about streak: make end_date of streak

``` 
{
  "date": date
}
```

Response:

- 200 OK
```
{
  "status": "success",
  "message": "Successfully marked"
}
```

### Books page

#### GET /books

List all books (optionally filtered)

Response:

- 200 OK

```
{
  "status": "success",
  "message": "Books retrieved",
  "data": [ /* Array of books (may be empty if no books) */ ]
}
```

#### GET /books/:book_id

Get single book

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Book details retrieved",
  "data": {
    "id": "uuid",
    "title": "Book Title",
    "author": "Author Name",
    "language": "lang",
    "cover": "https://cdn.example.com/cover.jpg"
  }
}
```

- 404 Not Found

```
{
  "status": "error",
  "message": "Book not found"
}
```

#### POST /books

Request:

```
{
  "title": "Book Title",
  "author": "Author Name",
  "language": "lang",
  "cover": "https://cdn.example.com/cover.jpg"
}
```

Validation steps:

1. Checks the title correctness
2. Checks the author correctness

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Book added",
  "data": {
      "id": "uuid",
      "title": "Book Title",
      "author": "Author Name",
      "language": "lang",
      "cover": "https://cdn.example.com/cover.jpg"
      }
}
```

- 400 Bad Request

```
{
  "status": "error",
  "message": "Invalid format of title or author"
}
```

#### PUT /books/:book_id

Update a book

Request:

```
{
  "title": "new title",
  "author": "new author",
  "status": "finished",
  "language": "English",
  "cover": "https://cdn.example.com/new-cover.jpg"
}
```

Validation steps:

1. Checks the title correctness
2. Checks the author correctness

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Book updated"
}
```

- 400 Bad Request

```
{
  "status": "error",
  "message": "Invalid format of title or author"
}
```

- 404 Not Found

```
{
  "status": "error",
  "message": "Book not found"
}
```

#### DELETE /books/:book_id

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Book deleted"
}
```

- 404 Not Found

```
{
  "status": "error",
  "message": "Book not found"
}
```

### My books page 

The page where user may add book and add status of reading, finishing etc

#### GET /me/books?{filter=status:reading} 

Response:

- 200 OK

```
{
  "status": "success",
  "message": "User books retrieved",
  "data": [ /* Array of books (may be empty if no books) */ ]
}
```

#### GET /me/books/:book_id

Get single book

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "User book details retrieved",
  "data": {
    "book_id": uuid,
    "start_date": "2025-01-01",
    "end_date": "",
    "status": "reading"
  }
}
```

- 404 Not Found

```
{
  "status": "error",
  "message": "User book not found"
}
```

#### POST /me/books

```
{
  "book_id": uuid,
  "start_date": "2025-01-01",
  "status": "reading"
}
```

Possible responses:

- 200 OK
```
{
  "status": "success",
  "message": "User book successfully added"
}
```

- 404 Not Found

```
{
  "status": "error",
  "message": "User book not found"
}
```

#### PUT /me/books/:book_id

Update the status/end_date of the user book

```
{
  "end_date": "2025-01-10",
  "status": "finished"
}
```

- 200 OK
```
{
  "status": "success",
  "message": "User book updated successfully"
}
```

- 404 Not Found

```
{
  "status": "error",
  "message": "User book not found"
}
```

#### DELETE /me/books/:book_id

- 200 OK
```
{
  "status": "success",
  "message": "User book deleted successfully"
}
```

- 404 Not Found

```
{
  "status": "error",
  "message": "User book not found"
}
```

### Users page (for subscriptions etc)

### Subscriptions

#### POST /subscriptions

```
{
  "subscribed_id": "user_id"
}
```

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Subscribed successfully"
}
```

- 404 Not Found

```
{
  "status": "error",
  "message": "User not found"
}
```


#### DELETE /subscriptions/:subscribed_id

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Unsubscribed successfully"
}
```

- 404 Not Found

```
{
  "status": "error",
  "message": "Subscriber not found"
}
```


#### GET /feed/collections?{limit=10&offset=20|user_id=uuid}
Get all collections from subscriptions (maybe we can add limit query parameter to get limited count)

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "collections retrieved successfully",
  "data": { 
    "items": [*/array of collections (may be empty)/*],
    "pagination": {
      "limit": 10,
      "offset": 20,
      "total": 123
    }
  }
}
```
?sort=rate|created_at

#### GET /feed/reviews?{limit=10&offset=20|user_id=uuid}
Get all reviews from subscriptions (maybe we can add limit query parameter to get limited count)

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "reviews retrieved successfully",
  "data": { 
    "items": [*/array of reviews (may be empty)/*],
    "pagination": {
      "limit": 10,
      "offset": 20,
      "total": 123
    }
  }
}
```

### Reviews page

#### GET /books/:book_id/reviews

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Reviews retrieved",
  "data": [ /* Array of reviews (may be empty) */ ]
}
```

#### GET /users/:user_id/reviews

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Reviews retrieved",
  "data": [ /* Array of reviews (may be empty) */ ]
}
```

#### GET /me/reviews/:review_id

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Review retrieved",
  "data": {
    "id": "uuid",
    "content_type": "good_review",
    "user_id": uuid
    "rate": 5,
    "text": "Great read!",
    "book_id": uuid
  }
}
```

- 404 Not Found

```
{
  "status": "error",
  "message": "Review not found"
}
```

#### POST /me/reviews

Request:

```
{
    "book_id": uuid,
    "rate": 5,
    "text": "Loved it!"
}
```

Validation steps:

1. Search book with this uuid.
2. Validate comment correctness.

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Review created"
}
```

- 400 Bad Request - Invalid text

```
{
  "status": "error",
  "message": "Invalid text"
}
```

- 404 Not Found - book with this uuid not found

```
{
  "status": "error",
  "message": "Book not found"
}
```

#### PUT /me/reviews/:review_id

```
{
    "rate": 3,
    "text": "Changed"
}
```

Validation steps:

1. Search book with this uuid.
2. Validate comment correctness.

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Review updated"
}
```

- 400 Bad Request - Invalid comment

```
{
  "status": "error",
  "message": "Invalid review"
}
```

- 404 Not Found - book with this uuid not found

```
{
  "status": "error",
  "message": "Book not found"
}
```

- 409 Conflict
```
{
  "status": "error",
  "message": "You do not have permission to modify this review."
}
```

#### DELETE /me/reviews/:review_id

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Review deleted"
}
```

- 404 Not Found

```
{
  "status": "error",
  "message": "Review not found"
}
```

- 409 Conflict
```
{
  "status": "error",
  "message": "You do not have permission to modify this review."
}
```

### Notes

#### GET /me/books/:book_id/notes

Response:

```
{
  "status": "success",
  "message": "Notes retrieved",
  "data": [ /* array of notes (may be empty) */ ]
}
```

#### POST /me/books/:book_id/notes

Request:

```
{
  "rate": "5",
  "text": "Interesting..."
}
```

Possible responses

- 200 OK

```
{
  "status": "success",
  "message": "Note added"
}
```

- 400 Bad Request

```
{
  "status": "error",
  "message": "Invalid note"
}
```

#### GET /me/notes/:note_id

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Note details retrieved",
  "data": {
    "id": uuid,
    "text": "Note text here",
    "book_id": uuid,
    "created_at": datetime,
  }
}
```

- 404 Not Found

```
{
  "status": "error",
  "message": "Note not found"
}
```

#### PUT /me/notes/:note_id

Request:

```
{
  "text": "Interesting car"
}
```

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Note updated"
}
```

- 400 Bad Request

```
{
  "status": "error",
  "message": "Invalid note"
}
```

- 404 Not Found

```
{
  "status": "error",
  "message": "Note not found"
}
```

#### DELETE /me/notes/:note_id

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Note deleted"
}
```

- 404 Not Found

```
{
  "status": "error",
  "message": "Note not found"
}
```

### My Collections

#### GET /me/collections

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "collections retrieved successfully",
  "data": { */array of collections (may be empty)/* }
}
```

#### GET /me/collections/:collection_id

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Collection fetched successfully",
  "data":
  {
    "collection_id": uuid,
    "title": "Collection",
    "description": "descriptions",
    "cover": "https://...",
    "user_id": uuid,
    "username": "username",
    "is_private": false,
    "created_at": datetime,
  }
}
```

- 404 Not Found

```
{
  "status": "error",
  "message": "Collection not found"
}
```

#### POST /me/collections

Applies JSON:
```
{
  "title": "title",
  "description": "description",
  "is_private": true,
  "cover": "https://..."
}
```
Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Collection created"
}
```

- 400 Bad Request

```
{
  "status": "error",
  "message": "Invalid collection"
}
```

#### PUT /me/collections/:collection_id

Update the collection.
```
{
  "title": "new title",
  "description": "new description",
  "is_private": false,
  "cover": "https://..."
}
```

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Collection updated"
}
```

- 404 Not Found

```
{
  "status": "error",
  "message": "Collection not found"
}
```


#### DELETE /me/collections/:collection_id

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Collection deleted"
}
```

- 404 Not Found

```
{
  "status": "error",
  "message": "Collection not found"
}
```

#### POST /me/collections/:collection_id/books

Add the book to the collection
Applies the JSON with uuid of the book:

```
{
  "book_id": uuid
}
```

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Book added to the collection"
}
```

- 404 Not Found

```
{
  "status": "error",
  "message": "Collection not found"
}
```

#### DELETE /me/collections/:collection_id/books/:book_id

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Book deleted from the collection"
}
```

- 404 Not Found

```
{
  "status": "error",
  "message": "Collection or book not found"
}
```
