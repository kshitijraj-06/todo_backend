from flask import Blueprint, request, jsonify

import app
from .models import Todo
from .extensions import db
from datetime import datetime

api = Blueprint('api', __name__)

@api.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])


@api.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    return jsonify(todo.to_dict())


@api.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()

    # Validate required fields
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400

    # Create new todo
    new_todo = Todo(
        title=data['title'],
        description=data.get('description', ''),
        completed=data.get('completed', False),
        due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None
    )

    db.session.add(new_todo)
    db.session.commit()

    return jsonify(new_todo.to_dict()), 201


@api.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    data = request.get_json()

    # Update fields
    if 'title' in data:
        todo.title = data['title']
    if 'description' in data:
        todo.description = data['description']
    if 'completed' in data:
        todo.completed = data['completed']
    if 'due_date' in data:
        todo.due_date = datetime.fromisoformat(data['due_date']) if data['due_date'] else None

    db.session.commit()

    return jsonify(todo.to_dict())


@api.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'}), 200

@api.route('/')
def home():
    return "Todo API is running", 200

@api.route('/todos/<int:todo_id>/complete', methods=['PUT'])
def complete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.completed = True
    db.session.commit()
    return jsonify(todo.to_dict())


@api.route('/todos/<int:todo_id>/uncomplete', methods=['PUT'])
def uncomplete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.completed = False
    db.session.commit()
    return jsonify(todo.to_dict())