from flask import Flask, jsonify, render_template
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
def index():
    return render_template("index.html")

@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)

@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/cancelled")
def cancelled():
    return render_template("cancelled.html")

@app.route("/create-checkout-session")
def create_checkout_session():
    domain_url = "http://127.0.0.1:5000/"
    stripe.api_key = stripe_keys["secret_key"]

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [payment_intent_data] - capture the payment later
        # [customer_email] - prefill the email input in the form
        # For full details see https://stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancelled",
            payment_method_types=["card"],
            mode="payment",
            # line_items=[
            #     {
            #         "name": "Test item",
            #         "quantity": 1,
            #         "currency": "usd",
            #         "amount": "2000",
            #     }
            # ],        #stripe has updated to put everything in price_data which is in line_items
            line_items=[{
                  "price_data": {
                    "currency": "usd",
                    "unit_amount": 500,
                    "product_data": {
                      "name": "name of the product",
                    },
                  },
                  "quantity": 1,
                }
              ]
        )
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e)), 403

if __name__ == "__main__":
    app.run()