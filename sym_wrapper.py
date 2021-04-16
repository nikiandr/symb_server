from sympy import symbols, diff, integrate


# json_try = {
#     'mode': 'derivative',
#     'variables': ['x'],
#     'function': 'x**2',
#     'order': ['x']  # 'order': ['x', 'x']
# }
# print(json.loads(json.dumps(json_try)))


def parse_derivative(data):
    func = data["function"]
    for d in data["order"]:
        func = diff(func, d)
    return str(func.doit())


def parse_indef_integral(data):
    return None


def parse_def_integral(data):
    return None


def parse_simplify(data):
    return None


def parse_fs(data):
    return None


def parse_req(data):
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
        result = "Error"
    return result
