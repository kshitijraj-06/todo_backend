from flask import Blueprint, render_template, jsonify, request
from app.models import User

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    return render_template('index.html')


@main_bp.route('/get_users')
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'email': u.email, 'name': u.name, 'picture': u.picture} for u in users])
