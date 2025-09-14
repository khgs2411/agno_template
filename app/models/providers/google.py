# Google model provider
# This will be implemented in Task 2.2

from enum import Enum
import os
from typing import Dict

from agno.models.google import Gemini
from dotenv import load_dotenv
from .openai import ModelMetadata  # Reuse the same metadata structure


class GoogleModels(Enum):
    """Google model identifiers"""

    # Gemini 2.5 models (latest)
    GEMINI_2_5_PRO = "gemini-2.5-pro"
    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GEMINI_2_5_FLASH_LITE = "gemini-2.5-flash-lite-preview-06-17"

    # Gemini 2.0 models
    GEMINI_2_0_FLASH = "gemini-2.0-flash"
    GEMINI_2_0_FLASH_LITE = "gemini-2.0-flash-lite"

    # Gemini 1.5 models
    GEMINI_1_5_PRO = "gemini-1.5-pro"
    GEMINI_1_5_FLASH = "gemini-1.5-flash"
    GEMINI_1_5_FLASH_8B = "gemini-1.5-flash-8b"

    # Legacy models
    GEMINI_PRO = "gemini-pro"
    GEMINI_PRO_VISION = "gemini-pro-vision"


class GoogleParams(Enum):
    """Google parameter constants"""

    # Temperature settings
    CREATIVE_TEMP = 0.9
    BALANCED_TEMP = 0.5
    PRECISE_TEMP = 0.1
    DETERMINISTIC_TEMP = 0.0

    # Max tokens settings
    DEFAULT_MAX_TOKENS = 8192
    LARGE_MAX_TOKENS = 32768
    SMALL_MAX_TOKENS = 2048

    # Other common parameters
    DEFAULT_TOP_P = 0.95
    DEFAULT_TOP_K = 40
    DEFAULT_SAFETY_THRESHOLD = "BLOCK_MEDIUM_AND_ABOVE"


# Model metadata dictionary with comprehensive information
GOOGLE_MODEL_METADATA: Dict[GoogleModels, ModelMetadata] = {
    # Gemini 2.5 models - latest generation with thinking capabilities
    GoogleModels.GEMINI_2_5_PRO: ModelMetadata(
        cost_per_1k_input=1.25,
        cost_per_1k_output=5.00,
        release_date="2024-12-11",
        context_window=2000000,  # 2M tokens
        max_output_tokens=8192,
        supports_vision=True,
        supports_function_calling=True,
        deprecation_date=None,
    ),
    GoogleModels.GEMINI_2_5_FLASH: ModelMetadata(
        cost_per_1k_input=0.075,
        cost_per_1k_output=0.30,
        release_date="2024-12-11",
        context_window=1000000,  # 1M tokens
        max_output_tokens=8192,
        supports_vision=True,
        supports_function_calling=True,
        deprecation_date=None,
    ),
    GoogleModels.GEMINI_2_5_FLASH_LITE: ModelMetadata(
        cost_per_1k_input=0.075,
        cost_per_1k_output=0.30,
        release_date="2024-12-17",
        context_window=1000000,  # 1M tokens
        max_output_tokens=8192,
        supports_vision=True,
        supports_function_calling=True,
        deprecation_date=None,
    ),
    # Gemini 2.0 models
    GoogleModels.GEMINI_2_0_FLASH: ModelMetadata(
        cost_per_1k_input=0.075,
        cost_per_1k_output=0.30,
        release_date="2024-12-11",
        context_window=1000000,  # 1M tokens
        max_output_tokens=8192,
        supports_vision=True,
        supports_function_calling=True,
        deprecation_date=None,
    ),
    GoogleModels.GEMINI_2_0_FLASH_LITE: ModelMetadata(
        cost_per_1k_input=0.075,
        cost_per_1k_output=0.30,
        release_date="2024-12-11",
        context_window=1000000,  # 1M tokens
        max_output_tokens=8192,
        supports_vision=True,
        supports_function_calling=True,
        deprecation_date=None,
    ),
    # Gemini 1.5 models
    GoogleModels.GEMINI_1_5_PRO: ModelMetadata(
        cost_per_1k_input=1.25,
        cost_per_1k_output=5.00,
        release_date="2024-05-14",
        context_window=2000000,  # 2M tokens
        max_output_tokens=8192,
        supports_vision=True,
        supports_function_calling=True,
        deprecation_date=None,
    ),
    GoogleModels.GEMINI_1_5_FLASH: ModelMetadata(
        cost_per_1k_input=0.075,
        cost_per_1k_output=0.30,
        release_date="2024-05-14",
        context_window=1000000,  # 1M tokens
        max_output_tokens=8192,
        supports_vision=True,
        supports_function_calling=True,
        deprecation_date=None,
    ),
    GoogleModels.GEMINI_1_5_FLASH_8B: ModelMetadata(
        cost_per_1k_input=0.0375,
        cost_per_1k_output=0.15,
        release_date="2024-10-03",
        context_window=1000000,  # 1M tokens
        max_output_tokens=8192,
        supports_vision=True,
        supports_function_calling=True,
        deprecation_date=None,
    ),
    # Legacy models
    GoogleModels.GEMINI_PRO: ModelMetadata(
        cost_per_1k_input=0.50,
        cost_per_1k_output=1.50,
        release_date="2023-12-13",
        context_window=32768,
        max_output_tokens=2048,
        supports_vision=False,
        supports_function_calling=True,
        deprecation_date="2024-02-15",  # Already deprecated
    ),
    GoogleModels.GEMINI_PRO_VISION: ModelMetadata(
        cost_per_1k_input=0.25,
        cost_per_1k_output=0.50,
        release_date="2023-12-13",
        context_window=16384,
        max_output_tokens=2048,
        supports_vision=True,
        supports_function_calling=False,
        deprecation_date="2024-02-15",  # Already deprecated
    ),
}


