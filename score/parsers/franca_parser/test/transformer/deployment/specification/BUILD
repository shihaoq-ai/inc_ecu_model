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

load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "fdepl_specification_transformer_test",
    srcs = ["fdepl_specification_transformer_test.py"],
    data = ["//score/parsers/franca_parser/test/spec_files:ipc"],
    deps = ["//score/parsers/franca_parser"],
)
