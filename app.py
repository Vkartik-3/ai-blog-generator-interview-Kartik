from flask import Flask

print(f"__name__ is: {__name__}")
app = Flask(__name__)
print(f"Flask app name is: {app.name}")

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == "__main__":
    print("Starting server because __name__ == '__main__'")
    app.run(debug=True)
else:
    print("File was imported, not starting server")