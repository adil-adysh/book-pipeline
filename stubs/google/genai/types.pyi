import datetime
import pydantic
import types as builtin_types
import typing
from . import _common
from _typeshed import Incomplete
from enum import Enum
from typing import Any, Callable, Literal
from typing_extensions import TypedDict

VersionedUnionType: Incomplete
PIL_Image: Incomplete
logger: Incomplete
T = typing.TypeVar('T', bound='GenerateContentResponse')

class Outcome(_common.CaseInSensitiveEnum):
    OUTCOME_UNSPECIFIED = 'OUTCOME_UNSPECIFIED'
    OUTCOME_OK = 'OUTCOME_OK'
    OUTCOME_FAILED = 'OUTCOME_FAILED'
    OUTCOME_DEADLINE_EXCEEDED = 'OUTCOME_DEADLINE_EXCEEDED'

class Language(_common.CaseInSensitiveEnum):
    LANGUAGE_UNSPECIFIED = 'LANGUAGE_UNSPECIFIED'
    PYTHON = 'PYTHON'

class Type(_common.CaseInSensitiveEnum):
    TYPE_UNSPECIFIED = 'TYPE_UNSPECIFIED'
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    INTEGER = 'INTEGER'
    BOOLEAN = 'BOOLEAN'
    ARRAY = 'ARRAY'
    OBJECT = 'OBJECT'

class HarmCategory(_common.CaseInSensitiveEnum):
    HARM_CATEGORY_UNSPECIFIED = 'HARM_CATEGORY_UNSPECIFIED'
    HARM_CATEGORY_HATE_SPEECH = 'HARM_CATEGORY_HATE_SPEECH'
    HARM_CATEGORY_DANGEROUS_CONTENT = 'HARM_CATEGORY_DANGEROUS_CONTENT'
    HARM_CATEGORY_HARASSMENT = 'HARM_CATEGORY_HARASSMENT'
    HARM_CATEGORY_SEXUALLY_EXPLICIT = 'HARM_CATEGORY_SEXUALLY_EXPLICIT'
    HARM_CATEGORY_CIVIC_INTEGRITY = 'HARM_CATEGORY_CIVIC_INTEGRITY'

class HarmBlockMethod(_common.CaseInSensitiveEnum):
    HARM_BLOCK_METHOD_UNSPECIFIED = 'HARM_BLOCK_METHOD_UNSPECIFIED'
    SEVERITY = 'SEVERITY'
    PROBABILITY = 'PROBABILITY'

class HarmBlockThreshold(_common.CaseInSensitiveEnum):
    HARM_BLOCK_THRESHOLD_UNSPECIFIED = 'HARM_BLOCK_THRESHOLD_UNSPECIFIED'
    BLOCK_LOW_AND_ABOVE = 'BLOCK_LOW_AND_ABOVE'
    BLOCK_MEDIUM_AND_ABOVE = 'BLOCK_MEDIUM_AND_ABOVE'
    BLOCK_ONLY_HIGH = 'BLOCK_ONLY_HIGH'
    BLOCK_NONE = 'BLOCK_NONE'
    OFF = 'OFF'

class Mode(_common.CaseInSensitiveEnum):
    MODE_UNSPECIFIED = 'MODE_UNSPECIFIED'
    MODE_DYNAMIC = 'MODE_DYNAMIC'

class State(_common.CaseInSensitiveEnum):
    STATE_UNSPECIFIED = 'STATE_UNSPECIFIED'
    ACTIVE = 'ACTIVE'
    ERROR = 'ERROR'

class FinishReason(_common.CaseInSensitiveEnum):
    FINISH_REASON_UNSPECIFIED = 'FINISH_REASON_UNSPECIFIED'
    STOP = 'STOP'
    MAX_TOKENS = 'MAX_TOKENS'
    SAFETY = 'SAFETY'
    RECITATION = 'RECITATION'
    OTHER = 'OTHER'
    BLOCKLIST = 'BLOCKLIST'
    PROHIBITED_CONTENT = 'PROHIBITED_CONTENT'
    SPII = 'SPII'
    MALFORMED_FUNCTION_CALL = 'MALFORMED_FUNCTION_CALL'

class HarmProbability(_common.CaseInSensitiveEnum):
    HARM_PROBABILITY_UNSPECIFIED = 'HARM_PROBABILITY_UNSPECIFIED'
    NEGLIGIBLE = 'NEGLIGIBLE'
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'

class HarmSeverity(_common.CaseInSensitiveEnum):
    HARM_SEVERITY_UNSPECIFIED = 'HARM_SEVERITY_UNSPECIFIED'
    HARM_SEVERITY_NEGLIGIBLE = 'HARM_SEVERITY_NEGLIGIBLE'
    HARM_SEVERITY_LOW = 'HARM_SEVERITY_LOW'
    HARM_SEVERITY_MEDIUM = 'HARM_SEVERITY_MEDIUM'
    HARM_SEVERITY_HIGH = 'HARM_SEVERITY_HIGH'

class BlockedReason(_common.CaseInSensitiveEnum):
    BLOCKED_REASON_UNSPECIFIED = 'BLOCKED_REASON_UNSPECIFIED'
    SAFETY = 'SAFETY'
    OTHER = 'OTHER'
    BLOCKLIST = 'BLOCKLIST'
    PROHIBITED_CONTENT = 'PROHIBITED_CONTENT'

class DeploymentResourcesType(_common.CaseInSensitiveEnum):
    DEPLOYMENT_RESOURCES_TYPE_UNSPECIFIED = 'DEPLOYMENT_RESOURCES_TYPE_UNSPECIFIED'
    DEDICATED_RESOURCES = 'DEDICATED_RESOURCES'
    AUTOMATIC_RESOURCES = 'AUTOMATIC_RESOURCES'
    SHARED_RESOURCES = 'SHARED_RESOURCES'

class JobState(_common.CaseInSensitiveEnum):
    JOB_STATE_UNSPECIFIED = 'JOB_STATE_UNSPECIFIED'
    JOB_STATE_QUEUED = 'JOB_STATE_QUEUED'
    JOB_STATE_PENDING = 'JOB_STATE_PENDING'
    JOB_STATE_RUNNING = 'JOB_STATE_RUNNING'
    JOB_STATE_SUCCEEDED = 'JOB_STATE_SUCCEEDED'
    JOB_STATE_FAILED = 'JOB_STATE_FAILED'
    JOB_STATE_CANCELLING = 'JOB_STATE_CANCELLING'
    JOB_STATE_CANCELLED = 'JOB_STATE_CANCELLED'
    JOB_STATE_PAUSED = 'JOB_STATE_PAUSED'
    JOB_STATE_EXPIRED = 'JOB_STATE_EXPIRED'
    JOB_STATE_UPDATING = 'JOB_STATE_UPDATING'
    JOB_STATE_PARTIALLY_SUCCEEDED = 'JOB_STATE_PARTIALLY_SUCCEEDED'

class AdapterSize(_common.CaseInSensitiveEnum):
    ADAPTER_SIZE_UNSPECIFIED = 'ADAPTER_SIZE_UNSPECIFIED'
    ADAPTER_SIZE_ONE = 'ADAPTER_SIZE_ONE'
    ADAPTER_SIZE_FOUR = 'ADAPTER_SIZE_FOUR'
    ADAPTER_SIZE_EIGHT = 'ADAPTER_SIZE_EIGHT'
    ADAPTER_SIZE_SIXTEEN = 'ADAPTER_SIZE_SIXTEEN'
    ADAPTER_SIZE_THIRTY_TWO = 'ADAPTER_SIZE_THIRTY_TWO'

class DynamicRetrievalConfigMode(_common.CaseInSensitiveEnum):
    MODE_UNSPECIFIED = 'MODE_UNSPECIFIED'
    MODE_DYNAMIC = 'MODE_DYNAMIC'

class FunctionCallingConfigMode(_common.CaseInSensitiveEnum):
    MODE_UNSPECIFIED = 'MODE_UNSPECIFIED'
    AUTO = 'AUTO'
    ANY = 'ANY'
    NONE = 'NONE'

class MediaResolution(_common.CaseInSensitiveEnum):
    MEDIA_RESOLUTION_UNSPECIFIED = 'MEDIA_RESOLUTION_UNSPECIFIED'
    MEDIA_RESOLUTION_LOW = 'MEDIA_RESOLUTION_LOW'
    MEDIA_RESOLUTION_MEDIUM = 'MEDIA_RESOLUTION_MEDIUM'
    MEDIA_RESOLUTION_HIGH = 'MEDIA_RESOLUTION_HIGH'

class SafetyFilterLevel(_common.CaseInSensitiveEnum):
    BLOCK_LOW_AND_ABOVE = 'BLOCK_LOW_AND_ABOVE'
    BLOCK_MEDIUM_AND_ABOVE = 'BLOCK_MEDIUM_AND_ABOVE'
    BLOCK_ONLY_HIGH = 'BLOCK_ONLY_HIGH'
    BLOCK_NONE = 'BLOCK_NONE'

class PersonGeneration(_common.CaseInSensitiveEnum):
    DONT_ALLOW = 'DONT_ALLOW'
    ALLOW_ADULT = 'ALLOW_ADULT'
    ALLOW_ALL = 'ALLOW_ALL'

class ImagePromptLanguage(_common.CaseInSensitiveEnum):
    auto = 'auto'
    en = 'en'
    ja = 'ja'
    ko = 'ko'
    hi = 'hi'

class MaskReferenceMode(_common.CaseInSensitiveEnum):
    MASK_MODE_DEFAULT = 'MASK_MODE_DEFAULT'
    MASK_MODE_USER_PROVIDED = 'MASK_MODE_USER_PROVIDED'
    MASK_MODE_BACKGROUND = 'MASK_MODE_BACKGROUND'
    MASK_MODE_FOREGROUND = 'MASK_MODE_FOREGROUND'
    MASK_MODE_SEMANTIC = 'MASK_MODE_SEMANTIC'

class ControlReferenceType(_common.CaseInSensitiveEnum):
    CONTROL_TYPE_DEFAULT = 'CONTROL_TYPE_DEFAULT'
    CONTROL_TYPE_CANNY = 'CONTROL_TYPE_CANNY'
    CONTROL_TYPE_SCRIBBLE = 'CONTROL_TYPE_SCRIBBLE'
    CONTROL_TYPE_FACE_MESH = 'CONTROL_TYPE_FACE_MESH'

class SubjectReferenceType(_common.CaseInSensitiveEnum):
    SUBJECT_TYPE_DEFAULT = 'SUBJECT_TYPE_DEFAULT'
    SUBJECT_TYPE_PERSON = 'SUBJECT_TYPE_PERSON'
    SUBJECT_TYPE_ANIMAL = 'SUBJECT_TYPE_ANIMAL'
    SUBJECT_TYPE_PRODUCT = 'SUBJECT_TYPE_PRODUCT'

class EditMode(_common.CaseInSensitiveEnum):
    EDIT_MODE_DEFAULT = 'EDIT_MODE_DEFAULT'
    EDIT_MODE_INPAINT_REMOVAL = 'EDIT_MODE_INPAINT_REMOVAL'
    EDIT_MODE_INPAINT_INSERTION = 'EDIT_MODE_INPAINT_INSERTION'
    EDIT_MODE_OUTPAINT = 'EDIT_MODE_OUTPAINT'
    EDIT_MODE_CONTROLLED_EDITING = 'EDIT_MODE_CONTROLLED_EDITING'
    EDIT_MODE_STYLE = 'EDIT_MODE_STYLE'
    EDIT_MODE_BGSWAP = 'EDIT_MODE_BGSWAP'
    EDIT_MODE_PRODUCT_IMAGE = 'EDIT_MODE_PRODUCT_IMAGE'

class FileState(_common.CaseInSensitiveEnum):
    STATE_UNSPECIFIED = 'STATE_UNSPECIFIED'
    PROCESSING = 'PROCESSING'
    ACTIVE = 'ACTIVE'
    FAILED = 'FAILED'

class FileSource(_common.CaseInSensitiveEnum):
    SOURCE_UNSPECIFIED = 'SOURCE_UNSPECIFIED'
    UPLOADED = 'UPLOADED'
    GENERATED = 'GENERATED'

