from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class APINotificationMessage:
    api_uri: Optional[str] = field(init=False, default=None)

@dataclass
class OrgSpecificMessage(APINotificationMessage):
    org_id: Optional[str] = field(init=False, default=None)

@dataclass
class TestsUpdateMessage(OrgSpecificMessage):
    updated_test_uuids: List[str]
    deleted_test_uuids: List[str]
    affected_duts: List[str]
    update_all: bool = False
    delete_all: bool = False

    @classmethod
    def create(self, **kwargs):
        defaults = dict(
            updated_test_uuids = [],
            deleted_test_uuids = [],
            affected_duts = [],
            update_all = False,
            delete_all = False
        )
        defaults.update(kwargs)
        return TestsUpdateMessage(**defaults)

@dataclass
class TestsUpdateQueryMessage(OrgSpecificMessage):
    query_dict: Dict[str, Any]

    @classmethod
    def from_message(cls, other_org_specific_message, **kwargs):
        obj = cls(**kwargs)
        obj.api_uri = other_org_specific_message.api_uri
        obj.org_id = other_org_specific_message.org_id
        return obj
