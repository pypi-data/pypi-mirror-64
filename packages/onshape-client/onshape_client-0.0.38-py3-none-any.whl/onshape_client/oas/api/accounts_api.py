# coding: utf-8

"""
    Onshape REST API

    The Onshape REST API consumed by all clients.  # noqa: E501

    The version of the OpenAPI document: 1.111
    Contact: api-support@onshape.zendesk.com
    Generated by: https://openapi-generator.tech
"""

from __future__ import absolute_import

# python 2 and python 3 compatibility library
import six
from onshape_client.oas.api_client import ApiClient
from onshape_client.oas.exceptions import ApiTypeError, ApiValueError
from onshape_client.oas.model_utils import (  # noqa: F401
    check_allowed_values,
    check_validations,
    file_type,
    int,
    none_type,
    str,
    validate_and_convert_types,
)
from onshape_client.oas.models import bt_list_response_bt_purchase_info
from onshape_client.oas.models import bt_purchase_info
from onshape_client.oas.models import bt_purchase_user_params


class AccountsApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

        def __cancel_purchase_new(self, aid, pid, **kwargs):
            """Cancel Recurring Subscription  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True
            >>> thread = api.cancel_purchase_new(aid, pid, async_req=True)
            >>> result = thread.get()

            Args:
                aid (str):
                pid (str):

            Keyword Args:
                cancel_immediately (bool): [optional] if omitted the server will use the default value of False
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int): specifies the index of the server
                    that we want to use.
                    Default is 0.
                async_req (bool): execute request asynchronously

            Returns:
                None
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs["async_req"] = kwargs.get("async_req", False)
            kwargs["_return_http_data_only"] = kwargs.get(
                "_return_http_data_only", True
            )
            kwargs["_preload_content"] = kwargs.get("_preload_content", True)
            kwargs["_request_timeout"] = kwargs.get("_request_timeout", None)
            kwargs["_check_input_type"] = kwargs.get("_check_input_type", True)
            kwargs["_check_return_type"] = kwargs.get("_check_return_type", True)
            kwargs["_host_index"] = kwargs.get("_host_index", 0)
            kwargs["aid"] = aid
            kwargs["pid"] = pid
            return self.call_with_http_info(**kwargs)

        self.cancel_purchase_new = Endpoint(
            settings={
                "response_type": None,
                "auth": ["OAuth2"],
                "endpoint_path": "/api/accounts/{aid}/purchases/{pid}",
                "operation_id": "cancel_purchase_new",
                "http_method": "DELETE",
                "servers": [],
            },
            params_map={
                "all": ["aid", "pid", "cancel_immediately",],
                "required": ["aid", "pid",],
                "nullable": [],
                "enum": [],
                "validation": [],
            },
            root_map={
                "validations": {},
                "allowed_values": {},
                "openapi_types": {
                    "aid": (str,),
                    "pid": (str,),
                    "cancel_immediately": (bool,),
                },
                "attribute_map": {
                    "aid": "aid",
                    "pid": "pid",
                    "cancel_immediately": "cancelImmediately",
                },
                "location_map": {
                    "aid": "path",
                    "pid": "path",
                    "cancel_immediately": "query",
                },
                "collection_format_map": {},
            },
            headers_map={
                "accept": [
                    "application/vnd.onshape.v1+json;charset=UTF-8;qs=0.1",
                    "application/json;charset=UTF-8; qs=0.09",
                ],
                "content_type": [],
            },
            api_client=api_client,
            callable=__cancel_purchase_new,
        )

        def __consume_purchase(self, pid, **kwargs):
            """Mark Purchase Consumed For User  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True
            >>> thread = api.consume_purchase(pid, async_req=True)
            >>> result = thread.get()

            Args:
                pid (str):

            Keyword Args:
                bt_purchase_user_params (bt_purchase_user_params.BTPurchaseUserParams): [optional]
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int): specifies the index of the server
                    that we want to use.
                    Default is 0.
                async_req (bool): execute request asynchronously

            Returns:
                bt_purchase_info.BTPurchaseInfo
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs["async_req"] = kwargs.get("async_req", False)
            kwargs["_return_http_data_only"] = kwargs.get(
                "_return_http_data_only", True
            )
            kwargs["_preload_content"] = kwargs.get("_preload_content", True)
            kwargs["_request_timeout"] = kwargs.get("_request_timeout", None)
            kwargs["_check_input_type"] = kwargs.get("_check_input_type", True)
            kwargs["_check_return_type"] = kwargs.get("_check_return_type", True)
            kwargs["_host_index"] = kwargs.get("_host_index", 0)
            kwargs["pid"] = pid
            return self.call_with_http_info(**kwargs)

        self.consume_purchase = Endpoint(
            settings={
                "response_type": (bt_purchase_info.BTPurchaseInfo,),
                "auth": ["OAuth2"],
                "endpoint_path": "/api/accounts/purchases/{pid}/consume",
                "operation_id": "consume_purchase",
                "http_method": "POST",
                "servers": [],
            },
            params_map={
                "all": ["pid", "bt_purchase_user_params",],
                "required": ["pid",],
                "nullable": [],
                "enum": [],
                "validation": [],
            },
            root_map={
                "validations": {},
                "allowed_values": {},
                "openapi_types": {
                    "pid": (str,),
                    "bt_purchase_user_params": (
                        bt_purchase_user_params.BTPurchaseUserParams,
                    ),
                },
                "attribute_map": {"pid": "pid",},
                "location_map": {"pid": "path", "bt_purchase_user_params": "body",},
                "collection_format_map": {},
            },
            headers_map={
                "accept": [
                    "application/vnd.onshape.v1+json;charset=UTF-8;qs=0.1",
                    "application/json;charset=UTF-8; qs=0.09",
                ],
                "content_type": ["application/json;charset=UTF-8; qs=0.09"],
            },
            api_client=api_client,
            callable=__consume_purchase,
        )

        def __get_plan_purchases(self, plan_id, **kwargs):
            """Get Plan Purchases  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True
            >>> thread = api.get_plan_purchases(plan_id, async_req=True)
            >>> result = thread.get()

            Args:
                plan_id (str):

            Keyword Args:
                offset (int): [optional] if omitted the server will use the default value of 0
                limit (int): [optional] if omitted the server will use the default value of 20
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int): specifies the index of the server
                    that we want to use.
                    Default is 0.
                async_req (bool): execute request asynchronously

            Returns:
                bt_list_response_bt_purchase_info.BTListResponseBTPurchaseInfo
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs["async_req"] = kwargs.get("async_req", False)
            kwargs["_return_http_data_only"] = kwargs.get(
                "_return_http_data_only", True
            )
            kwargs["_preload_content"] = kwargs.get("_preload_content", True)
            kwargs["_request_timeout"] = kwargs.get("_request_timeout", None)
            kwargs["_check_input_type"] = kwargs.get("_check_input_type", True)
            kwargs["_check_return_type"] = kwargs.get("_check_return_type", True)
            kwargs["_host_index"] = kwargs.get("_host_index", 0)
            kwargs["plan_id"] = plan_id
            return self.call_with_http_info(**kwargs)

        self.get_plan_purchases = Endpoint(
            settings={
                "response_type": (
                    bt_list_response_bt_purchase_info.BTListResponseBTPurchaseInfo,
                ),
                "auth": [],
                "endpoint_path": "/api/accounts/plans/{planId}/purchases",
                "operation_id": "get_plan_purchases",
                "http_method": "GET",
                "servers": [],
            },
            params_map={
                "all": ["plan_id", "offset", "limit",],
                "required": ["plan_id",],
                "nullable": [],
                "enum": [],
                "validation": [],
            },
            root_map={
                "validations": {},
                "allowed_values": {},
                "openapi_types": {
                    "plan_id": (str,),
                    "offset": (int,),
                    "limit": (int,),
                },
                "attribute_map": {
                    "plan_id": "planId",
                    "offset": "offset",
                    "limit": "limit",
                },
                "location_map": {
                    "plan_id": "path",
                    "offset": "query",
                    "limit": "query",
                },
                "collection_format_map": {},
            },
            headers_map={
                "accept": [
                    "application/vnd.onshape.v1+json;charset=UTF-8;qs=0.1",
                    "application/json;charset=UTF-8; qs=0.09",
                ],
                "content_type": [],
            },
            api_client=api_client,
            callable=__get_plan_purchases,
        )

        def __get_purchases(self, **kwargs):
            """Get User's Appstore Purchases.  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True
            >>> thread = api.get_purchases(async_req=True)
            >>> result = thread.get()


            Keyword Args:
                all (bool): [optional] if omitted the server will use the default value of False
                own_purchase_only (bool): [optional] if omitted the server will use the default value of False
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int): specifies the index of the server
                    that we want to use.
                    Default is 0.
                async_req (bool): execute request asynchronously

            Returns:
                [bt_purchase_info.BTPurchaseInfo]
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs["async_req"] = kwargs.get("async_req", False)
            kwargs["_return_http_data_only"] = kwargs.get(
                "_return_http_data_only", True
            )
            kwargs["_preload_content"] = kwargs.get("_preload_content", True)
            kwargs["_request_timeout"] = kwargs.get("_request_timeout", None)
            kwargs["_check_input_type"] = kwargs.get("_check_input_type", True)
            kwargs["_check_return_type"] = kwargs.get("_check_return_type", True)
            kwargs["_host_index"] = kwargs.get("_host_index", 0)
            return self.call_with_http_info(**kwargs)

        self.get_purchases = Endpoint(
            settings={
                "response_type": ([bt_purchase_info.BTPurchaseInfo],),
                "auth": [],
                "endpoint_path": "/api/accounts/purchases",
                "operation_id": "get_purchases",
                "http_method": "GET",
                "servers": [],
            },
            params_map={
                "all": ["all", "own_purchase_only",],
                "required": [],
                "nullable": [],
                "enum": [],
                "validation": [],
            },
            root_map={
                "validations": {},
                "allowed_values": {},
                "openapi_types": {"all": (bool,), "own_purchase_only": (bool,),},
                "attribute_map": {
                    "all": "all",
                    "own_purchase_only": "ownPurchaseOnly",
                },
                "location_map": {"all": "query", "own_purchase_only": "query",},
                "collection_format_map": {},
            },
            headers_map={
                "accept": [
                    "application/vnd.onshape.v1+json;charset=UTF-8;qs=0.1",
                    "application/json;charset=UTF-8; qs=0.09",
                ],
                "content_type": [],
            },
            api_client=api_client,
            callable=__get_purchases,
        )


