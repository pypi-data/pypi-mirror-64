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

class WebChatMemberInfo(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        WebChatMemberInfo - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'avatar_image_url': 'str',
            'role': 'str',
            'join_date': 'datetime',
            'leave_date': 'datetime',
            'authenticated_guest': 'bool',
            'custom_fields': 'dict(str, str)',
            'state': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'avatar_image_url': 'avatarImageUrl',
            'role': 'role',
            'join_date': 'joinDate',
            'leave_date': 'leaveDate',
            'authenticated_guest': 'authenticatedGuest',
            'custom_fields': 'customFields',
            'state': 'state'
        }

        self._id = None
        self._display_name = None
        self._avatar_image_url = None
        self._role = None
        self._join_date = None
        self._leave_date = None
        self._authenticated_guest = None
        self._custom_fields = None
        self._state = None

    @property
    def id(self):
        """
        Gets the id of this WebChatMemberInfo.
        The communicationId of this member.

        :return: The id of this WebChatMemberInfo.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this WebChatMemberInfo.
        The communicationId of this member.

        :param id: The id of this WebChatMemberInfo.
        :type: str
        """
        
        self._id = id

    @property
    def display_name(self):
        """
        Gets the display_name of this WebChatMemberInfo.
        The display name of the member.

        :return: The display_name of this WebChatMemberInfo.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this WebChatMemberInfo.
        The display name of the member.

        :param display_name: The display_name of this WebChatMemberInfo.
        :type: str
        """
        
        self._display_name = display_name

    @property
    def avatar_image_url(self):
        """
        Gets the avatar_image_url of this WebChatMemberInfo.
        The url to the avatar image of the member.

        :return: The avatar_image_url of this WebChatMemberInfo.
        :rtype: str
        """
        return self._avatar_image_url

    @avatar_image_url.setter
    def avatar_image_url(self, avatar_image_url):
        """
        Sets the avatar_image_url of this WebChatMemberInfo.
        The url to the avatar image of the member.

        :param avatar_image_url: The avatar_image_url of this WebChatMemberInfo.
        :type: str
        """
        
        self._avatar_image_url = avatar_image_url

    @property
    def role(self):
        """
        Gets the role of this WebChatMemberInfo.
        The role of the member, one of [agent, customer, acd, workflow]

        :return: The role of this WebChatMemberInfo.
        :rtype: str
        """
        return self._role

    @role.setter
    def role(self, role):
        """
        Sets the role of this WebChatMemberInfo.
        The role of the member, one of [agent, customer, acd, workflow]

        :param role: The role of this WebChatMemberInfo.
        :type: str
        """
        allowed_values = ["AGENT", "CUSTOMER", "WORKFLOW", "ACD"]
        if role.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for role -> " + role
            self._role = "outdated_sdk_version"
        else:
            self._role = role

    @property
    def join_date(self):
        """
        Gets the join_date of this WebChatMemberInfo.
        The time the member joined the conversation. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The join_date of this WebChatMemberInfo.
        :rtype: datetime
        """
        return self._join_date

    @join_date.setter
    def join_date(self, join_date):
        """
        Sets the join_date of this WebChatMemberInfo.
        The time the member joined the conversation. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param join_date: The join_date of this WebChatMemberInfo.
        :type: datetime
        """
        
        self._join_date = join_date

    @property
    def leave_date(self):
        """
        Gets the leave_date of this WebChatMemberInfo.
        The time the member left the conversation, or null if the member is still active in the conversation. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The leave_date of this WebChatMemberInfo.
        :rtype: datetime
        """
        return self._leave_date

    @leave_date.setter
    def leave_date(self, leave_date):
        """
        Sets the leave_date of this WebChatMemberInfo.
        The time the member left the conversation, or null if the member is still active in the conversation. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param leave_date: The leave_date of this WebChatMemberInfo.
        :type: datetime
        """
        
        self._leave_date = leave_date

    @property
    def authenticated_guest(self):
        """
        Gets the authenticated_guest of this WebChatMemberInfo.
        If true, the guest member is an authenticated guest.

        :return: The authenticated_guest of this WebChatMemberInfo.
        :rtype: bool
        """
        return self._authenticated_guest

    @authenticated_guest.setter
    def authenticated_guest(self, authenticated_guest):
        """
        Sets the authenticated_guest of this WebChatMemberInfo.
        If true, the guest member is an authenticated guest.

        :param authenticated_guest: The authenticated_guest of this WebChatMemberInfo.
        :type: bool
        """
        
        self._authenticated_guest = authenticated_guest

    @property
    def custom_fields(self):
        """
        Gets the custom_fields of this WebChatMemberInfo.
        Any custom fields of information pertaining to this member.

        :return: The custom_fields of this WebChatMemberInfo.
        :rtype: dict(str, str)
        """
        return self._custom_fields

    @custom_fields.setter
    def custom_fields(self, custom_fields):
        """
        Sets the custom_fields of this WebChatMemberInfo.
        Any custom fields of information pertaining to this member.

        :param custom_fields: The custom_fields of this WebChatMemberInfo.
        :type: dict(str, str)
        """
        
        self._custom_fields = custom_fields

    @property
    def state(self):
        """
        Gets the state of this WebChatMemberInfo.
        The connection state of this member.

        :return: The state of this WebChatMemberInfo.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this WebChatMemberInfo.
        The connection state of this member.

        :param state: The state of this WebChatMemberInfo.
        :type: str
        """
        allowed_values = ["CONNECTED", "DISCONNECTED", "ALERTING"]
        if state.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for state -> " + state
            self._state = "outdated_sdk_version"
        else:
            self._state = state

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

