# 💎 Sapphire Programming Language

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Platform: Windows | Linux | macOS](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-0078D6.svg)
![Release: v1.0.0](https://img.shields.io/badge/Release-v1.0.0-green.svg)
![ML: Tensor | Autograd | GPU](https://img.shields.io/badge/ML-Tensor%20%7C%20Autograd%20%7C%20GPU-8B5CF6.svg)

**Sapphire** is a cross-platform, autonomous-first programming language engineered for **PC Automation**, **Native AI Intelligence**, **Colorless Parallel Concurrency**, and a **full ML/Deep Learning stack** — all built into the language runtime with zero external dependencies.

Runs natively on **Windows**, **Linux (Kali, Ubuntu, Debian, Arch)**, and **macOS**.

---

## ✨ Key Features

### 🤖 Automation & AI
- **Native AI Primitives**: Built-in `ai.prompt("...")`, `ai.classify()`, `ai.extract_json()` directly in the syntax.
- **PC Automation**: System telemetry (`os.system_info()`), desktop notifications (`os.notify()`), clipboard access (`os.clip_write()`).
- **Colorless Concurrency**: Execute concurrent tasks with simple `parallel { ... }` blocks — no `async/await` coloring.
- **Persistent Schedulers**: Native background task scheduling via `scheduler.interval()`.

### 🔷 ML & Deep Learning Stack

| Capability | Sapphire API |
|---|---|
| **Massive Datasets** | `ml.dataset.from_csv()`, `.from_array()`, `.batch()`, `.shuffle()`, `.normalize()`, `.split()` |
| **Tensor Engine** | `ml.tensor(data)`, `.add()`, `.matmul()`, `.reshape()`, `.T`, `.softmax()`, `.relu()`, `.sigmoid()` |
| **Automatic Differentiation** | `ml.autograd.variable()`, `ml.autograd.gradient()`, `ml.autograd.tape()` (GradientTape) |
| **Model Architectures** | `ml.model.linear()`, `.relu()`, `.sigmoid()`, `.softmax()`, `.dropout()`, `.batch_norm()`, `.embedding()`, `.sequential()`, `.mlp()` |
| **Distributed Training** | `ml.train.fit(model, dataset, n_workers=4)` — data-parallel multi-worker training |
| **Numerical Kernels** | `ml.kernel.gemm()`, `.conv2d()`, `.max_pool2d()`, `.normalize()`, `.layer_norm()`, `.fft()`, `.dot()`, `.outer()` |
| **GPU/TPU Infrastructure** | `ml.gpu.info()`, `.to_device()`, `.allocate()`, `.synchronize()`, `.memory_stats()`, `.empty_cache()` |
| **Optimizers** | `ml.optim.adam()`, `.sgd()`, `.rmsprop()` |
| **Loss Functions** | `ml.loss.mse()`, `.cross_entropy()`, `.binary_cross_entropy()`, `.mae()`, `.huber()` |

### 🌐 Cross-Platform
Natively runs on Windows, Kali Linux, Ubuntu, Debian, Arch, and macOS.

---

## 🚀 Installation Guide

### 🪟 Windows Setup
Download **[Sapphire_Setup_Wizard.exe](https://github.com/impala19067-hub/Nexus-autonomous-language/releases)** from the Latest Release and double-click to install.

### 🐧 Linux (Kali, Ubuntu, Debian, Arch) & 🍎 macOS Setup

#### Method A: 1-Line Instant Installer (Recommended)
```bash
curl -sSL https://raw.githubusercontent.com/impala19067-hub/Nexus-autonomous-language/main/install.sh | bash
```

#### Method B: Native Kali / Debian Package (`.deb`)
```bash
sudo apt install ./nexus_1.0.0_all.deb
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

## 🔷 ML Code Examples

### 1. Tensor Operations

```sapphire
// Tensor arithmetic, matmul, reshape
let a = ml.tensor([[1, 2], [3, 4]]);
let b = ml.tensor([[5, 6], [7, 8]]);
let c = ml.matmul(a, b);
print("Matmul result: {c}");

// Activation functions
let x = ml.randn([8]);
let activated = x.relu();
let probs = ml.tensor([2.0, 1.0, 0.5]).softmax();
print("Softmax probs: {probs}");
```

### 2. Automatic Differentiation

```sapphire
// Compute gradients with GradientTape
let w = ml.autograd.variable(ml.tensor([0.5, -0.3, 0.8]), "weights");
let x = ml.autograd.variable(ml.tensor([1.0, 2.0, 3.0]), "inputs");

let loss_val = ml.tensor([3.14]);
let loss_var = ml.autograd.variable(loss_val, "loss");

let grads = ml.autograd.gradient(loss_var, [w, x]);
print("Weight gradients: {grads[0]}");
print("Input gradients:  {grads[1]}");
```

### 3. Dataset Loading & Preprocessing

```sapphire
// Synthetic dataset
let ds = ml.dataset.random(1000, 16, 3);  // 1000 samples, 16 features, 3 classes
let ds_norm = ds.normalize();
let split = ds_norm.split(0.8);           // 80/20 train/val

let train = split["train"];
let val   = split["val"];
print("Train: {train.size} samples, Val: {val.size} samples");

// From CSV file
let csv_ds = ml.dataset.from_csv("./data/iris.csv");
let batches = csv_ds.batch(32);
print("Batches: {batches.length}");
```

### 4. Model Architecture

```sapphire
// Build a neural network
let model = ml.model.sequential([
    ml.model.linear(16, 64),
    ml.model.relu(),
    ml.model.dropout(0.3),
    ml.model.linear(64, 32),
    ml.model.batch_norm(32),
    ml.model.relu(),
    ml.model.linear(32, 3),
    ml.model.softmax()
]);

print(model.summary());

// Quick MLP shorthand
let mlp = ml.model.mlp([16, 128, 64, 3], "relu");
```

### 5. Distributed Training

```sapphire
// Train across multiple workers
let ds = ml.dataset.random(2000, 16, 3);
let model = ml.model.mlp([16, 64, 32, 3], "relu");
let optimizer = ml.optim.adam(0.001);
let loss_fn = ml.loss.cross_entropy;

let result = ml.train.fit(
    model,
    ds,
    loss_fn,
    optimizer,
    epochs=20,
    batch_size=64,
    n_workers=4        // Distributed across 4 parallel workers
);

print("Final loss: {result.final_loss}");

// Evaluate
let metrics = ml.train.evaluate(model, ds.split(0.8)["val"]);
print("Validation accuracy: {metrics.accuracy}");
```

### 6. Numerical Kernels

```sapphire
// GEMM (General Matrix Multiply)
let A = ml.rand([4, 8]);
let B = ml.rand([8, 4]);
let C = ml.kernel.gemm(A, B, alpha=1.0);

// 2D Convolution
let image  = ml.rand([28, 28]);
let kernel = ml.rand([3, 3]);
let feature_map = ml.kernel.conv2d(image, kernel, stride=1, padding=1);
let pooled = ml.kernel.max_pool2d(feature_map, 2, 2);
print("Feature map shape: {feature_map.shape}");
print("Pooled shape: {pooled.shape}");

// Layer normalization
let h = ml.randn([64]);
let h_norm = ml.kernel.layer_norm(h);

// Fourier transform (signal processing)
let signal = ml.arange(0, 64);
let spectrum = ml.kernel.fft(signal);
print("FFT magnitude shape: {spectrum.shape}");
```

### 7. GPU/TPU Infrastructure

```sapphire
// Query available devices
let devices = ml.gpu.info();
print("Devices: {devices}");

// Allocate and move tensors to device
let t = ml.randn([512, 512]);
let t_gpu = ml.gpu.to_device(t, 0);

// Sync and memory management
ml.gpu.synchronize(0);
let stats = ml.gpu.memory_stats();
print("GPU Memory: {stats}");

ml.gpu.empty_cache();
print("Cache cleared");
```

---

## 🤖 Autonomous AI Bot Example (5 Lines)

```sapphire
fn main() {
    let stats = os.system_info();
    let opinion = ai.prompt("System RAM is at {stats.ram_percent}%. Is this healthy?");
    print("🤖 AI Evaluation: {opinion}");
    os.notify("Sapphire Bot Alert", opinion);
}
main();
```

---

## 📚 Documentation & Manuals

- [📘 Sapphire Coding & Usage Guide (PDF)](docs/Nexus_Coding_and_Usage_Guide.pdf)
- [🤖 Building Advanced Autonomous AI (PDF)](docs/Building_Advanced_Autonomous_AI.pdf)
- [📊 Autonomy & Performance Benchmarks (PDF)](docs/Nexus_Autonomy_and_Performance_Benchmarks.pdf)
- [🎓 Beginner's Guide: Your First Autonomous AI (PDF)](docs/Beginners_Guide_Your_First_Autonomous_AI.pdf)

---

## 📄 License
Released under the MIT License.
