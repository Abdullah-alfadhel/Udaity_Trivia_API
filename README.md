# Trivia API Backend
This is a game where you can play with the guys and test your knowledge and add to it too!!!
you can play the quiz, add questions, delete question, and search for questions.
## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

>_tip_: **npm i** is shorthand for **npm install**

## Required Tasks

## Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.
<br>

```bash
npm start
```

## Request Formatting

The frontend should be fairly straightforward and digestible. You can reference the frontend to view how it parses the responses. 
 

## Optional: Styling

In addition, you may want to customize and style the frontend by editing the CSS in the ```stylesheets``` folder. 

## API Reference

### Getting Started

* Backend Base URL: `http://127.0.0.1:5000/`
* Frontend Base URL: `http://127.0.0.1:3000/`
* Authentication: Authentication or API keys are not used in the project.

### Error Handling

Errors are returned in the following json format:

```json
      {
        "success": 'False',
        "error": 404,
        "message": 'Resource not found',
      }
```

The error codes currently returned are:

* 400 – Bad request error
* 404 – resource not found
* 422 – Uncrossable entity
* 500 – Internal error, please try again.

### Endpoints

#### GET /categories

- General: 
  - Returns all categories.

- Sample:  `curl http://127.0.0.1:5000/categories`

```json
    {
        "categories": {
            "1": "Science", 
            "2": "Art", 
            "3": "Geography", 
            "4": "History", 
            "5": "Entertainment", 
            "6": "Sports"
        }, 
        "success": True
    }
```

#### GET /questions
- General:
  - Returns all questions
  - questions are paginated.
  - pages could be requested by a query parameters in the format of ``` "questions/page?=int" ```

- Sample: `curl http://127.0.0.1:5000/questions`
<br>

```json
        {
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        ... etc
    ],
    "success": True,
    "total_questions": 19
}
```

#### DELETE /questions/<int:question_id>


- General:
  - Deletes a question by id form the url parameter.

- Sample: `curl http://127.0.0.1:5000/questions/6 -X DELETE`

```json
        {
          "success": True,
        }
```

#### POST /questions

- General:
  - Creates a new question based on a payload.

- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{
            "question": "what is my name?",
            "answer": "Abdullah",
            "difficulty": 1,
            "category": "6"
        }'`

```json
{
  "success": True
}
```

#### POST /questions/search

- General:
  - returns questions that has the search substring

- Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Tom"}'`

```json
{
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "success": True,
  "total_questions": 1,
  "categories": {1: "Science", 2: "Art", 3: "Geography", 4: "History", 5: "Entertainment", 6: "Sports"},
  "current_category" : "all"
}
```

#### GET /categories/<int:category_id>/questions

- General:
  - Gets questions by category using the category id from the url parameter.
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`
<br>

```json
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    ...etc
  ],
  "success": true,
  "total_questions": 3
}

```

#### POST /quizzes

- General
  - Takes the category and previous questions in the request if existed.
  - Return random question that is not in the previous questions.

- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [5, 9],
                                            "quiz_category": {"type": "History", "id": "4"}}'`

```json
{
    "success": true,
    "question": {
    "answer": "George Washington Carver",
    "category": 4,
    "difficulty": 2,
    "id": 12,
    "question": "Who invented Peanut Butter?"
  }
}

```
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Authors

- Abdullah Alfadhel
- Udacity team 

