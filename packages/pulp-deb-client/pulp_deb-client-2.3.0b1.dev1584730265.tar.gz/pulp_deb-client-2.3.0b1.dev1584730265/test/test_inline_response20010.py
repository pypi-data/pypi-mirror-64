# coding: utf-8

"""
    Pulp 3 API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulp_deb
from pulpcore.client.pulp_deb.models.inline_response20010 import InlineResponse20010  # noqa: E501
from pulpcore.client.pulp_deb.rest import ApiException

class TestInlineResponse20010(unittest.TestCase):
    """InlineResponse20010 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test InlineResponse20010
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_deb.models.inline_response20010.InlineResponse20010()  # noqa: E501
        if include_optional :
            return InlineResponse20010(
                count = 56, 
                next = '0', 
                previous = '0', 
                results = [
                    pulpcore.client.pulp_deb.models.deb/deb_publication.deb.DebPublication(
                        pulp_href = '0', 
                        pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        repository_version = '0', 
                        repository = '0', 
                        simple = True, 
                        structured = True, 
                        signing_service = '0', )
                    ]
            )
        else :
            return InlineResponse20010(
                count = 56,
                results = [
                    pulpcore.client.pulp_deb.models.deb/deb_publication.deb.DebPublication(
                        pulp_href = '0', 
                        pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        repository_version = '0', 
                        repository = '0', 
                        simple = True, 
                        structured = True, 
                        signing_service = '0', )
                    ],
        )

    def testInlineResponse20010(self):
        """Test InlineResponse20010"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
