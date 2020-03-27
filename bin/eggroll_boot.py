import os
import argparse
import sys

def eggroll_boot(module, sub_cmd, config_file, session_id, server_node_id, processor_id, port, transfer_port, pname):
    #if module == "egg_pair":
    if "egg_pair" in module:
        import roll_pair.egg_pair_bootstrap as bootstrap
    #elif module == "roll_pair_master_bootstrap":
    if "roll_pair_master_bootstrap" in module:
        import roll_pair.roll_pair_master_bootstrap as bootstrap

    if sub_cmd == "start":
        bootstrap.start(config_file, session_id, server_node_id, processor_id, port, transfer_port, pname)

    elif sub_cmd == "stop":
        pid_file = os.path.join('bin', 'pid', pname+'.pid')
        with open(pid_file, 'r') as file_to_read:
          pid = file_to_read.readline()
        bootstrap.stop(pid)

    elif sub_cmd == "kill":
        pid_file = os.path.join('bin', 'pid', pname+'.pid')
        with open(pid_file, 'r') as file_to_read:
          pid = file_to_read.readline()
        bootstrap.kill(pid)

if __name__ == '__main__':
    '''
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('-module', '--module')
    args_parser.add_argument('-sub_cmd', '--sub_cmd')
    args_parser.add_argument('-config', '--config')
    args_parser.add_argument('-s', '--session-id')
    args_parser.add_argument('-sn', '--server-node-id')
    args_parser.add_argument('-prid', '--processor-id')
    args_parser.add_argument('-port', '--port')
    args_parser.add_argument('-trans_portid', '--transfer-port-id')
    args_parser.add_argument('-pname', '--pname')

    args = args_parser.parse_args()

    module = args.module
    sub_cmd = args.sub_cmd
    #exe = args.exe
    pname = args.pname


    config_file = args.config
    session_id = args.session_id
    server_node_id = args.server_node_id
    processor_id = args.processor_id
    port = args.port
    transfer_port = args.transfer_port_id
    '''
    print("hwz:", sys.argv[1])
    sub_cmd = sys.argv[1]
    exe = sys.argv[2]
    pname = sys.argv[3]

    params = exe.split(" ")
    module = params[0]
    config_file = params[2]
    session_id = params[4]
    server_node_id = params[6]
    processor_id = params[8]

    eggroll_boot(module, sub_cmd, config_file, session_id, server_node_id, processor_id, port=None, transfer_port=None, pname=pname)
