import json
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data.json"

Abhilasha = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "flask_app")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "submissions")


def get_collection():
    """Create the Mongo client lazily so connection errors surface at submit time."""
    if not MONGO_URI:
        raise RuntimeError("MONGO_URI is not set. Add it to your .env file.")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    return client[DB_NAME][COLLECTION_NAME]


# ---------- Task 1: JSON API route ----------
@Abhilasha.route("/api")
def api():
    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)


# ---------- Task 2: Form + MongoDB Atlas ----------
@Abhilasha.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email:
            return render_template(
                "form.html", error="Name and email are required.", values=request.form
            )

        try:
            get_collection().insert_one(
                {"name": name, "email": email, "message": message}
            )
        except (PyMongoError, RuntimeError) as e:
            # Error: stay on the same page, no redirect
            return render_template("form.html", error=str(e), values=request.form)

        # Success: redirect to another page
        return redirect(url_for("success"))

    return render_template("form.html", error=None, values={})


@Abhilasha.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    Abhilasha.run(debug=True)
