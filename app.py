from startup import create_app
from flask_openapi3 import OpenAPI

app: OpenAPI = create_app()

if __name__ == "__main__":
    app.run(debug=True)