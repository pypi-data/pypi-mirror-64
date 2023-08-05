# coding: utf-8

"""
    Onshape REST API

    The Onshape REST API consumed by all clients.  # noqa: E501

    The version of the OpenAPI document: 1.111
    Contact: api-support@onshape.zendesk.com
    Generated by: https://openapi-generator.tech
"""

from __future__ import absolute_import

import sys  # noqa: F401

import six  # noqa: F401
from onshape_client.oas.model_utils import (  # noqa: F401
    ModelNormal,
    date,
    datetime,
    int,
    str,
)

try:
    from onshape_client.oas.models import bt_owner_info
except ImportError:
    bt_owner_info = sys.modules["onshape_client.oas.models.bt_owner_info"]
try:
    from onshape_client.oas.models import bt_rbac_permission_scheme_info
except ImportError:
    bt_rbac_permission_scheme_info = sys.modules[
        "onshape_client.oas.models.bt_rbac_permission_scheme_info"
    ]
try:
    from onshape_client.oas.models import bt_user_basic_summary_info
except ImportError:
    bt_user_basic_summary_info = sys.modules[
        "onshape_client.oas.models.bt_user_basic_summary_info"
    ]
try:
    from onshape_client.oas.models import role_map_entry
except ImportError:
    role_map_entry = sys.modules["onshape_client.oas.models.role_map_entry"]


class BTProjectInfo(ModelNormal):
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
            "can_move": (bool,),  # noqa: E501
            "created_at": (datetime,),  # noqa: E501
            "created_by": (
                bt_user_basic_summary_info.BTUserBasicSummaryInfo,
            ),  # noqa: E501
            "description": (str,),  # noqa: E501
            "href": (str,),  # noqa: E501
            "id": (str,),  # noqa: E501
            "is_container": (bool,),  # noqa: E501
            "is_enterprise_owned": (bool,),  # noqa: E501
            "is_mutable": (bool,),  # noqa: E501
            "modified_at": (datetime,),  # noqa: E501
            "modified_by": (
                bt_user_basic_summary_info.BTUserBasicSummaryInfo,
            ),  # noqa: E501
            "name": (str,),  # noqa: E501
            "owner": (bt_owner_info.BTOwnerInfo,),  # noqa: E501
            "permission_scheme": (
                bt_rbac_permission_scheme_info.BTRbacPermissionSchemeInfo,
            ),  # noqa: E501
            "permission_set": (
                bool,
                date,
                datetime,
                dict,
                float,
                int,
                list,
                str,
            ),  # noqa: E501
            "project_id": (str,),  # noqa: E501
            "resource_type": (str,),  # noqa: E501
            "role_map_entries": ([role_map_entry.RoleMapEntry],),  # noqa: E501
            "trash": (bool,),  # noqa: E501
            "tree_href": (str,),  # noqa: E501
            "view_ref": (str,),  # noqa: E501
        }

    @staticmethod
    def discriminator():
        return None

    attribute_map = {
        "can_move": "canMove",  # noqa: E501
        "created_at": "createdAt",  # noqa: E501
        "created_by": "createdBy",  # noqa: E501
        "description": "description",  # noqa: E501
        "href": "href",  # noqa: E501
        "id": "id",  # noqa: E501
        "is_container": "isContainer",  # noqa: E501
        "is_enterprise_owned": "isEnterpriseOwned",  # noqa: E501
        "is_mutable": "isMutable",  # noqa: E501
        "modified_at": "modifiedAt",  # noqa: E501
        "modified_by": "modifiedBy",  # noqa: E501
        "name": "name",  # noqa: E501
        "owner": "owner",  # noqa: E501
        "permission_scheme": "permissionScheme",  # noqa: E501
        "permission_set": "permissionSet",  # noqa: E501
        "project_id": "projectId",  # noqa: E501
        "resource_type": "resourceType",  # noqa: E501
        "role_map_entries": "roleMapEntries",  # noqa: E501
        "trash": "trash",  # noqa: E501
        "tree_href": "treeHref",  # noqa: E501
        "view_ref": "viewRef",  # noqa: E501
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
        """bt_project_info.BTProjectInfo - a model defined in OpenAPI


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
            can_move (bool): [optional]  # noqa: E501
            created_at (datetime): [optional]  # noqa: E501
            created_by (bt_user_basic_summary_info.BTUserBasicSummaryInfo): [optional]  # noqa: E501
            description (str): [optional]  # noqa: E501
            href (str): [optional]  # noqa: E501
            id (str): [optional]  # noqa: E501
            is_container (bool): [optional]  # noqa: E501
            is_enterprise_owned (bool): [optional]  # noqa: E501
            is_mutable (bool): [optional]  # noqa: E501
            modified_at (datetime): [optional]  # noqa: E501
            modified_by (bt_user_basic_summary_info.BTUserBasicSummaryInfo): [optional]  # noqa: E501
            name (str): [optional]  # noqa: E501
            owner (bt_owner_info.BTOwnerInfo): [optional]  # noqa: E501
            permission_scheme (bt_rbac_permission_scheme_info.BTRbacPermissionSchemeInfo): [optional]  # noqa: E501
            permission_set (bool, date, datetime, dict, float, int, list, str): [optional]  # noqa: E501
            project_id (str): [optional]  # noqa: E501
            resource_type (str): [optional]  # noqa: E501
            role_map_entries ([role_map_entry.RoleMapEntry]): [optional]  # noqa: E501
            trash (bool): [optional]  # noqa: E501
            tree_href (str): [optional]  # noqa: E501
            view_ref (str): [optional]  # noqa: E501
        """

        self._data_store = {}
        self._check_type = _check_type
        self._from_server = _from_server
        self._path_to_item = _path_to_item
        self._configuration = _configuration

        for var_name, var_value in six.iteritems(kwargs):
            setattr(self, var_name, var_value)