def get_google_model_class(**kwargs):
    """
    Initializes and returns an instance of the Gemini class for Google models.

    Retrieves the Google API key from the environment variable 'GOOGLE_API_KEY' and passes it,
    along with any additional keyword arguments, to the Gemini class constructor.

    Args:
        **kwargs: Arbitrary keyword arguments to be passed to the Gemini class.
        name: str = "Gemini",
        provider: str = "Google",
        supports_native_structured_outputs: bool = True,
        supports_json_schema_outputs: bool = False,
        _tool_choice: str | Dict[str, Any] | None = None,
        system_prompt: str | None = None,
        instructions: List[str] | None = None,
        tool_message_role: str = "tool",
        assistant_message_role: str = "assistant",
        function_declarations: List[Any] | None = None,
        generation_config: Any | None = None,
        safety_settings: List[Any] | None = None,
        generative_model_kwargs: Dict[str, Any] | None = None,
        search: bool = False,
        grounding: bool = False,
        grounding_dynamic_threshold: float | None = None,
        url_context: bool = False,
        vertexai_search: bool = False,
        vertexai_search_datastore: str | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        top_k: int | None = None,
        max_output_tokens: int | None = None,
        stop_sequences: list[str] | None = None,
        logprobs: bool | None = None,
        presence_penalty: float | None = None,
        frequency_penalty: float | None = None,
        seed: int | None = None,
        response_modalities: list[str] | None = None,
        speech_config: dict[str, Any] | None = None,
        cached_content: Any | None = None,
        thinking_budget: int | None = None,
        include_thoughts: bool | None = None,
        request_params: Dict[str, Any] | None = None,
        api_key: str | None = None,
        vertexai: bool = False,
        project_id: str | None = None,
        location: str | None = None,
        client_params: Dict[str, Any] | None = None,
        client: GeminiClient | None = None

    Returns:
        Gemini: An instance of the Gemini class initialized with the provided API key and arguments.
    """
    """Return the Gemini class for Google models."""
    api_key = os.getenv("GOOGLE_API_KEY")
    return Gemini(api_key=api_key, **kwargs)


# Model creation functions
def get_gemini_2_5_pro(
    max_output_tokens: int = GoogleParams.DEFAULT_MAX_TOKENS.value,
    temperature: float = GoogleParams.BALANCED_TEMP.value,
    **kwargs,
) -> Gemini:
    """Create a Gemini 2.5 Pro model instance with default settings."""
    return get_google_model_class(
        id=GoogleModels.GEMINI_2_5_PRO.value,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        **kwargs,
    )


def get_gemini_2_5_flash(
    max_output_tokens: int = GoogleParams.DEFAULT_MAX_TOKENS.value,
    temperature: float = GoogleParams.BALANCED_TEMP.value,
    **kwargs,
) -> Gemini:
    """Create a Gemini 2.5 Flash model instance with default settings."""
    return get_google_model_class(
        id=GoogleModels.GEMINI_2_5_FLASH.value,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        **kwargs,
    )


def get_gemini_2_5_flash_lite(
    max_output_tokens: int = GoogleParams.DEFAULT_MAX_TOKENS.value,
    temperature: float = GoogleParams.BALANCED_TEMP.value,
    **kwargs,
) -> Gemini:
    """Create a Gemini 2.5 Flash Lite model instance with default settings."""
    return get_google_model_class(
        id=GoogleModels.GEMINI_2_5_FLASH_LITE.value,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        **kwargs,
    )


def get_gemini_2_0_flash(
    max_output_tokens: int = GoogleParams.DEFAULT_MAX_TOKENS.value,
    temperature: float = GoogleParams.BALANCED_TEMP.value,
    **kwargs,
) -> Gemini:
    """Create a Gemini 2.0 Flash model instance with default settings."""
    return get_google_model_class(
        id=GoogleModels.GEMINI_2_0_FLASH.value,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        **kwargs,
    )


