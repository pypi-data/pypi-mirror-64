import os
from dataclasses import dataclass

from .api_client import SpintopAPIClientModule, SpintopAPISpecProvider
from .auth import FilePathCredentialsStore
from .persistence.mongo import MongoPersistenceFacade
from .persistence.postgresql import PostgreSQLPersistenceFacade
from .api_client.tests_facade import SpintopAPIPersistenceFacade

from .storage import SITE_DATA_DIR
from .messages import SpintopMessagePublisher

def alias_for(env_name):
    return property(
        fget= lambda env: env[env_name],
        fset= lambda env, value: env.__setitem__(env_name, value)
    )

NO_VALUE = object()

class SpintopEnv(object):
    SPINTOP_CREDENTIALS_FILE: str = os.path.join(SITE_DATA_DIR, '.spintop-credentials.yml')
    SPINTOP_PERSISTENCE_TYPE: str = 'api'

    # used if SPINTOP_PERSISTENCE_TYPE is 'api'
    SPINTOP_API_URI: str = 'https://cloud.spintop.io'
    SPINTOP_API_ACTIVE_ORG: str = None 

    # used if SPINTOP_PERSISTENCE_TYPE is 'mongo'
    SPINTOP_MONGO_URI: str 
    SPINTOP_DATABASE_NAME: str

    # used if SPINTOP_PERSISTENCE_TYPE is 'postgres'
    SPINTOP_POSTGRES_URI: str

    # Aliases for python-friendly attributes
    api_url = alias_for('SPINTOP_API_URI')
    credentials_filepath = alias_for('SPINTOP_CREDENTIALS_FILE')
    selected_org_id = alias_for('SPINTOP_API_ACTIVE_ORG')

    def __init__(self, _init_values=None, verbose=False, api_url=None, ignore_invalid_init_value=False):
        if _init_values is None:
            _init_values = {}

        # Replace default values by possible a real env value.
        for key in self.ENV_NAMES:
            default_value = NO_VALUE
            if hasattr(self, key):
                default_value = self[key]

            setattr(self, key, os.environ.get(key, default_value))

        for key, value in _init_values.items():
            try:
                self[key] = value # Will validate if key is part of the support env variables.
            except KeyError:
                if not ignore_invalid_init_value:
                    raise

        if api_url:
            # for some reason, the requests module adds 1 second to every request made using localhost
            # replacing it with 127.0.0.1 removes this strange issue.
            self.api_url = api_url.replace('//localhost', '//127.0.0.1') 
        
        self.verbose = verbose

    @property
    def ENV_NAMES(self):
        return list(self.__annotations__.keys())

    def __getattr__(self, key):
        """When an attribute does not exist, attempt to retrieve it from env."""
        try:
            self._must_be_an_env_key(key)
            return os.environ[key]
        except KeyError as e:
            # Raise as attribute error for __getattr__ 
            raise AttributeError(str(e))

    def __getitem__(self, key):
        self._must_be_an_env_key(key)
        value = getattr(self, key)
        if value is NO_VALUE:
            raise KeyError(key)
        return value
    
    def __setitem__(self, key, value):
        self._must_be_an_env_key(key)
        setattr(self, key, value)

    def get(self, key, default_value=None):
        try:
            return self[key]
        except:
            return default_value

    def _must_be_an_env_key(self, key):
        if key not in self.ENV_NAMES:
            raise KeyError(f'{key!r} is not a SpintopEnv variable.')

    def freeze(self):
        return {key: self[key] for key in self.ENV_NAMES}

    def get_facade_uri(self, facade_type):
        return self[f'SPINTOP_{facade_type.upper()}_URI']

    def persistence_facade_factory(self, message_publisher: SpintopMessagePublisher = None, database_name=None):
        facade_type = self.SPINTOP_PERSISTENCE_TYPE
        facade_cls_by_type = {
            'mongo': MongoPersistenceFacade,
            'postgres': PostgreSQLPersistenceFacade,
            'api': SpintopAPIPersistenceFacade,
        }

        if facade_type not in facade_cls_by_type:
            raise ValueError(f'Unknown facade type SPINTOP_PERSISTENCE_TYPE={facade_type!r}. Available: {list(facade_cls_by_type.keys())!r}')
        
        facade_cls = facade_cls_by_type[facade_type]

        if database_name is None:
            database_name = self.SPINTOP_DATABASE_NAME

        facade = facade_cls.from_env(
            uri=self.get_facade_uri(facade_type),
            database_name=database_name, # shared by all
            env=self 
        )
        if message_publisher is not None:
            facade.messages = message_publisher
        return facade
    
