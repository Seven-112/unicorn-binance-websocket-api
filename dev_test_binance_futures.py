#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: dev_test_binance_futures.py
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api
# Documentation: https://lucit-systems-and-development.github.io/unicorn-binance-websocket-api
# PyPI: https://pypi.org/project/unicorn-binance-websocket-api/
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2019-2022, LUCIT Systems and Development (https://www.lucit.tech) and Oliver Zehentleitner
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

from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager
import logging
import time
import os

logging.getLogger("unicorn_binance_websocket_api")
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com-futures")

binance_websocket_api_manager.create_stream('arr', '!miniTicker')

while True:
    if binance_websocket_api_manager.is_manager_stopping():
        exit(0)
    oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
    if oldest_stream_data_from_stream_buffer is False:
        time.sleep(0.01)
    else:
        print(f"{oldest_stream_data_from_stream_buffer}")
