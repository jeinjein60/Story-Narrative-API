import os
from flask import Flask, render_template, request, jsonify
import cohere
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    try:
        data = request.get_json()
        race = data.get("race")
        cls = data.get("class")
        alignment = data.get("alignment")
        map_area = data.get("map")

        prompt = (
            f"The user is a {alignment} {race} {cls} beginning their adventure in the {map_area}."
            "Set the stage for the user: describe the location, the character's background, and the moment the journey begins. "
            "Make it vivid, immersive, and exciting. Finish the paragraph with a complete thought."
        )

        response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=350
        )

        generated_text = response.generations[0].text.strip()
        return jsonify({
            "current_scene": generated_text,
            "state_id": None
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

#route for user input, 300 toekns
@app.route("/action", methods=["POST"])
def take_action():
    try:
        data = request.get_json()
        user_input = data.get('user_input', '')
        prompt = f"User's action: {user_input}. Now, continue the story."
        response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=300
        )

        new_scene = response.generations[0].text.strip()
        return jsonify({'scene': new_scene})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
