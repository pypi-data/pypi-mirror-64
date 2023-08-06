__copyright__ = "Copyright (C) 2019 Icerm"

__license__ = """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

__doc__ = """
:mod:`vsyspy.chain` vsys chain.
"""

from .errors import NetworkException
from .setting import *
from .crypto import *
from . import is_offline

import time
import logging


class Chain(object):
    """Class for Chain.

    It can be used to create vsys chain object

    .. attribute:: chain_name

        VSYS chain name.

    .. attribute:: chain_id

        VSYS chain id.

    .. attribute:: address_version

        address version on chain.

    .. attribute:: api_wrapper

        api wrapper.

    """
    def __init__(self, chain_name, chain_id, address_version, api_wrapper):
        self.chain_name = chain_name
        self.chain_id = chain_id
        self.address_version = address_version
        self.api_wrapper = api_wrapper
        self.logger = logging.getLogger(__name__)

    def height(self):
        if is_offline():
            raise NetworkException("Cannot check height in offline mode.")
        else:
            return self.api_wrapper.request('blocks/height')['height']

    def self_check(self, super_node_num=DEFAULT_SUPER_NODE_NUM):
        try:
            # check connected peers
            peers = self.get_connected_peers()
            if not peers:
                self.logger.error("The node {} does not connect any peers.".format(self.api_wrapper.node_host))
                return False
            # check height
            h2 = h1 = self.height()
            delay = max(int(60 / super_node_num), 1)
            count = 0
            while h2 <= h1 and count <= super_node_num:
                time.sleep(delay)
                h2 = self.height()
                count += 1
            if h2 <= h1:
                self.logger.error("The height is not update. Full node has problem or stopped.")
                return False
            # Add more check if need
            self.logger.debug("OK. Full node is alive.")
            return True
        except NetworkException:
            self.logger.error("Fail to connect full node.")
            return False

    def check_with_other_node(self, node_host, super_node_num=DEFAULT_SUPER_NODE_NUM):
        if is_offline():
            raise NetworkException("Cannot check height in offline mode.")
        try:
            h1 = self.height()
        except NetworkException:
            self.logger.error("Fail to connect {}.".format(node_host))
            return False
        try:
            other_api = Wrapper(node_host)
            h2 = other_api.request('blocks/height')['height']
        except NetworkException:
            self.logger.error("Fail to connect {}.".format(node_host))
            return False
        # Add more check if need
        return h2 - h1 <= super_node_num

    def get_connected_peers(self):
        if is_offline():
            raise NetworkException("Cannot check height in offline mode.")
        response = self.api_wrapper.request('peers/connected')
        if not response.get("peers"):
            return []
        else:
            return [peer["address"] for peer in response.get("peers")]

    def lastblock(self):
        return self.api_wrapper.request('blocks/last')

    def block(self, n):
        return self.api_wrapper.request('blocks/at/%d' % n)

    def tx(self, id):
        return self.api_wrapper.request('transactions/info/%s' % id)

    def unconfirmed_tx(self, id):
        return self.api_wrapper.request('transactions/unconfirmed/info/%s' % id)

    def slot_info(self, slot_id):
        return self.api_wrapper.request('consensus/slotInfo/%s' % slot_id)

    def validate_address(self, address):
        addr = bytes2str(base58.b58decode(address))
        if addr[0] != chr(self.address_version):
            self.logger.error("Wrong address version")
        elif addr[1] != self.chain_id:
            self.logger.error("Wrong chain id")
        elif len(addr) != ADDRESS_LENGTH:
            self.logger.error("Wrong address length")
        elif addr[-ADDRESS_CHECKSUM_LENGTH:] != hashChain(str2bytes(addr[:-ADDRESS_CHECKSUM_LENGTH]))[
                                                :ADDRESS_CHECKSUM_LENGTH]:
            self.logger.error("Wrong address checksum")
        else:
            return True
        return False

    def public_key_to_address(self, public_key):
        unhashedAddress = chr(self.address_version) + str(self.chain_id) + hashChain(public_key)[0:20]
        addressHash = hashChain(str2bytes(unhashedAddress))[0:4]
        address = bytes2str(base58.b58encode(str2bytes(unhashedAddress + addressHash)))
        return address
