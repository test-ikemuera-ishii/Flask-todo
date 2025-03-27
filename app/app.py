from flask import Flask, request, jsonify
import MySQLdb
import os

app = Flask(__name__)

# MySQLの設定
db = MySQLdb.connect(
    host="db",
    user="user",
    passwd="password",
    db="todo_db",
    charset="utf8"
)
cursor = db.cursor()

# タスクを取得するエンドポイント
@app.route("/tasks", methods=["GET"])
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return jsonify(tasks)

# タスクを追加するエンドポイント
@app.route("/task", methods=["POST"])
def add_task():
    data = request.get_json()
    cursor.execute("INSERT INTO tasks (task_name, due_date) VALUES (%s, %s)", (data["task_name"], data["due_date"]))
    db.commit()
    return jsonify({"message": "Task added!"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

