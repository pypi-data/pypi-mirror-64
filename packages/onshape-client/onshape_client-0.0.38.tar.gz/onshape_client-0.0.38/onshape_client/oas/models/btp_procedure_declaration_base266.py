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
    from onshape_client.oas.models import btp_annotation231
except ImportError:
    btp_annotation231 = sys.modules["onshape_client.oas.models.btp_annotation231"]
try:
    from onshape_client.oas.models import btp_argument_declaration232
except ImportError:
    btp_argument_declaration232 = sys.modules[
        "onshape_client.oas.models.btp_argument_declaration232"
    ]
try:
    from onshape_client.oas.models import btp_conversion_function1362
except ImportError:
    btp_conversion_function1362 = sys.modules[
        "onshape_client.oas.models.btp_conversion_function1362"
    ]
try:
    from onshape_client.oas.models import btp_function_or_predicate_declaration247
except ImportError:
    btp_function_or_predicate_declaration247 = sys.modules[
        "onshape_client.oas.models.btp_function_or_predicate_declaration247"
    ]
try:
    from onshape_client.oas.models import btp_identifier8
except ImportError:
    btp_identifier8 = sys.modules["onshape_client.oas.models.btp_identifier8"]
try:
    from onshape_client.oas.models import btp_operator_declaration264
except ImportError:
    btp_operator_declaration264 = sys.modules[
        "onshape_client.oas.models.btp_operator_declaration264"
    ]
try:
    from onshape_client.oas.models import btp_procedure_declaration_base266_all_of
except ImportError:
    btp_procedure_declaration_base266_all_of = sys.modules[
        "onshape_client.oas.models.btp_procedure_declaration_base266_all_of"
    ]
try:
    from onshape_client.oas.models import btp_space10
except ImportError:
    btp_space10 = sys.modules["onshape_client.oas.models.btp_space10"]
try:
    from onshape_client.oas.models import btp_statement269
except ImportError:
    btp_statement269 = sys.modules["onshape_client.oas.models.btp_statement269"]
try:
    from onshape_client.oas.models import btp_statement_block271
except ImportError:
    btp_statement_block271 = sys.modules[
        "onshape_client.oas.models.btp_statement_block271"
    ]
try:
    from onshape_client.oas.models import btp_top_level_node286
except ImportError:
    btp_top_level_node286 = sys.modules[
        "onshape_client.oas.models.btp_top_level_node286"
    ]
try:
    from onshape_client.oas.models import btp_type_name290
except ImportError:
    btp_type_name290 = sys.modules["onshape_client.oas.models.btp_type_name290"]


