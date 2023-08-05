# coding: utf-8

"""
ScriptsApi.py
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
"""

from __future__ import absolute_import

import sys
import os
import re

# python 2 and python 3 compatibility library
from six import iteritems

from ..configuration import Configuration
from ..api_client import ApiClient


class ScriptsApi(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient()
            self.api_client = config.api_client

    def get_script(self, script_id, **kwargs):
        """
        Get a script
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_script(script_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str script_id: Script ID (required)
        :return: Script
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['script_id']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_script" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'script_id' is set
        if ('script_id' not in params) or (params['script_id'] is None):
            raise ValueError("Missing the required parameter `script_id` when calling `get_script`")


        resource_path = '/api/v2/scripts/{scriptId}'.replace('{format}', 'json')
        path_params = {}
        if 'script_id' in params:
            path_params['scriptId'] = params['script_id']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='Script',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_script_page(self, script_id, page_id, **kwargs):
        """
        Get a page
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_script_page(script_id, page_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str script_id: Script ID (required)
        :param str page_id: Page ID (required)
        :param str script_data_version: Advanced usage - controls the data version of the script
        :return: Page
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['script_id', 'page_id', 'script_data_version']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_script_page" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'script_id' is set
        if ('script_id' not in params) or (params['script_id'] is None):
            raise ValueError("Missing the required parameter `script_id` when calling `get_script_page`")
        # verify the required parameter 'page_id' is set
        if ('page_id' not in params) or (params['page_id'] is None):
            raise ValueError("Missing the required parameter `page_id` when calling `get_script_page`")


        resource_path = '/api/v2/scripts/{scriptId}/pages/{pageId}'.replace('{format}', 'json')
        path_params = {}
        if 'script_id' in params:
            path_params['scriptId'] = params['script_id']
        if 'page_id' in params:
            path_params['pageId'] = params['page_id']

        query_params = {}
        if 'script_data_version' in params:
            query_params['scriptDataVersion'] = params['script_data_version']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='Page',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_script_pages(self, script_id, **kwargs):
        """
        Get the list of pages
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_script_pages(script_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str script_id: Script ID (required)
        :param str script_data_version: Advanced usage - controls the data version of the script
        :return: list[Page]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['script_id', 'script_data_version']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_script_pages" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'script_id' is set
        if ('script_id' not in params) or (params['script_id'] is None):
            raise ValueError("Missing the required parameter `script_id` when calling `get_script_pages`")


        resource_path = '/api/v2/scripts/{scriptId}/pages'.replace('{format}', 'json')
        path_params = {}
        if 'script_id' in params:
            path_params['scriptId'] = params['script_id']

        query_params = {}
        if 'script_data_version' in params:
            query_params['scriptDataVersion'] = params['script_data_version']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='list[Page]',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_scripts(self, **kwargs):
        """
        Get the list of scripts
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_scripts(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param int page_size: Page size
        :param int page_number: Page number
        :param str expand: Expand
        :param str name: Name filter
        :param str feature: Feature filter
        :param str flow_id: Secure flow id filter
        :param str sort_by: SortBy
        :param str sort_order: SortOrder
        :param str script_data_version: Advanced usage - controls the data version of the script
        :return: ScriptEntityListing
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['page_size', 'page_number', 'expand', 'name', 'feature', 'flow_id', 'sort_by', 'sort_order', 'script_data_version']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_scripts" % key
                )
            params[key] = val
        del params['kwargs']



        resource_path = '/api/v2/scripts'.replace('{format}', 'json')
        path_params = {}

        query_params = {}
        if 'page_size' in params:
            query_params['pageSize'] = params['page_size']
        if 'page_number' in params:
            query_params['pageNumber'] = params['page_number']
        if 'expand' in params:
            query_params['expand'] = params['expand']
        if 'name' in params:
            query_params['name'] = params['name']
        if 'feature' in params:
            query_params['feature'] = params['feature']
        if 'flow_id' in params:
            query_params['flowId'] = params['flow_id']
        if 'sort_by' in params:
            query_params['sortBy'] = params['sort_by']
        if 'sort_order' in params:
            query_params['sortOrder'] = params['sort_order']
        if 'script_data_version' in params:
            query_params['scriptDataVersion'] = params['script_data_version']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='ScriptEntityListing',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_scripts_published(self, **kwargs):
        """
        Get the published scripts.
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_scripts_published(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param int page_size: Page size
        :param int page_number: Page number
        :param str expand: Expand
        :param str name: Name filter
        :param str feature: Feature filter
        :param str flow_id: Secure flow id filter
        :param str script_data_version: Advanced usage - controls the data version of the script
        :return: ScriptEntityListing
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['page_size', 'page_number', 'expand', 'name', 'feature', 'flow_id', 'script_data_version']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_scripts_published" % key
                )
            params[key] = val
        del params['kwargs']



        resource_path = '/api/v2/scripts/published'.replace('{format}', 'json')
        path_params = {}

        query_params = {}
        if 'page_size' in params:
            query_params['pageSize'] = params['page_size']
        if 'page_number' in params:
            query_params['pageNumber'] = params['page_number']
        if 'expand' in params:
            query_params['expand'] = params['expand']
        if 'name' in params:
            query_params['name'] = params['name']
        if 'feature' in params:
            query_params['feature'] = params['feature']
        if 'flow_id' in params:
            query_params['flowId'] = params['flow_id']
        if 'script_data_version' in params:
            query_params['scriptDataVersion'] = params['script_data_version']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='ScriptEntityListing',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_scripts_published_script_id(self, script_id, **kwargs):
        """
        Get the published script.
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_scripts_published_script_id(script_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str script_id: Script ID (required)
        :param str script_data_version: Advanced usage - controls the data version of the script
        :return: Script
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['script_id', 'script_data_version']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_scripts_published_script_id" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'script_id' is set
        if ('script_id' not in params) or (params['script_id'] is None):
            raise ValueError("Missing the required parameter `script_id` when calling `get_scripts_published_script_id`")


        resource_path = '/api/v2/scripts/published/{scriptId}'.replace('{format}', 'json')
        path_params = {}
        if 'script_id' in params:
            path_params['scriptId'] = params['script_id']

        query_params = {}
        if 'script_data_version' in params:
            query_params['scriptDataVersion'] = params['script_data_version']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='Script',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_scripts_published_script_id_page(self, script_id, page_id, **kwargs):
        """
        Get the published page.
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_scripts_published_script_id_page(script_id, page_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str script_id: Script ID (required)
        :param str page_id: Page ID (required)
        :param str script_data_version: Advanced usage - controls the data version of the script
        :return: Page
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['script_id', 'page_id', 'script_data_version']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_scripts_published_script_id_page" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'script_id' is set
        if ('script_id' not in params) or (params['script_id'] is None):
            raise ValueError("Missing the required parameter `script_id` when calling `get_scripts_published_script_id_page`")
        # verify the required parameter 'page_id' is set
        if ('page_id' not in params) or (params['page_id'] is None):
            raise ValueError("Missing the required parameter `page_id` when calling `get_scripts_published_script_id_page`")


        resource_path = '/api/v2/scripts/published/{scriptId}/pages/{pageId}'.replace('{format}', 'json')
        path_params = {}
        if 'script_id' in params:
            path_params['scriptId'] = params['script_id']
        if 'page_id' in params:
            path_params['pageId'] = params['page_id']

        query_params = {}
        if 'script_data_version' in params:
            query_params['scriptDataVersion'] = params['script_data_version']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='Page',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_scripts_published_script_id_pages(self, script_id, **kwargs):
        """
        Get the list of published pages
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_scripts_published_script_id_pages(script_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str script_id: Script ID (required)
        :param str script_data_version: Advanced usage - controls the data version of the script
        :return: list[Page]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['script_id', 'script_data_version']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_scripts_published_script_id_pages" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'script_id' is set
        if ('script_id' not in params) or (params['script_id'] is None):
            raise ValueError("Missing the required parameter `script_id` when calling `get_scripts_published_script_id_pages`")


        resource_path = '/api/v2/scripts/published/{scriptId}/pages'.replace('{format}', 'json')
        path_params = {}
        if 'script_id' in params:
            path_params['scriptId'] = params['script_id']

        query_params = {}
        if 'script_data_version' in params:
            query_params['scriptDataVersion'] = params['script_data_version']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='list[Page]',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_scripts_published_script_id_variables(self, script_id, **kwargs):
        """
        Get the published variables
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_scripts_published_script_id_variables(script_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str script_id: Script ID (required)
        :param str input: input
        :param str output: output
        :param str type: type
        :param str script_data_version: Advanced usage - controls the data version of the script
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['script_id', 'input', 'output', 'type', 'script_data_version']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_scripts_published_script_id_variables" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'script_id' is set
        if ('script_id' not in params) or (params['script_id'] is None):
            raise ValueError("Missing the required parameter `script_id` when calling `get_scripts_published_script_id_variables`")


        resource_path = '/api/v2/scripts/published/{scriptId}/variables'.replace('{format}', 'json')
        path_params = {}
        if 'script_id' in params:
            path_params['scriptId'] = params['script_id']

        query_params = {}
        if 'input' in params:
            query_params['input'] = params['input']
        if 'output' in params:
            query_params['output'] = params['output']
        if 'type' in params:
            query_params['type'] = params['type']
        if 'script_data_version' in params:
            query_params['scriptDataVersion'] = params['script_data_version']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='object',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_scripts_upload_status(self, upload_id, **kwargs):
        """
        Get the upload status of an imported script
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_scripts_upload_status(upload_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str upload_id: Upload ID (required)
        :param bool long_poll: Enable longPolling endpoint
        :return: ImportScriptStatusResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['upload_id', 'long_poll']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_scripts_upload_status" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'upload_id' is set
        if ('upload_id' not in params) or (params['upload_id'] is None):
            raise ValueError("Missing the required parameter `upload_id` when calling `get_scripts_upload_status`")


        resource_path = '/api/v2/scripts/uploads/{uploadId}/status'.replace('{format}', 'json')
        path_params = {}
        if 'upload_id' in params:
            path_params['uploadId'] = params['upload_id']

        query_params = {}
        if 'long_poll' in params:
            query_params['longPoll'] = params['long_poll']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='ImportScriptStatusResponse',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def post_script_export(self, script_id, **kwargs):
        """
        Export a script via download service.
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.post_script_export(script_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str script_id: Script ID (required)
        :param ExportScriptRequest body: 
        :return: ExportScriptResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['script_id', 'body']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_script_export" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'script_id' is set
        if ('script_id' not in params) or (params['script_id'] is None):
            raise ValueError("Missing the required parameter `script_id` when calling `post_script_export`")


        resource_path = '/api/v2/scripts/{scriptId}/export'.replace('{format}', 'json')
        path_params = {}
        if 'script_id' in params:
            path_params['scriptId'] = params['script_id']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'POST',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='ExportScriptResponse',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response
