from converters.status_converter import StatusConverter


class FilePersistor:
    """
    Persists message to a file
    """

    def __init__(self, filename):
        self.filename = filename

    def persist(self, message):
        """
        Persists a message to a file
        :param message:
        :return:
        """
        with open(self.filename, 'ab') as file:
            file.write(StatusConverter.to_json(message))
            file.write(b'\n')
