# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import field
from enum import Enum, auto
from typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model import CreationInfo, Element, ExternalIdentifier, ExternalReference, IntegrityMethod


class AnnotationType(Enum):
    REVIEW = auto()
    OTHER = auto()


@dataclass_with_properties
class Annotation(Element):
    annotation_type: AnnotationType = None
    subject: str = None
    content_type: List[str] = field(default_factory=list)  # placeholder for MediaType
    statement: Optional[str] = None

    def __init__(
        self,
        spdx_id: str,
        creation_info: CreationInfo,
        annotation_type: AnnotationType,
        subject: str,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        comment: Optional[str] = None,
        verified_using: List[IntegrityMethod] = None,
        external_references: List[ExternalReference] = None,
        external_identifier: List[ExternalIdentifier] = None,
        extension: Optional[str] = None,
        content_type: List[str] = None,
        statement: Optional[str] = None,
    ):
        verified_using = [] if verified_using is None else verified_using
        external_references = [] if external_references is None else external_references
        external_identifier = [] if external_identifier is None else external_identifier
        content_type = [] if content_type is None else content_type
        check_types_and_set_values(self, locals())