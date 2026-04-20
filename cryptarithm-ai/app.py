from flask import Flask, render_template, request, jsonify
import itertools

app = Flask(__name__, template_folder="templates", static_folder="static")

def solve_cryptarithm(words, result):
    letters = set("".join(words) + result)
    letters = list(letters)

    if len(letters) > 10:
        return None

    digits = range(10)

    for perm in itertools.permutations(digits, len(letters)):
        mapping = dict(zip(letters, perm))

        # leading letters cannot be zero
        if any(mapping[word[0]] == 0 for word in words + [result]):
            continue

        def word_to_num(word):
            return int("".join(str(mapping[c]) for c in word))

        if sum(word_to_num(w) for w in words) == word_to_num(result):
            return mapping

    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/solve", methods=["POST"])
def solve():
    data = request.json
    words = data["words"]
    result = data["result"]

    solution = solve_cryptarithm(words, result)

    return jsonify(solution)


if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True,port=8000)