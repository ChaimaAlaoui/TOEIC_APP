from app import create_app
from app.myRoutes import init_routes

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)