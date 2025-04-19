import mysql.connector
from flask import Flask,request,jsonify,render_template

app = Flask(__name__)
# 文字化けめ、、
app.config['JSON_AS_ASCII'] = False

# MySQLとのコネクションを作成する関数
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='user',
        password='password',
        database='todo_db'
    )
    return conn

# tasksテーブルにデータを挿入する関数
def insert_task(content, completed=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO tasks (content, completed) VALUES (%s, %s)"
    cursor.execute(sql, (content, completed))
    conn.commit()
    cursor.close()
    conn.close()

# クライアントからタスクを受け取る関数
@app.route('/add-task', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({"error": "contentが必要です"}), 400

    content = data['content']
    completed = data.get('completed', False)

    try:
        insert_task(content, completed)
        return jsonify({"status": "success", "message": "タスクを追加しました"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#タスク一覧取得関数
@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(tasks)

#タスク編集関数
@app.route('/edit-task/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    data = request.get_json()
    content = data.get("content")
    completed = data.get("completed", False)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET content=%s, completed=%s WHERE id=%s", (content, completed, task_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "タスクを更新しました"})

#タスク削除関数
@app.route('/delete-task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "タスクを削除しました"})






@app.route('/')
def index():
    return render_template("index.html")

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
def index01():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