class Modality(_common.CaseInSensitiveEnum):
    MODALITY_UNSPECIFIED = 'MODALITY_UNSPECIFIED'
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'
    AUDIO = 'AUDIO'

class VideoMetadata(_common.BaseModel):
    end_offset: str | None
    start_offset: str | None

class VideoMetadataDict(TypedDict, total=False):
    end_offset: str | None
    start_offset: str | None
VideoMetadataOrDict = VideoMetadata | VideoMetadataDict

class CodeExecutionResult(_common.BaseModel):
    outcome: Outcome | None
    output: str | None

class CodeExecutionResultDict(TypedDict, total=False):
    outcome: Outcome | None
    output: str | None
CodeExecutionResultOrDict = CodeExecutionResult | CodeExecutionResultDict

class ExecutableCode(_common.BaseModel):
    code: str | None
    language: Language | None

class ExecutableCodeDict(TypedDict, total=False):
    code: str | None
    language: Language | None
ExecutableCodeOrDict = ExecutableCode | ExecutableCodeDict

class FileData(_common.BaseModel):
    file_uri: str | None
    mime_type: str | None

class FileDataDict(TypedDict, total=False):
    file_uri: str | None
    mime_type: str | None
FileDataOrDict = FileData | FileDataDict

class FunctionCall(_common.BaseModel):
    id: str | None
    args: dict[str, Any] | None
    name: str | None

class FunctionCallDict(TypedDict, total=False):
    id: str | None
    args: dict[str, Any] | None
    name: str | None
FunctionCallOrDict = FunctionCall | FunctionCallDict

class FunctionResponse(_common.BaseModel):
    id: str | None
    name: str | None
    response: dict[str, Any] | None

class FunctionResponseDict(TypedDict, total=False):
    id: str | None
    name: str | None
    response: dict[str, Any] | None
FunctionResponseOrDict = FunctionResponse | FunctionResponseDict

class Blob(_common.BaseModel):
    data: bytes | None
    mime_type: str | None

class BlobDict(TypedDict, total=False):
    data: bytes | None
    mime_type: str | None
BlobOrDict = Blob | BlobDict

class Part(_common.BaseModel):
    video_metadata: VideoMetadata | None
    thought: bool | None
    code_execution_result: CodeExecutionResult | None
    executable_code: ExecutableCode | None
    file_data: FileData | None
    function_call: FunctionCall | None
    function_response: FunctionResponse | None
    inline_data: Blob | None
    text: str | None
    @classmethod
    def from_uri(cls, *, file_uri: str, mime_type: str) -> Part: ...
    @classmethod
    def from_text(cls, *, text: str) -> Part: ...
    @classmethod
    def from_bytes(cls, *, data: bytes, mime_type: str) -> Part: ...
    @classmethod
    def from_function_call(cls, *, name: str, args: dict[str, Any]) -> Part: ...
    @classmethod
    def from_function_response(cls, *, name: str, response: dict[str, Any]) -> Part: ...
    @classmethod
    def from_video_metadata(cls, *, start_offset: str, end_offset: str) -> Part: ...
    @classmethod
    def from_executable_code(cls, *, code: str, language: Language) -> Part: ...
    @classmethod
    def from_code_execution_result(cls, *, outcome: Outcome, output: str) -> Part: ...

class PartDict(TypedDict, total=False):
    video_metadata: VideoMetadataDict | None
    thought: bool | None
    code_execution_result: CodeExecutionResultDict | None
    executable_code: ExecutableCodeDict | None
    file_data: FileDataDict | None
    function_call: FunctionCallDict | None
    function_response: FunctionResponseDict | None
    inline_data: BlobDict | None
    text: str | None
PartOrDict = Part | PartDict

class Content(_common.BaseModel):
    parts: list[Part] | None
    role: str | None

class UserContent(Content):
    role: Literal['user']
    parts: list[Part]
    def __init__(self, parts: PartUnionDict | list['PartUnionDict']) -> None: ...

class ModelContent(Content):
    role: Literal['model']
    parts: list[Part]
    def __init__(self, parts: PartUnionDict | list['PartUnionDict']) -> None: ...

class ContentDict(TypedDict, total=False):
    parts: list[PartDict] | None
    role: str | None
ContentOrDict = Content | ContentDict

class HttpOptions(_common.BaseModel):
    base_url: str | None
    api_version: str | None
    headers: dict[str, str] | None
    timeout: int | None

class HttpOptionsDict(TypedDict, total=False):
    base_url: str | None
    api_version: str | None
    headers: dict[str, str] | None
    timeout: int | None
HttpOptionsOrDict = HttpOptions | HttpOptionsDict

class Schema(_common.BaseModel):
    example: Any | None
    pattern: str | None
    minimum: float | None
    default: Any | None
    any_of: list['Schema'] | None
    max_length: int | None
    title: str | None
    min_length: int | None
    min_properties: int | None
    maximum: float | None
    max_properties: int | None
    description: str | None
    enum: list[str] | None
    format: str | None
    items: Schema | None
    max_items: int | None
    min_items: int | None
    nullable: bool | None
    properties: dict[str, 'Schema'] | None
    property_ordering: list[str] | None
    required: list[str] | None
    type: Type | None

class SchemaDict(TypedDict, total=False):
    example: Any | None
    pattern: str | None
    minimum: float | None
    default: Any | None
    any_of: list['SchemaDict'] | None
    max_length: int | None
    title: str | None
    min_length: int | None
    min_properties: int | None
    maximum: float | None
    max_properties: int | None
    description: str | None
    enum: list[str] | None
    format: str | None
    items: SchemaDict | None
    max_items: int | None
    min_items: int | None
    nullable: bool | None
    properties: dict[str, 'SchemaDict'] | None
    property_ordering: list[str] | None
    required: list[str] | None
    type: Type | None
SchemaOrDict = Schema | SchemaDict

class SafetySetting(_common.BaseModel):
    method: HarmBlockMethod | None
    category: HarmCategory | None
    threshold: HarmBlockThreshold | None

class SafetySettingDict(TypedDict, total=False):
    method: HarmBlockMethod | None
    category: HarmCategory | None
    threshold: HarmBlockThreshold | None
SafetySettingOrDict = SafetySetting | SafetySettingDict

class FunctionDeclaration(_common.BaseModel):
    response: Schema | None
    description: str | None
    name: str | None
    parameters: Schema | None
    @classmethod
    def from_callable_with_api_option(cls, *, callable: Callable, api_option: Literal['VERTEX_AI', 'GEMINI_API'] = 'GEMINI_API') -> FunctionDeclaration: ...
    @classmethod
    def from_callable(cls, *, client, callable: Callable) -> FunctionDeclaration: ...

class FunctionDeclarationDict(TypedDict, total=False):
    response: SchemaDict | None
    description: str | None
    name: str | None
    parameters: SchemaDict | None
FunctionDeclarationOrDict = FunctionDeclaration | FunctionDeclarationDict

class GoogleSearch(_common.BaseModel): ...
class GoogleSearchDict(TypedDict, total=False): ...
GoogleSearchOrDict = GoogleSearch | GoogleSearchDict

class DynamicRetrievalConfig(_common.BaseModel):
    mode: DynamicRetrievalConfigMode | None
    dynamic_threshold: float | None

class DynamicRetrievalConfigDict(TypedDict, total=False):
    mode: DynamicRetrievalConfigMode | None
    dynamic_threshold: float | None
DynamicRetrievalConfigOrDict = DynamicRetrievalConfig | DynamicRetrievalConfigDict

class GoogleSearchRetrieval(_common.BaseModel):
    dynamic_retrieval_config: DynamicRetrievalConfig | None

class GoogleSearchRetrievalDict(TypedDict, total=False):
    dynamic_retrieval_config: DynamicRetrievalConfigDict | None
GoogleSearchRetrievalOrDict = GoogleSearchRetrieval | GoogleSearchRetrievalDict

class VertexAISearch(_common.BaseModel):
    datastore: str | None

class VertexAISearchDict(TypedDict, total=False):
    datastore: str | None
VertexAISearchOrDict = VertexAISearch | VertexAISearchDict

class VertexRagStoreRagResource(_common.BaseModel):
    rag_corpus: str | None
    rag_file_ids: list[str] | None

class VertexRagStoreRagResourceDict(TypedDict, total=False):
    rag_corpus: str | None
    rag_file_ids: list[str] | None
VertexRagStoreRagResourceOrDict = VertexRagStoreRagResource | VertexRagStoreRagResourceDict

class VertexRagStore(_common.BaseModel):
    rag_corpora: list[str] | None
    rag_resources: list[VertexRagStoreRagResource] | None
    similarity_top_k: int | None
    vector_distance_threshold: float | None

class VertexRagStoreDict(TypedDict, total=False):
    rag_corpora: list[str] | None
    rag_resources: list[VertexRagStoreRagResourceDict] | None
    similarity_top_k: int | None
    vector_distance_threshold: float | None
VertexRagStoreOrDict = VertexRagStore | VertexRagStoreDict

class Retrieval(_common.BaseModel):
    disable_attribution: bool | None
    vertex_ai_search: VertexAISearch | None
    vertex_rag_store: VertexRagStore | None

class RetrievalDict(TypedDict, total=False):
    disable_attribution: bool | None
    vertex_ai_search: VertexAISearchDict | None
    vertex_rag_store: VertexRagStoreDict | None
RetrievalOrDict = Retrieval | RetrievalDict

class ToolCodeExecution(_common.BaseModel): ...
class ToolCodeExecutionDict(TypedDict, total=False): ...
ToolCodeExecutionOrDict = ToolCodeExecution | ToolCodeExecutionDict

class Tool(_common.BaseModel):
    function_declarations: list[FunctionDeclaration] | None
    retrieval: Retrieval | None
    google_search: GoogleSearch | None
    google_search_retrieval: GoogleSearchRetrieval | None
    code_execution: ToolCodeExecution | None

class ToolDict(TypedDict, total=False):
    function_declarations: list[FunctionDeclarationDict] | None
    retrieval: RetrievalDict | None
    google_search: GoogleSearchDict | None
    google_search_retrieval: GoogleSearchRetrievalDict | None
    code_execution: ToolCodeExecutionDict | None
ToolOrDict = Tool | ToolDict
ToolListUnion = list[Tool | Callable]
ToolListUnionDict = list[ToolDict | Callable]

class FunctionCallingConfig(_common.BaseModel):
    mode: FunctionCallingConfigMode | None
    allowed_function_names: list[str] | None

class FunctionCallingConfigDict(TypedDict, total=False):
    mode: FunctionCallingConfigMode | None
    allowed_function_names: list[str] | None
FunctionCallingConfigOrDict = FunctionCallingConfig | FunctionCallingConfigDict

class ToolConfig(_common.BaseModel):
    function_calling_config: FunctionCallingConfig | None

class ToolConfigDict(TypedDict, total=False):
    function_calling_config: FunctionCallingConfigDict | None
ToolConfigOrDict = ToolConfig | ToolConfigDict

class PrebuiltVoiceConfig(_common.BaseModel):
    voice_name: str | None

class PrebuiltVoiceConfigDict(TypedDict, total=False):
    voice_name: str | None
PrebuiltVoiceConfigOrDict = PrebuiltVoiceConfig | PrebuiltVoiceConfigDict

class VoiceConfig(_common.BaseModel):
    prebuilt_voice_config: PrebuiltVoiceConfig | None

class VoiceConfigDict(TypedDict, total=False):
    prebuilt_voice_config: PrebuiltVoiceConfigDict | None
VoiceConfigOrDict = VoiceConfig | VoiceConfigDict

class SpeechConfig(_common.BaseModel):
    voice_config: VoiceConfig | None

class SpeechConfigDict(TypedDict, total=False):
    voice_config: VoiceConfigDict | None
SpeechConfigOrDict = SpeechConfig | SpeechConfigDict

class AutomaticFunctionCallingConfig(_common.BaseModel):
    disable: bool | None
    maximum_remote_calls: int | None
    ignore_call_history: bool | None

class AutomaticFunctionCallingConfigDict(TypedDict, total=False):
    disable: bool | None
    maximum_remote_calls: int | None
    ignore_call_history: bool | None
