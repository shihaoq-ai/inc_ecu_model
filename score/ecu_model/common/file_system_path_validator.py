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

from pathlib import PurePath


def validate_path_text(value: str | None, field_name: str) -> str | None:
    """Validate an optional filesystem-like path string and return its stripped form."""
    if value is None:
        return None

    stripped = value.strip()
    if not stripped:
        raise ValueError(f"{field_name} must not be empty when provided")
    if "\x00" in stripped:
        raise ValueError(f"{field_name} must not contain null bytes")

    # Parsing via PurePath ensures filesystem-like path semantics.
    PurePath(stripped)
    return stripped
