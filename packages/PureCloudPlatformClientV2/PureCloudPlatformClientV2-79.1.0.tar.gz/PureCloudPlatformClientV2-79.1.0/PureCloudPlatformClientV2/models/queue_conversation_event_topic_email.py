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

class QueueConversationEventTopicEmail(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        QueueConversationEventTopicEmail - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'state': 'str',
            'held': 'bool',
            'auto_generated': 'bool',
            'subject': 'str',
            'provider': 'str',
            'script_id': 'str',
            'peer_id': 'str',
            'messages_sent': 'int',
            'error_info': 'QueueConversationEventTopicErrorDetails',
            'disconnect_type': 'str',
            'start_hold_time': 'datetime',
            'connected_time': 'datetime',
            'disconnected_time': 'datetime',
            'message_id': 'str',
            'direction': 'str',
            'draft_attachments': 'list[QueueConversationEventTopicAttachment]',
            'spam': 'bool',
            'additional_properties': 'object'
        }

        self.attribute_map = {
            'id': 'id',
            'state': 'state',
            'held': 'held',
            'auto_generated': 'autoGenerated',
            'subject': 'subject',
            'provider': 'provider',
            'script_id': 'scriptId',
            'peer_id': 'peerId',
            'messages_sent': 'messagesSent',
            'error_info': 'errorInfo',
            'disconnect_type': 'disconnectType',
            'start_hold_time': 'startHoldTime',
            'connected_time': 'connectedTime',
            'disconnected_time': 'disconnectedTime',
            'message_id': 'messageId',
            'direction': 'direction',
            'draft_attachments': 'draftAttachments',
            'spam': 'spam',
            'additional_properties': 'additionalProperties'
        }

        self._id = None
        self._state = None
        self._held = None
        self._auto_generated = None
        self._subject = None
        self._provider = None
        self._script_id = None
        self._peer_id = None
        self._messages_sent = None
        self._error_info = None
        self._disconnect_type = None
        self._start_hold_time = None
        self._connected_time = None
        self._disconnected_time = None
        self._message_id = None
        self._direction = None
        self._draft_attachments = None
        self._spam = None
        self._additional_properties = None

    @property
    def id(self):
        """
        Gets the id of this QueueConversationEventTopicEmail.


        :return: The id of this QueueConversationEventTopicEmail.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this QueueConversationEventTopicEmail.


        :param id: The id of this QueueConversationEventTopicEmail.
        :type: str
        """
        
        self._id = id

    @property
    def state(self):
        """
        Gets the state of this QueueConversationEventTopicEmail.


        :return: The state of this QueueConversationEventTopicEmail.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this QueueConversationEventTopicEmail.


        :param state: The state of this QueueConversationEventTopicEmail.
        :type: str
        """
        allowed_values = ["ALERTING", "CONNECTED", "DISCONNECTED", "NONE", "TRANSMITTING"]
        if state.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for state -> " + state
            self._state = "outdated_sdk_version"
        else:
            self._state = state

    @property
    def held(self):
        """
        Gets the held of this QueueConversationEventTopicEmail.


        :return: The held of this QueueConversationEventTopicEmail.
        :rtype: bool
        """
        return self._held

    @held.setter
    def held(self, held):
        """
        Sets the held of this QueueConversationEventTopicEmail.


        :param held: The held of this QueueConversationEventTopicEmail.
        :type: bool
        """
        
        self._held = held

    @property
    def auto_generated(self):
        """
        Gets the auto_generated of this QueueConversationEventTopicEmail.


        :return: The auto_generated of this QueueConversationEventTopicEmail.
        :rtype: bool
        """
        return self._auto_generated

    @auto_generated.setter
    def auto_generated(self, auto_generated):
        """
        Sets the auto_generated of this QueueConversationEventTopicEmail.


        :param auto_generated: The auto_generated of this QueueConversationEventTopicEmail.
        :type: bool
        """
        
        self._auto_generated = auto_generated

    @property
    def subject(self):
        """
        Gets the subject of this QueueConversationEventTopicEmail.


        :return: The subject of this QueueConversationEventTopicEmail.
        :rtype: str
        """
        return self._subject

    @subject.setter
    def subject(self, subject):
        """
        Sets the subject of this QueueConversationEventTopicEmail.


        :param subject: The subject of this QueueConversationEventTopicEmail.
        :type: str
        """
        
        self._subject = subject

    @property
    def provider(self):
        """
        Gets the provider of this QueueConversationEventTopicEmail.


        :return: The provider of this QueueConversationEventTopicEmail.
        :rtype: str
        """
        return self._provider

    @provider.setter
    def provider(self, provider):
        """
        Sets the provider of this QueueConversationEventTopicEmail.


        :param provider: The provider of this QueueConversationEventTopicEmail.
        :type: str
        """
        
        self._provider = provider

    @property
    def script_id(self):
        """
        Gets the script_id of this QueueConversationEventTopicEmail.


        :return: The script_id of this QueueConversationEventTopicEmail.
        :rtype: str
        """
        return self._script_id

    @script_id.setter
    def script_id(self, script_id):
        """
        Sets the script_id of this QueueConversationEventTopicEmail.


        :param script_id: The script_id of this QueueConversationEventTopicEmail.
        :type: str
        """
        
        self._script_id = script_id

    @property
    def peer_id(self):
        """
        Gets the peer_id of this QueueConversationEventTopicEmail.


        :return: The peer_id of this QueueConversationEventTopicEmail.
        :rtype: str
        """
        return self._peer_id

    @peer_id.setter
    def peer_id(self, peer_id):
        """
        Sets the peer_id of this QueueConversationEventTopicEmail.


        :param peer_id: The peer_id of this QueueConversationEventTopicEmail.
        :type: str
        """
        
        self._peer_id = peer_id

    @property
    def messages_sent(self):
        """
        Gets the messages_sent of this QueueConversationEventTopicEmail.


        :return: The messages_sent of this QueueConversationEventTopicEmail.
        :rtype: int
        """
        return self._messages_sent

    @messages_sent.setter
    def messages_sent(self, messages_sent):
        """
        Sets the messages_sent of this QueueConversationEventTopicEmail.


        :param messages_sent: The messages_sent of this QueueConversationEventTopicEmail.
        :type: int
        """
        
        self._messages_sent = messages_sent

    @property
    def error_info(self):
        """
        Gets the error_info of this QueueConversationEventTopicEmail.


        :return: The error_info of this QueueConversationEventTopicEmail.
        :rtype: QueueConversationEventTopicErrorDetails
        """
        return self._error_info

    @error_info.setter
    def error_info(self, error_info):
        """
        Sets the error_info of this QueueConversationEventTopicEmail.


        :param error_info: The error_info of this QueueConversationEventTopicEmail.
        :type: QueueConversationEventTopicErrorDetails
        """
        
        self._error_info = error_info

    @property
    def disconnect_type(self):
        """
        Gets the disconnect_type of this QueueConversationEventTopicEmail.


        :return: The disconnect_type of this QueueConversationEventTopicEmail.
        :rtype: str
        """
        return self._disconnect_type

    @disconnect_type.setter
    def disconnect_type(self, disconnect_type):
        """
        Sets the disconnect_type of this QueueConversationEventTopicEmail.


        :param disconnect_type: The disconnect_type of this QueueConversationEventTopicEmail.
        :type: str
        """
        allowed_values = ["ENDPOINT", "CLIENT", "SYSTEM", "TIMEOUT", "TRANSFER", "TRANSFER_CONFERENCE", "TRANSFER_CONSULT", "TRANSFER_FORWARD", "TRANSFER_NOANSWER", "TRANSFER_NOTAVAILABLE", "TRANSPORT_FAILURE", "ERROR", "PEER", "OTHER", "SPAM", "UNCALLABLE"]
        if disconnect_type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for disconnect_type -> " + disconnect_type
            self._disconnect_type = "outdated_sdk_version"
        else:
            self._disconnect_type = disconnect_type

    @property
    def start_hold_time(self):
        """
        Gets the start_hold_time of this QueueConversationEventTopicEmail.


        :return: The start_hold_time of this QueueConversationEventTopicEmail.
        :rtype: datetime
        """
        return self._start_hold_time

    @start_hold_time.setter
    def start_hold_time(self, start_hold_time):
        """
        Sets the start_hold_time of this QueueConversationEventTopicEmail.


        :param start_hold_time: The start_hold_time of this QueueConversationEventTopicEmail.
        :type: datetime
        """
        
        self._start_hold_time = start_hold_time

    @property
    def connected_time(self):
        """
        Gets the connected_time of this QueueConversationEventTopicEmail.


        :return: The connected_time of this QueueConversationEventTopicEmail.
        :rtype: datetime
        """
        return self._connected_time

    @connected_time.setter
    def connected_time(self, connected_time):
        """
        Sets the connected_time of this QueueConversationEventTopicEmail.


        :param connected_time: The connected_time of this QueueConversationEventTopicEmail.
        :type: datetime
        """
        
        self._connected_time = connected_time

    @property
    def disconnected_time(self):
        """
        Gets the disconnected_time of this QueueConversationEventTopicEmail.


        :return: The disconnected_time of this QueueConversationEventTopicEmail.
        :rtype: datetime
        """
        return self._disconnected_time

    @disconnected_time.setter
    def disconnected_time(self, disconnected_time):
        """
        Sets the disconnected_time of this QueueConversationEventTopicEmail.


        :param disconnected_time: The disconnected_time of this QueueConversationEventTopicEmail.
        :type: datetime
        """
        
        self._disconnected_time = disconnected_time

    @property
    def message_id(self):
        """
        Gets the message_id of this QueueConversationEventTopicEmail.


        :return: The message_id of this QueueConversationEventTopicEmail.
        :rtype: str
        """
        return self._message_id

    @message_id.setter
    def message_id(self, message_id):
        """
        Sets the message_id of this QueueConversationEventTopicEmail.


        :param message_id: The message_id of this QueueConversationEventTopicEmail.
        :type: str
        """
        
        self._message_id = message_id

    @property
    def direction(self):
        """
        Gets the direction of this QueueConversationEventTopicEmail.


        :return: The direction of this QueueConversationEventTopicEmail.
        :rtype: str
        """
        return self._direction

    @direction.setter
    def direction(self, direction):
        """
        Sets the direction of this QueueConversationEventTopicEmail.


        :param direction: The direction of this QueueConversationEventTopicEmail.
        :type: str
        """
        allowed_values = ["OUTBOUND", "INBOUND"]
        if direction.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for direction -> " + direction
            self._direction = "outdated_sdk_version"
        else:
            self._direction = direction

    @property
    def draft_attachments(self):
        """
        Gets the draft_attachments of this QueueConversationEventTopicEmail.


        :return: The draft_attachments of this QueueConversationEventTopicEmail.
        :rtype: list[QueueConversationEventTopicAttachment]
        """
        return self._draft_attachments

    @draft_attachments.setter
    def draft_attachments(self, draft_attachments):
        """
        Sets the draft_attachments of this QueueConversationEventTopicEmail.


        :param draft_attachments: The draft_attachments of this QueueConversationEventTopicEmail.
        :type: list[QueueConversationEventTopicAttachment]
        """
        
        self._draft_attachments = draft_attachments

    @property
    def spam(self):
        """
        Gets the spam of this QueueConversationEventTopicEmail.


        :return: The spam of this QueueConversationEventTopicEmail.
        :rtype: bool
        """
        return self._spam

    @spam.setter
    def spam(self, spam):
        """
        Sets the spam of this QueueConversationEventTopicEmail.


        :param spam: The spam of this QueueConversationEventTopicEmail.
        :type: bool
        """
        
        self._spam = spam

    @property
    def additional_properties(self):
        """
        Gets the additional_properties of this QueueConversationEventTopicEmail.


        :return: The additional_properties of this QueueConversationEventTopicEmail.
        :rtype: object
        """
        return self._additional_properties

    @additional_properties.setter
    def additional_properties(self, additional_properties):
        """
        Sets the additional_properties of this QueueConversationEventTopicEmail.


        :param additional_properties: The additional_properties of this QueueConversationEventTopicEmail.
        :type: object
        """
        
        self._additional_properties = additional_properties

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

