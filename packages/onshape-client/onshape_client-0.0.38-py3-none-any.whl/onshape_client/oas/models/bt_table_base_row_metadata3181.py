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
    str,
)

try:
    from onshape_client.oas.models import bt_base_sm_joint_table_row_metadata2232
except ImportError:
    bt_base_sm_joint_table_row_metadata2232 = sys.modules[
        "onshape_client.oas.models.bt_base_sm_joint_table_row_metadata2232"
    ]
try:
    from onshape_client.oas.models import bt_bill_of_materials_table_row_metadata1300
except ImportError:
    bt_bill_of_materials_table_row_metadata1300 = sys.modules[
        "onshape_client.oas.models.bt_bill_of_materials_table_row_metadata1300"
    ]
try:
    from onshape_client.oas.models import bt_table_base_cross_highlight_data2609
except ImportError:
    bt_table_base_cross_highlight_data2609 = sys.modules[
        "onshape_client.oas.models.bt_table_base_cross_highlight_data2609"
    ]
try:
    from onshape_client.oas.models import btfs_table_row_metadata2262
except ImportError:
    btfs_table_row_metadata2262 = sys.modules[
        "onshape_client.oas.models.btfs_table_row_metadata2262"
    ]


class BTTableBaseRowMetadata3181(ModelNormal):
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
            "bt_type": (str,),  # noqa: E501
            "cross_highlight_data_if_any": (
                bt_table_base_cross_highlight_data2609.BTTableBaseCrossHighlightData2609,
            ),
            # noqa: E501
        }

    @staticmethod
    def discriminator():
        return {
            "bt_type": {
                "BTFSTableRowMetadata-2262": btfs_table_row_metadata2262.BTFSTableRowMetadata2262,
                "BTBillOfMaterialsTableRowMetadata-1300": bt_bill_of_materials_table_row_metadata1300.BTBillOfMaterialsTableRowMetadata1300,
                "BTBaseSMJointTableRowMetadata-2232": bt_base_sm_joint_table_row_metadata2232.BTBaseSMJointTableRowMetadata2232,
            },
        }

    attribute_map = {
        "bt_type": "btType",  # noqa: E501
        "cross_highlight_data_if_any": "crossHighlightDataIfAny",  # noqa: E501
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
        """bt_table_base_row_metadata3181.BTTableBaseRowMetadata3181 - a model defined in OpenAPI


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
            bt_type (str): [optional]  # noqa: E501
            cross_highlight_data_if_any (bt_table_base_cross_highlight_data2609.BTTableBaseCrossHighlightData2609): [optional]  # noqa: E501
        """

        self._data_store = {}
        self._check_type = _check_type
        self._from_server = _from_server
        self._path_to_item = _path_to_item
        self._configuration = _configuration

        for var_name, var_value in six.iteritems(kwargs):
            setattr(self, var_name, var_value)

    @classmethod
    def get_discriminator_class(cls, from_server, data):
        """Returns the child class specified by the discriminator"""
        discriminator = cls.discriminator()
        discr_propertyname_py = list(discriminator.keys())[0]
        discr_propertyname_js = cls.attribute_map[discr_propertyname_py]
        if from_server:
            class_name = data[discr_propertyname_js]
        else:
            class_name = data[discr_propertyname_py]
        class_name_to_discr_class = discriminator[discr_propertyname_py]
        return class_name_to_discr_class.get(class_name)
