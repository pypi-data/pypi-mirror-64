import requests

class CenterIdentity:
    def __init__(self, api_key):
        self.api_key = api_key

    def add_user(self):
        pass

    def friend_request(self, requesting_user_id, requested_user_id):
        pass

    def accept_friend_request(self, friend_request):
        pass

    def recover_seed(self, rid):
        pass

    def save_seed(self, rid, encrypted_seed):
        pass
