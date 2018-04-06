import pickle
class Table:
    def __init__(self, name='', fields=tuple(), tups=None):
        self._name = ''.join(name.split('.txt'))
        self._fields = fields
        self._tuples = tups

    def __str__(self):
        output = f'{self._name}{self.fields}\n{"=" * len(self._name)}\n'
        for tuple in self._tuples:
            output += f'{tuple}\n'
        return output

    @property
    def fields(self):
        return self._fields

    @property
    def tuples(self):
        return self._tuples

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    # Relational operations:
    def select(self, field, val):
        index = self._fields.index(field)
        new_tuples = list()
        for tuple in self._tuples:
            if tuple[index] == val:
                new_tuples.append(tuple)
        return Table('result', self._fields, new_tuples)

    def project(self, *fields):
        new_tups = set()
        a = [self._fields.index(x) for x in fields]
        for tup in self._tuples:
            tup_list = []
            for i in a:
                tup_list.append(tup[i])
            new_tups.add(tuple(tup_list))
        return Table('result',tuple(fields),new_tups)

    @staticmethod
    def join(tab1, tab2):
        indx = [tab1.fields.index(i) for i in tab1.fields if i in tab2.fields]
        new_tuples = []
        new_fields = tuple((x for x in tab1.fields if x not in tab2.fields)) + tab2.fields
        for tup1 in tab1.tuples:
            for tup2 in tab2.tuples:
                if tup1[indx[0]] in tup2:
                    tupx = tuple((x for x in tup1 if x not in tup2))
                    new_tuples.append(tuple(tupx + tup2))
        return Table('results',new_fields,new_tuples)



    def insert(self, *tup):
        if tup not in self.tuples and len(tup) == len(self._fields):
            self._tuples.append(tuple(tup))
        else:
             print('Added tuple is wrong length')
        return (Table('result', self._fields, self._tuples))

    def remove(self, field, val):
        index = self._fields.index(field)
        new_tups = list()
        for i in self._tuples:
            if i[index] != val:
                new_tups.append(i)
        self._tuples = new_tups
    # Serialization and text backup
    def store(self):
        fname = self.name + ".db"
        pickle.dump(self,open(fname,'wb'))

    @staticmethod
    def restore(fname):
        result = pickle.load(open(fname, 'rb'))
        return result

    @staticmethod
    def read(fname):
        new_fields = None
        new_tups = list()
        with open(fname) as file:
            table = file.read().splitlines()
        for line in table:
            if line != ''.join(fname.split('.txt')):
                if not new_fields:
                    new_fields = tuple(line.split(','))
                else:
                    new_tups.append(tuple(line.split(',')))
        return Table(fname, new_fields, new_tups)

    def write(self, fname):
        result = open(fname,'w')
        result.write(''.join(fname.split('.txt')))
        result.write('\n'+','.join(self._fields) + '\n')
        for tuple in self._tuples:
            result.write(','.join(tuple) + '\n')