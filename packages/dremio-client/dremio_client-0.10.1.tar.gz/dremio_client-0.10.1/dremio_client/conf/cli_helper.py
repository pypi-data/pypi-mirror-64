# -*- coding: utf-8 -*-
from ..auth import auth

#
# Copyright (c) 2019 Ryan Murray.
#
# This file is part of Dremio Client
# (see https://github.com/rymurr/dremio_client).
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
from .config_parser import build_config


def get_base_url_token(args=None):
    config = build_config(args)
    ssl = "s" if config["ssl"].get(bool) else ""
    host = config["hostname"].get()
    port = ":" + str(config["port"].get(int))
    base_url = "http{}://{}{}".format(ssl, host, port)
    token = auth(base_url, config)
    return base_url, token, config["verify"].get()
