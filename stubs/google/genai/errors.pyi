import httpx
import requests
from .replay_api_client import ReplayResponse as ReplayResponse
from _typeshed import Incomplete

class APIError(Exception):
    code: int
    response: requests.Response | ReplayResponse | httpx.Response
    status: str | None
    message: str | None
    details: Incomplete
    def __init__(self, code: int, response: requests.Response | ReplayResponse | httpx.Response) -> None: ...
    @classmethod
    def raise_for_response(cls, response: requests.Response | ReplayResponse | httpx.Response): ...

class ClientError(APIError): ...
class ServerError(APIError): ...
class UnknownFunctionCallArgumentError(ValueError): ...
class UnsupportedFunctionError(ValueError): ...
class FunctionInvocationError(ValueError): ...
class ExperimentalWarning(Warning): ...
