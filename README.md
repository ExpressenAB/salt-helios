# salt-helios
A SaltStack Execution Module for Helios

## helios.create_job(job_id, image, args, **kwargs):
## helios.remove_job(job_id, **kwargs):
## helios.inspect_job(job_id, **kwargs):
## helios.deploy_job(job_id, hosts, **kwargs):
## helios.undeploy_job(job_id, hosts, **kwargs):
## helios.start_job(job_id, hosts, **kwargs):
## helios.stop_job(job_id, hosts, **kwargs):
## helios.history(job_id, **kwargs):
## helios.list_jobs(pattern, **kwargs):
## helios.list_hosts(pattern, **kwargs):
## helios.list_masters(**kwargs):
## helios.status(**kwargs):
## helios.watch(job_id, hosts, **kwargs):
## helios.register(host, id, **kwargs):
## helios.deregister(host, **kwargs):
## helios.create_deployment_group(name, host_selectors, **kwargs):
## helios.remove_deployment_group(name, **kwargs):
## helios.list_deployment_groups(**kwargs):
## helios.inspect_deployment_group(name, **kwargs):
## helios.deployment_group_status(name, **kwargs):
## helios.watch_deployment_group(name, **kwargs):
## helios.rolling_update(job_id, deployment_group_name, **kwargs):
## helios.stop_deployment_group(name, **kwargs):
## helios.version(**kwargs):
