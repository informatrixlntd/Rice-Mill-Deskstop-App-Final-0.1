from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import init_db, get_next_bill_no
from routes.slips import slips_bp
from routes.auth import auth_bp

app = Flask(__name__,
            static_folder='../frontend/static',
            template_folder='templates')

CORS(app)

app.register_blueprint(slips_bp)
app.register_blueprint(auth_bp)

init_db()

@app.route('/')
def index():
    """Serve the main form page"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/reports')
def reports():
    """Serve the reports page"""
    return send_from_directory('../frontend', 'reports.html')

@app.route('/api/next-bill-no')
def next_bill_no_route():
    """Get next bill number"""
    return jsonify({'bill_no': get_next_bill_no()})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌾 RICE MILL PURCHASE SLIP MANAGER")
    print("="*60)
    print("\n✅ Server starting...")
    print("📍 Open your browser and go to: http://127.0.0.1:5000")
    print("\n💡 Press CTRL+C to stop the server\n")
    app.run(debug=True, host='127.0.0.1', port=5000)
