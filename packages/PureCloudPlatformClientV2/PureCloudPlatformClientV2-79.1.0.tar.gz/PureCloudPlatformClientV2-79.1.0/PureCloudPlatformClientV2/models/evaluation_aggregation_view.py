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

class EvaluationAggregationView(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        EvaluationAggregationView - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'target': 'str',
            'name': 'str',
            'function': 'str',
            'range': 'AggregationRange'
        }

        self.attribute_map = {
            'target': 'target',
            'name': 'name',
            'function': 'function',
            'range': 'range'
        }

        self._target = None
        self._name = None
        self._function = None
        self._range = None

    @property
    def target(self):
        """
        Gets the target of this EvaluationAggregationView.
        Target metric name

        :return: The target of this EvaluationAggregationView.
        :rtype: str
        """
        return self._target

    @target.setter
    def target(self, target):
        """
        Sets the target of this EvaluationAggregationView.
        Target metric name

        :param target: The target of this EvaluationAggregationView.
        :type: str
        """
        allowed_values = ["nEvaluations", "nEvaluationsDeleted", "nEvaluationsRescored", "oTotalCriticalScore", "oTotalScore"]
        if target.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for target -> " + target
            self._target = "outdated_sdk_version"
        else:
            self._target = target

    @property
    def name(self):
        """
        Gets the name of this EvaluationAggregationView.
        A unique name for this view. Must be distinct from other views and built-in metric names.

        :return: The name of this EvaluationAggregationView.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this EvaluationAggregationView.
        A unique name for this view. Must be distinct from other views and built-in metric names.

        :param name: The name of this EvaluationAggregationView.
        :type: str
        """
        
        self._name = name

    @property
    def function(self):
        """
        Gets the function of this EvaluationAggregationView.
        Type of view you wish to create

        :return: The function of this EvaluationAggregationView.
        :rtype: str
        """
        return self._function

    @function.setter
    def function(self, function):
        """
        Sets the function of this EvaluationAggregationView.
        Type of view you wish to create

        :param function: The function of this EvaluationAggregationView.
        :type: str
        """
        allowed_values = ["rangeBound"]
        if function.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for function -> " + function
            self._function = "outdated_sdk_version"
        else:
            self._function = function

    @property
    def range(self):
        """
        Gets the range of this EvaluationAggregationView.
        Range of numbers for slicing up data

        :return: The range of this EvaluationAggregationView.
        :rtype: AggregationRange
        """
        return self._range

    @range.setter
    def range(self, range):
        """
        Sets the range of this EvaluationAggregationView.
        Range of numbers for slicing up data

        :param range: The range of this EvaluationAggregationView.
        :type: AggregationRange
        """
        
        self._range = range

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

