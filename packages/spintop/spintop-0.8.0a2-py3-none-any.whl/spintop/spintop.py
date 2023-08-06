import os
from incremental_module_loader import IncrementalModuleLoader

from .auth import AuthModule, FilePathCredentialsStore
from .logs import _logger, setup_logging
from .storage import SITE_DATA_DIR
from .api_client import SpintopAPIClientModule, SpintopAPISpecProvider

from .env import SpintopEnv

logger = _logger('root')

def Spintop(verbose=False, api_url=None):
    init_env = {} 
    return SpintopFactory(env=SpintopEnv(init_env, verbose=verbose, api_url=api_url))

def SpintopFactory(
        env=None,
        logs_factory=setup_logging,
        api_spec_provider_factory=SpintopAPISpecProvider,
        credentials_store_factory=FilePathCredentialsStore,
        auth_factory=AuthModule, 
        spintop_api_factory=SpintopAPIClientModule,
        final_factory=None
    ):

    if env is None: 
        env = SpintopEnv() # Default env

    loader = IncrementalModuleLoader()
    loader.update(
        api_url=env.api_url,
        credentials_filepath=env.credentials_filepath,
        selected_org_id=env.selected_org_id
    )
    
    loader.load(logs=logs_factory)
    loader.load(credentials_store=credentials_store_factory)
    loader.load(api_spec_provider=api_spec_provider_factory)
    loader.load(auth=auth_factory)
    loader.load(spintop_api=spintop_api_factory)
    spintop_or_final = loader.load(spintop=SpintopModule)
    
    if final_factory:
        spintop_or_final = loader.load(final_factory)
    
    return spintop_or_final

def SpintopWorkerFactory(worker_cls, **factory_kwargs):
    worker = SpintopFactory(final_factory=worker_cls, **factory_kwargs)
    return worker
    

class SpintopModule(object):
    def __init__(self, spintop_api, auth):
        self.spintop_api = spintop_api
        self.auth = auth
    
    def assert_no_login(self):
        self.auth.assert_no_login()
    
    def login_user_pass(self, username, password):
        self.auth.login_user_pass(username, password)

    def login_browser(self):
        return self.auth.login_device_flow()

    def stored_logged_username(self):
        if self.auth.credentials:
            return self.auth.credentials.get('username')
        else:
            return None
    
    def logout(self):
        return self.auth.logout()
    
    def register_machine(self, name, token, org_id=None):
        return self.spintop_api.register_machine(name, token, org_id=org_id)
    
    def get_user_orgs(self):
        return self.auth.user_orgs

    @property
    def tests(self):
        return self.spintop_api.tests

        
        
    
    
        