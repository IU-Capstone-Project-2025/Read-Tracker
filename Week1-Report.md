# Week #1

## Project description

### Project name: Read Tracker

**Code repository**: https://github.com/IU-Capstone-Project-2025/Read-Tracker

Our project is aimed at creating a multifunctional system for reading people. 
It includes: a tracker for reading, 
storing information about books read (when finished, a review of the book read), 
creating your own collections according to certain criteria (for example, "the 10 best books in the fantasy genre"). 
Thanks to our system, users will be able to track their reading progress and store information about what they have read, but they will also be able to share this information with others (if desired).

### **Team Members**

| Team Member                             | Telegram Alias   | Email Address                      | Track                                       | Responsibilities   |
|-----------------------------------------|------------------|------------------------------------|---------------------------------------------|--------------------|
| Darya Tolmeneva (Lead)                  | @DinPg           | d.tolmeneva@innopolis.university   | Fullstack + Reports                         | [Responsibilities] |
| Andrey Torgashinov                      | @TovarishDru     | a.torgashinov@innopolis.university | DevOps                                      | [Responsibilities] |
| Ivan Isakov                             | @Muhozhukich     | i.isakov@innopolis.university      | Backend                                     | [Responsibilities] |
| Ivan Savelev                            | @Savelev_IV      | i.savelev@innopolis.university     | Frontend                                    | [Responsibilities] |
| Batraz Dzesov                           | @Borodum         | b.dzesov@innopolis.university      | Backend                                     | [Responsibilities] |


## Brainstorming

### Ideas during brainstorming
The project description has already added the ideas that we came up with during brainstorming, but below we will add information about the order in which the ideas appeared.


The original idea is a tracker. But this is too trivial and it was necessary to develop the project somehow. 
That's why we had the idea to keep lists of what we've read and, accordingly, reviews of these books we've read. 
Then we decided that it would be nice to create our own collections of books (because they are more thematic and focused than just "I want to read"). 
After that, we thought it would be nice for users to share information with each other. 
But since this is not comfortable for everyone, we decided that the user will decide for himself what to share and what not to share. If he wants to stay completely private, then he will

### Brief market research / problem validation

https://readed.me/books
 - There is tracking, calendar, statistics, general database of books, reviews and rating
 - There is no way to make your own collections and share them.
 - It is not possible to subscribe to other users or read their collections.

   
https://rj-ten.vercel.app/
 - A simpler solution
 - You can crack how many pages you read per day in a book
 - There are functions of a reader's diary, reading progress and statistics
 - There is no global literature list, all books are downloaded locally
 - No reviews, no global rating
 - The only way to share literature is through the creation of groups, where, again, all books are uploaded manually by the creator
 - There are no collections, as such, there are no user accounts to subscribe to and whose recommendations can be viewed.


## Basic requirements

### Target users and their primary needs

The target user is a person who reads and wants to track his progress (by the number of days he has read), 
as well as store information about what he has already read or wants to read and his reviews of the books 
he has read (which can be public or private, depending on the user's desire). In addition, the target user
wants to create collections of books (for example, "The top 10 books that everyone should read") that they 
can share with other users or keep secret. The user will be able to subscribe to other users to read their reviews, watch collections and progress.

### User stories

*...*

### Initial scope

*...*


## Tech-stack

- HTML + CSS
- Javascript
- Python
- Fast API
- Flask
- SQL Alchemy
- Postgre SQL
- Docker


# Weekly commitments

## Individual contribution of each participant
**Darya:** wrote a report


**Ivan Savelev and Batraz:** сreated the directory structure and files, docker-compose and `README.md`


**Ivan Isakov and Andrey:** studied the market and product analogues

## Confirmation of the code's operability

We confirm that the code in the main branch:
- [ ] In working condition.
- [ ] Run via docker-compose (or another alternative described in the `README.md`).