AutomaticFunctionCallingConfigOrDict = AutomaticFunctionCallingConfig | AutomaticFunctionCallingConfigDict

class ThinkingConfig(_common.BaseModel):
    include_thoughts: bool | None

class ThinkingConfigDict(TypedDict, total=False):
    include_thoughts: bool | None
ThinkingConfigOrDict = ThinkingConfig | ThinkingConfigDict

class FileStatus(_common.BaseModel):
    details: list[dict[str, Any]] | None
    message: str | None
    code: int | None

class FileStatusDict(TypedDict, total=False):
    details: list[dict[str, Any]] | None
    message: str | None
    code: int | None
FileStatusOrDict = FileStatus | FileStatusDict

class File(_common.BaseModel):
    name: str | None
    display_name: str | None
    mime_type: str | None
    size_bytes: int | None
    create_time: datetime.datetime | None
    expiration_time: datetime.datetime | None
    update_time: datetime.datetime | None
    sha256_hash: str | None
    uri: str | None
    download_uri: str | None
    state: FileState | None
    source: FileSource | None
    video_metadata: dict[str, Any] | None
    error: FileStatus | None

class FileDict(TypedDict, total=False):
    name: str | None
    display_name: str | None
    mime_type: str | None
    size_bytes: int | None
    create_time: datetime.datetime | None
    expiration_time: datetime.datetime | None
    update_time: datetime.datetime | None
    sha256_hash: str | None
    uri: str | None
    download_uri: str | None
    state: FileState | None
    source: FileSource | None
    video_metadata: dict[str, Any] | None
    error: FileStatusDict | None
FileOrDict = File | FileDict
PartUnion = File | Part | PIL_Image | str
PartUnion = File | Part | str
PartUnionDict = PartUnion | PartDict
ContentUnion = Content | list[PartUnion] | PartUnion
ContentUnionDict = ContentUnion | ContentDict
SchemaUnion = dict | type | Schema | builtin_types.GenericAlias | VersionedUnionType
SchemaUnionDict = SchemaUnion | SchemaDict

class GenerationConfigRoutingConfigAutoRoutingMode(_common.BaseModel):
    model_routing_preference: Literal['UNKNOWN', 'PRIORITIZE_QUALITY', 'BALANCED', 'PRIORITIZE_COST'] | None

class GenerationConfigRoutingConfigAutoRoutingModeDict(TypedDict, total=False):
    model_routing_preference: Literal['UNKNOWN', 'PRIORITIZE_QUALITY', 'BALANCED', 'PRIORITIZE_COST'] | None
GenerationConfigRoutingConfigAutoRoutingModeOrDict = GenerationConfigRoutingConfigAutoRoutingMode | GenerationConfigRoutingConfigAutoRoutingModeDict

class GenerationConfigRoutingConfigManualRoutingMode(_common.BaseModel):
    model_name: str | None

class GenerationConfigRoutingConfigManualRoutingModeDict(TypedDict, total=False):
    model_name: str | None
GenerationConfigRoutingConfigManualRoutingModeOrDict = GenerationConfigRoutingConfigManualRoutingMode | GenerationConfigRoutingConfigManualRoutingModeDict

class GenerationConfigRoutingConfig(_common.BaseModel):
    auto_mode: GenerationConfigRoutingConfigAutoRoutingMode | None
    manual_mode: GenerationConfigRoutingConfigManualRoutingMode | None

class GenerationConfigRoutingConfigDict(TypedDict, total=False):
    auto_mode: GenerationConfigRoutingConfigAutoRoutingModeDict | None
    manual_mode: GenerationConfigRoutingConfigManualRoutingModeDict | None
GenerationConfigRoutingConfigOrDict = GenerationConfigRoutingConfig | GenerationConfigRoutingConfigDict
SpeechConfigUnion = SpeechConfig | str
SpeechConfigUnionDict = SpeechConfigUnion | SpeechConfigDict

class GenerateContentConfig(_common.BaseModel):
    http_options: HttpOptions | None
    system_instruction: ContentUnion | None
    temperature: float | None
    top_p: float | None
    top_k: float | None
    candidate_count: int | None
    max_output_tokens: int | None
    stop_sequences: list[str] | None
    response_logprobs: bool | None
    logprobs: int | None
    presence_penalty: float | None
    frequency_penalty: float | None
    seed: int | None
    response_mime_type: str | None
    response_schema: SchemaUnion | None
    routing_config: GenerationConfigRoutingConfig | None
    safety_settings: list[SafetySetting] | None
    tools: ToolListUnion | None
    tool_config: ToolConfig | None
    labels: dict[str, str] | None
    cached_content: str | None
    response_modalities: list[str] | None
    media_resolution: MediaResolution | None
    speech_config: SpeechConfigUnion | None
    audio_timestamp: bool | None
    automatic_function_calling: AutomaticFunctionCallingConfig | None
    thinking_config: ThinkingConfig | None

class GenerateContentConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
    system_instruction: ContentUnionDict | None
    temperature: float | None
    top_p: float | None
    top_k: float | None
    candidate_count: int | None
    max_output_tokens: int | None
    stop_sequences: list[str] | None
    response_logprobs: bool | None
    logprobs: int | None
    presence_penalty: float | None
    frequency_penalty: float | None
    seed: int | None
    response_mime_type: str | None
    response_schema: SchemaUnionDict | None
    routing_config: GenerationConfigRoutingConfigDict | None
    safety_settings: list[SafetySettingDict] | None
    tools: ToolListUnionDict | None
    tool_config: ToolConfigDict | None
    labels: dict[str, str] | None
    cached_content: str | None
    response_modalities: list[str] | None
    media_resolution: MediaResolution | None
    speech_config: SpeechConfigUnionDict | None
    audio_timestamp: bool | None
    automatic_function_calling: AutomaticFunctionCallingConfigDict | None
    thinking_config: ThinkingConfigDict | None
GenerateContentConfigOrDict = GenerateContentConfig | GenerateContentConfigDict
ContentListUnion = list[ContentUnion] | ContentUnion
ContentListUnionDict = list[ContentUnionDict] | ContentUnionDict

class _GenerateContentParameters(_common.BaseModel):
    model: str | None
    contents: ContentListUnion | None
    config: GenerateContentConfig | None

class _GenerateContentParametersDict(TypedDict, total=False):
    model: str | None
    contents: ContentListUnionDict | None
    config: GenerateContentConfigDict | None

class GoogleTypeDate(_common.BaseModel):
    day: int | None
    month: int | None
    year: int | None

class GoogleTypeDateDict(TypedDict, total=False):
    day: int | None
    month: int | None
    year: int | None
GoogleTypeDateOrDict = GoogleTypeDate | GoogleTypeDateDict

class Citation(_common.BaseModel):
    end_index: int | None
    license: str | None
    publication_date: GoogleTypeDate | None
    start_index: int | None
    title: str | None
    uri: str | None

class CitationDict(TypedDict, total=False):
    end_index: int | None
    license: str | None
    publication_date: GoogleTypeDateDict | None
    start_index: int | None
    title: str | None
    uri: str | None
CitationOrDict = Citation | CitationDict

class CitationMetadata(_common.BaseModel):
    citations: list[Citation] | None

class CitationMetadataDict(TypedDict, total=False):
    citations: list[CitationDict] | None
CitationMetadataOrDict = CitationMetadata | CitationMetadataDict

class GroundingChunkRetrievedContext(_common.BaseModel):
    text: str | None
    title: str | None
    uri: str | None

class GroundingChunkRetrievedContextDict(TypedDict, total=False):
    text: str | None
    title: str | None
    uri: str | None
GroundingChunkRetrievedContextOrDict = GroundingChunkRetrievedContext | GroundingChunkRetrievedContextDict

class GroundingChunkWeb(_common.BaseModel):
    title: str | None
    uri: str | None

class GroundingChunkWebDict(TypedDict, total=False):
    title: str | None
    uri: str | None
GroundingChunkWebOrDict = GroundingChunkWeb | GroundingChunkWebDict

class GroundingChunk(_common.BaseModel):
    retrieved_context: GroundingChunkRetrievedContext | None
    web: GroundingChunkWeb | None

class GroundingChunkDict(TypedDict, total=False):
    retrieved_context: GroundingChunkRetrievedContextDict | None
    web: GroundingChunkWebDict | None
GroundingChunkOrDict = GroundingChunk | GroundingChunkDict

class Segment(_common.BaseModel):
    end_index: int | None
    part_index: int | None
    start_index: int | None
    text: str | None

class SegmentDict(TypedDict, total=False):
    end_index: int | None
    part_index: int | None
    start_index: int | None
    text: str | None
SegmentOrDict = Segment | SegmentDict

class GroundingSupport(_common.BaseModel):
    confidence_scores: list[float] | None
    grounding_chunk_indices: list[int] | None
    segment: Segment | None

class GroundingSupportDict(TypedDict, total=False):
    confidence_scores: list[float] | None
    grounding_chunk_indices: list[int] | None
    segment: SegmentDict | None
GroundingSupportOrDict = GroundingSupport | GroundingSupportDict

class RetrievalMetadata(_common.BaseModel):
    google_search_dynamic_retrieval_score: float | None

class RetrievalMetadataDict(TypedDict, total=False):
    google_search_dynamic_retrieval_score: float | None
RetrievalMetadataOrDict = RetrievalMetadata | RetrievalMetadataDict

class SearchEntryPoint(_common.BaseModel):
    rendered_content: str | None
    sdk_blob: bytes | None

class SearchEntryPointDict(TypedDict, total=False):
    rendered_content: str | None
    sdk_blob: bytes | None
SearchEntryPointOrDict = SearchEntryPoint | SearchEntryPointDict

class GroundingMetadata(_common.BaseModel):
    grounding_chunks: list[GroundingChunk] | None
    grounding_supports: list[GroundingSupport] | None
    retrieval_metadata: RetrievalMetadata | None
    retrieval_queries: list[str] | None
    search_entry_point: SearchEntryPoint | None
    web_search_queries: list[str] | None

class GroundingMetadataDict(TypedDict, total=False):
    grounding_chunks: list[GroundingChunkDict] | None
    grounding_supports: list[GroundingSupportDict] | None
    retrieval_metadata: RetrievalMetadataDict | None
    retrieval_queries: list[str] | None
    search_entry_point: SearchEntryPointDict | None
    web_search_queries: list[str] | None
GroundingMetadataOrDict = GroundingMetadata | GroundingMetadataDict

class LogprobsResultCandidate(_common.BaseModel):
    log_probability: float | None
    token: str | None
    token_id: int | None

class LogprobsResultCandidateDict(TypedDict, total=False):
    log_probability: float | None
    token: str | None
    token_id: int | None
LogprobsResultCandidateOrDict = LogprobsResultCandidate | LogprobsResultCandidateDict

class LogprobsResultTopCandidates(_common.BaseModel):
    candidates: list[LogprobsResultCandidate] | None

class LogprobsResultTopCandidatesDict(TypedDict, total=False):
    candidates: list[LogprobsResultCandidateDict] | None
LogprobsResultTopCandidatesOrDict = LogprobsResultTopCandidates | LogprobsResultTopCandidatesDict

class LogprobsResult(_common.BaseModel):
    chosen_candidates: list[LogprobsResultCandidate] | None
    top_candidates: list[LogprobsResultTopCandidates] | None

class LogprobsResultDict(TypedDict, total=False):
    chosen_candidates: list[LogprobsResultCandidateDict] | None
    top_candidates: list[LogprobsResultTopCandidatesDict] | None
LogprobsResultOrDict = LogprobsResult | LogprobsResultDict

class SafetyRating(_common.BaseModel):
    blocked: bool | None
    category: HarmCategory | None
    probability: HarmProbability | None
    probability_score: float | None
    severity: HarmSeverity | None
    severity_score: float | None

class SafetyRatingDict(TypedDict, total=False):
    blocked: bool | None
    category: HarmCategory | None
    probability: HarmProbability | None
    probability_score: float | None
    severity: HarmSeverity | None
    severity_score: float | None
SafetyRatingOrDict = SafetyRating | SafetyRatingDict

