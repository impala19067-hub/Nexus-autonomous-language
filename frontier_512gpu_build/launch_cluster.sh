#!/usr/bin/env bash
# 💎 SAPPHIRE DISTRIBUTED RUNTIME LAUNCHER
# Launching on 64 Nodes with 8 GPUs per node (512 total GPUs)

export NCCL_DEBUG=INFO
export NCCL_IB_DISABLE=0
export NCCL_NET_GDR_LEVEL=5
export CUDA_DEVICE_MAX_CONNECTIONS=1

torchrun \
    --nproc_per_node=8 \
    --nnodes=64 \
    --node_rank=$SLURM_NODEID \
    --master_addr=$MASTER_ADDR \
    --master_port=29500 \
    train_distributed_pytorch.py
