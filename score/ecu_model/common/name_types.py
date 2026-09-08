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

"""Common interfaces for source-language identifier value objects."""

from abc import ABC, abstractmethod

from pydantic_core import core_schema


class BaseIdentifier(ABC):
    """Common typed identifier representation shared by source languages."""

    @property
    @abstractmethod
    def as_str(self) -> str:
        """Return the identifier text."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Return the identifier text."""
        return self.as_str

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: object, handler: object) -> core_schema.CoreSchema:
        """Validate that values are concrete identifier instances."""
        if cls is not BaseIdentifier:
            return handler(source_type)
        del source_type, handler
        return core_schema.is_instance_schema(cls)


class BaseQualifiedName(ABC):
    """Common interface for source-language qualified names."""

    @property
    @abstractmethod
    def names(self) -> list[BaseIdentifier]:
        """Return the ordered identifier components."""
        try:
            return self.__dict__["names"]
        except KeyError as error:
            raise NotImplementedError from error

    @property
    @abstractmethod
    def as_str(self) -> str:
        """Return the source-language qualified name text."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Return the source-language qualified name text."""
        return self.as_str

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: object, handler: object) -> core_schema.CoreSchema:
        """Validate that values are concrete qualified-name instances."""
        if cls is not BaseQualifiedName:
            return handler(source_type)
        del source_type, handler
        return core_schema.is_instance_schema(cls)
