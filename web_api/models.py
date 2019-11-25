
frequent_word = api.model('FrequentWord', {
    'word': fields.String(),
    'frequency': fields.Integer()
})

top_words = api.model('TopWords', {
    'words': fields.List(frequent_word, description='Most Frequent Words')
})