class Candidate(_common.BaseModel):
    content: Content | None
    citation_metadata: CitationMetadata | None
    finish_message: str | None
    token_count: int | None
    avg_logprobs: float | None
    finish_reason: FinishReason | None
    grounding_metadata: GroundingMetadata | None
    index: int | None
    logprobs_result: LogprobsResult | None
    safety_ratings: list[SafetyRating] | None

class CandidateDict(TypedDict, total=False):
    content: ContentDict | None
    citation_metadata: CitationMetadataDict | None
    finish_message: str | None
    token_count: int | None
    avg_logprobs: float | None
    finish_reason: FinishReason | None
    grounding_metadata: GroundingMetadataDict | None
    index: int | None
    logprobs_result: LogprobsResultDict | None
    safety_ratings: list[SafetyRatingDict] | None
CandidateOrDict = Candidate | CandidateDict

class GenerateContentResponsePromptFeedback(_common.BaseModel):
    block_reason: BlockedReason | None
    block_reason_message: str | None
    safety_ratings: list[SafetyRating] | None

class GenerateContentResponsePromptFeedbackDict(TypedDict, total=False):
    block_reason: BlockedReason | None
    block_reason_message: str | None
    safety_ratings: list[SafetyRatingDict] | None
GenerateContentResponsePromptFeedbackOrDict = GenerateContentResponsePromptFeedback | GenerateContentResponsePromptFeedbackDict

class GenerateContentResponseUsageMetadata(_common.BaseModel):
    cached_content_token_count: int | None
    candidates_token_count: int | None
    prompt_token_count: int | None
    total_token_count: int | None

class GenerateContentResponseUsageMetadataDict(TypedDict, total=False):
    cached_content_token_count: int | None
    candidates_token_count: int | None
    prompt_token_count: int | None
    total_token_count: int | None
GenerateContentResponseUsageMetadataOrDict = GenerateContentResponseUsageMetadata | GenerateContentResponseUsageMetadataDict

class GenerateContentResponse(_common.BaseModel):
    candidates: list[Candidate] | None
    create_time: datetime.datetime | None
    response_id: str | None
    model_version: str | None
    prompt_feedback: GenerateContentResponsePromptFeedback | None
    usage_metadata: GenerateContentResponseUsageMetadata | None
    automatic_function_calling_history: list[Content] | None
    parsed: pydantic.BaseModel | dict | Enum | None
    @property
    def text(self) -> str | None: ...
    @property
    def function_calls(self) -> list[FunctionCall] | None: ...
    @property
    def executable_code(self) -> str | None: ...
    @property
    def code_execution_result(self) -> str | None: ...

class GenerateContentResponseDict(TypedDict, total=False):
    candidates: list[CandidateDict] | None
    create_time: datetime.datetime | None
    response_id: str | None
    model_version: str | None
    prompt_feedback: GenerateContentResponsePromptFeedbackDict | None
    usage_metadata: GenerateContentResponseUsageMetadataDict | None
GenerateContentResponseOrDict = GenerateContentResponse | GenerateContentResponseDict

class EmbedContentConfig(_common.BaseModel):
    http_options: HttpOptions | None
    task_type: str | None
    title: str | None
    output_dimensionality: int | None
    mime_type: str | None
    auto_truncate: bool | None

class EmbedContentConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
    task_type: str | None
    title: str | None
    output_dimensionality: int | None
    mime_type: str | None
    auto_truncate: bool | None
EmbedContentConfigOrDict = EmbedContentConfig | EmbedContentConfigDict

class _EmbedContentParameters(_common.BaseModel):
    model: str | None
    contents: ContentListUnion | None
    config: EmbedContentConfig | None

class _EmbedContentParametersDict(TypedDict, total=False):
    model: str | None
    contents: ContentListUnionDict | None
    config: EmbedContentConfigDict | None

class ContentEmbeddingStatistics(_common.BaseModel):
    truncated: bool | None
    token_count: float | None

class ContentEmbeddingStatisticsDict(TypedDict, total=False):
    truncated: bool | None
    token_count: float | None
ContentEmbeddingStatisticsOrDict = ContentEmbeddingStatistics | ContentEmbeddingStatisticsDict

class ContentEmbedding(_common.BaseModel):
    values: list[float] | None
    statistics: ContentEmbeddingStatistics | None

class ContentEmbeddingDict(TypedDict, total=False):
    values: list[float] | None
    statistics: ContentEmbeddingStatisticsDict | None
ContentEmbeddingOrDict = ContentEmbedding | ContentEmbeddingDict

class EmbedContentMetadata(_common.BaseModel):
    billable_character_count: int | None

class EmbedContentMetadataDict(TypedDict, total=False):
    billable_character_count: int | None
EmbedContentMetadataOrDict = EmbedContentMetadata | EmbedContentMetadataDict

class EmbedContentResponse(_common.BaseModel):
    embeddings: list[ContentEmbedding] | None
    metadata: EmbedContentMetadata | None

class EmbedContentResponseDict(TypedDict, total=False):
    embeddings: list[ContentEmbeddingDict] | None
    metadata: EmbedContentMetadataDict | None
EmbedContentResponseOrDict = EmbedContentResponse | EmbedContentResponseDict

class GenerateImagesConfig(_common.BaseModel):
    http_options: HttpOptions | None
    output_gcs_uri: str | None
    negative_prompt: str | None
    number_of_images: int | None
    aspect_ratio: str | None
    guidance_scale: float | None
    seed: int | None
    safety_filter_level: SafetyFilterLevel | None
    person_generation: PersonGeneration | None
    include_safety_attributes: bool | None
    include_rai_reason: bool | None
    language: ImagePromptLanguage | None
    output_mime_type: str | None
    output_compression_quality: int | None
    add_watermark: bool | None
    enhance_prompt: bool | None

class GenerateImagesConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
    output_gcs_uri: str | None
    negative_prompt: str | None
    number_of_images: int | None
    aspect_ratio: str | None
    guidance_scale: float | None
    seed: int | None
    safety_filter_level: SafetyFilterLevel | None
    person_generation: PersonGeneration | None
    include_safety_attributes: bool | None
    include_rai_reason: bool | None
    language: ImagePromptLanguage | None
    output_mime_type: str | None
    output_compression_quality: int | None
    add_watermark: bool | None
    enhance_prompt: bool | None
GenerateImagesConfigOrDict = GenerateImagesConfig | GenerateImagesConfigDict

class _GenerateImagesParameters(_common.BaseModel):
    model: str | None
    prompt: str | None
    config: GenerateImagesConfig | None

class _GenerateImagesParametersDict(TypedDict, total=False):
    model: str | None
    prompt: str | None
    config: GenerateImagesConfigDict | None

class Image(_common.BaseModel):
    gcs_uri: str | None
    image_bytes: bytes | None
    mime_type: str | None
    @classmethod
    def from_file(cls, *, location: str, mime_type: str | None = None) -> Image: ...
    def show(self) -> None: ...
    def save(self, location: str): ...

JOB_STATES_SUCCEEDED_VERTEX: Incomplete
JOB_STATES_SUCCEEDED_MLDEV: Incomplete
JOB_STATES_SUCCEEDED: Incomplete
JOB_STATES_ENDED_VERTEX: Incomplete
JOB_STATES_ENDED_MLDEV: Incomplete
JOB_STATES_ENDED: Incomplete

class ImageDict(TypedDict, total=False):
    gcs_uri: str | None
    image_bytes: bytes | None
    mime_type: str | None
ImageOrDict = Image | ImageDict

class GeneratedImage(_common.BaseModel):
    image: Image | None
    rai_filtered_reason: str | None
    enhanced_prompt: str | None

class GeneratedImageDict(TypedDict, total=False):
    image: ImageDict | None
    rai_filtered_reason: str | None
    enhanced_prompt: str | None
GeneratedImageOrDict = GeneratedImage | GeneratedImageDict

class GenerateImagesResponse(_common.BaseModel):
    generated_images: list[GeneratedImage] | None

class GenerateImagesResponseDict(TypedDict, total=False):
    generated_images: list[GeneratedImageDict] | None
GenerateImagesResponseOrDict = GenerateImagesResponse | GenerateImagesResponseDict

class MaskReferenceConfig(_common.BaseModel):
    mask_mode: MaskReferenceMode | None
    segmentation_classes: list[int] | None
    mask_dilation: float | None

class MaskReferenceConfigDict(TypedDict, total=False):
    mask_mode: MaskReferenceMode | None
    segmentation_classes: list[int] | None
    mask_dilation: float | None
MaskReferenceConfigOrDict = MaskReferenceConfig | MaskReferenceConfigDict

class ControlReferenceConfig(_common.BaseModel):
    control_type: ControlReferenceType | None
    enable_control_image_computation: bool | None

class ControlReferenceConfigDict(TypedDict, total=False):
    control_type: ControlReferenceType | None
    enable_control_image_computation: bool | None
ControlReferenceConfigOrDict = ControlReferenceConfig | ControlReferenceConfigDict

class StyleReferenceConfig(_common.BaseModel):
    style_description: str | None

class StyleReferenceConfigDict(TypedDict, total=False):
    style_description: str | None
StyleReferenceConfigOrDict = StyleReferenceConfig | StyleReferenceConfigDict

class SubjectReferenceConfig(_common.BaseModel):
    subject_type: SubjectReferenceType | None
    subject_description: str | None

class SubjectReferenceConfigDict(TypedDict, total=False):
    subject_type: SubjectReferenceType | None
    subject_description: str | None
SubjectReferenceConfigOrDict = SubjectReferenceConfig | SubjectReferenceConfigDict

class _ReferenceImageAPI(_common.BaseModel):
    reference_image: Image | None
    reference_id: int | None
    reference_type: str | None
    mask_image_config: MaskReferenceConfig | None
    control_image_config: ControlReferenceConfig | None
    style_image_config: StyleReferenceConfig | None
    subject_image_config: SubjectReferenceConfig | None

class _ReferenceImageAPIDict(TypedDict, total=False):
    reference_image: ImageDict | None
    reference_id: int | None
    reference_type: str | None
    mask_image_config: MaskReferenceConfigDict | None
    control_image_config: ControlReferenceConfigDict | None
    style_image_config: StyleReferenceConfigDict | None
    subject_image_config: SubjectReferenceConfigDict | None

class EditImageConfig(_common.BaseModel):
    http_options: HttpOptions | None
    output_gcs_uri: str | None
    negative_prompt: str | None
    number_of_images: int | None
    aspect_ratio: str | None
    guidance_scale: float | None
    seed: int | None
    safety_filter_level: SafetyFilterLevel | None
    person_generation: PersonGeneration | None
    include_safety_attributes: bool | None
    include_rai_reason: bool | None
    language: ImagePromptLanguage | None
    output_mime_type: str | None
    output_compression_quality: int | None
    edit_mode: EditMode | None

class EditImageConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
    output_gcs_uri: str | None
    negative_prompt: str | None
    number_of_images: int | None
    aspect_ratio: str | None
    guidance_scale: float | None
    seed: int | None
    safety_filter_level: SafetyFilterLevel | None
    person_generation: PersonGeneration | None
    include_safety_attributes: bool | None
    include_rai_reason: bool | None
    language: ImagePromptLanguage | None
    output_mime_type: str | None
    output_compression_quality: int | None
    edit_mode: EditMode | None
EditImageConfigOrDict = EditImageConfig | EditImageConfigDict

class _EditImageParameters(_common.BaseModel):
    model: str | None
    prompt: str | None
    reference_images: list[_ReferenceImageAPI] | None
    config: EditImageConfig | None

class _EditImageParametersDict(TypedDict, total=False):
    model: str | None
    prompt: str | None
    reference_images: list[_ReferenceImageAPIDict] | None
    config: EditImageConfigDict | None

class EditImageResponse(_common.BaseModel):
    generated_images: list[GeneratedImage] | None

class EditImageResponseDict(TypedDict, total=False):
    generated_images: list[GeneratedImageDict] | None
EditImageResponseOrDict = EditImageResponse | EditImageResponseDict

class _UpscaleImageAPIConfig(_common.BaseModel):
    http_options: HttpOptions | None
    include_rai_reason: bool | None
    output_mime_type: str | None
    output_compression_quality: int | None
    number_of_images: int | None
    mode: str | None

