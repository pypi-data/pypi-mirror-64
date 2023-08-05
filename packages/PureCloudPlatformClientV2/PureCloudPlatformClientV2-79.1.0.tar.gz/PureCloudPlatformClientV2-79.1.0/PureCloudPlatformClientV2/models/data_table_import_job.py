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

class DataTableImportJob(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        DataTableImportJob - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'owner': 'AddressableEntityRef',
            'status': 'str',
            'date_created': 'datetime',
            'date_completed': 'datetime',
            'upload_uri': 'str',
            'import_mode': 'str',
            'error_information': 'ErrorBody',
            'count_records_updated': 'int',
            'count_records_deleted': 'int',
            'count_records_failed': 'int',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'owner': 'owner',
            'status': 'status',
            'date_created': 'dateCreated',
            'date_completed': 'dateCompleted',
            'upload_uri': 'uploadURI',
            'import_mode': 'importMode',
            'error_information': 'errorInformation',
            'count_records_updated': 'countRecordsUpdated',
            'count_records_deleted': 'countRecordsDeleted',
            'count_records_failed': 'countRecordsFailed',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._owner = None
        self._status = None
        self._date_created = None
        self._date_completed = None
        self._upload_uri = None
        self._import_mode = None
        self._error_information = None
        self._count_records_updated = None
        self._count_records_deleted = None
        self._count_records_failed = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this DataTableImportJob.
        The globally unique identifier for the object.

        :return: The id of this DataTableImportJob.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this DataTableImportJob.
        The globally unique identifier for the object.

        :param id: The id of this DataTableImportJob.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this DataTableImportJob.


        :return: The name of this DataTableImportJob.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this DataTableImportJob.


        :param name: The name of this DataTableImportJob.
        :type: str
        """
        
        self._name = name

    @property
    def owner(self):
        """
        Gets the owner of this DataTableImportJob.
        The PureCloud user who started the import job

        :return: The owner of this DataTableImportJob.
        :rtype: AddressableEntityRef
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """
        Sets the owner of this DataTableImportJob.
        The PureCloud user who started the import job

        :param owner: The owner of this DataTableImportJob.
        :type: AddressableEntityRef
        """
        
        self._owner = owner

    @property
    def status(self):
        """
        Gets the status of this DataTableImportJob.
        The status of the import job

        :return: The status of this DataTableImportJob.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this DataTableImportJob.
        The status of the import job

        :param status: The status of this DataTableImportJob.
        :type: str
        """
        allowed_values = ["WaitingForUpload", "Processing", "Failed", "Succeeded"]
        if status.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for status -> " + status
            self._status = "outdated_sdk_version"
        else:
            self._status = status

    @property
    def date_created(self):
        """
        Gets the date_created of this DataTableImportJob.
        The timestamp of when the import began. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_created of this DataTableImportJob.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this DataTableImportJob.
        The timestamp of when the import began. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_created: The date_created of this DataTableImportJob.
        :type: datetime
        """
        
        self._date_created = date_created

    @property
    def date_completed(self):
        """
        Gets the date_completed of this DataTableImportJob.
        The timestamp of when the import stopped (either successfully or unsuccessfully). Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_completed of this DataTableImportJob.
        :rtype: datetime
        """
        return self._date_completed

    @date_completed.setter
    def date_completed(self, date_completed):
        """
        Sets the date_completed of this DataTableImportJob.
        The timestamp of when the import stopped (either successfully or unsuccessfully). Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_completed: The date_completed of this DataTableImportJob.
        :type: datetime
        """
        
        self._date_completed = date_completed

    @property
    def upload_uri(self):
        """
        Gets the upload_uri of this DataTableImportJob.
        The URL of the location at which the caller can upload the file to be imported

        :return: The upload_uri of this DataTableImportJob.
        :rtype: str
        """
        return self._upload_uri

    @upload_uri.setter
    def upload_uri(self, upload_uri):
        """
        Sets the upload_uri of this DataTableImportJob.
        The URL of the location at which the caller can upload the file to be imported

        :param upload_uri: The upload_uri of this DataTableImportJob.
        :type: str
        """
        
        self._upload_uri = upload_uri

    @property
    def import_mode(self):
        """
        Gets the import_mode of this DataTableImportJob.
        The indication of whether the processing should remove rows that don't appear in the import file

        :return: The import_mode of this DataTableImportJob.
        :rtype: str
        """
        return self._import_mode

    @import_mode.setter
    def import_mode(self, import_mode):
        """
        Sets the import_mode of this DataTableImportJob.
        The indication of whether the processing should remove rows that don't appear in the import file

        :param import_mode: The import_mode of this DataTableImportJob.
        :type: str
        """
        allowed_values = ["ReplaceAll", "Append"]
        if import_mode.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for import_mode -> " + import_mode
            self._import_mode = "outdated_sdk_version"
        else:
            self._import_mode = import_mode

    @property
    def error_information(self):
        """
        Gets the error_information of this DataTableImportJob.
        Any error information, or null of the processing is not in an error state

        :return: The error_information of this DataTableImportJob.
        :rtype: ErrorBody
        """
        return self._error_information

    @error_information.setter
    def error_information(self, error_information):
        """
        Sets the error_information of this DataTableImportJob.
        Any error information, or null of the processing is not in an error state

        :param error_information: The error_information of this DataTableImportJob.
        :type: ErrorBody
        """
        
        self._error_information = error_information

    @property
    def count_records_updated(self):
        """
        Gets the count_records_updated of this DataTableImportJob.
        The current count of the number of records processed

        :return: The count_records_updated of this DataTableImportJob.
        :rtype: int
        """
        return self._count_records_updated

    @count_records_updated.setter
    def count_records_updated(self, count_records_updated):
        """
        Sets the count_records_updated of this DataTableImportJob.
        The current count of the number of records processed

        :param count_records_updated: The count_records_updated of this DataTableImportJob.
        :type: int
        """
        
        self._count_records_updated = count_records_updated

    @property
    def count_records_deleted(self):
        """
        Gets the count_records_deleted of this DataTableImportJob.
        The current count of the number of records deleted

        :return: The count_records_deleted of this DataTableImportJob.
        :rtype: int
        """
        return self._count_records_deleted

    @count_records_deleted.setter
    def count_records_deleted(self, count_records_deleted):
        """
        Sets the count_records_deleted of this DataTableImportJob.
        The current count of the number of records deleted

        :param count_records_deleted: The count_records_deleted of this DataTableImportJob.
        :type: int
        """
        
        self._count_records_deleted = count_records_deleted

    @property
    def count_records_failed(self):
        """
        Gets the count_records_failed of this DataTableImportJob.
        The current count of the number of records that failed to import

        :return: The count_records_failed of this DataTableImportJob.
        :rtype: int
        """
        return self._count_records_failed

    @count_records_failed.setter
    def count_records_failed(self, count_records_failed):
        """
        Sets the count_records_failed of this DataTableImportJob.
        The current count of the number of records that failed to import

        :param count_records_failed: The count_records_failed of this DataTableImportJob.
        :type: int
        """
        
        self._count_records_failed = count_records_failed

    @property
    def self_uri(self):
        """
        Gets the self_uri of this DataTableImportJob.
        The URI for this object

        :return: The self_uri of this DataTableImportJob.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this DataTableImportJob.
        The URI for this object

        :param self_uri: The self_uri of this DataTableImportJob.
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

