import pymysql
import pymysql.cursors

__all__ = ['ReturnKind', 'go', 'check_conn']

# enum for use with go() below; e.g., ReturnKind.ALLROWS
ReturnKind = type('ReturnKind', (), {'SINGLEVAL':1, 'ONEROW':2, 'ALLROWS':3})

def go(db_spec
      ,parameterized_stmt
      ,data_tuple
      ,returnkind=ReturnKind.ALLROWS
      ,commit=False
      ,useDictCursor=False):
  '''Execute a SQL statement in a MySQL database. 
  Throws on error.
  Arguments:
    o db_spec: a map of key-value pairs like so:
        { "host" : "localhost"
        , "user" : "X"
        , "password" : "X"
        , "db" : "mydb" 
        , "charset" : "utf8mb4" }
    o parameterized_stmt: parameterized SQL statement.
    o data_tuple: tuple containing data corresponding to the 
      parameterized statement. If running a select statement, etc.,
      then just pass in an empty tuple.
    o returnkind: a ReturnKind enum value; specifes shape of result
      to return.
    o commit: default is False; use True if you are running 
              an insert statment, etc.
  '''
  rslt = ()
  conn = None
  if useDictCursor:
    conn = pymysql.connect(cursorclass=pymysql.cursors.DictCursor, **db_spec)
  else:
    conn = pymysql.connect(**db_spec)
  try:
    with conn.cursor() as cursor:
      cursor.execute(parameterized_stmt, data_tuple)
      # fetchall will return a tuple -- e.g., ((0,),)
      rslt = cursor.fetchall() 
      if commit: conn.commit()
  except: raise
  finally:
    conn.close()
  # Customize how result is returned.
  if returnkind == ReturnKind.SINGLEVAL: 
    if len(rslt) and len(rslt[0]): return rslt[0][0]
    else: return ''
  elif returnkind == ReturnKind.ONEROW:
    if len(rslt): return rslt[0]
    else: return ()
  else:
    # Else ALLROWS, in essence.
    return rslt

def check_conn(db_spec):
  qy = 'select version(), user(), database();'
  return go(db_spec, qy, (), ReturnKind.ONEROW)

