#!/usr/bin/env python

from ruamel.yaml import YAML
import sys
import argparse
import fileinput

def main():
    output_an = {}
    output_gl = {}

    with open('dosk.yml') as config:
        
        yaml = YAML()
        code = yaml.load(config)

        for idx, obj in enumerate(code):
            load = one(code, obj)
            print(load)

def one(code, obj):
    load = {}
    if isinstance(code[obj], str):
        load[obj] = code[obj]
    else:
        subtasks = []
        for subspec in code[obj]:
            if subspec in code:
                temp = two(code, subspec)
                subtasks.append(temp)
            else:
                subtasks.append(subspec)
        load[obj] = subtasks

    return load

def _parse_tasks(self, parsed):
    tasks = {}
load = {}
for taskname, body in parsed.items():
    logging.debug("Parsing `{}`".format(body))
    if isinstance(body, str):
        load[taskname] = Task(body.format(**self.vars), self.env)
    else:
        subtasks = []
        for subspec in body:
            try:
                subtasks.append(load[subspec])
            except KeyError:
                    if subspec in parsed:
                        print(subspec)
                    subtasks.append(
                        Task(subspec.format(**self.vars), self.env)
                    )
        if taskname.endswith("@"):
            load[taskname[:-1]] = ConcurrentTaskList(subtasks)
        else:
            load[taskname] = SequentialTaskList(subtasks)

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
                if subspec in parsed:
                    subtasks.append(load[subspec])
                else:
                    subtasks.append(
                        Task(subspec.format(**self.vars), self.env)
                    )
        if taskname.endswith("@"):
            tasks[taskname[:-1]] = ConcurrentTaskList(subtasks)
        else:
            tasks[taskname] = SequentialTaskList(subtasks)
return tasks


def two(code, obj):
    load = {}
    if isinstance(code[obj], str):
        load[obj] = code[obj]
    else:
        subtasks = []
        for subspec in code[obj]:
            if subspec in code:
                temp = one(code, subspec)
                subtasks.append(temp)
            else:
                subtasks.append(subspec)
        load[obj] = subtasks

    return load
                    


if __name__ == "__main__":
    main()
