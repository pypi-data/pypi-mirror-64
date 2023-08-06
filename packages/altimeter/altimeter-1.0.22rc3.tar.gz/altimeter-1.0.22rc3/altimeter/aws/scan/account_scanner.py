"""An AccountScanner scans a set of accounts using an AccountScanPlan to define scan
parameters"""
from altimeter.core.artifact_io.writer import ArtifactWriter
from altimeter.aws.scan.settings import (
    RESOURCE_SPEC_CLASSES,
    INFRA_RESOURCE_SPEC_CLASSES,
    ORG_RESOURCE_SPEC_CLASSES,
)
from altimeter.aws.settings import GRAPH_NAME, GRAPH_VERSION
from altimeter.aws.scan.account_scan_plan import AccountScanPlan
from altimeter.aws.scan.base_scanner import BaseScanner


class AccountScanner(BaseScanner):  # pylint: disable=too-few-public-methods
    """An AccountScanner scans a set of accounts using an AccountScanPlan to define scan parameters
    and writes the output using an ArtifactWriter.

    Args:
        account_scan_plan: AccountScanPlan describing scan targets
        artifact_writer: ArtifactWriter for writing out artifacts
        scan_sub_accounts: if set to True, if this account is an org master any subaccounts
                           of that org will also be scanned.
        max_account_threads: max number of accounts to scan concurrently
        max_svc_threads: max number of service scan threads per account to run concurrently.
        graph_name: name of graph
        graph_version: version string for graph
    """

    def __init__(
        self,
        account_scan_plan: AccountScanPlan,
        artifact_writer: ArtifactWriter,
        scan_sub_accounts: bool,
        max_account_threads: int = 16,
        max_svc_threads: int = 4,
        graph_name: str = GRAPH_NAME,
        graph_version: str = GRAPH_VERSION,
    ) -> None:
        resource_spec_classes = RESOURCE_SPEC_CLASSES + INFRA_RESOURCE_SPEC_CLASSES
        if scan_sub_accounts:
            resource_spec_classes += ORG_RESOURCE_SPEC_CLASSES
        super().__init__(
            account_scan_plan=account_scan_plan,
            artifact_writer=artifact_writer,
            max_account_threads=max_account_threads,
            max_svc_threads=max_svc_threads,
            graph_name=graph_name,
            graph_version=graph_version,
            resource_spec_classes=resource_spec_classes,
        )
