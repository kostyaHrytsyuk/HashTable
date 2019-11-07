import abc
import math


class HashTable:

    def __init__(self, hash_type, values):
        if hash_type == 1:
            self.h_table = HashTableDivision(values)
        elif hash_type == 2:
            self.h_table = HashTableMultiplication(values)
        elif hash_type == 3:
            self.h_table = HashTableOpenAddressingLinearProbing(values)
        elif hash_type == 4:
            self.h_table = HashTableOpenAddressingQuadraticProbing(values)
        elif hash_type == 5:
            self.h_table = HashTableOpenAddressingDoubleHashing(values)

    def get_collisions_amount(self):
        return self.h_table.collisions

    def find_sum(self, s):
        if isinstance(self.h_table, HashTableChaining):
            for i in range(self.h_table._get_table_size()):
                if self.h_table.table[i]:
                    for j in range(len(self.h_table.table[i])):
                        y = s - self.h_table.table[i][j]
                        if self.h_table.hash_search(y):
                            return self.h_table.table[i][j], y
        else:
            for j in range(self.h_table._get_table_size()):
                if self.h_table.table[j]:
                    y = s - self.h_table.table[j]
                    if self.h_table.hash_search(y):
                        return self.h_table.table[j], y
        return None


class MyHashTable:
    table = []
    collisions = 0

    @abc.abstractmethod
    def hash(self, key):
        pass

    @staticmethod
    def __get_golden_ratio():
        return ((5 ** 0.5) - 1) / 2

    def _get_table_size(self):
        res = len(self.table)
        return res

    def hash_division(self, key):
        return key % self._get_table_size()

    def hash_multiplication(self, key):
        res = (key * self.__get_golden_ratio()) % 1
        m = 2 ** 4
        hash_code = math.floor(m * res)
        return hash_code

    @abc.abstractmethod
    def hash_search(self, y):
        pass


class HashTableChaining(MyHashTable):
    def hash_search(self, y):
        pass

    def hash(self, key):
        pass


class HashTableDivision(HashTableChaining):
    def __init__(self, values):
        self.table = [[] for _ in range(len(values))]
        for _ in range(len(values)):
            key = self.hash(values[_])
            if len(self.table[key]) != 0:
                self.collisions += 1
            self.table[key].append(values[_])

    def hash(self, key):
        return super().hash_division(key)

    def hash_search(self, y):
        hashed_y = self.hash(y)
        item = self.table[hashed_y]
        if not item:
            return None
        elif y in item:
            return y
        else:
            return None


class HashTableMultiplication(HashTableChaining):

    def __init__(self, values):
        self.table = [[] for _ in range(3 * len(values))]
        for i in range(len(values)):
            key = self.hash(values[i])
            if len(self.table[key]) != 0:
                self.collisions += 1
            self.table[key].append(values[i])

    def hash(self, key):
        return super().hash_multiplication(key)

    def hash_search(self, y):
        hashed_y = self.hash(y)
        item = self.table[hashed_y]
        if not item:
            return None
        elif y in item:
            return y
        else:
            return None


class HashTableProbing(MyHashTable):

    def __init__(self, values):
        self.table = len(values) * [None]

    def hash(self, key):
        return super().hash_division(key)

    def hash_search(self, y):
        pass

    @abc.abstractmethod
    def insert(self, key):
        pass


class HashTableOpenAddressingLinearProbing(HashTableProbing):

    def __init__(self, values):
        super().__init__(values)
        for i in range(len(values)):
            self.insert(values[i])

    def hash_linear_probing(self, key, i):
        hashed_key = super().hash(key)
        return self.hash(hashed_key + i)

    def insert(self, val):
        for n in range(len(self.table)):
            key = super().hash_division(val)
            if self.table[key]:
                self.table[key] = val
            else:
                self.collisions += 1
                key += 1
                while key < len(self.table):
                    key = self.hash_linear_probing(val, key)
                    if not self.table[key]:
                        self.table[key] = val
                        return
                    key += 1

    def hash_search(self, y):
        for i in range(len(self.table)):
            key = super().hash_division(y)
            if self.table[key] == y:
                return True
            else:
                key += 1
                while key < len(self.table):
                    key = self.hash_linear_probing(y, key)
                    if self.table[key] == y:
                        return y
        return False


class HashTableOpenAddressingQuadraticProbing(HashTableProbing):

    def __init__(self, values):
        super().__init__(values)
        for i in range(len(values)):
            self.insert(values[i])

    def insert(self, val):
        for n in range(len(self.table)):
            j = self.hash_quadratic_probing(val, n)
            if not self.table[j]:
                self.table[j] = val
                return

    def hash_quadratic_probing(self, key, i):
        hashed_key = super().hash(key)
        return super().hash(hashed_key + 2*i + 7*i**2)

    def hash_search(self, y):
        for i in range(len(self.table)):
                j = self.hash_quadratic_probing(y, i)
                if self.table[j] == y:
                    return y
        return None


class HashTableOpenAddressingDoubleHashing(HashTableProbing):

    def __init__(self, values):
        super().__init__(values)
        for i in range(len(values)):
            self.insert(values[i])

    def insert(self, val):
        for n in range(len(self.table)):
            key = super().hash_division(val)
            if self.table[key]:
                self.table[key] = val
            else:
                self.collisions += 1
                counter = 0
                while counter < len(self.table):
                    key = 1 + self.double_hash(val, key)
                    if not self.table[key]:
                        self.table[key] = val
                        return
                    counter += 1

    def double_hash(self, key, i):
        first = self.add_hash_first(key)
        second = self.add_hash_second(key)
        hash_code = (first + (second * (i + 1))) % 7
        return hash_code

    def hash_search(self, y):
        for i in range(len(self.table)):
            j = super().hash_division(y)
            if self.table[j] == y:
                return True
            else:
                counter = 0
                while counter < len(self.table):
                    j = 1 + self.double_hash(y, j)
                    if self.table[j] == y:
                        return True
                    counter += 1
        return False

    @staticmethod
    def add_hash_first(key):
        return key % 16

    @staticmethod
    def add_hash_second(key):
        return 1 + (key ** 2)


# tbl = [[7, 5], [8, 4], [9, 3], [10, 2], [1, 10], [3, 15], [8, 10], [6, 4], [5, 3], [7, 3]]

tbl = [42, 92, 13, 40, 46, 27, 33, 65, 33, 84]

h = HashTable(3, tbl)

print(h.find_sum(108))
print(h.find_sum(117))
print(h.find_sum(134))
print(h.find_sum(48))
