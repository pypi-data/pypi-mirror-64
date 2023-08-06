#!/usr/bin/env python3
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

"""Core definitions for the AEA command-line tool."""

import os
import shutil
import sys
import time
from pathlib import Path

import click

import aea
from aea.cli.add import add
from aea.cli.common import (
    AgentDirectory,
    Context,
    logger,
    pass_ctx,
    try_to_load_agent_config,
)
from aea.cli.config import config
from aea.cli.create import create
from aea.cli.fetch import fetch
from aea.cli.generate import generate
from aea.cli.init import init
from aea.cli.install import install
from aea.cli.launch import launch
from aea.cli.list import list as _list
from aea.cli.loggers import simple_verbosity_option
from aea.cli.login import login
from aea.cli.publish import publish
from aea.cli.push import push
from aea.cli.remove import remove
from aea.cli.run import _verify_or_create_private_keys, run
from aea.cli.scaffold import scaffold
from aea.cli.search import search
from aea.configurations.base import DEFAULT_AEA_CONFIG_FILE
from aea.crypto.ethereum import EthereumCrypto
from aea.crypto.fetchai import FetchAICrypto
from aea.crypto.helpers import (
    ETHEREUM_PRIVATE_KEY_FILE,
    FETCHAI_PRIVATE_KEY_FILE,
    TESTNETS,
    _try_generate_testnet_wealth,
    _validate_private_key_path,
)
from aea.crypto.ledger_apis import LedgerApis
from aea.crypto.wallet import Wallet


FUNDS_RELEASE_TIMEOUT = 10


@click.group(name="aea")
@click.version_option(aea.__version__, prog_name="aea")
@simple_verbosity_option(logger, default="INFO")
@click.pass_context
def cli(ctx) -> None:
    """Command-line tool for setting up an Autonomous Economic Agent."""
    ctx.obj = Context(cwd=".")


@cli.command()
@click.argument(
    "agent_name", type=AgentDirectory(), required=True,
)
@pass_ctx
def delete(ctx: Context, agent_name):
    """Delete an agent."""
    click.echo("Deleting AEA project directory './{}'...".format(agent_name))

    # delete the agent's directory
    try:
        shutil.rmtree(agent_name, ignore_errors=False)
    except OSError:
        logger.error(
            "An error occurred while deleting the agent directory. Aborting..."
        )
        sys.exit(1)


@cli.command()
@pass_ctx
def freeze(ctx: Context):
    """Get the dependencies."""
    try_to_load_agent_config(ctx)
    for dependency_name, dependency_data in sorted(
        ctx.get_dependencies().items(), key=lambda x: x[0]
    ):
        print(dependency_name + dependency_data.get("version", ""))


@cli.command()
@pass_ctx
@click.option("-p", "--port", default=8080)
def gui(ctx: Context, port):
    """Run the CLI GUI."""
    import aea.cli_gui  # pragma: no cover

    click.echo("Running the GUI.....(press Ctrl+C to exit)")  # pragma: no cover
    aea.cli_gui.run(port)  # pragma: no cover


@cli.command()
@click.argument(
    "type_",
    metavar="TYPE",
    type=click.Choice([FetchAICrypto.identifier, EthereumCrypto.identifier, "all"]),
    required=True,
)
@pass_ctx
def generate_key(ctx: Context, type_):
    """Generate private keys."""

    def _can_write(path) -> bool:
        if Path(path).exists():
            value = click.confirm(
                "The file {} already exists. Do you want to overwrite it?".format(path),
                default=False,
            )
            return value
        else:
            return True

    if type_ in (FetchAICrypto.identifier, "all"):
        if _can_write(FETCHAI_PRIVATE_KEY_FILE):
            FetchAICrypto().dump(open(FETCHAI_PRIVATE_KEY_FILE, "wb"))
    if type_ in (EthereumCrypto.identifier, "all"):
        if _can_write(ETHEREUM_PRIVATE_KEY_FILE):
            EthereumCrypto().dump(open(ETHEREUM_PRIVATE_KEY_FILE, "wb"))


def _try_add_key(ctx, type_, filepath):
    try:
        ctx.agent_config.private_key_paths.create(type_, filepath)
    except ValueError as e:  # pragma: no cover
        logger.error(str(e))
        sys.exit(1)
    ctx.agent_loader.dump(
        ctx.agent_config, open(os.path.join(ctx.cwd, DEFAULT_AEA_CONFIG_FILE), "w")
    )


