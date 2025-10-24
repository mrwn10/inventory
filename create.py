from flask import Blueprint, render_template, request, redirect, url_for
from database import get_connection, close_connection

create_bp = Blueprint('create', __name__)

@create_bp.route('/create', methods=['GET'])
def create_form():
    """Display the create form"""
    return render_template('create.html')

@create_bp.route('/create', methods=['POST'])
def create_record():
    """Handle form submission to create a new record"""
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    description = request.form.get('description')
    
    if not name:
        return "Name is required", 400
    
    conn = get_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO records (name, email, phone, description) VALUES (%s, %s, %s, %s)",
            (name, email, phone, description)
        )
        conn.commit()
        
        return redirect(url_for('read.index'))
        
    except Exception as e:
        conn.rollback()
        return f"Error creating record: {str(e)}", 500
    finally:
        if cursor:
            close_connection(conn, cursor)