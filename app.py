from flask import Flask, request, send_file, jsonify
from bin.filters import apply_filter

app = Flask(__name__)

# Read the PIL document to find out which filters are available out-of the box
filters_available = [
    "blur",
    "cotour",
    "detail",
    "edge_enhance",
    "edge_enhance_more",
    "emboss",
    "find_edges",
    "sharpen",
    "smooth",
    "smooth_more"
]


@app.route("/", methods=["GET", "POST"])
def index():
    response = {
        "filters_available":filters_available,
        "usage":{"http_method":"POST", "URL":"/<filters_avaible>/"},
    }
    return jsonify(response)


@app.post("/<filter>")
def image_filter(filter):
    """
    TODO:
    1. Checks if the provided filter is available, if not, return an error
    2. Check if a file has been provided in the POST request, if not return an error
    3. Apply the filter using apply_filter() method from bin.filters
    4. Return the filtered image as response
    """

    if filter not in filters_available:
        response = {"error":"filter nor avaible"}
        return jsonify(response)
    
    file = request.files("image")
    if not file:
        response = {"error":"no file avaible"}
        return jsonify(response)
    
    filtered_image = apply_filter(file, filter)
    return send_file(filtered_image, minetype="image/JPEG")

if __name__ == "__main__":
    app.run()
    