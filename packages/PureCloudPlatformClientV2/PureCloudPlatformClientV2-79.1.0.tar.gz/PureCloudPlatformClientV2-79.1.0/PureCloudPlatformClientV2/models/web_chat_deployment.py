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

class WebChatDeployment(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        WebChatDeployment - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'description': 'str',
            'authentication_required': 'bool',
            'authentication_url': 'str',
            'disabled': 'bool',
            'web_chat_config': 'WebChatConfig',
            'allowed_domains': 'list[str]',
            'flow': 'DomainEntityRef',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'description': 'description',
            'authentication_required': 'authenticationRequired',
            'authentication_url': 'authenticationUrl',
            'disabled': 'disabled',
            'web_chat_config': 'webChatConfig',
            'allowed_domains': 'allowedDomains',
            'flow': 'flow',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._description = None
        self._authentication_required = None
        self._authentication_url = None
        self._disabled = None
        self._web_chat_config = None
        self._allowed_domains = None
        self._flow = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this WebChatDeployment.
        The globally unique identifier for the object.

        :return: The id of this WebChatDeployment.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this WebChatDeployment.
        The globally unique identifier for the object.

        :param id: The id of this WebChatDeployment.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this WebChatDeployment.


        :return: The name of this WebChatDeployment.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this WebChatDeployment.


        :param name: The name of this WebChatDeployment.
        :type: str
        """
        
        self._name = name

    @property
    def description(self):
        """
        Gets the description of this WebChatDeployment.


        :return: The description of this WebChatDeployment.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this WebChatDeployment.


        :param description: The description of this WebChatDeployment.
        :type: str
        """
        
        self._description = description

    @property
    def authentication_required(self):
        """
        Gets the authentication_required of this WebChatDeployment.


        :return: The authentication_required of this WebChatDeployment.
        :rtype: bool
        """
        return self._authentication_required

    @authentication_required.setter
    def authentication_required(self, authentication_required):
        """
        Sets the authentication_required of this WebChatDeployment.


        :param authentication_required: The authentication_required of this WebChatDeployment.
        :type: bool
        """
        
        self._authentication_required = authentication_required

    @property
    def authentication_url(self):
        """
        Gets the authentication_url of this WebChatDeployment.
        URL for third party service authenticating web chat clients. See https://github.com/MyPureCloud/authenticated-web-chat-server-examples

        :return: The authentication_url of this WebChatDeployment.
        :rtype: str
        """
        return self._authentication_url

    @authentication_url.setter
    def authentication_url(self, authentication_url):
        """
        Sets the authentication_url of this WebChatDeployment.
        URL for third party service authenticating web chat clients. See https://github.com/MyPureCloud/authenticated-web-chat-server-examples

        :param authentication_url: The authentication_url of this WebChatDeployment.
        :type: str
        """
        
        self._authentication_url = authentication_url

    @property
    def disabled(self):
        """
        Gets the disabled of this WebChatDeployment.


        :return: The disabled of this WebChatDeployment.
        :rtype: bool
        """
        return self._disabled

    @disabled.setter
    def disabled(self, disabled):
        """
        Sets the disabled of this WebChatDeployment.


        :param disabled: The disabled of this WebChatDeployment.
        :type: bool
        """
        
        self._disabled = disabled

    @property
    def web_chat_config(self):
        """
        Gets the web_chat_config of this WebChatDeployment.


        :return: The web_chat_config of this WebChatDeployment.
        :rtype: WebChatConfig
        """
        return self._web_chat_config

    @web_chat_config.setter
    def web_chat_config(self, web_chat_config):
        """
        Sets the web_chat_config of this WebChatDeployment.


        :param web_chat_config: The web_chat_config of this WebChatDeployment.
        :type: WebChatConfig
        """
        
        self._web_chat_config = web_chat_config

    @property
    def allowed_domains(self):
        """
        Gets the allowed_domains of this WebChatDeployment.


        :return: The allowed_domains of this WebChatDeployment.
        :rtype: list[str]
        """
        return self._allowed_domains

    @allowed_domains.setter
    def allowed_domains(self, allowed_domains):
        """
        Sets the allowed_domains of this WebChatDeployment.


        :param allowed_domains: The allowed_domains of this WebChatDeployment.
        :type: list[str]
        """
        
        self._allowed_domains = allowed_domains

    @property
    def flow(self):
        """
        Gets the flow of this WebChatDeployment.
        The URI of the Inbound Chat Flow to run when new chats are initiated under this Deployment.

        :return: The flow of this WebChatDeployment.
        :rtype: DomainEntityRef
        """
        return self._flow

    @flow.setter
    def flow(self, flow):
        """
        Sets the flow of this WebChatDeployment.
        The URI of the Inbound Chat Flow to run when new chats are initiated under this Deployment.

        :param flow: The flow of this WebChatDeployment.
        :type: DomainEntityRef
        """
        
        self._flow = flow

    @property
    def self_uri(self):
        """
        Gets the self_uri of this WebChatDeployment.
        The URI for this object

        :return: The self_uri of this WebChatDeployment.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this WebChatDeployment.
        The URI for this object

        :param self_uri: The self_uri of this WebChatDeployment.
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

