"""
Sapphire Frontier Distributed AI & Auto-Parallelism Module
Exports:
- Transformer: Frontier LLM model definition
- Cluster: Hardware supercomputer cluster topology
- train: 5D Auto-Parallelism distributed compiler & trainer
- AutoParallelismSolver: 5D (TP x PP x DP x EP x SP x ZeRO) Solver
- CollectiveCommunicationEngine: NCCL collective scheduling
- KernelOptimizer: FlashAttention-3 & FP8 TransformerEngine
- DistributedCodegen: PyTorch / CUDA / DeepSpeed code generator
"""

from src.stdlib.distributed.transformer_spec import Transformer
from src.stdlib.distributed.cluster_spec import Cluster
from src.stdlib.distributed.auto_parallelism import AutoParallelismSolver, ParallelismPlan
from src.stdlib.distributed.collectives import CollectiveCommunicationEngine
from src.stdlib.distributed.kernel_optimizer import KernelOptimizer
from src.stdlib.distributed.codegen import DistributedCodegen
from src.stdlib.distributed.runtime import DistributedTrainJob, train

class DistributedModule:
    """
    Namespace class for ml.distributed in Sapphire.
    """
    Transformer = Transformer
    Cluster = Cluster
    train = staticmethod(train)
    auto_parallelism = AutoParallelismSolver
    collectives = CollectiveCommunicationEngine
    kernels = KernelOptimizer
    codegen = DistributedCodegen

    @staticmethod
    def info() -> str:
        return (
            "=== 💎 Sapphire Frontier Distributed LLM Architecture ===\n"
            "  • 5D Auto-Parallelism : Tensor (TP) x Pipeline (PP) x Data (DP) x Expert (EP) x Sequence (SP)\n"
            "  • Sharding Stacks     : FSDP / ZeRO-1/2/3 & Hybrid Sharded Data Parallel (HSDP)\n"
            "  • Precisions          : FP8 (E4M3/E5M2 Delayed Scaling), BF16, Dynamic FP16\n"
            "  • Fused Kernels       : FlashAttention-3, Triton Fused RMSNorm/SwiGLU, Chunked Loss\n"
            "  • Collective Engine   : NCCL Topology-Aware Hierarchical Ring & Tree Overlap\n"
            "  • Codegen Backends    : PyTorch Distributed, Megatron-Core, DeepSpeed, Torchrun\n"
        )