@cli.command()
@click.argument(
    "type_",
    metavar="TYPE",
    type=click.Choice([FetchAICrypto.identifier, EthereumCrypto.identifier]),
    required=True,
)
@click.argument(
    "file",
    metavar="FILE",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    required=True,
)
@pass_ctx
def add_key(ctx: Context, type_, file):
    """Add a private key to the wallet."""
    try_to_load_agent_config(ctx)
    _validate_private_key_path(file, type_)
    _try_add_key(ctx, type_, file)


def _try_get_address(ctx, type_):
    private_key_paths = {
        config_pair[0]: config_pair[1]
        for config_pair in ctx.agent_config.private_key_paths.read_all()
    }
    try:
        wallet = Wallet(private_key_paths)
        address = wallet.addresses[type_]
        return address
    except ValueError as e:  # pragma: no cover
        logger.error(str(e))
        sys.exit(1)


@cli.command()
@click.argument(
    "type_",
    metavar="TYPE",
    type=click.Choice([FetchAICrypto.identifier, EthereumCrypto.identifier]),
    required=True,
)
@pass_ctx
def get_address(ctx: Context, type_):
    """Get the address associated with the private key."""
    try_to_load_agent_config(ctx)
    _verify_or_create_private_keys(ctx)
    address = _try_get_address(ctx, type_)
    click.echo(address)


def _try_get_balance(agent_config, wallet, type_):
    try:
        ledger_apis = LedgerApis(
            agent_config.ledger_apis_dict, agent_config.default_ledger
        )

        address = wallet.addresses[type_]
        return ledger_apis.token_balance(type_, address)
    except (AssertionError, ValueError) as e:  # pragma: no cover
        logger.error(str(e))
        sys.exit(1)


def _try_get_wealth(ctx, type_):
    private_key_paths = {
        config_pair[0]: config_pair[1]
        for config_pair in ctx.agent_config.private_key_paths.read_all()
    }
    wallet = Wallet(private_key_paths)
    return _try_get_balance(ctx.agent_config, wallet, type_)


@cli.command()
@click.argument(
    "type_",
    metavar="TYPE",
    type=click.Choice([FetchAICrypto.identifier, EthereumCrypto.identifier]),
    required=True,
)
@pass_ctx
def get_wealth(ctx: Context, type_):
    """Get the wealth associated with the private key."""
    try_to_load_agent_config(ctx)
    _verify_or_create_private_keys(ctx)
    wealth = _try_get_wealth(ctx, type_)
    click.echo(wealth)


def _wait_funds_release(agent_config, wallet, type_):
    start_balance = _try_get_balance(agent_config, wallet, type_)
    end_time = time.time() + FUNDS_RELEASE_TIMEOUT
    while time.time() < end_time:
        if start_balance != _try_get_balance(agent_config, wallet, type_):
            break  # pragma: no cover
        else:
            time.sleep(1)


def _try_generate_wealth(ctx, type_, sync):
    private_key_paths = {
        config_pair[0]: config_pair[1]
        for config_pair in ctx.agent_config.private_key_paths.read_all()
    }
    wallet = Wallet(private_key_paths)
    try:
        address = wallet.addresses[type_]
        testnet = TESTNETS[type_]
        click.echo(
            "Requesting funds for address {} on test network '{}'".format(
                address, testnet
            )
        )
        _try_generate_testnet_wealth(type_, address)
        if sync:
            _wait_funds_release(ctx.agent_config, wallet, type_)

    except (AssertionError, ValueError) as e:  # pragma: no cover
        logger.error(str(e))
        sys.exit(1)


@cli.command()
@click.argument(
    "type_",
    metavar="TYPE",
    type=click.Choice([FetchAICrypto.identifier, EthereumCrypto.identifier]),
    required=True,
)
@click.option(
    "--sync", is_flag=True, help="For waiting till the faucet has released the funds."
)
@pass_ctx
def generate_wealth(ctx: Context, sync, type_):
    """Generate wealth for address on test network."""
    try_to_load_agent_config(ctx)
    _verify_or_create_private_keys(ctx)
    _try_generate_wealth(ctx, type_, sync)


cli.add_command(_list)
cli.add_command(add)
cli.add_command(create)
cli.add_command(config)
cli.add_command(fetch)
cli.add_command(generate)
cli.add_command(init)
cli.add_command(install)
cli.add_command(launch)
cli.add_command(login)
cli.add_command(publish)
cli.add_command(push)
cli.add_command(remove)
cli.add_command(run)
cli.add_command(scaffold)
cli.add_command(search)
