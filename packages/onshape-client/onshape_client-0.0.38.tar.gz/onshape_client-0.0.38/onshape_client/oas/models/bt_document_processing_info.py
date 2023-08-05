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
    date,
    datetime,
    int,
    str,
    validate_get_composed_info,
)

try:
    from onshape_client.oas.models import bt_base_info
except ImportError:
    bt_base_info = sys.modules["onshape_client.oas.models.bt_base_info"]
try:
    from onshape_client.oas.models import bt_document_info
except ImportError:
    bt_document_info = sys.modules["onshape_client.oas.models.bt_document_info"]
try:
    from onshape_client.oas.models import bt_document_label_info
except ImportError:
    bt_document_label_info = sys.modules[
        "onshape_client.oas.models.bt_document_label_info"
    ]
try:
    from onshape_client.oas.models import bt_document_processing_info_all_of
except ImportError:
    bt_document_processing_info_all_of = sys.modules[
        "onshape_client.oas.models.bt_document_processing_info_all_of"
    ]
try:
    from onshape_client.oas.models import bt_owner_info
except ImportError:
    bt_owner_info = sys.modules["onshape_client.oas.models.bt_owner_info"]
try:
    from onshape_client.oas.models import bt_thumbnail_info
except ImportError:
    bt_thumbnail_info = sys.modules["onshape_client.oas.models.bt_thumbnail_info"]
try:
    from onshape_client.oas.models import bt_user_basic_summary_info
except ImportError:
    bt_user_basic_summary_info = sys.modules[
        "onshape_client.oas.models.bt_user_basic_summary_info"
    ]
try:
    from onshape_client.oas.models import bt_workspace_info
except ImportError:
    bt_workspace_info = sys.modules["onshape_client.oas.models.bt_workspace_info"]


