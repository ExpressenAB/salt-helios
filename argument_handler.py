# TODO - escape characters and stuff
# TODO - Validation of input?

class ArgumentHandler:
#    master_host = __salt__['config.get']('helios.url') or __salt__['config.get']('helios:url')
    # Global arguments
    def __init__(self, master=None, domains=None, srv_name=None, username=None):
        self.master_arg = master
        self.domains_arg = domains
        self.srv_name_arg = srv_name
        self.username_arg = username
        self.verbose_arg = False
        self.json_arg = True


    def master(self, data):
        self.master_arg = data
        return ''


    def domains(self, data):
        self.domains_arg = data
        return ''


    def srv_name(self, data):
        self.srv_name_arg = data
        return ''


    def username(self, data):
        self.username_arg = data
        return ''

    def verbose(self, data):
        self.verbose_arg = data
        return ''

    def json(self, data):
        self.json_arg = data
        return ''

    def get_global_args(self):
        glob_str = ''
        if self.master_arg:
            glob_str += ' --master ' + self.master_arg
        if self.domains_arg:
            glob_str += ' --domain ' + ' --domain '.join(self.domains_arg)
        if self.srv_name_arg:
            glob_str += ' --srv-name ' + self.srv_name_arg
        if self.username_arg:
            glob_str += ' --username ' + self.username_arg
        if self.verbose_arg:
            glob_str += ' --verbose'
        if self.json_arg:
            glob_str += ' --json'
        return glob_str


    # Create job arguments
#
#    def command(data):
#        return ' "' + data.replace('"', '\\"') + '"'


    def file(self, data):
        return ' --file ' + data


    def template(self, data):
        return ' --template ' + data


    def token(self, data):
        return ' --token ' + data


    def env_vars(self, data):
        arg_str = ''
        for k,v in data.iteritems():
            arg_str += ' --env ' + k + '=' + v
        return arg_str[:-1]


    def ports(self, data):
        arg_str = ''
        for k,v in data.iteritems():
            arg_str += ' --port ' + k + '=' + str(v['internal_port'])
            if 'external_port' in v:
                arg_str += ':' + str(v['external_port'])
            if 'protocol' in v:
                arg_str += '/' + v['protocol']
        return arg_str


    def registration(self, data):
        arg_str = ''
        for k,v in data.iteritems():
            arg_str += ' --register ' + k
            if 'ports' in v:
                arg_str += '=' + v['ports'].keys()[0]
        return arg_str


    def registration_domain(self, data):
        return ' --registration-domain ' + data


    def grace_period(self, data):
        return ' --grace-period ' + str(data)


    def volumes(self, data):
        arg_str = ''
        for k,v in data.iteritems():
            arg_str += ' --volume ' + k + ':' + v
            if 'access' in v:
                arg_str += ':' + v['access']
        return arg_str


    def expires(self, data):
        return ' --expires ' + data


    def exec_check(self, data):
        return ' --exec-check "' + data['command'].replace('"', '\\"') + '"'


    def http_check(self, data):
        return ' --http-check "' + data['port'] + ':' + data['path'] +'"'


    def tcp_check(self, data):
        return ' --tcp-check "' + data['port']


    def hostname(self, data):
        pass
        # TODO - Doesn't seem to be supported in the CLI


    def security_opt(self, data):
        return ' --security-opts ' + data


    def network_mode(self, data):
        return ' --network-mode ' + data

    # Remove job arguments

    def yes(self, data):
        return ArgumentHandler.return_if_true(data, ' --yes')

    def force(self, data):
        return ArgumentHandler.return_if_true(data, ' --force')

    # Inspect job arguments
    # TODO - Will this ever be used in salt?

    # Deploy job arguments

    def no_start(self, data):
        return ArgumentHandler.return_if_true(data, ' --no-start')


    def watch(self, data):
        return ArgumentHandler.return_if_true(data, ' --watch')


    def interval(self, data):
        return ' --interval ' + str(data)

    # Undeploy job arguments

    def all(self, data):
        return ArgumentHandler.return_if_true(data, ' --all')

    # Start stopped job argument                start a stopped job
    # Nothing new

    # Stop running job arguments                stop a running job without undeploying it
    # Nothing new

    # History arguments                         see the run history of a job
    # Nothing new

    # List jobs arguments                       list jobs

    def f(self, data):
        return ArgumentHandler.return_if_true(data, ' -f')


    def q(self, data):
        return ArgumentHandler.return_if_true(data, ' --q')


    def y(self, data):
        return ArgumentHandler.return_if_true(data, ' --y')

    # Status of job or host arguments           show job or host status

    def job(self, data):
        return ' --job ' + data


    def host(self, data):
        return ' --host ' + data

    # Watch jobs arguments                      watch jobs

    def exact(self, data):
        return ArgumentHandler.return_if_true(data, ' --exact')

    # List hosts arguments                      list hosts

    def labels(self, data):
        for k,v in data.iteritems():
            arg_str = ' --label'
            arg_str += ' ' + k + '=' + v
        return arg_str

    # Register a host arguments                 register a host
    # Nothing to add

    # Deregister a host arguments               deregister a host
    # Nothing new

    # List masters arguments                    list masters
    # Nothing new

    # Create deployment group arguments         create a deployment group
    # Nothing new

    # Remove deployment group arguments         remove a deployment-group. Note that this does not undeploy jobs previously deployed by the deployment-group
    # Nothing new

    # List deployment groups arguments          list deployment groups
    # Nothing new

    # Inspect deployment group arguments        inspect a deployment group
    # Nothing new

    # Deployment group status arguments         Show deployment-group status
    # Nothing new

    # Watch deployment group arguments          watch deployment groups
    # Nothin new

    # Rolling update arguments                  Initiate a rolling update

    def timeout(self, data):
        return ' --timeout ' + str(data)


    def par(self, data):
        return ' --par ' + str(data)


    def async(self, data):
        return ArgumentHandler.return_if_true(data, ' --async')


    def rollout_timeout(self, data):
        return ' --rollout-timeout ' + str(data)


    def migrate(self, data):
        return ArgumentHandler.return_if_true(data, ' --migrate')
    # Stop deployment group arguments           Stop a deployment-group or abort a rolling-update
    # Nothin new

    # Helper methods
    @staticmethod
    def return_if_true(bool, value):
        if bool == True:
            return value
        else:
            return ''
