from flask import Flask, render_template
from read import read_bp
from create import create_bp
from update import update_bp
from delete import delete_bp
import secrets

app = Flask(__name__)

# Set secret key for sessions and flash messages
app.secret_key = secrets.token_hex(16)  # Secure random key

# Register all blueprints
app.register_blueprint(read_bp)
app.register_blueprint(create_bp)
app.register_blueprint(update_bp)
app.register_blueprint(delete_bp)

# Add index route if not in blueprints
@app.route('/')
def index():
    # You might want to redirect to your read blueprint or handle it there
    from read import get_all_records  # Import here to avoid circular imports
    records = get_all_records()
    return render_template('index.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)