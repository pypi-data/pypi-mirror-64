# -*- coding: utf-8 -*-

"""
Add schema endpoint if you have models to expose
"""

from restapi.rest.definition import EndpointResource
from restapi.decorators import catch_error
# from restapi.utilities.logs import log


class RecoverSchema(EndpointResource):
    @catch_error()
    def get(self, **kwargs):
        """ Expose schemas for UIs automatic form building """

        # FIXME: not from json but from query
        method = self.get_input(single_parameter='method', default='POST')

        # schema_definition = self.get_endpoint_definition(
        #     key='parameters', is_schema_url=True, method=method)

        custom_definition = self.get_endpoint_custom_definition(
            method=method, is_schema_url=True
        )

        return self.force_response(custom_definition)
