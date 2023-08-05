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
    from onshape_client.oas.models import btm_parameter1
except ImportError:
    btm_parameter1 = sys.modules["onshape_client.oas.models.btm_parameter1"]
try:
    from onshape_client.oas.models import btm_sketch_curve4
except ImportError:
    btm_sketch_curve4 = sys.modules["onshape_client.oas.models.btm_sketch_curve4"]
try:
    from onshape_client.oas.models import btm_sketch_image_entity763
except ImportError:
    btm_sketch_image_entity763 = sys.modules[
        "onshape_client.oas.models.btm_sketch_image_entity763"
    ]
try:
    from onshape_client.oas.models import btm_sketch_point158
except ImportError:
    btm_sketch_point158 = sys.modules["onshape_client.oas.models.btm_sketch_point158"]
try:
    from onshape_client.oas.models import btm_sketch_text_entity1761
except ImportError:
    btm_sketch_text_entity1761 = sys.modules[
        "onshape_client.oas.models.btm_sketch_text_entity1761"
    ]


class BTMSketchGeomEntity5(ModelNormal):
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
            "control_box_ids": ([str],),  # noqa: E501
            "entity_id": (str,),  # noqa: E501
            "entity_id_and_replace_in_dependent_fields": (str,),  # noqa: E501
            "import_microversion": (str,),  # noqa: E501
            "is_construction": (bool,),  # noqa: E501
            "namespace": (str,),  # noqa: E501
            "node_id": (str,),  # noqa: E501
            "parameters": ([btm_parameter1.BTMParameter1],),  # noqa: E501
        }

    @staticmethod
    def discriminator():
        return {
            "bt_type": {
                "BTMSketchImageEntity-763": btm_sketch_image_entity763.BTMSketchImageEntity763,
                "BTMSketchTextEntity-1761": btm_sketch_text_entity1761.BTMSketchTextEntity1761,
                "BTMSketchCurve-4": btm_sketch_curve4.BTMSketchCurve4,
                "BTMSketchPoint-158": btm_sketch_point158.BTMSketchPoint158,
            },
        }

    attribute_map = {
        "bt_type": "btType",  # noqa: E501
        "control_box_ids": "controlBoxIds",  # noqa: E501
        "entity_id": "entityId",  # noqa: E501
        "entity_id_and_replace_in_dependent_fields": "entityIdAndReplaceInDependentFields",  # noqa: E501
        "import_microversion": "importMicroversion",  # noqa: E501
        "is_construction": "isConstruction",  # noqa: E501
        "namespace": "namespace",  # noqa: E501
        "node_id": "nodeId",  # noqa: E501
        "parameters": "parameters",  # noqa: E501
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
        """btm_sketch_geom_entity5.BTMSketchGeomEntity5 - a model defined in OpenAPI


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
            control_box_ids ([str]): [optional]  # noqa: E501
            entity_id (str): [optional]  # noqa: E501
            entity_id_and_replace_in_dependent_fields (str): [optional]  # noqa: E501
            import_microversion (str): [optional]  # noqa: E501
            is_construction (bool): [optional]  # noqa: E501
            namespace (str): [optional]  # noqa: E501
            node_id (str): [optional]  # noqa: E501
            parameters ([btm_parameter1.BTMParameter1]): [optional]  # noqa: E501
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
