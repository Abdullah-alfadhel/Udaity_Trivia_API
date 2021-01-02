import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
# paginating the questions function that take the questions and the request to
# paginate


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(
      app, resources={r"/": {
        "origins": "http://localhost:3000", 'credentials': True}}
      )

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
          'Access-Control-Allow-Credentials', 'true'
          )
        response.headers.add(
          'Access-Control-Allow-Origin', 'http://localhost:3000'
          )
        response.headers.add(
          'Access-Control-Allow-Headers', 'Content-Type,Authorization,true'
          )
        response.headers.add(
          'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS'
          )
        return response
    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample
    route after completing the TODOs /Done
    I decided to allow just the front end for more safety
    '''

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow /Done
    '''

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories. /Done
    '''
    @app.route('/categories', methods=["GET"])
    def categories_in_game():
        # fetches the categories and sort them in a
        # dictionary format to be accepted by the font end.
        try:
            categories = Category.query.all()
            data = {}
            for category in categories:
                data[category.id] = category.type
            return jsonify({
              'success': True,
              'categories': data
            }), 200
        except Exception:
            abort(500)
    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories. /Done

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at
    the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. /Done
    '''
    @app.route('/questions', methods=["GET"])
    def get_questions():
        # fetches the question and categories form the
        #  database to be formated for the font end.
        selection = Question.query.all()
        current_questions = paginate_questions(request, selection)
        categories = Category.query.all()
        question_categories = {}

        for category in categories:
            question_categories[category.id] = category.type
        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': question_categories,
            'current_category': 'all'
          }), 200
    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID. /Done

    TEST: When you click the trash icon next to a question,
     the question will be removed.
    This removal will persist in the database and
     when you refresh the page. /Done
    '''
    @app.route('/questions/<int:question_id>', methods=["DELETE"])
    def question_delete(question_id):
        # deletes the question by geting the
        # question id and then perform a delete command on it.
        try:
            question = Question.query.get(question_id)
            question.delete()
            return jsonify({
                'success': True,
              }), 200
        except Exception:
            abort(422)
    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score. /Done

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will
     appear at the end of the last page
    of the questions list in the "List" tab.  /Done
    '''
    @app.route('/questions', methods=["POST"])
    def adding_question():
        # checking if all the required information comming from the font end
        data = request.get_json()
        question = data.get('question', '')
        answer = data.get('answer', '')
        difficulty = data.get('difficulty', '')
        category = data.get('category', '')
        if ((question == '') or (answer == '')
                or (difficulty == '') or (category == '')):
            abort(422)
        try:
            # jsonify the request to handle it easily.
            newQuestion = request.get_json()
            question = Question(
                  question=question,
                  answer=answer,
                  difficulty=difficulty,
                  category=category
            )
            # creating the question in the database.
            question.insert()

            return jsonify({
                'success': True,
              }), 201
        except Exception:
            abort(422)
    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question. /Done

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start. /Done
    '''
    @app.route('/questions/search', methods=["POST"])
    def questions_search():
        try:
            # jsonify the request to handle it easily.
            searchTerm = request.get_json()['searchTerm']
            selection = Question.query.filter(
              Question.question.ilike(f'%{searchTerm}%')).all()
            current_questions = paginate_questions(request, selection)
            categories = Category.query.all()
            data = {}
            # formating the categories into
            #  dictionary to be accepted in the front end
            for category in categories:
                data[category.id] = category.type
            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'categories': data,
                'current_category': 'all'
              }), 200

        except Exception:
            abort(404)
    '''
    @TODO:
    Create a GET endpoint to get questions based on category. / Done

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.  /Done
    '''
    @app.route('/categories/<int:category_id>/questions', methods=["GET"])
    def categories_and_the_questions(category_id):
        try:
            selected = Question.query.filter_by(category=category_id).all()
            category = Category.query.get(category_id)
            questions = paginate_questions(request, selected)
            return jsonify({
              'success': True,
              'questions': questions,
              'total_questions': len(questions),
              'current_category': category.type
              }), 200
        except Exception:
            abort(422)
    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.  /Done

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. /Done
    '''
    @app.route('/quizzes', methods=["POST"])
    def play_quizzes():
        try:
            # jsonify the request to handele it easily
            data = request.get_json()
            previous_questions = data['previous_questions']
            quiz_category = data['quiz_category']
            # if there is no categories or previous questions rase an error
            if ((quiz_category is None) or (previous_questions is None)):
                abort(400)
            if quiz_category['id'] == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter_by(
                    category=quiz_category['id']).all()
            current_question = questions[
              random.randint(0, len(questions) - 1)].format()
            # cheking term to be used in the cheking loop
            is_it_new = True
            # cheking if the question is in the
            # previous questions and assign a new one.
            while is_it_new:
                if current_question in previous_questions:
                    current_question = questions[
                      random.randint(0, len(questions) - 1)].format()
                else:
                    is_it_new = False
            return jsonify({
                'success': True,
                'question': current_question
              }), 200
        except Exception:
            abort(400)

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422. /Done
    '''
    # all the errors that are used in the backend.
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request error'
        }), 400

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
          'success': False,
          'error': 404,
          'message': 'Resource not found'
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
          'success': False,
          'error': 500,
          'message': 'Internal error, please try again.'
        }), 500

    @app.errorhandler(422)
    def uncrossable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Uncrossable entity'
        }), 422
    return app
