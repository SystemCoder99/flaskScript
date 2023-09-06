from flask import jsonify, Flask, request
from flask_cors import CORS
import uuid

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

BOOKS = [
    {
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'title': 'The Lightning Thief',
        'author': 'Rick Riordan',
        'read': False
    },
    {
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

booklist = [
    {
        'id': uuid.uuid4().hex,
        'FolderPath': 'Books/Destiny Lore',
        'Title': 'Volume_I_Dark_Mirror.epub',
        'tags': 'destiny, fiction'
    },
    {
        'id': uuid.uuid4().hex,
        'FolderPath': 'Books/Destiny Lore',
        'Title': 'Volume_II.epub',
        'tags': "destiny, fiction"
    }
]


def remove_book(book_id):
    for book in booklist:
        if book['id'] == book_id:
            booklist.remove(book)
            return True
    return False


# sanity check route
@app.route("/ping", methods=["GET"])
def ping_pong():
    return jsonify("Pong!")


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        booklist.append({
            'id': uuid.uuid4().hex,
            'FolderPath': post_data.get('FolderPath'),
            'Title': post_data.get('Title'),
            'tags': post_data.get('tags')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = booklist
    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        booklist.append({
            'id': uuid.uuid4().hex,
            'FolderPath': post_data.get('FolderPath'),
            'Title': post_data.get('Title'),
            'tags': post_data.get('tags')
        })
        response_object['message'] = 'Book updated!'
    return jsonify(response_object)





if __name__ == "__main__":
    app.run()
