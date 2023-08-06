"""
Proposals provide a mechanism for suggesting changes to submissions.

The primary use-case in the classic submission & moderation system is for
suggesting changes to the primary or cross-list classification. Such proposals
are generated both automatically based on the results of the classifier and
manually by moderators.
"""

from typing import Optional, Union, List
from datetime import datetime
import hashlib

from dataclasses import dataclass, asdict, field
from enum import Enum

from arxiv.taxonomy import Category

from .annotation import Comment
from .util import get_tzaware_utc_now
from .agent import Agent, agent_factory


@dataclass
class Proposal:
    """Represents a proposal to apply an event to a submission."""

    class Status(Enum):
        PENDING = 'pending'
        REJECTED = 'rejected'
        ACCEPTED = 'accepted'

    event_id: str
    creator: Agent
    created: datetime = field(default_factory=get_tzaware_utc_now)
    # scope: str      # TODO: document this.
    proxy: Optional[Agent] = field(default=None)

    proposed_event_type: Optional[type] = field(default=None)
    proposed_event_data: dict = field(default_factory=dict)
    comments: List[Comment] = field(default_factory=list)
    status: Status = field(default=Status.PENDING)

    @property
    def proposal_type(self) -> str:
        """Name (str) of the type of annotation."""
        assert self.proposed_event_type is not None
        return self.proposed_event_type.__name__

    def __post_init__(self) -> None:
        """Check our enums and agents."""
        if self.creator and isinstance(self.creator, dict):
            self.creator = agent_factory(**self.creator)
        if self.proxy and isinstance(self.proxy, dict):
            self.proxy = agent_factory(**self.proxy)
        self.status = self.Status(self.status)

    def is_rejected(self) -> bool:
        return self.status == self.Status.REJECTED

    def is_accepted(self) -> bool:
        return self.status == self.Status.ACCEPTED

    def is_pending(self) -> bool:
        return self.status == self.Status.PENDING
