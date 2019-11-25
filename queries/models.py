

class Query:
    def __init__(self, term: str, place: str, start_time: str, end_time: str, k: int):
        self.term = term
        self.place = place
        self.start_time = start_time
        self.end_time = end_time
        self.k = k
