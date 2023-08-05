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

class DncListCreate(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        DncListCreate - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'date_created': 'datetime',
            'date_modified': 'datetime',
            'version': 'int',
            'import_status': 'ImportStatus',
            'size': 'int',
            'dnc_source_type': 'str',
            'login_id': 'str',
            'dnc_codes': 'list[str]',
            'license_id': 'str',
            'division': 'DomainEntityRef',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'date_created': 'dateCreated',
            'date_modified': 'dateModified',
            'version': 'version',
            'import_status': 'importStatus',
            'size': 'size',
            'dnc_source_type': 'dncSourceType',
            'login_id': 'loginId',
            'dnc_codes': 'dncCodes',
            'license_id': 'licenseId',
            'division': 'division',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._date_created = None
        self._date_modified = None
        self._version = None
        self._import_status = None
        self._size = None
        self._dnc_source_type = None
        self._login_id = None
        self._dnc_codes = None
        self._license_id = None
        self._division = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this DncListCreate.
        The globally unique identifier for the object.

        :return: The id of this DncListCreate.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this DncListCreate.
        The globally unique identifier for the object.

        :param id: The id of this DncListCreate.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this DncListCreate.
        The name of the DncList.

        :return: The name of this DncListCreate.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this DncListCreate.
        The name of the DncList.

        :param name: The name of this DncListCreate.
        :type: str
        """
        
        self._name = name

    @property
    def date_created(self):
        """
        Gets the date_created of this DncListCreate.
        Creation time of the entity. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_created of this DncListCreate.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this DncListCreate.
        Creation time of the entity. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_created: The date_created of this DncListCreate.
        :type: datetime
        """
        
        self._date_created = date_created

    @property
    def date_modified(self):
        """
        Gets the date_modified of this DncListCreate.
        Last modified time of the entity. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_modified of this DncListCreate.
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """
        Sets the date_modified of this DncListCreate.
        Last modified time of the entity. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_modified: The date_modified of this DncListCreate.
        :type: datetime
        """
        
        self._date_modified = date_modified

    @property
    def version(self):
        """
        Gets the version of this DncListCreate.
        Required for updates, must match the version number of the most recent update

        :return: The version of this DncListCreate.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this DncListCreate.
        Required for updates, must match the version number of the most recent update

        :param version: The version of this DncListCreate.
        :type: int
        """
        
        self._version = version

    @property
    def import_status(self):
        """
        Gets the import_status of this DncListCreate.
        The status of the import process

        :return: The import_status of this DncListCreate.
        :rtype: ImportStatus
        """
        return self._import_status

    @import_status.setter
    def import_status(self, import_status):
        """
        Sets the import_status of this DncListCreate.
        The status of the import process

        :param import_status: The import_status of this DncListCreate.
        :type: ImportStatus
        """
        
        self._import_status = import_status

    @property
    def size(self):
        """
        Gets the size of this DncListCreate.
        The total number of phone numbers in the DncList.

        :return: The size of this DncListCreate.
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """
        Sets the size of this DncListCreate.
        The total number of phone numbers in the DncList.

        :param size: The size of this DncListCreate.
        :type: int
        """
        
        self._size = size

    @property
    def dnc_source_type(self):
        """
        Gets the dnc_source_type of this DncListCreate.
        The type of the DncList.

        :return: The dnc_source_type of this DncListCreate.
        :rtype: str
        """
        return self._dnc_source_type

    @dnc_source_type.setter
    def dnc_source_type(self, dnc_source_type):
        """
        Sets the dnc_source_type of this DncListCreate.
        The type of the DncList.

        :param dnc_source_type: The dnc_source_type of this DncListCreate.
        :type: str
        """
        allowed_values = ["rds", "dnc.com", "gryphon"]
        if dnc_source_type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for dnc_source_type -> " + dnc_source_type
            self._dnc_source_type = "outdated_sdk_version"
        else:
            self._dnc_source_type = dnc_source_type

    @property
    def login_id(self):
        """
        Gets the login_id of this DncListCreate.
        A dnc.com loginId. Required if the dncSourceType is dnc.com.

        :return: The login_id of this DncListCreate.
        :rtype: str
        """
        return self._login_id

    @login_id.setter
    def login_id(self, login_id):
        """
        Sets the login_id of this DncListCreate.
        A dnc.com loginId. Required if the dncSourceType is dnc.com.

        :param login_id: The login_id of this DncListCreate.
        :type: str
        """
        
        self._login_id = login_id

    @property
    def dnc_codes(self):
        """
        Gets the dnc_codes of this DncListCreate.
        The list of dnc.com codes to be treated as DNC. Required if the dncSourceType is dnc.com.

        :return: The dnc_codes of this DncListCreate.
        :rtype: list[str]
        """
        return self._dnc_codes

    @dnc_codes.setter
    def dnc_codes(self, dnc_codes):
        """
        Sets the dnc_codes of this DncListCreate.
        The list of dnc.com codes to be treated as DNC. Required if the dncSourceType is dnc.com.

        :param dnc_codes: The dnc_codes of this DncListCreate.
        :type: list[str]
        """
        
        self._dnc_codes = dnc_codes

    @property
    def license_id(self):
        """
        Gets the license_id of this DncListCreate.
        A gryphon license number. Required if the dncSourceType is gryphon.

        :return: The license_id of this DncListCreate.
        :rtype: str
        """
        return self._license_id

    @license_id.setter
    def license_id(self, license_id):
        """
        Sets the license_id of this DncListCreate.
        A gryphon license number. Required if the dncSourceType is gryphon.

        :param license_id: The license_id of this DncListCreate.
        :type: str
        """
        
        self._license_id = license_id

    @property
    def division(self):
        """
        Gets the division of this DncListCreate.
        The division this DncList belongs to.

        :return: The division of this DncListCreate.
        :rtype: DomainEntityRef
        """
        return self._division

    @division.setter
    def division(self, division):
        """
        Sets the division of this DncListCreate.
        The division this DncList belongs to.

        :param division: The division of this DncListCreate.
        :type: DomainEntityRef
        """
        
        self._division = division

    @property
    def self_uri(self):
        """
        Gets the self_uri of this DncListCreate.
        The URI for this object

        :return: The self_uri of this DncListCreate.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this DncListCreate.
        The URI for this object

        :param self_uri: The self_uri of this DncListCreate.
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