class _UpscaleImageAPIConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
    include_rai_reason: bool | None
    output_mime_type: str | None
    output_compression_quality: int | None
    number_of_images: int | None
    mode: str | None

class _UpscaleImageAPIParameters(_common.BaseModel):
    model: str | None
    image: Image | None
    upscale_factor: str | None
    config: _UpscaleImageAPIConfig | None

class _UpscaleImageAPIParametersDict(TypedDict, total=False):
    model: str | None
    image: ImageDict | None
    upscale_factor: str | None
    config: _UpscaleImageAPIConfigDict | None

class UpscaleImageResponse(_common.BaseModel):
    generated_images: list[GeneratedImage] | None

class UpscaleImageResponseDict(TypedDict, total=False):
    generated_images: list[GeneratedImageDict] | None
UpscaleImageResponseOrDict = UpscaleImageResponse | UpscaleImageResponseDict

class GetModelConfig(_common.BaseModel):
    http_options: HttpOptions | None

class GetModelConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
GetModelConfigOrDict = GetModelConfig | GetModelConfigDict

class _GetModelParameters(_common.BaseModel):
    model: str | None
    config: GetModelConfig | None

class _GetModelParametersDict(TypedDict, total=False):
    model: str | None
    config: GetModelConfigDict | None

class Endpoint(_common.BaseModel):
    name: str | None
    deployed_model_id: str | None

class EndpointDict(TypedDict, total=False):
    name: str | None
    deployed_model_id: str | None
EndpointOrDict = Endpoint | EndpointDict

class TunedModelInfo(_common.BaseModel):
    base_model: str | None
    create_time: datetime.datetime | None
    update_time: datetime.datetime | None

class TunedModelInfoDict(TypedDict, total=False):
    base_model: str | None
    create_time: datetime.datetime | None
    update_time: datetime.datetime | None
TunedModelInfoOrDict = TunedModelInfo | TunedModelInfoDict

class Model(_common.BaseModel):
    name: str | None
    display_name: str | None
    description: str | None
    version: str | None
    endpoints: list[Endpoint] | None
    labels: dict[str, str] | None
    tuned_model_info: TunedModelInfo | None
    input_token_limit: int | None
    output_token_limit: int | None
    supported_actions: list[str] | None

class ModelDict(TypedDict, total=False):
    name: str | None
    display_name: str | None
    description: str | None
    version: str | None
    endpoints: list[EndpointDict] | None
    labels: dict[str, str] | None
    tuned_model_info: TunedModelInfoDict | None
    input_token_limit: int | None
    output_token_limit: int | None
    supported_actions: list[str] | None
ModelOrDict = Model | ModelDict

class ListModelsConfig(_common.BaseModel):
    http_options: HttpOptions | None
    page_size: int | None
    page_token: str | None
    filter: str | None
    query_base: bool | None

class ListModelsConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
    page_size: int | None
    page_token: str | None
    filter: str | None
    query_base: bool | None
ListModelsConfigOrDict = ListModelsConfig | ListModelsConfigDict

class _ListModelsParameters(_common.BaseModel):
    config: ListModelsConfig | None

class _ListModelsParametersDict(TypedDict, total=False):
    config: ListModelsConfigDict | None

class ListModelsResponse(_common.BaseModel):
    next_page_token: str | None
    models: list[Model] | None

class ListModelsResponseDict(TypedDict, total=False):
    next_page_token: str | None
    models: list[ModelDict] | None
ListModelsResponseOrDict = ListModelsResponse | ListModelsResponseDict

class UpdateModelConfig(_common.BaseModel):
    http_options: HttpOptions | None
    display_name: str | None
    description: str | None

class UpdateModelConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
    display_name: str | None
    description: str | None
UpdateModelConfigOrDict = UpdateModelConfig | UpdateModelConfigDict

class _UpdateModelParameters(_common.BaseModel):
    model: str | None
    config: UpdateModelConfig | None

class _UpdateModelParametersDict(TypedDict, total=False):
    model: str | None
    config: UpdateModelConfigDict | None

class DeleteModelConfig(_common.BaseModel):
    http_options: HttpOptions | None

class DeleteModelConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
DeleteModelConfigOrDict = DeleteModelConfig | DeleteModelConfigDict

class _DeleteModelParameters(_common.BaseModel):
    model: str | None
    config: DeleteModelConfig | None

class _DeleteModelParametersDict(TypedDict, total=False):
    model: str | None
    config: DeleteModelConfigDict | None

class DeleteModelResponse(_common.BaseModel): ...
class DeleteModelResponseDict(TypedDict, total=False): ...
DeleteModelResponseOrDict = DeleteModelResponse | DeleteModelResponseDict

class GenerationConfig(_common.BaseModel):
    audio_timestamp: bool | None
    candidate_count: int | None
    frequency_penalty: float | None
    logprobs: int | None
    max_output_tokens: int | None
    presence_penalty: float | None
    response_logprobs: bool | None
    response_mime_type: str | None
    response_schema: Schema | None
    routing_config: GenerationConfigRoutingConfig | None
    seed: int | None
    stop_sequences: list[str] | None
    temperature: float | None
    top_k: float | None
    top_p: float | None

class GenerationConfigDict(TypedDict, total=False):
    audio_timestamp: bool | None
    candidate_count: int | None
    frequency_penalty: float | None
    logprobs: int | None
    max_output_tokens: int | None
    presence_penalty: float | None
    response_logprobs: bool | None
    response_mime_type: str | None
    response_schema: SchemaDict | None
    routing_config: GenerationConfigRoutingConfigDict | None
    seed: int | None
    stop_sequences: list[str] | None
    temperature: float | None
    top_k: float | None
    top_p: float | None
GenerationConfigOrDict = GenerationConfig | GenerationConfigDict

class CountTokensConfig(_common.BaseModel):
    http_options: HttpOptions | None
    system_instruction: ContentUnion | None
    tools: list[Tool] | None
    generation_config: GenerationConfig | None

class CountTokensConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
    system_instruction: ContentUnionDict | None
    tools: list[ToolDict] | None
    generation_config: GenerationConfigDict | None
CountTokensConfigOrDict = CountTokensConfig | CountTokensConfigDict

class _CountTokensParameters(_common.BaseModel):
    model: str | None
    contents: ContentListUnion | None
    config: CountTokensConfig | None

class _CountTokensParametersDict(TypedDict, total=False):
    model: str | None
    contents: ContentListUnionDict | None
    config: CountTokensConfigDict | None

class CountTokensResponse(_common.BaseModel):
    total_tokens: int | None
    cached_content_token_count: int | None

class CountTokensResponseDict(TypedDict, total=False):
    total_tokens: int | None
    cached_content_token_count: int | None
CountTokensResponseOrDict = CountTokensResponse | CountTokensResponseDict

class ComputeTokensConfig(_common.BaseModel):
    http_options: HttpOptions | None

class ComputeTokensConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
ComputeTokensConfigOrDict = ComputeTokensConfig | ComputeTokensConfigDict

class _ComputeTokensParameters(_common.BaseModel):
    model: str | None
    contents: ContentListUnion | None
    config: ComputeTokensConfig | None

class _ComputeTokensParametersDict(TypedDict, total=False):
    model: str | None
    contents: ContentListUnionDict | None
    config: ComputeTokensConfigDict | None

class TokensInfo(_common.BaseModel):
    role: str | None
    token_ids: list[int] | None
    tokens: list[bytes] | None

class TokensInfoDict(TypedDict, total=False):
    role: str | None
    token_ids: list[int] | None
    tokens: list[bytes] | None
TokensInfoOrDict = TokensInfo | TokensInfoDict

class ComputeTokensResponse(_common.BaseModel):
    tokens_info: list[TokensInfo] | None

class ComputeTokensResponseDict(TypedDict, total=False):
    tokens_info: list[TokensInfoDict] | None
ComputeTokensResponseOrDict = ComputeTokensResponse | ComputeTokensResponseDict

class GenerateVideosConfig(_common.BaseModel):
    http_options: HttpOptions | None
    number_of_videos: int | None
    output_gcs_uri: str | None
    fps: int | None
    duration_seconds: int | None
    seed: int | None
    aspect_ratio: str | None
    resolution: str | None
    person_generation: str | None
    pubsub_topic: str | None
    negative_prompt: str | None
    enhance_prompt: bool | None

class GenerateVideosConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
    number_of_videos: int | None
    output_gcs_uri: str | None
    fps: int | None
    duration_seconds: int | None
    seed: int | None
    aspect_ratio: str | None
    resolution: str | None
    person_generation: str | None
    pubsub_topic: str | None
    negative_prompt: str | None
    enhance_prompt: bool | None
GenerateVideosConfigOrDict = GenerateVideosConfig | GenerateVideosConfigDict

class _GenerateVideosParameters(_common.BaseModel):
    model: str | None
    prompt: str | None
    image: Image | None
    config: GenerateVideosConfig | None

class _GenerateVideosParametersDict(TypedDict, total=False):
    model: str | None
    prompt: str | None
    image: ImageDict | None
    config: GenerateVideosConfigDict | None

class Video(_common.BaseModel):
    uri: str | None
    video_bytes: bytes | None
    mime_type: str | None
    def save(self, path: str) -> None: ...
    def show(self): ...

class VideoDict(TypedDict, total=False):
    uri: str | None
    video_bytes: bytes | None
    mime_type: str | None
VideoOrDict = Video | VideoDict

class GeneratedVideo(_common.BaseModel):
    video: Video | None

class GeneratedVideoDict(TypedDict, total=False):
    video: VideoDict | None
GeneratedVideoOrDict = GeneratedVideo | GeneratedVideoDict

class GenerateVideosResponse(_common.BaseModel):
    generated_videos: list[GeneratedVideo] | None
    rai_media_filtered_count: int | None
    rai_media_filtered_reasons: list[str] | None

class GenerateVideosResponseDict(TypedDict, total=False):
    generated_videos: list[GeneratedVideoDict] | None
    rai_media_filtered_count: int | None
    rai_media_filtered_reasons: list[str] | None
GenerateVideosResponseOrDict = GenerateVideosResponse | GenerateVideosResponseDict

class GenerateVideosOperation(_common.BaseModel):
    name: str | None
    metadata: dict[str, Any] | None
    done: bool | None
    error: dict[str, Any] | None
    response: dict[str, Any] | None
    result: GenerateVideosResponse | None

class GenerateVideosOperationDict(TypedDict, total=False):
    name: str | None
    metadata: dict[str, Any] | None
    done: bool | None
    error: dict[str, Any] | None
    response: dict[str, Any] | None
    result: GenerateVideosResponseDict | None
GenerateVideosOperationOrDict = GenerateVideosOperation | GenerateVideosOperationDict

class GetTuningJobConfig(_common.BaseModel):
    http_options: HttpOptions | None

class GetTuningJobConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
GetTuningJobConfigOrDict = GetTuningJobConfig | GetTuningJobConfigDict

class _GetTuningJobParameters(_common.BaseModel):
    name: str | None
    config: GetTuningJobConfig | None

class _GetTuningJobParametersDict(TypedDict, total=False):
    name: str | None
    config: GetTuningJobConfigDict | None

class TunedModel(_common.BaseModel):
    model: str | None
    endpoint: str | None

class TunedModelDict(TypedDict, total=False):
    model: str | None
    endpoint: str | None
TunedModelOrDict = TunedModel | TunedModelDict

class GoogleRpcStatus(_common.BaseModel):
    code: int | None
    details: list[dict[str, Any]] | None
    message: str | None

class GoogleRpcStatusDict(TypedDict, total=False):
    code: int | None
    details: list[dict[str, Any]] | None
    message: str | None
GoogleRpcStatusOrDict = GoogleRpcStatus | GoogleRpcStatusDict

class SupervisedHyperParameters(_common.BaseModel):
    adapter_size: AdapterSize | None
    epoch_count: int | None
    learning_rate_multiplier: float | None

class SupervisedHyperParametersDict(TypedDict, total=False):
    adapter_size: AdapterSize | None
    epoch_count: int | None
    learning_rate_multiplier: float | None
SupervisedHyperParametersOrDict = SupervisedHyperParameters | SupervisedHyperParametersDict

