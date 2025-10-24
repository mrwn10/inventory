from flask import Blueprint, redirect, url_for
from database import get_connection, close_connection

delete_bp = Blueprint('delete', __name__)

@delete_bp.route('/delete/<int:record_id>')
def delete_record(record_id):
    """Delete a record by ID"""
    conn = get_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM records WHERE id = %s", (record_id,))
        conn.commit()
        
        # Redirect back to home page with success message
        return redirect(url_for('read.index'))
        
    except Exception as e:
        return f"Error deleting record: {str(e)}", 500
    finally:
        if cursor:
            close_connection(conn, cursor)