from flask import Flask

# Initialize Flask app
app = Flask(__name__)

# Register the blueprints
from register import register_bp
from login import login_bp
from homepage import homepage_bp
from logout import logout_bp
from admin import admin_bp 

app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(homepage_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(admin_bp) 

if __name__ == "__main__":
    app.run(debug=True)
