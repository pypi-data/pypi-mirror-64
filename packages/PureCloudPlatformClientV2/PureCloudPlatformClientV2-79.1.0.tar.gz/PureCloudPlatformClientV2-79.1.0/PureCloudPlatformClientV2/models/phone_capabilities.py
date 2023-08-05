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

class PhoneCapabilities(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        PhoneCapabilities - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'provisions': 'bool',
            'registers': 'bool',
            'dual_registers': 'bool',
            'hardware_id_type': 'str',
            'allow_reboot': 'bool',
            'no_rebalance': 'bool',
            'no_cloud_provisioning': 'bool',
            'media_codecs': 'list[str]'
        }

        self.attribute_map = {
            'provisions': 'provisions',
            'registers': 'registers',
            'dual_registers': 'dualRegisters',
            'hardware_id_type': 'hardwareIdType',
            'allow_reboot': 'allowReboot',
            'no_rebalance': 'noRebalance',
            'no_cloud_provisioning': 'noCloudProvisioning',
            'media_codecs': 'mediaCodecs'
        }

        self._provisions = None
        self._registers = None
        self._dual_registers = None
        self._hardware_id_type = None
        self._allow_reboot = None
        self._no_rebalance = None
        self._no_cloud_provisioning = None
        self._media_codecs = None

    @property
    def provisions(self):
        """
        Gets the provisions of this PhoneCapabilities.


        :return: The provisions of this PhoneCapabilities.
        :rtype: bool
        """
        return self._provisions

    @provisions.setter
    def provisions(self, provisions):
        """
        Sets the provisions of this PhoneCapabilities.


        :param provisions: The provisions of this PhoneCapabilities.
        :type: bool
        """
        
        self._provisions = provisions

    @property
    def registers(self):
        """
        Gets the registers of this PhoneCapabilities.


        :return: The registers of this PhoneCapabilities.
        :rtype: bool
        """
        return self._registers

    @registers.setter
    def registers(self, registers):
        """
        Sets the registers of this PhoneCapabilities.


        :param registers: The registers of this PhoneCapabilities.
        :type: bool
        """
        
        self._registers = registers

    @property
    def dual_registers(self):
        """
        Gets the dual_registers of this PhoneCapabilities.


        :return: The dual_registers of this PhoneCapabilities.
        :rtype: bool
        """
        return self._dual_registers

    @dual_registers.setter
    def dual_registers(self, dual_registers):
        """
        Sets the dual_registers of this PhoneCapabilities.


        :param dual_registers: The dual_registers of this PhoneCapabilities.
        :type: bool
        """
        
        self._dual_registers = dual_registers

    @property
    def hardware_id_type(self):
        """
        Gets the hardware_id_type of this PhoneCapabilities.


        :return: The hardware_id_type of this PhoneCapabilities.
        :rtype: str
        """
        return self._hardware_id_type

    @hardware_id_type.setter
    def hardware_id_type(self, hardware_id_type):
        """
        Sets the hardware_id_type of this PhoneCapabilities.


        :param hardware_id_type: The hardware_id_type of this PhoneCapabilities.
        :type: str
        """
        
        self._hardware_id_type = hardware_id_type

    @property
    def allow_reboot(self):
        """
        Gets the allow_reboot of this PhoneCapabilities.


        :return: The allow_reboot of this PhoneCapabilities.
        :rtype: bool
        """
        return self._allow_reboot

    @allow_reboot.setter
    def allow_reboot(self, allow_reboot):
        """
        Sets the allow_reboot of this PhoneCapabilities.


        :param allow_reboot: The allow_reboot of this PhoneCapabilities.
        :type: bool
        """
        
        self._allow_reboot = allow_reboot

    @property
    def no_rebalance(self):
        """
        Gets the no_rebalance of this PhoneCapabilities.


        :return: The no_rebalance of this PhoneCapabilities.
        :rtype: bool
        """
        return self._no_rebalance

    @no_rebalance.setter
    def no_rebalance(self, no_rebalance):
        """
        Sets the no_rebalance of this PhoneCapabilities.


        :param no_rebalance: The no_rebalance of this PhoneCapabilities.
        :type: bool
        """
        
        self._no_rebalance = no_rebalance

    @property
    def no_cloud_provisioning(self):
        """
        Gets the no_cloud_provisioning of this PhoneCapabilities.


        :return: The no_cloud_provisioning of this PhoneCapabilities.
        :rtype: bool
        """
        return self._no_cloud_provisioning

    @no_cloud_provisioning.setter
    def no_cloud_provisioning(self, no_cloud_provisioning):
        """
        Sets the no_cloud_provisioning of this PhoneCapabilities.


        :param no_cloud_provisioning: The no_cloud_provisioning of this PhoneCapabilities.
        :type: bool
        """
        
        self._no_cloud_provisioning = no_cloud_provisioning

    @property
    def media_codecs(self):
        """
        Gets the media_codecs of this PhoneCapabilities.


        :return: The media_codecs of this PhoneCapabilities.
        :rtype: list[str]
        """
        return self._media_codecs

    @media_codecs.setter
    def media_codecs(self, media_codecs):
        """
        Sets the media_codecs of this PhoneCapabilities.


        :param media_codecs: The media_codecs of this PhoneCapabilities.
        :type: list[str]
        """
        
        self._media_codecs = media_codecs

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

