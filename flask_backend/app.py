from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)  # Allow front-end to comunicate with back-end

# Configuration of SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) # Database instance

# Define Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Create database tables
with app.app_context(): # Create tables only if they don't exist
    db.create_all()

# API Routes
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all() # Get all tasks from database
    return jsonify([{'id':task.id, 'title':task.title, 'completed':task.completed} for task in tasks])

@app.route('/tasks', methods=['POST'])
def add_tasks():
    data = request.json
    new_task = Task(title=data['title'], completed=False)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added successfully"}) # Return a message

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = not task.completed # Toggle task status
        db.session.commit()
        return jsonify({"message": "Task updated successfully"})
    return jsonify({"message": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully"})
    return jsonify({"message": "Task not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)