class Endpoint(object):
    def __init__(
        self,
        settings=None,
        params_map=None,
        root_map=None,
        headers_map=None,
        api_client=None,
        callable=None,
    ):
        """Creates an endpoint

        Args:
            settings (dict): see below key value pairs
                'response_type' (tuple/None): response type
                'auth' (list): a list of auth type keys
                'endpoint_path' (str): the endpoint path
                'operation_id' (str): endpoint string identifier
                'http_method' (str): POST/PUT/PATCH/GET etc
                'servers' (list): list of str servers that this endpoint is at
            params_map (dict): see below key value pairs
                'all' (list): list of str endpoint parameter names
                'required' (list): list of required parameter names
                'nullable' (list): list of nullable parameter names
                'enum' (list): list of parameters with enum values
                'validation' (list): list of parameters with validations
            root_map
                'validations' (dict): the dict mapping endpoint parameter tuple
                    paths to their validation dictionaries
                'allowed_values' (dict): the dict mapping endpoint parameter
                    tuple paths to their allowed_values (enum) dictionaries
                'openapi_types' (dict): param_name to openapi type
                'attribute_map' (dict): param_name to camelCase name
                'location_map' (dict): param_name to  'body', 'file', 'form',
                    'header', 'path', 'query'
                collection_format_map (dict): param_name to `csv` etc.
            headers_map (dict): see below key value pairs
                'accept' (list): list of Accept header strings
                'content_type' (list): list of Content-Type header strings
            api_client (ApiClient) api client instance
            callable (function): the function which is invoked when the
                Endpoint is called
        """
        self.settings = settings
        self.params_map = params_map
        self.params_map["all"].extend(
            [
                "async_req",
                "_host_index",
                "_preload_content",
                "_request_timeout",
                "_return_http_data_only",
                "_check_input_type",
                "_check_return_type",
            ]
        )
        self.params_map["nullable"].extend(["_request_timeout"])
        self.validations = root_map["validations"]
        self.allowed_values = root_map["allowed_values"]
        self.openapi_types = root_map["openapi_types"]
        extra_types = {
            "async_req": (bool,),
            "_host_index": (int,),
            "_preload_content": (bool,),
            "_request_timeout": (none_type, int, (int,), [int]),
            "_return_http_data_only": (bool,),
            "_check_input_type": (bool,),
            "_check_return_type": (bool,),
        }
        self.openapi_types.update(extra_types)
        self.attribute_map = root_map["attribute_map"]
        self.location_map = root_map["location_map"]
        self.collection_format_map = root_map["collection_format_map"]
        self.headers_map = headers_map
        self.api_client = api_client
        self.callable = callable

    def __validate_inputs(self, kwargs):
        for param in self.params_map["enum"]:
            if param in kwargs:
                check_allowed_values(self.allowed_values, (param,), kwargs[param])

        for param in self.params_map["validation"]:
            if param in kwargs:
                check_validations(self.validations, (param,), kwargs[param])

        if kwargs["_check_input_type"] is False:
            return

        for key, value in six.iteritems(kwargs):
            fixed_val = validate_and_convert_types(
                value,
                self.openapi_types[key],
                [key],
                False,
                kwargs["_check_input_type"],
                configuration=self.api_client.configuration,
            )
            kwargs[key] = fixed_val

    def __gather_params(self, kwargs):
        params = {
            "body": None,
            "collection_format": {},
            "file": {},
            "form": [],
            "header": {},
            "path": {},
            "query": [],
        }

        for param_name, param_value in six.iteritems(kwargs):
            param_location = self.location_map.get(param_name)
            if param_location is None:
                continue
            if param_location:
                if param_location == "body":
                    params["body"] = param_value
                    continue
                base_name = self.attribute_map[param_name]
                if param_location == "form" and self.openapi_types[param_name] == (
                    file_type,
                ):
                    params["file"][param_name] = [param_value]
                elif param_location == "form" and self.openapi_types[param_name] == (
                    [file_type],
                ):
                    # param_value is already a list
                    params["file"][param_name] = param_value
                elif param_location in {"form", "query"}:
                    param_value_full = (base_name, param_value)
                    params[param_location].append(param_value_full)
                if param_location not in {"form", "query"}:
                    params[param_location][base_name] = param_value
                collection_format = self.collection_format_map.get(param_name)
                if collection_format:
                    params["collection_format"][base_name] = collection_format

        return params

    def __call__(self, *args, **kwargs):
        """ This method is invoked when endpoints are called
        Example:
        pet_api = PetApi()
        pet_api.add_pet  # this is an instance of the class Endpoint
        pet_api.add_pet()  # this invokes pet_api.add_pet.__call__()
        which then invokes the callable functions stored in that endpoint at
        pet_api.add_pet.callable or self.callable in this class
        """
        return self.callable(self, *args, **kwargs)

    def call_with_http_info(self, **kwargs):

        try:
            _host = self.settings["servers"][kwargs["_host_index"]]
        except IndexError:
            if self.settings["servers"]:
                raise ApiValueError(
                    "Invalid host index. Must be 0 <= index < %s"
                    % len(self.settings["servers"])
                )
            _host = None

        for key, value in six.iteritems(kwargs):
            if key not in self.params_map["all"]:
                raise ApiTypeError(
                    "Got an unexpected parameter '%s'"
                    " to method `%s`" % (key, self.settings["operation_id"])
                )
            # only throw this nullable ApiValueError if _check_input_type
            # is False, if _check_input_type==True we catch this case
            # in self.__validate_inputs
            if (
                key not in self.params_map["nullable"]
                and value is None
                and kwargs["_check_input_type"] is False
            ):
                raise ApiValueError(
                    "Value may not be None for non-nullable parameter `%s`"
                    " when calling `%s`" % (key, self.settings["operation_id"])
                )

        for key in self.params_map["required"]:
            if key not in kwargs.keys():
                raise ApiValueError(
                    "Missing the required parameter `%s` when calling "
                    "`%s`" % (key, self.settings["operation_id"])
                )

        self.__validate_inputs(kwargs)

        params = self.__gather_params(kwargs)

        accept_headers_list = self.headers_map["accept"]
        if accept_headers_list:
            params["header"]["Accept"] = self.api_client.select_header_accept(
                accept_headers_list
            )

        content_type_headers_list = self.headers_map["content_type"]
        if content_type_headers_list:
            header_list = self.api_client.select_header_content_type(
                content_type_headers_list
            )
            params["header"]["Content-Type"] = header_list

        return self.api_client.call_api(
            self.settings["endpoint_path"],
            self.settings["http_method"],
            params["path"],
            params["query"],
            params["header"],
            body=params["body"],
            post_params=params["form"],
            files=params["file"],
            response_type=self.settings["response_type"],
            auth_settings=self.settings["auth"],
            async_req=kwargs["async_req"],
            _check_type=kwargs["_check_return_type"],
            _return_http_data_only=kwargs["_return_http_data_only"],
            _preload_content=kwargs["_preload_content"],
            _request_timeout=kwargs["_request_timeout"],
            _host=_host,
            collection_formats=params["collection_format"],
        )
