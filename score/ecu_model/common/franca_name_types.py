# *******************************************************************************
# Copyright (c) 2026 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0
#
# SPDX-License-Identifier: Apache-2.0
# *******************************************************************************

"""Franca identifier and qualified-name value objects."""

from pydantic import BaseModel, Field, RootModel, field_validator

from score.ecu_model.common.name_types import (
    BaseIdentifier,
    BaseQualifiedName,
)


class ValidIdentifier(BaseIdentifier, RootModel[str]):
    """Typed Franca identifier with escaped keyword markers removed."""

    @field_validator("root")
    @classmethod
    def _remove_escape_characters(cls, value: str) -> str:
        """Remove Franca escape characters from an identifier."""
        return value.replace("^", "")

    @property
    def as_str(self) -> str:
        """Return the Franca identifier text."""
        return self.root


class FullyQualifiedName(BaseModel, BaseQualifiedName):
    """Typed Franca fully qualified name represented by its identifier components."""

    names: list[ValidIdentifier] = Field(
        default_factory=list,
        description="Ordered Franca identifier components",
    )

    @property
    def as_str(self) -> str:
        """Return the dot-separated Franca qualified name."""
        return ".".join(name.as_str for name in self.names)

    def __str__(self) -> str:
        """Return the Franca qualified name text."""
        return self.as_str

    @property
    def as_path(self) -> str:
        """Return the slash-separated Franca qualified name."""
        return "/".join(name.as_str for name in self.names)
