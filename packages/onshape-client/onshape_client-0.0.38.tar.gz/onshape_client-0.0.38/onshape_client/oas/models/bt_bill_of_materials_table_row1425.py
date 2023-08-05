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
    ModelComposed,
    int,
    str,
    validate_get_composed_info,
)

try:
    from onshape_client.oas.models import bt_bill_of_materials_table_row1425_all_of
except ImportError:
    bt_bill_of_materials_table_row1425_all_of = sys.modules[
        "onshape_client.oas.models.bt_bill_of_materials_table_row1425_all_of"
    ]
try:
    from onshape_client.oas.models import bt_bill_of_materials_unique_item_id2029
except ImportError:
    bt_bill_of_materials_unique_item_id2029 = sys.modules[
        "onshape_client.oas.models.bt_bill_of_materials_unique_item_id2029"
    ]
try:
    from onshape_client.oas.models import bt_table_base_row_metadata3181
except ImportError:
    bt_table_base_row_metadata3181 = sys.modules[
        "onshape_client.oas.models.bt_table_base_row_metadata3181"
    ]
try:
    from onshape_client.oas.models import bt_table_cell1114
except ImportError:
    bt_table_cell1114 = sys.modules["onshape_client.oas.models.bt_table_cell1114"]
try:
    from onshape_client.oas.models import bt_table_row1054
except ImportError:
    bt_table_row1054 = sys.modules["onshape_client.oas.models.bt_table_row1054"]
try:
    from onshape_client.oas.models import bt_tree_node20
except ImportError:
    bt_tree_node20 = sys.modules["onshape_client.oas.models.bt_tree_node20"]


class BTBillOfMaterialsTableRow1425(ModelComposed):
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

    allowed_values = {
        ("expansion_status",): {
            "NOT_EXPANDABLE": "NOT_EXPANDABLE",
            "EXPANDED": "EXPANDED",
            "COLLAPSED": "COLLAPSED",
            "UNKNOWN": "UNKNOWN",
        },
        ("exclusion_status",): {
            "NOT_EXCLUDED": "NOT_EXCLUDED",
            "PARENT_EXCLUDED": "PARENT_EXCLUDED",
            "EXCLUDED": "EXCLUDED",
            "UNKNOWN": "UNKNOWN",
        },
    }

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
            "unique_item_id": (
                bt_bill_of_materials_unique_item_id2029.BTBillOfMaterialsUniqueItemId2029,
            ),
            # noqa: E501
            "indent_level": (int,),  # noqa: E501
            "expansion_status": (str,),  # noqa: E501
            "exclusion_status": (str,),  # noqa: E501
            "exclude_is_editable": (bool,),  # noqa: E501
            "metadata_update_href": (str,),  # noqa: E501
            "bt_type": (str,),  # noqa: E501
            "column_id_to_cell": (
                {str: (bt_table_cell1114.BTTableCell1114,)},
            ),  # noqa: E501
            "id": (str,),  # noqa: E501
            "meta_data": (bt_tree_node20.BTTreeNode20,),  # noqa: E501
            "node_id": (str,),  # noqa: E501
            "row_metadata": (
                bt_table_base_row_metadata3181.BTTableBaseRowMetadata3181,
            ),  # noqa: E501
        }

    @staticmethod
    def discriminator():
        return None

    attribute_map = {
        "unique_item_id": "uniqueItemId",  # noqa: E501
        "indent_level": "indentLevel",  # noqa: E501
        "expansion_status": "expansionStatus",  # noqa: E501
        "exclusion_status": "exclusionStatus",  # noqa: E501
        "exclude_is_editable": "excludeIsEditable",  # noqa: E501
        "metadata_update_href": "metadataUpdateHref",  # noqa: E501
        "bt_type": "btType",  # noqa: E501
        "column_id_to_cell": "columnIdToCell",  # noqa: E501
        "id": "id",  # noqa: E501
        "meta_data": "metaData",  # noqa: E501
        "node_id": "nodeId",  # noqa: E501
        "row_metadata": "rowMetadata",  # noqa: E501
    }

    required_properties = set(
        [
            "_data_store",
            "_check_type",
            "_from_server",
            "_path_to_item",
            "_configuration",
            "_composed_instances",
            "_var_name_to_model_instances",
            "_additional_properties_model_instances",
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
        """bt_bill_of_materials_table_row1425.BTBillOfMaterialsTableRow1425 - a model defined in OpenAPI


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
            unique_item_id (bt_bill_of_materials_unique_item_id2029.BTBillOfMaterialsUniqueItemId2029): [optional]  # noqa: E501
            indent_level (int): [optional]  # noqa: E501
            expansion_status (str): [optional]  # noqa: E501
            exclusion_status (str): [optional]  # noqa: E501
            exclude_is_editable (bool): [optional]  # noqa: E501
            metadata_update_href (str): [optional]  # noqa: E501
            bt_type (str): [optional]  # noqa: E501
            column_id_to_cell ({str: (bt_table_cell1114.BTTableCell1114,)}): [optional]  # noqa: E501
            id (str): [optional]  # noqa: E501
            meta_data (bt_tree_node20.BTTreeNode20): [optional]  # noqa: E501
            node_id (str): [optional]  # noqa: E501
            row_metadata (bt_table_base_row_metadata3181.BTTableBaseRowMetadata3181): [optional]  # noqa: E501
        """

        self._data_store = {}
        self._check_type = _check_type
        self._from_server = _from_server
        self._path_to_item = _path_to_item
        self._configuration = _configuration

        constant_args = {
            "_check_type": _check_type,
            "_path_to_item": _path_to_item,
            "_from_server": _from_server,
            "_configuration": _configuration,
        }
        model_args = {}
        model_args.update(kwargs)
        composed_info = validate_get_composed_info(constant_args, model_args, self)
        self._composed_instances = composed_info[0]
        self._var_name_to_model_instances = composed_info[1]
        self._additional_properties_model_instances = composed_info[2]

        for var_name, var_value in six.iteritems(kwargs):
            setattr(self, var_name, var_value)

    @staticmethod
    def _composed_schemas():
        # we need this here to make our import statements work
        # we must store _composed_schemas in here so the code is only run
        # when we invoke this method. If we kept this at the class
        # level we would get an error beause the class level
        # code would be run when this module is imported, and these composed
        # classes don't exist yet because their module has not finished
        # loading
        return {
            "anyOf": [],
            "allOf": [
                bt_bill_of_materials_table_row1425_all_of.BTBillOfMaterialsTableRow1425AllOf,
                bt_table_row1054.BTTableRow1054,
            ],
            "oneOf": [],
        }
