# Central model factory for all language models

from typing import Union, Any, Optional, Literal
from .providers.openai import OpenAIModels, ModelMetadata
from .providers.google import GoogleModels
from .provider_registry import ProviderRegistry, Providers


class ModelFactory:
    """
    Central factory for creating language model instances.

    Provides two access patterns:
    1. get(provider) - returns default model for a provider
    2. get_model(model_id) - returns specific model instance

    Uses ProviderRegistry for all provider-related operations.
    """

    # Provider registry handles all state management
    _provider_registry = ProviderRegistry()

    @classmethod
    def providers(cls) -> type[Providers]:
        """
        Get provider names as a typed namespace with IDE autocomplete.

        Returns:
            Providers class with typed constants for IDE support

        Usage:
            providers = ModelFactory.providers()
            model = ModelFactory.get(providers.GEMINI)  # IDE autocomplete works!
            model = ModelFactory.get(providers.OPENAI)  # IDE knows all available providers
        """
        return cls._provider_registry.get_providers_namespace()

    @classmethod
    def get(cls, provider: Union[str, Any], **kwargs) -> Any:
        """
        Get the default model for a provider.

        Args:
            provider: Provider name (string like 'openai', 'google', 'gemini')
                     or Providers constant (e.g., ModelFactory.Providers().OPENAI)
            **kwargs: Additional parameters to pass to model constructor

        Returns:
            Configured model instance

        Raises:
            ValueError: If provider is not supported

        Examples:
            # Using string
            model = ModelFactory.get("openai")

            # Using constants for IDE support
            Providers = ModelFactory.Providers()
            model = ModelFactory.get(Providers.OPENAI)
        """
        # Handle both string and constant values
        provider_str = str(provider) if not isinstance(provider, str) else provider

        if not cls._provider_registry.is_provider_supported(provider_str):
            raise ValueError(f"Unsupported provider: {provider_str}")

        cls._provider_registry.ensure_provider_initialized(provider_str, cls)

        default_model = cls._provider_registry.get_default_model(provider_str)
        if default_model is None:
            raise ValueError(
                f"No default model configured for provider: {provider_str}"
            )

        return cls.get_model(default_model, **kwargs)

    @classmethod
    def get_model(cls, model_id: Union[OpenAIModels, GoogleModels], **kwargs) -> Any:
        """
        Get a specific model instance.

        Args:
            model_id: Model identifier (string or enum)
            **kwargs: Additional parameters to pass to model constructor

        Returns:
            Configured model instance

        Raises:
            ValueError: If model is not supported
        """
        # Ensure all providers are initialized
        cls._provider_registry.ensure_all_providers_initialized(cls)

        # Find the model key (handles both enums and strings)
        model_key = cls._provider_registry.find_enum_by_value(model_id)

        creation_function = cls._provider_registry.get_model_creation_function(
            model_key
        )
        if creation_function is None:
            raise ValueError(f"Unsupported model: {model_id}")

        return creation_function(**kwargs)

    @classmethod
    def get_metadata(
        cls, model_id: Union[str, OpenAIModels, GoogleModels]
    ) -> Optional[ModelMetadata]:
        """
        Get metadata for a specific model.

        Args:
            model_id: Model identifier (string or enum)

        Returns:
            Model metadata or None if not found
        """
        # Ensure all providers are initialized
        cls._provider_registry.ensure_all_providers_initialized(cls)

        # Find the model key (handles both enums and strings)
        model_key = cls._provider_registry.find_enum_by_value(model_id)

        return cls._provider_registry.get_model_metadata(model_key)

    @classmethod
    def register_model(
        cls,
        model_enum,
        creation_function,
        metadata: Optional[ModelMetadata] = None,
        is_default: bool = False,
        provider: Optional[str] = None,
    ):
        """
        Register a model with the factory.

        Args:
            model_enum: Model enum value
            creation_function: Function that creates the model instance
            metadata: Model metadata
            is_default: Whether this is the default model for its provider
            provider: Provider name if this is a default model
        """
        cls._provider_registry.register_model(
            model_enum, creation_function, metadata, is_default, provider
        )

    @classmethod
    def list_models(cls) -> list:
        """
        List all available models.

        Returns:
            List of available model identifiers
        """
        # Ensure all providers are initialized
        cls._provider_registry.ensure_all_providers_initialized(cls)

        return cls._provider_registry.list_models()

    @classmethod
    def list_providers(cls) -> list:
        """
        List all available providers.

        Returns:
            List of provider names
        """
        return cls._provider_registry.list_providers()
