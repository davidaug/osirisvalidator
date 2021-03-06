# OSIRIS VALIDATOR

Osiris Validator is a set of decorators for validation with SQLAlchemy

(Readme is under construction...)

## Getting Started

### Installing

```
pip install osirisvalidator
```

### Usage

To use the decorators, the **validates()** decorator from SQLAlchemy must be used before, and the pattern must be followed.

The parameter "field" is mandatory and you can set a custom message.
```python
from sqlalchemy.orm import validates
from osirisvalidator.string import *
from osirisvalidator.internet import valid_email

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(60), nullable=False)

    @validates('name')
    @not_blank(field='name', message='Custom message')
    @is_alpha_space(field='name')
    @string_len(field='name', min=3, max=100)
    def validate_name(self, key, name):
        return name

    @validates('email')
    @not_blank(field='email')
    @valid_email(field='email')
    def validate_email(self, key, email):
        return email

``` 
When a validation error occurs, a **ValidationException** is thrown.

#### Flask example

Full example in: https://github.com/davidaug/osirisvalidator-flask-example

```python
@app.route('api/User', methods=['POST'])
def saveuser():
    try:
        user = User()
        user.name = request.form['name']
        user.email = request.form['email']
        db.session.add(user)
        db.session.commit()
    except ValidationException as ve:
        return jsonify({"status": 400, "message": "Validation error!", "errors": ve.errors}), 400

    return jsonify(user)
```


#### Flask-restless example
The parameter *validation_exceptions* in **APIManager.create_api()**  from Flask-restless must be set to use osiris' **ValidationException**.

```python
from osirisvalidator.exceptions import ValidationException

[...]

manager = APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(User, validation_exceptions=[ValidationException], methods=['GET', 'POST'])
```

See about in: https://flask-restless.readthedocs.io/en/stable/customizing.html#capturing-validation-errors

## List of validators

### osirisvalidator.string
- not_empty
- not_blank
- is_alpha
- is_alpha_space (alpha characters and space)
- is_alnum
- is_alnum_space (alphanumeric characters and space)
- is_digit
- string_len (mandatory parameters: **min** and **max**)
- match_regex (mandatory parameter: **regex**) 

### osirisvalidator.number
- min_max (mandatory parameters: **min** and **max**)
- not_null

### osirisvalidator.internet
- valid_email

## osiris.intl.br
- valid_cpf
- valid_cnpj
