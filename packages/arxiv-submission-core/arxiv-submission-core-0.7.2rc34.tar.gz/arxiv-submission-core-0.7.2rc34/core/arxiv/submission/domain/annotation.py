"""
Provides quality-assurance annotations for the submission & moderation system.
"""

import hashlib
from datetime import datetime
from enum import Enum
from typing import Optional, Union, List, Dict, Type, Any

from dataclasses import dataclass, asdict, field
from mypy_extensions import TypedDict

from arxiv.taxonomy import Category

from .agent import Agent, agent_factory
from .util import get_tzaware_utc_now


@dataclass
class Comment:
    """A freeform textual annotation."""

    event_id: str
    creator: Agent
    created: datetime
    proxy: Optional[Agent] = field(default=None)
    body: str = field(default_factory=str)

    def __post_init__(self) -> None:
        """Check our agents."""
        if self.creator and isinstance(self.creator, dict):
            self.creator = agent_factory(**self.creator)
        if self.proxy and isinstance(self.proxy, dict):
            self.proxy = agent_factory(**self.proxy)


ClassifierResult = TypedDict('ClassifierResult',
                             {'category': Category, 'probability': float})


@dataclass
class Annotation:
    event_id: str
    creator: Agent
    created: datetime

    def __post_init__(self) -> None:
        """Check our agents."""
        if self.creator and isinstance(self.creator, dict):
            self.creator = agent_factory(**self.creator)


@dataclass
class ClassifierResults(Annotation):
    """Represents suggested classifications from an auto-classifier."""

    class Classifiers(Enum):
        """Supported classifiers."""

        CLASSIC = "classic"

    # event_id: str
    # creator: Agent
    # created: datetime
    proxy: Optional[Agent] = field(default=None)
    classifier: Classifiers = field(default=Classifiers.CLASSIC)
    results: List[ClassifierResult] = field(default_factory=list)
    annotation_type: str = field(default='ClassifierResults')

    def __post_init__(self) -> None:
        """Check our enums."""
        super(ClassifierResults, self).__post_init__()
        if self.proxy and isinstance(self.proxy, dict):
            self.proxy = agent_factory(**self.proxy)
        self.classifier = self.Classifiers(self.classifier)


@dataclass
class Feature(Annotation):
    """Represents features drawn from the content of the submission."""

    class Type(Enum):
        """Supported features."""

        CHARACTER_COUNT = "chars"
        PAGE_COUNT = "pages"
        STOPWORD_COUNT = "stops"
        STOPWORD_PERCENT = "%stop"
        WORD_COUNT = "words"

    # event_id: str
    # created: datetime
    # creator: Agent
    feature_type: Type
    proxy: Optional[Agent] = field(default=None)
    feature_value: Union[int, float] = field(default=0)
    annotation_type: str = field(default='Feature')

    def __post_init__(self) -> None:
        """Check our enums."""
        super(Feature, self).__post_init__()
        if self.proxy and isinstance(self.proxy, dict):
            self.proxy = agent_factory(**self.proxy)
        self.feature_type = self.Type(self.feature_type)


annotation_types: Dict[str, Type[Annotation]] = {
    'Feature': Feature,
    'ClassifierResults': ClassifierResults
}


def annotation_factory(**data: Any) -> Annotation:
    an: Annotation = annotation_types[data.pop('annotation_type')](**data)
    return an
