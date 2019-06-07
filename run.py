from app import my_app, create_db

def start_app():
    create_db()
    my_app.run()

if __name__ == "__main__":
    start_app()
