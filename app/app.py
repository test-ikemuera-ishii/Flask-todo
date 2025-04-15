from flask import Flask,request,jsonify,render_template

app = Flask(__name__)

@app.route('/')
def index01():
    return 'Hello World'

@app.route('/test')
def test():
    return 'Hello test'

@app.route("/post-message",methods=['POST'])
def post_message():
    name = request.form.get("name")
    message = request.form.get("message")
    return f"{name}からのメッセージを受け取りました。内容：{message}"

@app.route("/json-api",methods=["POST"])
def json_api():
    data = request.get_json()

    if not data:
        return  jsonify({"error":"JSONが送られていません"}),400
    
    name = data.get("name","")
    age  = data.get("age",0)

    response = {
        "received_name": name,
        "received_age": age,
        "message": f"{name}は {age} 歳だ"
    }

    return jsonify(response),200

@app.route("/html",methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

