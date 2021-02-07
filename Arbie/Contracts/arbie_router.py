"""Utility functions for interacting with Arbie.sol."""

import logging

from Arbie.Contracts.contract import Contract
from Arbie.Contracts.tokens import GenericToken
from Arbie.Variables import BigNumber, Trade

logger = logging.getLogger()


class ArbieRouter(Contract):
    name = "ArbieRouter"
    protocol = "arbie"

    def check_out_given_in(self, trade: Trade):
        return self.router.check_out_given_in(trade)

    def safe_swap(self, trade, dry_run=False):
        return self.router.swap(trade, dry_run)

    def approve(self, weth: GenericToken):
        if weth.allowance(self.get_address()) < BigNumber(10e6):  # noqa: WPS432
            return weth.approve(self.get_address(), BigNumber(10e8))  # noqa: WPS432
        return True

    def swap(self, trade, amounts, dry_run=False):
        return self._transact_info(self._swap_transaction(trade, amounts), dry_run=dry_run)

    def _swap_transaction(self, trade: Trade, amounts):
        pools = list(map(lambda p: p.address, trade.pools))
        path = list(map(lambda t: t.address, trade.path))
        return self.contract.functions.swap(
            amounts,
            pools,
            path,
        )