class SupervisedTuningSpec(_common.BaseModel):
    hyper_parameters: SupervisedHyperParameters | None
    training_dataset_uri: str | None
    validation_dataset_uri: str | None

class SupervisedTuningSpecDict(TypedDict, total=False):
    hyper_parameters: SupervisedHyperParametersDict | None
    training_dataset_uri: str | None
    validation_dataset_uri: str | None
SupervisedTuningSpecOrDict = SupervisedTuningSpec | SupervisedTuningSpecDict

class DatasetDistributionDistributionBucket(_common.BaseModel):
    count: int | None
    left: float | None
    right: float | None

class DatasetDistributionDistributionBucketDict(TypedDict, total=False):
    count: int | None
    left: float | None
    right: float | None
DatasetDistributionDistributionBucketOrDict = DatasetDistributionDistributionBucket | DatasetDistributionDistributionBucketDict

class DatasetDistribution(_common.BaseModel):
    buckets: list[DatasetDistributionDistributionBucket] | None
    max: float | None
    mean: float | None
    median: float | None
    min: float | None
    p5: float | None
    p95: float | None
    sum: float | None

class DatasetDistributionDict(TypedDict, total=False):
    buckets: list[DatasetDistributionDistributionBucketDict] | None
    max: float | None
    mean: float | None
    median: float | None
    min: float | None
    p5: float | None
    p95: float | None
    sum: float | None
DatasetDistributionOrDict = DatasetDistribution | DatasetDistributionDict

class DatasetStats(_common.BaseModel):
    total_billable_character_count: int | None
    total_tuning_character_count: int | None
    tuning_dataset_example_count: int | None
    tuning_step_count: int | None
    user_dataset_examples: list[Content] | None
    user_input_token_distribution: DatasetDistribution | None
    user_message_per_example_distribution: DatasetDistribution | None
    user_output_token_distribution: DatasetDistribution | None

class DatasetStatsDict(TypedDict, total=False):
    total_billable_character_count: int | None
    total_tuning_character_count: int | None
    tuning_dataset_example_count: int | None
    tuning_step_count: int | None
    user_dataset_examples: list[ContentDict] | None
    user_input_token_distribution: DatasetDistributionDict | None
    user_message_per_example_distribution: DatasetDistributionDict | None
    user_output_token_distribution: DatasetDistributionDict | None
DatasetStatsOrDict = DatasetStats | DatasetStatsDict

class DistillationDataStats(_common.BaseModel):
    training_dataset_stats: DatasetStats | None

class DistillationDataStatsDict(TypedDict, total=False):
    training_dataset_stats: DatasetStatsDict | None
DistillationDataStatsOrDict = DistillationDataStats | DistillationDataStatsDict

class SupervisedTuningDatasetDistributionDatasetBucket(_common.BaseModel):
    count: float | None
    left: float | None
    right: float | None

class SupervisedTuningDatasetDistributionDatasetBucketDict(TypedDict, total=False):
    count: float | None
    left: float | None
    right: float | None
SupervisedTuningDatasetDistributionDatasetBucketOrDict = SupervisedTuningDatasetDistributionDatasetBucket | SupervisedTuningDatasetDistributionDatasetBucketDict

class SupervisedTuningDatasetDistribution(_common.BaseModel):
    billable_sum: int | None
    buckets: list[SupervisedTuningDatasetDistributionDatasetBucket] | None
    max: float | None
    mean: float | None
    median: float | None
    min: float | None
    p5: float | None
    p95: float | None
    sum: int | None

class SupervisedTuningDatasetDistributionDict(TypedDict, total=False):
    billable_sum: int | None
    buckets: list[SupervisedTuningDatasetDistributionDatasetBucketDict] | None
    max: float | None
    mean: float | None
    median: float | None
    min: float | None
    p5: float | None
    p95: float | None
    sum: int | None
SupervisedTuningDatasetDistributionOrDict = SupervisedTuningDatasetDistribution | SupervisedTuningDatasetDistributionDict

class SupervisedTuningDataStats(_common.BaseModel):
    total_billable_character_count: int | None
    total_billable_token_count: int | None
    total_truncated_example_count: int | None
    total_tuning_character_count: int | None
    truncated_example_indices: list[int] | None
    tuning_dataset_example_count: int | None
    tuning_step_count: int | None
    user_dataset_examples: list[Content] | None
    user_input_token_distribution: SupervisedTuningDatasetDistribution | None
    user_message_per_example_distribution: SupervisedTuningDatasetDistribution | None
    user_output_token_distribution: SupervisedTuningDatasetDistribution | None

class SupervisedTuningDataStatsDict(TypedDict, total=False):
    total_billable_character_count: int | None
    total_billable_token_count: int | None
    total_truncated_example_count: int | None
    total_tuning_character_count: int | None
    truncated_example_indices: list[int] | None
    tuning_dataset_example_count: int | None
    tuning_step_count: int | None
    user_dataset_examples: list[ContentDict] | None
    user_input_token_distribution: SupervisedTuningDatasetDistributionDict | None
    user_message_per_example_distribution: SupervisedTuningDatasetDistributionDict | None
    user_output_token_distribution: SupervisedTuningDatasetDistributionDict | None
SupervisedTuningDataStatsOrDict = SupervisedTuningDataStats | SupervisedTuningDataStatsDict

class TuningDataStats(_common.BaseModel):
    distillation_data_stats: DistillationDataStats | None
    supervised_tuning_data_stats: SupervisedTuningDataStats | None

class TuningDataStatsDict(TypedDict, total=False):
    distillation_data_stats: DistillationDataStatsDict | None
    supervised_tuning_data_stats: SupervisedTuningDataStatsDict | None
TuningDataStatsOrDict = TuningDataStats | TuningDataStatsDict

class EncryptionSpec(_common.BaseModel):
    kms_key_name: str | None

class EncryptionSpecDict(TypedDict, total=False):
    kms_key_name: str | None
EncryptionSpecOrDict = EncryptionSpec | EncryptionSpecDict

class PartnerModelTuningSpec(_common.BaseModel):
    hyper_parameters: dict[str, Any] | None
    training_dataset_uri: str | None
    validation_dataset_uri: str | None

class PartnerModelTuningSpecDict(TypedDict, total=False):
    hyper_parameters: dict[str, Any] | None
    training_dataset_uri: str | None
    validation_dataset_uri: str | None
PartnerModelTuningSpecOrDict = PartnerModelTuningSpec | PartnerModelTuningSpecDict

class DistillationHyperParameters(_common.BaseModel):
    adapter_size: AdapterSize | None
    epoch_count: int | None
    learning_rate_multiplier: float | None

class DistillationHyperParametersDict(TypedDict, total=False):
    adapter_size: AdapterSize | None
    epoch_count: int | None
    learning_rate_multiplier: float | None
DistillationHyperParametersOrDict = DistillationHyperParameters | DistillationHyperParametersDict

class DistillationSpec(_common.BaseModel):
    base_teacher_model: str | None
    hyper_parameters: DistillationHyperParameters | None
    pipeline_root_directory: str | None
    student_model: str | None
    training_dataset_uri: str | None
    tuned_teacher_model_source: str | None
    validation_dataset_uri: str | None

class DistillationSpecDict(TypedDict, total=False):
    base_teacher_model: str | None
    hyper_parameters: DistillationHyperParametersDict | None
    pipeline_root_directory: str | None
    student_model: str | None
    training_dataset_uri: str | None
    tuned_teacher_model_source: str | None
    validation_dataset_uri: str | None
DistillationSpecOrDict = DistillationSpec | DistillationSpecDict

class TuningJob(_common.BaseModel):
    name: str | None
    state: JobState | None
    create_time: datetime.datetime | None
    start_time: datetime.datetime | None
    end_time: datetime.datetime | None
    update_time: datetime.datetime | None
    error: GoogleRpcStatus | None
    description: str | None
    base_model: str | None
    tuned_model: TunedModel | None
    supervised_tuning_spec: SupervisedTuningSpec | None
    tuning_data_stats: TuningDataStats | None
    encryption_spec: EncryptionSpec | None
    partner_model_tuning_spec: PartnerModelTuningSpec | None
    distillation_spec: DistillationSpec | None
    experiment: str | None
    labels: dict[str, str] | None
    pipeline_job: str | None
    tuned_model_display_name: str | None
    @property
    def has_ended(self) -> bool: ...
    @property
    def has_succeeded(self) -> bool: ...

class TuningJobDict(TypedDict, total=False):
    name: str | None
    state: JobState | None
    create_time: datetime.datetime | None
    start_time: datetime.datetime | None
    end_time: datetime.datetime | None
    update_time: datetime.datetime | None
    error: GoogleRpcStatusDict | None
    description: str | None
    base_model: str | None
    tuned_model: TunedModelDict | None
    supervised_tuning_spec: SupervisedTuningSpecDict | None
    tuning_data_stats: TuningDataStatsDict | None
    encryption_spec: EncryptionSpecDict | None
    partner_model_tuning_spec: PartnerModelTuningSpecDict | None
    distillation_spec: DistillationSpecDict | None
    experiment: str | None
    labels: dict[str, str] | None
    pipeline_job: str | None
    tuned_model_display_name: str | None
TuningJobOrDict = TuningJob | TuningJobDict

class ListTuningJobsConfig(_common.BaseModel):
    http_options: HttpOptions | None
    page_size: int | None
    page_token: str | None
    filter: str | None

class ListTuningJobsConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
    page_size: int | None
    page_token: str | None
    filter: str | None
ListTuningJobsConfigOrDict = ListTuningJobsConfig | ListTuningJobsConfigDict

class _ListTuningJobsParameters(_common.BaseModel):
    config: ListTuningJobsConfig | None

class _ListTuningJobsParametersDict(TypedDict, total=False):
    config: ListTuningJobsConfigDict | None

class ListTuningJobsResponse(_common.BaseModel):
    next_page_token: str | None
    tuning_jobs: list[TuningJob] | None

class ListTuningJobsResponseDict(TypedDict, total=False):
    next_page_token: str | None
    tuning_jobs: list[TuningJobDict] | None
ListTuningJobsResponseOrDict = ListTuningJobsResponse | ListTuningJobsResponseDict

class TuningExample(_common.BaseModel):
    text_input: str | None
    output: str | None

class TuningExampleDict(TypedDict, total=False):
    text_input: str | None
    output: str | None
TuningExampleOrDict = TuningExample | TuningExampleDict

class TuningDataset(_common.BaseModel):
    gcs_uri: str | None
    examples: list[TuningExample] | None

class TuningDatasetDict(TypedDict, total=False):
    gcs_uri: str | None
    examples: list[TuningExampleDict] | None
TuningDatasetOrDict = TuningDataset | TuningDatasetDict

class TuningValidationDataset(_common.BaseModel):
    gcs_uri: str | None

class TuningValidationDatasetDict(TypedDict, total=False):
    gcs_uri: str | None
TuningValidationDatasetOrDict = TuningValidationDataset | TuningValidationDatasetDict

class CreateTuningJobConfig(_common.BaseModel):
    http_options: HttpOptions | None
    validation_dataset: TuningValidationDataset | None
    tuned_model_display_name: str | None
    description: str | None
    epoch_count: int | None
    learning_rate_multiplier: float | None
    adapter_size: AdapterSize | None
    batch_size: int | None
    learning_rate: float | None

class CreateTuningJobConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
    validation_dataset: TuningValidationDatasetDict | None
    tuned_model_display_name: str | None
    description: str | None
    epoch_count: int | None
    learning_rate_multiplier: float | None
    adapter_size: AdapterSize | None
    batch_size: int | None
    learning_rate: float | None
CreateTuningJobConfigOrDict = CreateTuningJobConfig | CreateTuningJobConfigDict

class _CreateTuningJobParameters(_common.BaseModel):
    base_model: str | None
    training_dataset: TuningDataset | None
    config: CreateTuningJobConfig | None

class _CreateTuningJobParametersDict(TypedDict, total=False):
    base_model: str | None
    training_dataset: TuningDatasetDict | None
    config: CreateTuningJobConfigDict | None

class Operation(_common.BaseModel):
    name: str | None
    metadata: dict[str, Any] | None
    done: bool | None
    error: dict[str, Any] | None
    response: dict[str, Any] | None