def get_gemini_2_0_flash_lite(
    max_output_tokens: int = GoogleParams.DEFAULT_MAX_TOKENS.value,
    temperature: float = GoogleParams.BALANCED_TEMP.value,
    **kwargs,
) -> Gemini:
    """Create a Gemini 2.0 Flash Lite model instance with default settings."""
    return get_google_model_class(
        id=GoogleModels.GEMINI_2_0_FLASH_LITE.value,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        **kwargs,
    )


def get_gemini_1_5_pro(
    max_output_tokens: int = GoogleParams.DEFAULT_MAX_TOKENS.value,
    temperature: float = GoogleParams.BALANCED_TEMP.value,
    **kwargs,
) -> Gemini:
    """Create a Gemini 1.5 Pro model instance with default settings."""
    return get_google_model_class(
        id=GoogleModels.GEMINI_1_5_PRO.value,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        **kwargs,
    )


def get_gemini_1_5_flash(
    max_output_tokens: int = GoogleParams.DEFAULT_MAX_TOKENS.value,
    temperature: float = GoogleParams.BALANCED_TEMP.value,
    **kwargs,
) -> Gemini:
    """Create a Gemini 1.5 Flash model instance with default settings."""
    return get_google_model_class(
        id=GoogleModels.GEMINI_1_5_FLASH.value,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        **kwargs,
    )


def get_gemini_1_5_flash_8b(
    max_output_tokens: int = GoogleParams.DEFAULT_MAX_TOKENS.value,
    temperature: float = GoogleParams.BALANCED_TEMP.value,
    **kwargs,
) -> Gemini:
    """Create a Gemini 1.5 Flash-8B model instance with default settings."""
    return get_google_model_class(
        id=GoogleModels.GEMINI_1_5_FLASH_8B.value,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        **kwargs,
    )


def get_gemini_pro(
    max_output_tokens: int = GoogleParams.SMALL_MAX_TOKENS.value,
    temperature: float = GoogleParams.BALANCED_TEMP.value,
    **kwargs,
) -> Gemini:
    """Create a Gemini Pro model instance with default settings (deprecated)."""
    return get_google_model_class(
        id=GoogleModels.GEMINI_PRO.value,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        **kwargs,
    )


def get_gemini_pro_vision(
    max_output_tokens: int = GoogleParams.SMALL_MAX_TOKENS.value,
    temperature: float = GoogleParams.BALANCED_TEMP.value,
    **kwargs,
) -> Gemini:
    """Create a Gemini Pro Vision model instance with default settings (deprecated)."""
    return get_google_model_class(
        id=GoogleModels.GEMINI_PRO_VISION.value,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        **kwargs,
    )


def get_default_google_model(**kwargs) -> Gemini:
    """Get the default Google model (Gemini 2.5 Flash)."""
    return get_gemini_2_5_flash(**kwargs)


# Model registry mapping enums to creation functions
MODEL_CREATION_FUNCTIONS = {
    GoogleModels.GEMINI_2_5_PRO: get_gemini_2_5_pro,
    GoogleModels.GEMINI_2_5_FLASH: get_gemini_2_5_flash,
    GoogleModels.GEMINI_2_5_FLASH_LITE: get_gemini_2_5_flash_lite,
    GoogleModels.GEMINI_2_0_FLASH: get_gemini_2_0_flash,
    GoogleModels.GEMINI_2_0_FLASH_LITE: get_gemini_2_0_flash_lite,
    GoogleModels.GEMINI_1_5_PRO: get_gemini_1_5_pro,
    GoogleModels.GEMINI_1_5_FLASH: get_gemini_1_5_flash,
    GoogleModels.GEMINI_1_5_FLASH_8B: get_gemini_1_5_flash_8b,
    GoogleModels.GEMINI_PRO: get_gemini_pro,
    GoogleModels.GEMINI_PRO_VISION: get_gemini_pro_vision,
}


def register_google_models(model_factory_class):
    """Register all Google models with the ModelFactory."""
    # Register all models
    for model_enum, creation_function in MODEL_CREATION_FUNCTIONS.items():
        metadata = GOOGLE_MODEL_METADATA.get(model_enum)
        is_default = (
            model_enum == DEFAULT_GOOGLE_MODEL
        )  # Gemini 2.5 Flash is the new default

        model_factory_class.register_model(
            model_enum=model_enum,
            creation_function=creation_function,
            metadata=metadata,
            is_default=is_default,
            provider="google" if is_default else None,
        )


# Default model for provider access
DEFAULT_GOOGLE_MODEL = GoogleModels.GEMINI_2_0_FLASH
