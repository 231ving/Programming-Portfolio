import flask
import os
import argparse

app = flask.Flask(__name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(ROOT_DIR, 'public')
print(PUBLIC_DIR)


def handle_template(filename):
    # Set default parameters
    parameters = {
        'max_guesses': 6,
        'answer': 'silver',
        'guesses': 'studio,flange,sliver,silver'
    }

    # Override the defaults with any values from the query string
    parameters.update(flask.request.args)

    # Turn the string of guesses into a list
    parameters['guesses'] = parameters['guesses'].split(',')

    # Turn the max guess into a usable int
    parameters['max_guesses'] = int(parameters['max_guesses'])

    # Turn all guesses in the list to lowercase
    temp_guess = []
    for i in parameters['guesses']:
        temp_guess.append(i.upper())
    parameters['guesses'] = temp_guess

    parameters['answer'] = parameters['answer'].upper()

    letter_map = {}
    max_guess = parameters['max_guesses']
    answer = parameters['answer']
    guess_results = []
    if len(temp_guess) <= max_guess:
        for guess in range(0, len(temp_guess)):
            if len(temp_guess[guess]) == len(answer):
                for j in range(0, len(answer)):
                    if temp_guess[guess][j] == answer[j]:
                        letter_map.update({f"{temp_guess[guess][j]}": 'correct'})
                        guess_results.append([f'{temp_guess[guess][j]}', 'correct'])
                    elif temp_guess[guess][j] in answer:
                        if temp_guess[guess][j] in letter_map:
                            if letter_map[temp_guess[guess][j]] != 'correct':
                                letter_map.update({f"{temp_guess[guess][j]}": 'almost'})
                        else:
                            letter_map.update({f"{temp_guess[guess][j]}": 'almost'})
                        guess_results.append([f'{temp_guess[guess][j]}', 'almost'])
                    elif temp_guess[guess][j] not in letter_map:
                        letter_map.update({f"{temp_guess[guess][j]}": 'miss'})
                        guess_results.append([f'{temp_guess[guess][j]}', 'miss'])
                    else:
                        guess_results.append([f'{temp_guess[guess][j]}', 'miss'])

    parameters['letter_map'] = letter_map
    parameters['guess_results'] = guess_results

    return flask.render_template(f"{filename}.j2", **parameters)


@app.route('/<path:filename>')
def serve_files_and_templates(filename):
    # if the route does not contain an extension (i.e., a '.')
    # assume it is a template. Otherwise, just serve it as a 
    # static file.
    if '.' not in filename:
        return handle_template(filename)
    else:
        return flask.send_from_directory(PUBLIC_DIR, filename)


@app.route('/')
def root_route():
    return "No root route defined."


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a Flask server to serve files from the public directory.')
    parser.add_argument('--port', '-p', type=int, default=5000, help='Port to run the server on (default: 5000)')
    args = parser.parse_args()

    app.run(debug=True, port=args.port)
