# coding: utf-8

"""
    Onshape REST API

    The Onshape REST API consumed by all clients.  # noqa: E501

    The version of the OpenAPI document: 1.108
    Contact: api-support@onshape.zendesk.com
    Generated by: https://openapi-generator.tech
"""

from __future__ import absolute_import

import sys  # noqa: F401

import six  # noqa: F401
from onshape_client.oas.model_utils import (  # noqa: F401
    ModelComposed,
    datetime,
    int,
    str,
    validate_get_composed_info,
)

try:
    from onshape_client.oas.models import bt_billing_plan_info
except ImportError:
    bt_billing_plan_info = sys.modules["onshape_client.oas.models.bt_billing_plan_info"]
try:
    from onshape_client.oas.models import bt_company_summary_info
except ImportError:
    bt_company_summary_info = sys.modules[
        "onshape_client.oas.models.bt_company_summary_info"
    ]
try:
    from onshape_client.oas.models import bt_device_login_secret_info
except ImportError:
    bt_device_login_secret_info = sys.modules[
        "onshape_client.oas.models.bt_device_login_secret_info"
    ]
try:
    from onshape_client.oas.models import bt_discount
except ImportError:
    bt_discount = sys.modules["onshape_client.oas.models.bt_discount"]
try:
    from onshape_client.oas.models import bt_privacy_consent_info
except ImportError:
    bt_privacy_consent_info = sys.modules[
        "onshape_client.oas.models.bt_privacy_consent_info"
    ]
try:
    from onshape_client.oas.models import bt_purchase_info
except ImportError:
    bt_purchase_info = sys.modules["onshape_client.oas.models.bt_purchase_info"]
try:
    from onshape_client.oas.models import bt_session_credential_info
except ImportError:
    bt_session_credential_info = sys.modules[
        "onshape_client.oas.models.bt_session_credential_info"
    ]
try:
    from onshape_client.oas.models import bt_trial_info
except ImportError:
    bt_trial_info = sys.modules["onshape_client.oas.models.bt_trial_info"]
try:
    from onshape_client.oas.models import bt_user_admin_info_all_of
except ImportError:
    bt_user_admin_info_all_of = sys.modules[
        "onshape_client.oas.models.bt_user_admin_info_all_of"
    ]
try:
    from onshape_client.oas.models import bt_user_info
except ImportError:
    bt_user_info = sys.modules["onshape_client.oas.models.bt_user_info"]
try:
    from onshape_client.oas.models import bt_user_metrics_info
except ImportError:
    bt_user_metrics_info = sys.modules["onshape_client.oas.models.bt_user_metrics_info"]
try:
    from onshape_client.oas.models import global_permission_info
except ImportError:
    global_permission_info = sys.modules[
        "onshape_client.oas.models.global_permission_info"
    ]


