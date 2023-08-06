import dataset
import sys

DEBUG = True

if DEBUG is False:
    print = lambda *a, **k: None


def RegisterDBURI(dburi=None):
    global _DB
    global _DBURI
    if dburi is None:
        if sys.platform.startswith('win'):
            dburi = 'sqlite:///MyDatabase.db'
        else:  # linux
            dburi = 'sqlite:////MyDatabase.db'

    _DBURI = dburi
    _DB = dataset.connect(dburi)
    print('_DB=', _DB)


class BaseTable(dict):
    def __init__(self, *a, **k):
        for key, value in k.items():
            if isinstance(value, bytes):
                raise TypeError('Dont pass bytes-type, instead use b''.decode()')

        self._initComplete = False
        super().__init__(*a, **k)

        self._initComplete = True

    def __setitem__(self, key, value):
        '''
        Any time a value is set to this newObj, the change will be updated in the database
        :param key:
        :param value:
        :return:
        '''
        print('__setitem__', key, value)
        super().__setitem__(key, value)
        if self._initComplete:
            _Upsert(self)  # save changes to DB

    def __str__(self):
        '''

        :return: string like '<BaseDictabaseTable: email=me@website.com, name=John>'
        '''
        itemsList = []
        for k, v, in self.items():
            if isinstance(v, str) and len(v) > 25:
                v = v[:25]
            itemsList.append(('{}={}'.format(k, v)))

        return '<{}: {}>'.format(
            type(self).__name__,
            ', '.join(itemsList)
        )

    def __repr__(self):
        return str(self)


def New(cls, **k):
    '''
    Creates a new row in the table(cls)
    Returns the new dict-like object

    cls should inherit from BaseTable
    '''
    # print('New(cls=', cls, ', k=', k)
    newObj = cls(**k)

    tableName = cls.__name__
    _DB.begin()
    ID = _DB[tableName].insert(newObj)
    _DB.commit()

    newObj.update({'id': ID})
    return newObj


def _Upsert(obj):
    print('_Upsert(obj=', obj)
    tableName = type(obj).__name__
    _DB.begin()
    _DB[tableName].upsert(obj, ['id'])  # find row with matching 'id' and update it
    _DB.commit()


def FindOne(cls, **k):
    # _DB.begin() # dont do this
    print('_DB.tables=', _DB.tables)
    dbName = cls.__name__
    tbl = _DB[dbName]
    ret = tbl.find_one(**k)
    print('FindOne ret=', ret)

    if ret:

        return cls(ret)
    else:
        return None


def FindAll(cls, **k):
    # special kwargs
    reverse = k.pop('_reverse', False)  # bool
    orderBy = k.pop('_orderBy', None)  # str
    if reverse is True:
        if orderBy is not None:
            orderBy = '-' + orderBy
        else:
            orderBy = '-id'

    # do look up
    dbName = cls.__name__
    if len(k) is 0:
        ret = _DB[dbName].all(order_by=[f'{orderBy}'])
    else:
        if orderBy is not None:
            ret = _DB[dbName].find(order_by=['{}'.format(orderBy)], **k)
        else:
            ret = _DB[dbName].find(**k)

    # yield type-cast items one by one
    for item in ret:
        yield cls(item)


def Drop(cls, confirm=False):
    global _DB
    if confirm:
        _DB.begin()
        tableName = cls.__name__
        _DB[tableName].drop()
        _DB.commit()

        _DB = dataset.connect(_DBURI)
    else:
        raise Exception('Cannot drop unless you pass confirm=True as kwarg')


def Delete(obj):
    _DB.begin()
    dbName = type(obj).__name__
    _DB[dbName].delete(**obj)
    _DB.commit()


if __name__ == '__main__':
    import time

    RegisterDBURI(
        'postgres://xfgkxpzruxledr:5b83aece4fbad7827cb1d9df48bf5b9c9ad2b33538662308a9ef1d8701bfda4b@ec2-35-174-88-65.compute-1.amazonaws.com:5432/d8832su8tgbh82')


    def TestA():
        class A(BaseTable):
            pass

        Drop(A, confirm=True)

        for i in range(10):
            New(A, time=time.asctime(), count=i)

        print('FindAll(A)=', list(FindAll(A)))
        print('FindOne(A, count=5)=', FindOne(A, count=5))

        for item in FindAll(A):
            item['count'] += 10

        print('FindAll(A)=', list(FindAll(A)))

        for i in range(0, 10, 2):
            obj = FindOne(A, count=i + 10)
            if obj:
                Delete(obj)

        print('FindAll(A)=', list(FindAll(A)))


    def TestBytes():
        # test bytes type
        class B(BaseTable):
            pass

        Drop(B, confirm=True)

        d = ('0' * 100).encode()
        try:
            large = New(B, data=d)

        except Exception as e:
            print(e)
        large = New(B, data=d.decode())
        print("large['data'] == d is", large['data'] == d)

        largeID = large['id']

        findLarge = FindOne(B, id=largeID)
        print("findLarge['data'] == d is", findLarge['data'].encode() == d)


    #################
    TestBytes()
