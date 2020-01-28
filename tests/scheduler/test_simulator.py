from collections import Counter
from dataclasses import dataclass
import pytest
from pprint import pprint
import random
from typing import Dict, List

from wca.scheduler.algorithms.ffd_generic import FFDGeneric, FFDGeneric_AsymetricMembw
from wca.scheduler.cluster_simulator import ClusterSimulator, Node, Resources, GB, Task
from wca.scheduler.data_providers.cluster_simulator_data_provider import (
        ClusterSimulatorDataProvider)
from wca.scheduler.types import ResourceType
from wca.scheduler.simulator_experiments.experiment_1 import single_run


def task_creation_fun(identifier):
    r = Resources({ResourceType.CPU: 8, ResourceType.MEM: 10, ResourceType.MEMBW: 10})
    t = Task('stress_ng_{}'.format(identifier), r)
    return t


def test_single_run():
    simulator_dimensions = set([ResourceType.CPU, ResourceType.MEM, ResourceType.MEMBW,])
    nodes = [Node('0', Resources({ResourceType.CPU: 96, ResourceType.MEM: 1000, ResourceType.MEMBW: 50})),
             Node('1', Resources({ResourceType.CPU: 96, ResourceType.MEM: 320, ResourceType.MEMBW: 150}))]
    extra_simulator_args = {"allow_rough_assignment": True,
                            "dimensions": simulator_dimensions}
    scheduler_class = FFDGeneric
    extra_scheduler_kwargs = {"dimensions": set([ResourceType.CPU, ResourceType.MEM])}

    simulator = single_run(nodes, task_creation_fun, extra_simulator_args,
                           scheduler_class, extra_scheduler_kwargs)
    assert len(simulator.tasks) == 23
    assert len([node for node in simulator.nodes if node.unassigned.data[ResourceType.MEMBW] < 0]) == 1


def test_single_run_membw_write_read():
    """check code membw write/read specific"""
    simulator_dimensions = set([ResourceType.CPU, ResourceType.MEM, 
                                ResourceType.MEMBW_READ, ResourceType.MEMBW_WRITE,])
    nodes = [Node('0', Resources({ResourceType.CPU: 96, ResourceType.MEM: 1000, ResourceType.MEMBW: 50})),
             Node('1', Resources({ResourceType.CPU: 96, ResourceType.MEM: 320, ResourceType.MEMBW: 150}))]
    extra_simulator_args = {"allow_rough_assignment": True,
                            "dimensions": simulator_dimensions}
    scheduler_class = FFDGeneric_AsymetricMembw
    extra_scheduler_kwargs = {}

    simulator = single_run(nodes, create_task, extra_simulator_args,
                           scheduler_class, extra_scheduler_kwargs)
    assert len(simulator.tasks) == 23
    assert len([node for node in simulator.nodes if node.unassigned.data[ResourceType.MEMBW] < 0]) == 1
