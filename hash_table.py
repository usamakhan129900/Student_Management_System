# hash_table.py

class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return True
        self.table[index].append((key, value))
        return True

    def retrieve(self, key):
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def delete(self, key):
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                return True
        return False

    def get_all_students(self):
        students = []
        for bucket in self.table:
            for k, v in bucket:
                students.append(v)
        return students

    def get_all_students_dict(self):
        students_dict = {}
        for bucket in self.table:
            for k, v in bucket:
                students_dict[k] = v
        return students_dict

    def clear(self):
        self.table = [[] for _ in range(self.size)]
