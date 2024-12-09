"""
Abstraction of a Spotted Apple User
"""

class User:
    def __init__(self, user_data: dict):
        self.info = user_data

        for key, value in self.info.items():
            if key == 'created':
                value = self._get_created(value)
            self.info[key] = value
            setattr(self, key, value)

    def is_valid(self):
        """
        A user object is only valid if the email, first name, and last name fields
        are not None, as they are required fields for creating a new user.
        """
        required_fields = ['email', 'first_name', 'last_name']
        try:
            assert all([required_field in self.user_data.keys() for required_field in required_fields])
            return True
        except AssertionError:
            return False

    def add_fields(self, data):
        self.info.update(data)
        for key, value in self.info.items():
            if key == 'created':
                value = self._get_created(value)
            self.info[key] = value
            setattr(self, key, value)            

    @staticmethod
    def _get_created(raw_created):
        try:
            created = raw_created.isoformat(timespec='milliseconds')
        except (KeyError, AttributeError):
            return raw_created
        return created
