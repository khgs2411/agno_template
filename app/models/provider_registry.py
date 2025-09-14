# Provider registry for managing model provider initialization

from typing import Dict, Set, Callable, Any, Optional, Union, TypedDict, Literal

# Import actual references for crystal clear dependencies
from .providers.openai import register_openai_models, OpenAIModels
from .providers.google import register_google_models, GoogleModels


# ==========================================
# PROVIDER CONSTANTS - SINGLE DECLARATION
# ==========================================
# Declare each provider constant ONCE here
# These will be used in config AND provide IDE autocomplete!
class ProviderConstants:
    """Provider name constants - declared once, used everywhere."""

    OPENAI: Literal["openai"] = "openai"
    GOOGLE: Literal["google"] = "google"
    GEMINI: Literal["gemini"] = "gemini"
    # Add new providers here - just one line per provider!
    # ANTHROPIC: Literal["anthropic"] = "anthropic"
    # MISTRAL: Literal["mistral"] = "mistral"
    # ... supports 230+ providers with one line each


class ProviderConfigType(TypedDict):
    """Type definition for provider configuration."""

    register_function: Callable
    models_enum: type
    synonyms: Optional[list[str]]  # Just the synonym values


# ==========================================
# PROVIDER CONFIGURATION
# ==========================================
# Use the declared constants - no duplication!
PROVIDER_CONFIG: Dict[str, ProviderConfigType] = {
    ProviderConstants.OPENAI: {
        "register_function": register_openai_models,
        "models_enum": OpenAIModels,
        "synonyms": None,
    },
    ProviderConstants.GOOGLE: {
        "register_function": register_google_models,
        "models_enum": GoogleModels,
        "synonyms": [ProviderConstants.GEMINI],  # Use constant for synonym too!
    },
}

# The Providers class is just an alias to ProviderConstants for backward compatibility
# and a cleaner API. All providers are declared once in ProviderConstants.
Providers = ProviderConstants


class ProviderRegistry:
    """
    Complete state manager for ModelFactory.

    Handles all state-related logic including:
    - Provider initialization and tracking
    - Model registration and metadata
    - Synonym management
    - Provider discovery

    This keeps the ModelFactory focused on high-level stateless operations.
    """

    def __init__(self):
        # Auto-generate all registries from PROVIDER_CONFIG
        self._generate_registries_from_config()

        # Track which providers have been initialized
        self.initialized_providers: Set[str] = set()

        # Registry mapping model IDs/enums to creation functions
        self.model_registry: Dict[Any, Callable] = {}

        # Registry mapping model IDs/enums to metadata
        self.metadata_registry: Dict[Any, Any] = {}

    def _generate_registries_from_config(self):
        """Generate all provider registries from the single PROVIDER_CONFIG."""
        # Generate provider defaults (all providers + synonyms start as None)
        self.provider_defaults: Dict[str, Any] = {}

        # Generate provider synonyms mapping
        self.provider_synonyms: Dict[str, str] = {}

        # Generate provider initializers mapping
        self.provider_initializers: Dict[str, Callable] = {}

        # Process each provider in config
        for provider_name, config in PROVIDER_CONFIG.items():
            # Add to defaults
            self.provider_defaults[provider_name] = None

            # Add generic initializer (no per-provider methods needed!)
            self.provider_initializers[provider_name] = (
                lambda factory, name=provider_name: self._init_provider(name, factory)
            )

            # Add synonyms if any
            synonyms = config.get("synonyms") or []
            for synonym in synonyms:
                self.provider_synonyms[synonym] = provider_name
                self.provider_defaults[synonym] = None  # Synonyms also get defaults

    def _init_provider(self, provider_name: str, factory):
        """Generic provider initializer using direct function references!"""
        try:
            config = PROVIDER_CONFIG[provider_name]
            register_function = config[
                "register_function"
            ]  # ✨ Already a function reference!

            # Direct function call - no dynamic imports needed!
            register_function(factory)
            self.initialized_providers.add(provider_name)

        except KeyError as e:
            raise RuntimeError(f"Provider '{provider_name}' not found in config: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize provider '{provider_name}': {e}")

    def ensure_provider_initialized(self, provider: str, factory):
        """Ensure a specific provider has been initialized."""
        # Resolve synonyms to actual provider
        actual_provider = self.provider_synonyms.get(provider, provider)

        if actual_provider not in self.initialized_providers:
            initializer = self.provider_initializers.get(actual_provider)
            if initializer:
                initializer(factory)

    def ensure_all_providers_initialized(self, factory):
        """Ensure all registered providers are initialized."""
        # Initialize only the base providers (not synonyms)
        base_providers = set(self.provider_initializers.keys())
        for provider in base_providers:
            self.ensure_provider_initialized(provider, factory)

    def get_providers_namespace(self) -> type[Providers]:
        """
        Get provider names as a typed namespace with IDE autocomplete.

        Returns:
            Providers class with typed provider constants

        Usage:
            providers = registry.get_providers_namespace()
            model = ModelFactory.get(providers.GEMINI)  # IDE autocomplete works!
        """
        return Providers  # Return the class itself, not an instance

    def list_providers(self) -> list:
        """List all available providers."""
        return list(self.provider_defaults.keys())

    def is_provider_supported(self, provider: str) -> bool:
        """Check if a provider is supported."""
        return provider in self.provider_defaults

    def set_default_model(self, provider: str, model):
        """Set the default model for a provider."""
        if provider in self.provider_defaults:
            self.provider_defaults[provider] = model
            # Also set defaults for any synonyms
            for synonym, actual in self.provider_synonyms.items():
                if actual == provider:
                    self.provider_defaults[synonym] = model

    def get_default_model(self, provider: str) -> Optional[Any]:
        """Get the default model for a provider."""
        return self.provider_defaults.get(provider)

    # Model registry methods
    def register_model(
        self,
        model_enum,
        creation_function,
        metadata=None,
        is_default=False,
        provider=None,
    ):
        """Register a model with the registry."""
        self.model_registry[model_enum] = creation_function

        if metadata:
            self.metadata_registry[model_enum] = metadata

        if is_default and provider:
            self.set_default_model(provider, model_enum)

    def get_model_creation_function(self, model_key):
        """Get the creation function for a model."""
        return self.model_registry.get(model_key)

    def get_model_metadata(self, model_key):
        """Get metadata for a model."""
        return self.metadata_registry.get(model_key)

    def list_models(self) -> list:
        """List all available models."""
        return list(self.model_registry.keys())

    def find_enum_by_value(self, value: Union[str, Any]):
        """Find enum member by its string value or return if already an enum."""
        # If it's already an enum, return as-is
        if hasattr(value, "value"):
            return value

        # If it's a string, search using direct enum references!
        if isinstance(value, str):
            for config in PROVIDER_CONFIG.values():
                try:
                    enum_class = config[
                        "models_enum"
                    ]  # ✨ Already an enum class reference!

                    # Search in this provider's models - direct enum access!
                    # enum_class is the enum type itself, iterate over it
                    for model in enum_class:  # type: ignore - enum classes are iterable
                        if model.value == value:
                            return model
                except Exception:
                    # Skip if enum iteration fails
                    continue

        return None
