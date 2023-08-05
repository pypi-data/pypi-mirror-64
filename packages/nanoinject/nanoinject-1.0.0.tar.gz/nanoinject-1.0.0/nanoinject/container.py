from .definition import Definition

class Container:
    _definitions: dict = {}
    _instances: dict = {}

    def __init__(self):
        self._definitions = {}
        self._instances = {}

    def add(self, service: str, callback) -> Definition:
        self._definitions[service] = Definition(callback)

        return self._definitions[service]

    def get(self, service: str):
        definition = self._get_definition(service)

        if definition.is_shared(): 
            return self._get_instance(service, definition)

        return self._build_instance(definition)

    def _get_definition(self, service: str) -> Definition:
        if service not in self._definitions:
            raise KeyError('Undefined service "%s"' % service)
        return self._definitions[service]

    def _get_instance(self, service: str, definition: Definition):
        if service not in self._instances:
            self._instances[service] = self._build_instance(definition)
        
        return self._instances[service]

    def _build_instance(self, definition: Definition):
        return definition.get_callback()(self)
