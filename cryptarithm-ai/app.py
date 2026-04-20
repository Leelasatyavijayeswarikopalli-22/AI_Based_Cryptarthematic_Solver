from flask import Flask, render_template, request, jsonify
import itertools

app = Flask(__name__, template_folder="templates", static_folder="static")

def solve_cryptarithm(words, result):
   letters = sorted(set("".join(words) + result))
   steps = []

   for i, perm in enumerate(itertools.permutations(range(10), len(letters))):

     mapping = dict(zip(letters, perm))

     if i < 200000 and i % 20000 == 0:
        steps.append(f"Trying #{i}: {mapping}")

     if any(mapping[w[0]] == 0 for w in words + [result]):
        continue

     def word_to_num(word):
        return int("".join(str(mapping[c]) for c in word))

     if sum(word_to_num(w) for w in words) == word_to_num(result):
        steps.append("Solution found 🎉")
        return {"solution": mapping, "steps": steps}

   steps.append("No solution found")
   return {"solution": None, "steps": steps}

@app.route("/")
def index():
    print("INDEX HIT")
    return render_template("index.html")


@app.route("/solve", methods=["POST"])
def solve():
    data = request.get_json(force=True, silent=True)
    if not data:
     return jsonify({"error": "Invalid JSON"}), 400
    if not data:
     return jsonify({"error": "Invalid JSON"}), 400 

    words = data.get("words", [])
    result = data.get("result", "")

    # 🔴 Validation 1: empty check
    if not words or not result:
        return jsonify({"error": "Words or result missing"}), 400

    # 🔴 Validation 2: only alphabets allowed
    for w in words + [result]:
        if not w.isalpha():
            return jsonify({"error": "Only alphabets allowed"}), 400

    # 🔴 Validation 3: duplicates
    if len(words) != len(set(words)):
        return jsonify({"error": "Duplicate words not allowed"}), 400

    solution = solve_cryptarithm(words, result)
    return jsonify(solution)

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True, port=8000)