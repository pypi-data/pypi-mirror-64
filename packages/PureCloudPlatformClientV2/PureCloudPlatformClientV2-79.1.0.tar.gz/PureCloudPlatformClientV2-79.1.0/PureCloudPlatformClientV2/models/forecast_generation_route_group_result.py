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

class ForecastGenerationRouteGroupResult(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ForecastGenerationRouteGroupResult - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'route_group': 'RouteGroupAttributes',
            'metric_results': 'list[ForecastTimeSeriesResult]'
        }

        self.attribute_map = {
            'route_group': 'routeGroup',
            'metric_results': 'metricResults'
        }

        self._route_group = None
        self._metric_results = None

    @property
    def route_group(self):
        """
        Gets the route_group of this ForecastGenerationRouteGroupResult.
        The route group this result represents

        :return: The route_group of this ForecastGenerationRouteGroupResult.
        :rtype: RouteGroupAttributes
        """
        return self._route_group

    @route_group.setter
    def route_group(self, route_group):
        """
        Sets the route_group of this ForecastGenerationRouteGroupResult.
        The route group this result represents

        :param route_group: The route_group of this ForecastGenerationRouteGroupResult.
        :type: RouteGroupAttributes
        """
        
        self._route_group = route_group

    @property
    def metric_results(self):
        """
        Gets the metric_results of this ForecastGenerationRouteGroupResult.
        The generation results for the associated route group

        :return: The metric_results of this ForecastGenerationRouteGroupResult.
        :rtype: list[ForecastTimeSeriesResult]
        """
        return self._metric_results

    @metric_results.setter
    def metric_results(self, metric_results):
        """
        Sets the metric_results of this ForecastGenerationRouteGroupResult.
        The generation results for the associated route group

        :param metric_results: The metric_results of this ForecastGenerationRouteGroupResult.
        :type: list[ForecastTimeSeriesResult]
        """
        
        self._metric_results = metric_results

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

