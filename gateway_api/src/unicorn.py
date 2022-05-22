from app import create_app, socketio
app = create_app({})

if __name__ == "__main__":
    app = create_app({}).run(host="0.0.0.0", port=8080, debug=True)