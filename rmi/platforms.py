from dataclasses import dataclass
from typing import List, Dict

from rmi.metrics import Metric

# 0-based logical processor number (matches the value of "processor" in /proc/cpuinfo)
CpuId = int


@dataclass
class Platform:

    # Topology:
    sockets: int  # number of sockets
    cores: int    # number of physical cores in total (sum over all sockets)
    cpus: int     # logical processors equal to the output of "nproc" Linux command

    # Utilization (usage):
    # counter like, sum of all modes based on /proc/stat
    # "cpu line" with 10ms resolution expressed in [ms]
    cpus_usage: Dict[CpuId, int]

    # [bytes] based on /proc/meminfo (gauge like)
    # difference between MemTotal and MemAvail (or MemFree)
    total_memory_used: int


def collect_platform_information() -> (Platform, List[Metric], Dict[str, str]):
    """Returns Platform information, metrics and common labels.


    Returned objects meaning:
    - Platform is a static information about topology as well as some metrics about platform 
    level resource usages.
    - List[Metric] covers the same information as platform but serialized to storage accepted type.
    - "common labels" are used to mark every other metric (generated by other sources) e.g. host

    Note: returned metrics should be consistent with information covered by platform
    
    """
    # TODO: implement me
    return Platform(0, 0, 0, {}, 0), [], {"host":"localhost"}
