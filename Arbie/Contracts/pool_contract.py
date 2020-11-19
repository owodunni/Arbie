"""Base abstract class for pool contracts."""

from math import isclose
from typing import List

from asyncstdlib.builtins import list as alist
from asyncstdlib.builtins import map as amap

from Arbie import PoolValueError
from Arbie.Contracts.contract import Contract
from Arbie.Contracts.tokens import GenericToken
from Arbie.Variables import BigNumber, Pool, Token


async def create_token(token_contract: GenericToken):
    return await token_contract.create_token()


class PoolContract(Contract):
    def get_tokens(self) -> List[GenericToken]:
        raise NotImplementedError()

    def get_balances(self) -> List[BigNumber]:
        raise NotImplementedError()

    def get_weights(self) -> List[float]:
        raise NotImplementedError()

    def get_fee(self) -> float:
        raise NotImplementedError()

    async def create_tokens(self) -> List[Token]:
        return await alist(amap(create_token, self.get_tokens()))

    async def create_pool(self) -> Pool:
        tokens = await self.create_tokens()
        if len(tokens) < 2:
            raise PoolValueError(
                f"Pool: {self.get_address}, has insufficient tokens: {len(tokens)}"
            )
        balances_bg = await self.get_balances()
        balances = list(map((lambda bg: bg.to_number()), balances_bg))
        if isclose(sum(balances), 0, abs_tol=1e-3):  # noqa: WPS432
            raise PoolValueError(
                f"Pool: {self.get_address}, balances {sum(balances)} == 0"
            )

        weights = self.get_weights()
        if not isclose(sum(weights), 1, abs_tol=1e-3):  # noqa: WPS432
            raise PoolValueError(
                f"Pool: {self.get_address}, weights {sum(weights)} != 1"
            )
        return Pool(
            tokens,
            balances,
            weights,
            self.get_fee(),
            address=self.get_address(),
        )
