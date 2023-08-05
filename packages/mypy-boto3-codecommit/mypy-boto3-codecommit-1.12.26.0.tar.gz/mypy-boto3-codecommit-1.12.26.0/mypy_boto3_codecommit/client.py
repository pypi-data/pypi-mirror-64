"""
Main interface for codecommit service client

Usage::

    import boto3
    from mypy_boto3.codecommit import CodeCommitClient

    session = boto3.Session()

    client: CodeCommitClient = boto3.client("codecommit")
    session_client: CodeCommitClient = session.client("codecommit")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
import sys
from typing import Any, Dict, IO, List, TYPE_CHECKING, Union, overload
from botocore.exceptions import ClientError as Boto3ClientError
from mypy_boto3_codecommit.paginator import (
    DescribePullRequestEventsPaginator,
    GetCommentsForComparedCommitPaginator,
    GetCommentsForPullRequestPaginator,
    GetDifferencesPaginator,
    ListBranchesPaginator,
    ListPullRequestsPaginator,
    ListRepositoriesPaginator,
)
from mypy_boto3_codecommit.type_defs import (
    BatchAssociateApprovalRuleTemplateWithRepositoriesOutputTypeDef,
    BatchDescribeMergeConflictsOutputTypeDef,
    BatchDisassociateApprovalRuleTemplateFromRepositoriesOutputTypeDef,
    BatchGetCommitsOutputTypeDef,
    BatchGetRepositoriesOutputTypeDef,
    ConflictResolutionTypeDef,
    CreateApprovalRuleTemplateOutputTypeDef,
    CreateCommitOutputTypeDef,
    CreatePullRequestApprovalRuleOutputTypeDef,
    CreatePullRequestOutputTypeDef,
    CreateRepositoryOutputTypeDef,
    CreateUnreferencedMergeCommitOutputTypeDef,
    DeleteApprovalRuleTemplateOutputTypeDef,
    DeleteBranchOutputTypeDef,
    DeleteCommentContentOutputTypeDef,
    DeleteFileEntryTypeDef,
    DeleteFileOutputTypeDef,
    DeletePullRequestApprovalRuleOutputTypeDef,
    DeleteRepositoryOutputTypeDef,
    DescribeMergeConflictsOutputTypeDef,
    DescribePullRequestEventsOutputTypeDef,
    EvaluatePullRequestApprovalRulesOutputTypeDef,
    GetApprovalRuleTemplateOutputTypeDef,
    GetBlobOutputTypeDef,
    GetBranchOutputTypeDef,
    GetCommentOutputTypeDef,
    GetCommentsForComparedCommitOutputTypeDef,
    GetCommentsForPullRequestOutputTypeDef,
    GetCommitOutputTypeDef,
    GetDifferencesOutputTypeDef,
    GetFileOutputTypeDef,
    GetFolderOutputTypeDef,
    GetMergeCommitOutputTypeDef,
    GetMergeConflictsOutputTypeDef,
    GetMergeOptionsOutputTypeDef,
    GetPullRequestApprovalStatesOutputTypeDef,
    GetPullRequestOutputTypeDef,
    GetPullRequestOverrideStateOutputTypeDef,
    GetRepositoryOutputTypeDef,
    GetRepositoryTriggersOutputTypeDef,
    ListApprovalRuleTemplatesOutputTypeDef,
    ListAssociatedApprovalRuleTemplatesForRepositoryOutputTypeDef,
    ListBranchesOutputTypeDef,
    ListPullRequestsOutputTypeDef,
    ListRepositoriesForApprovalRuleTemplateOutputTypeDef,
    ListRepositoriesOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    LocationTypeDef,
    MergeBranchesByFastForwardOutputTypeDef,
    MergeBranchesBySquashOutputTypeDef,
    MergeBranchesByThreeWayOutputTypeDef,
    MergePullRequestByFastForwardOutputTypeDef,
    MergePullRequestBySquashOutputTypeDef,
    MergePullRequestByThreeWayOutputTypeDef,
    PostCommentForComparedCommitOutputTypeDef,
    PostCommentForPullRequestOutputTypeDef,
    PostCommentReplyOutputTypeDef,
    PutFileEntryTypeDef,
    PutFileOutputTypeDef,
    PutRepositoryTriggersOutputTypeDef,
    RepositoryTriggerTypeDef,
    SetFileModeEntryTypeDef,
    TargetTypeDef,
    TestRepositoryTriggersOutputTypeDef,
    UpdateApprovalRuleTemplateContentOutputTypeDef,
    UpdateApprovalRuleTemplateDescriptionOutputTypeDef,
    UpdateApprovalRuleTemplateNameOutputTypeDef,
    UpdateCommentOutputTypeDef,
    UpdatePullRequestApprovalRuleContentOutputTypeDef,
    UpdatePullRequestDescriptionOutputTypeDef,
    UpdatePullRequestStatusOutputTypeDef,
    UpdatePullRequestTitleOutputTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("CodeCommitClient",)


class Exceptions:
    ActorDoesNotExistException: Boto3ClientError
    ApprovalRuleContentRequiredException: Boto3ClientError
    ApprovalRuleDoesNotExistException: Boto3ClientError
    ApprovalRuleNameAlreadyExistsException: Boto3ClientError
    ApprovalRuleNameRequiredException: Boto3ClientError
    ApprovalRuleTemplateContentRequiredException: Boto3ClientError
    ApprovalRuleTemplateDoesNotExistException: Boto3ClientError
    ApprovalRuleTemplateInUseException: Boto3ClientError
    ApprovalRuleTemplateNameAlreadyExistsException: Boto3ClientError
    ApprovalRuleTemplateNameRequiredException: Boto3ClientError
    ApprovalStateRequiredException: Boto3ClientError
    AuthorDoesNotExistException: Boto3ClientError
    BeforeCommitIdAndAfterCommitIdAreSameException: Boto3ClientError
    BlobIdDoesNotExistException: Boto3ClientError
    BlobIdRequiredException: Boto3ClientError
    BranchDoesNotExistException: Boto3ClientError
    BranchNameExistsException: Boto3ClientError
    BranchNameIsTagNameException: Boto3ClientError
    BranchNameRequiredException: Boto3ClientError
    CannotDeleteApprovalRuleFromTemplateException: Boto3ClientError
    CannotModifyApprovalRuleFromTemplateException: Boto3ClientError
    ClientError: Boto3ClientError
    ClientRequestTokenRequiredException: Boto3ClientError
    CommentContentRequiredException: Boto3ClientError
    CommentContentSizeLimitExceededException: Boto3ClientError
    CommentDeletedException: Boto3ClientError
    CommentDoesNotExistException: Boto3ClientError
    CommentIdRequiredException: Boto3ClientError
    CommentNotCreatedByCallerException: Boto3ClientError
    CommitDoesNotExistException: Boto3ClientError
    CommitIdDoesNotExistException: Boto3ClientError
    CommitIdRequiredException: Boto3ClientError
    CommitIdsLimitExceededException: Boto3ClientError
    CommitIdsListRequiredException: Boto3ClientError
    CommitMessageLengthExceededException: Boto3ClientError
    CommitRequiredException: Boto3ClientError
    ConcurrentReferenceUpdateException: Boto3ClientError
    DefaultBranchCannotBeDeletedException: Boto3ClientError
    DirectoryNameConflictsWithFileNameException: Boto3ClientError
    EncryptionIntegrityChecksFailedException: Boto3ClientError
    EncryptionKeyAccessDeniedException: Boto3ClientError
    EncryptionKeyDisabledException: Boto3ClientError
    EncryptionKeyNotFoundException: Boto3ClientError
    EncryptionKeyUnavailableException: Boto3ClientError
    FileContentAndSourceFileSpecifiedException: Boto3ClientError
    FileContentRequiredException: Boto3ClientError
    FileContentSizeLimitExceededException: Boto3ClientError
    FileDoesNotExistException: Boto3ClientError
    FileEntryRequiredException: Boto3ClientError
    FileModeRequiredException: Boto3ClientError
    FileNameConflictsWithDirectoryNameException: Boto3ClientError
    FilePathConflictsWithSubmodulePathException: Boto3ClientError
    FileTooLargeException: Boto3ClientError
    FolderContentSizeLimitExceededException: Boto3ClientError
    FolderDoesNotExistException: Boto3ClientError
    IdempotencyParameterMismatchException: Boto3ClientError
    InvalidActorArnException: Boto3ClientError
    InvalidApprovalRuleContentException: Boto3ClientError
    InvalidApprovalRuleNameException: Boto3ClientError
    InvalidApprovalRuleTemplateContentException: Boto3ClientError
    InvalidApprovalRuleTemplateDescriptionException: Boto3ClientError
    InvalidApprovalRuleTemplateNameException: Boto3ClientError
    InvalidApprovalStateException: Boto3ClientError
    InvalidAuthorArnException: Boto3ClientError
    InvalidBlobIdException: Boto3ClientError
    InvalidBranchNameException: Boto3ClientError
    InvalidClientRequestTokenException: Boto3ClientError
    InvalidCommentIdException: Boto3ClientError
    InvalidCommitException: Boto3ClientError
    InvalidCommitIdException: Boto3ClientError
    InvalidConflictDetailLevelException: Boto3ClientError
    InvalidConflictResolutionException: Boto3ClientError
    InvalidConflictResolutionStrategyException: Boto3ClientError
    InvalidContinuationTokenException: Boto3ClientError
    InvalidDeletionParameterException: Boto3ClientError
    InvalidDescriptionException: Boto3ClientError
    InvalidDestinationCommitSpecifierException: Boto3ClientError
    InvalidEmailException: Boto3ClientError
    InvalidFileLocationException: Boto3ClientError
    InvalidFileModeException: Boto3ClientError
    InvalidFilePositionException: Boto3ClientError
    InvalidMaxConflictFilesException: Boto3ClientError
    InvalidMaxMergeHunksException: Boto3ClientError
    InvalidMaxResultsException: Boto3ClientError
    InvalidMergeOptionException: Boto3ClientError
    InvalidOrderException: Boto3ClientError
    InvalidOverrideStatusException: Boto3ClientError
    InvalidParentCommitIdException: Boto3ClientError
    InvalidPathException: Boto3ClientError
    InvalidPullRequestEventTypeException: Boto3ClientError
    InvalidPullRequestIdException: Boto3ClientError
    InvalidPullRequestStatusException: Boto3ClientError
    InvalidPullRequestStatusUpdateException: Boto3ClientError
    InvalidReferenceNameException: Boto3ClientError
    InvalidRelativeFileVersionEnumException: Boto3ClientError
    InvalidReplacementContentException: Boto3ClientError
    InvalidReplacementTypeException: Boto3ClientError
    InvalidRepositoryDescriptionException: Boto3ClientError
    InvalidRepositoryNameException: Boto3ClientError
    InvalidRepositoryTriggerBranchNameException: Boto3ClientError
    InvalidRepositoryTriggerCustomDataException: Boto3ClientError
    InvalidRepositoryTriggerDestinationArnException: Boto3ClientError
    InvalidRepositoryTriggerEventsException: Boto3ClientError
    InvalidRepositoryTriggerNameException: Boto3ClientError
    InvalidRepositoryTriggerRegionException: Boto3ClientError
    InvalidResourceArnException: Boto3ClientError
    InvalidRevisionIdException: Boto3ClientError
    InvalidRuleContentSha256Exception: Boto3ClientError
    InvalidSortByException: Boto3ClientError
    InvalidSourceCommitSpecifierException: Boto3ClientError
    InvalidSystemTagUsageException: Boto3ClientError
    InvalidTagKeysListException: Boto3ClientError
    InvalidTagsMapException: Boto3ClientError
    InvalidTargetBranchException: Boto3ClientError
    InvalidTargetException: Boto3ClientError
    InvalidTargetsException: Boto3ClientError
    InvalidTitleException: Boto3ClientError
    ManualMergeRequiredException: Boto3ClientError
    MaximumBranchesExceededException: Boto3ClientError
    MaximumConflictResolutionEntriesExceededException: Boto3ClientError
    MaximumFileContentToLoadExceededException: Boto3ClientError
    MaximumFileEntriesExceededException: Boto3ClientError
    MaximumItemsToCompareExceededException: Boto3ClientError
    MaximumNumberOfApprovalsExceededException: Boto3ClientError
    MaximumOpenPullRequestsExceededException: Boto3ClientError
    MaximumRepositoryNamesExceededException: Boto3ClientError
    MaximumRepositoryTriggersExceededException: Boto3ClientError
    MaximumRuleTemplatesAssociatedWithRepositoryException: Boto3ClientError
    MergeOptionRequiredException: Boto3ClientError
    MultipleConflictResolutionEntriesException: Boto3ClientError
    MultipleRepositoriesInPullRequestException: Boto3ClientError
    NameLengthExceededException: Boto3ClientError
    NoChangeException: Boto3ClientError
    NumberOfRuleTemplatesExceededException: Boto3ClientError
    NumberOfRulesExceededException: Boto3ClientError
    OverrideAlreadySetException: Boto3ClientError
    OverrideStatusRequiredException: Boto3ClientError
    ParentCommitDoesNotExistException: Boto3ClientError
    ParentCommitIdOutdatedException: Boto3ClientError
    ParentCommitIdRequiredException: Boto3ClientError
    PathDoesNotExistException: Boto3ClientError
    PathRequiredException: Boto3ClientError
    PullRequestAlreadyClosedException: Boto3ClientError
    PullRequestApprovalRulesNotSatisfiedException: Boto3ClientError
    PullRequestCannotBeApprovedByAuthorException: Boto3ClientError
    PullRequestDoesNotExistException: Boto3ClientError
    PullRequestIdRequiredException: Boto3ClientError
    PullRequestStatusRequiredException: Boto3ClientError
    PutFileEntryConflictException: Boto3ClientError
    ReferenceDoesNotExistException: Boto3ClientError
    ReferenceNameRequiredException: Boto3ClientError
    ReferenceTypeNotSupportedException: Boto3ClientError
    ReplacementContentRequiredException: Boto3ClientError
    ReplacementTypeRequiredException: Boto3ClientError
    RepositoryDoesNotExistException: Boto3ClientError
    RepositoryLimitExceededException: Boto3ClientError
    RepositoryNameExistsException: Boto3ClientError
    RepositoryNameRequiredException: Boto3ClientError
    RepositoryNamesRequiredException: Boto3ClientError
    RepositoryNotAssociatedWithPullRequestException: Boto3ClientError
    RepositoryTriggerBranchNameListRequiredException: Boto3ClientError
    RepositoryTriggerDestinationArnRequiredException: Boto3ClientError
    RepositoryTriggerEventsListRequiredException: Boto3ClientError
    RepositoryTriggerNameRequiredException: Boto3ClientError
    RepositoryTriggersListRequiredException: Boto3ClientError
    ResourceArnRequiredException: Boto3ClientError
    RestrictedSourceFileException: Boto3ClientError
    RevisionIdRequiredException: Boto3ClientError
    RevisionNotCurrentException: Boto3ClientError
    SameFileContentException: Boto3ClientError
    SamePathRequestException: Boto3ClientError
    SourceAndDestinationAreSameException: Boto3ClientError
    SourceFileOrContentRequiredException: Boto3ClientError
    TagKeysListRequiredException: Boto3ClientError
    TagPolicyException: Boto3ClientError
    TagsMapRequiredException: Boto3ClientError
    TargetRequiredException: Boto3ClientError
    TargetsRequiredException: Boto3ClientError
    TipOfSourceReferenceIsDifferentException: Boto3ClientError
    TipsDivergenceExceededException: Boto3ClientError
    TitleRequiredException: Boto3ClientError
    TooManyTagsException: Boto3ClientError


class CodeCommitClient:
    """
    [CodeCommit.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client)
    """

    exceptions: Exceptions

    def associate_approval_rule_template_with_repository(
        self, approvalRuleTemplateName: str, repositoryName: str
    ) -> None:
        """
        [Client.associate_approval_rule_template_with_repository documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.associate_approval_rule_template_with_repository)
        """

    def batch_associate_approval_rule_template_with_repositories(
        self, approvalRuleTemplateName: str, repositoryNames: List[str]
    ) -> BatchAssociateApprovalRuleTemplateWithRepositoriesOutputTypeDef:
        """
        [Client.batch_associate_approval_rule_template_with_repositories documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.batch_associate_approval_rule_template_with_repositories)
        """

    def batch_describe_merge_conflicts(
        self,
        repositoryName: str,
        destinationCommitSpecifier: str,
        sourceCommitSpecifier: str,
        mergeOption: Literal["FAST_FORWARD_MERGE", "SQUASH_MERGE", "THREE_WAY_MERGE"],
        maxMergeHunks: int = None,
        maxConflictFiles: int = None,
        filePaths: List[str] = None,
        conflictDetailLevel: Literal["FILE_LEVEL", "LINE_LEVEL"] = None,
        conflictResolutionStrategy: Literal[
            "NONE", "ACCEPT_SOURCE", "ACCEPT_DESTINATION", "AUTOMERGE"
        ] = None,
        nextToken: str = None,
    ) -> BatchDescribeMergeConflictsOutputTypeDef:
        """
        [Client.batch_describe_merge_conflicts documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.batch_describe_merge_conflicts)
        """

    def batch_disassociate_approval_rule_template_from_repositories(
        self, approvalRuleTemplateName: str, repositoryNames: List[str]
    ) -> BatchDisassociateApprovalRuleTemplateFromRepositoriesOutputTypeDef:
        """
        [Client.batch_disassociate_approval_rule_template_from_repositories documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.batch_disassociate_approval_rule_template_from_repositories)
        """

    def batch_get_commits(
        self, commitIds: List[str], repositoryName: str
    ) -> BatchGetCommitsOutputTypeDef:
        """
        [Client.batch_get_commits documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.batch_get_commits)
        """

    def batch_get_repositories(
        self, repositoryNames: List[str]
    ) -> BatchGetRepositoriesOutputTypeDef:
        """
        [Client.batch_get_repositories documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.batch_get_repositories)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.can_paginate)
        """

    def create_approval_rule_template(
        self,
        approvalRuleTemplateName: str,
        approvalRuleTemplateContent: str,
        approvalRuleTemplateDescription: str = None,
    ) -> CreateApprovalRuleTemplateOutputTypeDef:
        """
        [Client.create_approval_rule_template documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.create_approval_rule_template)
        """

    def create_branch(self, repositoryName: str, branchName: str, commitId: str) -> None:
        """
        [Client.create_branch documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.create_branch)
        """

    def create_commit(
        self,
        repositoryName: str,
        branchName: str,
        parentCommitId: str = None,
        authorName: str = None,
        email: str = None,
        commitMessage: str = None,
        keepEmptyFolders: bool = None,
        putFiles: List[PutFileEntryTypeDef] = None,
        deleteFiles: List[DeleteFileEntryTypeDef] = None,
        setFileModes: List[SetFileModeEntryTypeDef] = None,
    ) -> CreateCommitOutputTypeDef:
        """
        [Client.create_commit documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.create_commit)
        """

    def create_pull_request(
        self,
        title: str,
        targets: List[TargetTypeDef],
        description: str = None,
        clientRequestToken: str = None,
    ) -> CreatePullRequestOutputTypeDef:
        """
        [Client.create_pull_request documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.create_pull_request)
        """

    def create_pull_request_approval_rule(
        self, pullRequestId: str, approvalRuleName: str, approvalRuleContent: str
    ) -> CreatePullRequestApprovalRuleOutputTypeDef:
        """
        [Client.create_pull_request_approval_rule documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.create_pull_request_approval_rule)
        """

    def create_repository(
        self, repositoryName: str, repositoryDescription: str = None, tags: Dict[str, str] = None
    ) -> CreateRepositoryOutputTypeDef:
        """
        [Client.create_repository documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.create_repository)
        """

    def create_unreferenced_merge_commit(
        self,
        repositoryName: str,
        sourceCommitSpecifier: str,
        destinationCommitSpecifier: str,
        mergeOption: Literal["FAST_FORWARD_MERGE", "SQUASH_MERGE", "THREE_WAY_MERGE"],
        conflictDetailLevel: Literal["FILE_LEVEL", "LINE_LEVEL"] = None,
        conflictResolutionStrategy: Literal[
            "NONE", "ACCEPT_SOURCE", "ACCEPT_DESTINATION", "AUTOMERGE"
        ] = None,
        authorName: str = None,
        email: str = None,
        commitMessage: str = None,
        keepEmptyFolders: bool = None,
        conflictResolution: ConflictResolutionTypeDef = None,
    ) -> CreateUnreferencedMergeCommitOutputTypeDef:
        """
        [Client.create_unreferenced_merge_commit documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.create_unreferenced_merge_commit)
        """

    def delete_approval_rule_template(
        self, approvalRuleTemplateName: str
    ) -> DeleteApprovalRuleTemplateOutputTypeDef:
        """
        [Client.delete_approval_rule_template documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.delete_approval_rule_template)
        """

    def delete_branch(self, repositoryName: str, branchName: str) -> DeleteBranchOutputTypeDef:
        """
        [Client.delete_branch documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.delete_branch)
        """

    def delete_comment_content(self, commentId: str) -> DeleteCommentContentOutputTypeDef:
        """
        [Client.delete_comment_content documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.delete_comment_content)
        """

    def delete_file(
        self,
        repositoryName: str,
        branchName: str,
        filePath: str,
        parentCommitId: str,
        keepEmptyFolders: bool = None,
        commitMessage: str = None,
        name: str = None,
        email: str = None,
    ) -> DeleteFileOutputTypeDef:
        """
        [Client.delete_file documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.delete_file)
        """

    def delete_pull_request_approval_rule(
        self, pullRequestId: str, approvalRuleName: str
    ) -> DeletePullRequestApprovalRuleOutputTypeDef:
        """
        [Client.delete_pull_request_approval_rule documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.delete_pull_request_approval_rule)
        """

    def delete_repository(self, repositoryName: str) -> DeleteRepositoryOutputTypeDef:
        """
        [Client.delete_repository documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.delete_repository)
        """

    def describe_merge_conflicts(
        self,
        repositoryName: str,
        destinationCommitSpecifier: str,
        sourceCommitSpecifier: str,
        mergeOption: Literal["FAST_FORWARD_MERGE", "SQUASH_MERGE", "THREE_WAY_MERGE"],
        filePath: str,
        maxMergeHunks: int = None,
        conflictDetailLevel: Literal["FILE_LEVEL", "LINE_LEVEL"] = None,
        conflictResolutionStrategy: Literal[
            "NONE", "ACCEPT_SOURCE", "ACCEPT_DESTINATION", "AUTOMERGE"
        ] = None,
        nextToken: str = None,
    ) -> DescribeMergeConflictsOutputTypeDef:
        """
        [Client.describe_merge_conflicts documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.describe_merge_conflicts)
        """

    def describe_pull_request_events(
        self,
        pullRequestId: str,
        pullRequestEventType: Literal[
            "PULL_REQUEST_CREATED",
            "PULL_REQUEST_STATUS_CHANGED",
            "PULL_REQUEST_SOURCE_REFERENCE_UPDATED",
            "PULL_REQUEST_MERGE_STATE_CHANGED",
            "PULL_REQUEST_APPROVAL_RULE_CREATED",
            "PULL_REQUEST_APPROVAL_RULE_UPDATED",
            "PULL_REQUEST_APPROVAL_RULE_DELETED",
            "PULL_REQUEST_APPROVAL_RULE_OVERRIDDEN",
            "PULL_REQUEST_APPROVAL_STATE_CHANGED",
        ] = None,
        actorArn: str = None,
        nextToken: str = None,
        maxResults: int = None,
    ) -> DescribePullRequestEventsOutputTypeDef:
        """
        [Client.describe_pull_request_events documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.describe_pull_request_events)
        """

    def disassociate_approval_rule_template_from_repository(
        self, approvalRuleTemplateName: str, repositoryName: str
    ) -> None:
        """
        [Client.disassociate_approval_rule_template_from_repository documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.disassociate_approval_rule_template_from_repository)
        """

    def evaluate_pull_request_approval_rules(
        self, pullRequestId: str, revisionId: str
    ) -> EvaluatePullRequestApprovalRulesOutputTypeDef:
        """
        [Client.evaluate_pull_request_approval_rules documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.evaluate_pull_request_approval_rules)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.generate_presigned_url)
        """

    def get_approval_rule_template(
        self, approvalRuleTemplateName: str
    ) -> GetApprovalRuleTemplateOutputTypeDef:
        """
        [Client.get_approval_rule_template documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.get_approval_rule_template)
        """

    def get_blob(self, repositoryName: str, blobId: str) -> GetBlobOutputTypeDef:
        """
        [Client.get_blob documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.get_blob)
        """

    def get_branch(
        self, repositoryName: str = None, branchName: str = None
    ) -> GetBranchOutputTypeDef:
        """
        [Client.get_branch documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.get_branch)
        """

    def get_comment(self, commentId: str) -> GetCommentOutputTypeDef:
        """
        [Client.get_comment documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.get_comment)
        """

    def get_comments_for_compared_commit(
        self,
        repositoryName: str,
        afterCommitId: str,
        beforeCommitId: str = None,
        nextToken: str = None,
        maxResults: int = None,
    ) -> GetCommentsForComparedCommitOutputTypeDef:
        """
        [Client.get_comments_for_compared_commit documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.get_comments_for_compared_commit)
        """

    def get_comments_for_pull_request(
        self,
        pullRequestId: str,
        repositoryName: str = None,
        beforeCommitId: str = None,
        afterCommitId: str = None,
        nextToken: str = None,
        maxResults: int = None,
    ) -> GetCommentsForPullRequestOutputTypeDef:
        """
        [Client.get_comments_for_pull_request documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.get_comments_for_pull_request)
        """

    def get_commit(self, repositoryName: str, commitId: str) -> GetCommitOutputTypeDef:
        """
        [Client.get_commit documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.get_commit)
        """

    def get_differences(
        self,
        repositoryName: str,
        afterCommitSpecifier: str,
        beforeCommitSpecifier: str = None,
        beforePath: str = None,
        afterPath: str = None,
        MaxResults: int = None,
        NextToken: str = None,
    ) -> GetDifferencesOutputTypeDef:
        """
        [Client.get_differences documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.get_differences)
        """

    def get_file(
        self, repositoryName: str, filePath: str, commitSpecifier: str = None
    ) -> GetFileOutputTypeDef:
        """
        [Client.get_file documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.get_file)
        """

    def get_folder(
        self, repositoryName: str, folderPath: str, commitSpecifier: str = None
    ) -> GetFolderOutputTypeDef:
        """
        [Client.get_folder documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.get_folder)
        """

    def get_merge_commit(
        self,
        repositoryName: str,
        sourceCommitSpecifier: str,
        destinationCommitSpecifier: str,
        conflictDetailLevel: Literal["FILE_LEVEL", "LINE_LEVEL"] = None,
        conflictResolutionStrategy: Literal[
            "NONE", "ACCEPT_SOURCE", "ACCEPT_DESTINATION", "AUTOMERGE"
        ] = None,
    ) -> GetMergeCommitOutputTypeDef:
        """
        [Client.get_merge_commit documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.get_merge_commit)
        """

    def get_merge_conflicts(
        self,
        repositoryName: str,
        destinationCommitSpecifier: str,
        sourceCommitSpecifier: str,
        mergeOption: Literal["FAST_FORWARD_MERGE", "SQUASH_MERGE", "THREE_WAY_MERGE"],
        conflictDetailLevel: Literal["FILE_LEVEL", "LINE_LEVEL"] = None,
        maxConflictFiles: int = None,
        conflictResolutionStrategy: Literal[
            "NONE", "ACCEPT_SOURCE", "ACCEPT_DESTINATION", "AUTOMERGE"
        ] = None,
        nextToken: str = None,
    ) -> GetMergeConflictsOutputTypeDef:
        """
        [Client.get_merge_conflicts documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.get_merge_conflicts)
        """

    def get_merge_options(
        self,
        repositoryName: str,
        sourceCommitSpecifier: str,
        destinationCommitSpecifier: str,
        conflictDetailLevel: Literal["FILE_LEVEL", "LINE_LEVEL"] = None,
        conflictResolutionStrategy: Literal[
            "NONE", "ACCEPT_SOURCE", "ACCEPT_DESTINATION", "AUTOMERGE"
        ] = None,
    ) -> GetMergeOptionsOutputTypeDef:
        """
        [Client.get_merge_options documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.get_merge_options)
        """

    def get_pull_request(self, pullRequestId: str) -> GetPullRequestOutputTypeDef:
        """
        [Client.get_pull_request documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.get_pull_request)
        """

    def get_pull_request_approval_states(
        self, pullRequestId: str, revisionId: str
    ) -> GetPullRequestApprovalStatesOutputTypeDef:
        """
        [Client.get_pull_request_approval_states documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.get_pull_request_approval_states)
        """

    def get_pull_request_override_state(
        self, pullRequestId: str, revisionId: str
    ) -> GetPullRequestOverrideStateOutputTypeDef:
        """
        [Client.get_pull_request_override_state documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.get_pull_request_override_state)
        """

    def get_repository(self, repositoryName: str) -> GetRepositoryOutputTypeDef:
        """
        [Client.get_repository documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.get_repository)
        """

    def get_repository_triggers(self, repositoryName: str) -> GetRepositoryTriggersOutputTypeDef:
        """
        [Client.get_repository_triggers documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.get_repository_triggers)
        """

    def list_approval_rule_templates(
        self, nextToken: str = None, maxResults: int = None
    ) -> ListApprovalRuleTemplatesOutputTypeDef:
        """
        [Client.list_approval_rule_templates documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.list_approval_rule_templates)
        """

    def list_associated_approval_rule_templates_for_repository(
        self, repositoryName: str, nextToken: str = None, maxResults: int = None
    ) -> ListAssociatedApprovalRuleTemplatesForRepositoryOutputTypeDef:
        """
        [Client.list_associated_approval_rule_templates_for_repository documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.list_associated_approval_rule_templates_for_repository)
        """

    def list_branches(
        self, repositoryName: str, nextToken: str = None
    ) -> ListBranchesOutputTypeDef:
        """
        [Client.list_branches documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.list_branches)
        """

    def list_pull_requests(
        self,
        repositoryName: str,
        authorArn: str = None,
        pullRequestStatus: Literal["OPEN", "CLOSED"] = None,
        nextToken: str = None,
        maxResults: int = None,
    ) -> ListPullRequestsOutputTypeDef:
        """
        [Client.list_pull_requests documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.list_pull_requests)
        """

    def list_repositories(
        self,
        nextToken: str = None,
        sortBy: Literal["repositoryName", "lastModifiedDate"] = None,
        order: Literal["ascending", "descending"] = None,
    ) -> ListRepositoriesOutputTypeDef:
        """
        [Client.list_repositories documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.list_repositories)
        """

    def list_repositories_for_approval_rule_template(
        self, approvalRuleTemplateName: str, nextToken: str = None, maxResults: int = None
    ) -> ListRepositoriesForApprovalRuleTemplateOutputTypeDef:
        """
        [Client.list_repositories_for_approval_rule_template documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.list_repositories_for_approval_rule_template)
        """

    def list_tags_for_resource(
        self, resourceArn: str, nextToken: str = None
    ) -> ListTagsForResourceOutputTypeDef:
        """
        [Client.list_tags_for_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.list_tags_for_resource)
        """

    def merge_branches_by_fast_forward(
        self,
        repositoryName: str,
        sourceCommitSpecifier: str,
        destinationCommitSpecifier: str,
        targetBranch: str = None,
    ) -> MergeBranchesByFastForwardOutputTypeDef:
        """
        [Client.merge_branches_by_fast_forward documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.merge_branches_by_fast_forward)
        """

    def merge_branches_by_squash(
        self,
        repositoryName: str,
        sourceCommitSpecifier: str,
        destinationCommitSpecifier: str,
        targetBranch: str = None,
        conflictDetailLevel: Literal["FILE_LEVEL", "LINE_LEVEL"] = None,
        conflictResolutionStrategy: Literal[
            "NONE", "ACCEPT_SOURCE", "ACCEPT_DESTINATION", "AUTOMERGE"
        ] = None,
        authorName: str = None,
        email: str = None,
        commitMessage: str = None,
        keepEmptyFolders: bool = None,
        conflictResolution: ConflictResolutionTypeDef = None,
    ) -> MergeBranchesBySquashOutputTypeDef:
        """
        [Client.merge_branches_by_squash documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.merge_branches_by_squash)
        """

    def merge_branches_by_three_way(
        self,
        repositoryName: str,
        sourceCommitSpecifier: str,
        destinationCommitSpecifier: str,
        targetBranch: str = None,
        conflictDetailLevel: Literal["FILE_LEVEL", "LINE_LEVEL"] = None,
        conflictResolutionStrategy: Literal[
            "NONE", "ACCEPT_SOURCE", "ACCEPT_DESTINATION", "AUTOMERGE"
        ] = None,
        authorName: str = None,
        email: str = None,
        commitMessage: str = None,
        keepEmptyFolders: bool = None,
        conflictResolution: ConflictResolutionTypeDef = None,
    ) -> MergeBranchesByThreeWayOutputTypeDef:
        """
        [Client.merge_branches_by_three_way documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.merge_branches_by_three_way)
        """

    def merge_pull_request_by_fast_forward(
        self, pullRequestId: str, repositoryName: str, sourceCommitId: str = None
    ) -> MergePullRequestByFastForwardOutputTypeDef:
        """
        [Client.merge_pull_request_by_fast_forward documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.merge_pull_request_by_fast_forward)
        """

    def merge_pull_request_by_squash(
        self,
        pullRequestId: str,
        repositoryName: str,
        sourceCommitId: str = None,
        conflictDetailLevel: Literal["FILE_LEVEL", "LINE_LEVEL"] = None,
        conflictResolutionStrategy: Literal[
            "NONE", "ACCEPT_SOURCE", "ACCEPT_DESTINATION", "AUTOMERGE"
        ] = None,
        commitMessage: str = None,
        authorName: str = None,
        email: str = None,
        keepEmptyFolders: bool = None,
        conflictResolution: ConflictResolutionTypeDef = None,
    ) -> MergePullRequestBySquashOutputTypeDef:
        """
        [Client.merge_pull_request_by_squash documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.merge_pull_request_by_squash)
        """

    def merge_pull_request_by_three_way(
        self,
        pullRequestId: str,
        repositoryName: str,
        sourceCommitId: str = None,
        conflictDetailLevel: Literal["FILE_LEVEL", "LINE_LEVEL"] = None,
        conflictResolutionStrategy: Literal[
            "NONE", "ACCEPT_SOURCE", "ACCEPT_DESTINATION", "AUTOMERGE"
        ] = None,
        commitMessage: str = None,
        authorName: str = None,
        email: str = None,
        keepEmptyFolders: bool = None,
        conflictResolution: ConflictResolutionTypeDef = None,
    ) -> MergePullRequestByThreeWayOutputTypeDef:
        """
        [Client.merge_pull_request_by_three_way documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.merge_pull_request_by_three_way)
        """

    def override_pull_request_approval_rules(
        self, pullRequestId: str, revisionId: str, overrideStatus: Literal["OVERRIDE", "REVOKE"]
    ) -> None:
        """
        [Client.override_pull_request_approval_rules documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.override_pull_request_approval_rules)
        """

    def post_comment_for_compared_commit(
        self,
        repositoryName: str,
        afterCommitId: str,
        content: str,
        beforeCommitId: str = None,
        location: LocationTypeDef = None,
        clientRequestToken: str = None,
    ) -> PostCommentForComparedCommitOutputTypeDef:
        """
        [Client.post_comment_for_compared_commit documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.post_comment_for_compared_commit)
        """

    def post_comment_for_pull_request(
        self,
        pullRequestId: str,
        repositoryName: str,
        beforeCommitId: str,
        afterCommitId: str,
        content: str,
        location: LocationTypeDef = None,
        clientRequestToken: str = None,
    ) -> PostCommentForPullRequestOutputTypeDef:
        """
        [Client.post_comment_for_pull_request documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.post_comment_for_pull_request)
        """

    def post_comment_reply(
        self, inReplyTo: str, content: str, clientRequestToken: str = None
    ) -> PostCommentReplyOutputTypeDef:
        """
        [Client.post_comment_reply documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.post_comment_reply)
        """

    def put_file(
        self,
        repositoryName: str,
        branchName: str,
        fileContent: Union[bytes, IO],
        filePath: str,
        fileMode: Literal["EXECUTABLE", "NORMAL", "SYMLINK"] = None,
        parentCommitId: str = None,
        commitMessage: str = None,
        name: str = None,
        email: str = None,
    ) -> PutFileOutputTypeDef:
        """
        [Client.put_file documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.put_file)
        """

    def put_repository_triggers(
        self, repositoryName: str, triggers: List[RepositoryTriggerTypeDef]
    ) -> PutRepositoryTriggersOutputTypeDef:
        """
        [Client.put_repository_triggers documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.put_repository_triggers)
        """

    def tag_resource(self, resourceArn: str, tags: Dict[str, str]) -> None:
        """
        [Client.tag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.tag_resource)
        """

    def test_repository_triggers(
        self, repositoryName: str, triggers: List[RepositoryTriggerTypeDef]
    ) -> TestRepositoryTriggersOutputTypeDef:
        """
        [Client.test_repository_triggers documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.test_repository_triggers)
        """

    def untag_resource(self, resourceArn: str, tagKeys: List[str]) -> None:
        """
        [Client.untag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.untag_resource)
        """

    def update_approval_rule_template_content(
        self,
        approvalRuleTemplateName: str,
        newRuleContent: str,
        existingRuleContentSha256: str = None,
    ) -> UpdateApprovalRuleTemplateContentOutputTypeDef:
        """
        [Client.update_approval_rule_template_content documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.update_approval_rule_template_content)
        """

    def update_approval_rule_template_description(
        self, approvalRuleTemplateName: str, approvalRuleTemplateDescription: str
    ) -> UpdateApprovalRuleTemplateDescriptionOutputTypeDef:
        """
        [Client.update_approval_rule_template_description documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.update_approval_rule_template_description)
        """

    def update_approval_rule_template_name(
        self, oldApprovalRuleTemplateName: str, newApprovalRuleTemplateName: str
    ) -> UpdateApprovalRuleTemplateNameOutputTypeDef:
        """
        [Client.update_approval_rule_template_name documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.update_approval_rule_template_name)
        """

    def update_comment(self, commentId: str, content: str) -> UpdateCommentOutputTypeDef:
        """
        [Client.update_comment documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.update_comment)
        """

    def update_default_branch(self, repositoryName: str, defaultBranchName: str) -> None:
        """
        [Client.update_default_branch documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.update_default_branch)
        """

    def update_pull_request_approval_rule_content(
        self,
        pullRequestId: str,
        approvalRuleName: str,
        newRuleContent: str,
        existingRuleContentSha256: str = None,
    ) -> UpdatePullRequestApprovalRuleContentOutputTypeDef:
        """
        [Client.update_pull_request_approval_rule_content documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.update_pull_request_approval_rule_content)
        """

    def update_pull_request_approval_state(
        self, pullRequestId: str, revisionId: str, approvalState: Literal["APPROVE", "REVOKE"]
    ) -> None:
        """
        [Client.update_pull_request_approval_state documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.update_pull_request_approval_state)
        """

    def update_pull_request_description(
        self, pullRequestId: str, description: str
    ) -> UpdatePullRequestDescriptionOutputTypeDef:
        """
        [Client.update_pull_request_description documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.update_pull_request_description)
        """

    def update_pull_request_status(
        self, pullRequestId: str, pullRequestStatus: Literal["OPEN", "CLOSED"]
    ) -> UpdatePullRequestStatusOutputTypeDef:
        """
        [Client.update_pull_request_status documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.update_pull_request_status)
        """

    def update_pull_request_title(
        self, pullRequestId: str, title: str
    ) -> UpdatePullRequestTitleOutputTypeDef:
        """
        [Client.update_pull_request_title documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.update_pull_request_title)
        """

    def update_repository_description(
        self, repositoryName: str, repositoryDescription: str = None
    ) -> None:
        """
        [Client.update_repository_description documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.update_repository_description)
        """

    def update_repository_name(self, oldName: str, newName: str) -> None:
        """
        [Client.update_repository_name documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Client.update_repository_name)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_pull_request_events"]
    ) -> DescribePullRequestEventsPaginator:
        """
        [Paginator.DescribePullRequestEvents documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Paginator.DescribePullRequestEvents)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_comments_for_compared_commit"]
    ) -> GetCommentsForComparedCommitPaginator:
        """
        [Paginator.GetCommentsForComparedCommit documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Paginator.GetCommentsForComparedCommit)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_comments_for_pull_request"]
    ) -> GetCommentsForPullRequestPaginator:
        """
        [Paginator.GetCommentsForPullRequest documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Paginator.GetCommentsForPullRequest)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_differences"]) -> GetDifferencesPaginator:
        """
        [Paginator.GetDifferences documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Paginator.GetDifferences)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_branches"]) -> ListBranchesPaginator:
        """
        [Paginator.ListBranches documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Paginator.ListBranches)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_pull_requests"]
    ) -> ListPullRequestsPaginator:
        """
        [Paginator.ListPullRequests documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Paginator.ListPullRequests)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_repositories"]
    ) -> ListRepositoriesPaginator:
        """
        [Paginator.ListRepositories documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.26/reference/services/codecommit.html#CodeCommit.Paginator.ListRepositories)
        """
