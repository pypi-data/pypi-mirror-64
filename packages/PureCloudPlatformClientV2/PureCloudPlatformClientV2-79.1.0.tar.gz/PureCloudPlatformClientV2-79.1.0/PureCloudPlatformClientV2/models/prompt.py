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

class Prompt(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        Prompt - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'description': 'str',
            'resources': 'list[PromptAsset]',
            'current_operation': 'Operation',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'description': 'description',
            'resources': 'resources',
            'current_operation': 'currentOperation',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._description = None
        self._resources = None
        self._current_operation = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this Prompt.
        The prompt identifier

        :return: The id of this Prompt.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Prompt.
        The prompt identifier

        :param id: The id of this Prompt.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this Prompt.
        The prompt name.

        :return: The name of this Prompt.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Prompt.
        The prompt name.

        :param name: The name of this Prompt.
        :type: str
        """
        
        self._name = name

    @property
    def description(self):
        """
        Gets the description of this Prompt.


        :return: The description of this Prompt.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this Prompt.


        :param description: The description of this Prompt.
        :type: str
        """
        
        self._description = description

    @property
    def resources(self):
        """
        Gets the resources of this Prompt.


        :return: The resources of this Prompt.
        :rtype: list[PromptAsset]
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """
        Sets the resources of this Prompt.


        :param resources: The resources of this Prompt.
        :type: list[PromptAsset]
        """
        
        self._resources = resources

    @property
    def current_operation(self):
        """
        Gets the current_operation of this Prompt.


        :return: The current_operation of this Prompt.
        :rtype: Operation
        """
        return self._current_operation

    @current_operation.setter
    def current_operation(self, current_operation):
        """
        Sets the current_operation of this Prompt.


        :param current_operation: The current_operation of this Prompt.
        :type: Operation
        """
        
        self._current_operation = current_operation

    @property
    def self_uri(self):
        """
        Gets the self_uri of this Prompt.
        The URI for this object

        :return: The self_uri of this Prompt.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this Prompt.
        The URI for this object

        :param self_uri: The self_uri of this Prompt.
        :type: str
        """
        
        self._self_uri = self_uri

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

