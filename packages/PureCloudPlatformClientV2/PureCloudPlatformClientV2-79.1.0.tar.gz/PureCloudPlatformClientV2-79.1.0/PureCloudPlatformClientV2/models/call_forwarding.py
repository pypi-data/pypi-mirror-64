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

class CallForwarding(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        CallForwarding - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'user': 'User',
            'enabled': 'bool',
            'phone_number': 'str',
            'calls': 'list[CallRoute]',
            'voicemail': 'str',
            'modified_date': 'datetime',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'user': 'user',
            'enabled': 'enabled',
            'phone_number': 'phoneNumber',
            'calls': 'calls',
            'voicemail': 'voicemail',
            'modified_date': 'modifiedDate',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._user = None
        self._enabled = None
        self._phone_number = None
        self._calls = None
        self._voicemail = None
        self._modified_date = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this CallForwarding.
        The globally unique identifier for the object.

        :return: The id of this CallForwarding.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this CallForwarding.
        The globally unique identifier for the object.

        :param id: The id of this CallForwarding.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this CallForwarding.


        :return: The name of this CallForwarding.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this CallForwarding.


        :param name: The name of this CallForwarding.
        :type: str
        """
        
        self._name = name

    @property
    def user(self):
        """
        Gets the user of this CallForwarding.


        :return: The user of this CallForwarding.
        :rtype: User
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Sets the user of this CallForwarding.


        :param user: The user of this CallForwarding.
        :type: User
        """
        
        self._user = user

    @property
    def enabled(self):
        """
        Gets the enabled of this CallForwarding.
        Whether or not CallForwarding is enabled

        :return: The enabled of this CallForwarding.
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """
        Sets the enabled of this CallForwarding.
        Whether or not CallForwarding is enabled

        :param enabled: The enabled of this CallForwarding.
        :type: bool
        """
        
        self._enabled = enabled

    @property
    def phone_number(self):
        """
        Gets the phone_number of this CallForwarding.
        This property is deprecated. Please use the calls property

        :return: The phone_number of this CallForwarding.
        :rtype: str
        """
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        """
        Sets the phone_number of this CallForwarding.
        This property is deprecated. Please use the calls property

        :param phone_number: The phone_number of this CallForwarding.
        :type: str
        """
        
        self._phone_number = phone_number

    @property
    def calls(self):
        """
        Gets the calls of this CallForwarding.
        An ordered list of CallRoutes to be executed when CallForwarding is enabled

        :return: The calls of this CallForwarding.
        :rtype: list[CallRoute]
        """
        return self._calls

    @calls.setter
    def calls(self, calls):
        """
        Sets the calls of this CallForwarding.
        An ordered list of CallRoutes to be executed when CallForwarding is enabled

        :param calls: The calls of this CallForwarding.
        :type: list[CallRoute]
        """
        
        self._calls = calls

    @property
    def voicemail(self):
        """
        Gets the voicemail of this CallForwarding.
        The type of voicemail to use with the callForwarding configuration

        :return: The voicemail of this CallForwarding.
        :rtype: str
        """
        return self._voicemail

    @voicemail.setter
    def voicemail(self, voicemail):
        """
        Sets the voicemail of this CallForwarding.
        The type of voicemail to use with the callForwarding configuration

        :param voicemail: The voicemail of this CallForwarding.
        :type: str
        """
        allowed_values = ["PURECLOUD", "LASTCALL", "NONE"]
        if voicemail.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for voicemail -> " + voicemail
            self._voicemail = "outdated_sdk_version"
        else:
            self._voicemail = voicemail

    @property
    def modified_date(self):
        """
        Gets the modified_date of this CallForwarding.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The modified_date of this CallForwarding.
        :rtype: datetime
        """
        return self._modified_date

    @modified_date.setter
    def modified_date(self, modified_date):
        """
        Sets the modified_date of this CallForwarding.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param modified_date: The modified_date of this CallForwarding.
        :type: datetime
        """
        
        self._modified_date = modified_date

    @property
    def self_uri(self):
        """
        Gets the self_uri of this CallForwarding.
        The URI for this object

        :return: The self_uri of this CallForwarding.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this CallForwarding.
        The URI for this object

        :param self_uri: The self_uri of this CallForwarding.
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