class BTUserAdminInfo(ModelComposed):
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
        ("roles",): {
            "ANONYMOUS": "ANONYMOUS",
            "TOTPPENDINGUSER": "TOTPPENDINGUSER",
            "USER": "USER",
            "DEVELOPER": "DEVELOPER",
            "PARTNER": "PARTNER",
            "ONSHAPECOMPANYUSER": "ONSHAPECOMPANYUSER",
            "ADMIN": "ADMIN",
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
            "is_trial_request": (bool,),  # noqa: E501
            "discount": (bt_discount.BTDiscount,),  # noqa: E501
            "invited_by_email": (str,),  # noqa: E501
            "invited_document_id": (str,),  # noqa: E501
            "user_metrics": (bt_user_metrics_info.BTUserMetricsInfo,),  # noqa: E501
            "privacy_consents": (
                [bt_privacy_consent_info.BTPrivacyConsentInfo],
            ),  # noqa: E501
            "invitation_id": (str,),  # noqa: E501
            "image": (str,),  # noqa: E501
            "state": (int,),  # noqa: E501
            "href": (str,),  # noqa: E501
            "view_ref": (str,),  # noqa: E501
            "name": (str,),  # noqa: E501
            "id": (str,),  # noqa: E501
            "json_type": (str,),  # noqa: E501
            "first_name": (str,),  # noqa: E501
            "last_name": (str,),  # noqa: E501
            "email": (str,),  # noqa: E501
            "last_login_time": (datetime,),  # noqa: E501
            "company": (bt_company_summary_info.BTCompanySummaryInfo,),  # noqa: E501
            "global_permissions": (
                global_permission_info.GlobalPermissionInfo,
            ),  # noqa: E501
            "is_guest": (bool,),  # noqa: E501
            "is_light": (bool,),  # noqa: E501
            "source": (int,),  # noqa: E501
            "default_company_name": (str,),  # noqa: E501
            "description": (str,),  # noqa: E501
            "own_purchase": (bt_purchase_info.BTPurchaseInfo,),  # noqa: E501
            "active_purchases": ([bt_purchase_info.BTPurchaseInfo],),  # noqa: E501
            "enterprise": (bool,),  # noqa: E501
            "active_trial_info": (bt_trial_info.BTTrialInfo,),  # noqa: E501
            "active_plan_id": (str,),  # noqa: E501
            "last_trial_info": (bt_trial_info.BTTrialInfo,),  # noqa: E501
            "device_info": (
                bt_device_login_secret_info.BTDeviceLoginSecretInfo,
            ),  # noqa: E501
            "eula_required": (bool,),  # noqa: E501
            "eula_id": (str,),  # noqa: E501
            "credential": (
                bt_session_credential_info.BTSessionCredentialInfo,
            ),  # noqa: E501
            "startup_page": (int,),  # noqa: E501
            "forum_id": (str,),  # noqa: E501
            "phone_number": (str,),  # noqa: E501
            "totp_enabled": (bool,),  # noqa: E501
            "created_at": (datetime,),  # noqa: E501
            "country_code": (str,),  # noqa: E501
            "role": (int,),  # noqa: E501
            "cad_system_at_signup": (str,),  # noqa: E501
            "system_user": (bool,),  # noqa: E501
            "billing_update_required": (bool,),  # noqa: E501
            "active_plan": (bt_billing_plan_info.BTBillingPlanInfo,),  # noqa: E501
            "roles": ([str],),  # noqa: E501
        }

    @staticmethod
    def discriminator():
        return None

    attribute_map = {
        "is_trial_request": "isTrialRequest",  # noqa: E501
        "discount": "discount",  # noqa: E501
        "invited_by_email": "invitedByEmail",  # noqa: E501
        "invited_document_id": "invitedDocumentId",  # noqa: E501
        "user_metrics": "userMetrics",  # noqa: E501
        "privacy_consents": "privacyConsents",  # noqa: E501
        "invitation_id": "invitationId",  # noqa: E501
        "image": "image",  # noqa: E501
        "state": "state",  # noqa: E501
        "href": "href",  # noqa: E501
        "view_ref": "viewRef",  # noqa: E501
        "name": "name",  # noqa: E501
        "id": "id",  # noqa: E501
        "json_type": "jsonType",  # noqa: E501
        "first_name": "firstName",  # noqa: E501
        "last_name": "lastName",  # noqa: E501
        "email": "email",  # noqa: E501
        "last_login_time": "lastLoginTime",  # noqa: E501
        "company": "company",  # noqa: E501
        "global_permissions": "globalPermissions",  # noqa: E501
        "is_guest": "isGuest",  # noqa: E501
        "is_light": "isLight",  # noqa: E501
        "source": "source",  # noqa: E501
        "default_company_name": "defaultCompanyName",  # noqa: E501
        "description": "description",  # noqa: E501
        "own_purchase": "ownPurchase",  # noqa: E501
        "active_purchases": "activePurchases",  # noqa: E501
        "enterprise": "enterprise",  # noqa: E501
        "active_trial_info": "activeTrialInfo",  # noqa: E501
        "active_plan_id": "activePlanId",  # noqa: E501
        "last_trial_info": "lastTrialInfo",  # noqa: E501
        "device_info": "deviceInfo",  # noqa: E501
        "eula_required": "eulaRequired",  # noqa: E501
        "eula_id": "eulaId",  # noqa: E501
        "credential": "credential",  # noqa: E501
        "startup_page": "startupPage",  # noqa: E501
        "forum_id": "forumId",  # noqa: E501
        "phone_number": "phoneNumber",  # noqa: E501
        "totp_enabled": "totpEnabled",  # noqa: E501
        "created_at": "createdAt",  # noqa: E501
        "country_code": "countryCode",  # noqa: E501
        "role": "role",  # noqa: E501
        "cad_system_at_signup": "cadSystemAtSignup",  # noqa: E501
        "system_user": "systemUser",  # noqa: E501
        "billing_update_required": "billingUpdateRequired",  # noqa: E501
        "active_plan": "activePlan",  # noqa: E501
        "roles": "roles",  # noqa: E501
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
        """bt_user_admin_info.BTUserAdminInfo - a model defined in OpenAPI


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
            is_trial_request (bool): [optional]  # noqa: E501
            discount (bt_discount.BTDiscount): [optional]  # noqa: E501
            invited_by_email (str): [optional]  # noqa: E501
            invited_document_id (str): [optional]  # noqa: E501
            user_metrics (bt_user_metrics_info.BTUserMetricsInfo): [optional]  # noqa: E501
            privacy_consents ([bt_privacy_consent_info.BTPrivacyConsentInfo]): [optional]  # noqa: E501
            invitation_id (str): [optional]  # noqa: E501
            image (str): [optional]  # noqa: E501
            state (int): [optional]  # noqa: E501
            href (str): [optional]  # noqa: E501
            view_ref (str): [optional]  # noqa: E501
            name (str): [optional]  # noqa: E501
            id (str): [optional]  # noqa: E501
            json_type (str): [optional]  # noqa: E501
            first_name (str): [optional]  # noqa: E501
            last_name (str): [optional]  # noqa: E501
            email (str): [optional]  # noqa: E501
            last_login_time (datetime): [optional]  # noqa: E501
            company (bt_company_summary_info.BTCompanySummaryInfo): [optional]  # noqa: E501
            global_permissions (global_permission_info.GlobalPermissionInfo): [optional]  # noqa: E501
            is_guest (bool): [optional]  # noqa: E501
            is_light (bool): [optional]  # noqa: E501
            source (int): [optional]  # noqa: E501
            default_company_name (str): [optional]  # noqa: E501
            description (str): [optional]  # noqa: E501
            own_purchase (bt_purchase_info.BTPurchaseInfo): [optional]  # noqa: E501
            active_purchases ([bt_purchase_info.BTPurchaseInfo]): [optional]  # noqa: E501
            enterprise (bool): [optional]  # noqa: E501
            active_trial_info (bt_trial_info.BTTrialInfo): [optional]  # noqa: E501
            active_plan_id (str): [optional]  # noqa: E501
            last_trial_info (bt_trial_info.BTTrialInfo): [optional]  # noqa: E501
            device_info (bt_device_login_secret_info.BTDeviceLoginSecretInfo): [optional]  # noqa: E501
            eula_required (bool): [optional]  # noqa: E501
            eula_id (str): [optional]  # noqa: E501
            credential (bt_session_credential_info.BTSessionCredentialInfo): [optional]  # noqa: E501
            startup_page (int): [optional]  # noqa: E501
            forum_id (str): [optional]  # noqa: E501
            phone_number (str): [optional]  # noqa: E501
            totp_enabled (bool): [optional]  # noqa: E501
            created_at (datetime): [optional]  # noqa: E501
            country_code (str): [optional]  # noqa: E501
            role (int): [optional]  # noqa: E501
            cad_system_at_signup (str): [optional]  # noqa: E501
            system_user (bool): [optional]  # noqa: E501
            billing_update_required (bool): [optional]  # noqa: E501
            active_plan (bt_billing_plan_info.BTBillingPlanInfo): [optional]  # noqa: E501
            roles ([str]): [optional]  # noqa: E501
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
                bt_user_admin_info_all_of.BTUserAdminInfoAllOf,
                bt_user_info.BTUserInfo,
            ],
            "oneOf": [],
        }
