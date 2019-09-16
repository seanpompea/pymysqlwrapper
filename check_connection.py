import json
import pymysqlwrapper

with open('./enclave/db_spec.json') as f:
  db_spec = json.load(f)
print pymysqlwrapper.check_conn(db_spec)

