import google.auth
import io
from . import errors as errors
from ._api_client import BaseApiClient as BaseApiClient, HttpOptions as HttpOptions, HttpRequest as HttpRequest, HttpResponse as HttpResponse
from ._common import BaseModel as BaseModel
from _typeshed import Incomplete
from typing import Any, Literal

def redact_http_request(http_request: HttpRequest): ...

class ReplayRequest(BaseModel):
    method: str
    url: str
    headers: dict[str, str]
    body_segments: list[dict[str, object]]

class ReplayResponse(BaseModel):
    status_code: int
    headers: dict[str, str]
    body_segments: list[dict[str, object]]
    byte_segments: list[bytes] | None
    sdk_response_segments: list[dict[str, object]]
    def model_post_init(self, /, __context: Any) -> None: ...

class ReplayInteraction(BaseModel):
    request: ReplayRequest
    response: ReplayResponse

class ReplayFile(BaseModel):
    replay_id: str
    interactions: list[ReplayInteraction]

class ReplayApiClient(BaseApiClient):
    replays_directory: Incomplete
    replay_session: Incomplete
    def __init__(self, mode: Literal['record', 'replay', 'auto', 'api'], replay_id: str, replays_directory: str | None = None, vertexai: bool = False, api_key: str | None = None, credentials: google.auth.credentials.Credentials | None = None, project: str | None = None, location: str | None = None, http_options: HttpOptions | None = None) -> None: ...
    def initialize_replay_session(self, replay_id: str): ...
    def close(self) -> None: ...
    def upload_file(self, file_path: str | io.IOBase, upload_url: str, upload_size: int): ...
    async def async_upload_file(self, file_path: str | io.IOBase, upload_url: str, upload_size: int) -> str: ...
    async def async_download_file(self, path: str, http_options): ...
