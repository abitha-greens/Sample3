
import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=API_KEY)


def generate_response(prompt):

    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.7
    )

    return response.choices[0].message.content


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    try:

        data = request.get_json()

        topic = data.get("topic", "").strip()
        audience = data.get("audience", "").strip()

        if not topic or not audience:
            return jsonify({"error": "Please enter all details."}), 400

        # Prompt 1

        prompt1 = f"""
        Create simple Instagram content about {topic}.
        Target audience: {audience}.
        """

        content = generate_response(prompt1)

        # Prompt 2

        prompt2 = f"""
        Create an attractive Instagram caption
        based on this content:

        {content}
        """

        caption = generate_response(prompt2)

        # Prompt 3

        prompt3 = f"""
        Generate 5 relevant Instagram hashtags
        based on this caption:

        {caption}
        """

        hashtags = generate_response(prompt3)

        return jsonify({

            "content": content,
            "caption": caption,
            "hashtags": hashtags

        })

    except Exception as e:

        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":

    app.run(debug=True)
