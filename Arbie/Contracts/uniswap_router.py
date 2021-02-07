"""Utility functions for interacting with Uniswap router."""
import logging
from typing import Tuple

from Arbie.Contracts.contract import Contract
from Arbie.Contracts.tokens import GenericToken
from Arbie.Variables import BigNumber, Trade

logger = logging.getLogger()


class UniswapV2Router(Contract):
    name = "UniswapV2Router02"
    protocol = "uniswap"

    def approve(self, weth: GenericToken):
        if weth.allowance(self.get_address()) < BigNumber(10e6):  # noqa: WPS432
            return weth.approve(self.get_address(), BigNumber(10e8))  # noqa: WPS432
        return True

    def check_out_given_in(self, trade: Trade):
        path_address = list(map(lambda t: t.address, trade.path))
        amount_out = self.contract.functions.getAmountsOut(
            BigNumber(trade.amount_in).value, path_address
        ).call()
        return BigNumber.from_value(amount_out[-1]).to_number(), amount_out

    def safe_swap(self, trade, dry_run=False):
        return self.swap(trade, dry_run)

    def swap(self, trade, dry_run=False) -> Tuple[bool, float]:
        return self._transact_info(self._swap_transaction(trade), dry_run=dry_run)

    def _swap_transaction(self, trade):
        path = list(map(lambda t: t.address, trade.path))
        return self.contract.functions.swapExactTokensForTokens(
            BigNumber(trade.amount_in).value,
            BigNumber(trade.amount_in).value,
            path,
            self._get_account(),
            self.w3.eth.getBlock("latest").timestamp + self.timeout,
        )
