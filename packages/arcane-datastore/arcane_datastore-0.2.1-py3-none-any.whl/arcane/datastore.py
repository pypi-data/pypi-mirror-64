from typing import Union

import backoff
from google.cloud.datastore import Client as GoogleDatastoreClient, Entity
from arcane.core.exceptions import GOOGLE_EXCEPTIONS_TO_RETRY


class Client(GoogleDatastoreClient):
    def __init__(self, project=None, credentials=None, _http=None):
        super().__init__(project=project, credentials=credentials, _http=_http)
    
    @backoff.on_exception(backoff.expo, GOOGLE_EXCEPTIONS_TO_RETRY, max_tries=5)
    def get_entity(self, kind: str, entity_id: int) -> Union[Entity, None]:
        return self.get(self.key(kind, entity_id))
