#!/usr/bin/env python3

import argparse
import json
import asyncio
import functools
import logging
import os
import shlex
import signal
import string
import sys
from ruamel.yaml import YAML

from pathlib import Path

log = logging.getLogger(name="dosk")
__version__ = "0.1.3.dev"

def main():
    args = parse_args()
    logging.basicConfig(level=args.verbose)
    tasks = TaskDefs('dosk.yml')
    try:
        task = tasks[args.task]
    except KeyError:
        error("Task {} not defined. {}".format(args.task, tasks))
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGQUIT):
        handler = functools.partial(handle_signal, sig, task)
        loop.add_signal_handler(sig, handler)
    loop.run_until_complete(task.run())

def parse_args():
    parser = argparse.ArgumentParser(prog ='dock', description ='Do Task - The Simple DevOps Task Runner') 
  
    parser.add_argument("task", nargs="?",
                        help="Name of task to execute")

    parser.add_argument('--local', '-l', action ='store_const', const = True, 
                        default = False, dest ='local', 
                        help ="Load local variables") 

    verbose = parser.add_mutually_exclusive_group()
    verbose.add_argument('--verbose', '-v',  action="store_const", const=logging.DEBUG, default=logging.INFO,
                        help="Print additional information")

    verbose.add_argument('--quiet', '-q', action="store_const", dest="verbose", const=logging.WARNING,
                        help="Print less information")

    args = parser.parse_args()
    if not args.task:
        parser.error("Must specify a task")
    return args

def error(message):
    """ Give error message and exit"""
    log.error(message)
    sys.exit(1)


def _extract_env_and_vars(parsed):
    # There has *got* to be a way to do this more simply
    env = os.environ.copy()
    vars = {}
    if 'vars' in parsed:
        o_vars = parsed['vars']
    vars = json.loads(json.dumps(o_vars))
    return env, vars

def inplace_change(filename, old_string, new_string):
    reading_file = open(filename, "r")
    new_file_content = ""
    for line in reading_file:
        new_line = line.replace(old_string, new_string)
        new_file_content += new_line
    reading_file.close()

    writing_file = open(filename, "w")
    writing_file.write(new_file_content)
    writing_file.close()

class TaskDefs(dict):
    def __init__(self, taskfile):
        self.taskfile = Path(taskfile)
        with open(taskfile) as config:
            yaml = YAML()
            parsed = yaml.load(config)
            self.env, self.vars = _extract_env_and_vars(parsed)
            self.tasks = self._parse_tasks(parsed)
        
    def __getitem__(self, key):
        return self.tasks[key]

    def __str__(self):
        """Print available tasks and exit"""
        to_str = ["Available tasks:"]
        to_str.extend(["\t{}".format(task) for task in self.tasks])
        return "\n".join(to_str)

    def _parse_tasks(self, parsed):
        tasks = {}
        condition = ''
        loop = ''

        for taskname, obj in parsed.items():
            run=True
            length=0

            if 'replace' in obj:
                if isinstance(obj['replace'], list):
                    for line in obj['replace']:
                        inplace_change(line[0], line[1], line[2])
                else:
                    inplace_change(obj['replace'][0], obj['replace'][1], obj['replace'][2])

            if 'condition' in obj:
                condition = obj['condition']
                if not eval(condition, self.vars):
                    tasks[taskname] = Task("echo 'Condition not met'")
                    run=False

            if 'loop' in obj:
                if isinstance(obj['loop'], int):
                    loop = 'count < ' + str(obj['loop'])
                else:
                    length = len(self.vars['fruit'])
                    loop = 'count < ' + str(length)
            else:
                loop = 'count < 1'

            if 'task' in obj and run:
                count = 0
                subtasks = []
                while eval(loop):
                    if count <= length :
                        self.vars.update( loop = self.vars['fruit'][count])
                    count += 1
                    self.vars.update( count = count )
                    logging.debug("Parsing `{}`".format(obj['task']))
                    if isinstance(obj['task'], str):
                        subtasks.append(Task(obj['task'].format(**self.vars), self.env))
                    else:
                        for subspec in obj['task']:
                            try:
                                subtasks.append(tasks[subspec])
                            except KeyError:
                                subtasks.append(Task(subspec.format(**self.vars), self.env))
                if taskname.endswith("@"):
                    tasks[taskname[:-1]] = ConcurrentTaskList(subtasks)
                else:
                    tasks[taskname] = SequentialTaskList(subtasks)
        return tasks

class Task(object):
    def __init__(self, cmd, env=None):
        logging.debug('Creating task with command "{}"'.format(cmd))
        self.cmd = cmd
        self.proc = None
        self.env = env or {}

    def terminate(self):
        """Terminate the task's process, if running"""
        try:
            if self.proc.returncode is None:
                log.debug("Terminating {}".format(self.cmd))
                self.proc.terminate()
        except AttributeError:
            pass

    async def run(self, args=None):
        cmd = self.cmd
        if args:
            cmd = " ".join(
                [cmd, " ".join(shlex.quote(token) for token in args)]
            )
        log.info(cmd)
        self.proc = await asyncio.create_subprocess_shell(cmd, env=self.env)
        await self.proc.wait()


class TaskList(object):
    def __init__(self, tasks, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tasks = tasks


class SequentialTaskList(TaskList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kill = False
        self.current = None

    async def run(self, args=None):
        last = len(self.tasks) - 1
        for i, task in enumerate(self.tasks):
            if self.kill:
                break
            self.current = task
            await task.run(args if i == last else None)

    def terminate(self):
        self.kill = True
        try:
            self.current.terminate()
        except AttributeError:
            pass


class ConcurrentTaskList(TaskList):
    async def run(self, args=None):
        if args:
            error("Additional arguments not valid for concurrent tasks")
        await asyncio.wait(
            [task.run() for task in self.tasks],
            return_when=asyncio.FIRST_EXCEPTION,
        )

    def terminate(self):
        for task in self.tasks:
            task.terminate()

def handle_signal(signum, task):
    """On any signal, terminate the active task"""
    log.debug("Caught {}".format(signal.Signals(signum).name))
    task.terminate()

if __name__ == "__main__":
    main()

