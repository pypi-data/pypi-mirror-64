# coding: utf-8

"""
Copyright 2016 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from pprint import pformat
from six import iteritems
import re
import json

from ..utils import sanitize_for_serialization

class GKNDocumentationSearchRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        GKNDocumentationSearchRequest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'sort_order': 'str',
            'sort_by': 'str',
            'page_size': 'int',
            'page_number': 'int',
            'sort': 'list[SearchSort]',
            'query': 'list[GKNDocumentationSearchCriteria]'
        }

        self.attribute_map = {
            'sort_order': 'sortOrder',
            'sort_by': 'sortBy',
            'page_size': 'pageSize',
            'page_number': 'pageNumber',
            'sort': 'sort',
            'query': 'query'
        }

        self._sort_order = None
        self._sort_by = None
        self._page_size = None
        self._page_number = None
        self._sort = None
        self._query = None

    @property
    def sort_order(self):
        """
        Gets the sort_order of this GKNDocumentationSearchRequest.
        The sort order for results

        :return: The sort_order of this GKNDocumentationSearchRequest.
        :rtype: str
        """
        return self._sort_order

    @sort_order.setter
    def sort_order(self, sort_order):
        """
        Sets the sort_order of this GKNDocumentationSearchRequest.
        The sort order for results

        :param sort_order: The sort_order of this GKNDocumentationSearchRequest.
        :type: str
        """
        allowed_values = ["ASC", "DESC", "SCORE"]
        if sort_order.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for sort_order -> " + sort_order
            self._sort_order = "outdated_sdk_version"
        else:
            self._sort_order = sort_order

    @property
    def sort_by(self):
        """
        Gets the sort_by of this GKNDocumentationSearchRequest.
        The field in the resource that you want to sort the results by

        :return: The sort_by of this GKNDocumentationSearchRequest.
        :rtype: str
        """
        return self._sort_by

    @sort_by.setter
    def sort_by(self, sort_by):
        """
        Sets the sort_by of this GKNDocumentationSearchRequest.
        The field in the resource that you want to sort the results by

        :param sort_by: The sort_by of this GKNDocumentationSearchRequest.
        :type: str
        """
        
        self._sort_by = sort_by

    @property
    def page_size(self):
        """
        Gets the page_size of this GKNDocumentationSearchRequest.
        The number of results per page

        :return: The page_size of this GKNDocumentationSearchRequest.
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """
        Sets the page_size of this GKNDocumentationSearchRequest.
        The number of results per page

        :param page_size: The page_size of this GKNDocumentationSearchRequest.
        :type: int
        """
        
        self._page_size = page_size

    @property
    def page_number(self):
        """
        Gets the page_number of this GKNDocumentationSearchRequest.
        The page of resources you want to retrieve

        :return: The page_number of this GKNDocumentationSearchRequest.
        :rtype: int
        """
        return self._page_number

    @page_number.setter
    def page_number(self, page_number):
        """
        Sets the page_number of this GKNDocumentationSearchRequest.
        The page of resources you want to retrieve

        :param page_number: The page_number of this GKNDocumentationSearchRequest.
        :type: int
        """
        
        self._page_number = page_number

    @property
    def sort(self):
        """
        Gets the sort of this GKNDocumentationSearchRequest.
        Multi-value sort order, list of multiple sort values

        :return: The sort of this GKNDocumentationSearchRequest.
        :rtype: list[SearchSort]
        """
        return self._sort

    @sort.setter
    def sort(self, sort):
        """
        Sets the sort of this GKNDocumentationSearchRequest.
        Multi-value sort order, list of multiple sort values

        :param sort: The sort of this GKNDocumentationSearchRequest.
        :type: list[SearchSort]
        """
        
        self._sort = sort

    @property
    def query(self):
        """
        Gets the query of this GKNDocumentationSearchRequest.


        :return: The query of this GKNDocumentationSearchRequest.
        :rtype: list[GKNDocumentationSearchCriteria]
        """
        return self._query

    @query.setter
    def query(self, query):
        """
        Sets the query of this GKNDocumentationSearchRequest.


        :param query: The query of this GKNDocumentationSearchRequest.
        :type: list[GKNDocumentationSearchCriteria]
        """
        
        self._query = query

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_json(self):
        """
        Returns the model as raw JSON
        """
        return json.dumps(sanitize_for_serialization(self.to_dict()))

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

