#!/usr/bin/env python3
'''
DBaaS tunnel
'''

import click
import logging
import yaml
import re
import os
import getpass
import signal
import subprocess
import socket
import time

from click import ClickException

CONFIG_DIR_PATH = click.get_app_dir('piu')
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR_PATH, 'piu.yaml')
ODD_USERNAME = 'odd'


def do_nothing(signum, frame):
    pass


def load_config(path, **kwargs):
    try:
        with open(path, 'rb') as fd:
            config = yaml.safe_load(fd)
    except:
        config = {}

    for k, v in kwargs.items():
        if v:
            config[k] = v

    return config


@click.command(epilog="""
Examples:

\b
    $ gotthard 172.31.150.202 pg_isready
    localhost:50474 - accepting connections

\b
    $ gotthard mydb.team.example.com -- psql -c "SELECT clock_timestamp(), current_user" -XAt
    2016-06-03 09:21:14.68289+00|myuser

    $ gotthard mydb.team.example.com
""")
@click.option('--config-file', '-c', help='Use alternative piu configuration file', default=CONFIG_FILE_PATH,
              metavar='PATH')
@click.option('-O', '--odd-host', help='Odd SSH bastion hostname', envvar='ODD_HOST', metavar='HOSTNAME')
@click.option('-U', '--user', help='Username to use for connecting', envvar='PIU_USER', metavar='NAME')
@click.option('-S', '--spilo-stack-name', help='Name for spilo stacks', default="spilo", type=str)
@click.option('-p', '--port', help='Remote port to use', default=5432, type=int)
@click.option('-l', '--local-port', help='The local port to use for the tunnel', type=int, metavar='PORT')
@click.option('-r', '--reason', help='If specified, request access using REASON', type=str, metavar='REASON')
@click.option('--region', help='The region to connect to', type=str, multiple=True, metavar='AWS_REGION_ID')
@click.option('-o', '--option', help='PIU option to pass on to piu (e.g. -t=1)', type=str, multiple=True)
@click.option('-v', '--verbose', is_flag=True, help='Enable DEBUG logging')
@click.argument('remote_host', nargs=1, metavar='DBHOSTNAME')
@click.argument('command', nargs=-1, metavar='[--] COMMAND [arg1] [argn]')
def tunnel(config_file, odd_host, user, spilo_stack_name, remote_host, port, command, verbose, local_port,
           reason, option, region):
    """Gotthard allows you to dig a base tunnel through a bastion (Stups: odd) host.

       It can run in 2 different modes: in the foreground and in the background.
       If you specify a COMMAND to execute it will run in foreground mode.

       When running in the background, gotthard establishes a tunnel in the background and terminates.
       When running in the foreground, the tunnel is established and the COMMAND you specify is executed.
       Once your COMMAND finishes, the tunnel is closed.
       If you need to pass options to the command, you will have to add the -- to signify that the following options
       should not be interpreted by gotthard.
       """

    loglevel = os.environ.get('LOGLEVEL', 'WARNING').upper() if not verbose else 'DEBUG'
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=loglevel)

    user = user or getpass.getuser()
    config = load_config(config_file, odd_host=odd_host, username=user)

    if len(region) == 0:
        region = ['eu-central-1', 'eu-west-1']

    logging.debug(config)

    if config.get('odd_host') is None:
        raise ClickException('No odd-host found in configuration')

    logging.info(region)
    remote_host, region = get_remote_host(remote_host, region, spilo_stack_name)

    if region:
        config['odd_host'] = re.sub('^odd-[^\.]+', 'odd-{}'.format(region), config['odd_host'])
        logging.info('Explicitly setting odd_host to {}'.format(config['odd_host']))

    if reason:
        piu_cmd = ['piu', '-c', config_file, 'request-access', '-O', config.get('odd_host'), config.get('odd_host')]
        for o in list(option):
            piu_cmd += [x.strip() for x in o.split('=', 1)]
        piu_cmd.append(reason)
        logging.info("Requesting access with piu:\n{}".format(piu_cmd))

        with open(os.devnull, 'r') as devnull:
            piu = subprocess.Popen(piu_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=devnull)
            out, err = piu.communicate()
            logging.debug(out)
            logging.debug(err)

        if piu.returncode != 0:
            raise ClickException("PIU: {}\nexitcode:{}".format(err.decode('utf-8'), piu.returncode))

    ok, output = test_ssh(ODD_USERNAME, config.get('odd_host'), remote_host, port)
    if not ok:
        if 'was revoked by even' in output:
            raise ClickException("""
You should request access to your odd host using piu.
For example, to request access for 3 hours to fix an incident:

    piu request-access {odd_host} --lifetime 180 "Fixing incident INC-123"

Optionally, provide the --reason option to autimatically try to get access.
""".format(**config))
        else:
            raise Exception(output)

    tunnel_port, process = setup_tunnel(ODD_USERNAME, config['odd_host'], remote_host, port, local_port)
    if tunnel_port is None:
        raise ClickException("Could not establish tunnel")

    config['pid'] = process.pid
    config['port'] = port
    config['tunnel_port'] = tunnel_port

    env = dict(os.environ)
    env['PGPORT'] = str(tunnel_port)
    env['PGHOST'] = 'localhost'
    env.setdefault('PGSSLMODE', 'require')
    env.setdefault('PGUSER', user)
    env.setdefault('PGDATABASE', 'postgres')
    env.setdefault('GOTTHARDPID', str(process.pid))

    export_keys = ['PGPORT', 'PGHOST', 'PGSSLMODE', 'PGUSER', 'PGDATABASE', 'GOTTHARDPID']
    config['export_vars'] = '\n'.join(['export {}="{}"'.format(k, v) for k, v in env.items() if k in export_keys])

    if not command:
        click.echo("""\
# Tunnel established, you can now use the tunnel with your favourite tools.
#
# Process pid: {pid} is listening on localhost:{tunnel_port}
#
# You can use the following environment variables to connect using the tunnel:
{export_vars}
# Some examples:
#
#    ## Connect using url, using key value, or using parameters
#    psql postgresql://{username}@localhost:{tunnel_port}/postgres?sslmode=require
#    psql "host=localhost port={tunnel_port} user={username} sslmode=require dbname=postgres"
#    psql -h localhost -p {tunnel_port} -U {username} -d postgres
#
#    pg_dump --schema-only -h localhost -p {tunnel_port} -U {username} -d my_live_database
#
# WARNING: The ssh process with pid {pid} keeps running in the background. Terminate it if not needed anymore.
""".format(**config))
    else:
        original_sigint = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, do_nothing)

        subprocess.call(args=command, env=env)

        signal.signal(signal.SIGINT, original_sigint)

        logging.info("Terminating ssh tunnel (pid={})".format(process.pid))
        process.kill()


