"""
Module for providing.
"""
from dataclasses import dataclass
from wca.scheduler.cluster_simulator import ClusterSimulator
from wca.scheduler.data_providers import DataProvider
from wca.scheduler.types import ResourceType


@dataclass
class ClusterSimulatorDataProvider(DataProvider):
    simulator: ClusterSimulator

    def get_node_free_space_resource(self, node: str, resource_type: ResourceType) -> float:
        node = self.simulator.get_node_by_name(node)

        if node is None:
            raise Exception('no such node')

        if resource_type == ResourceType.CPU:
            return node.unassigned.cpu
        if resource_type == ResourceType.MEMBW:
            return node.unassigned.membw
        if resource_type == ResourceType.MEM:
            return node.unassigned.mem

    def get_app_requested_resource(self, app: str, resource_type: ResourceType) -> float:
        task = self.simulator.get_task_by_name(app)

        if task is None:
            raise Exception('no such task')

        if resource_type == ResourceType.CPU:
            return task.initial.cpu
        if resource_type == ResourceType.MEMBW:
            return task.initial.membw
        if resource_type == ResourceType.MEM:
            return task.initial.mem