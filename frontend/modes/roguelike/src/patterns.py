class SingletonMeta(type):  # noqa: D101
    _instance = None  # type: object | None

    def __call__(cls: type["SingletonMeta"], *args: object, **kwargs: object) -> object:
        """Return the singleton instance, creating it if necessary."""
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
