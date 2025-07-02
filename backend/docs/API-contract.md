### Login page interaction

On the auth page user may register, login or reset password:

#### POST /auth/register

```
{
  "email": "user@example.com",
  "password": "password"
}
```

Validation Steps:

1. Checks if the email is in a valid format (e.g., user@domain.com).
2. Verifies that the email is not already registered in the system.
3. Ensures the password meets security requirements (e.g., minimum length, special characters).

Possible Responses:

- 201 Created – Registration successful.

```
{
  "status": "success",
  "message": "User registered successfully."
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
  "password": "secure_password123"
}
```

Validation Steps:

1. Checks if the email exists in the system.
2. Verifies the password matches the stored hash.
3. Generates a session token or JWT for authenticated users.

Possible Responses:

- 200 OK – Login successful.

```
{
  "status": "success",
  "message": "Login successful.",
  "token": "abc123...",  // JWT or session token
  "user_id": uuid
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

#### GET /auth/profile

Get the current user info (token required)

Response

- 200 OK

```
{
"status": "success",
  "message": "User fetched successfully",
  "data": {
    "id": "uuid",
    "username": "Username",
    "email": "user@example.com"
  }
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

1. Email must be valid email adress
2. Checks if the email exists in the system.
3. Generates unique token for reset  (e.g., 6-digit numeric or UUID or digits with letters).
4. Sends the link to the email with this format:

https://{read-tracker.com}/auth/reset-password?token=abc123...

Possible responses:

- 200 OK – Если email существует (но не раскрываем статус в целях безопасности).

```
{
  "status": "success",
  "message": "If the email is registered, a reset link has been sent."
}
```

- 400 Bad Request – Некорректный email.

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

- 400 Bad Request – Invalid or expired token.

```
{
  "status": "error",
  "message": "Invalid or expired token."
}
```

### User profile page

#### GET /users/:user_id

Response:

```
{
  "status": "success",
  "message": "Profile retrieved",
  "data": {
    "id": "uuid",
    "username": "Username",
    "avatar": "https://cdn.example.com/avatar.jpg",
    "isVisible": true
  }
}
```

#### PUT /users/:user_id/avatar

Request:

```
{
  "avatarUrl": "https://cdn.example.com/new-avatar.jpg"
}
```

Responses:

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

#### PUT /users/:user_id/visibility

Request:

```
{
  "isVisible": false
}
```

Response:

```
{
  "status": "success",
  "message": "Visibility updated"
}
```

#### PUT /users/:user_id/password

Request:

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

### My Books page

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
    "status": "not started" // or "reading" or "finished"
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
  "title": "Back to the Future",
  "author": "Robert Zemekis"
  "language": "English",
  "description": "science fiction"
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
  "description": "smth"
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
  "message": "Review not found"
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

### Reviews page

#### GET /reviews

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Reviews retrieved",
  "data": [ /* Array of reviews (may be empty) */ ]
}
```

#### GET /reviews/:review_id

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

#### POST /reviews

Request:

```
{
    "book_id": uuid,
    "content_type": "good_review",
    "rate": 5,
    "text": "Loved it!"
    "data": {
      "id": "uuid"
    }
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

#### PUT /reviews/:review_id

```
{
    "content_type": "bad_review",
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
  "message": "Review changed"
}
```

- 400 Bad Request - Invalid comment

```
{
  "status": "error",
  "message": "Invalid comment"
}
```

- 404 Not Found - book with this uuid not found

```
{
  "status": "error",
  "message": "Book not found"
}
```

#### DELETE /reviews/:review_id

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

### Notes

#### GET /books/:book_id/notes

Response:

```
{
  "status": "success",
  "message": "Notes retrieved",
  "data": [ /* array of notes (may be empty) */ ]
}
```

#### POST /books/:book_id/notes

Request:

```
{
  "content_type": "
  "text": "Interesting car"
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
  "status": "success",
  "message": "Invalid note"
}
```

#### GET /notes/:note_id

Possible responses:

- 200 OK

```
{
  "status": "success",
  "message": "Note details retrieved",
  "data": {
    "id": uuid,
    "content_type": type,
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

#### PUT /notes/:note_id

Request:

```
{
  "content_type": "
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
  "status": "success",
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

#### DELETE /notes/:note_id

Possible response:

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

### Collections




