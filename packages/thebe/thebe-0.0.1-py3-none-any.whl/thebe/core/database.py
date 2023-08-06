import sqlite3
import satyrn.core.constants as Constant
from datetime import datetime
import dill
import os

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        if col[0] == 'cells' or col[0] == 'local_scope' or col[0] == 'global_scope':
            d[col[0]] = dill.loads(row[idx])
        else:
            d[col[0]] = row[idx]
    return d
DATABASE = '%s/database.sqlite' % os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(DATABASE)
conn.row_factory = dict_factory
c = conn.cursor()

def getLedger(target):
    c.execute('SELECT * FROM ledger WHERE name=?', (target,))
    fetched=c.fetchone()
    if bool(fetched):
        r=fetched
        return r['cells'], r['global_scope'], r['local_scope']
    else:
        print('Creating ledger...')
        createLedger(target)
        return getLedger(target)

def getExecutions(target):
    c.execute('SELECT executions FROM ledger WHERE name=?', (target,))
    return c.fetchone()['executions']

def createLedger(target):
    print('Creating ledger %s' % target)
    now=datetime.now().strftime('%a, %B, %d, %y')
    c.execute('INSERT INTO ledger (name, last_edit, created, cells, global_scope, local_scope) VALUES (?,?,?,?,?,?)', (target, now, now, dill.dumps([]), dill.dumps({}), dill.dumps({})))
#    c.execute('INSERT INTO ledger (name, last_edit, created, cells, ledger, global_scope, local_scope) VALUES (?,?,?,?,?,?,?)', (target, now, now, dill.dumps([]), dill.dumps([]), dill.dumps({}), dill.dumps({})))

def update(target, cells, globalScope, localScope, executions):
    c.execute('UPDATE ledger SET cells=?, global_scope=?, local_scope=?, executions=? WHERE name=?', (dill.dumps(cells), dill.dumps(globalScope), dill.dumps(localScope), executions, target))