class BTPProcedureDeclarationBase266(ModelComposed):
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
        ("documentation_type",): {
            "FUNCTION": "FUNCTION",
            "PREDICATE": "PREDICATE",
            "CONSTANT": "CONSTANT",
            "ENUM": "ENUM",
            "USER_TYPE": "USER_TYPE",
            "FEATURE_DEFINITION": "FEATURE_DEFINITION",
            "FILE_HEADER": "FILE_HEADER",
            "UNDOCUMENTABLE": "UNDOCUMENTABLE",
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
            "bt_type": (str,),  # noqa: E501
            "body": (btp_statement_block271.BTPStatementBlock271,),  # noqa: E501
            "arguments": (
                [btp_argument_declaration232.BTPArgumentDeclaration232],
            ),  # noqa: E501
            "precondition": (btp_statement269.BTPStatement269,),  # noqa: E501
            "space_after_arglist": (btp_space10.BTPSpace10,),  # noqa: E501
            "space_in_empty_list": (btp_space10.BTPSpace10,),  # noqa: E501
            "return_type": (btp_type_name290.BTPTypeName290,),  # noqa: E501
            "atomic": (bool,),  # noqa: E501
            "documentation_type": (str,),  # noqa: E501
            "end_source_location": (int,),  # noqa: E501
            "node_id": (str,),  # noqa: E501
            "short_descriptor": (str,),  # noqa: E501
            "space_after": (btp_space10.BTPSpace10,),  # noqa: E501
            "space_before": (btp_space10.BTPSpace10,),  # noqa: E501
            "space_default": (bool,),  # noqa: E501
            "start_source_location": (int,),  # noqa: E501
            "deprecated": (bool,),  # noqa: E501
            "symbol_name": (btp_identifier8.BTPIdentifier8,),  # noqa: E501
            "arguments_to_document": (
                [btp_argument_declaration232.BTPArgumentDeclaration232],
            ),  # noqa: E501
            "deprecated_explanation": (str,),  # noqa: E501
            "for_export": (bool,),  # noqa: E501
            "space_after_export": (btp_space10.BTPSpace10,),  # noqa: E501
            "annotation": (btp_annotation231.BTPAnnotation231,),  # noqa: E501
        }

    @staticmethod
    def discriminator():
        return {
            "bt_type": {
                "BTPConversionFunction-1362": btp_conversion_function1362.BTPConversionFunction1362,
                "BTPOperatorDeclaration-264": btp_operator_declaration264.BTPOperatorDeclaration264,
                "BTPFunctionOrPredicateDeclaration-247": btp_function_or_predicate_declaration247.BTPFunctionOrPredicateDeclaration247,
            },
        }

    attribute_map = {
        "bt_type": "btType",  # noqa: E501
        "body": "body",  # noqa: E501
        "arguments": "arguments",  # noqa: E501
        "precondition": "precondition",  # noqa: E501
        "space_after_arglist": "spaceAfterArglist",  # noqa: E501
        "space_in_empty_list": "spaceInEmptyList",  # noqa: E501
        "return_type": "returnType",  # noqa: E501
        "atomic": "atomic",  # noqa: E501
        "documentation_type": "documentationType",  # noqa: E501
        "end_source_location": "endSourceLocation",  # noqa: E501
        "node_id": "nodeId",  # noqa: E501
        "short_descriptor": "shortDescriptor",  # noqa: E501
        "space_after": "spaceAfter",  # noqa: E501
        "space_before": "spaceBefore",  # noqa: E501
        "space_default": "spaceDefault",  # noqa: E501
        "start_source_location": "startSourceLocation",  # noqa: E501
        "deprecated": "deprecated",  # noqa: E501
        "symbol_name": "symbolName",  # noqa: E501
        "arguments_to_document": "argumentsToDocument",  # noqa: E501
        "deprecated_explanation": "deprecatedExplanation",  # noqa: E501
        "for_export": "forExport",  # noqa: E501
        "space_after_export": "spaceAfterExport",  # noqa: E501
        "annotation": "annotation",  # noqa: E501
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
        """btp_procedure_declaration_base266.BTPProcedureDeclarationBase266 - a model defined in OpenAPI


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
            body (btp_statement_block271.BTPStatementBlock271): [optional]  # noqa: E501
            arguments ([btp_argument_declaration232.BTPArgumentDeclaration232]): [optional]  # noqa: E501
            precondition (btp_statement269.BTPStatement269): [optional]  # noqa: E501
            space_after_arglist (btp_space10.BTPSpace10): [optional]  # noqa: E501
            space_in_empty_list (btp_space10.BTPSpace10): [optional]  # noqa: E501
            return_type (btp_type_name290.BTPTypeName290): [optional]  # noqa: E501
            atomic (bool): [optional]  # noqa: E501
            documentation_type (str): [optional]  # noqa: E501
            end_source_location (int): [optional]  # noqa: E501
            node_id (str): [optional]  # noqa: E501
            short_descriptor (str): [optional]  # noqa: E501
            space_after (btp_space10.BTPSpace10): [optional]  # noqa: E501
            space_before (btp_space10.BTPSpace10): [optional]  # noqa: E501
            space_default (bool): [optional]  # noqa: E501
            start_source_location (int): [optional]  # noqa: E501
            deprecated (bool): [optional]  # noqa: E501
            symbol_name (btp_identifier8.BTPIdentifier8): [optional]  # noqa: E501
            arguments_to_document ([btp_argument_declaration232.BTPArgumentDeclaration232]): [optional]  # noqa: E501
            deprecated_explanation (str): [optional]  # noqa: E501
            for_export (bool): [optional]  # noqa: E501
            space_after_export (btp_space10.BTPSpace10): [optional]  # noqa: E501
            annotation (btp_annotation231.BTPAnnotation231): [optional]  # noqa: E501
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
                btp_procedure_declaration_base266_all_of.BTPProcedureDeclarationBase266AllOf,
                btp_top_level_node286.BTPTopLevelNode286,
            ],
            "oneOf": [],
        }

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
