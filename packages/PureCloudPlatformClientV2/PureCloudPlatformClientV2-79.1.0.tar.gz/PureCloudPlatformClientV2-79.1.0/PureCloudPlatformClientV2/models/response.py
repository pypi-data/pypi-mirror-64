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

class Response(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        Response - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'version': 'int',
            'libraries': 'list[DomainEntityRef]',
            'texts': 'list[ResponseText]',
            'created_by': 'User',
            'date_created': 'datetime',
            'interaction_type': 'str',
            'substitutions': 'list[ResponseSubstitution]',
            'substitutions_schema': 'JsonSchemaDocument',
            'response_type': 'str',
            'messaging_template': 'MessagingTemplate',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'version': 'version',
            'libraries': 'libraries',
            'texts': 'texts',
            'created_by': 'createdBy',
            'date_created': 'dateCreated',
            'interaction_type': 'interactionType',
            'substitutions': 'substitutions',
            'substitutions_schema': 'substitutionsSchema',
            'response_type': 'responseType',
            'messaging_template': 'messagingTemplate',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._version = None
        self._libraries = None
        self._texts = None
        self._created_by = None
        self._date_created = None
        self._interaction_type = None
        self._substitutions = None
        self._substitutions_schema = None
        self._response_type = None
        self._messaging_template = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this Response.
        The globally unique identifier for the object.

        :return: The id of this Response.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Response.
        The globally unique identifier for the object.

        :param id: The id of this Response.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this Response.


        :return: The name of this Response.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Response.


        :param name: The name of this Response.
        :type: str
        """
        
        self._name = name

    @property
    def version(self):
        """
        Gets the version of this Response.
        Version number required for updates.

        :return: The version of this Response.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this Response.
        Version number required for updates.

        :param version: The version of this Response.
        :type: int
        """
        
        self._version = version

    @property
    def libraries(self):
        """
        Gets the libraries of this Response.
        One or more libraries response is associated with.

        :return: The libraries of this Response.
        :rtype: list[DomainEntityRef]
        """
        return self._libraries

    @libraries.setter
    def libraries(self, libraries):
        """
        Sets the libraries of this Response.
        One or more libraries response is associated with.

        :param libraries: The libraries of this Response.
        :type: list[DomainEntityRef]
        """
        
        self._libraries = libraries

    @property
    def texts(self):
        """
        Gets the texts of this Response.
        One or more texts associated with the response.

        :return: The texts of this Response.
        :rtype: list[ResponseText]
        """
        return self._texts

    @texts.setter
    def texts(self, texts):
        """
        Sets the texts of this Response.
        One or more texts associated with the response.

        :param texts: The texts of this Response.
        :type: list[ResponseText]
        """
        
        self._texts = texts

    @property
    def created_by(self):
        """
        Gets the created_by of this Response.
        User that created the response

        :return: The created_by of this Response.
        :rtype: User
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """
        Sets the created_by of this Response.
        User that created the response

        :param created_by: The created_by of this Response.
        :type: User
        """
        
        self._created_by = created_by

    @property
    def date_created(self):
        """
        Gets the date_created of this Response.
        The date and time the response was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_created of this Response.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this Response.
        The date and time the response was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_created: The date_created of this Response.
        :type: datetime
        """
        
        self._date_created = date_created

    @property
    def interaction_type(self):
        """
        Gets the interaction_type of this Response.
        The interaction type for this response.

        :return: The interaction_type of this Response.
        :rtype: str
        """
        return self._interaction_type

    @interaction_type.setter
    def interaction_type(self, interaction_type):
        """
        Sets the interaction_type of this Response.
        The interaction type for this response.

        :param interaction_type: The interaction_type of this Response.
        :type: str
        """
        allowed_values = ["chat", "email", "twitter"]
        if interaction_type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for interaction_type -> " + interaction_type
            self._interaction_type = "outdated_sdk_version"
        else:
            self._interaction_type = interaction_type

    @property
    def substitutions(self):
        """
        Gets the substitutions of this Response.
        Details about any text substitutions used in the texts for this response.

        :return: The substitutions of this Response.
        :rtype: list[ResponseSubstitution]
        """
        return self._substitutions

    @substitutions.setter
    def substitutions(self, substitutions):
        """
        Sets the substitutions of this Response.
        Details about any text substitutions used in the texts for this response.

        :param substitutions: The substitutions of this Response.
        :type: list[ResponseSubstitution]
        """
        
        self._substitutions = substitutions

    @property
    def substitutions_schema(self):
        """
        Gets the substitutions_schema of this Response.
        Metadata about the text substitutions in json schema format.

        :return: The substitutions_schema of this Response.
        :rtype: JsonSchemaDocument
        """
        return self._substitutions_schema

    @substitutions_schema.setter
    def substitutions_schema(self, substitutions_schema):
        """
        Sets the substitutions_schema of this Response.
        Metadata about the text substitutions in json schema format.

        :param substitutions_schema: The substitutions_schema of this Response.
        :type: JsonSchemaDocument
        """
        
        self._substitutions_schema = substitutions_schema

    @property
    def response_type(self):
        """
        Gets the response_type of this Response.
        The response type represented by the response

        :return: The response_type of this Response.
        :rtype: str
        """
        return self._response_type

    @response_type.setter
    def response_type(self, response_type):
        """
        Sets the response_type of this Response.
        The response type represented by the response

        :param response_type: The response_type of this Response.
        :type: str
        """
        allowed_values = ["MessagingTemplate"]
        if response_type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for response_type -> " + response_type
            self._response_type = "outdated_sdk_version"
        else:
            self._response_type = response_type

    @property
    def messaging_template(self):
        """
        Gets the messaging_template of this Response.
        The messaging template definition. This is required when adding to a library with responseType set to MessagingTemplate.

        :return: The messaging_template of this Response.
        :rtype: MessagingTemplate
        """
        return self._messaging_template

    @messaging_template.setter
    def messaging_template(self, messaging_template):
        """
        Sets the messaging_template of this Response.
        The messaging template definition. This is required when adding to a library with responseType set to MessagingTemplate.

        :param messaging_template: The messaging_template of this Response.
        :type: MessagingTemplate
        """
        
        self._messaging_template = messaging_template

    @property
    def self_uri(self):
        """
        Gets the self_uri of this Response.
        The URI for this object

        :return: The self_uri of this Response.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this Response.
        The URI for this object

        :param self_uri: The self_uri of this Response.
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

