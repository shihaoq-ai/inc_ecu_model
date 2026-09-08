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


def validate_bazel_target_text(value: str | None, field_name: str) -> str | None:
    """Validate an optional Bazel label string and return its stripped form."""
    if value is None:
        return None

    stripped = value.strip()
    if not stripped:
        raise ValueError(f"{field_name} must not be empty when provided")
    if "\x00" in stripped:
        raise ValueError(f"{field_name} must not contain null bytes")

    absolute_label_pattern = (
        r"(?:@[A-Za-z0-9._+-]+)?//(?:[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*)?"
        r"(?::[A-Za-z0-9._+-]+)?"
    )
    relative_label_pattern = r":[A-Za-z0-9._+-]+"
    if not fullmatch(f"(?:{absolute_label_pattern}|{relative_label_pattern})", stripped):
        raise ValueError(f"{field_name} must be a valid Bazel label")
    return stripped
