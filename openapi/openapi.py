from .object_base import ObjectBase

class OpenAPI(ObjectBase):
    """
    This class represents the root of the OpenAPI schema document, as defined
    in `the spec`_

    .. _the spec: https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.1.md#openapi-object
    """
    __slots__ = ['openapi','info','servers','paths','components','security','tags','externalDocs']

    def __init__(self, raw_document):
        """
        Creates a new OpenAPI document from a loaded spec file

        :param raw_document: The raw OpenAPI file loaded into python
        :type raw_document: dct
        """
        super().__init__([], raw_document) # as the document root, we have no path

        self._required_fields('openapi', 'info', 'paths')

        self.openapi = self._get('openapi', str)
        self.info = self._get('info', 'Info')
        raw_servers = self._get('servers', list)
        raw_paths = self._get('paths', dict)
        self.components = self._get('components', dict)
        self.security = self._get('security', dict)
        self.tags = self._get('tags', dict)
        self.externalDocs = self._get('externalDocs', dict)

        self.servers = self.parse_list(raw_servers, 'Server')

        # parse the path objects
        self.paths = {}
        for k, v in raw_paths.items():
            self.paths[k] = ObjectBase.get_object_type('Path')(['paths',k],v)