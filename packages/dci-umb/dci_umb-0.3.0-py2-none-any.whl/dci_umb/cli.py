#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os

EXAMPLES = """
examples:
  # listen on virtual topic topic://VirtualTopic.dci
  # and bounce all the events to an http endpoint "http://localhost:5000/api/v1/events"
  dci-umb --key /tmp/umb.key --crt /tmp/umb.crt --ca /tmp/umb.ca --source topic://VirtualTopic.dci --destination http://localhost:5000/api/v1/events
"""

COPYRIGHT = """
copyright:
  Copyright © 2019 Red Hat.
  Licensed under the Apache License, Version 2.0
"""


def parse_arguments(arguments):
    parser = argparse.ArgumentParser(
        usage="dci-umb [OPTIONS]",
        description=" listen on virtual topic and bounce all the events",
        epilog=EXAMPLES + COPYRIGHT,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    default_key_file_path = os.environ.get("KEY_FILE_PATH", None)
    parser.add_argument(
        "--key",
        default=default_key_file_path,
        dest="key_file",
        metavar="KEY_FILE_PATH",
        help="key file to identify the connection to UMB",
    )
    default_crt_file_path = os.environ.get("CRT_FILE_PATH", None)
    parser.add_argument(
        "--crt",
        default=default_crt_file_path,
        dest="crt_file",
        metavar="CRT_FILE_PATH",
        help="cert file to identify the connection to UMB",
    )
    default_ca_file_path = os.environ.get("CA_FILE_PATH", None)
    parser.add_argument(
        "--ca",
        default=default_ca_file_path,
        dest="ca_file",
        metavar="CA_FILE_PATH",
        help="ca file to identify the connection to UMB",
    )
    default_brokers = os.environ.get("BROKERS", "").split()
    parser.add_argument(
        "--broker",
        action="append",
        metavar="BROKER",
        dest="brokers",
        default=default_brokers,
        help="amqps broker to listen to",
    )
    default_topic_source = os.environ.get("TOPIC_SOURCE", None)
    parser.add_argument(
        "--source",
        default=default_topic_source,
        dest="source",
        metavar="TOPIC_SOURCE",
        help="virtual topic source to listen to",
    )
    default_http_destination_host = os.environ.get("HTTP_DESTINATION_HOST", None)
    parser.add_argument(
        "--destination",
        default=default_http_destination_host,
        dest="destination",
        metavar="HTTP_DESTINATION_HOST",
        help="destination for the bounced events",
    )
    parsed_arguments = parser.parse_args(arguments)
    return vars(parsed_arguments)
