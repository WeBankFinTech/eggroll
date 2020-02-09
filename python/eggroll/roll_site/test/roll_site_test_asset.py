#  Copyright (c) 2019 - now, Eggroll Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#


import configparser
import json
import os

import eggroll.roll_pair.test.roll_pair_test_assets as rpta
from eggroll.core.constants import StoreTypes
from eggroll.core.meta_model import ErStore, ErStoreLocator, ErEndpoint
from eggroll.roll_site.roll_site import RollSiteContext

is_standalone = False
manager_port_guest = 4671
egg_port_guest = 20003
transfer_port_guest = 20004
manager_port_host = 4670
egg_port_host = 20001
transfer_port_host = 20002
remote_parties = [('host', '10001')]
get_parties = [('guest', '10002')]

EGGROLL_HOME = os.environ['EGGROLL_HOME']

default_props_file = f"{EGGROLL_HOME}/conf/eggroll.properties"


def get_option(role, conf_file=default_props_file):
    configs = configparser.ConfigParser()

    configs.read(conf_file)
    eggroll_configs = configs['eggroll']

    options = {}
    party_id = eggroll_configs['partyId']
    options['self_party_id'] = party_id
    options['self_role'] = role

    with open(f"{EGGROLL_HOME}/conf/route_table.json") as route_table_file:
        route_table = json.load(route_table_file)["route_table"]
        proxy_endpoint = route_table[party_id]["default"][0]

        options['proxy_endpoint'] = ErEndpoint(host=proxy_endpoint["ip"], port=proxy_endpoint["port"])

    return options


host_ip = 'localhost'
guest_ip = 'localhost'
host_options = {'self_role': 'host',
                'self_party_id': 10001,
                'proxy_endpoint': ErEndpoint(host=host_ip, port=9395),
                }

guest_options = {'self_role': 'guest',
                 'self_party_id': 10002,
                 'proxy_endpoint': ErEndpoint(host=guest_ip, port=9396),
                 }



ER_STORE1 = ErStore(
        store_locator=ErStoreLocator(store_type=StoreTypes.ROLLPAIR_LEVELDB,
                                     namespace="namespace",
                                     name="name"))


def get_debug_test_context(is_standalone=False,
        manager_port=4670,
        egg_port=20001,
        transfer_port=20002,
        session_id='testing',
        role='host',
        props_file=default_props_file):
    rp_context = rpta.get_debug_test_context(is_standalone=is_standalone,
                                             manager_port=manager_port,
                                             egg_port=egg_port,
                                             transfer_port=transfer_port,
                                             session_id=session_id)

    rs_context = RollSiteContext("atest", options=get_option(role, props_file),
                                 rp_ctx=rp_context)

    return rs_context


def get_standalone_context(role, props_file=default_props_file):
    rp_context = rpta.get_standalone_context()
    rs_context = RollSiteContext("atest", options=get_option(role, props_file),
                                 rp_ctx=rp_context)

    return rs_context


def get_cluster_context(role, options: dict = None, props_file=default_props_file):
    if options is None:
        options = {}
    rp_context = rpta.get_cluster_context(options=options)
    rs_context = RollSiteContext("atest", options=get_option(role, props_file),
                                 rp_ctx=rp_context)

    return rs_context


if __name__ == "__main__":
    options = get_option()
    print(options)
