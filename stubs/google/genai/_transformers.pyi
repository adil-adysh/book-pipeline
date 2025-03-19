import types as builtin_types
from . import _api_client, types as types
from _typeshed import Incomplete
from collections.abc import Iterable, Mapping
from typing import Any

logger: Incomplete
VersionedUnionType = builtin_types.UnionType

def t_model(client: _api_client.BaseApiClient, model: str): ...
def t_models_url(api_client: _api_client.BaseApiClient, base_models: bool) -> str: ...
def t_extract_models(api_client: _api_client.BaseApiClient, response: dict[str, list[types.ModelDict]]) -> list[types.ModelDict] | None: ...
def t_caches_model(api_client: _api_client.BaseApiClient, model: str): ...
def pil_to_blob(img) -> types.Blob: ...
def t_part(part: types.PartUnionDict | None) -> types.Part: ...
def t_parts(parts: list[types.PartUnionDict] | types.PartUnionDict | None) -> list[types.Part]: ...
def t_image_predictions(client: _api_client.BaseApiClient, predictions: Iterable[Mapping[str, Any]] | None) -> list[types.GeneratedImage] | None: ...

ContentType: Incomplete

def t_content(client: _api_client.BaseApiClient, content: ContentType | None) -> types.Content: ...
def t_contents_for_embed(client: _api_client.BaseApiClient, contents: list[types.Content] | list[types.ContentDict] | ContentType): ...
def t_contents(client: _api_client.BaseApiClient, contents: types.ContentListUnion | types.ContentListUnionDict | None) -> list[types.Content]: ...
def handle_null_fields(schema: dict[str, Any]): ...
def process_schema(schema: dict[str, Any], client: _api_client.BaseApiClient, defs: dict[str, Any] | None = None, *, order_properties: bool = True): ...
def t_schema(client: _api_client.BaseApiClient, origin: types.SchemaUnionDict | Any) -> types.Schema | None: ...
def t_speech_config(_: _api_client.BaseApiClient, origin: types.SpeechConfigUnionDict | Any) -> types.SpeechConfig | None: ...
def t_tool(client: _api_client.BaseApiClient, origin) -> types.Tool | None: ...
def t_tools(client: _api_client.BaseApiClient, origin: list[Any]) -> list[types.Tool]: ...
def t_cached_content_name(client: _api_client.BaseApiClient, name: str): ...
def t_batch_job_source(client: _api_client.BaseApiClient, src: str): ...
def t_batch_job_destination(client: _api_client.BaseApiClient, dest: str): ...
def t_batch_job_name(client: _api_client.BaseApiClient, name: str): ...

LRO_POLLING_INITIAL_DELAY_SECONDS: float
LRO_POLLING_MAXIMUM_DELAY_SECONDS: float
LRO_POLLING_TIMEOUT_SECONDS: float
LRO_POLLING_MULTIPLIER: float

def t_resolve_operation(api_client: _api_client.BaseApiClient, struct: dict): ...
def t_file_name(api_client: _api_client.BaseApiClient, name: str | types.File | types.Video | types.GeneratedVideo | None): ...
def t_tuning_job_status(api_client: _api_client.BaseApiClient, status: str) -> types.JobState | str: ...
def t_bytes(api_client: _api_client.BaseApiClient, data: bytes) -> str: ...
