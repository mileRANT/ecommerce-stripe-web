from flask import Flask, jsonify
import os
import stripe

app = Flask(__name__)

# note that stripe keys have been added into the environment to keep them hidden
stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
}

stripe.api_key = stripe_keys["secret_key"]
@app.route("/hello")
def hello_world():
    return jsonify("hello, world!")

@app.route("/")
def home():
    return jsonify("hello, world!")


if __name__ == "__main__":
    app.run()