from __future__ import annotations
import yaml
import importlib 
import logging
import re

from schema import Schema, And, Use, Optional

from .container import Container

class Config:
    """Allows end-users to configure the container based on either a Python dict or a YAML file."""
    def __init__(self, config: dict):
        # @TODO Do validation / sanity checking.
        self._config = self._validate_config(config)

    def configure(self, container: Container) -> Container:
        """Configures the container based on the configuration in this Config object"""
        for service_name, service_config in self._config['services'].items():
            definition = container.add(service_name, self._build_builder(service_name, service_config))

            if 'shared' in service_config and service_config['shared'] == False:
                definition.not_shared()

        return container

    @classmethod
    def from_yaml_file(cls, file_name: str) -> Config:
        """Parse a YAML file into config, and return an instance of Config"""
        with open(file_name, 'r') as file_handle:
            config = yaml.load(file_handle, Loader=yaml.FullLoader)

            return Config(config)

    def _build_builder(self, service_name, service_config):
        """Return a building callback"""
        module = importlib.import_module(service_config['module'])
        _class = getattr(module, service_config['class'])

        def build(container: Container):
            args = []
            if 'dependencies' in service_config:
                for dependency in service_config['dependencies']:
                    args.append(self._resolve_dependency(dependency, container))

            return _class(*args)

        return build

    def _resolve_dependency(self, dependency: str, container: Container):
        if dependency.startswith('value:'):
            match = re.match(r'^value:([^$]+)$', dependency)
            return self._get_value(match.group(1))

        return container.get(dependency)

    def _get_value(self, key: str):
        if (('values' not in self._config) or (key not in self._config['values'])):
            raise KeyError('Unable to find value named "%s"' % key)

        return self._config['values'][key]

    def _validate_config(self, config: dict) -> dict:
        config_schema = Schema({
            'services': And(Use(dict)),
            Optional('values'): And(Use(dict))
        })
        config_schema.validate(config)

        for service_name, service_config in config['services'].items():
            Schema(Use(str)).validate(service_name)
            service_schema = Schema({
                'class': And(Use(str)),
                'module': And(Use(str)),
                Optional('dependencies'): And(Use(list)),
                Optional('shared'): And(Use(bool))
            })

            service_schema.validate(service_config)

        return config
