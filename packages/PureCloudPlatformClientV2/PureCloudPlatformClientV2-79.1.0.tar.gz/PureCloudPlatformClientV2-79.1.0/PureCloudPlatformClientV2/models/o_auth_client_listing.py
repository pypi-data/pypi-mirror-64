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

class OAuthClientListing(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        OAuthClientListing - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'access_token_validity_seconds': 'int',
            'description': 'str',
            'registered_redirect_uri': 'list[str]',
            'secret': 'str',
            'role_ids': 'list[str]',
            'date_created': 'datetime',
            'date_modified': 'datetime',
            'created_by': 'DomainEntityRef',
            'modified_by': 'DomainEntityRef',
            'scope': 'list[str]',
            'role_divisions': 'list[RoleDivision]',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'access_token_validity_seconds': 'accessTokenValiditySeconds',
            'description': 'description',
            'registered_redirect_uri': 'registeredRedirectUri',
            'secret': 'secret',
            'role_ids': 'roleIds',
            'date_created': 'dateCreated',
            'date_modified': 'dateModified',
            'created_by': 'createdBy',
            'modified_by': 'modifiedBy',
            'scope': 'scope',
            'role_divisions': 'roleDivisions',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._access_token_validity_seconds = None
        self._description = None
        self._registered_redirect_uri = None
        self._secret = None
        self._role_ids = None
        self._date_created = None
        self._date_modified = None
        self._created_by = None
        self._modified_by = None
        self._scope = None
        self._role_divisions = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this OAuthClientListing.
        The globally unique identifier for the object.

        :return: The id of this OAuthClientListing.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this OAuthClientListing.
        The globally unique identifier for the object.

        :param id: The id of this OAuthClientListing.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this OAuthClientListing.
        The name of the OAuth client.

        :return: The name of this OAuthClientListing.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this OAuthClientListing.
        The name of the OAuth client.

        :param name: The name of this OAuthClientListing.
        :type: str
        """
        
        self._name = name

    @property
    def access_token_validity_seconds(self):
        """
        Gets the access_token_validity_seconds of this OAuthClientListing.
        The number of seconds, between 5mins and 48hrs, until tokens created with this client expire. If this field is omitted, a default of 24 hours will be applied.

        :return: The access_token_validity_seconds of this OAuthClientListing.
        :rtype: int
        """
        return self._access_token_validity_seconds

    @access_token_validity_seconds.setter
    def access_token_validity_seconds(self, access_token_validity_seconds):
        """
        Sets the access_token_validity_seconds of this OAuthClientListing.
        The number of seconds, between 5mins and 48hrs, until tokens created with this client expire. If this field is omitted, a default of 24 hours will be applied.

        :param access_token_validity_seconds: The access_token_validity_seconds of this OAuthClientListing.
        :type: int
        """
        
        self._access_token_validity_seconds = access_token_validity_seconds

    @property
    def description(self):
        """
        Gets the description of this OAuthClientListing.


        :return: The description of this OAuthClientListing.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this OAuthClientListing.


        :param description: The description of this OAuthClientListing.
        :type: str
        """
        
        self._description = description

    @property
    def registered_redirect_uri(self):
        """
        Gets the registered_redirect_uri of this OAuthClientListing.
        List of allowed callbacks for this client. For example: https://myap.example.com/auth/callback

        :return: The registered_redirect_uri of this OAuthClientListing.
        :rtype: list[str]
        """
        return self._registered_redirect_uri

    @registered_redirect_uri.setter
    def registered_redirect_uri(self, registered_redirect_uri):
        """
        Sets the registered_redirect_uri of this OAuthClientListing.
        List of allowed callbacks for this client. For example: https://myap.example.com/auth/callback

        :param registered_redirect_uri: The registered_redirect_uri of this OAuthClientListing.
        :type: list[str]
        """
        
        self._registered_redirect_uri = registered_redirect_uri

    @property
    def secret(self):
        """
        Gets the secret of this OAuthClientListing.
        System created secret assigned to this client. Secrets are required for code authorization and client credential grants.

        :return: The secret of this OAuthClientListing.
        :rtype: str
        """
        return self._secret

    @secret.setter
    def secret(self, secret):
        """
        Sets the secret of this OAuthClientListing.
        System created secret assigned to this client. Secrets are required for code authorization and client credential grants.

        :param secret: The secret of this OAuthClientListing.
        :type: str
        """
        
        self._secret = secret

    @property
    def role_ids(self):
        """
        Gets the role_ids of this OAuthClientListing.
        Deprecated. Use roleDivisions instead.

        :return: The role_ids of this OAuthClientListing.
        :rtype: list[str]
        """
        return self._role_ids

    @role_ids.setter
    def role_ids(self, role_ids):
        """
        Sets the role_ids of this OAuthClientListing.
        Deprecated. Use roleDivisions instead.

        :param role_ids: The role_ids of this OAuthClientListing.
        :type: list[str]
        """
        
        self._role_ids = role_ids

    @property
    def date_created(self):
        """
        Gets the date_created of this OAuthClientListing.
        Date this client was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_created of this OAuthClientListing.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this OAuthClientListing.
        Date this client was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_created: The date_created of this OAuthClientListing.
        :type: datetime
        """
        
        self._date_created = date_created

    @property
    def date_modified(self):
        """
        Gets the date_modified of this OAuthClientListing.
        Date this client was last modified. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_modified of this OAuthClientListing.
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """
        Sets the date_modified of this OAuthClientListing.
        Date this client was last modified. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_modified: The date_modified of this OAuthClientListing.
        :type: datetime
        """
        
        self._date_modified = date_modified

    @property
    def created_by(self):
        """
        Gets the created_by of this OAuthClientListing.
        User that created this client

        :return: The created_by of this OAuthClientListing.
        :rtype: DomainEntityRef
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """
        Sets the created_by of this OAuthClientListing.
        User that created this client

        :param created_by: The created_by of this OAuthClientListing.
        :type: DomainEntityRef
        """
        
        self._created_by = created_by

    @property
    def modified_by(self):
        """
        Gets the modified_by of this OAuthClientListing.
        User that last modified this client

        :return: The modified_by of this OAuthClientListing.
        :rtype: DomainEntityRef
        """
        return self._modified_by

    @modified_by.setter
    def modified_by(self, modified_by):
        """
        Sets the modified_by of this OAuthClientListing.
        User that last modified this client

        :param modified_by: The modified_by of this OAuthClientListing.
        :type: DomainEntityRef
        """
        
        self._modified_by = modified_by

    @property
    def scope(self):
        """
        Gets the scope of this OAuthClientListing.
        The scope requested by this client. Scopes only apply to clients not using the client_credential grant

        :return: The scope of this OAuthClientListing.
        :rtype: list[str]
        """
        return self._scope

    @scope.setter
    def scope(self, scope):
        """
        Sets the scope of this OAuthClientListing.
        The scope requested by this client. Scopes only apply to clients not using the client_credential grant

        :param scope: The scope of this OAuthClientListing.
        :type: list[str]
        """
        
        self._scope = scope

    @property
    def role_divisions(self):
        """
        Gets the role_divisions of this OAuthClientListing.
        Set of roles and their corresponding divisions associated with this client. Roles and divisions only apply to clients using the client_credential grant

        :return: The role_divisions of this OAuthClientListing.
        :rtype: list[RoleDivision]
        """
        return self._role_divisions

    @role_divisions.setter
    def role_divisions(self, role_divisions):
        """
        Sets the role_divisions of this OAuthClientListing.
        Set of roles and their corresponding divisions associated with this client. Roles and divisions only apply to clients using the client_credential grant

        :param role_divisions: The role_divisions of this OAuthClientListing.
        :type: list[RoleDivision]
        """
        
        self._role_divisions = role_divisions

    @property
    def self_uri(self):
        """
        Gets the self_uri of this OAuthClientListing.
        The URI for this object

        :return: The self_uri of this OAuthClientListing.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this OAuthClientListing.
        The URI for this object

        :param self_uri: The self_uri of this OAuthClientListing.
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

