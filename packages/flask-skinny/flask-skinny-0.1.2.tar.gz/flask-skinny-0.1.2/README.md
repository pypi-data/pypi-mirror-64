# flask-skinny

A Flask extension that forces extremely skinny controllers.

```python
@app.route("/dogs/<int:dog_id>", methods=["POST"])
@skinny.responses({200: responses.greet_dog, 400: responses.bad_request})
@skinny.intent(intents.greet_dog)
def greet_dog(dog_id):
    pass
```

## Description

This extension contains two decorators, `@skinny.intent` and `@skinny.responses`.

* `@skinny.intent(callable)`
    * `callable`: Receives `flask.request`, returns `status_code` and `outcome`.
* `@skinny.responses({status_code: callable, ...})`
    * `callable`: Receives `flask.request` and `outcome`, returns `headers` and `body`.

`@skinny.responses` will choose an appropriate response by `status_code`.

## Simple Usage

```python
from flask import Flask
from flask_skinny import skinny
from random import randint
import json


def intent(request):
    if randint(0, 1) == 0:
        status_code = 200
        outcome = "OK"
    else:
        status_code = 403
        outcome = "Forbidden"
    return status_code, outcome


def response(request, outcome):
    headers = {"content-type": "application/json"}
    body = json.dumps({"message": outcome}) + "\n"
    return headers, body


app = Flask(__name__)


@app.route("/", methods=["GET"])
@skinny.responses({200: response, 403: response})
@skinny.intent(intent)
def index():
    pass
```

## Detailed Usage

See [app.py](https://github.com/iwamot/flask-skinny/blob/master/app.py).

## Installation

`$ pip install flask-skinny`

## Contribution

Create new Pull Request.

## License

[MIT](https://opensource.org/licenses/MIT)