class OperationDict(TypedDict, total=False):
    name: str | None
    metadata: dict[str, Any] | None
    done: bool | None
    error: dict[str, Any] | None
    response: dict[str, Any] | None
OperationOrDict = Operation | OperationDict

class CreateCachedContentConfig(_common.BaseModel):
    http_options: HttpOptions | None
    ttl: str | None
    expire_time: datetime.datetime | None
    display_name: str | None
    contents: ContentListUnion | None
    system_instruction: ContentUnion | None
    tools: list[Tool] | None
    tool_config: ToolConfig | None

class CreateCachedContentConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
    ttl: str | None
    expire_time: datetime.datetime | None
    display_name: str | None
    contents: ContentListUnionDict | None
    system_instruction: ContentUnionDict | None
    tools: list[ToolDict] | None
    tool_config: ToolConfigDict | None
CreateCachedContentConfigOrDict = CreateCachedContentConfig | CreateCachedContentConfigDict

class _CreateCachedContentParameters(_common.BaseModel):
    model: str | None
    config: CreateCachedContentConfig | None

class _CreateCachedContentParametersDict(TypedDict, total=False):
    model: str | None
    config: CreateCachedContentConfigDict | None

class CachedContentUsageMetadata(_common.BaseModel):
    audio_duration_seconds: int | None
    image_count: int | None
    text_count: int | None
    total_token_count: int | None
    video_duration_seconds: int | None

class CachedContentUsageMetadataDict(TypedDict, total=False):
    audio_duration_seconds: int | None
    image_count: int | None
    text_count: int | None
    total_token_count: int | None
    video_duration_seconds: int | None
CachedContentUsageMetadataOrDict = CachedContentUsageMetadata | CachedContentUsageMetadataDict

class CachedContent(_common.BaseModel):
    name: str | None
    display_name: str | None
    model: str | None
    create_time: datetime.datetime | None
    update_time: datetime.datetime | None
    expire_time: datetime.datetime | None
    usage_metadata: CachedContentUsageMetadata | None

class CachedContentDict(TypedDict, total=False):
    name: str | None
    display_name: str | None
    model: str | None
    create_time: datetime.datetime | None
    update_time: datetime.datetime | None
    expire_time: datetime.datetime | None
    usage_metadata: CachedContentUsageMetadataDict | None
CachedContentOrDict = CachedContent | CachedContentDict

class GetCachedContentConfig(_common.BaseModel):
    http_options: HttpOptions | None

class GetCachedContentConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
GetCachedContentConfigOrDict = GetCachedContentConfig | GetCachedContentConfigDict

class _GetCachedContentParameters(_common.BaseModel):
    name: str | None
    config: GetCachedContentConfig | None

class _GetCachedContentParametersDict(TypedDict, total=False):
    name: str | None
    config: GetCachedContentConfigDict | None

class DeleteCachedContentConfig(_common.BaseModel):
    http_options: HttpOptions | None

class DeleteCachedContentConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
DeleteCachedContentConfigOrDict = DeleteCachedContentConfig | DeleteCachedContentConfigDict

class _DeleteCachedContentParameters(_common.BaseModel):
    name: str | None
    config: DeleteCachedContentConfig | None

class _DeleteCachedContentParametersDict(TypedDict, total=False):
    name: str | None
    config: DeleteCachedContentConfigDict | None

class DeleteCachedContentResponse(_common.BaseModel): ...
class DeleteCachedContentResponseDict(TypedDict, total=False): ...
DeleteCachedContentResponseOrDict = DeleteCachedContentResponse | DeleteCachedContentResponseDict

class UpdateCachedContentConfig(_common.BaseModel):
    http_options: HttpOptions | None
    ttl: str | None
    expire_time: datetime.datetime | None

class UpdateCachedContentConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
    ttl: str | None
    expire_time: datetime.datetime | None
UpdateCachedContentConfigOrDict = UpdateCachedContentConfig | UpdateCachedContentConfigDict

class _UpdateCachedContentParameters(_common.BaseModel):
    name: str | None
    config: UpdateCachedContentConfig | None

class _UpdateCachedContentParametersDict(TypedDict, total=False):
    name: str | None
    config: UpdateCachedContentConfigDict | None

class ListCachedContentsConfig(_common.BaseModel):
    http_options: HttpOptions | None
    page_size: int | None
    page_token: str | None

class ListCachedContentsConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
    page_size: int | None
    page_token: str | None
ListCachedContentsConfigOrDict = ListCachedContentsConfig | ListCachedContentsConfigDict

class _ListCachedContentsParameters(_common.BaseModel):
    config: ListCachedContentsConfig | None

class _ListCachedContentsParametersDict(TypedDict, total=False):
    config: ListCachedContentsConfigDict | None

class ListCachedContentsResponse(_common.BaseModel):
    next_page_token: str | None
    cached_contents: list[CachedContent] | None

class ListCachedContentsResponseDict(TypedDict, total=False):
    next_page_token: str | None
    cached_contents: list[CachedContentDict] | None
ListCachedContentsResponseOrDict = ListCachedContentsResponse | ListCachedContentsResponseDict

class ListFilesConfig(_common.BaseModel):
    http_options: HttpOptions | None
    page_size: int | None
    page_token: str | None

class ListFilesConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
    page_size: int | None
    page_token: str | None
ListFilesConfigOrDict = ListFilesConfig | ListFilesConfigDict

class _ListFilesParameters(_common.BaseModel):
    config: ListFilesConfig | None

class _ListFilesParametersDict(TypedDict, total=False):
    config: ListFilesConfigDict | None

class ListFilesResponse(_common.BaseModel):
    next_page_token: str | None
    files: list[File] | None

class ListFilesResponseDict(TypedDict, total=False):
    next_page_token: str | None
    files: list[FileDict] | None
ListFilesResponseOrDict = ListFilesResponse | ListFilesResponseDict

class CreateFileConfig(_common.BaseModel):
    http_options: HttpOptions | None

class CreateFileConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
CreateFileConfigOrDict = CreateFileConfig | CreateFileConfigDict

class _CreateFileParameters(_common.BaseModel):
    file: File | None
    config: CreateFileConfig | None

class _CreateFileParametersDict(TypedDict, total=False):
    file: FileDict | None
    config: CreateFileConfigDict | None

class CreateFileResponse(_common.BaseModel):
    http_headers: dict[str, str] | None

class CreateFileResponseDict(TypedDict, total=False):
    http_headers: dict[str, str] | None
CreateFileResponseOrDict = CreateFileResponse | CreateFileResponseDict

class GetFileConfig(_common.BaseModel):
    http_options: HttpOptions | None

class GetFileConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
GetFileConfigOrDict = GetFileConfig | GetFileConfigDict

class _GetFileParameters(_common.BaseModel):
    name: str | None
    config: GetFileConfig | None

class _GetFileParametersDict(TypedDict, total=False):
    name: str | None
    config: GetFileConfigDict | None

class DeleteFileConfig(_common.BaseModel):
    http_options: HttpOptions | None

class DeleteFileConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
DeleteFileConfigOrDict = DeleteFileConfig | DeleteFileConfigDict

class _DeleteFileParameters(_common.BaseModel):
    name: str | None
    config: DeleteFileConfig | None

class _DeleteFileParametersDict(TypedDict, total=False):
    name: str | None
    config: DeleteFileConfigDict | None

class DeleteFileResponse(_common.BaseModel): ...
class DeleteFileResponseDict(TypedDict, total=False): ...
DeleteFileResponseOrDict = DeleteFileResponse | DeleteFileResponseDict

class BatchJobSource(_common.BaseModel):
    format: str | None
    gcs_uri: list[str] | None
    bigquery_uri: str | None

class BatchJobSourceDict(TypedDict, total=False):
    format: str | None
    gcs_uri: list[str] | None
    bigquery_uri: str | None
BatchJobSourceOrDict = BatchJobSource | BatchJobSourceDict

class BatchJobDestination(_common.BaseModel):
    format: str | None
    gcs_uri: str | None
    bigquery_uri: str | None

class BatchJobDestinationDict(TypedDict, total=False):
    format: str | None
    gcs_uri: str | None
    bigquery_uri: str | None
BatchJobDestinationOrDict = BatchJobDestination | BatchJobDestinationDict

class CreateBatchJobConfig(_common.BaseModel):
    http_options: HttpOptions | None
    display_name: str | None
    dest: str | None

class CreateBatchJobConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
    display_name: str | None
    dest: str | None
CreateBatchJobConfigOrDict = CreateBatchJobConfig | CreateBatchJobConfigDict

class _CreateBatchJobParameters(_common.BaseModel):
    model: str | None
    src: str | None
    config: CreateBatchJobConfig | None

class _CreateBatchJobParametersDict(TypedDict, total=False):
    model: str | None
    src: str | None
    config: CreateBatchJobConfigDict | None

class JobError(_common.BaseModel):
    details: list[str] | None
    code: int | None
    message: str | None

class JobErrorDict(TypedDict, total=False):
    details: list[str] | None
    code: int | None
    message: str | None
JobErrorOrDict = JobError | JobErrorDict

class BatchJob(_common.BaseModel):
    name: str | None
    display_name: str | None
    state: JobState | None
    error: JobError | None
    create_time: datetime.datetime | None
    start_time: datetime.datetime | None
    end_time: datetime.datetime | None
    update_time: datetime.datetime | None
    model: str | None
    src: BatchJobSource | None
    dest: BatchJobDestination | None

class BatchJobDict(TypedDict, total=False):
    name: str | None
    display_name: str | None
    state: JobState | None
    error: JobErrorDict | None
    create_time: datetime.datetime | None
    start_time: datetime.datetime | None
    end_time: datetime.datetime | None
    update_time: datetime.datetime | None
    model: str | None
    src: BatchJobSourceDict | None
    dest: BatchJobDestinationDict | None
BatchJobOrDict = BatchJob | BatchJobDict

class GetBatchJobConfig(_common.BaseModel):
    http_options: HttpOptions | None

class GetBatchJobConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
GetBatchJobConfigOrDict = GetBatchJobConfig | GetBatchJobConfigDict

class _GetBatchJobParameters(_common.BaseModel):
    name: str | None
    config: GetBatchJobConfig | None

class _GetBatchJobParametersDict(TypedDict, total=False):
    name: str | None
    config: GetBatchJobConfigDict | None

class CancelBatchJobConfig(_common.BaseModel):
    http_options: HttpOptions | None

class CancelBatchJobConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
CancelBatchJobConfigOrDict = CancelBatchJobConfig | CancelBatchJobConfigDict

class _CancelBatchJobParameters(_common.BaseModel):
    name: str | None
    config: CancelBatchJobConfig | None

class _CancelBatchJobParametersDict(TypedDict, total=False):
    name: str | None
    config: CancelBatchJobConfigDict | None

class ListBatchJobsConfig(_common.BaseModel):
    http_options: HttpOptions | None
    page_size: int | None
    page_token: str | None
    filter: str | None

class ListBatchJobsConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
    page_size: int | None
    page_token: str | None
    filter: str | None
ListBatchJobsConfigOrDict = ListBatchJobsConfig | ListBatchJobsConfigDict

class _ListBatchJobsParameters(_common.BaseModel):
    config: ListBatchJobsConfig | None

class _ListBatchJobsParametersDict(TypedDict, total=False):
    config: ListBatchJobsConfigDict | None

class ListBatchJobsResponse(_common.BaseModel):
    next_page_token: str | None
    batch_jobs: list[BatchJob] | None

class ListBatchJobsResponseDict(TypedDict, total=False):
    next_page_token: str | None
    batch_jobs: list[BatchJobDict] | None
ListBatchJobsResponseOrDict = ListBatchJobsResponse | ListBatchJobsResponseDict

class DeleteBatchJobConfig(_common.BaseModel):
    http_options: HttpOptions | None

class DeleteBatchJobConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
DeleteBatchJobConfigOrDict = DeleteBatchJobConfig | DeleteBatchJobConfigDict

class _DeleteBatchJobParameters(_common.BaseModel):
    name: str | None
    config: DeleteBatchJobConfig | None

