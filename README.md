# Library Management System
This is a Library Management System built using MySQL and Docker Compose. 
The system allows users to keep track of books in a library, including adding, editing, and deleting books, as well as checking out and returning books.
# Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
# Prerequisites
- Docker and Docker Compose must be installed on your machine
- A MySQL server running on the default port (3306)
- MySql Workbench - is advanced , only for debugging
# Installing
1. Clone the repository to your local machine:
git clone https://github.com/sdouek/MLM.git
2. Navigate to the project directory and run the following command to start the application: 
 **docker-compose up --build**
This cmd will start the MySQL server and the application in separate containers.
3. The application will be accessible at http://127.0.0.1:8084
# Usage
The application provides the following functionality:

- POST /user/register
- POST /book
- DELETE /book/<book_id>
- GET /catalog
- PUT /checkout/book/<book_id>
- PUT /return/book/<book_id>
- GET /checked_out/book/<user_name>

# Include Tests
- cd MLM/tests
- There is collection for postman that can be export and run   

# Built With
- [Docker](https://www.docker.com/) - Containerization platform
- [Docker Compose](https://docs.docker.com/compose/) - Tool for defining and running multi-container applications
- [MySQL](https://www.mysql.com/) - Relational database management system

# Authors
Sara Douek - sdouek
