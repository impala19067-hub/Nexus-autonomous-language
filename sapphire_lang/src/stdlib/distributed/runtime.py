"""
Sapphire Distributed Training Runtime & Execution Orchestrator
Executes:
- Auto-Parallelism Strategy Synthesis
- NCCL Collective Communication Scheduling
- High-Performance Kernel Dispatch Table
- Theoretical Cluster Throughput & TFLOPs Simulator
- 1-Click PyTorch / CUDA Codegen Compilation
"""

import os
import json
import time
from typing import Dict, Any, Optional

from src.stdlib.distributed.transformer_spec import Transformer
from src.stdlib.distributed.cluster_spec import Cluster
from src.stdlib.distributed.auto_parallelism import AutoParallelismSolver, ParallelismPlan
from src.stdlib.distributed.collectives import CollectiveCommunicationEngine
from src.stdlib.distributed.kernel_optimizer import KernelOptimizer
from src.stdlib.distributed.codegen import DistributedCodegen

class DistributedTrainJob:
    """
    Sapphire Frontier Distributed Training Job.
    Compiles and executes distributed training models.
    """
    def __init__(
        self,
        model: Transformer,
        cluster: Cluster,
        strategy: str = "auto",
        precision: str = "fp8",
        optimizer: str = "adamw",
        global_batch_size: int = 1024,
        micro_batch_size: Optional[int] = None,
        sequence_length: Optional[int] = None,
        checkpoint_every: int = 1000,
        flash_attention: bool = True,
        activation_checkpointing: bool = True,
        export_codegen: bool = True,
        output_dir: str = "./distributed_build"
    ):
        self.model = model
        self.cluster = cluster
        self.strategy = strategy
        self.precision = precision.lower()
        self.optimizer = optimizer
        self.global_batch_size = int(global_batch_size)
        self.micro_batch_size = micro_batch_size
        self.sequence_length = int(sequence_length) if sequence_length else model.seq_len
        self.checkpoint_every = int(checkpoint_every)
        self.flash_attention = bool(flash_attention)
        self.activation_checkpointing = bool(activation_checkpointing)
        self.export_codegen = bool(export_codegen)
        self.output_dir = output_dir

        # Run Auto-Parallelism Solver
        self.plan = AutoParallelismSolver.solve(
            model=self.model,
            cluster=self.cluster,
            precision=self.precision,
            global_batch_size=self.global_batch_size,
            micro_batch_size=self.micro_batch_size,
            seq_len=self.sequence_length,
            strategy=self.strategy,
            activation_checkpointing=self.activation_checkpointing
        )

        # Compute Cluster Training Throughput
        self.throughput_metrics = self._compute_throughput()

        # Generate Codegen Artifacts
        if self.export_codegen:
            self._generate_codegen_artifacts()

    def _compute_throughput(self) -> Dict[str, Any]:
        """Calculates theoretical tokens/sec, step time, and cluster TFLOPs."""
        tokens_per_batch = self.global_batch_size * self.sequence_length
        flops_per_batch = tokens_per_batch * self.model.flops_per_token

        # Cluster peak compute based on precision
        peak_tflops_per_gpu = self.cluster.fp8_tflops_per_gpu if "fp8" in self.precision else self.cluster.bf16_tflops_per_gpu
        cluster_peak_tflops = self.cluster.gpus * peak_tflops_per_gpu
        
        # Effective compute delivered (MFU)
        delivered_tflops = cluster_peak_tflops * self.plan.estimated_mfu

        # Step time in seconds
        step_time_sec = (flops_per_batch / 1e12) / max(1.0, delivered_tflops)
        tokens_per_sec = tokens_per_batch / max(0.001, step_time_sec)

        # Time to train 10 Trillion tokens (standard frontier dataset)
        target_tokens = 10e12
        days_to_train_10t = (target_tokens / tokens_per_sec) / (3600 * 24)

        return {
            "tokens_per_batch": tokens_per_batch,
            "tokens_per_sec": round(tokens_per_sec, 1),
            "step_time_ms": round(step_time_sec * 1000.0, 2),
            "cluster_delivered_pflops": round(delivered_tflops / 1000.0, 2),
            "cluster_peak_pflops": round(cluster_peak_tflops / 1000.0, 2),
            "mfu_percent": round(self.plan.estimated_mfu * 100.0, 2),
            "days_to_train_10T_tokens": round(days_to_train_10t, 2)
        }

    def _generate_codegen_artifacts(self):
        """Emits PyTorch, Shell, and IR build files."""
        os.makedirs(self.output_dir, exist_ok=True)

        py_path = os.path.join(self.output_dir, "train_distributed_pytorch.py")
        with open(py_path, "w", encoding="utf-8") as f:
            f.write(DistributedCodegen.generate_pytorch_script(self.model, self.cluster, self.plan))

        sh_path = os.path.join(self.output_dir, "launch_cluster.sh")
        with open(sh_path, "w", encoding="utf-8") as f:
            f.write(DistributedCodegen.generate_launch_script(self.cluster))

        ir_path = os.path.join(self.output_dir, "sapphire_dist_ir.json")
        with open(ir_path, "w", encoding="utf-8") as f:
            ir_data = {
                "sapphire_version": "1.0.0",
                "model": self.model.summary(),
                "cluster": self.cluster.summary(),
                "parallelism_plan": self.plan.summary(),
                "throughput": self.throughput_metrics,
                "kernels": KernelOptimizer.get_kernel_dispatch_table(self.flash_attention, self.precision),
                "fp8_recipe": KernelOptimizer.fp8_recipe() if "fp8" in self.precision else None
            }
            json.dump(ir_data, f, indent=2)

    def summary(self) -> Dict[str, Any]:
        return {
            "model": self.model.summary(),
            "cluster": self.cluster.summary(),
            "plan": self.plan.summary(),
            "throughput": self.throughput_metrics,
            "codegen_artifacts": {
                "pytorch_script": os.path.join(self.output_dir, "train_distributed_pytorch.py"),
                "launch_script": os.path.join(self.output_dir, "launch_cluster.sh"),
                "ir_graph": os.path.join(self.output_dir, "sapphire_dist_ir.json")
            }
        }

    def __repr__(self) -> str:
        s = self.summary()
        return (
            f"💎 Sapphire.DistributedTrainJob(\n"
            f"  Model: {self.model.total_params / 1e9:.1f}B params on {self.cluster.gpus} GPUs ({self.cluster.aggregate_memory_tb:.1f} TB VRAM)\n"
            f"  Strategy: {self.plan.strategy_name}\n"
            f"  Throughput: {self.throughput_metrics['tokens_per_sec']:,.0f} tokens/s ({self.throughput_metrics['cluster_delivered_pflops']} PFLOPs, MFU: {self.throughput_metrics['mfu_percent']}%)\n"
            f"  10T Tokens Estimated Time: {self.throughput_metrics['days_to_train_10T_tokens']} Days\n"
            f")"
        )

