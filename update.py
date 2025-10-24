from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_connection, close_connection

update_bp = Blueprint('update', __name__)

@update_bp.route('/edit/<int:record_id>', methods=['GET', 'POST'])
def edit_record(record_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        description = request.form.get('description', '')
        status = request.form.get('status', 'active')
        
        try:
            # Update record in database
            cursor.execute("""
                UPDATE records 
                SET name = %s, email = %s, phone = %s, description = %s, status = %s, updated_at = CURRENT_TIMESTAMP 
                WHERE id = %s
            """, (name, email, phone, description, status, record_id))
            
            connection.commit()
            flash('Record updated successfully!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            connection.rollback()
            flash(f'Error updating record: {str(e)}', 'error')
            
        finally:
            cursor.close()
            close_connection(connection)
    
    else:
        # GET request - fetch record data
        try:
            cursor.execute("SELECT * FROM records WHERE id = %s", (record_id,))
            record = cursor.fetchone()
            
            if not record:
                flash('Record not found!', 'error')
                return redirect(url_for('index'))
            
            return render_template('update.html', record=record)
            
        except Exception as e:
            flash(f'Error fetching record: {str(e)}', 'error')
            return redirect(url_for('index'))
            
        finally:
            cursor.close()
            close_connection(connection)