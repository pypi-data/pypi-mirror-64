#!/usr/bin/env python3

import argparse
import asyncio
import collections
import functools
import logging
import os
import shlex
import signal
import sys
import yaml

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
    first = tuple(parsed.keys())[0]
    if first in {"env", "vars"}:
        if first == "env":
            env.update(parsed.pop("env"))
        else:
            vars = parsed.pop("vars")
        second = tuple(parsed.keys())[0]
        if second in {"env", "vars"}:
            if second == "env":
                env.update(parsed.pop("env"))
            else:
                vars = parsed.pop("vars")
    return env, vars


class TaskDefs(dict):
    def __init__(self, taskfile):
        self.taskfile = Path(taskfile)
        parsed = yaml.load(self.taskfile.open(), Loader=yaml.SafeLoader)
        self.env, self.vars = _extract_env_and_vars(parsed)
        self.tasks = self._parse_tasks(parsed)

    def __getitem__(self, key):
        return self.tasks[key]

    def _parse_tasks(self, parsed):
        tasks = {}
        for taskname, body in parsed.items():
            logging.debug("Parsing `{}`".format(body))
            if isinstance(body, str):
                tasks[taskname] = Task(body.format(**self.vars), self.env)
            else:
                subtasks = []
                for subspec in body:
                    try:
                        subtasks.append(tasks[subspec])
                    except KeyError:
                        subtasks.append(
                            Task(subspec.format(**self.vars), self.env)
                        )
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

                        for deepname, deepbody in parsed.items():
                            if subspec == deepname:
                                print(subspec)
                                skip = True
                                break
                        if not skip: