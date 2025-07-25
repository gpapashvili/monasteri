import sqlalchemy as sqla

# uses sqlalchemy to create engine for later use
def create_db_engine(_user, _passw, _db_server, _db_name, _db_ms = 'postgresql',):
    _url = f'{_db_ms}://{_user}:{_passw}@{_db_server}/{_db_name}'
    try:
        _eng = sqla.create_engine(_url)
        with _eng.connect() as _conn:
            _results = _conn.execute(sqla.text(("SELECT 1"))).fetchall()
        return _eng if _results else "SQL-ის გაშვებისას დაფიქსირდა შეცდომა"
    except Exception as e:
        return f"ბაზასთან დაკავშირებისას დაფიქსირდა შეცდომა: {e}"


import pandas as pd
# uses pandas to get data from db
# stick to this one, it will also give tou chance to connect database separately
def pd_query(_stat, _eng):
    df = pd.read_sql_query(sqla.text(_stat), _eng)
    # transforms dataframe to list of series for each row
    return [pd_series for pd_series in (row for i, row in df.iterrows())]


# use sqlalchemy native way to get data as list
def query(_stat, _eng):
    with _eng.connect() as _conn:
        _results = _conn.execute(sqla.text(_stat)).fetchall()
    return _results


# not yet tested
def crt_query(_stat, _eng):
    with _eng.connect() as _conn:
        _conn.execute(sqla.text(_stat))
        _conn.commit()
    return True


# not yes tested
def insert_query(_table_name, _data, _eng):
    """Insert data query, _stat should be like "INSERT INTO table (col1, col2) VALUES (:col1, :col2)"
    data should be like [{"col1": val1, "col2": val2}, {"col1": val3, "col2": val4}] """

    # first check if columns from data are subset of columns from db
    columns_from_db = set(pd.read_sql_query(sqla.text(f"SELECT * FROM {_table_name} LIMIT 0"), _eng).columns)
    columns_from_data = set(key for row in _data for key in row.keys())
    # raise Valueerror if not subset
    if not columns_from_data.issubset(columns_from_db):
        message = 'Mismatch in column names:\n'
        message += f'columns_from_db:\t{sorted(columns_from_db)}\n'
        message += f'columns_from_data:\t{sorted(columns_from_data)}'
        return message

    # next create insert statement
    cols_str = ", ".join(_data[0].keys())
    placeholders = ", ".join(f":{column}" for column in _data[0].keys())
    stat = f"""INSERT INTO {_table_name} ({cols_str}) VALUES ({placeholders})""".strip()
    # connect to db, execute and commit
    with _eng.connect() as _conn:
        _conn.execute(sqla.text(stat), _data)
        _conn.commit()
    return True


from django.db import connection
# djangos native vay to execute query and get results in
def django_sql(stat="SELECT 10"):
    with connection.cursor() as cursor:
        cursor.execute(stat)
        row = cursor.fetchall()
    return row


