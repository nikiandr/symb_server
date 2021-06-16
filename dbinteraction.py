import sqlite3
import json


def db_connect(name: str = 'main.db') -> sqlite3.Connection:
    """
    Function to connect to auth database

    Args:
        name: database full name (with .db)
    Returns:
        sqlite3.Connection object - connection to DB
    """
    return sqlite3.connect(name)


def check_user_exists(db: sqlite3.Connection, nickname: str) -> bool:
    """
    Function to check if user already exists or not

    Args:
        db: sqlite3.Connection object - currently used database
        nickname: nickname of user

    Returns:
        boolean value - whether user already exists or not
    """
    cursor = db.cursor()
    for row in cursor.execute('select Count() from Users where Nickname = ?;', (nickname,)):
        result = bool(row[0])
    return result


def register(db: sqlite3.Connection, nickname: str, password: str):
    """
    Tries to register by adding new data to DB

    Args:
        db: sqlite3.Connection object - currently used database
        nickname: nickname of user
        password: password of user

    Returns:
        dictionary in CATP-compatible form
    """
    if check_user_exists(db, nickname):
        return {
            'type': 'registration_error',
            'result': 'User with this nickname already exists'
        }, 0
    else:
        cursor = db.cursor()
        cursor.execute('insert into Users(Nickname, Password) values (?, ?);', (nickname.strip(), password.strip()))
        db.commit()
        for row in cursor.execute('select Id from Users where Nickname = ? and Password = ?;',
                                  (nickname.strip(), password.strip())):
            user_id = int(row[0])
        return {'type': 'registration_success'}, user_id


def login(db: sqlite3.Connection, nickname: str, password: str):
    """
    Tries to login by adding new data to DB

    Args:
        db: sqlite3.Connection object - currently used database
        nickname: nickname of user
        password: password of user

    Returns:
        tuple of dictionary in CATP-compatible form and user ID
    """
    if not check_user_exists(db, nickname):
        return ({
            'type': 'login_error',
            'result': 'User with this nickname does not exist'
            }, 0)
    else:
        cursor = db.cursor()
        for row in cursor.execute('select Count() from Users where Nickname = ? and Password = ?;',
                                  (nickname.strip(), password.strip())):
            result = bool(row[0])
        if result:
            for row in cursor.execute('select Id from Users where Nickname = ? and Password = ?;',
                                      (nickname.strip(), password.strip())):
                user_id = int(row[0])
            return ({
                'type': 'login_success'
            }, user_id)
        else:
            return ({
                        'type': 'login_error',
                        'result': 'Wrong nickname or password.'
                }, 0)


def add_history(db: sqlite3.Connection, user_id: int, request: dict, response: dict):
    """
    Adds request/response session to history to DB.

    Args:
        db: Database sqlite3.Connection used
        user_id: Id of user - requester
        request: CATP-compatible dictionary with request by user
        response: CATP-compatible dictionary with response by server

    Returns:
        Nothing
    """
    cursor = db.cursor()
    if 'password' in request:
        request['password'] = request['password'].decode('ascii')
    cursor.execute('insert into History(Request, Response, UserId) values (?, ?, ?);',
                   (json.dumps(request), json.dumps(response), user_id))


def read_history(db: sqlite3.Connection, user_id: int) -> dict:
    """
    Read history for user with certain UserId

    Args:
        db: Database sqlite3.Connection used
        user_id: user_id: Id of user - requester

    Returns: CATP-compatible dictionary

    """
    any_history = bool()
    cursor = db.cursor()
    for row in cursor.execute('select Count() from History where UserId = ?;',
                              (user_id, )):
        any_history = bool(row[0])
    if any_history:
        nickname = str()
        query = cursor.execute('select Nickname from Users where Id = ?', (user_id, ))
        for row in query:
            nickname = str(row[0])
        histories = list()
        selection = cursor.execute('select Request, Response from History where UserId = ?', (user_id, ))
        for row in selection:
            histories.append(
                'User: ' + nickname + '\nRequest: ' + str(row[0]) + '\nResponse: ' + str(row[1])
            )
        return {
            'type': 'history_success',
            'history': histories
        }
    else:
        return {
            'type': 'history_error',
            'history': "History is empty"
        }


if __name__ == '__main__':
    conn = db_connect()
    print(register(conn, "nikiandr", "070801"))
    print(check_user_exists(conn, "nikiandr"))
    data, uid = login(conn, "nikiandr", "070801")
    print(data)
    add_history(conn, uid, {"1": 1}, {"2": 2})
    add_history(conn, uid, {"3": 3}, {"4": 4})
    add_history(conn, uid, {"5": 5}, {"6": 6})
    print(read_history(conn, uid))
