"""
Main interface for cloudfront service client

Usage::

    import boto3
    from mypy_boto3.cloudfront import CloudFrontClient

    session = boto3.Session()

    client: CloudFrontClient = boto3.client("cloudfront")
    session_client: CloudFrontClient = session.client("cloudfront")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
import sys
from typing import Any, Dict, TYPE_CHECKING, overload
from botocore.exceptions import ClientError as Boto3ClientError
from mypy_boto3_cloudfront.paginator import (
    ListCloudFrontOriginAccessIdentitiesPaginator,
    ListDistributionsPaginator,
    ListInvalidationsPaginator,
    ListStreamingDistributionsPaginator,
)
from mypy_boto3_cloudfront.type_defs import (
    CloudFrontOriginAccessIdentityConfigTypeDef,
    CreateCloudFrontOriginAccessIdentityResultTypeDef,
    CreateDistributionResultTypeDef,
    CreateDistributionWithTagsResultTypeDef,
    CreateFieldLevelEncryptionConfigResultTypeDef,
    CreateFieldLevelEncryptionProfileResultTypeDef,
    CreateInvalidationResultTypeDef,
    CreatePublicKeyResultTypeDef,
    CreateStreamingDistributionResultTypeDef,
    CreateStreamingDistributionWithTagsResultTypeDef,
    DistributionConfigTypeDef,
    DistributionConfigWithTagsTypeDef,
    FieldLevelEncryptionConfigTypeDef,
    FieldLevelEncryptionProfileConfigTypeDef,
    GetCloudFrontOriginAccessIdentityConfigResultTypeDef,
    GetCloudFrontOriginAccessIdentityResultTypeDef,
    GetDistributionConfigResultTypeDef,
    GetDistributionResultTypeDef,
    GetFieldLevelEncryptionConfigResultTypeDef,
    GetFieldLevelEncryptionProfileConfigResultTypeDef,
    GetFieldLevelEncryptionProfileResultTypeDef,
    GetFieldLevelEncryptionResultTypeDef,
    GetInvalidationResultTypeDef,
    GetPublicKeyConfigResultTypeDef,
    GetPublicKeyResultTypeDef,
    GetStreamingDistributionConfigResultTypeDef,
    GetStreamingDistributionResultTypeDef,
    InvalidationBatchTypeDef,
    ListCloudFrontOriginAccessIdentitiesResultTypeDef,
    ListDistributionsByWebACLIdResultTypeDef,
    ListDistributionsResultTypeDef,
    ListFieldLevelEncryptionConfigsResultTypeDef,
    ListFieldLevelEncryptionProfilesResultTypeDef,
    ListInvalidationsResultTypeDef,
    ListPublicKeysResultTypeDef,
    ListStreamingDistributionsResultTypeDef,
    ListTagsForResourceResultTypeDef,
    PublicKeyConfigTypeDef,
    StreamingDistributionConfigTypeDef,
    StreamingDistributionConfigWithTagsTypeDef,
    TagKeysTypeDef,
    TagsTypeDef,
    UpdateCloudFrontOriginAccessIdentityResultTypeDef,
    UpdateDistributionResultTypeDef,
    UpdateFieldLevelEncryptionConfigResultTypeDef,
    UpdateFieldLevelEncryptionProfileResultTypeDef,
    UpdatePublicKeyResultTypeDef,
    UpdateStreamingDistributionResultTypeDef,
)
from mypy_boto3_cloudfront.waiter import (
    DistributionDeployedWaiter,
    InvalidationCompletedWaiter,
    StreamingDistributionDeployedWaiter,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("CloudFrontClient",)


class Exceptions:
    AccessDenied: Boto3ClientError
    BatchTooLarge: Boto3ClientError
    CNAMEAlreadyExists: Boto3ClientError
    CannotChangeImmutablePublicKeyFields: Boto3ClientError
    ClientError: Boto3ClientError
    CloudFrontOriginAccessIdentityAlreadyExists: Boto3ClientError
    CloudFrontOriginAccessIdentityInUse: Boto3ClientError
    DistributionAlreadyExists: Boto3ClientError
    DistributionNotDisabled: Boto3ClientError
    FieldLevelEncryptionConfigAlreadyExists: Boto3ClientError
    FieldLevelEncryptionConfigInUse: Boto3ClientError
    FieldLevelEncryptionProfileAlreadyExists: Boto3ClientError
    FieldLevelEncryptionProfileInUse: Boto3ClientError
    FieldLevelEncryptionProfileSizeExceeded: Boto3ClientError
    IllegalFieldLevelEncryptionConfigAssociationWithCacheBehavior: Boto3ClientError
    IllegalUpdate: Boto3ClientError
    InconsistentQuantities: Boto3ClientError
    InvalidArgument: Boto3ClientError
    InvalidDefaultRootObject: Boto3ClientError
    InvalidErrorCode: Boto3ClientError
    InvalidForwardCookies: Boto3ClientError
    InvalidGeoRestrictionParameter: Boto3ClientError
    InvalidHeadersForS3Origin: Boto3ClientError
    InvalidIfMatchVersion: Boto3ClientError
    InvalidLambdaFunctionAssociation: Boto3ClientError
    InvalidLocationCode: Boto3ClientError
    InvalidMinimumProtocolVersion: Boto3ClientError
    InvalidOrigin: Boto3ClientError
    InvalidOriginAccessIdentity: Boto3ClientError
    InvalidOriginKeepaliveTimeout: Boto3ClientError
    InvalidOriginReadTimeout: Boto3ClientError
    InvalidProtocolSettings: Boto3ClientError
    InvalidQueryStringParameters: Boto3ClientError
    InvalidRelativePath: Boto3ClientError
    InvalidRequiredProtocol: Boto3ClientError
    InvalidResponseCode: Boto3ClientError
    InvalidTTLOrder: Boto3ClientError
    InvalidTagging: Boto3ClientError
    InvalidViewerCertificate: Boto3ClientError
    InvalidWebACLId: Boto3ClientError
    MissingBody: Boto3ClientError
    NoSuchCloudFrontOriginAccessIdentity: Boto3ClientError
    NoSuchDistribution: Boto3ClientError
    NoSuchFieldLevelEncryptionConfig: Boto3ClientError
    NoSuchFieldLevelEncryptionProfile: Boto3ClientError
    NoSuchInvalidation: Boto3ClientError
    NoSuchOrigin: Boto3ClientError
    NoSuchPublicKey: Boto3ClientError
    NoSuchResource: Boto3ClientError
    NoSuchStreamingDistribution: Boto3ClientError
    PreconditionFailed: Boto3ClientError
    PublicKeyAlreadyExists: Boto3ClientError
    PublicKeyInUse: Boto3ClientError
    QueryArgProfileEmpty: Boto3ClientError
    StreamingDistributionAlreadyExists: Boto3ClientError
    StreamingDistributionNotDisabled: Boto3ClientError
    TooManyCacheBehaviors: Boto3ClientError
    TooManyCertificates: Boto3ClientError
    TooManyCloudFrontOriginAccessIdentities: Boto3ClientError
    TooManyCookieNamesInWhiteList: Boto3ClientError
    TooManyDistributionCNAMEs: Boto3ClientError
    TooManyDistributions: Boto3ClientError
    TooManyDistributionsAssociatedToFieldLevelEncryptionConfig: Boto3ClientError
    TooManyDistributionsWithLambdaAssociations: Boto3ClientError
    TooManyFieldLevelEncryptionConfigs: Boto3ClientError
    TooManyFieldLevelEncryptionContentTypeProfiles: Boto3ClientError
    TooManyFieldLevelEncryptionEncryptionEntities: Boto3ClientError
    TooManyFieldLevelEncryptionFieldPatterns: Boto3ClientError
    TooManyFieldLevelEncryptionProfiles: Boto3ClientError
    TooManyFieldLevelEncryptionQueryArgProfiles: Boto3ClientError
    TooManyHeadersInForwardedValues: Boto3ClientError
    TooManyInvalidationsInProgress: Boto3ClientError
    TooManyLambdaFunctionAssociations: Boto3ClientError
    TooManyOriginCustomHeaders: Boto3ClientError
    TooManyOriginGroupsPerDistribution: Boto3ClientError
    TooManyOrigins: Boto3ClientError
    TooManyPublicKeys: Boto3ClientError
    TooManyQueryStringParameters: Boto3ClientError
    TooManyStreamingDistributionCNAMEs: Boto3ClientError
    TooManyStreamingDistributions: Boto3ClientError
    TooManyTrustedSigners: Boto3ClientError
    TrustedSignerDoesNotExist: Boto3ClientError


class CloudFrontClient:
    """
    [CloudFront.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client)
    """

    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.can_paginate)
        """

    def create_cloud_front_origin_access_identity(
        self, CloudFrontOriginAccessIdentityConfig: CloudFrontOriginAccessIdentityConfigTypeDef
    ) -> CreateCloudFrontOriginAccessIdentityResultTypeDef:
        """
        [Client.create_cloud_front_origin_access_identity documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.create_cloud_front_origin_access_identity)
        """

    def create_distribution(
        self, DistributionConfig: DistributionConfigTypeDef
    ) -> CreateDistributionResultTypeDef:
        """
        [Client.create_distribution documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.create_distribution)
        """

    def create_distribution_with_tags(
        self, DistributionConfigWithTags: DistributionConfigWithTagsTypeDef
    ) -> CreateDistributionWithTagsResultTypeDef:
        """
        [Client.create_distribution_with_tags documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.create_distribution_with_tags)
        """

    def create_field_level_encryption_config(
        self, FieldLevelEncryptionConfig: FieldLevelEncryptionConfigTypeDef
    ) -> CreateFieldLevelEncryptionConfigResultTypeDef:
        """
        [Client.create_field_level_encryption_config documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.create_field_level_encryption_config)
        """

    def create_field_level_encryption_profile(
        self, FieldLevelEncryptionProfileConfig: FieldLevelEncryptionProfileConfigTypeDef
    ) -> CreateFieldLevelEncryptionProfileResultTypeDef:
        """
        [Client.create_field_level_encryption_profile documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.create_field_level_encryption_profile)
        """

    def create_invalidation(
        self, DistributionId: str, InvalidationBatch: InvalidationBatchTypeDef
    ) -> CreateInvalidationResultTypeDef:
        """
        [Client.create_invalidation documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.create_invalidation)
        """

    def create_public_key(
        self, PublicKeyConfig: PublicKeyConfigTypeDef
    ) -> CreatePublicKeyResultTypeDef:
        """
        [Client.create_public_key documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.create_public_key)
        """

    def create_streaming_distribution(
        self, StreamingDistributionConfig: StreamingDistributionConfigTypeDef
    ) -> CreateStreamingDistributionResultTypeDef:
        """
        [Client.create_streaming_distribution documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.create_streaming_distribution)
        """

    def create_streaming_distribution_with_tags(
        self, StreamingDistributionConfigWithTags: StreamingDistributionConfigWithTagsTypeDef
    ) -> CreateStreamingDistributionWithTagsResultTypeDef:
        """
        [Client.create_streaming_distribution_with_tags documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.create_streaming_distribution_with_tags)
        """

    def delete_cloud_front_origin_access_identity(self, Id: str, IfMatch: str = None) -> None:
        """
        [Client.delete_cloud_front_origin_access_identity documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.delete_cloud_front_origin_access_identity)
        """

    def delete_distribution(self, Id: str, IfMatch: str = None) -> None:
        """
        [Client.delete_distribution documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.delete_distribution)
        """

    def delete_field_level_encryption_config(self, Id: str, IfMatch: str = None) -> None:
        """
        [Client.delete_field_level_encryption_config documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.delete_field_level_encryption_config)
        """

    def delete_field_level_encryption_profile(self, Id: str, IfMatch: str = None) -> None:
        """
        [Client.delete_field_level_encryption_profile documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.delete_field_level_encryption_profile)
        """

    def delete_public_key(self, Id: str, IfMatch: str = None) -> None:
        """
        [Client.delete_public_key documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.delete_public_key)
        """

    def delete_streaming_distribution(self, Id: str, IfMatch: str = None) -> None:
        """
        [Client.delete_streaming_distribution documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.delete_streaming_distribution)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.generate_presigned_url)
        """

    def get_cloud_front_origin_access_identity(
        self, Id: str
    ) -> GetCloudFrontOriginAccessIdentityResultTypeDef:
        """
        [Client.get_cloud_front_origin_access_identity documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.get_cloud_front_origin_access_identity)
        """

    def get_cloud_front_origin_access_identity_config(
        self, Id: str
    ) -> GetCloudFrontOriginAccessIdentityConfigResultTypeDef:
        """
        [Client.get_cloud_front_origin_access_identity_config documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.get_cloud_front_origin_access_identity_config)
        """

    def get_distribution(self, Id: str) -> GetDistributionResultTypeDef:
        """
        [Client.get_distribution documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.get_distribution)
        """

    def get_distribution_config(self, Id: str) -> GetDistributionConfigResultTypeDef:
        """
        [Client.get_distribution_config documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.get_distribution_config)
        """

    def get_field_level_encryption(self, Id: str) -> GetFieldLevelEncryptionResultTypeDef:
        """
        [Client.get_field_level_encryption documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.get_field_level_encryption)
        """

    def get_field_level_encryption_config(
        self, Id: str
    ) -> GetFieldLevelEncryptionConfigResultTypeDef:
        """
        [Client.get_field_level_encryption_config documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.get_field_level_encryption_config)
        """

    def get_field_level_encryption_profile(
        self, Id: str
    ) -> GetFieldLevelEncryptionProfileResultTypeDef:
        """
        [Client.get_field_level_encryption_profile documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.get_field_level_encryption_profile)
        """

    def get_field_level_encryption_profile_config(
        self, Id: str
    ) -> GetFieldLevelEncryptionProfileConfigResultTypeDef:
        """
        [Client.get_field_level_encryption_profile_config documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.get_field_level_encryption_profile_config)
        """

    def get_invalidation(self, DistributionId: str, Id: str) -> GetInvalidationResultTypeDef:
        """
        [Client.get_invalidation documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.get_invalidation)
        """

    def get_public_key(self, Id: str) -> GetPublicKeyResultTypeDef:
        """
        [Client.get_public_key documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.get_public_key)
        """

    def get_public_key_config(self, Id: str) -> GetPublicKeyConfigResultTypeDef:
        """
        [Client.get_public_key_config documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.get_public_key_config)
        """

    def get_streaming_distribution(self, Id: str) -> GetStreamingDistributionResultTypeDef:
        """
        [Client.get_streaming_distribution documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.get_streaming_distribution)
        """

    def get_streaming_distribution_config(
        self, Id: str
    ) -> GetStreamingDistributionConfigResultTypeDef:
        """
        [Client.get_streaming_distribution_config documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.get_streaming_distribution_config)
        """

    def list_cloud_front_origin_access_identities(
        self, Marker: str = None, MaxItems: str = None
    ) -> ListCloudFrontOriginAccessIdentitiesResultTypeDef:
        """
        [Client.list_cloud_front_origin_access_identities documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.list_cloud_front_origin_access_identities)
        """

    def list_distributions(
        self, Marker: str = None, MaxItems: str = None
    ) -> ListDistributionsResultTypeDef:
        """
        [Client.list_distributions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.list_distributions)
        """

    def list_distributions_by_web_acl_id(
        self, WebACLId: str, Marker: str = None, MaxItems: str = None
    ) -> ListDistributionsByWebACLIdResultTypeDef:
        """
        [Client.list_distributions_by_web_acl_id documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.list_distributions_by_web_acl_id)
        """

    def list_field_level_encryption_configs(
        self, Marker: str = None, MaxItems: str = None
    ) -> ListFieldLevelEncryptionConfigsResultTypeDef:
        """
        [Client.list_field_level_encryption_configs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.list_field_level_encryption_configs)
        """

    def list_field_level_encryption_profiles(
        self, Marker: str = None, MaxItems: str = None
    ) -> ListFieldLevelEncryptionProfilesResultTypeDef:
        """
        [Client.list_field_level_encryption_profiles documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.list_field_level_encryption_profiles)
        """

    def list_invalidations(
        self, DistributionId: str, Marker: str = None, MaxItems: str = None
    ) -> ListInvalidationsResultTypeDef:
        """
        [Client.list_invalidations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.list_invalidations)
        """

    def list_public_keys(
        self, Marker: str = None, MaxItems: str = None
    ) -> ListPublicKeysResultTypeDef:
        """
        [Client.list_public_keys documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.list_public_keys)
        """

    def list_streaming_distributions(
        self, Marker: str = None, MaxItems: str = None
    ) -> ListStreamingDistributionsResultTypeDef:
        """
        [Client.list_streaming_distributions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.list_streaming_distributions)
        """

    def list_tags_for_resource(self, Resource: str) -> ListTagsForResourceResultTypeDef:
        """
        [Client.list_tags_for_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.list_tags_for_resource)
        """

    def tag_resource(self, Resource: str, Tags: TagsTypeDef) -> None:
        """
        [Client.tag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.tag_resource)
        """

    def untag_resource(self, Resource: str, TagKeys: TagKeysTypeDef) -> None:
        """
        [Client.untag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.untag_resource)
        """

    def update_cloud_front_origin_access_identity(
        self,
        CloudFrontOriginAccessIdentityConfig: CloudFrontOriginAccessIdentityConfigTypeDef,
        Id: str,
        IfMatch: str = None,
    ) -> UpdateCloudFrontOriginAccessIdentityResultTypeDef:
        """
        [Client.update_cloud_front_origin_access_identity documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.update_cloud_front_origin_access_identity)
        """

    def update_distribution(
        self, DistributionConfig: DistributionConfigTypeDef, Id: str, IfMatch: str = None
    ) -> UpdateDistributionResultTypeDef:
        """
        [Client.update_distribution documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.update_distribution)
        """

    def update_field_level_encryption_config(
        self,
        FieldLevelEncryptionConfig: FieldLevelEncryptionConfigTypeDef,
        Id: str,
        IfMatch: str = None,
    ) -> UpdateFieldLevelEncryptionConfigResultTypeDef:
        """
        [Client.update_field_level_encryption_config documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.update_field_level_encryption_config)
        """

    def update_field_level_encryption_profile(
        self,
        FieldLevelEncryptionProfileConfig: FieldLevelEncryptionProfileConfigTypeDef,
        Id: str,
        IfMatch: str = None,
    ) -> UpdateFieldLevelEncryptionProfileResultTypeDef:
        """
        [Client.update_field_level_encryption_profile documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.update_field_level_encryption_profile)
        """

    def update_public_key(
        self, PublicKeyConfig: PublicKeyConfigTypeDef, Id: str, IfMatch: str = None
    ) -> UpdatePublicKeyResultTypeDef:
        """
        [Client.update_public_key documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.update_public_key)
        """

    def update_streaming_distribution(
        self,
        StreamingDistributionConfig: StreamingDistributionConfigTypeDef,
        Id: str,
        IfMatch: str = None,
    ) -> UpdateStreamingDistributionResultTypeDef:
        """
        [Client.update_streaming_distribution documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Client.update_streaming_distribution)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_cloud_front_origin_access_identities"]
    ) -> ListCloudFrontOriginAccessIdentitiesPaginator:
        """
        [Paginator.ListCloudFrontOriginAccessIdentities documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Paginator.ListCloudFrontOriginAccessIdentities)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_distributions"]
    ) -> ListDistributionsPaginator:
        """
        [Paginator.ListDistributions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Paginator.ListDistributions)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_invalidations"]
    ) -> ListInvalidationsPaginator:
        """
        [Paginator.ListInvalidations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Paginator.ListInvalidations)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_streaming_distributions"]
    ) -> ListStreamingDistributionsPaginator:
        """
        [Paginator.ListStreamingDistributions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Paginator.ListStreamingDistributions)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["distribution_deployed"]
    ) -> DistributionDeployedWaiter:
        """
        [Waiter.DistributionDeployed documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Waiter.DistributionDeployed)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["invalidation_completed"]
    ) -> InvalidationCompletedWaiter:
        """
        [Waiter.InvalidationCompleted documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Waiter.InvalidationCompleted)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["streaming_distribution_deployed"]
    ) -> StreamingDistributionDeployedWaiter:
        """
        [Waiter.StreamingDistributionDeployed documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.28/reference/services/cloudfront.html#CloudFront.Waiter.StreamingDistributionDeployed)
        """
