from sympy import diff, integrate, simplify


def parse_derivative(data):
    try:
        func = data["function"]
        for d in data["order"]:
            func = diff(func, d)
        res = {'type': 'success',
               'mode': 'derivative',
               'result': str(func.doit())}
    except ValueError as e:
        res = {'type': 'error',
               'mode': 'derivative',
               'result': str(e)}
    return res


def parse_indef_integral(data):
    try:
        res = {'type': 'success',
               'mode': 'indef_integral',
               'result': str(integrate(data["function"],
                                       data["variables"])
                             .doit())}
    except ValueError as e:
        res = {'type': 'error',
               'mode': 'indef_integral',
               'result': str(e)}
    return res


def parse_def_integral(data):
    try:
        res = {'type': 'success',
               'mode': 'def_integral',
               'result': str(integrate(data["function"], (data["variables"][0],
                                                          data["interval"][0],
                                                          data["interval"][1]))
                             .doit())}
    except ValueError as e:
        res = {'type': 'error',
               'mode': 'def_integral',
               'result': str(e)}
    return res


def parse_simplify(data):
    try:
        res = {
               'type': 'success',
               'mode': 'simplify',  # or any other mode from request
               'result': str(simplify(data["expression"], doit=True))
              }
    except ValueError as e:
        res = {'type': 'error',
               'mode': 'simplify',
               'result': str(e)}
    return res


def parse_request(data):
    try:
        if data['mode'] == 'derivative':
            result = parse_derivative(data)
        elif data['mode'] == 'indef_integral':
            result = parse_indef_integral(data)
        elif data['mode'] == 'def_integral':
            result = parse_def_integral(data)
        elif data['mode'] == 'simplify':
            result = parse_simplify(data)
        else:
            result = {'type': 'error',
                      'mode': data['mode'],
                      'result': 'Unknown mode'}
    except Exception as e:
        result = {'type': 'error',
                  'mode': data['mode'],
                  'result': str(e)}
    return result
