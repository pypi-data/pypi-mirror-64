import os
import sys

from itertools import chain
from pathlib import Path

from configDmanager import Config
from configDmanager.errors import ConfigNotFoundError, ConfigManagerError
from configDmanager.config_types import JsonType, YamlType


class ConfigManager:
    supported_types = {'json': JsonType,
                       'yml': YamlType,
                       'yaml': YamlType}
    default_export_type = 'json'

    @classmethod
    def import_config(cls, name, path=None, type_=None):
        level, path = cls.__level_parse(name, path)
        return cls.__config_import(name[level:], path, level, type_)[0]

    @classmethod
    def update_config(cls, mod, name, path=None, type_=None):
        level, path = cls.__level_parse(name, path)
        config, name_base, c_path = cls.__config_import(name[level:], path, level, type_)
        if isinstance(mod, dict) or isinstance(mod, Config):
            config.update(mod)
        elif callable(mod):
            config.update(mod(config))
        else:
            raise ValueError('mod must be a dict, Config or a callable that returns a dict or a Config')
        cls.export_config(config, name_base, c_path, type_)
        return config

    @classmethod
    def export_config(cls, config, name, path=None, type_=None):
        level, path = cls.__level_parse(name, path)
        return cls.__config_export(config, name[level:], path, level, type_)

    @classmethod
    def export_config_file(cls, obj, config_name=None, path=None, type_=None, **kwargs):
        config_dict = obj.to_dict()
        type_ = type_ or config_dict.get('__type', cls.default_export_type)
        cls.__set_metadata(config_dict, obj, config_name, type_)
        config_path = cls.__get_config_path(config_name if config_name else obj.get_name() or obj.__name__, path, type_)
        with open(config_path, 'w') as config_file:
            cls.supported_types[type_].export_config(config_dict, config_file, **kwargs)

    @classmethod
    def __load_config(cls, config_name, path, type_=None):
        # todo implement type_ as a list that features all parents types
        config_dict = cls.__read_config_file(config_name, path, type_)
        parent_config = cls.__load_parent_config(config_dict, path)
        return Config(config_dict, parent_config, config_name, path, type_)

    @classmethod
    def __read_config_file(cls, config_name, path, type_=None):
        config_path, type_ = cls.__get_config_path_and_type(config_name, path, type_)
        with open(config_path, 'r') as config_file:
            config_dict = cls.supported_types[type_].import_config(config_file)
        return config_dict

    @classmethod
    def __load_parent_config(cls, config_dict, path, type_=None):
        parent_name = config_dict.get('__parent', None)
        parent_path = config_dict.get('__parent_path', path)
        parent_type = config_dict.get('__parent_type', type_)
        return cls.import_config(parent_name, parent_path, parent_type) if parent_name else None

    @classmethod
    def __config_import(cls, name, path, level=0, type_=None):
        for c_path in chain([path], sys.path):
            try:
                if c_path:
                    name_base, c_path = cls.__parse_path(name, c_path, level)
                    return cls.__load_config(name_base, c_path, type_), name_base, c_path
            except (FileNotFoundError, PermissionError):
                pass

        raise ConfigNotFoundError(name, path)

    @classmethod
    def __config_export(cls, config, name, path=None, level=0, type_=None):
        name_base, c_path = cls.__parse_path(name, path or os.getcwd(), level)
        return cls.export_config_file(config, name_base, c_path, type_)

    @classmethod
    def __get_config_path_and_type(cls, config_name, path, type_=None):
        if type_ is None:
            type_, ext = cls.__detect_type(config_name, path)
        else:
            ext = type_
        return cls.__get_config_path(config_name, path, ext), type_.lower()

    @classmethod
    def __detect_type(cls, config_name, path):
        candidates = [os.path.splitext(f)[1][1:] for f in os.listdir(path)
                      if os.path.isfile(os.path.join(path, f)) and f.startswith(config_name)]
        # first detection based on the extension:
        for ext in candidates:
            ext = ext.lower()
            if ext in cls.supported_types:
                full_path = cls.__get_config_path(config_name, path, ext)
                if cls.supported_types[ext].is_readable(full_path):
                    return ext, ext
        # second detection based on the content:
        for ext in candidates:
            ext = ext.lower() if ext else ext
            for type_ in cls.supported_types:
                full_path = cls.__get_config_path(config_name, path, ext)
                if cls.supported_types[type_].is_readable(full_path):
                    return type_, ext
        if candidates:
            raise ConfigManagerError(f'Could not auto-detect type of Config: {config_name}')
        else:
            raise FileNotFoundError

    @classmethod
    def __parse_path(cls, name, path, level):
        cls.__sanity_check(name, path, level)
        base, _, name_base = name.rpartition('.')
        base = base.replace('.', '/')
        c_path = Path(path)
        c_path = (c_path.parent if level == 2 else c_path) / base
        return name_base, c_path

    @staticmethod
    def __sanity_check(name, path, level):
        """Verify arguments are "sane"."""
        if not isinstance(name, str):
            raise TypeError('configuration name must be str, not {}'.format(type(name)))
        if level < 0:
            raise ValueError('level must be >= 0')
        if level > 0:
            if not isinstance(path, str):
                raise TypeError('path not set to a string')
            elif not path:
                raise ImportError('attempted relative import with no known path')
        if level > 2:
            raise ValueError('Invalid Path: level must be <= 2')
        if not name and level == 0:
            raise ValueError('Empty configuration name')

    @staticmethod
    def __get_config_path(config_name, path, type_=None):
        return Path(path) / (config_name + f'.{type_}' if type_ else '')

    @staticmethod
    def __level_parse(name, path=None):
        level = 0
        if name.startswith('.'):
            if not path:
                path = os.getcwd()
            for character in name:
                if character != '.':
                    break
                level += 1
        return level, path

    @staticmethod
    def __set_metadata(config_dict, obj, config_name, type_):
        config_dict['__name'] = config_name
        parent = obj.get_parent()
        parent_type = parent.get('__type', None) if parent else None
        if parent_type:
            config_dict['__parent_type'] = parent_type
        config_dict['__type'] = type_
        return config_dict
