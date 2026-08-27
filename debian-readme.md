# Sapphire Programming Language 1.0.5 - Debian and Kali Linux

This distribution supports source installation on Debian, Kali, Ubuntu, Linux Mint, and related Linux systems. It provides the Python interpreter, Sapphire standard library, command-line launcher, and source tools.

## Install From This Folder

### Option 1: Debian package

Build or use the included package, then install it with:

```bash
sudo apt install ./sapphire_1.0.5_all.deb
```

The package installs the `sapphire` launcher and source runtime under `/usr/share/sapphire_lang`.

### Option 2: Source installer

```bash
chmod +x install.sh
./install.sh
```

The installer copies the runtime to `~/.sapphire_lang` or `/usr/local/bin` when writable, then creates the `sapphire` command. Open a new shell or source the shell configuration after installation.

### Option 3: Remote installer

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

Sapphire provides local tensors, datasets, model helpers, autodiff, losses, optimizers, and a basic training loop. The optional `ml.torch_train` backend uses a separately installed PyTorch package for real CPU or CUDA training, validation loss, training history, and checkpoints.

Install PyTorch separately for that backend. CUDA also requires compatible NVIDIA hardware and drivers. NumPy, PyTorch, AI services, and other integrations are optional and are not bundled assumptions.

The distributed API generates topology, memory, communication, and launcher plans. It does not launch or validate a multi-node cluster by itself.

## GUI Availability

The Windows distribution includes Emerald Developer Studio as a packaged GUI. This Debian distribution is source/terminal focused; use the Sapphire CLI and Python source tools unless you provide and configure your own GUI environment.
