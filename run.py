from app.server import app
from app.routes.route import api_routes
from app.auth.routes import auth_routes

app.register_blueprint(auth_routes, url_prefix="/auth")
app.register_blueprint(api_routes)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3012, debug=False)