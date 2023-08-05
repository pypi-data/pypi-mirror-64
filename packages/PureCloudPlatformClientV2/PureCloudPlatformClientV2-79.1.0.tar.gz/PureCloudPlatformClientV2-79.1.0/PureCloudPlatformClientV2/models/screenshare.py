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

class Screenshare(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        Screenshare - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'state': 'str',
            'id': 'str',
            'context': 'str',
            'sharing': 'bool',
            'peer_count': 'int',
            'disconnect_type': 'str',
            'start_alerting_time': 'datetime',
            'connected_time': 'datetime',
            'disconnected_time': 'datetime',
            'provider': 'str',
            'peer_id': 'str',
            'segments': 'list[Segment]'
        }

        self.attribute_map = {
            'state': 'state',
            'id': 'id',
            'context': 'context',
            'sharing': 'sharing',
            'peer_count': 'peerCount',
            'disconnect_type': 'disconnectType',
            'start_alerting_time': 'startAlertingTime',
            'connected_time': 'connectedTime',
            'disconnected_time': 'disconnectedTime',
            'provider': 'provider',
            'peer_id': 'peerId',
            'segments': 'segments'
        }

        self._state = None
        self._id = None
        self._context = None
        self._sharing = None
        self._peer_count = None
        self._disconnect_type = None
        self._start_alerting_time = None
        self._connected_time = None
        self._disconnected_time = None
        self._provider = None
        self._peer_id = None
        self._segments = None

    @property
    def state(self):
        """
        Gets the state of this Screenshare.
        The connection state of this communication.

        :return: The state of this Screenshare.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this Screenshare.
        The connection state of this communication.

        :param state: The state of this Screenshare.
        :type: str
        """
        allowed_values = ["alerting", "dialing", "contacting", "offering", "connected", "disconnected", "terminated", "none"]
        if state.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for state -> " + state
            self._state = "outdated_sdk_version"
        else:
            self._state = state

    @property
    def id(self):
        """
        Gets the id of this Screenshare.
        A globally unique identifier for this communication.

        :return: The id of this Screenshare.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Screenshare.
        A globally unique identifier for this communication.

        :param id: The id of this Screenshare.
        :type: str
        """
        
        self._id = id

    @property
    def context(self):
        """
        Gets the context of this Screenshare.
        The room id context (xmpp jid) for the conference session.

        :return: The context of this Screenshare.
        :rtype: str
        """
        return self._context

    @context.setter
    def context(self, context):
        """
        Sets the context of this Screenshare.
        The room id context (xmpp jid) for the conference session.

        :param context: The context of this Screenshare.
        :type: str
        """
        
        self._context = context

    @property
    def sharing(self):
        """
        Gets the sharing of this Screenshare.
        Indicates whether this participant is sharing their screen.

        :return: The sharing of this Screenshare.
        :rtype: bool
        """
        return self._sharing

    @sharing.setter
    def sharing(self, sharing):
        """
        Sets the sharing of this Screenshare.
        Indicates whether this participant is sharing their screen.

        :param sharing: The sharing of this Screenshare.
        :type: bool
        """
        
        self._sharing = sharing

    @property
    def peer_count(self):
        """
        Gets the peer_count of this Screenshare.
        The number of peer participants from the perspective of the participant in the conference.

        :return: The peer_count of this Screenshare.
        :rtype: int
        """
        return self._peer_count

    @peer_count.setter
    def peer_count(self, peer_count):
        """
        Sets the peer_count of this Screenshare.
        The number of peer participants from the perspective of the participant in the conference.

        :param peer_count: The peer_count of this Screenshare.
        :type: int
        """
        
        self._peer_count = peer_count

    @property
    def disconnect_type(self):
        """
        Gets the disconnect_type of this Screenshare.
        System defined string indicating what caused the communication to disconnect. Will be null until the communication disconnects.

        :return: The disconnect_type of this Screenshare.
        :rtype: str
        """
        return self._disconnect_type

    @disconnect_type.setter
    def disconnect_type(self, disconnect_type):
        """
        Sets the disconnect_type of this Screenshare.
        System defined string indicating what caused the communication to disconnect. Will be null until the communication disconnects.

        :param disconnect_type: The disconnect_type of this Screenshare.
        :type: str
        """
        allowed_values = ["endpoint", "client", "system", "timeout", "transfer", "transfer.conference", "transfer.consult", "transfer.forward", "transfer.noanswer", "transfer.notavailable", "transport.failure", "error", "peer", "other", "spam", "uncallable"]
        if disconnect_type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for disconnect_type -> " + disconnect_type
            self._disconnect_type = "outdated_sdk_version"
        else:
            self._disconnect_type = disconnect_type

    @property
    def start_alerting_time(self):
        """
        Gets the start_alerting_time of this Screenshare.
        The timestamp the communication has when it is first put into an alerting state. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The start_alerting_time of this Screenshare.
        :rtype: datetime
        """
        return self._start_alerting_time

    @start_alerting_time.setter
    def start_alerting_time(self, start_alerting_time):
        """
        Sets the start_alerting_time of this Screenshare.
        The timestamp the communication has when it is first put into an alerting state. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param start_alerting_time: The start_alerting_time of this Screenshare.
        :type: datetime
        """
        
        self._start_alerting_time = start_alerting_time

    @property
    def connected_time(self):
        """
        Gets the connected_time of this Screenshare.
        The timestamp when this communication was connected in the cloud clock. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The connected_time of this Screenshare.
        :rtype: datetime
        """
        return self._connected_time

    @connected_time.setter
    def connected_time(self, connected_time):
        """
        Sets the connected_time of this Screenshare.
        The timestamp when this communication was connected in the cloud clock. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param connected_time: The connected_time of this Screenshare.
        :type: datetime
        """
        
        self._connected_time = connected_time

    @property
    def disconnected_time(self):
        """
        Gets the disconnected_time of this Screenshare.
        The timestamp when this communication disconnected from the conversation in the provider clock. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The disconnected_time of this Screenshare.
        :rtype: datetime
        """
        return self._disconnected_time

    @disconnected_time.setter
    def disconnected_time(self, disconnected_time):
        """
        Sets the disconnected_time of this Screenshare.
        The timestamp when this communication disconnected from the conversation in the provider clock. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param disconnected_time: The disconnected_time of this Screenshare.
        :type: datetime
        """
        
        self._disconnected_time = disconnected_time

    @property
    def provider(self):
        """
        Gets the provider of this Screenshare.
        The source provider for the screen share.

        :return: The provider of this Screenshare.
        :rtype: str
        """
        return self._provider

    @provider.setter
    def provider(self, provider):
        """
        Sets the provider of this Screenshare.
        The source provider for the screen share.

        :param provider: The provider of this Screenshare.
        :type: str
        """
        
        self._provider = provider

    @property
    def peer_id(self):
        """
        Gets the peer_id of this Screenshare.
        The id of the peer communication corresponding to a matching leg for this communication.

        :return: The peer_id of this Screenshare.
        :rtype: str
        """
        return self._peer_id

    @peer_id.setter
    def peer_id(self, peer_id):
        """
        Sets the peer_id of this Screenshare.
        The id of the peer communication corresponding to a matching leg for this communication.

        :param peer_id: The peer_id of this Screenshare.
        :type: str
        """
        
        self._peer_id = peer_id

    @property
    def segments(self):
        """
        Gets the segments of this Screenshare.
        The time line of the participant's call, divided into activity segments.

        :return: The segments of this Screenshare.
        :rtype: list[Segment]
        """
        return self._segments

    @segments.setter
    def segments(self, segments):
        """
        Sets the segments of this Screenshare.
        The time line of the participant's call, divided into activity segments.

        :param segments: The segments of this Screenshare.
        :type: list[Segment]
        """
        
        self._segments = segments

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

