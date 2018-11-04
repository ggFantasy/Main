from crontab import CronTab

from ggfantasy.timelord.jobs.league_enqueuer import LeagueEnqueuer
from util import Util

"""
    TimeLord is a cron job manager
    
    Functions:
    If you run the file, you run the script which executes Enqueuers
    If you call the class, you can add jobs to the manager
    
    Ideal Ops:
    Runs once a day to audit list of jobs to make sure scripts that should be run
    are in the queue
"""

JOBS = {
    'League Enqueuer', LeagueEnqueuer
}


class TimeLord:
    def __init__(self, job_config={}, user=True):
        self.cron = CronTab(user=user)
        if job_config:
            self.schedule_job(job_config)

    def launch(self):
        for job in JOBS:
            name, script = job
            print('Running {}'.format(name))
            script.run()

    # TODO Add a dry run mode where it hits a fake endpoint to get a schedule
    def schedule_job(self, job_config):
        command = '{}/venv/bin/python'.format(Util.get_root_dir())
        job = self.cron.new(command='{} {}'.format(command, job_config['target']))

        date = job_config['date']
        job.day.on(date.day)
        job.hour.on(date.hour)
        job.minute.on(date.minute)

    def get_jobs(self):
        jobs = list()
        for job in self.cron:
            print(job)
            jobs.append(job)

        return jobs

    def update_job(self):
        raise Exception('Not yet implemented')

    def remove_job(self):
        raise Exception('Not yet implemented')

    def run_jobs(self):
        raise Exception('Not yet implemented')


if __name__ == "__main__":
    print("Initiating Timelord...")
    timelord = TimeLord()
    timelord.launch()
    timelord.get_jobs()
