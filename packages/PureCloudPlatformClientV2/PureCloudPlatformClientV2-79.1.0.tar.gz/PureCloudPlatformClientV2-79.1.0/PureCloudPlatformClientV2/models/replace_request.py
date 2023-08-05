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

class ReplaceRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ReplaceRequest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'change_number': 'int',
            'name': 'str',
            'auth_token': 'str'
        }

        self.attribute_map = {
            'change_number': 'changeNumber',
            'name': 'name',
            'auth_token': 'authToken'
        }

        self._change_number = None
        self._name = None
        self._auth_token = None

    @property
    def change_number(self):
        """
        Gets the change_number of this ReplaceRequest.


        :return: The change_number of this ReplaceRequest.
        :rtype: int
        """
        return self._change_number

    @change_number.setter
    def change_number(self, change_number):
        """
        Sets the change_number of this ReplaceRequest.


        :param change_number: The change_number of this ReplaceRequest.
        :type: int
        """
        
        self._change_number = change_number

    @property
    def name(self):
        """
        Gets the name of this ReplaceRequest.


        :return: The name of this ReplaceRequest.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ReplaceRequest.


        :param name: The name of this ReplaceRequest.
        :type: str
        """
        
        self._name = name

    @property
    def auth_token(self):
        """
        Gets the auth_token of this ReplaceRequest.


        :return: The auth_token of this ReplaceRequest.
        :rtype: str
        """
        return self._auth_token

    @auth_token.setter
    def auth_token(self, auth_token):
        """
        Sets the auth_token of this ReplaceRequest.


        :param auth_token: The auth_token of this ReplaceRequest.
        :type: str
        """
        
        self._auth_token = auth_token

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