class BTDocumentProcessingInfo(ModelComposed):
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
        ("permission",): {
            "NOACCESS": "NOACCESS",
            "ANONYMOUS_ACCESS": "ANONYMOUS_ACCESS",
            "READ": "READ",
            "READ_COPY_EXPORT": "READ_COPY_EXPORT",
            "COMMENT": "COMMENT",
            "WRITE": "WRITE",
            "RESHARE": "RESHARE",
            "FULL": "FULL",
            "OWNER": "OWNER",
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
            "translation_event_key": (str,),  # noqa: E501
            "translation_id": (str,),  # noqa: E501
            "anonymous_access_allowed": (bool,),  # noqa: E501
            "anonymous_allows_export": (bool,),  # noqa: E501
            "beta_capability_ids": ([str],),  # noqa: E501
            "can_move": (bool,),  # noqa: E501
            "can_unshare": (bool,),  # noqa: E501
            "created_at": (datetime,),  # noqa: E501
            "created_by": (
                bt_user_basic_summary_info.BTUserBasicSummaryInfo,
            ),  # noqa: E501
            "created_with_education_plan": (bool,),  # noqa: E501
            "default_element_id": (str,),  # noqa: E501
            "default_workspace": (bt_workspace_info.BTWorkspaceInfo,),  # noqa: E501
            "description": (str,),  # noqa: E501
            "document_labels": (
                [bt_document_label_info.BTDocumentLabelInfo],
            ),  # noqa: E501
            "document_thumbnail_element_id": (str,),  # noqa: E501
            "duplicate_name_violation_error": (str,),  # noqa: E501
            "has_pending_owner": (bool,),  # noqa: E501
            "has_release_revisionable_objects": (bool,),  # noqa: E501
            "has_relevant_insertables": (bool,),  # noqa: E501
            "href": (str,),  # noqa: E501
            "id": (str,),  # noqa: E501
            "is_container": (bool,),  # noqa: E501
            "is_enterprise_owned": (bool,),  # noqa: E501
            "is_mutable": (bool,),  # noqa: E501
            "is_orphaned": (bool,),  # noqa: E501
            "is_upgraded_to_latest_version": (bool,),  # noqa: E501
            "is_using_managed_workflow": (bool,),  # noqa: E501
            "json_type": (str,),  # noqa: E501
            "liked_by_current_user": (bool,),  # noqa: E501
            "likes": (int,),  # noqa: E501
            "modified_at": (datetime,),  # noqa: E501
            "modified_by": (
                bt_user_basic_summary_info.BTUserBasicSummaryInfo,
            ),  # noqa: E501
            "name": (str,),  # noqa: E501
            "not_revision_managed": (bool,),  # noqa: E501
            "number_of_times_copied": (int,),  # noqa: E501
            "number_of_times_referenced": (int,),  # noqa: E501
            "owner": (bt_owner_info.BTOwnerInfo,),  # noqa: E501
            "parent_id": (str,),  # noqa: E501
            "permission": (str,),  # noqa: E501
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
            "public": (bool,),  # noqa: E501
            "recent_version": (bt_base_info.BTBaseInfo,),  # noqa: E501
            "resource_type": (str,),  # noqa: E501
            "support_team_user_and_shared": (bool,),  # noqa: E501
            "tags": ([str],),  # noqa: E501
            "thumbnail": (bt_thumbnail_info.BTThumbnailInfo,),  # noqa: E501
            "total_workspaces_scheduled_for_update": (int,),  # noqa: E501
            "total_workspaces_updating": (int,),  # noqa: E501
            "trash": (bool,),  # noqa: E501
            "trashed_at": (datetime,),  # noqa: E501
            "tree_href": (str,),  # noqa: E501
            "user_account_limits_breached": (bool,),  # noqa: E501
            "view_ref": (str,),  # noqa: E501
        }

    @staticmethod
    def discriminator():
        return None

    attribute_map = {
        "translation_event_key": "translationEventKey",  # noqa: E501
        "translation_id": "translationId",  # noqa: E501
        "anonymous_access_allowed": "anonymousAccessAllowed",  # noqa: E501
        "anonymous_allows_export": "anonymousAllowsExport",  # noqa: E501
        "beta_capability_ids": "betaCapabilityIds",  # noqa: E501
        "can_move": "canMove",  # noqa: E501
        "can_unshare": "canUnshare",  # noqa: E501
        "created_at": "createdAt",  # noqa: E501
        "created_by": "createdBy",  # noqa: E501
        "created_with_education_plan": "createdWithEducationPlan",  # noqa: E501
        "default_element_id": "defaultElementId",  # noqa: E501
        "default_workspace": "defaultWorkspace",  # noqa: E501
        "description": "description",  # noqa: E501
        "document_labels": "documentLabels",  # noqa: E501
        "document_thumbnail_element_id": "documentThumbnailElementId",  # noqa: E501
        "duplicate_name_violation_error": "duplicateNameViolationError",  # noqa: E501
        "has_pending_owner": "hasPendingOwner",  # noqa: E501
        "has_release_revisionable_objects": "hasReleaseRevisionableObjects",  # noqa: E501
        "has_relevant_insertables": "hasRelevantInsertables",  # noqa: E501
        "href": "href",  # noqa: E501
        "id": "id",  # noqa: E501
        "is_container": "isContainer",  # noqa: E501
        "is_enterprise_owned": "isEnterpriseOwned",  # noqa: E501
        "is_mutable": "isMutable",  # noqa: E501
        "is_orphaned": "isOrphaned",  # noqa: E501
        "is_upgraded_to_latest_version": "isUpgradedToLatestVersion",  # noqa: E501
        "is_using_managed_workflow": "isUsingManagedWorkflow",  # noqa: E501
        "json_type": "jsonType",  # noqa: E501
        "liked_by_current_user": "likedByCurrentUser",  # noqa: E501
        "likes": "likes",  # noqa: E501
        "modified_at": "modifiedAt",  # noqa: E501
        "modified_by": "modifiedBy",  # noqa: E501
        "name": "name",  # noqa: E501
        "not_revision_managed": "notRevisionManaged",  # noqa: E501
        "number_of_times_copied": "numberOfTimesCopied",  # noqa: E501
        "number_of_times_referenced": "numberOfTimesReferenced",  # noqa: E501
        "owner": "owner",  # noqa: E501
        "parent_id": "parentId",  # noqa: E501
        "permission": "permission",  # noqa: E501
        "permission_set": "permissionSet",  # noqa: E501
        "project_id": "projectId",  # noqa: E501
        "public": "public",  # noqa: E501
        "recent_version": "recentVersion",  # noqa: E501
        "resource_type": "resourceType",  # noqa: E501
        "support_team_user_and_shared": "supportTeamUserAndShared",  # noqa: E501
        "tags": "tags",  # noqa: E501
        "thumbnail": "thumbnail",  # noqa: E501
        "total_workspaces_scheduled_for_update": "totalWorkspacesScheduledForUpdate",  # noqa: E501
        "total_workspaces_updating": "totalWorkspacesUpdating",  # noqa: E501
        "trash": "trash",  # noqa: E501
        "trashed_at": "trashedAt",  # noqa: E501
        "tree_href": "treeHref",  # noqa: E501
        "user_account_limits_breached": "userAccountLimitsBreached",  # noqa: E501
        "view_ref": "viewRef",  # noqa: E501
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
        """bt_document_processing_info.BTDocumentProcessingInfo - a model defined in OpenAPI


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
            translation_event_key (str): [optional]  # noqa: E501
            translation_id (str): [optional]  # noqa: E501
            anonymous_access_allowed (bool): [optional]  # noqa: E501
            anonymous_allows_export (bool): [optional]  # noqa: E501
            beta_capability_ids ([str]): [optional]  # noqa: E501
            can_move (bool): [optional]  # noqa: E501
            can_unshare (bool): [optional]  # noqa: E501
            created_at (datetime): [optional]  # noqa: E501
            created_by (bt_user_basic_summary_info.BTUserBasicSummaryInfo): [optional]  # noqa: E501
            created_with_education_plan (bool): [optional]  # noqa: E501
            default_element_id (str): [optional]  # noqa: E501
            default_workspace (bt_workspace_info.BTWorkspaceInfo): [optional]  # noqa: E501
            description (str): [optional]  # noqa: E501
            document_labels ([bt_document_label_info.BTDocumentLabelInfo]): [optional]  # noqa: E501
            document_thumbnail_element_id (str): [optional]  # noqa: E501
            duplicate_name_violation_error (str): [optional]  # noqa: E501
            has_pending_owner (bool): [optional]  # noqa: E501
            has_release_revisionable_objects (bool): [optional]  # noqa: E501
            has_relevant_insertables (bool): [optional]  # noqa: E501
            href (str): [optional]  # noqa: E501
            id (str): [optional]  # noqa: E501
            is_container (bool): [optional]  # noqa: E501
            is_enterprise_owned (bool): [optional]  # noqa: E501
            is_mutable (bool): [optional]  # noqa: E501
            is_orphaned (bool): [optional]  # noqa: E501
            is_upgraded_to_latest_version (bool): [optional]  # noqa: E501
            is_using_managed_workflow (bool): [optional]  # noqa: E501
            json_type (str): [optional]  # noqa: E501
            liked_by_current_user (bool): [optional]  # noqa: E501
            likes (int): [optional]  # noqa: E501
            modified_at (datetime): [optional]  # noqa: E501
            modified_by (bt_user_basic_summary_info.BTUserBasicSummaryInfo): [optional]  # noqa: E501
            name (str): [optional]  # noqa: E501
            not_revision_managed (bool): [optional]  # noqa: E501
            number_of_times_copied (int): [optional]  # noqa: E501
            number_of_times_referenced (int): [optional]  # noqa: E501
            owner (bt_owner_info.BTOwnerInfo): [optional]  # noqa: E501
            parent_id (str): [optional]  # noqa: E501
            permission (str): [optional]  # noqa: E501
            permission_set (bool, date, datetime, dict, float, int, list, str): [optional]  # noqa: E501
            project_id (str): [optional]  # noqa: E501
            public (bool): [optional]  # noqa: E501
            recent_version (bt_base_info.BTBaseInfo): [optional]  # noqa: E501
            resource_type (str): [optional]  # noqa: E501
            support_team_user_and_shared (bool): [optional]  # noqa: E501
            tags ([str]): [optional]  # noqa: E501
            thumbnail (bt_thumbnail_info.BTThumbnailInfo): [optional]  # noqa: E501
            total_workspaces_scheduled_for_update (int): [optional]  # noqa: E501
            total_workspaces_updating (int): [optional]  # noqa: E501
            trash (bool): [optional]  # noqa: E501
            trashed_at (datetime): [optional]  # noqa: E501
            tree_href (str): [optional]  # noqa: E501
            user_account_limits_breached (bool): [optional]  # noqa: E501
            view_ref (str): [optional]  # noqa: E501
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
                bt_document_info.BTDocumentInfo,
                bt_document_processing_info_all_of.BTDocumentProcessingInfoAllOf,
            ],
            "oneOf": [],
        }
