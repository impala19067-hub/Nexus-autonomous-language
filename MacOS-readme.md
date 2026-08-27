# Sapphire Programming Language 1.0.5 - macOS

This distribution provides the Python source runtime and terminal installer for Intel and Apple Silicon Macs. It does not include a native macOS GUI setup wizard executable.

## Install

From this folder, open Terminal and run:

```bash
chmod +x install.sh
./install.sh
```

The installer copies the runtime to `~/.sapphire_lang` and creates a `sapphire` launcher in `/usr/local/bin` when writable, or in `~/.local/bin` otherwise. Start a new shell after installation so the PATH change is available.

You can also use the remote installer:

```bash
curl -sSL https://raw.githubusercontent.com/impala19067-hub/Sapphire-autonomous-language/main/install.sh | bash
```

## Verify

```bash
sapphire info
sapphire run examples/01_basics.sp
sapphire repl
sapphire eval 'print("Sapphire is running");'
```

## Current ML Scope

The source runtime provides tensors, datasets, basic model helpers, autodiff, losses, optimizers, and local training utilities. The optional `ml.torch_train` backend uses a separately installed PyTorch package for real CPU or CUDA training, validation, history, and checkpoints.

PyTorch is not bundled. CUDA requires compatible NVIDIA hardware, drivers, and a CUDA-enabled PyTorch installation. AI service integrations also require their own local service or credentials.

The distributed API produces planning and launcher artifacts. It does not run or verify multi-node training by itself. Emerald Developer Studio is currently packaged for Windows; macOS users should use the terminal and source tools in this distribution.
