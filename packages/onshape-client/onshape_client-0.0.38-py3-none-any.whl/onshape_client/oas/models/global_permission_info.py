# coding: utf-8

"""
    Onshape REST API

    The Onshape REST API consumed by all clients.  # noqa: E501

    The version of the OpenAPI document: 1.111
    Contact: api-support@onshape.zendesk.com
    Generated by: https://openapi-generator.tech
"""

from __future__ import absolute_import

import six  # noqa: F401
from onshape_client.oas.model_utils import ModelNormal  # noqa: F401


class GlobalPermissionInfo(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {}

    validations = {}

    additional_properties_type = None

    @staticmethod
    def openapi_types():
        """
        This must be a class method so a model may have properties that are
        of type self, this ensures that we don't create a cyclic import

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        return {
            "access_reports": (bool,),  # noqa: E501
            "admin_enterprise": (bool,),  # noqa: E501
            "allow_app_store_access": (bool,),  # noqa: E501
            "approve_releases": (bool,),  # noqa: E501
            "create_project": (bool,),  # noqa: E501
            "create_releases": (bool,),  # noqa: E501
            "delete_permanently": (bool,),  # noqa: E501
            "manage_guest_users": (bool,),  # noqa: E501
            "manage_rbac": (bool,),  # noqa: E501
            "manage_users": (bool,),  # noqa: E501
            "share_for_anonymous_access": (bool,),  # noqa: E501
        }

    @staticmethod
    def discriminator():
        return None

    attribute_map = {
        "access_reports": "accessReports",  # noqa: E501
        "admin_enterprise": "adminEnterprise",  # noqa: E501
        "allow_app_store_access": "allowAppStoreAccess",  # noqa: E501
        "approve_releases": "approveReleases",  # noqa: E501
        "create_project": "createProject",  # noqa: E501
        "create_releases": "createReleases",  # noqa: E501
        "delete_permanently": "deletePermanently",  # noqa: E501
        "manage_guest_users": "manageGuestUsers",  # noqa: E501
        "manage_rbac": "manageRbac",  # noqa: E501
        "manage_users": "manageUsers",  # noqa: E501
        "share_for_anonymous_access": "shareForAnonymousAccess",  # noqa: E501
    }

    @staticmethod
    def _composed_schemas():
        return None

    required_properties = set(
        [
            "_data_store",
            "_check_type",
            "_from_server",
            "_path_to_item",
            "_configuration",
        ]
    )

    def __init__(
        self,
        _check_type=True,
        _from_server=False,
        _path_to_item=(),
        _configuration=None,
        **kwargs
    ):  # noqa: E501
        """global_permission_info.GlobalPermissionInfo - a model defined in OpenAPI


        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _from_server (bool): True if the data is from the server
                                False if the data is from the client (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            access_reports (bool): [optional]  # noqa: E501
            admin_enterprise (bool): [optional]  # noqa: E501
            allow_app_store_access (bool): [optional]  # noqa: E501
            approve_releases (bool): [optional]  # noqa: E501
            create_project (bool): [optional]  # noqa: E501
            create_releases (bool): [optional]  # noqa: E501
            delete_permanently (bool): [optional]  # noqa: E501
            manage_guest_users (bool): [optional]  # noqa: E501
            manage_rbac (bool): [optional]  # noqa: E501
            manage_users (bool): [optional]  # noqa: E501
            share_for_anonymous_access (bool): [optional]  # noqa: E501
        """

        self._data_store = {}
        self._check_type = _check_type
        self._from_server = _from_server
        self._path_to_item = _path_to_item
        self._configuration = _configuration

        for var_name, var_value in six.iteritems(kwargs):
            setattr(self, var_name, var_value)
