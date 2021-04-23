from sympy import symbols, diff, integrate


def parse_derivative(data):
    func = data["function"]
    for d in data["order"]:
        func = diff(func, d)
    return {'type': 'success',
            'mode': 'derivative',
            'result': str(func.doit())}


def parse_indef_integral(data):
    return {'type': 'success',
            'mode': 'indef_integral',
            'result': str(integrate(data["function"], data["variables"]).doit())}


def parse_def_integral(data):
    return {'type': 'success',
            'mode': 'indef_integral',
            'result': str(integrate(data["function"], (data["variables"][0],
                                                       data["interval"][0],
                                                       data["interval"][1])).doit())}


def parse_simplify(data):
    return None


def parse_fs(data):
    return None


def parse_request(data):
    result = ""
    if data['mode'] == 'derivative':
        result = parse_derivative(data)
    elif data['mode'] == 'indef_integral':
        result = parse_indef_integral(data)
    elif data['mode'] == 'def_integral':
        result = parse_def_integral(data)
    elif data['mode'] == 'simplify':
        result = parse_simplify(data)
    elif data['mode'] == 'fourier_series':
        result = parse_fs(data)
    else:
        result = {'type': 'error',
                  'mode': data['mode'],
                  'description': 'Unknown mode'}
    return result