def get_remote_host(remote_host, regions, spilo_stack_name):
    # We allow instance ids or stack names to be specified
    # If it looks like one, we will try to get a host and port using boto3
    # Spilo member names replace - with _, so we accept instance id's with both
    match = re.match('^(i[_-])?([a-zA-Z0-9]+)$', remote_host)
    if match is None:
        return remote_host, None

    import boto3

    from botocore.exceptions import NoCredentialsError, ClientError

    try:
        if match.group(1) is None:
            ec2_instance_id = None
            for region in regions:
                logging.debug("Trying to find Spilo {} in region {}".format(remote_host, region))
                cf = boto3.client('cloudformation', region)
                elb = boto3.client('elb', region)
                ec2_instance_id = get_spilo_master(cf, elb, spilo_stack_name, remote_host)
                if ec2_instance_id is not None:
                    break
            if ec2_instance_id is None:
                raise ClickException('Could not find a Cloud Formation stack for Spilo {}'.format(remote_host))
            regions = [region]
        else:
            ec2_instance_id = re.sub('^i[-_]', 'i-', remote_host)
            logging.debug(regions)

        for region in regions:
            ec2 = boto3.client('ec2', region)
            ip = None
            try:
                logging.debug("Trying to find instance {} in region {}".format(ec2_instance_id, region))
                ip = get_instance_ip(ec2, ec2_instance_id, region)
                if ip is not None:
                    return ip, region
            except ClientError as ce:
                if ce.response['Error']['Code'] != 'InvalidInstanceID.NotFound':
                    raise
        raise ClickException('Could not determine IP-address for instance {}'.format(ec2_instance_id))
    except ClientError as ce:
        logging.warning(ce.response['Error']['Code'])
        if ce.response['Error']['Code'] in ['ExpiredToken', 'RequestExpired']:
            raise ClickException('\nAWS credentials have expired.\n' +
                                 'Use the "zaws require" command line tool to get a new temporary access key.')
        else:
            raise ce
    except NoCredentialsError:
        raise ClickException('\nNo AWS credentials found.\n' +
                             'Use the "zaws require" command line tool to get a temporary access key\n')