class _DeleteBatchJobParametersDict(TypedDict, total=False):
    name: str | None
    config: DeleteBatchJobConfigDict | None

class DeleteResourceJob(_common.BaseModel):
    name: str | None
    done: bool | None
    error: JobError | None

class DeleteResourceJobDict(TypedDict, total=False):
    name: str | None
    done: bool | None
    error: JobErrorDict | None
DeleteResourceJobOrDict = DeleteResourceJob | DeleteResourceJobDict

class GetOperationConfig(_common.BaseModel):
    http_options: HttpOptions | None

class GetOperationConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
GetOperationConfigOrDict = GetOperationConfig | GetOperationConfigDict

class _GetOperationParameters(_common.BaseModel):
    operation_name: str | None
    config: GetOperationConfig | None

class _GetOperationParametersDict(TypedDict, total=False):
    operation_name: str | None
    config: GetOperationConfigDict | None

class FetchPredictOperationConfig(_common.BaseModel):
    http_options: HttpOptions | None

class FetchPredictOperationConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
FetchPredictOperationConfigOrDict = FetchPredictOperationConfig | FetchPredictOperationConfigDict

class _FetchPredictOperationParameters(_common.BaseModel):
    operation_name: str | None
    resource_name: str | None
    config: FetchPredictOperationConfig | None

class _FetchPredictOperationParametersDict(TypedDict, total=False):
    operation_name: str | None
    resource_name: str | None
    config: FetchPredictOperationConfigDict | None

class TestTableItem(_common.BaseModel):
    name: str | None
    parameters: dict[str, Any] | None
    exception_if_mldev: str | None
    exception_if_vertex: str | None
    override_replay_id: str | None
    has_union: bool | None
    skip_in_api_mode: str | None

class TestTableItemDict(TypedDict, total=False):
    name: str | None
    parameters: dict[str, Any] | None
    exception_if_mldev: str | None
    exception_if_vertex: str | None
    override_replay_id: str | None
    has_union: bool | None
    skip_in_api_mode: str | None
TestTableItemOrDict = TestTableItem | TestTableItemDict

class TestTableFile(_common.BaseModel):
    comment: str | None
    test_method: str | None
    parameter_names: list[str] | None
    test_table: list[TestTableItem] | None

class TestTableFileDict(TypedDict, total=False):
    comment: str | None
    test_method: str | None
    parameter_names: list[str] | None
    test_table: list[TestTableItemDict] | None
TestTableFileOrDict = TestTableFile | TestTableFileDict

class ReplayRequest(_common.BaseModel):
    method: str | None
    url: str | None
    headers: dict[str, str] | None
    body_segments: list[dict[str, Any]] | None

class ReplayRequestDict(TypedDict, total=False):
    method: str | None
    url: str | None
    headers: dict[str, str] | None
    body_segments: list[dict[str, Any]] | None
ReplayRequestOrDict = ReplayRequest | ReplayRequestDict

class ReplayResponse(_common.BaseModel):
    status_code: int | None
    headers: dict[str, str] | None
    body_segments: list[dict[str, Any]] | None
    sdk_response_segments: list[dict[str, Any]] | None

class ReplayResponseDict(TypedDict, total=False):
    status_code: int | None
    headers: dict[str, str] | None
    body_segments: list[dict[str, Any]] | None
    sdk_response_segments: list[dict[str, Any]] | None
ReplayResponseOrDict = ReplayResponse | ReplayResponseDict

class ReplayInteraction(_common.BaseModel):
    request: ReplayRequest | None
    response: ReplayResponse | None

class ReplayInteractionDict(TypedDict, total=False):
    request: ReplayRequestDict | None
    response: ReplayResponseDict | None
ReplayInteractionOrDict = ReplayInteraction | ReplayInteractionDict

class ReplayFile(_common.BaseModel):
    replay_id: str | None
    interactions: list[ReplayInteraction] | None

class ReplayFileDict(TypedDict, total=False):
    replay_id: str | None
    interactions: list[ReplayInteractionDict] | None
ReplayFileOrDict = ReplayFile | ReplayFileDict

class UploadFileConfig(_common.BaseModel):
    http_options: HttpOptions | None
    name: str | None
    mime_type: str | None
    display_name: str | None

class UploadFileConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
    name: str | None
    mime_type: str | None
    display_name: str | None
UploadFileConfigOrDict = UploadFileConfig | UploadFileConfigDict

class DownloadFileConfig(_common.BaseModel):
    http_options: HttpOptions | None

class DownloadFileConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
DownloadFileConfigOrDict = DownloadFileConfig | DownloadFileConfigDict

class UpscaleImageConfig(_common.BaseModel):
    http_options: HttpOptions | None
    include_rai_reason: bool | None
    output_mime_type: str | None
    output_compression_quality: int | None

class UpscaleImageConfigDict(TypedDict, total=False):
    http_options: HttpOptionsDict | None
    include_rai_reason: bool | None
    output_mime_type: str | None
    output_compression_quality: int | None
UpscaleImageConfigOrDict = UpscaleImageConfig | UpscaleImageConfigDict

class UpscaleImageParameters(_common.BaseModel):
    model: str | None
    image: Image | None
    upscale_factor: str | None
    config: UpscaleImageConfig | None

class UpscaleImageParametersDict(TypedDict, total=False):
    model: str | None
    image: ImageDict | None
    upscale_factor: str | None
    config: UpscaleImageConfigDict | None
UpscaleImageParametersOrDict = UpscaleImageParameters | UpscaleImageParametersDict

class RawReferenceImage(_common.BaseModel):
    reference_image: Image | None
    reference_id: int | None
    reference_type: str | None

class RawReferenceImageDict(TypedDict, total=False):
    reference_image: ImageDict | None
    reference_id: int | None
    reference_type: str | None
RawReferenceImageOrDict = RawReferenceImage | RawReferenceImageDict

class MaskReferenceImage(_common.BaseModel):
    reference_image: Image | None
    reference_id: int | None
    reference_type: str | None
    config: MaskReferenceConfig | None
    mask_image_config: MaskReferenceConfig | None

class MaskReferenceImageDict(TypedDict, total=False):
    reference_image: ImageDict | None
    reference_id: int | None
    reference_type: str | None
    config: MaskReferenceConfigDict | None
MaskReferenceImageOrDict = MaskReferenceImage | MaskReferenceImageDict

class ControlReferenceImage(_common.BaseModel):
    reference_image: Image | None
    reference_id: int | None
    reference_type: str | None
    config: ControlReferenceConfig | None
    control_image_config: ControlReferenceConfig | None

class ControlReferenceImageDict(TypedDict, total=False):
    reference_image: ImageDict | None
    reference_id: int | None
    reference_type: str | None
    config: ControlReferenceConfigDict | None
ControlReferenceImageOrDict = ControlReferenceImage | ControlReferenceImageDict

class StyleReferenceImage(_common.BaseModel):
    reference_image: Image | None
    reference_id: int | None
    reference_type: str | None
    config: StyleReferenceConfig | None
    style_image_config: StyleReferenceConfig | None

class StyleReferenceImageDict(TypedDict, total=False):
    reference_image: ImageDict | None
    reference_id: int | None
    reference_type: str | None
    config: StyleReferenceConfigDict | None
StyleReferenceImageOrDict = StyleReferenceImage | StyleReferenceImageDict

class SubjectReferenceImage(_common.BaseModel):
    reference_image: Image | None
    reference_id: int | None
    reference_type: str | None
    config: SubjectReferenceConfig | None
    subject_image_config: SubjectReferenceConfig | None

class SubjectReferenceImageDict(TypedDict, total=False):
    reference_image: ImageDict | None
    reference_id: int | None
    reference_type: str | None
    config: SubjectReferenceConfigDict | None
SubjectReferenceImageOrDict = SubjectReferenceImage | SubjectReferenceImageDict

class LiveServerSetupComplete(_common.BaseModel): ...
class LiveServerSetupCompleteDict(TypedDict, total=False): ...
LiveServerSetupCompleteOrDict = LiveServerSetupComplete | LiveServerSetupCompleteDict

class LiveServerContent(_common.BaseModel):
    model_turn: Content | None
    turn_complete: bool | None
    interrupted: bool | None

class LiveServerContentDict(TypedDict, total=False):
    model_turn: ContentDict | None
    turn_complete: bool | None
    interrupted: bool | None
LiveServerContentOrDict = LiveServerContent | LiveServerContentDict

class LiveServerToolCall(_common.BaseModel):
    function_calls: list[FunctionCall] | None

class LiveServerToolCallDict(TypedDict, total=False):
    function_calls: list[FunctionCallDict] | None
LiveServerToolCallOrDict = LiveServerToolCall | LiveServerToolCallDict

class LiveServerToolCallCancellation(_common.BaseModel):
    ids: list[str] | None

class LiveServerToolCallCancellationDict(TypedDict, total=False):
    ids: list[str] | None
LiveServerToolCallCancellationOrDict = LiveServerToolCallCancellation | LiveServerToolCallCancellationDict

class LiveServerMessage(_common.BaseModel):
    setup_complete: LiveServerSetupComplete | None
    server_content: LiveServerContent | None
    tool_call: LiveServerToolCall | None
    tool_call_cancellation: LiveServerToolCallCancellation | None
    @property
    def text(self) -> str | None: ...
    @property
    def data(self) -> bytes | None: ...

class LiveServerMessageDict(TypedDict, total=False):
    setup_complete: LiveServerSetupCompleteDict | None
    server_content: LiveServerContentDict | None
    tool_call: LiveServerToolCallDict | None
    tool_call_cancellation: LiveServerToolCallCancellationDict | None
LiveServerMessageOrDict = LiveServerMessage | LiveServerMessageDict

class LiveClientSetup(_common.BaseModel):
    model: str | None
    generation_config: GenerationConfig | None
    system_instruction: Content | None
    tools: ToolListUnion | None

class LiveClientSetupDict(TypedDict, total=False):
    model: str | None
    generation_config: GenerationConfigDict | None
    system_instruction: ContentDict | None
    tools: ToolListUnionDict | None
LiveClientSetupOrDict = LiveClientSetup | LiveClientSetupDict

class LiveClientContent(_common.BaseModel):
    turns: list[Content] | None
    turn_complete: bool | None

class LiveClientContentDict(TypedDict, total=False):
    turns: list[ContentDict] | None
    turn_complete: bool | None
LiveClientContentOrDict = LiveClientContent | LiveClientContentDict

class LiveClientRealtimeInput(_common.BaseModel):
    media_chunks: list[Blob] | None

class LiveClientRealtimeInputDict(TypedDict, total=False):
    media_chunks: list[BlobDict] | None
LiveClientRealtimeInputOrDict = LiveClientRealtimeInput | LiveClientRealtimeInputDict

class LiveClientToolResponse(_common.BaseModel):
    function_responses: list[FunctionResponse] | None

class LiveClientToolResponseDict(TypedDict, total=False):
    function_responses: list[FunctionResponseDict] | None
LiveClientToolResponseOrDict = LiveClientToolResponse | LiveClientToolResponseDict

class LiveClientMessage(_common.BaseModel):
    setup: LiveClientSetup | None
    client_content: LiveClientContent | None
    realtime_input: LiveClientRealtimeInput | None
    tool_response: LiveClientToolResponse | None

class LiveClientMessageDict(TypedDict, total=False):
    setup: LiveClientSetupDict | None
    client_content: LiveClientContentDict | None
    realtime_input: LiveClientRealtimeInputDict | None
    tool_response: LiveClientToolResponseDict | None
LiveClientMessageOrDict = LiveClientMessage | LiveClientMessageDict

class LiveConnectConfig(_common.BaseModel):
    generation_config: GenerationConfig | None
    response_modalities: list[Modality] | None
    speech_config: SpeechConfig | None
    system_instruction: Content | None
    tools: ToolListUnion | None

class LiveConnectConfigDict(TypedDict, total=False):
    generation_config: GenerationConfigDict | None
    response_modalities: list[Modality] | None
    speech_config: SpeechConfigDict | None
    system_instruction: ContentDict | None
    tools: ToolListUnionDict | None
LiveConnectConfigOrDict = LiveConnectConfig | LiveConnectConfigDict
