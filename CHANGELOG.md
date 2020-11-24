# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[Unreleased]

## [0.4.1] - 2020-11-24
### Added
- Add PoolUpdater action for updating pools
- Add Prometheus client for exporting performance metrics
### Changed
- ActionTree now runs actions async.
- Optimize Contracts using async await.
- Optimize PoolFinder using async await.
### Removed
- Remove circuit breaker, trust retry on the request lib to keep us from failing.
### Fixed

## [0.4.0] The Pusher - 2020-11-17
### Added
- Add settings to Path Finder for choosing depth, when searching for cycles.
  So that we don't have to wait untill the heat death of the universe.
- Add possibility to specify variable creation in config.yaml.
- Make it possible to run action tree by subscribing to redis channel.
  Publish to channel when adding varaible state to redis.
### Changed
- How contract factories, web3 and redis connections are created.

### Removed
- No longer possible to save and load store state to disk. We now use redis for
  keeping track of the state.
- Address() we now use str as address representation. This integrates better with
  web3.py

## [0.3.2] - 2020-11-08
### Fixed
- Issue where names would not be added when creating Tokens from contracts.
- Issue where pools with zero balance would not be filtered by PoolFinder.

## [0.3.1] - 2020-11-07
### Added
- Add logging to file. Logging rotated between 5 1mb files.
- Make it possible to load and save arbie state on startup, exit and crash.
- Add CLI option for log path.
- Add CLI option for state save path.
- Add CLI option for state load path.

### Removed
- Move examples to [arbie-examples](https://github.com/owodunni/arbie-examples) to remove repo size and
  make it easier to keep examples up to date.

### Fixed
- Issue with pickeling store containing contracts.
- Issue with pools not normalizing to 1 and being filtered out.

## [0.3.0] - The Scraper - 2020-11-02
### Added
- Find all cycles in a set of Pools. These can then be converted to trading opertunities.
- CLI application structure. Making it possible to configure Actions from yaml config.
- Add logging framework. Making it possible to write info to console.
- Add Action for finding Pools from PoolContracts like Uniswap and Balancer.
- Make it possible to specify address to WETH in config.yaml.
- Add functionality making it possible to find all pools and pairs.

## [0.2.0] - The Base - 2020-10-12
### Added
- Smart contract wrapper for interacting with balancer and uniswap.
- Automated market maker modell called Pool. Can be used to simulate Uniswap or balancer.
- TradingGraph functionality built on top of Networkx.
- Ethereum system tests against Geth

### Changed

### Removed