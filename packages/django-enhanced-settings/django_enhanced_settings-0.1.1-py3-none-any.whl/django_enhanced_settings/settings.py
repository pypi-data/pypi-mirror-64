from copy import copy
import json
import os
import time

from . import read_types


class CachedConfigValue:
    def __init__(self, key, value, cache_ttl):
        self.key = key
        self.value = value
        self.cache_ttl = cache_ttl
        if self.cache_ttl > 0:
            self.cache_end = time.time() + cache_ttl
        else:
            self.cache_end = None

    @property
    def expired(self) -> bool:
        if self.cache_ttl == -1:
            return False
        if self.cache_ttl == 0:
            return True
        return time.time() >= self.cache_end


class Config:
    def __init__(self, base_dir: str, config_file_path: str = 'config.json', gcp_project_id: str = None):
        self._BASE_DIR = base_dir
        self._CONFIG_FILE_PATH = config_file_path
        self._GCP_PROJECT_ID = gcp_project_id

        self._config_file = None
        self._env_vars = None
        self._secret_manager_secrets = {}

        self._cache = {}

    def _load_config_file(self):
        try:
            with open(os.path.join(self.BASE_DIR, self.CONFIG_FILE_PATH)) as fp:
                self._config_file = json.load(fp)
        except FileNotFoundError:
            self._config_file = {}

    def _load_env_vars(self):
        self._env_vars = copy(os.environ)

    def _fetch_config_file_value(self, key: str):
        """Returns a list, dict or str, or None if key not found."""
        if self._config_file is None:
            self._load_config_file()
        return self._config_file.get(key, None)

    def _fetch_env_vars_value(self, key: str):
        """Returns a str or None if key not found."""
        if self._env_vars is None:
            self._load_env_vars()
        return self._env_vars.get(key, None)

    def _cache_value(self, key: str, value, cache_ttl: int):
        if cache_ttl == 0:
            # Do not cache
            return
        if cache_ttl < -1:
            raise ValueError('Cache TTL must be >= -1')
        self._cache[key] = CachedConfigValue(key, value, cache_ttl)
        return value

    def _check_cache(self, key: str):
        if (cached_value := self._cache.get(key, None)) is not None:
            if cached_value.expired:
                del self._cache[key]
                return
            return cached_value.value

    def get(self, read_function, read_args: dict, *, key: str, default, required: bool, cache_ttl: int):
        if value := self._check_cache(key):
            return value
        if value := self._fetch_env_vars_value(key):
            pass
        elif value := self._fetch_config_file_value(key):
            pass
        if value is not None:
            value = read_function(value, **read_args)
            self._cache_value(key, value, cache_ttl)
            return value
        if required is True:
            raise ValueError(f'Value not provided for required setting {key}')
        return default


class Settings:
    def __init__(self, base_dir: str, config_file_path: str = 'config.json', suffix_underscore=False,
                 gcp_project_id: str = None):
        self._config = Config(base_dir, config_file_path, gcp_project_id)
        self._suffix_underscore = suffix_underscore

    def set_gcp_project_id(self, gcp_project_id: str):
        self._config._GCP_PROJECT_ID = gcp_project_id

    def dir(self, global_vars: dict):
        out = []
        for global_variable_name in global_vars.keys():
            if global_variable_name.startswith('__'):
                continue
            if global_variable_name.endswith('__'):
                continue
            if global_variable_name.isupper() is False:
                continue
            if self._suffix_underscore is True:
                if global_variable_name.endswith('_'):
                    global_variable_name = global_variable_name[:-1]
            else:
                if global_variable_name.startswith('_'):
                    global_variable_name = global_variable_name[1:]
            out.append(global_variable_name)
        return out

    def getattr(self, global_vars: dict, item: str):
        if item in self.dir(global_vars):
            name = f'{item}_' if self._suffix_underscore else f'_{item}'
            if name in global_vars:
                if isinstance(var := global_vars[name], ConfigValue):
                    return var.value
        raise AttributeError()

    def custom_value(self, get_kwargs: dict, read_function, read_args: dict, value_type):
        return ConfigValue(self._config, read_function, value_type, read_args, get_kwargs)

    def string_value(self, key: str, default=None, *, required=False, cache_ttl: int = -1) -> 'ConfigValue':
        read_args = dict()
        get_kwargs = dict(
            key=key,
            default=default,
            required=required,
            cache_ttl=cache_ttl,
        )
        return self.custom_value(get_kwargs, read_types.read_str, read_args, str)

    def bool_value(self, key: str, default=None, *, required=False, cache_ttl: int = -1) -> 'ConfigValue':
        read_args = dict()
        get_kwargs = dict(
            key=key,
            default=default,
            required=required,
            cache_ttl=cache_ttl,
        )
        return self.custom_value(get_kwargs, read_types.read_bool, read_args, bool)

    def list_value(self, key: str, default=None, *, required=False, cache_ttl: int = -1,
                   split_char=';') -> 'ConfigValue':
        read_args = dict(
            split_char=split_char,
        )
        get_kwargs = dict(
            key=key,
            default=default,
            required=required,
            cache_ttl=cache_ttl,
        )
        return self.custom_value(get_kwargs, read_types.read_list, read_args, list)


class ConfigValue:
    def __init__(self, config: Config, read_function, value_type, read_args: dict, get_kwargs: dict):
        self._config = config
        self._read_function = read_function
        self.value_type = value_type
        self._read_args = read_args
        self._get_kwargs = get_kwargs

    @property
    def value(self):
        return self._config.get(self._read_function, self._read_args, **self._get_kwargs)

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)
