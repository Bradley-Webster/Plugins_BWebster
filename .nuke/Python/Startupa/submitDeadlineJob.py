#!/usr/bin/env python

import argparse

from deadline.jobs import command as deadline_command


def send_job(cmd, jobdata, name, queue):
    '''
    Uses PyDeadline command to send job to deadline with correct args
    '''
    job = deadline_command.CommandJob()
    job.name = name
    job.label = name
    job.arguments = cmd
    job.batch_name = "command_job"
    job.execute_in_shell = True
    job.pool = "batch_publish"
    job.submit()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Tactic DB Server')

    parser.add_argument("-cmd", dest="cmd")
    parser.add_argument("-jobdata", dest="jobdata")
    parser.add_argument("-name", dest="name")
    parser.add_argument("-queue", dest="queue")

    args = parser.parse_args()
    send_job(args.cmd, args.jobdata, args.name, args.queue)
