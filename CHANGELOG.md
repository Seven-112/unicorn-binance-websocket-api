# unicorn-binance-websocket-api Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to 
[Semantic Versioning](http://semver.org/).

## 1.28.0.dev (development stage/unreleased/unstable)

## 1.28.0
### Changed
- the stream signal `DISCONNECT` includes `last_received_data_record` which returns now `None` if there is no record available
### Fixed
- Cannot use `in` with RuntimeError, must convert to string first. [PR#136 thx @Bosma](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/pull/136)
### Removed
- Deprecated methods `set_private_api_config()` and `get_websocket_uri_length()`

## 1.27.0
### Added
- `timeout=10` to [`get_result_by_request_id()`](https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.get_result_by_request_id): 
  Wait for `timeout` seconds to receive the requested result or return `False`
- logging the use of stream_buffer or process_stream_data and the used OS plattform
- individual `max_subscriptions_per_stream` for each endpoint
- `stream_signal_buffer` to receive signals if a stream gets connected or disconnected
- ['add_to_stream_signal_buffer()'](https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html?highlight=add_to_stream_signal_buffer#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.add_to_stream_signal_buffer)
- ['pop_stream_signal_from_stream_signal_buffer()'](https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html?highlight=pop_stream_signal#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.pop_stream_signal_from_stream_signal_buffer)
- Support for stream signals: `CONNECT`, `DISCONNECT`, `FIRST_RECEIVED_DATA` 
### Changed
- max subscriptions of futures endpoints to 200 [issue#127](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/127)
- max subscriptions of jex endpoint to 10
### Fixed
-  Added a gracefull shutdown if the Python interpreter dies [issue#131](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/131)
 
## 1.26.0
### Added
- parameter `ping_interval`, `ping_timeout`, `close_timeout` to [`manager.create_stream()`](https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html?highlight=create_stream#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.create_stream)
  and [`replace_stream()`](https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html?highlight=replace_stream#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.replace_stream)
- show `ping_interval`, `ping_timeout`, `close_timeout` in [`print_stream_info()`](https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html?highlight=print_stream_info#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.print_stream_info)
- `manager.set_heartbeat()` to `connection.send()`
- [`get_result_by_request_id()`](https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.get_result_by_request_id)
### Changed
- log warning about high cpu usage is logged after 5 seconds if > 95% 

## 1.25.0
### Added
- [`get_user_agent()`](https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.get_user_agent)
### Changed
- `get_stream_subscriptions()` returns now the used `request_id` instead of `True`

## 1.24.0
### Added
- [`output_default`](https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html?highlight=output_default)
  to `BinanceWebSocketApiManager` 
### Removed
- unused import of `ujson` in connection class
- 4 parameters from `_create_stream_thread`

## 1.23.0
### Added
- timestamp to `receiving_speed_peak` in manager
- log warning if the cpu usage is > 95%
- logging.info if new `highest_receiving_speed` is reached
### Fixed
- `listen_key` was printed to logfiles
- `listen_key` cache time was not set in `get_listen_key()` so it pinged immediately after its creation again, which caused
a higher weight
- restart stream if "The future belongs to a different loop than the one specified as the loop argument" [issue#121](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/121)
### Changed
- renamed `_add_socket_to_socket_list` to `_add_stream_to_stream_list`
 
## 1.22.0
### Added
- `get_current_receiving_speed_global()`
- better logging in socket class
- `highest_receiving_speed` in `print_summary()`
### Changed
- renamed variable `ubwa` to `manager` in restclient class
- renamed variable `unicorn_binance_websocket_api_manager` to `manager` in socket class
- renamed variable `total_receiving_speed` to `average_receiving_speed`
- renamed variable `unicorn_binance_websocket_api_connection` to `connection`
- renamed variable `unicorn_binance_websocket_api_socket` to `socket`
- shorted user agent string for rest and websocket client
### Removed
- removed the sending of the payload in __aenter__ in connection class, from now on its only done in the socket class!
 
## 1.21.0
### Added 
- `is_update_availabe_unicorn_fy()` and `get_version_unicorn_fy()`
- `new_output` to [`replace_stream()`](https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html?highlight=replace_stream#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.replace_stream)
### Changed
- Rewrite of `BinanceWebSocketApiRestclient()`, its more or less stateless but compatible to the current system. Now 
we use one instance globally instead of creating a new one every time we need it. It will help to implement isolated
margin with more than one symbol. [issue#111](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/111)
- `time.sleep()` in `_frequent_checks()` from 0.1 to 0.3 seconds
### Fixed
- `RuntimeError` exception in `_create_stream_thread()` - no handling added, only logging and a "Todo"

## 1.20.0
### Added
- `dict` to [`create_stream(output='dict')`](https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.create_stream)
### Fixed
- StreamBuffer reset on restart [issue#119](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/119)
 
## 1.19.0
### Added
- [`UnicornFy`](https://github.com/oliver-zehentleitner/unicorn-fy) to 
[`create_stream(output='UnicornFy')`](https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.create_stream)
### Changed
- Links in docstrings

## 1.18.2
### Fixed
- added KeyError exception and `return False` to a few methods
- binance endpoints expects `symbol` not `symbols`
- RuntimeException in `close()`

## 1.18.1
### Fixed
- restclient: `symbol` to `symbols` 

## 1.18.0
### Added
- binance.com testnets (spot, margin, isolated_margin, future)
- `show_secrets_in_logs` parameter 
### Changed
- `symbol` to `symbols` (isolated_margin)
### Fixed
- update `binance_api_status`

## 1.17.4
### Added
- `replace_stream()`: new_stream_label=None, new_stream_buffer_name=False, new_symbol=False, new_api_key=False, 
new_api_secret=False
### Fixed 
- reconnect counter (bug since 1.17.0)

## 1.17.3
### Fixed
- [issue #109](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/109)
- [issue #110](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/110)

## 1.17.2
### Added 
- Handling of unknown error msg from Binance if uri = dict in connection class

## 1.17.1
### Fixed
- reference of api_key and secret in connection class

## 1.17.0
### Added
- Isolated margin endpoints [issue #109](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/109)
- Support for `@arr@@s1` [issue #101](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/101)
- Added `symbol` to `print_stream_info()`
- Added `api_key` and `api_secret` to `create_stream()` [issue #84](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/84) 

## 1.16.9
### Added
- Restart to ssl.SSLError exception in connection
### Removed
- error 2 code [PR #98](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/pull/98) (Thanks Flowelcat)

## 1.16.7
### Added
- Restart again if OSError in `BinanceWebSocketApiConnection()`
### Changed
- Logging in `BinanceWebSocketApiConnection()`

## 1.16.6
### Changed
- Loglevels
### Fixed
- Fixed exception that thrown when api key is real but was deleted from binance. [PR #96](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/pull/96) (Thanks Flowelcat)
- Package configuration is wrong. Currently one needs to have the bin-folder of the venv in the PATH. That is not feasible since you often have one venv per project. [PR #97](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/pull/97) (Thanks uggel)

## 1.16.5
- REMOVED

## 1.16.4
### Changed
- Loglevels
### Fixed
- Fixed double slash bug when getting listen key for userDataStream. 
[PR #87](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/pull/87) 
- Fixed RuntimeError in connection row 243 (added restart)

## 1.16.3
### Fixed
- restart if "with connection" in socket gets closed
- exception json.decoder.JSONDecodeError: respond = request_handler.json() 

## 1.16.2
### Fixed
- Exception AttributeError Info: module 'asyncio.base_futures' has no attribute 'InvalidStateError' [issue #72](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/83)

## 1.16.1
### Fixed
- exception in `print_suammary()`

## 1.16.0
### Added
- stream_buffer control: create_stream(channels, markets, stream_buffer_name=None): 
If `False` the data is going to get written to the default stream_buffer, set to `True` to read the data via 
`pop_stream_data_from_stream_buffer(stream_id)` or provide a string to create and use a shared stream_buffer 
and read it via `pop_stream_data_from_stream_buffer('string')`.
- `add_to_ringbuffer_error()`
- `add_to_ringbuffer_result()`
- `set_ringbuffer_error_max_size()`
- `set_ringbuffer_result_max_size()`
- `get_errors_from_endpoints()`
- `get_results_from_endpoints()`
- `get_ringbuffer_error_max_size()`
- `get_ringbuffer_result_max_size()`
### Changed
- renamed `restart_stream()` to `_restart_stream` and execute it only with a valid restart_request
### Fixed
- Ensure that during a restart, only the recent thread is able to send the payload for subscription

## 1.15.0
### Added 
- psutil (new requirement)
- exception handling of `websockets.exceptions.InvalidMessage` [issue #72](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/72)
- general exception handling
- show threads, memory and cpu usage in `print_summary()`
- `get_process_usage_memory()`
- `get_process_usage_cpu()`
- `get_process_usage_threads()`
### Fixed
- Close WS only if open in connection class row 190 [issue #72](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/72)
### Removed
- some code in connection row 206 which is not needed anymore and is causing a coroutine error
- `is_websocket_uri_length_valid()`

## 1.14.0
### Added
- new parameter `stream_label` in `manager.create_stream()`[issue #60](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/60)
- `manager.get_stream_label()` [issue #60](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/60)
- `manager.get_stream_id_by_label()` [issue #60](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/60)
- `manager.set_stream_label()` [issue #60](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/60)
- added `stream_label` to `manager.print_stream_info()` [issue #60](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/60)
- added `stream_label` to `manager.print_summary()` [issue #60](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/60)
- `manager.help()`
- `unicorn_binance_websocket_api_exceptions.py` with exception `StreamRecoveryError` and `UnknownExchange`
- `fill_up_space_right()`
- `self.restart_timeout`
### Changed
- raising `UnknownExchange` or `StreamRecoveryError` instead of `ValueError`
- `fill_up_space()` to `fill_up_space_left()`
### Fixed
- reset the payloads of a stream at a stream restart
- moved some code for a stream restart from `_keepalive_streams()` to `restart_stream()` which caused that the direct
call of `restart_stream()` worked only inside of `_keepalive_streams()`
- handling of `RuntimeWarning` in class connection at row 189
### Removed
- code to start new `_keepalive_streams()` and `_frequent_checks()` threads

## 1.13.0
### Added
- `disable_print` in `print_summary()` [pull #48](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/pull/48)
- `print_summary_export_path` - if provided, the lib is going to export the output of `print_summary()` to a PNG image.
- `get_number_of_all_subscriptions()` and show all subscriptions number in `print_summary()`
### Fixed
- ping listen_key if "!userData" is in `channels`, not only in `markets`. 
- format of some logs
- stream buffer size [issue #51](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/51),
 [pull #51](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/pull/52)

## 1.12.0
### RECOMMENDED UPDATE!
https://github.com/binance-exchange/binance-official-api-docs/blob/5fccfd572db2f530e25e302c02be5dec12759cf9/CHANGELOG.md#2020-04-23
### Added
- avoid sending more than 5 messages per stream per second [issue #45](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/45)
- stop streams and set status to "crashed" if they exceed the limit of 1024 subscriptions per stream [issue #45](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/45)
    - `is_stop_as_crash_request()`
    - `stop_stream_as_crash()`
- `get_limit_of_subscriptions_per_stream()`
- `get_number_of_free_subscription_slots()`
- `BinanceWebSocketApiManager(throw_exception_if_unrepairable=True)` - raise `StreamRecoveryError` if a stream is not repairable 
(invalid api-key format or exceeding the 1024 subscription limit)

### Changed
- loglevel `connection.send()` loglevels from error to critical.
- loglevel `manager.create_websocket_uri()` of known errors from error to critical.
### Fixed
- `OSError` exception for `self.monitoring_api_server.start()` if its already started
- `for keepalive_streams_id in self.keepalive_streams_list:` added threadding lock ([issue #47](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/47))

## 1.11.0
### Added
- binance jex
### Changed
- dependency websockets from 7.0 to 8.1 which needs python>=3.6.1 ([issue #11](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/11))
### Fixed
- expception handling of send() ([issue #43](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/43))
- thread lock for `frequent_checks_list` ([comment #590914274](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/11#issuecomment-590914274))
- `current_receiving_speed` did not reset to 0 if all streams are offline

## 1.10.6
### Added
- fill_up_space_centered()
- update check on manager start
### Changed
- print_stream_info() and print_summary(): unicorn-binance-websocket-api_<version>-python_<version> in top boarder row
- count subscriptions
### Fixed
- lower for cex and upper for dex with exceptions for arr, $all, ! and array channels

## 1.10.5
### Fixed
- `lower()` markets in `create_payload()` and exception for `!userData`
- get_active_stream_list() took len() of false item
- reconnect handling in send() ([issue #40](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/40))

## 1.10.4
### Changed
- making `self.stream_buffer` thread safe

## 1.10.3
### Changed
- removed simplejson exception in restclient
- set OSError from error to critical

## 1.10.2
### Fixed
- `['receives_statistic_last_second']` dict is changing size during iteration. ([issue #37](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/37))

## 1.10.1
### Changed
- Using ujson instead of stock json lib
- cleaning `create_payload()` for CEX 

## 1.10.0
### Important infos, [please read!](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/38)
### Added
- `unicorn_binance_websocket_api_manager.is_exchange_type()`
- support for subscribe/unsubscribe for CEX websockets
- `unicorn_binance_websocket_api_manager.get_stream_subscriptions()`
- `unicorn_binance_websocket_api_manager.increase_transmitted_counter()` and added output to 
  `print_summary()` and `print_stream_info()` 
- `split_payload()`
### Changed
- The 8004 char limit for URIs on websocket connect is bypassed via subscriptions with websocket.send() and 
`is_websocket_uri_length_valid()` allways returns `True` now!
### Fixed
- Subscribe/unsubscribe items of DEX websockets ([card #5](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/projects/5#card-23700264))
- `['receives_statistic_last_second']` dict is changing size during iteration. ([issue #37](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/37))

## 1.9.1
### Added
- Python version in print_stream_info() and print_summary()
### Fixed 
- Typo in text string

## 1.9.0
### Added 
- Endpoints for www.binance.com margin UserData listenkey ([issue #35](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/35))
### Changed
- Endpoints for www.binance.com spot UserData listenkey ([issue #35](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/35))
- Endpoints for www.binance.com futures UserData listenkey ([issue #35](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/35))

## 1.8.2
### Fixed
- Errors when creating private DEX streams ([issue #34](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/34))

## 1.8.1
### Changed
- Moved docs to github pages

## 1.8.0
### Added 
- binance.com Futures websocket support and [example_binance_futures.py](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/blob/master/example_binance_futures.py) and [example_bookticker.py](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/blob/master/example_bookticker.py) ([issue#32](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/32))

## 1.7.0
### Added 
- binance.us websocket support and [example_binance_us.py](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/blob/master/example_binance_us.py) ([issue#22](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/22))

## 1.6.6
### Fixed
- Trailing / is no longer accepted by the endpoints: 
https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/31

## 1.6.5
### Fixed
- 'websockets>=7.0' to 'websockets==7.0': Websockets 8 is released and it seems to be not compatible

## 1.6.4
### Added
- Amount of active streams to icinga status msg
### Fix
- RuntimeError in _frequent_checks

## 1.6.3
### Fix
- 'except websockets.exceptions.InvalidStatusCode as error_msg:' moved to right place 

## 1.6.2
### Fix
- 'except websockets.exceptions.InvalidStatusCode as error_msg:' in connnection line 97 with restart
- 'except KeyError:' in connection line 162

## 1.6.1
### Fix
- get_monitoring_status_plain(): exception for outdated UnicornFy

## 1.6.0
### Added
- is_update_availabe_check_command()
- get_latest_version_check_command()
- get_latest_release_info_check_command()
### Changed
- get_monitoring_status_plain()
- get_monitoring_status_icinga()
- _start_monitoring_api()
### Removed!
- https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/blob/master/tools/icinga/ 
(to https://github.com/oliver-zehentleitner/check_unicorn_monitoring_api)

## 1.5.0
### Added 
- support for binance.org and testnet.binance.org websockets
- exchange name to icinga status msg
- binance_manager init: throw exception for unknown exchanges
- get_current_receiving_speed()
- exchange name and lib version to print_stream_info()
- current_receiving_speed to print_summary() and print_stream_info()
- get_exchange()
- set_private_dex_config() **(not in use for now)**
- subscribe_to_stream() - **(dont use in productive! Its not clean and will get rewritten and maybe change behaviour)**
- unsubscribe_from_stream() - **(dont use in productive! Its not clean and will get rewritten and maybe change change 
behaviour)**
- _create_payload()
### Changed 
- rewrite create_websocket_url(): 
    1. a multiplex socket now returns false if it includes a single stream type like !userData, !Ticker or !miniTicker
    2. added support for binance.org Binance Chain DEX
- is_websocket_uri_length_valid() now always returns True for DEX websockets

## 1.4.0
### Added 
- support for binance.je (Binance Jersey) websockets
- logging on failure in `create_stream()`
- `add_string` in `print_summary()` and `print_stream_info()`
- `warn_on_update` in `get_monitoring_status_icinga()`, `get_monitoring_status_plain()` and `start_monitoring_api()`
- support for binance jersey https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/21
- show the used exchange in `print_summary()` and `print_stream_info()`
### Fixed
- removed space from `total_received_length` in `get_monitoring_status_icinga()` to avoid 'no data' error in ICINGA

## 1.3.10
### Added
- exception for `asyncio.base_futures.InvalidStateError` by DaWe35 
https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/18
### Changed
- create_stream() returns False if websocket URL is to long
### Fixed
- `is_websocket_uri_length_valid()` to work with !userData on the pre test in `create_stream()` without api secrets

## 1.3.9
### Changed
- Docstrings for `markets` and `channels` to support: str, tuple, list, set
- Fine tuning of perfdata output in `get_monitoring_status_plain()` and `get_monitoring_status_icinga()`

## 1.3.8
### Added
- `get_stream_buffer_length()` by DaWe35 https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/pull/12
### Fixed
- the `stream_buffer` FIFO stack was a LIFO stack (Thanks to DaWe35 for recognizing and fixing this issue 
https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/pull/12)
- `get_stream_buffer_byte_size` returns now the real size of the stream_buffer

## 1.3.7
### Changed
- added round received items to 2 decimals instead of 0

## 1.3.6
- wrong version in manager class ...

## 1.3.5
### Added
- is_manager_stopping()
### Fixed
- is_update_available returns False if github API is not available.

## 1.3.4
### Changed
- get_monitoring_status_icinga(): update check

## 1.3.3
### Added
- get_monitoring_status_icinga(): reconnects and update check
- get_monitoring_status_plain()
- start_monitoring_api()
- 1 hour cache for release checks on github
- stop_monitoring_api()
### Rewrite
- ./tools/icinga/check_binance_websocket_api_manager (check_command for ICINGA)
### Changed 
- example_monitoring.py

## 1.3.2
### Added
- example_monitoring.py and tools/check_binance_websocket_api_manager
- get_monitoring_status_icinga tests for available updates and changes the `return_code` to WARNING if an update is 
available. but i recognized an API ban from github in cause of too many requests. i have to extend it ...
### Changed
- get_monitoring_status_icinga: changed `status` dict node to `return_code`

## 1.3.1
### Changed
- changing output of get_monitoring_status_icinga

## 1.3.0
### Added
- get_monitoring_status_icinga() in manager class

## 1.2.8
### Added
- lib version to print_summary()
### Fixed
- Typo in text in print_summary()
- KeyError in manager class row 148

## 1.2.7
### Fixed
- Bug in class UnicornFy: kline_close_time had the value kline_start_time
### Changed
- Moved UnicornFy from UNICORN Binance WebSocket API to its own [repository](https://github.com/oliver-zehentleitner/unicorn-fy) 
- connection handling (improved)

## 1.2.6
### Fixed
- `markets` in keepalive listen_key can come as str or as list and the routine only handled it as list, now str gets 
converted to list to keep the function working

## 1.2.5
### Added 
- "UTC" text to printed times
### Fixed
- listen_key 30 min cache

## 1.2.4
### Added 
- method to delete a listen_key
- binance_api_status added to print_stream_info()
### Changed
- README.md

## 1.2.3
### Changed
- rewrite coloring for status_code in print_summary
- ping_interval from None to 20 seconds
### Fixed
- listen_key keepalive didnt work propper

## 1.2.2
### Fixed
- TypeError in print_summary()

## 1.2.1
### Added 
- handling for status_code and used_weight from the binance REST Api (used for listen_key) - see `get_binance_api_status()`
### Fixed
- reconnect issues
### Changed
- log levels

## 1.2.0
### Changed
- if no method is provided to BinanceWebSocketApiManager when creating the instance, then all data will be written to 
the stream_buffer.
- comments and code in examples

## 1.1.20
### Changed
- show stream_buffer content if items len > 50
### Removed
- removed stream_buffer log

## 1.1.19
### Change
- renamed get_stream_data_from_stream_buffer to pop_stream_data_from_stream_buffer 
### Fixed 
- IndexError in pop_stream_data_from_stream_buffer

## 1.1.18
### Removed
- _forward_stream_buffer_data: system change - no pushing anymore, its better to buffer everything and run a import class
 in a separate thread, that is able to reconnect to the database

## 1.1.17
### Changed
- rewrite of keepalive and frequentchecks restarts

## 1.1.16
### Changed 
- stream_buffer logging: log amount of items in buffer

## 1.1.15
### Changed 
- stream_buffer logging: log amount of items in buffer
### Fixed
- added two mac os specific exceptions to connection class for better reconnect management

## 1.1.14
### Fixed
- updated the "update" methods in manager class (error handling while no internet connection)
- trying other behaviour on `400 - bad request' error 
- added handling for -2015 error from get_listen_key_from_restclient in create_websocket_uri

## 1.1.13
### Changed
- changed the waiting time before setting a restart request on 400 error to 5 seconds in connection class
### Fixed
- replaced tabs in print_summary() with blanks

## 1.1.12
### Fixed
- KeyError in unicorn_binance_websocket_api_connection.py error exception 414
- UnicornFy was very buggy with ticker and miniTicker handling

## 1.1.11
### Fixed
- KeyError in unicorn_binance_websocket_api_manager.py

## 1.1.10
### Added
- restarting streams row to print_summary()
- show active restarting and stopped streams only if not 0
- error message handling for userData streams
- reconnect depends from disconnect reason now (network or api-settings)
### Fixed
- del restart request in stop_stream()

## 1.1.9
### Fixed
- !miniTicker and !userData didnt work in cause of lower case all currencies. added an exception for them.

## 1.1.8
### Added
- pypi_install_packaging_tools.sh
### Changed
- README.md
- Removed 2nd argument from binance_websocket_api_manager.stream_is_stopping()
### Fixed
- Tabs in print_summary() for windows platform
- Fixing format errors from auto reformat in unicorn_binance_websocket_api_connection

## 1.1.7 failed build

## 1.1.6
### Fixed
- Catching "ssl.SSLError" BinanceWebSocketApiConnection.receive()
- Improvment of reconnect on invalid URI caused by no network issue and a missing listen_key from Binance

## 1.1.5
### Added
- 30 min cache for Binance "listenKey" from rest api to avoid weight costs and hammering the Binance API on a 
flapping network connection
### Fixed
- Reconnect issue on userData stream
- Reset "has_stopped" attr from "stream_list" after a conncection restart
- Modyfied docstrings descriptions
- Tabs in print_summary() on windows
