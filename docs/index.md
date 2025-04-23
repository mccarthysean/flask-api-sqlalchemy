# flask-api-sqlalchemy

A Flask extension that automatically generates RESTful APIs from SQLAlchemy models.

<p align="center">
<a href="https://github.com/mccarthysean/flask-api-sqlalchemy/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/mccarthysean/flask-api-sqlalchemy/workflows/Test/badge.svg" alt="Test">
</a>
<a href="https://codecov.io/gh/mccarthysean/flask-api-sqlalchemy" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/mccarthysean/flask-api-sqlalchemy?color=%2334D058" alt="Coverage">
</a>
<a href="https://github.com/mccarthysean/flask-api-sqlalchemy/actions?query=workflow%3Apypi" target="_blank">
    <img src="https://github.com/mccarthysean/flask-api-sqlalchemy/workflows/Upload%20Package%20to%20PyPI/badge.svg" alt="Publish">
</a>
<a href="https://pypi.org/project/flask-api-sqlalchemy" target="_blank">
    <img src="https://img.shields.io/pypi/v/flask-api-sqlalchemy?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/flask-api-sqlalchemy/" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/flask-api-sqlalchemy.svg" alt="Python Versions">
</a>
</p>


## Features

- Simple integration with existing Flask and SQLAlchemy applications
- Automatic discovery of SQLAlchemy models
- Automatic mapping of SQLAlchemy types to Flask-RESTX API model types
- Fully generated REST endpoints for all models
- Comprehensive test suite

## Installation for Your Project

[Install from PyPI](https://pypi.org/project/flask-api-sqlalchemy/)

```bash
pip install flask-api-sqlalchemy
```

## Installation for Development

```bash
pip install -e .

## Usage

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_api import Api

# Create Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define your SQLAlchemy models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Initialize the API extension
api = Api()
api.init_app(app, db)

if __name__ == '__main__':
    app.run()
```

That's it! The extension automatically:
1. Discovers all your SQLAlchemy models
2. Creates appropriate Flask-RESTX models and serializers
3. Generates full CRUD API endpoints for each model
4. Provides Swagger documentation at `/api/docs`

# LICENSE

MIT License

Copyright (c) 2025 Sean McCarthy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Author Info

Sean McCarthy is Chief Data Scientist at [IJACK Technologies Inc](https://myijack.com), a leading manufacturer of fully-automated pumps to green the oil and gas industry.

<br>
<a href="https://mccarthysean.dev">
    <img src="https://raw.githubusercontent.com/mccarthysean/flask-api-sqlalchemy/main/docs/assets/mccarthysean.svg?sanitize=1" alt="Sean McCarthy's blog">
</a>
<a href="https://www.linkedin.com/in/seanmccarthy2/">
    <img src="https://raw.githubusercontent.com/mccarthysean/flask-api-sqlalchemy/main/docs/assets/linkedin.svg?sanitize=1" alt="LinkedIn">
</a>
<a href="https://github.com/mccarthysean">
    <img src="https://raw.githubusercontent.com/mccarthysean/flask-api-sqlalchemy/main/docs/assets/github.svg?sanitize=1" alt="GitHub">
</a>
<a href="https://twitter.com/mccarthysean">
    <img src="https://raw.githubusercontent.com/mccarthysean/flask-api-sqlalchemy/main/docs/assets/twitter.svg?sanitize=1" alt="Twitter">
</a>
<a href="https://www.facebook.com/sean.mccarth">
    <img src="https://raw.githubusercontent.com/mccarthysean/flask-api-sqlalchemy/main/docs/assets/facebook.svg?sanitize=1" alt="Facebook">
</a>
<a href="https://medium.com/@mccarthysean">
    <img src="https://raw.githubusercontent.com/mccarthysean/flask-api-sqlalchemy/main/docs/assets/medium.svg?sanitize=1" alt="Medium">
</a>
<a href="https://www.instagram.com/mccarthysean/">
    <img src="https://raw.githubusercontent.com/mccarthysean/flask-api-sqlalchemy/main/docs/assets/instagram.svg?sanitize=1" alt="Instagram">
</a>
