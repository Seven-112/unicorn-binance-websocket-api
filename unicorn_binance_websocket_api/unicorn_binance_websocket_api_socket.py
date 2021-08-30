#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_websocket_api/unicorn_binance_websocket_api_socket.py
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api
# Documentation: https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api
# PyPI: https://pypi.org/project/unicorn-binance-websocket-api/
#
# Author: Oliver Zehentleitner
#         https://about.me/oliver-zehentleitner
#
# Copyright (c) 2019-2021, Oliver Zehentleitner
# All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from __future__ import print_function
from .unicorn_binance_websocket_api_connection import BinanceWebSocketApiConnection
from unicorn_fy.unicorn_fy import UnicornFy
import ujson as json
import logging
import sys
import time
import uuid
import websockets


class BinanceWebSocketApiSocket(object):
    def __init__(self, manager, stream_id, channels, markets):
        self.manager = manager
        self.stream_id = stream_id
        self.channels = channels
        self.markets = markets
        self.socket_id = uuid.uuid4()
        self.manager.stream_list[self.stream_id]['recent_socket_id'] = self.socket_id
        self.symbols = self.manager.stream_list[self.stream_id]['symbols']
        self.output = self.manager.stream_list[self.stream_id]['output']
        self.unicorn_fy = UnicornFy()
        self.exchange = manager.get_exchange()

    async def start_socket(self):
        logging.info(f"BinanceWebSocketApiSocket.start_socket({str(self.stream_id)}, {str(self.channels)}, "
                     f"{str(self.markets)}) socket_id={str(self.socket_id)} recent_socket_id={str(self.socket_id)}")
        async with BinanceWebSocketApiConnection(self.manager,
                                                 self.stream_id,
                                                 self.socket_id,
                                                 self.channels,
                                                 self.markets,
                                                 symbols=self.symbols) as websocket:
            while True:
                if self.manager.is_stop_request(self.stream_id):
                    self.manager.stream_is_stopping(self.stream_id)
                    await websocket.close()
                    sys.exit(0)
                elif self.manager.is_stop_as_crash_request(self.stream_id):
                    await websocket.close()
                    sys.exit(1)
                try:
                    if self.manager.stream_list[self.stream_id]['recent_socket_id'] != self.socket_id:
                        logging.error(f"BinanceWebSocketApiSocket.start_socket({str(self.stream_id)}, "
                                      f"{str(self.channels)}, {str(self.markets)} socket_id={str(self.socket_id)} "
                                      f"recent_socket_id={str(self.socket_id)} - Sending payload - exit because its "
                                      f"not the recent socket id! stream_id={str(self.stream_id)}, recent_socket_id="
                                      f"{str(self.manager.stream_list[self.stream_id]['recent_socket_id'])}")
                        sys.exit(0)
                except KeyError:
                    sys.exit(1)
                while self.manager.stream_list[self.stream_id]['payload']:
                    logging.info(f"BinanceWebSocketApiSocket.start_socket({str(self.stream_id)}, "
                                 f"{str(self.channels)}, {str(self.markets)} socket_id={str(self.socket_id)} "
                                 f"recent_socket_id={str(self.socket_id)} - Sending payload started ...")
                    if self.manager.stream_list[self.stream_id]['recent_socket_id'] != self.socket_id:
                        logging.error(f"BinanceWebSocketApiSocket.start_socket({str(self.stream_id)}, "
                                      f"{str(self.channels)}, {str(self.markets)} socket_id={str(self.socket_id)} "
                                      f"recent_socket_id={str(self.socket_id)} - Sending payload - exit because its "
                                      f"not the recent socket id! stream_id={str(self.stream_id)}, recent_socket_id="
                                      f"{str(self.manager.stream_list[self.stream_id]['recent_socket_id'])}")
                        sys.exit(0)
                    payload = self.manager.stream_list[self.stream_id]['payload'].pop(0)
                    logging.info(f"BinanceWebSocketApiSocket.start_socket({str(self.stream_id)}, "
                                 f"{str(self.channels)}, {str(self.markets)} - Sending payload: {str(payload)}")
                    await websocket.send(json.dumps(payload, ensure_ascii=False))
                    # To avoid a ban we respect the limits of binance:
                    # https://github.com/binance-exchange/binance-official-api-docs/blob/5fccfd572db2f530e25e302c02be5dec12759cf9/CHANGELOG.md#2020-04-23
                    # Limit: max 5 messages per second inclusive pings/pong
                    max_subscriptions_per_second = self.manager.max_send_messages_per_second - \
                                                   self.manager.max_send_messages_per_second_reserve
                    idle_time = 1/max_subscriptions_per_second
                    time.sleep(idle_time)
                try:
                    received_stream_data_json = await websocket.receive()
                    if received_stream_data_json is not None:
                        if self.output == "UnicornFy":
                            if self.exchange == "binance.com":
                                received_stream_data = self.unicorn_fy.binance_com_websocket(received_stream_data_json)
                            elif self.exchange == "binance.com-testnet":
                                received_stream_data = self.unicorn_fy.binance_com_websocket(received_stream_data_json)
                            elif self.exchange == "binance.com-margin":
                                received_stream_data = self.unicorn_fy.binance_com_margin_websocket(received_stream_data_json)
                            elif self.exchange == "binance.com-margin-testnet":
                                received_stream_data = self.unicorn_fy.binance_com_margin_websocket(received_stream_data_json)
                            elif self.exchange == "binance.com-isolated_margin":
                                received_stream_data = self.unicorn_fy.binance_com_isolated_margin_websocket(received_stream_data_json)
                            elif self.exchange == "binance.com-isolated_margin-testnet":
                                received_stream_data = self.unicorn_fy.binance_com_isolated_margin_websocket(received_stream_data_json)
                            elif self.exchange == "binance.com-futures":
                                received_stream_data = self.unicorn_fy.binance_com_futures_websocket(received_stream_data_json)
                            elif self.exchange == "binance.com-futures-testnet":
                                received_stream_data = self.unicorn_fy.binance_com_futures_websocket(received_stream_data_json)
                            elif self.exchange == "binance.com-coin-futures":
                                received_stream_data = self.unicorn_fy.binance_com_coin_futures_websocket(received_stream_data_json)
                            elif self.exchange == "binance.je":
                                received_stream_data = self.unicorn_fy.binance_je_websocket(received_stream_data_json)
                            elif self.exchange == "binance.us":
                                received_stream_data = self.unicorn_fy.binance_us_websocket(received_stream_data_json)
                            elif self.exchange == "trbinance.com":
                                received_stream_data = self.unicorn_fy.binance_tr_websocket(received_stream_data_json)
                            elif self.exchange == "jex.com":
                                received_stream_data = self.unicorn_fy.jex_com_websocket(received_stream_data_json)
                            elif self.exchange == "binance.org":
                                received_stream_data = self.unicorn_fy.binance_org_websocket(received_stream_data_json)
                            elif self.exchange == "binance.org-testnet":
                                received_stream_data = self.unicorn_fy.binance_org_websocket(received_stream_data_json)
                            else:
                                received_stream_data = received_stream_data_json
                        elif self.output == "dict":
                            received_stream_data = json.loads(received_stream_data_json)
                        else:
                            received_stream_data = received_stream_data_json
                        try:
                            stream_buffer_name = self.manager.stream_list[self.stream_id]['stream_buffer_name']
                        except KeyError:
                            stream_buffer_name = False
                        self.manager.process_stream_data(received_stream_data,
                                                         stream_buffer_name=stream_buffer_name)
                        if "error" in received_stream_data_json:
                            logging.error("BinanceWebSocketApiSocket.start_socket(" +
                                          str(self.stream_id) + ") "
                                          "- Received error message: " + str(received_stream_data_json))
                            self.manager.add_to_ringbuffer_error(received_stream_data_json)
                        elif "result" in received_stream_data_json:
                            logging.info("BinanceWebSocketApiSocket.start_socket(" +
                                         str(self.stream_id) + ") "
                                         "- Received result message: " + str(received_stream_data_json))
                            self.manager.add_to_ringbuffer_result(received_stream_data_json)
                        else:
                            if self.manager.stream_list[self.stream_id]['last_received_data_record'] is None:
                                self.manager.process_stream_signals("FIRST_RECEIVED_DATA",
                                                                    self.stream_id,
                                                                    received_stream_data)
                            self.manager.stream_list[self.stream_id]['last_received_data_record'] = received_stream_data

                except websockets.exceptions.ConnectionClosed as error_msg:
                    logging.critical("BinanceWebSocketApiSocket.start_socket(" + str(self.stream_id) + ", " +
                                     str(self.channels) + ", " + str(self.markets) + ") - Exception ConnectionClosed "
                                     "- error_msg: " + str(error_msg))
                    if "WebSocket connection is closed: code = 1008" in str(error_msg):
                        websocket.close()
                        self.manager.stream_is_crashing(self.stream_id, error_msg)
                        self.manager.set_restart_request(self.stream_id)
                        sys.exit(1)
                    elif "WebSocket connection is closed: code = 1006" in str(error_msg):
                        self.manager.stream_is_crashing(self.stream_id, error_msg)
                        self.manager.set_restart_request(self.stream_id)
                        sys.exit(1)
                    else:
                        self.manager.stream_is_crashing(self.stream_id, str(error_msg))
                        self.manager.set_restart_request(self.stream_id)
                        sys.exit(1)
                except AttributeError as error_msg:
                    logging.error("BinanceWebSocketApiSocket.start_socket(" + str(self.stream_id) + ", " +
                                  str(self.channels) + ", " + str(self.markets) + ") - Exception AttributeError - "
                                  "error_msg: " + str(error_msg))
                    self.manager.stream_is_crashing(self.stream_id, str(error_msg))
                    self.manager.set_restart_request(self.stream_id)
                    sys.exit(1)

                except Exception as error_msg:
                    logging.error("BinanceWebSocketApiSocket.start_socket(" + str(self.stream_id) + ", " +
                                  str(self.channels) + ", " + str(self.markets) + ") - Exception General Exception - "
                                                                                  "error_msg: " + str(error_msg))
                    self.manager.stream_is_crashing(self.stream_id, str(error_msg))
                    self.manager.set_restart_request(self.stream_id)
                    sys.exit(1)
