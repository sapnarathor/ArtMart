from flask import Flask, render_template, redirect, url_for, session, request

app = Flask(__name__)

# Required for Flask session
app.secret_key = "artmart-demo-secret-key"


# =========================================================
# ARTWORK DATA
# =========================================================

artworks = [
    {
        "id": 1,
        "image": "sunset.png",
        "name": "Sunset Dreams",
        "artist": "Riya Rathor",
        "price": 4500,
        "category": "Landscape",
        "description": "A beautiful sunset inspired artwork."
    },
    {
        "id": 2,
        "image": "rainy-street.png",
        "name": "Rainy Street",
        "artist": "Meera Sharma",
        "price": 3200,
        "category": "Landscape",
        "description": "A peaceful rainy street painting."
    },
    {
        "id": 3,
        "image": "royal-beauty.png",
        "name": "Royal Beauty",
        "artist": "Aarav Patel",
        "price": 4000,
        "category": "Abstract",
        "description": "A modern abstract artwork."
    },
    {
        "id": 4,
        "image": "nature-love.png",
        "name": "Nature Love",
        "artist": "Rohan Verma",
        "price": 2800,
        "category": "Nature",
        "description": "An artwork inspired by nature."
    }
]


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        artworks=artworks
    )


# =========================================================
# ALL ARTWORKS
# =========================================================

@app.route("/artworks")
def artworks_page():

    return render_template(
        "artworks.html",
        artworks=artworks
    )


# =========================================================
# ARTWORK DETAILS
# =========================================================

@app.route("/artwork/<int:artwork_id>")
def artwork_details(artwork_id):

    artwork = None

    for item in artworks:

        if item["id"] == artwork_id:
            artwork = item
            break

    if artwork is None:
        return "Artwork not found", 404

    return render_template(
        "artwork.html",
        artwork=artwork
    )


# =========================================================
# ARTISTS
# =========================================================

@app.route("/artists")
def artists():

    return render_template("artists.html")


# =========================================================
# ADD TO CART
# =========================================================

@app.route("/add-to-cart/<int:artwork_id>")
def add_to_cart(artwork_id):

    # Check that artwork exists
    artwork_exists = False

    for artwork in artworks:

        if artwork["id"] == artwork_id:
            artwork_exists = True
            break

    if not artwork_exists:
        return "Artwork not found", 404


    # Get existing cart
    cart = session.get("cart", [])


    # Add artwork
    cart.append(artwork_id)


    # Save cart
    session["cart"] = cart


    # Make sure Flask saves session
    session.modified = True


    # Go to cart
    return redirect(url_for("cart"))


# =========================================================
# CART
# =========================================================

@app.route("/cart")
def cart():

    cart_ids = session.get("cart", [])

    cart_items = [
        artwork
        for artwork in artworks
        if artwork["id"] in cart_ids
    ]

    total = sum(
        artwork["price"]
        for artwork in cart_items
    )

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total
    )


# =========================================================
# REMOVE FROM CART
# =========================================================

@app.route("/remove-from-cart/<int:artwork_id>")
def remove_from_cart(artwork_id):

    cart = session.get("cart", [])


    if artwork_id in cart:

        cart.remove(artwork_id)


    session["cart"] = cart

    session.modified = True


    return redirect(url_for("cart"))


# =========================================================
# CHECKOUT
# =========================================================

@app.route("/checkout", methods=["GET", "POST"])
def checkout():

    if request.method == "POST":

        # Clear cart after demo order
        session["cart"] = []

        session.modified = True

        return redirect(url_for("success"))


    return render_template("checkout.html")


# =========================================================
# ORDER SUCCESS
# =========================================================

@app.route("/success")
def success():

    return render_template("success.html")


# =========================================================
# CONTACT
# =========================================================

@app.route("/contact", methods=["GET", "POST"])
def contact():

    message_sent = False


    if request.method == "POST":

        message_sent = True


    return render_template(
        "contact.html",
        message_sent=message_sent
    )


# =========================================================
# ABOUT
# =========================================================

@app.route("/about")
def about():

    return render_template("about.html")


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    return {
        "status": "healthy",
        "application": "ArtMart"
    }


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )