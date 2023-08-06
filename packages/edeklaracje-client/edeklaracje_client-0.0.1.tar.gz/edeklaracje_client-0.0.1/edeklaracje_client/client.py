from enum import Enum

from waiting import wait
from zeep import Client


class Environment(Enum):
    PRODUCTION = "https://bramka.e-deklaracje.mf.gov.pl/uslugi/dokumenty?wsdl"
    TEST = 'https://test-bramka.edeklaracje.gov.pl/uslugi/dokumenty?wsdl'


class EDeklaracjeClient:
    def __init__(self, env: Environment):
        self.client = Client(env.value)

    def send_document(self, serialized_document: str) -> str:
        result = self.client.service.sendUnsignDocument(serialized_document.encode())
        self._raise_exception_if_needed(result)
        return result.refId

    def send_and_wait_for_upo(self, document: str) -> str:
        return self.get_upo_if_present(self.send_document(document))

    def get_upo_if_present(self, refId: str):
        result = self.client.service.requestUPO(refId)
        self._raise_exception_if_needed(result)
        return result.upo

    def wait_for_upo(self, refId: str, timeout_in_seconds: int = 600):
        return wait(lambda: self.get_upo_if_present(refId), timeout_seconds=timeout_in_seconds)

    def _raise_exception_if_needed(self, result):
        if 301 <= result.status < 400 or result.status == 200:
            return
        raise Exception("{}: {}".format(result.status, result.statusOpis))
