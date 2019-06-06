from app import my_app, Base, engine

def start_app():
    # Base.metadata.create_all(engine)
    my_app.run()

if __name__ == "__main__":
    start_app()
