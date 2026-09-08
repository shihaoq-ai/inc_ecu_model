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

"""Lark parsing and import discovery for declared Franca source files."""

from pathlib import Path

from lark import Lark
from lark.exceptions import VisitError

from score.parsers.franca_parser.model.parsed_file import ParsedFile
from score.parsers.franca_parser.transformer.import_transformer import (
    FrancaImportTransformer,
)


class FrancaParser:
    """Parse declared FIDL and FDEPL files with their imports exactly once."""

    def __init__(self, root_files: list[Path], dependency_files: list[Path]) -> None:
        self._root_files = root_files
        self._allowed_files = {path.resolve() for path in root_files + dependency_files}
        self._parsed_files: dict[Path, ParsedFile] = {}
        self._grammar_directory = Path(__file__).parent / "grammar"
        self._grammar_names = {
            ".fidl": "franca_fidl.lark",
            ".fdepl": "franca_fdepl.lark",
        }
        self._parsers: dict[str, Lark] = {}

    @property
    def parsed_files(self) -> dict[Path, ParsedFile]:
        """Return parsed files indexed by canonical source path."""
        return self._parsed_files

    def parse_files(self) -> dict[Path, ParsedFile]:
        """Discover and parse every root file and transitive declared import."""
        pending_files = list(self._root_files)
        while pending_files:
            file_path = pending_files.pop().resolve()
            if file_path in self._parsed_files:
                continue
            if file_path not in self._allowed_files:
                raise FileNotFoundError(f"Franca source is not declared as srcs or deps: {file_path}")
            parsed_file = ParsedFile(
                file_path=file_path,
                parse_tree=self._parser_for(file_path).parse(file_path.read_text()),
            )
            collector = FrancaImportTransformer(lambda import_uri: self._resolve_import_path(file_path, import_uri))
            try:
                collector.transform(parsed_file.parse_tree)
            except VisitError as error:
                if isinstance(error.orig_exc, FileNotFoundError):
                    raise error.orig_exc from error
                raise
            parsed_file.imports = collector.imported_namespaces
            self._parsed_files[file_path] = parsed_file
            pending_files.extend(imported.file_path for imported in parsed_file.imports)
        return self._parsed_files

    def _parser_for(self, file_path: Path) -> Lark:
        """Return the cached parser for a supported file type, creating it on demand."""
        suffix = file_path.suffix
        grammar_name = self._grammar_names.get(suffix)
        if grammar_name is None:
            raise ValueError(f"Unsupported Franca source type: {file_path}")
        if suffix not in self._parsers:
            self._parsers[suffix] = Lark(
                (self._grammar_directory / grammar_name).read_text(),
                parser="lalr",
                import_paths=[self._grammar_directory],
            )
        return self._parsers[suffix]

    def _resolve_import_path(self, importing_file: Path, import_uri: str) -> Path:
        candidate = (importing_file.parent / import_uri).resolve()
        if candidate in self._allowed_files:
            return candidate
        raise FileNotFoundError(f"Could not resolve declared Franca import '{import_uri}' in '{importing_file}'")
