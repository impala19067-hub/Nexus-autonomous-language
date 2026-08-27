# Sapphire Programming Language

<<<<<<< HEAD
<<<<<<< HEAD
Sapphire is a Python-based interpreted programming language and Windows distribution for local scripting, automation, AI-assisted workflows, and prototype ML tooling. It is designed for learning, experimentation, and local PC automation rather than for claiming a full production-grade distributed AI platform.

## Current release
=======
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Platform: Windows | Linux | macOS](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-0078D6.svg)
![Release: v1.0.0](https://img.shields.io/badge/Release-v1.0.0-green.svg)
![ML: Tensor | Autograd | GPU](https://img.shields.io/badge/ML-Tensor%20%7C%20Autograd%20%7C%20GPU-8B5CF6.svg)
![Distributed: 5D Auto-Parallelism](https://img.shields.io/badge/Distributed-5D%20Auto--Parallelism-FF6B35.svg)
![LLM: 512 GPU Frontier Training](https://img.shields.io/badge/LLM-512%20GPU%20Frontier%20Training-E11D48.svg)

**Sapphire** is a cross-platform, **autonomous-first programming language** engineered for **PC Automation**, **Native AI Intelligence**, **Colorless Parallel Concurrency**, and a **full ML/Deep Learning stack** — including a **frontier-scale distributed LLM training engine** (`ml.distributed`) capable of orchestrating 512-GPU H100 clusters with 5D Auto-Parallelism, FlashAttention-3, FP8, and NCCL-optimized collectives — all built into the language runtime with zero external dependencies.
>>>>>>> bf07d50 (docs: add ch14 Distributed LLM to tutor, regenerate all 5 PDFs, update README with frontier stats)
=======
Sapphire is a Python-based interpreted programming language and Windows distribution for local scripting, automation, AI-assisted workflows, and prototype ML tooling. It is designed for learning, experimentation, and local PC automation rather than for claiming a full production-grade distributed AI platform.

## Current release
>>>>>>> 732e4d1 (Update README and documentation bundle)

- Language and installer version: 1.0.5
- Tested interpreter: Python 3.12.10
- Primary distribution: Windows setup wizard, CLI tools, and bundled documentation
- Optional integrations: NumPy, PyTorch, psutil, requests, audio packages, and configured AI service backends

## What Sapphire includes

<<<<<<< HEAD
<<<<<<< HEAD
### Language features
=======
## 🆕 What's New in v1.0.0 — Frontier Distributed LLM Engine
=======
### Language features
>>>>>>> 732e4d1 (Update README and documentation bundle)

- `let` and `const` declarations with optional type annotations
- Functions, conditionals, loops, arrays, maps, structs, lambdas, returns, and exceptions
- Arithmetic, comparisons, boolean logic, indexing, member access, and pipelines
- `parallel { ... }` execution blocks
- Shell/process literals using backticks or `$`, returning a `ProcessResult`
- `.sp` script execution, REPL mode, inline evaluation, and CLI inspection tools

### Standard library

<<<<<<< HEAD
## ✨ Key Features
>>>>>>> bf07d50 (docs: add ch14 Distributed LLM to tutor, regenerate all 5 PDFs, update README with frontier stats)

- `let` and `const` declarations with optional type annotations
- Functions, conditionals, loops, arrays, maps, structs, lambdas, returns, and exceptions
- Arithmetic, comparisons, boolean logic, indexing, member access, and pipelines
- `parallel { ... }` execution blocks
- Shell/process literals using backticks or `$`, returning a `ProcessResult`
- `.sp` script execution, REPL mode, inline evaluation, and CLI inspection tools

### Standard library

<<<<<<< HEAD
- `os`: system information, process control, notifications, clipboard access, and bounded command execution
- `fs`: file read/write/append/remove operations
- `http`: optional HTTP helpers when the dependency is installed
- `ai`: prompt, classification, and JSON extraction flows via local/cloud backends or offline fallback behavior
- `ml`: tensor primitives, dataset helpers, optimization and loss utilities, and optional CUDA/PyTorch execution paths
- `scheduler`: SQLite-backed scheduled work
- `agent`: memory, planning, permissions, bounded execution, and orchestration support
=======
| Capability | Sapphire API |
|---|---|
| **Massive Datasets** | `ml.dataset.from_csv()`, `.from_array()`, `.batch()`, `.shuffle()`, `.normalize()`, `.split()` |
| **Tensor Engine** | `ml.tensor(data)`, `.add()`, `.matmul()`, `.reshape()`, `.T`, `.softmax()`, `.relu()`, `.sigmoid()` |
| **Automatic Differentiation** | `ml.autograd.variable()`, `ml.autograd.gradient()`, `ml.autograd.tape()` (GradientTape) |
| **Model Architectures** | `ml.model.linear()`, `.relu()`, `.sigmoid()`, `.softmax()`, `.dropout()`, `.batch_norm()`, `.embedding()`, `.sequential()`, `.mlp()` |
| **Basic Distributed Training** | `ml.train.fit(model, dataset, n_workers=4)` — data-parallel multi-worker training |
| **Numerical Kernels** | `ml.kernel.gemm()`, `.conv2d()`, `.max_pool2d()`, `.normalize()`, `.layer_norm()`, `.fft()`, `.dot()`, `.outer()` |
| **GPU/TPU Infrastructure** | `ml.gpu.info()`, `.to_device()`, `.allocate()`, `.synchronize()`, `.memory_stats()`, `.empty_cache()` |
| **Optimizers** | `ml.optim.adam()`, `.sgd()`, `.rmsprop()` |
| **Loss Functions** | `ml.loss.mse()`, `.cross_entropy()`, `.binary_cross_entropy()`, `.mae()`, `.huber()` |
| **🌐 Frontier Distributed LLM** | `ml.distributed.Transformer()`, `.Cluster()`, `.train()` — full 5D frontier training |
=======
- `os`: system information, process control, notifications, clipboard access, and bounded command execution
- `fs`: file read/write/append/remove operations
- `http`: optional HTTP helpers when the dependency is installed
- `ai`: prompt, classification, and JSON extraction flows via local/cloud backends or offline fallback behavior
- `ml`: tensor primitives, dataset helpers, optimization and loss utilities, and optional CUDA/PyTorch execution paths
- `scheduler`: SQLite-backed scheduled work
- `agent`: memory, planning, permissions, bounded execution, and orchestration support

> Optional integrations depend on installed packages, hardware, drivers, credentials, and service availability. They are not automatically available just because the API exists.

## Project tools

- `Emerald_Studio.exe`: editor, runner, template builder, hardware display, and agent runtime panel
- `Sapphire_Compiler.exe`: script execution and AST/IR inspection tool
- `Sapphire_Setup_Wizard.exe`: installer for the runtime, docs, PATH configuration, `.sp` association, and shortcuts
>>>>>>> 732e4d1 (Update README and documentation bundle)

## Installation

<<<<<<< HEAD
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
>>>>>>> bf07d50 (docs: add ch14 Distributed LLM to tutor, regenerate all 5 PDFs, update README with frontier stats)

> Optional integrations depend on installed packages, hardware, drivers, credentials, and service availability. They are not automatically available just because the API exists.

## Project tools

<<<<<<< HEAD
- `Emerald_Studio.exe`: editor, runner, template builder, hardware display, and agent runtime panel
- `Sapphire_Compiler.exe`: script execution and AST/IR inspection tool
- `Sapphire_Setup_Wizard.exe`: installer for the runtime, docs, PATH configuration, `.sp` association, and shortcuts
=======
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
>>>>>>> bf07d50 (docs: add ch14 Distributed LLM to tutor, regenerate all 5 PDFs, update README with frontier stats)

## Installation

On Windows, run `Sapphire_Setup_Wizard.exe` and keep PATH and shortcuts enabled if desired. After installation, open a new terminal and run:

=======
On Windows, run `Sapphire_Setup_Wizard.exe` and keep PATH and shortcuts enabled if desired. After installation, open a new terminal and run:

>>>>>>> 732e4d1 (Update README and documentation bundle)
```text
sapphire info
sapphire run hello.sp
sapphire studio
```

For source execution from the repository:

<<<<<<< HEAD
<<<<<<< HEAD
```text
python sapphire_lang/src/cli.py run path/to/script.sp
python -m unittest sapphire_lang.tests.test_sapphire sapphire_lang.tests.test_industrial_readiness
=======
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
>>>>>>> bf07d50 (docs: add ch14 Distributed LLM to tutor, regenerate all 5 PDFs, update README with frontier stats)
=======
```text
python sapphire_lang/src/cli.py run path/to/script.sp
python -m unittest sapphire_lang.tests.test_sapphire sapphire_lang.tests.test_industrial_readiness
>>>>>>> 732e4d1 (Update README and documentation bundle)
```

## Included documentation bundle

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 732e4d1 (Update README and documentation bundle)
The project root includes the following manuals and guides:

- [Sapphire_Coding_and_Usage_Guide.pdf](Sapphire_Coding_and_Usage_Guide.pdf) — practical coding reference and usage guide
- [Building_Advanced_Autonomous_AI.pdf](Building_Advanced_Autonomous_AI.pdf) — advanced automation and autonomous AI patterns
- [Sapphire_Autonomy_and_Performance_Benchmarks.pdf](Sapphire_Autonomy_and_Performance_Benchmarks.pdf) — benchmark and autonomy analysis
- [Beginners_Guide_Your_First_Autonomous_AI.pdf](Beginners_Guide_Your_First_Autonomous_AI.pdf) — beginner-facing onboarding guide
- [Sapphire_Language_Specification_and_Automation_Manual.pdf](Sapphire_Language_Specification_and_Automation_Manual.pdf) — specification and automation reference
- [Sapphire_Capabilities_and_Transparency_Manual.pdf](Sapphire_Capabilities_and_Transparency_Manual.pdf) — current scope, transparency notes, and known limitations

Additional project documentation:

- [INSTALLATION_AND_USAGE_GUIDE.md](INSTALLATION_AND_USAGE_GUIDE.md)
- [INDUSTRIAL_READINESS.md](INDUSTRIAL_READINESS.md)

## Validation and limits

The repository includes validation around language execution, process and file helpers, concurrency, agent planning, failure handling, persistence, sandbox boundaries, CPU/ML behavior, and optional CUDA reporting.

A benchmark can be run with:

```text
python benchmarks/benchmark_runtime.py
<<<<<<< HEAD
```

One reference run on Python 3.12.10 completed 100 parse-and-interpret iterations of a 100-item loop with:

- result: 4950
- median: 0.21095 ms
- minimum: 0.2023 ms
- maximum: 0.7817 ms

Those numbers are machine-specific and are not a language-wide guarantee. This project does not currently include cross-language, cluster-scale, or large GPU-training validation.

## Roadmap and known limitations

The following are not presented as completed production features: native compiler backend, strong isolation guarantees, persistent vector embeddings, event-driven agent declarations, DAG scheduling, verified multi-node training, automatic cluster recovery, and broad security certification.

See [INDUSTRIAL_READINESS.md](INDUSTRIAL_READINESS.md) and [Sapphire_Capabilities_and_Transparency_Manual.pdf](Sapphire_Capabilities_and_Transparency_Manual.pdf) for the tested scope and known limitations.

## Quick start

```text
python -m pip install -r requirements.txt
python sapphire_lang/src/cli.py --help
```

Then run a sample script or launch the included studio tool:

```text
python sapphire_lang/src/cli.py run examples/01_basics.sp
```

If the Windows installer is used, the bundled `.sp` association and runtime tools are installed automatically.
=======
```sapphire
let w = ml.autograd.variable(ml.tensor([0.5, -0.3, 0.8]), "weights");
let x = ml.autograd.variable(ml.tensor([1.0, 2.0, 3.0]), "inputs");
let loss_var = ml.autograd.variable(ml.tensor([3.14]), "loss");
let grads = ml.autograd.gradient(loss_var, [w, x]);
print("Weight gradients: {grads[0]}");
=======
>>>>>>> 732e4d1 (Update README and documentation bundle)
```

One reference run on Python 3.12.10 completed 100 parse-and-interpret iterations of a 100-item loop with:

- result: 4950
- median: 0.21095 ms
- minimum: 0.2023 ms
- maximum: 0.7817 ms

Those numbers are machine-specific and are not a language-wide guarantee. This project does not currently include cross-language, cluster-scale, or large GPU-training validation.

## Roadmap and known limitations

The following are not presented as completed production features: native compiler backend, strong isolation guarantees, persistent vector embeddings, event-driven agent declarations, DAG scheduling, verified multi-node training, automatic cluster recovery, and broad security certification.

See [INDUSTRIAL_READINESS.md](INDUSTRIAL_READINESS.md) and [Sapphire_Capabilities_and_Transparency_Manual.pdf](Sapphire_Capabilities_and_Transparency_Manual.pdf) for the tested scope and known limitations.

## Quick start

```text
python -m pip install -r requirements.txt
python sapphire_lang/src/cli.py --help
```

Then run a sample script or launch the included studio tool:

```text
python sapphire_lang/src/cli.py run examples/01_basics.sp
```

<<<<<<< HEAD
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
>>>>>>> bf07d50 (docs: add ch14 Distributed LLM to tutor, regenerate all 5 PDFs, update README with frontier stats)
=======
If the Windows installer is used, the bundled `.sp` association and runtime tools are installed automatically.
>>>>>>> 732e4d1 (Update README and documentation bundle)
