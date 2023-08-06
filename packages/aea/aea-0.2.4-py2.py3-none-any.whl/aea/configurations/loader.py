# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Implementation of the parser for configuration file."""

import inspect
import json
import os
import re
from pathlib import Path
from typing import Generic, TextIO, Type, TypeVar, Union

import jsonschema
from jsonschema import Draft4Validator

import yaml
from yaml import SafeLoader

from aea.configurations.base import (
    AgentConfig,
    ConfigurationType,
    ConnectionConfig,
    ProtocolConfig,
    ProtocolSpecification,
    SkillConfig,
)

_CUR_DIR = os.path.dirname(inspect.getfile(inspect.currentframe()))  # type: ignore
_SCHEMAS_DIR = os.path.join(_CUR_DIR, "schemas")

T = TypeVar(
    "T",
    AgentConfig,
    SkillConfig,
    ConnectionConfig,
    ProtocolConfig,
    ProtocolSpecification,
)


class ConfigLoader(Generic[T]):
    """This class implement parsing, serialization and validation functionalities for the 'aea' configuration files."""

    def __init__(self, schema_filename: str, configuration_type: Type[T]):
        """
        Initialize the parser for configuration files.

        :param schema_filename: the path to the JSON-schema file in 'aea/configurations/schemas'.
        :param configuration_type:
        """
        self.schema = json.load(open(os.path.join(_SCHEMAS_DIR, schema_filename)))
        root_path = "file://{}{}".format(Path(_SCHEMAS_DIR).absolute(), os.path.sep)
        self.resolver = jsonschema.RefResolver(root_path, self.schema)
        self.validator = Draft4Validator(self.schema, resolver=self.resolver)
        self.configuration_type = configuration_type  # type: Type[T]

    def load_protocol_specification(self, file_pointer: TextIO) -> T:
        """
        Load an agent configuration file.

        :param file_pointer: the file pointer to the configuration file
        :return: the configuration object.
        :raises
        """
        yaml_data = yaml.safe_load_all(file_pointer)
        yaml_documents = []
        for document in yaml_data:
            yaml_documents.append(document)
        configuration_file_json = yaml_documents[0]
        if len(yaml_documents) == 2:
            protobuf_snippets_json = yaml_documents[1]
        elif len(yaml_documents) == 1:
            protobuf_snippets_json = {}
        else:
            raise ValueError("Wrong number of documents in protocol specification.")
        try:
            self.validator.validate(instance=configuration_file_json)
        except Exception:
            raise
        protocol_specification = self.configuration_type.from_json(
            configuration_file_json
        )
        protocol_specification.protobuf_snippets = protobuf_snippets_json
        return protocol_specification

    def load(self, file_pointer: TextIO) -> T:
        """
        Load an agent configuration file.

        :param file_pointer: the file pointer to the configuration file
        :return: the configuration object.
        :raises
        """
        configuration_file_json = yaml.safe_load(file_pointer)
        try:
            self.validator.validate(instance=configuration_file_json)
        except Exception:
            raise
        return self.configuration_type.from_json(configuration_file_json)

    def dump(self, configuration: T, file_pointer: TextIO) -> None:
        """Dump a configuration.

        :param configuration: the configuration to be dumped.
        :param file_pointer: the file pointer to the configuration file
        :return: None
        """
        result = configuration.json
        self.validator.validate(instance=result)
        yaml.safe_dump(result, file_pointer)

    @classmethod
    def from_configuration_type(
        cls, configuration_type: Union[ConfigurationType, str]
    ) -> "ConfigLoader":
        """Get the configuration loader from the type."""
        configuration_type = ConfigurationType(configuration_type)
        if configuration_type == ConfigurationType.AGENT:
            return ConfigLoader("aea-config_schema.json", AgentConfig)
        elif configuration_type == ConfigurationType.PROTOCOL:
            return ConfigLoader("protocol-config_schema.json", ProtocolConfig)
        elif configuration_type == ConfigurationType.CONNECTION:
            return ConfigLoader("connection-config_schema.json", ConnectionConfig)
        elif configuration_type == ConfigurationType.SKILL:
            return ConfigLoader("skill-config_schema.json", SkillConfig)
        else:  # pragma: no cover
            raise ValueError("Invalid configuration type.")


def _config_loader():
    envvar_matcher = re.compile(r"\${([^}^{]+)\}")

    def envvar_constructor(_loader, node):  # pragma: no cover
        """Extract the matched value, expand env variable, and replace the match."""
        node_value = node.value
        match = envvar_matcher.match(node_value)
        env_var = match.group()[2:-1]

        # check for defaults
        var_name, default_value = env_var.split(":")
        var_name = var_name.strip()
        default_value = default_value.strip()
        var_value = os.getenv(var_name, default_value)
        return var_value + node_value[match.end() :]

    yaml.add_implicit_resolver("!envvar", envvar_matcher, None, SafeLoader)
    yaml.add_constructor("!envvar", envvar_constructor, SafeLoader)


_config_loader()
