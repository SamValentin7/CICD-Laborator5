from flask import Flask, render_template, request, redirect, url_for
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Flask configuration from environment
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['DEBUG'] = os.environ.get('DEBUG', 'True').lower() == 'true'

# Database configuration from environment
DB_HOST = os.environ.get('DB_HOST', 'cicd5-db')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'messages_db')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
DB_SSL_MODE = os.environ.get('DB_SSL_MODE', 'disable')

def get_db_connection():
    """Create database connection"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            sslmode=DB_SSL_MODE
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        print(f"Connection details: host={DB_HOST}, port={DB_PORT}, db={DB_NAME}, user={DB_USER}")
        return None

def init_database():
    """Initialize database with messages table"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                        id SERIAL PRIMARY KEY,
                        content TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                conn.commit()
                print("Database initialized successfully")
        except Exception as e:
            print(f"Database initialization error: {e}")
        finally:
            conn.close()

@app.route('/')
def index():
    """Display all messages"""
    conn = get_db_connection()
    messages = []
    
    if conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM messages ORDER BY created_at DESC")
                messages = cur.fetchall()
        except Exception as e:
            print(f"Error fetching messages: {e}")
        finally:
            conn.close()
    
    return render_template('index.html', messages=messages)

@app.route('/add', methods=['POST'])
def add_message():
    """Add a new message"""
    content = request.form.get('content', '').strip()
    
    if content:
        conn = get_db_connection()
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO messages (content) VALUES (%s)", (content,))
                    conn.commit()
            except Exception as e:
                print(f"Error adding message: {e}")
            finally:
                conn.close()
    
    return redirect(url_for('index'))

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'service': 'cicd5 Flask App'}

if __name__ == '__main__':
    # Initialize database on startup
    init_database()
    
    # Run Flask application
    app.run(host='0.0.0.0', port=5000, debug=True)