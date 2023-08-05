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
    from onshape_client.oas.models import bt_workflow_action_info
except ImportError:
    bt_workflow_action_info = sys.modules[
        "onshape_client.oas.models.bt_workflow_action_info"
    ]
try:
    from onshape_client.oas.models import bt_workflow_state_info
except ImportError:
    bt_workflow_state_info = sys.modules[
        "onshape_client.oas.models.bt_workflow_state_info"
    ]


class BTWorkflowSnapshotInfo(ModelNormal):
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
            "actions": ([bt_workflow_action_info.BTWorkflowActionInfo],),  # noqa: E501
            "approver_ids": ([str],),  # noqa: E501
            "is_discarded": (bool,),  # noqa: E501
            "is_frozen": (bool,),  # noqa: E501
            "is_setup": (bool,),  # noqa: E501
            "metadata_state": (str,),  # noqa: E501
            "notifier_ids": ([str],),  # noqa: E501
            "state": (bt_workflow_state_info.BTWorkflowStateInfo,),  # noqa: E501
        }

    @staticmethod
    def discriminator():
        return None

    attribute_map = {
        "actions": "actions",  # noqa: E501
        "approver_ids": "approverIds",  # noqa: E501
        "is_discarded": "isDiscarded",  # noqa: E501
        "is_frozen": "isFrozen",  # noqa: E501
        "is_setup": "isSetup",  # noqa: E501
        "metadata_state": "metadataState",  # noqa: E501
        "notifier_ids": "notifierIds",  # noqa: E501
        "state": "state",  # noqa: E501
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
        """bt_workflow_snapshot_info.BTWorkflowSnapshotInfo - a model defined in OpenAPI


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
            actions ([bt_workflow_action_info.BTWorkflowActionInfo]): [optional]  # noqa: E501
            approver_ids ([str]): [optional]  # noqa: E501
            is_discarded (bool): [optional]  # noqa: E501
            is_frozen (bool): [optional]  # noqa: E501
            is_setup (bool): [optional]  # noqa: E501
            metadata_state (str): [optional]  # noqa: E501
            notifier_ids ([str]): [optional]  # noqa: E501
            state (bt_workflow_state_info.BTWorkflowStateInfo): [optional]  # noqa: E501
        """

        self._data_store = {}
        self._check_type = _check_type
        self._from_server = _from_server
        self._path_to_item = _path_to_item
        self._configuration = _configuration

        for var_name, var_value in six.iteritems(kwargs):
            setattr(self, var_name, var_value)
