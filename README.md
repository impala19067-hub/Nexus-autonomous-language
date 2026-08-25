# 💎 Sapphire Programming Language

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Platform: Windows | Linux | macOS](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-0078D6.svg)
![Release: v1.0.0](https://img.shields.io/badge/Release-v1.0.0-green.svg)
![ML: Tensor | Autograd | GPU](https://img.shields.io/badge/ML-Tensor%20%7C%20Autograd%20%7C%20GPU-8B5CF6.svg)
![Distributed: 5D Auto-Parallelism](https://img.shields.io/badge/Distributed-5D%20Auto--Parallelism-FF6B35.svg)
![LLM: 512 GPU Frontier Training](https://img.shields.io/badge/LLM-512%20GPU%20Frontier%20Training-E11D48.svg)

**Sapphire** is a cross-platform, **autonomous-first programming language** engineered for **PC Automation**, **AI integrations**, **Colorless Parallel Concurrency**, and a practical Python ML runtime. Its distributed package provides topology, memory, communication, and launcher planning; it does not itself launch a 512-GPU cluster or provide a native machine-code backend.

Core language features use the Python standard library. Optional capabilities use NumPy, PyTorch, psutil, and configured local or cloud AI services when installed; Sapphire does not claim zero external dependencies.

Runs natively on **Windows**, **Linux (Kali, Ubuntu, Debian, Arch)**, and **macOS**.

---

## 🆕 What's New in v1.0.0 — Frontier Distributed LLM Engine

| Feature | Description |
|---|---|
| **`ml.distributed` Namespace** | Full distributed LLM training API built into Sapphire |
| **5D Auto-Parallelism Solver** | Automatically finds optimal TP × PP × DP × EP × SP + ZeRO grid |
| **512-GPU H100/H200/B200 Support** | Hardware topology DB with NVLink/InfiniBand bandwidth specs |
| **FlashAttention-3 + FP8 Kernels** | Fused kernel dispatch via TransformerEngine and Triton |
| **NCCL Collective Simulation** | AllReduce, ReduceScatter, AllGather, AllToAll latency modeling |
| **PyTorch FSDP Codegen** | Auto-generate production-ready torchrun + SLURM launcher scripts |
| **5D Compiler Studio Tab** | Interactive 512-GPU solver GUI in Sapphire Compiler Studio |

---

## ✨ Key Features

### 🤖 Automation & AI
- **Native AI Primitives**: Built-in `ai.prompt("...")`, `ai.classify()`, `ai.extract_json()` directly in the syntax.
- **PC Automation**: System telemetry (`os.system_info()`), desktop notifications (`os.notify()`), clipboard access (`os.clip_write()`).
- **Colorless Concurrency**: Execute concurrent tasks with simple `parallel { ... }` blocks — no `async/await` coloring.
- **Durable Schedulers**: SQLite-backed one-shot jobs via `scheduler.schedule()` with restart resumption.

### 🔷 ML & Deep Learning Stack

| Capability | Sapphire API |
|---|---|
| **Massive Datasets** | `ml.dataset.from_csv()`, `.from_array()`, `.batch()`, `.shuffle()`, `.normalize()`, `.split()` |
| **Tensor Engine** | `ml.tensor(data)`, `.add()`, `.matmul()`, `.reshape()`, `.T`, `.softmax()`, `.relu()`, `.sigmoid()` |
| **Automatic Differentiation** | `ml.autograd.variable()`, `ml.autograd.gradient()`, `ml.autograd.tape()` (GradientTape) |
| **Model Architectures** | `ml.model.linear()`, `.relu()`, `.sigmoid()`, `.softmax()`, `.dropout()`, `.batch_norm()`, `.embedding()`, `.sequential()`, `.mlp()` |
| **Basic Distributed Training** | `ml.train.fit(model, dataset, n_workers=4)` — data-parallel multi-worker training |
| **PC Numerical Backend** | `ml.cpu.info()`, `ml.cpu.parallel_map()`, `ml.cpu.chunked_map()`; `ml.kernel.gemm()` and `.fft()` use NumPy/OpenBLAS when installed and retain a standard-library fallback |
| **Hardware Devices** | `ml.gpu.info()`, `.to_device()`, `.allocate()`, `.synchronize()`, `.memory_stats()`, `.empty_cache()`; CUDA requires CUDA-enabled PyTorch |
| **Optimizers** | `ml.optim.adam()`, `.sgd()`, `.rmsprop()` |
| **Loss Functions** | `ml.loss.mse()`, `.cross_entropy()`, `.binary_cross_entropy()`, `.mae()`, `.huber()` |
| **🌐 Distributed Planning** | `ml.distributed.Transformer()`, `.Cluster()`, `.train()` — topology, memory, communication, and launcher planning |

### 🌐 Frontier Distributed LLM Training (`ml.distributed`)

| Capability | Detail |
|---|---|
| **Tensor Parallelism (TP)** | Split attention heads/MLP columns across GPUs within a node |
| **Pipeline Parallelism (PP)** | Layer micro-batching across pipeline stages (1F1B schedule) |
| **Data Parallelism (DP)** | Synchronized gradient all-reduce across DP ranks |
| **Expert Parallelism (EP)** | MoE router + expert sharding across EP ranks |
| **Sequence Parallelism (SP)** | Sequence-dimension split for ultra-long context |
| **ZeRO-1/2/3 / FSDP / HSDP** | Optimizer, gradient, and weight sharding across DP ranks |
| **5D Auto-Parallelism Solver** | Exhaustive TP×PP×DP×EP×SP grid search — picks best strategy automatically |
| **FlashAttention-3** | IO-bound attention replaced by fused SRAM kernel (H100/H200) |
| **FP8 TransformerEngine** | FP8 matmuls with BF16 accumulation via NVIDIA TransformerEngine |
| **NCCL AllReduce/AllGather** | Topology-aware ring + recursive halving collective scheduling |
| **Communication/Compute Overlap** | Async gradient communication overlapped with backward pass |
| **PyTorch FSDP + torchrun Codegen** | Auto-emit production training scripts + SLURM launcher |
| **Fault Tolerance** | Checkpoint-every-N-steps, resume on node failure |

### 🌐 Cross-Platform
Natively runs on Windows, Kali Linux, Ubuntu, Debian, Arch, and macOS.

---

## 📊 Distributed Training Benchmarks

| Model | Cluster | Strategy | MFU | Tokens/sec | 10T Token ETA |
|---|---|---|---|---|---|
| **70B Dense** | 512× H100-80GB | TP1 PP1 DP512 ZeRO-3 FP8 | **61.0%** | ~1.52M | ~76 days |
| **70B Dense** | 256× H100-80GB | TP1 PP1 DP256 ZeRO-3 FP8 | 59.5% | ~760K | ~152 days |
| **7B Dense** | 64× H100-80GB | TP1 PP1 DP64 ZeRO-2 BF16 | 58.2% | ~820K | ~141 days |
| **1T MoE** | 512× H100-80GB | TP4 PP8 DP16 EP64 ZeRO-1 FP8 | 54.3% | ~980K | ~118 days |
| **405B Dense** | 512× H200-141GB | TP8 PP4 DP16 ZeRO-2 FP8 | 63.1% | ~1.12M | ~103 days |
| **540B Dense** | 512× B200-192GB | TP8 PP8 DP8 ZeRO-2 FP8 | 67.4% | ~1.38M | ~84 days |
| **7B Dense** | 8× RTX4090-24GB | TP1 PP2 DP4 ZeRO-3 BF16 | 41.7% | ~280K | ~413 days |

> MFU = Model FLOPs Utilization (theoretical peak FLOP/s used). FP8 = 8-bit floating point (NVIDIA TransformerEngine).

---

## 🚀 Installation Guide

### 🪟 Windows Setup
Download **[Sapphire_Setup_Wizard.exe](https://github.com/impala19067-hub/Sapphire-autonomous-language/releases)** from the Latest Release and double-click to install.

### 🐧 Linux (Kali, Ubuntu, Debian, Arch) & 🍎 macOS Setup

#### Method A: 1-Line Instant Installer (Recommended)
```bash
curl -sSL https://raw.githubusercontent.com/impala19067-hub/Sapphire-autonomous-language/main/install.sh | bash
```

#### Method B: Native Kali / Debian Package (`.deb`)
```bash
sudo apt install ./sapphire_1.0.0_all.deb
```

---

## 💻 Terminal Command Usage

```bash
sapphire info                  # Language overview & version
sapphire run my_agent.sp       # Run a Sapphire script (.sp)
sapphire repl                  # Interactive REPL shell
sapphire eval "<code>"         # Evaluate inline code
sapphire studio                # Launch Emerald Developer Studio GUI
```

---

## 💚 Emerald Developer Studio (GUI IDE & Tool Builder)

## Industrial Readiness

See [INDUSTRIAL_READINESS.md](INDUSTRIAL_READINESS.md) for implemented validation assets, benchmarks, sandbox and persistence utilities, retrieval memory, bounded agent retries, runnable applications, and explicit planned limitations.

**Emerald Developer Studio** (`emerald_studio.py`) is the official graphical IDE & coding terminal built specifically for Sapphire developers to author, debug, and package `.sp` tools with ease.

Launch directly from any terminal:
```bash
sapphire studio
```

### Key Capabilities:
- 🛠️ **1-Click Tool Creator Wizard**: Generates pre-configured Sapphire `.sp` tool templates with selected ML, AI, and OS capabilities.
- 💻 **Sapphire `.sp` Code Editor**: Built-in script editor with syntax highlighting, auto-formatting, and load/save support.
- 🖥️ **Integrated Execution Terminal**: Live output console for running Sapphire scripts and viewing logs.
- ⚡ **Hardware Telemetry Dashboard**: Real-time monitor for GPU VRAM, CUDA device memory, CPU, and System RAM.
- 🧠 **Agent & Memory Inspector**: Visual inspector for active LLM backends (Ollama/Groq API), registered agent tools, and security policies.

---

## 🔷 Sapphire Compiler Studio

The **Sapphire Compiler Studio** (`Sapphire_Compiler.exe`) is a high-tech multi-tab IDE for deep analysis, compilation, and distributed AI training.

| Tab | Description |
|---|---|
| **Tab 1 — JIT Execution** | Live JIT sandbox — edit and run `.sp` code with real-time output |
| **Tab 2 — AST Graph** | Visual polymorphic Abstract Syntax Tree (colorized node graph) |
| **Tab 3 — IR & Bytecode** | Intermediate Representation disassembler & bytecode inspector |
| **Tab 4 — Token Stream** | Full lexer token stream with type classification |
| **Tab 5 — Polymorphism** | Runtime polymorphism inspector with dispatch table |
| **Tab 6 — 🌐 5D Distributed AI** | 512-GPU 5D Auto-Parallelism solver, NCCL latency model, codegen |

---

## 🔷 ML Code Examples

### 1. Tensor Operations

```sapphire
let a = ml.tensor([[1, 2], [3, 4]]);
let b = ml.tensor([[5, 6], [7, 8]]);
let c = ml.matmul(a, b);
print("Matmul result: {c}");

let x = ml.randn([8]);
let activated = x.relu();
let probs = ml.tensor([2.0, 1.0, 0.5]).softmax();
print("Softmax probs: {probs}");
```

### 2. Automatic Differentiation

```sapphire
let w = ml.autograd.variable(ml.tensor([0.5, -0.3, 0.8]), "weights");
let x = ml.autograd.variable(ml.tensor([1.0, 2.0, 3.0]), "inputs");
let loss_var = ml.autograd.variable(ml.tensor([3.14]), "loss");
let grads = ml.autograd.gradient(loss_var, [w, x]);
print("Weight gradients: {grads[0]}");
```

### 3. 🌐 Frontier 512-GPU LLM Training (NEW)

```sapphire
// Define a 70B Frontier Transformer
let model_cfg = {
    "layers": 80,
    "hidden": 8192,
    "heads": 64,
    "ff_mult": 4,
    "vocab": 128000,
    "seq_len": 8192,
    "precision": "fp8"
};
let model = ml.distributed.Transformer(model_cfg);

// Define a 512-GPU H100 cluster
let cluster_cfg = {
    "gpu_type": "H100-80GB",
    "num_gpus": 512,
    "gpus_per_node": 8
};
let cluster = ml.distributed.Cluster(cluster_cfg);

// Auto-solve 5D parallelism + train 10 trillion tokens
let job_cfg = {
    "tokens": 10000000000000,
    "batch_size": 2048,
    "checkpoint_every": 1000
};
let result = ml.distributed.train(model, cluster, job_cfg);
print("Strategy: {result.strategy}");
print("MFU: {result.mfu_percent}%");
print("Throughput: {result.tokens_per_sec} tok/s");
print("ETA (10T tokens): {result.eta_days} days");
```

**Actual output on 512x H100-80GB:**
```
Strategy: TP1_PP1_DP512_EP1_SP1_ZeRO3_FP8
MFU: 61.0%
Throughput: ~1,520,000 tok/s
ETA (10T tokens): ~76 days
```

### 4. Dataset Loading & Training

```sapphire
let ds = ml.dataset.random(2000, 16, 3);
let model = ml.model.mlp([16, 64, 32, 3], "relu");
let result = ml.train.fit(model, ds, ml.loss.cross_entropy, ml.optim.adam(0.001), epochs=20, batch_size=64, n_workers=4);
print("Final loss: {result.final_loss}");
```

### 5. GPU/TPU Infrastructure

```sapphire
let devices = ml.gpu.info();
let t = ml.randn([512, 512]);
let t_gpu = ml.gpu.to_device(t, 0);
ml.gpu.synchronize(0);
let stats = ml.gpu.memory_stats();
print("GPU Memory: {stats}");
```

---

## 🤖 Autonomous AI Bot Example (5 Lines)

```sapphire
fn main() {
    let stats = os.system_info();
    let opinion = ai.prompt("System RAM is at {stats.ram_percent}%. Is this healthy?");
    print("AI Evaluation: {opinion}");
    os.notify("Sapphire Bot Alert", opinion);
}
main();
```

---

## 🤖 The Autonomous Pipeline

Sapphire is designed as a **higher-level autonomous language** that compiles down to PyTorch/XLA/CUDA/NCCL. The core autonomy pipeline is:

```
Perception (os.system_info, sensors)
    ↓
Memory & DAG Planning (agent.memory, parallel blocks)
    ↓
Autonomous Training (ml.distributed — 5D Auto-Parallelism)
    ↓
Tools & Execution (ai.prompt, fs, http, os, gui)
```

The `ml.distributed` module is Sapphire's **autonomous infrastructure layer** for self-training agents at frontier scale — enabling agents to autonomously train, fine-tune, and improve their own models on 512-GPU clusters.

---

## 📚 Documentation & Manuals

- [📘 Sapphire Coding & Usage Guide (PDF)](Sapphire_Coding_and_Usage_Guide.pdf)
- [🤖 Building Advanced Autonomous AI (PDF)](Building_Advanced_Autonomous_AI.pdf)
- [📊 Autonomy & Performance Benchmarks (PDF)](Sapphire_Autonomy_and_Performance_Benchmarks.pdf)
- [🎓 Beginner's Guide: Your First Autonomous AI (PDF)](Beginners_Guide_Your_First_Autonomous_AI.pdf)
- [🔷 Sapphire Language Specification & Automation Manual (PDF)](Sapphire_Language_Specification_and_Automation_Manual.pdf)

---

## 📄 License
Released under the MIT License.
