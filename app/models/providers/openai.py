# OpenAI model provider
# This will be implemented in Task 2.1

from enum import Enum
from typing import Optional, Dict, Any
from dataclasses import dataclass

from agno.models.openai import OpenAIChat


@dataclass
class ModelMetadata:
    """Metadata for language models"""

    cost_per_1k_input: Optional[float] = None
    cost_per_1k_output: Optional[float] = None
    release_date: Optional[str] = None
    context_window: Optional[int] = None
    max_output_tokens: Optional[int] = None
    supports_vision: bool = False
    supports_function_calling: bool = False
    deprecation_date: Optional[str] = None


class OpenAIModels(Enum):
    """OpenAI model identifiers"""

    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4_1 = "gpt-4.1"
    GPT_4_1_MINI = "gpt-4.1-mini"
    O3_MINI = "o3-mini"
    GPT_3_5_TURBO = "gpt-3.5-turbo"


class OpenAIParams(Enum):
    """OpenAI parameter constants"""

    # Temperature settings
    CREATIVE_TEMP = 0.7
    BALANCED_TEMP = 0.5
    PRECISE_TEMP = 0.1
    DETERMINISTIC_TEMP = 0.0

    # Max tokens settings
    DEFAULT_MAX_TOKENS = 4096
    LARGE_MAX_TOKENS = 8192
    SMALL_MAX_TOKENS = 1024

    # Other common parameters
    DEFAULT_TOP_P = 1.0
    DEFAULT_FREQUENCY_PENALTY = 0.0
    DEFAULT_PRESENCE_PENALTY = 0.0


# Model metadata dictionary with comprehensive information
OPENAI_MODEL_METADATA: Dict[OpenAIModels, ModelMetadata] = {
    OpenAIModels.GPT_4O: ModelMetadata(
        cost_per_1k_input=2.50,
        cost_per_1k_output=10.00,
        context_window=128000,
        max_output_tokens=4096,
        supports_vision=True,
        supports_function_calling=True,
        deprecation_date=None,
    ),
    OpenAIModels.GPT_4O_MINI: ModelMetadata(
        cost_per_1k_input=0.15,
        cost_per_1k_output=0.60,
        release_date="2024-07-18",
        context_window=128000,
        max_output_tokens=16384,
        supports_vision=True,
        supports_function_calling=True,
        deprecation_date=None,
    ),
    OpenAIModels.GPT_4_1: ModelMetadata(
        cost_per_1k_input=30.00,
        cost_per_1k_output=60.00,
        release_date="2024-12-05",
        context_window=200000,
        max_output_tokens=100000,
        supports_vision=False,
        supports_function_calling=True,
        deprecation_date=None,
    ),
    
    OpenAIModels.O3_MINI: ModelMetadata(
        cost_per_1k_input=1.00,
        cost_per_1k_output=4.00,
        release_date="2024-12-20",
        context_window=128000,
        max_output_tokens=65536,
        supports_vision=False,
        supports_function_calling=True,
        deprecation_date=None,
    ),
    OpenAIModels.GPT_3_5_TURBO: ModelMetadata(
        cost_per_1k_input=0.50,
        cost_per_1k_output=1.50,
        release_date="2023-03-01",
        context_window=16385,
        max_output_tokens=4096,
        supports_vision=False,
        supports_function_calling=True,
        deprecation_date="2025-09-13",
    ),
}


# Model creation functions
def get_gpt_4o(
    max_tokens: int = OpenAIParams.DEFAULT_MAX_TOKENS.value,
    temperature: float = OpenAIParams.BALANCED_TEMP.value,
    **kwargs
) -> OpenAIChat:
    """Create a GPT-4o model instance with default settings."""
    return OpenAIChat(
        id=OpenAIModels.GPT_4O.value,
        max_tokens=max_tokens,
        temperature=temperature,
        **kwargs
    )


def get_gpt_4o_mini(
    max_tokens: int = OpenAIParams.DEFAULT_MAX_TOKENS.value,
    temperature: float = OpenAIParams.BALANCED_TEMP.value,
    **kwargs
) -> OpenAIChat:
    """Create a GPT-4o-mini model instance with default settings."""
    return OpenAIChat(
        id=OpenAIModels.GPT_4O_MINI.value,
        max_tokens=max_tokens,
        temperature=temperature,
        **kwargs
    )


def get_gpt_4_1(
    max_tokens: int = OpenAIParams.DEFAULT_MAX_TOKENS.value,
    temperature: float = OpenAIParams.BALANCED_TEMP.value,
    **kwargs
) -> OpenAIChat:
    """Create a GPT-4.1 model instance with default settings."""
    return OpenAIChat(
        id=OpenAIModels.GPT_4_1.value,
        max_tokens=max_tokens,
        temperature=temperature,
        **kwargs
    )

def get_gpt_4_1_mini(
    max_tokens: int = OpenAIParams.DEFAULT_MAX_TOKENS.value,
    temperature: float = OpenAIParams.BALANCED_TEMP.value,
    **kwargs
) -> OpenAIChat:
    """Create a GPT-4.1-mini model instance with default settings."""
    return OpenAIChat(
        id=OpenAIModels.GPT_4_1_MINI.value,
        max_tokens=max_tokens,
        temperature=temperature,
        **kwargs
    )


def get_o3_mini(
    max_tokens: int = OpenAIParams.DEFAULT_MAX_TOKENS.value,
    temperature: float = OpenAIParams.BALANCED_TEMP.value,
    **kwargs
) -> OpenAIChat:
    """Create an O3-mini model instance with default settings."""
    return OpenAIChat(
        id=OpenAIModels.O3_MINI.value,
        max_tokens=max_tokens,
        temperature=temperature,
        **kwargs
    )


def get_gpt_3_5_turbo(
    max_tokens: int = OpenAIParams.DEFAULT_MAX_TOKENS.value,
    temperature: float = OpenAIParams.BALANCED_TEMP.value,
    **kwargs
) -> OpenAIChat:
    """Create a GPT-3.5-turbo model instance with default settings."""
    return OpenAIChat(
        id=OpenAIModels.GPT_3_5_TURBO.value,
        max_tokens=max_tokens,
        temperature=temperature,
        **kwargs
    )


def get_default_openai_model(**kwargs) -> OpenAIChat:
    """Get the default OpenAI model (GPT-4o)."""
    return get_gpt_4o(**kwargs)


# Model registry mapping enums to creation functions
MODEL_CREATION_FUNCTIONS = {
    OpenAIModels.GPT_4O: get_gpt_4o,
    OpenAIModels.GPT_4O_MINI: get_gpt_4o_mini,
    OpenAIModels.GPT_4_1: get_gpt_4_1,
    OpenAIModels.GPT_4_1_MINI: get_gpt_4_1_mini,
    OpenAIModels.O3_MINI: get_o3_mini,
    OpenAIModels.GPT_3_5_TURBO: get_gpt_3_5_turbo,
}


def register_openai_models(model_factory_class):
    """Register all OpenAI models with the ModelFactory."""
    # Register all models
    for model_enum, creation_function in MODEL_CREATION_FUNCTIONS.items():
        metadata = OPENAI_MODEL_METADATA.get(model_enum)
        is_default = model_enum == DEFAULT_OPENAI_MODEL  # GPT-4o is the default

        model_factory_class.register_model(
            model_enum=model_enum,
            creation_function=creation_function,
            metadata=metadata,
            is_default=is_default,
            provider="openai" if is_default else None,
        )


# Default model for provider access
DEFAULT_OPENAI_MODEL = OpenAIModels.GPT_4_1_MINI
