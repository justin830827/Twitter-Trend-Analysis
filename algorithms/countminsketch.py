import mmh3


class CountMinSketch(object):
    def __init__(self, width, depth):
        self.width = width
        self.depth = depth
        self.table = []

        for _ in range(depth):
            row = [0 for _ in range(width)]
            self.table.append(row)

    def hashes(self, word):
        index = []
        hash1 = mmh3.hash(word, 0)
        hash2 = mmh3.hash(word, hash1)
        for i in range(self.depth):
            index.append(abs(hash1 + i + hash2) % self.width)
        return index

    def add(self, word):
        index = self.hashes(word)
        for row, i in zip(self.table, index):
            row[i] += 1
        return self

    def __getitem__(self, x):
        value = []
        index = self.hashes(x)
        for row, i in zip(self.table, index):
            value.append(row[i])
        return min(value)

    def merge(self, cms_to_merge):
        for row_idx in range(self.depth):
            for column_idx in range(self.width):
                self.table[row_idx][column_idx] += cms_to_merge.table[row_idx][column_idx]
        return self


class TopK(object):
    def __init__(self, word, count_min_sketch):
        self.count = count_min_sketch[word]
        self.value = word
        return

    def __lt__(self, other):
        return self.count < other.count


def topK(x, CMS, q, k):
    if len(q.queue) < k:
        q.put(TopK(x, CMS))
    elif len(q.queue) == k:
        check = 0
        index = -1
        tmp = []
        for i in range(k):
            if q.queue[i].value == x:
                index = i
                check = 1
                break

        if check == 0:
            temp = q.get()
            if temp.count <= CMS[x]:
                q.put(TopK(x, CMS))
            else:
                q.put(temp)
        elif check == 1:
            for i in range(index + 1):
                temp = q.get()
                tmp.append(temp.value)
            for i in tmp:
                q.put(TopK(i, CMS))
    return q
