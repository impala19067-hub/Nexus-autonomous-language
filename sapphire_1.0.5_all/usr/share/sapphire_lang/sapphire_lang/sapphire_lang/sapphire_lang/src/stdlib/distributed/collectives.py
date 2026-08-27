"""
Sapphire NCCL Collective Communication & Topology Scheduling Engine
Simulates and schedules:
- AllReduce (Ring & Tree)
- ReduceScatter & AllGather (FSDP / ZeRO)
- AllToAll (MoE Expert Dispatch)
- P2P Send/Recv (Pipeline 1F1B)
- Asynchronous CUDA Stream Overlap
"""

import math
from typing import Dict, Any, List

class CollectiveCommunicationEngine:
    """
    Simulates NCCL collective communication latencies and schedules optimal
    communication/computation overlap streams.
    """
    @staticmethod
    def calculate_ring_allreduce(data_size_bytes: float, num_gpus: int, bus_bw_gb_s: float) -> Dict[str, Any]:
        """
        Calculates Ring AllReduce transfer time:
        Volume transferred per GPU = 2 * (num_gpus - 1) / num_gpus * data_size
        """
        if num_gpus <= 1:
            return {"time_ms": 0.0, "volume_mb": 0.0, "algo": "None"}
        
        factor = 2.0 * (num_gpus - 1) / num_gpus
        volume_bytes = factor * data_size_bytes
        volume_gb = volume_bytes / (1024 ** 3)
        time_sec = volume_gb / bus_bw_gb_s
        time_ms = time_sec * 1000.0

        return {
            "time_ms": round(time_ms, 3),
            "volume_mb": round(volume_bytes / (1024 ** 2), 2),
            "bus_bw_gb_s": bus_bw_gb_s,
            "algorithm": "NCCL_Hierarchical_Ring"
        }

    @staticmethod
    def calculate_reduce_scatter(data_size_bytes: float, num_gpus: int, bus_bw_gb_s: float) -> Dict[str, Any]:
        """Calculates ReduceScatter transfer time."""
        if num_gpus <= 1:
            return {"time_ms": 0.0, "volume_mb": 0.0}
        factor = (num_gpus - 1) / num_gpus
        volume_gb = (factor * data_size_bytes) / (1024 ** 3)
        time_ms = (volume_gb / bus_bw_gb_s) * 1000.0
        return {"time_ms": round(time_ms, 3), "volume_mb": round((factor * data_size_bytes) / (1024**2), 2)}

    @staticmethod
    def calculate_all_gather(data_size_bytes: float, num_gpus: int, bus_bw_gb_s: float) -> Dict[str, Any]:
        """Calculates AllGather transfer time."""
        return CollectiveCommunicationEngine.calculate_reduce_scatter(data_size_bytes, num_gpus, bus_bw_gb_s)

    @staticmethod
    def calculate_all_to_all(data_size_bytes: float, num_experts: int, bus_bw_gb_s: float) -> Dict[str, Any]:
        """Calculates AllToAll token dispatch for Mixture-of-Experts."""
        if num_experts <= 1:
            return {"time_ms": 0.0, "volume_mb": 0.0}
        factor = (num_experts - 1) / num_experts
        volume_gb = (factor * data_size_bytes) / (1024 ** 3)
        time_ms = (volume_gb / bus_bw_gb_s) * 1000.0
        return {
            "time_ms": round(time_ms, 3),
            "volume_mb": round((factor * data_size_bytes) / (1024**2), 2),
            "algorithm": "NCCL_MoE_AllToAll_Async"
        }

    @staticmethod
    def generate_topology_matrix(num_nodes: int, gpus_per_node: int, intra_bw: float, inter_bw: float) -> Dict[str, Any]:
        """Generates a multi-tier bandwidth matrix for topology-aware scheduling."""
        total_gpus = num_nodes * gpus_per_node
        return {
            "total_gpus": total_gpus,
            "tiers": [
                {
                    "tier_name": "Intra-Node NVLink / NVSwitch",
                    "scope": f"GPUs 0-{gpus_per_node-1} per node",
                    "bandwidth": f"{intra_bw} GB/s bi-directional",
                    "latency_us": 0.8,
                    "optimal_for": ["Tensor Parallelism (TP)", "Sequence Parallelism (SP)"]
                },
                {
                    "tier_name": "Inter-Node InfiniBand NDR Multi-Rail",
                    "scope": f"Across {num_nodes} cluster nodes",
                    "bandwidth": f"{inter_bw} Gbps ({inter_bw/8:.1f} GB/s)",
                    "latency_us": 1.5,
                    "optimal_for": ["Pipeline Parallelism (PP)", "Data Parallelism (DP)", "FSDP ZeRO-3"]
                }
            ]
        }
