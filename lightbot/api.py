"""

https://docs.go-cqhttp.org/api/
"""

class Api:
    def __init__(self, action, **params):
        self.action = action
        self.params = params
    
    def __getattr__(self, k):
        return self.params.get(k, None)
    
    def json(self):
        return {
            "action": self.action,
            "params": self.params
        }

    def __repr__(self):
        return str(self.json())

class SendGroupMessage(Api):
    def __init__(self, group_id, message):
        params = {
            'group_id': group_id,
            'message': message
        }
        super().__init__('send_group_msg', **params)
    

if __name__ == "__main__":
    # api = Api("send_group_msg", group_id=123456, message="hello!")
    api = SendGroupMessage(12355, 'asdfasdf')
    print(api)

