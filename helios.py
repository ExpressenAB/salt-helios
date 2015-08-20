#!/usr/bin/env python

import json
import re
import salt
import salt.exceptions
from functools import wraps

from argument_handler import ArgumentHandler

__virtualname__ = 'helios'

valid_kwargs = {
    'global': [
        'master',
        'sites',
        'domains',
        'srv_name',
        'username',
        'verbose',
        'version',
        'json'
    ],
    'create': [
        'file',
        'template',
        'token',
        'env_vars',
        'ports',
        'registration',
        'registration_domain',
        'grace_period',
        'volumes',
        'expires',
        'exec_check',
        'http_check',
        'tcp_check',
        'security_opt',
        'network_mode'
    ],
    'remove': [
        'token',
        'yes',
        'force'
    ],
    'inspect': [],
    'deploy': [
        'token',
        'no_start',
        'watch',
        'interval'
    ],
    'undeploy': [
        'token',
        'all',
        'yes',
        'force'
    ],
    'start': [
        'token'
    ],
    'stop': [
        'token'
    ],
    'history': [],
    'jobs': [
        'f',
        'q',
        'y'
    ],
    'status': [
        'job',
        'host',
        'f'
    ],
    'watch': [
        'interval',
        'exact'
    ],
    'hosts': [
        'q',
        'f',
        'labels'
    ],
    'register': [],
    'deregister': [
        'yes',
        'force'
    ],
    'masters': [
        'f'
    ],
    'create_deployment_group': [
        'q'
    ],
    'remove_deployment_group': [],
    'list_deployment_groups': [],
    'inspect_deployment_group': [],
    'deployment_group_status': [
        'f'
    ],
    'watch_deployment_group': [
        'f',
        'interval'
    ],
    'rolling_update': [
        'timeout',
        'par',
        'async',
        'rollout_timeout',
        'migrate'
    ],
    'stop_deployment_group': [],
    'version': [],
}

# TODO - Populate with statuses that means success
success_status = [
    'OK',
    'CREATED',
    'REMOVED',
    'NOT_MODIFIED'
]

def __virtual__():
    required_cmds = ['helios']

    # Iterate over all of the commands this module uses and make sure
    # each of them are available in the standard PATH to prevent breakage
    for cmd in required_cmds:
        if not salt.utils.which(cmd):
            return False

    return __virtualname__

def kwargs_to_string(method, kwargs):
    master = __salt__['config.get']('helios:master')
    domains = __salt__['config.get']('helios:domains')
    srv_name = __salt__['config.get']('helios:srv_name')
    username = __salt__['config.get']('helios:username')

    arg_handler = ArgumentHandler(master=master, domains=domains, srv_name=srv_name, username=username)
    arg_str = ''
    for k,v in kwargs.iteritems():
        if "__pub" in k:
            continue
        if not k in valid_kwargs[method] and not k in valid_kwargs['global']:
            return False
        arg_str += getattr(arg_handler, k)(v)
    return arg_handler.get_global_args() + arg_str

def call(method, args, kwargs):
    ret = { 'success': True }
    kwargs_string = kwargs_to_string(method, kwargs)
    if not kwargs_string:
        ret['success'] = False
        ret['result'] = {'status': 'INVALID_KWARG'}
        ret['errors'] = ['Invalid key/value argument, see docs.']
        return ret

    arg_string = 'helios ' + method.replace('_', '-') + ' ' + args + kwargs_to_string(method, kwargs)
    res = __salt__['cmd.run'](arg_string)
    try:
        ret['result'] = json.loads(res)
    except ValueError:
        ret['success'] = False
        ret['result'] = {'status': 'REQUEST_FAILED'}
        ret['errors'] = [res]
        return ret

    if 'status' in ret['result'] and ret['result']['status'] not in success_status:
        ret['success'] = False

    return ret


def create(job_id, image, args, **kwargs):
    '''
        Create a new helios job

        :param name: name:version of the job
        :param image: image, the container image to use
        :param args: args, List of command line arguments passed to the container
    '''
    arg_string = job_id + ' ' + image
    for arg in args:
        arg_string += ' "' + arg.replace('"', '\\"') + '"'

    return call('create', arg_string, kwargs)

def remove(job_id, **kwargs):
    '''
        Remove a helios job
    '''
    arg_string = job_id
    return call('remove', arg_string, kwargs)

def inspect(job_id, **kwargs):
    arg_string = job_id
    return call('create', arg_string, kwargs)

# Hosts must be a list
# TODO - How does this work in orchestrate?
def deploy(job_id, hosts, **kwargs):
    arg_string = job_id + ' ' + ' '.join(hosts)
    return call('deploy', arg_string, kwargs)

def undeploy(job_id, hosts, **kwargs):
    arg_string = job_id + ' ' + ' '.join(hosts)
    return call('undeploy', arg_string, kwargs)

def start(job_id, hosts, **kwargs):
    arg_string = job_id + ' ' + ' '.join(hosts)
    return call('start', arg_string, kwargs)

def stop(job_id, hosts, **kwargs):
    arg_string = job_id + ' ' + ' '.join(hosts)
    return call('stop', arg_string, kwargs)

def history(job_id, **kwargs):
    arg_string = job_id
    return call('history', arg_string, kwargs)

def jobs(pattern, **kwargs):
    arg_string = pattern
    return call('jobs', arg_string, kwargs)

def status(**kwargs):
    arg_string = ''
    return call('status', arg_string, kwargs)

def watch(job_id, hosts, **kwargs):
    arg_string = job_id + ' ' + ' '.join(hosts)
    return call('watch', arg_string, kwargs)

def hosts(pattern = '', **kwargs):
    arg_string = pattern
    return call('hosts', arg_string, kwargs)

def register(host, id, **kwargs):
    arg_string = host + ' ' + id
    return call('register', arg_string, kwargs)

def deregister(host, **kwargs):
    arg_string = host
    return call('deregister', arg_string, kwargs)

def masters(**kwargs):
    arg_string = ''
    return call('masters', arg_string, kwargs)

# TODO - Check how to handle host_selectors
def create_deployment_group(name, host_selectors, **kwargs):
    arg_string = name
    for host_selector in host_selectors:
        k = host_selector.keys()[0]
        arg_string += ' ' + k + '=' + host_selector[k]
    return call('create_deployment_group', arg_string, kwargs)

def remove_deployment_group(name, **kwargs):
    arg_string = name
    return call('remove_deployment_group', arg_string, kwargs)

def list_deployment_groups(**kwargs):
    arg_string = ''
    return call('list_deployment_groups', arg_string, kwargs)

def inspect_deployment_group(name, **kwargs):
    arg_string = name
    return call('inspect_deployment_group', arg_string, kwargs)

def deployment_group_status(name, **kwargs):
    arg_string = name
    return call('deployment_group_status', arg_string, kwargs)

def watch_deployment_group(name, **kwargs):
    arg_string = name
    return call('watch_deployment_group', arg_string, kwargs)

def rolling_update(job_id, deployment_group_name, **kwargs):
    arg_string = job_id + ' ' + deployment_group_name
    return call('rolling_update', arg_string, kwargs)

def stop_deployment_group(name, **kwargs):
    arg_string = name
    return call('stop_deployment_group', arg_string, kwargs)

def version(**kwargs):
    arg_string = ''
    return call('version', arg_string, kwargs)

# TODO - fix non optional arguments
