from flask import Blueprint, render_template, jsonify
from database import get_connection, close_connection

read_bp = Blueprint('read', __name__)

@read_bp.route('/')
def index():
    """Display all records on the home page"""
    conn = get_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM records ORDER BY created_at DESC")
        records = cursor.fetchall()
        
        return render_template('index.html', records=records)
        
    except Exception as e:
        return f"Error: {str(e)}", 500
    finally:
        if cursor:
            close_connection(conn, cursor)

@read_bp.route('/api/record/<int:record_id>')
def get_record(record_id):
    """API endpoint to get record details for modal"""
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM records WHERE id = %s", (record_id,))
        record = cursor.fetchone()
        
        if not record:
            return jsonify({"error": "Record not found"}), 404
        
        # Convert datetime to string for JSON serialization
        if record.get('created_at'):
            record['created_at'] = record['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        if record.get('updated_at'):
            record['updated_at'] = record['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
            
        return jsonify(record)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            close_connection(conn, cursor)