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

from re import fullmatch

from pydantic import Field, RootModel, field_validator

from score.ecu_model.common.name_types import (
    BaseIdentifier,
    BaseQualifiedName,
)


class Identifier(BaseIdentifier, RootModel[str]):
    """Typed C++ identifier used by names and enum literals."""

    root: str = Field(
        description="Plain C++ identifier, e.g. LaneInfo, SpeedLimit, uint32_t",
    )

    @field_validator("root")
    @classmethod
    def _validate_root_is_cpp_identifier(cls, value: str) -> str:
        """Validate the identifier as a non-empty C++ identifier."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("identifier must not be empty")
        if not fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", stripped):
            raise ValueError("identifier must be a valid C++ identifier (e.g. LaneInfo, SpeedLimit, uint32_t)")
        return stripped

    @property
    def as_str(self) -> str:
        """Return the C++ identifier text."""
        return self.root


class QualifiedNamespace(BaseQualifiedName, RootModel[str]):
    """Typed C++ namespace path used by data type definitions."""

    root: str = Field(
        description="Qualified C++ namespace path, e.g. company::project::module",
    )

    @field_validator("root")
    @classmethod
    def _validate_root_is_cpp_qualified_name(cls, value: str) -> str:
        """Validate the namespace as a non-empty qualified C++ namespace path."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("namespace must not be empty when provided")
        if not fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(?:::[A-Za-z_][A-Za-z0-9_]*)*", stripped):
            raise ValueError("namespace must be a valid C++ namespace (e.g. my_ns::sub_ns)")
        return stripped

    @property
    def names(self) -> list[Identifier]:
        """Return the ordered namespace identifier components."""
        return [Identifier(name) for name in self.root.split("::")]

    @property
    def as_str(self) -> str:
        """Return the C++ namespace text."""
        return self.root


class QualifiedName(BaseQualifiedName, RootModel[str]):
    """Typed C++ qualified name in the form `identifier` or `namespace::identifier`."""

    root: str = Field(
        description="Qualified C++ name, e.g. LaneInfo or demo::LaneInfo",
    )

    @field_validator("root")
    @classmethod
    def _validate_root_is_identifier_or_qualified_name(cls, value: str) -> str:
        """Validate a plain identifier or a namespace-qualified identifier."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("qualified name must not be empty")

        namespace_candidate, separator, identifier_candidate = stripped.rpartition("::")
        identifier = identifier_candidate if separator else stripped

        Identifier(identifier)
        if separator:
            QualifiedNamespace(namespace_candidate)
        return stripped

    @property
    def identifier(self) -> Identifier:
        """Return the final identifier component of the qualified name."""
        _, _, identifier_candidate = self.root.rpartition("::")
        return Identifier(identifier_candidate or self.root)

    @property
    def names(self) -> list[Identifier]:
        """Return the ordered qualified-name identifier components."""
        return [Identifier(name) for name in self.root.split("::")]

    @property
    def as_str(self) -> str:
        """Return the C++ qualified-name text."""
        return self.root


class DataTypeReference(QualifiedName):
    """Typed reference to another data type definition via registry key."""

    @property
    def data_type_key(self) -> str:
        """Return the referenced data type key."""
        return self.root
