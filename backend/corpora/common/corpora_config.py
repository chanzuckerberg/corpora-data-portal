import os

from .utils.secret_config import SecretConfig


class CorporaDbConfig(SecretConfig):
    def __init__(self, *args, **kwargs):
        super().__init__(
            component_name="backend",
            secret_name=f"database{'_local' if 'CORPORA_LOCAL_DEV' in os.environ else ''}",
            **kwargs,
        )