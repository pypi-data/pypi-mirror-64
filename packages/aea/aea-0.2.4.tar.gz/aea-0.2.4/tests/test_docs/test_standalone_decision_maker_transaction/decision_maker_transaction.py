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

"""This module contains the tests for the code-blocks in the decision-maker-transaction.md file."""

import logging
import time
from threading import Thread
from typing import Optional, cast

from aea.aea import AEA
from aea.configurations.base import ProtocolId, PublicId
from aea.connections.stub.connection import StubConnection
from aea.crypto.fetchai import FETCHAI
from aea.crypto.helpers import _create_fetchai_private_key, _try_generate_testnet_wealth
from aea.crypto.ledger_apis import LedgerApis
from aea.crypto.wallet import Wallet
from aea.decision_maker.messages.transaction import TransactionMessage
from aea.identity.base import Identity
from aea.protocols.base import Message
from aea.registries.base import Resources
from aea.skills.base import Handler

logger = logging.getLogger("aea")
logging.basicConfig(level=logging.INFO)

FETCHAI_PRIVATE_KEY_FILE_1 = "fet_private_key_1.txt"
FETCHAI_PRIVATE_KEY_FILE_2 = "fet_private_key_2.txt"

INPUT_FILE = "input.txt"
OUTPUT_FILE = "output.txt"


def run():
    # Create a private keys
    _create_fetchai_private_key(private_key_file=FETCHAI_PRIVATE_KEY_FILE_1)
    _create_fetchai_private_key(private_key_file=FETCHAI_PRIVATE_KEY_FILE_2)

    # Set up the wallets
    wallet_1 = Wallet({FETCHAI: FETCHAI_PRIVATE_KEY_FILE_1})
    wallet_2 = Wallet({FETCHAI: FETCHAI_PRIVATE_KEY_FILE_2})

    # Generate some wealth
    _try_generate_testnet_wealth(FETCHAI, wallet_1.addresses[FETCHAI])

    # Set up the LedgerApis
    ledger_apis = LedgerApis({FETCHAI: {"network": "testnet"}}, FETCHAI)

    tx_handler = TransactionHandler(skill_context="skill_context", name="fake_skill")
    resources = Resources()
    resources.handler_registry.register(
        (
            PublicId.from_str("fetchai/fake_skill:0.1.0"),
            PublicId.from_str("fetchai/internal:0.1.0"),
        ),
        tx_handler,
    )

    stub_connection = StubConnection(
        input_file_path=INPUT_FILE, output_file_path=OUTPUT_FILE
    )

    identity_1 = Identity(
        name="my_aea",
        address=wallet_1.addresses.get(FETCHAI),
        default_address_key=FETCHAI,
    )

    identity_2 = Identity(
        name="my_aea_2",
        address=wallet_2.addresses.get(FETCHAI),
        default_address_key=FETCHAI,
    )

    # create the AEA

    my_aea = AEA(identity_1, [stub_connection], wallet_1, ledger_apis, resources)
    ledger_api = ledger_apis.apis[FETCHAI]
    tx_nonce = ledger_api.generate_tx_nonce(
        identity_1.addresses.get(FETCHAI), identity_2.addresses.get(FETCHAI)
    )

    tx_msg = TransactionMessage(
        performative=TransactionMessage.Performative.PROPOSE_FOR_SETTLEMENT,
        skill_callback_ids=[PublicId("fetchai", "fake_skill", "0.1.0")],
        tx_id="transaction0",
        tx_sender_addr=identity_1.addresses.get(FETCHAI),
        tx_counterparty_addr=identity_2.addresses.get(FETCHAI),
        tx_amount_by_currency_id={"FET": -1},
        tx_sender_fee=1,
        tx_counterparty_fee=0,
        tx_quantities_by_good_id={},
        ledger_id=FETCHAI,
        info={"some_info_key": "some_info_value"},
        tx_nonce=tx_nonce,
    )
    my_aea.context.decision_maker_message_queue.put_nowait(tx_msg)

    # Set the AEA running in a different thread
    try:
        logger.info("STARTING AEA NOW!")
        t = Thread(target=my_aea.start)
        t.start()

        # Let it run long enough to interact with the weather station
        time.sleep(20)
    finally:
        # Shut down the AEA
        logger.info("STOPPING AEA NOW!")
        my_aea.stop()
        t.join()


class TransactionHandler(Handler):
    """Implement the transaction handler."""

    SUPPORTED_PROTOCOL = TransactionMessage.protocol_id  # type: Optional[ProtocolId]

    def setup(self) -> None:
        """Implement the setup for the handler."""
        pass

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to a message.

        :param message: the message
        :return: None
        """
        tx_msg_response = cast(TransactionMessage, message)
        logger.info(tx_msg_response)
        if (
            tx_msg_response is not None
            and tx_msg_response.performative
            == TransactionMessage.Performative.SUCCESSFUL_SETTLEMENT
        ):
            logger.info("Transaction was successful.")
            logger.info(tx_msg_response.tx_digest)
        else:
            logger.info("Transaction was not successful.")

    def teardown(self) -> None:
        """
        Implement the handler teardown.

        :return: None
        """
        pass


if __name__ == "__main__":
    run()
