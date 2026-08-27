"""
Sapphire Cluster Hardware Topology & Interconnect Specification
Defines:
- Cluster: Multi-node GPU supercomputer topology
- Hardware profiles: H100, B200, H200, A100, RTX4090, TPU v5p
- Interconnect specs: NVLink, NVSwitch, InfiniBand NDR/HDR, PCIe 5.0
"""

from typing import Dict, Any, Optional

GPU_HARDWARE_DATABASE = {
    "H100-80GB": {
        "memory_gb": 80.0,
        "memory_bw_tb_s": 3.35, # HBM3
        "fp8_tflops": 1979.0,   # Tensor Core FP8 with sparsity
        "bf16_tflops": 989.0,   # Tensor Core BF16 with sparsity
        "fp16_tflops": 989.0,
        "fp32_tflops": 67.0,
        "intra_node_bw_gb_s": 900.0, # NVLink 4
        "inter_node_default_gbps": 400.0 # InfiniBand NDR
    },
    "H200-141GB": {
        "memory_gb": 141.0,
        "memory_bw_tb_s": 4.8,  # HBM3e
        "fp8_tflops": 1979.0,
        "bf16_tflops": 989.0,
        "fp16_tflops": 989.0,
        "fp32_tflops": 67.0,
        "intra_node_bw_gb_s": 900.0,
        "inter_node_default_gbps": 800.0
    },
    "B200-192GB": {
        "memory_gb": 192.0,
        "memory_bw_tb_s": 8.0,  # HBM3e
        "fp8_tflops": 4500.0,   # Blackwell FP8
        "bf16_tflops": 2250.0,
        "fp16_tflops": 2250.0,
        "fp32_tflops": 90.0,
        "intra_node_bw_gb_s": 1800.0, # NVLink 5
        "inter_node_default_gbps": 800.0
    },
    "A100-80GB": {
        "memory_gb": 80.0,
        "memory_bw_tb_s": 2.039,
        "fp8_tflops": 0.0,      # A100 does not have native FP8
        "bf16_tflops": 312.0,
        "fp16_tflops": 312.0,
        "fp32_tflops": 19.5,
        "intra_node_bw_gb_s": 600.0, # NVLink 3
        "inter_node_default_gbps": 200.0 # InfiniBand HDR
    },
    "RTX-4090-24GB": {
        "memory_gb": 24.0,
        "memory_bw_tb_s": 1.008,
        "fp8_tflops": 660.0,
        "bf16_tflops": 165.0,
        "fp16_tflops": 165.0,
        "fp32_tflops": 82.6,
        "intra_node_bw_gb_s": 64.0,  # PCIe 4.0 x16
        "inter_node_default_gbps": 10.0 # Ethernet 10GbE
    }
}

class Cluster:
    """
    Sapphire Cluster Hardware Topology Specification.
    Models multi-node GPU supercomputers with exact memory, bandwidth, and compute FLOPs.
    """
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            kwargs = {**args[0], **kwargs}

        self.gpus = int(kwargs.get("gpus", args[0] if len(args) > 0 and not isinstance(args[0], dict) else 512))
        self.gpus_per_node = int(kwargs.get("gpus_per_node", args[2] if len(args) > 2 else 8))
        nodes_arg = kwargs.get("nodes", args[1] if len(args) > 1 else None)
        self.nodes = int(nodes_arg) if nodes_arg is not None else max(1, self.gpus // self.gpus_per_node)
        self.gpu_type = str(kwargs.get("gpu_type", args[3] if len(args) > 3 else "H100-80GB"))
        self.interconnect = str(kwargs.get("interconnect", "NVLink-InfiniBand"))

        # Lookup hardware specs
        hw = GPU_HARDWARE_DATABASE.get(self.gpu_type, GPU_HARDWARE_DATABASE["H100-80GB"])
        mem_gb = kwargs.get("memory_per_gpu_gb", None)
        self.memory_per_gpu_gb = float(mem_gb) if mem_gb is not None else hw["memory_gb"]
        
        intra_bw = kwargs.get("intra_node_bw_gb_s", None)
        self.intra_node_bw_gb_s = float(intra_bw) if intra_bw is not None else hw["intra_node_bw_gb_s"]
        
        inter_bw = kwargs.get("inter_node_bw_gbps", None)
        self.inter_node_bw_gbps = float(inter_bw) if inter_bw is not None else hw["inter_node_default_gbps"]
        
        self.fp8_tflops_per_gpu = hw["fp8_tflops"]
        self.bf16_tflops_per_gpu = hw["bf16_tflops"]
        self.memory_bw_tb_s = hw["memory_bw_tb_s"]

        # Aggregate Metrics
        self.aggregate_memory_tb = (self.gpus * self.memory_per_gpu_gb) / 1024.0
        self.aggregate_bf16_pflops = (self.gpus * self.bf16_tflops_per_gpu) / 1000.0
        self.aggregate_fp8_pflops = (self.gpus * self.fp8_tflops_per_gpu) / 1000.0

    def summary(self) -> Dict[str, Any]:
        return {
            "gpus": self.gpus,
            "nodes": self.nodes,
            "gpus_per_node": self.gpus_per_node,
            "gpu_type": self.gpu_type,
            "memory_per_gpu_gb": self.memory_per_gpu_gb,
            "aggregate_memory_tb": round(self.aggregate_memory_tb, 2),
            "aggregate_bf16_pflops": round(self.aggregate_bf16_pflops, 2),
            "aggregate_fp8_pflops": round(self.aggregate_fp8_pflops, 2),
            "interconnect": self.interconnect,
            "intra_node_bw_gb_s": self.intra_node_bw_gb_s,
            "inter_node_bw_gbps": self.inter_node_bw_gbps
        }

    def __repr__(self) -> str:
        s = self.summary()
        return (
            f"💎 Sapphire.Cluster({self.gpus}x {self.gpu_type}, {self.nodes} nodes, "
            f"Total Memory={s['aggregate_memory_tb']} TB, Peak BF16={s['aggregate_bf16_pflops']} PFLOPs)"
        )
