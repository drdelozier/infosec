#
# database.py
#
# Model database for security education
#
import os.path
import json

def always(v):
    return True

def everything(v):
    return v

class Database:
    def __init__(self, path, verbose=False):
        self._path_ = path
        self._verbose = verbose
        if os.path.isfile(self._path_):
            with open(self._path_,'r') as f:
                self._data = json.load(f)
        else:
            self._data = []
            self.commit()
        if self._verbose: print('database initialized')

    def commit(self):
        with open(self._path_,'w') as f:
            json.dump(self._data,f)
        if self._verbose: print('commit completed')

    def count(self, where=always):
        if self._verbose: print('counting...')
        return len([item for item in self._data if where(item)])

    def load(self, data=[]):
        self._data = data
        self.commit()
        with open(self._path_,'r') as f:
            self._data = json.load(f)

    def read(self, select=everything, where=always, order_by=None, reverse=False):
        if self._verbose: print('reading...')
        # results = []
        # for item in self._data:
        #     if where(item):
        #         results.append(select(item))
        results = [select(item) for item in self._data if where(item)]
        if order_by:
            if order_by is str:
                results = sorted(results, key=lambda x:x[order_by], reverse=reverse)
            else:
                results = sorted(results, key=order_by, reverse=reverse)
            return results
        if reverse: #but not order
            return results[::-1] #idiom to reverse a list
        return results

    def update(self, values={}, where=None):
        assert(where)
        for item in self._data:
            if where(item):
                for key in values:
                    item[key] = values[key]
        self.commit()
        if self._verbose: print('update completed')

    def delete(self, where=None):
        assert(where)
        copy = []
        for item in self._data:
            if not where(item):
                copy.append(item)
        self._data = copy
        self.commit()
        if self._verbose: print('delete completed')

test_data = [
    {'table':'user', 'name':'greg',    'role':'professor', 'dept':'dog_studies'},
    {'table':'user', 'name':'janet',   'role':'professor', 'dept':'dog_studies'},
    {'table':'user', 'name':'suzy',    'role':'student'},
    {'table':'user', 'name':'dorothy', 'role':'student'},
    {'table':'user', 'name':'allie',   'role':'student'},

    {'table':'class', 'name':'advanced_fetching', 'professor':'greg'},
    {'table':'class', 'name':'treat_finding',     'professor':'janet'},

    {'table':'enrollment', 'student':'suzy',    'class':'advanced_fetching', 'grade':'A'},
    {'table':'enrollment', 'student':'dorothy', 'class':'advanced_fetching', 'grade':'C-'},
    {'table':'enrollment', 'student':'dorothy', 'class':'treat_finding',     'grade':'B'},
    {'table':'enrollment', 'student':'allie',   'class':'advanced_fetching', 'grade':'B'},

    {'table':'document', 'name':'alpha', 'facts':'abcde',  'level':'unclassified'},
    {'table':'document', 'name':'gamma', 'facts':'hijkl',  'level':'confidential'},
    {'table':'document', 'name':'sigma', 'facts':'mnopq',  'level':'secret'},
    {'table':'document', 'name':'theta', 'facts':'uvwxyz', 'level':'top-secret'},
]

def test_init():
    print("testing db.init")
    db = Database("example.json")
    assert type(db) is Database
    db = Database("example.json", verbose=True)
    assert type(db) is Database

def test_load():
    print('testing db.load')
    db = Database('example.json')
    db.load(test_data)
    assert len(db._data) == len(test_data)
    db = Database('example.json')
    assert len(db._data) == len(test_data)
    assert db.count() == len(test_data)

def test_count():
    print('testing db.count')
    db = Database('example.json')
    db.load(test_data)
    db = Database('example.json')
    assert db.count() == len(test_data)
    assert db.count(where=lambda x: x['table'] == 'user' and x.get('role') ) == 5
    assert db.count(where=lambda x: x['table'] == 'user' and x['role'] == 'student' ) == 3

def test_read():
    print('testing db.read')
    db = Database('example.json')
    db.load(test_data)
    results = db.read(where=lambda x: x['table'] == 'user' and x.get('role') )
    assert len(results) == 5
    assert results[0]['name'] == 'greg'
    results = db.read(where=lambda x: x['table'] == 'user' and x['role'] == 'student' )
    assert len(results) == 3
    print(results)
    assert results[0]['name'] == 'suzy'
    results = db.read(
        where=lambda x: x['table'] == 'user' and x['role'] == 'student',
        select=lambda x: {'name': x['name'], 'role': x['role']}
        )
    assert len(results) == 3
    assert results[0] == {'name': 'suzy', 'role': 'student'}
    results = db.read(where=lambda x: x['table'] == 'user', reverse=True)
    assert len(results) == 5
    assert results[0]['name'] == 'allie'
    assert results[4]['name'] == 'greg'
    results = db.read(where=lambda x: x['table'] == 'user', order_by=lambda x: x['name'])
    assert len(results) == 5
    assert results[0]['name'] == 'allie'
    assert results[4]['name'] == 'suzy'
    results = db.read(where=lambda x: x['table'] == 'user', order_by=lambda x: x['name'], reverse=True)
    for result in results:
        print(result)

def test_commit():
    print('testing db.commit')
    db = Database('example.json')
    db.load(test_data)
    db.commit()
    results = db.read(where=lambda x: x['table'] == 'user' and x.get('role') )
    assert len(results) == 5
    assert results[0]['name'] == 'greg'
    results = db.read(where=lambda x: x['table'] == 'user' and x['role'] == 'student' )
    assert len(results) == 3
    assert results[0]['name'] == 'suzy'

def test_update():
    print('testing db.update')
    db = Database('example.json')
    db.load(test_data)
    results = db.read(where=lambda x: x['table'] == 'user')
    assert len(results) == 5
    assert results[0]['name'] == 'greg'
    db.update(where=lambda x: x['table'] == 'user' and x['name'] == 'greg', values={'name':'gregory'})
    results = db.read(where=lambda x: x['table'] == 'user')
    assert len(results) == 5
    assert results[0]['name'] == 'gregory'
    db = Database('example.json')
    results = db.read(where=lambda x: x['table'] == 'user')
    assert len(results) == 5
    assert results[0]['name'] == 'gregory'

def test_delete():
    print('testing db.delete')
    db = Database('example.json')
    db.load(test_data)
    results = db.read(where=lambda x: x['table'] == 'user')
    print(results)
    assert len(results) == 5
    assert results[0]['name'] == 'greg'
    db.delete(where=lambda x: x['table'] == 'user' and x['name'] == 'greg')
    results = db.read(where=lambda x: x['table'] == 'user')
    assert len(results) == 4
    assert results[0]['name'] == 'janet'
    db = Database('example.json')
    results = db.read(where=lambda x: x['table'] == 'user')
    assert len(results) == 4
    assert results[0]['name'] == 'janet'

if __name__ == "__main__":
    test_init()
    test_load()
    test_count()
    test_read()
    test_commit()
    test_update()
    test_delete()

