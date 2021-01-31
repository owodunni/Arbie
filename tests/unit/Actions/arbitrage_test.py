"""Unittest of arbitrage."""

import pytest

from Arbie.Actions import ActionTree, Store
from Arbie.Actions.arbitrage import Arbitrage, ArbitrageFinder
from Arbie.address import dummy_token_generator
from Arbie.Variables import Pool, Trade


@pytest.fixture
def tokens(dai, eth):
    return [dai, eth]


@pytest.fixture
def trade1(tokens, dai, eth):
    pool1 = Pool(tokens, [400, 1], [0.5, 0.5])
    pool2 = Pool(tokens, [410, 1], [0.5, 0.5])
    return Trade([pool1, pool2], [dai, eth, dai])


@pytest.fixture
def trade2(tokens, dai, eth):
    pool1 = Pool(tokens, [400, 1], [0.9, 0.1])
    pool2 = Pool(tokens, [410, 1], [0.1, 0.9])
    return Trade([pool1, pool2], [dai, eth, dai])


class TestArbitrage(object):
    """Test Arbitrage."""

    def test_find_arbitrage(self, trade1):
        amount, _ = ArbitrageFinder(trade1).find_arbitrage()
        assert amount == pytest.approx(2.48456731316587)  # noqa: WPS432

    def test_find_arbitrage_unbalanced(self, trade2):
        amount, _ = ArbitrageFinder(trade2).find_arbitrage()
        assert amount == pytest.approx(27.8547574719045)  # noqa: WPS432

    def test_find_arbitrage_no_opportunity(self, tokens, dai, eth):
        pool1 = Pool(tokens, [400, 1], [0.9, 0.1])
        pool2 = Pool(tokens, [410, 1], [0.1, 0.9])
        trade = [Trade(pool1, eth, dai), Trade(pool2, dai, eth)]

        with pytest.raises(ValueError):
            ArbitrageFinder(trade).find_arbitrage()

    def test_calc_optimal_arbitrage_no_opportunity(self, tokens, dai, eth):
        pool1 = Pool(tokens, [400, 1], [0.9, 0.1])
        pool2 = Pool(tokens, [410, 1], [0.1, 0.9])
        trade = Trade([pool1, pool2], [eth, dai, eth])

        with pytest.raises(ValueError) as e:
            ArbitrageFinder(trade).calculate_optimal_arbitrage()
            assert e.message == "No arbitrage opportunity found."

    def test_find_arbitrage_wrong_token(self, tokens, dai):
        pool1 = Pool(tokens, [400, 1], [0.9, 0.1])
        pool2 = Pool(tokens, [410, 1], [0.1, 0.9])
        sai = dummy_token_generator("sai", 300.0)
        trade = Trade([pool1, pool2], [dai, sai, dai])

        with pytest.raises(ValueError):
            ArbitrageFinder(trade).find_arbitrage()

    def test_find_arbitrage_hard(self):
        weth = dummy_token_generator('Weth', 0)
        dai = dummy_token_generator('Dai', 0)
        wbtc = dummy_token_generator('Wbtc', 0)
        pool_dai_weth = Pool([dai, weth], [1E9, 1E7/3], [0.5, 0.5], fee=0.003)
        pool_wbtc_dai = Pool([wbtc, dai], [1E5, 1E9], [0.5, 0.5], fee=0.003)
        pool_wbtc_weth = Pool([wbtc, weth], [1E5, 3508772], [0.5, 0.5], fee=0.003)

        trade = Trade([pool_dai_weth, pool_wbtc_dai, pool_wbtc_weth], [weth, dai, wbtc, weth])
        trade.amount_in, trade.profit = ArbitrageFinder(trade).find_arbitrage()

        assert trade.profit == pytest.approx(510.233038753510)


class TestArbitrageAction(object):
    @pytest.mark.asyncio
    async def test_on_next(self, trade1, trade2):
        store = Store()
        store.add("all_trades", [trade1, trade2])
        tree = ActionTree(store)
        tree.add_action(Arbitrage())
        await tree.run()

        assert len(store.get("filtered_trades")) == 2
