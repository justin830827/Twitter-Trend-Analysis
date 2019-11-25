import json
from tweepy import Status


class StatusConverter:
    """
    Converts Twitter Status to a JSON message
    """

    @staticmethod
    def to_json(status: Status):
        """
        Converts a status into JSON
        :param status:
        :return:
        """
        message = {
            'id': status.id,
            'created_at': status.created_at.isoformat(),
            'text': status.text
        }
        if status.place is not None:
            message['place'] = status.place.full_name

        return json.dumps(message, ensure_ascii=False).encode('utf8')