def train(*args, **kwargs) -> DistributedTrainJob:
    """Entry point function for Sapphire ml.distributed.train(...)"""
    if len(args) == 1 and isinstance(args[0], dict):
        kwargs = {**args[0], **kwargs}

    model = kwargs.get("model", args[0] if len(args) > 0 and not isinstance(args[0], dict) else None)
    cluster = kwargs.get("cluster", args[1] if len(args) > 1 else None)
    strategy = str(kwargs.get("strategy", args[2] if len(args) > 2 else "auto"))
    precision = str(kwargs.get("precision", args[3] if len(args) > 3 else "fp8"))
    optimizer = str(kwargs.get("optimizer", args[4] if len(args) > 4 else "adamw"))
    global_batch_size = int(kwargs.get("global_batch_size", 1024))
    micro_batch_size = kwargs.get("micro_batch_size", None)
    sequence_length = kwargs.get("sequence_length", None)
    checkpoint_every = int(kwargs.get("checkpoint_every", 1000))
    flash_attention = bool(kwargs.get("flash_attention", True))
    activation_checkpointing = bool(kwargs.get("activation_checkpointing", True))
    export_codegen = bool(kwargs.get("export_codegen", True))
    output_dir = str(kwargs.get("output_dir", "./distributed_build"))

    job = DistributedTrainJob(
        model=model,
        cluster=cluster,
        strategy=strategy,
        precision=precision,
        optimizer=optimizer,
        global_batch_size=global_batch_size,
        micro_batch_size=micro_batch_size,
        sequence_length=sequence_length,
        checkpoint_every=checkpoint_every,
        flash_attention=flash_attention,
        activation_checkpointing=activation_checkpointing,
        export_codegen=export_codegen,
        output_dir=output_dir
    )
    return job
