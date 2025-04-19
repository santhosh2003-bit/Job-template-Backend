from app.server import app
from app.routes.route import api_routes
from app.auth.routes import auth_routes

app.register_blueprint(auth_routes, url_prefix="/auth")
app.register_blueprint(api_routes)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render’s PORT env
    app.run(host="0.0.0.0", port=port)        # Bind to all interfaces
