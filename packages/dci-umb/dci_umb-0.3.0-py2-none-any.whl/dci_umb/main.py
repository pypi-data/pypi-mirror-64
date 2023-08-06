# Copyright 2019 Red Hat
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
import logging
import sys

from proton.reactor import Container

from dci_umb.receiver import Receiver
from dci_umb.cli import parse_arguments


def main():
    arguments = sys.argv[1:]
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    try:
        cli_arguments = parse_arguments(arguments)
        Container(Receiver(cli_arguments)).run()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
