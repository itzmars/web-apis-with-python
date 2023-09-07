# dictionary-api-python-flask/app.py
from flask import Flask, request, jsonify, render_template
from model.dbHandler import match_exact, match_like

app = Flask(__name__)


@app.get("/")
def index():
    """
    DEFAULT ROUTE
    This method will
    1. Provide usage instructions formatted as JSON
    """
    response = {"usage": "/dict?=<word>"}
    # Since this is a website with front-end, we don't need to send the usage instructions
    return render_template("index.html")


@app.get("/dict")
def dictionary():
    words = request.args.getlist("word")

    if not words:
        
        response = ({"status":"error","word":"words", "data": "word not fount"})
        return jsonify(response)
    
    response = {"words":[]}

    for word in words:
    
        definitions =  match_exact(word)

        if definitions:
            response["words"].append({"status":"success", "data":definitions, "word":word})
        else:    
        
            definitions = match_like(word)

            if definitions:
                response["words"].append({"status":"partial", "data":definitions,"word":word})
            else:
                response["words"].append({"status":"error", "data":"word not found", "word":word})

    return render_template("results.html", response=jsonify(response))

if __name__ == "__main__":
    app.run()