def setup_tunnel(user, odd_host, remote_host, remote_port, tunnel_port):
    tunnel_port = get_port(tunnel_port)

    if not tunnel_port:
        raise ClickException('Could not get a free local port for listening')

    ssh_command = ['ssh',
                   '-oExitOnForwardFailure=yes',
                   '-oBatchMode=yes',
                   '-L', '{}:{}:{}'.format(tunnel_port, remote_host, remote_port),
                   '{}@{}'.format(user, odd_host),
                   '-N']

    process = subprocess.Popen(ssh_command, preexec_fn=os.setpgrp)

    logging.debug("Testing if tunnel is listening")
    for i in range(50):
        try:
            time.sleep(0.2)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('localhost', tunnel_port))
            s.close()
            return tunnel_port, process
        except Exception:
            pass
        finally:
            s.close()

    logging.warning("Could not connect to port {}, killing ssh process with pid {}".format(tunnel_port, process.pid))
    process.kill()
    process, tunnel_port = None, None

    return tunnel_port, process


def get_port(port=None):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", port or 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
    except OSError as oe:
        if 'Address already in use' in str(oe):
            raise ClickException('Port {} is already in use'.format(port))
        raise
    return port


def get_instance_ip(ec2, instance_id, region):
    for r in ec2.describe_instances(InstanceIds=[instance_id])['Reservations']:
        for i in r['Instances']:
            return i['PrivateIpAddress']


def get_spilo_master(cf, elb, spilo_stack_name, spilo_cluster):
    logging.debug('Trying to find Spilo {}'.format(spilo_cluster))

    candidates = get_spilo_stacks(cf, spilo_stack_name, spilo_cluster)
    for c in candidates:
        for res in cf.describe_stack_resources(StackName=c, LogicalResourceId='PostgresLoadBalancer')['StackResources']:
            logging.debug(yaml.dump(res, default_flow_style=False))
            instance_states = elb.describe_instance_health(LoadBalancerName=res['PhysicalResourceId'])['InstanceStates']
            for i in instance_states:
                if i['State'] == 'InService':
                    return i['InstanceId']
            instances = [i['InstanceId'] for i in instance_states]
            raise ClickException('No running master found for Spilo {}, members: {}'.format(spilo_cluster, instances))


def get_spilo_stacks(cf, spilo_stack_name, spilo_cluster):
    allowed_stack_statuses = ['CREATE_COMPLETE', 'UPDATE_IN_PROGRESS', 'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS',
                              'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_IN_PROGRESS', 'UPDATE_ROLLBACK_FAILED',
                              'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS', 'UPDATE_ROLLBACK_COMPLETE']
    spilo_tag = 'SpiloCluster'

    full_stack_name = '{0}-{1}'.format(spilo_stack_name, spilo_cluster)
    stacks = cf.describe_stacks(StackName=full_stack_name)['Stacks']
    for stack in stacks:
        stack_name = stack['StackName']
        if stack['StackStatus'] not in allowed_stack_statuses:
            logging.warning("Ignoring stack {0} with status {1}".format(full_stack_name, stack['StackStatus']))
        else:
            for t in stack['Tags']:
                if t['Key'] == spilo_tag and (not spilo_cluster or t['Value'] == spilo_cluster):
                    yield stack_name
                    break
            else:
                logging.warning("Ignoring stack {0} without matching {1} tag".format(full_stack_name, spilo_tag))


def test_ssh(user, odd_host, remote_host, remote_port):
    logging.debug("Checking if we can connect to {}:{} via {}@{}".format(remote_host, remote_port, user, odd_host))
    out = ''
    try:
        ssh_cmd = ['ssh', '{}@{}'.format(user, odd_host), 'nc -z {} {} -w 2'.format(remote_host, remote_port)]
        out = subprocess.check_output(ssh_cmd)
    except subprocess.CalledProcessError as cpe:
        logging.debug(cpe)
        raise ClickException("""
Could not establish connection to the remote host and remote port
Please ensure you can connect to the remote host and remote port from the odd host you specify.

For troubleshooting, test the following command:

{}
""".format(' '.join(ssh_cmd)))

    except Exception as e:
        logging.exception(e)

    return out == b'', out.decode("utf-8")


def main():
    tunnel()
