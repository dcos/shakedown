import time
import urllib
from dcos import config, errors, http

def post_job(job):
    return http.post(_metronome_url('v1/jobs'), json=job)


def get_job(job_id, history=True):
    url = 'v1/jobs/{}'.format(job_id)
    if history:
        url = url + '?embed=history'
    return http.get(_metronome_url(url))


def post_run(job_id):
    return http.post(_metronome_url('v1/jobs/{}/runs').format(job_id))


def get_run(job_id, run_id):
    return http.get(_metronome_url('v1/jobs/{}/runs/{}').format(job_id, run_id))


def run_job(job_spec, wait=True, assertSuccess=True):
    job_id = post_job(job_spec).json()['id']
    run_id = post_run(job_id).json()['id']
    if wait:
        wait_for_run(job_id, run_id)
    if assertSuccess:
        job = get_job(job_id).json()
        assert(len(job['history']['successfulFinishedRuns']) > 0)
    return job_id


def wait_for_run(job_id, run_id):
    while True:
        try:
            response = get_run(job_id, run_id)
        except errors.DCOSHTTPException as ex:
            if ex.response.status_code == 404:
                break
            else:
                raise ex
        time.sleep(5)


def _metronome_url(url):
    dcos_url = config.get_config_val('core.dcos_url')
    return urllib.parse.urljoin(
        urllib.parse.urljoin(dcos_url, 'service/metronome/'),
        url)
