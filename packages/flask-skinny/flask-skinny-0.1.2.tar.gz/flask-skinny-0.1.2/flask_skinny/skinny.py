import flask
import functools


def intent(intent_callable):
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            f(*args, **kwargs)
            return intent_callable(flask.request, **kwargs)

        return decorated_function

    return decorator


def responses(responses_dict):
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            intent_result = f(*args, **kwargs)
            if intent_result is None:
                if len(responses_dict) == 0:
                    flask.abort(500)
                status_code = list(responses_dict.keys())[0]
                outcome = None
                response_callable = responses_dict[status_code]
            else:
                status_code, outcome = intent_result
                response_callable = responses_dict.get(status_code, None)
                if response_callable is None:
                    flask.abort(status_code)
            headers, body = response_callable(flask.request, outcome)
            return flask.Response(body, status_code, headers)

        return decorated_function

    return decorator
