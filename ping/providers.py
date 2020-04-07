from notifiers.core import Provider, Response

__all__ = ["monekypatch_providers"]

class Dummy(Provider):
    """ Dummy Implementation """
    name = "dummy"
    base_url ="http://localhost"
    site_url="http://localhost"
    _required = {"required": ["message"]}
    _schema = {
        'type': 'object',
        "properties": {
            "message": { "type": "string", "title": "The Message Schema", }
        }
    }

    def _process_data(self, **kwargs):
        return kwargs

    def _send_notification(self, data):
        print(f"send {data}")
        return self.create_response(data)
    

def monekypatch_providers():
    import notifiers.providers
    notifiers.providers._all_providers.update({'dummy': Dummy})
