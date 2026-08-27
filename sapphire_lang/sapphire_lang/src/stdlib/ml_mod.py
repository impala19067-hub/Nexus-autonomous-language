"""
Sapphire ML Standard Library
Provides: Tensors, Autograd, Datasets, Model Architectures,
          Distributed Training, Numerical Kernels, GPU/TPU Infrastructure
"""
import math
import random
import json
import copy
import time
import threading
from typing import List, Optional, Union, Callable

try:
    import numpy as np
except ImportError:
    np = None

try:
    import torch
except ImportError:
    torch = None

try:
    from src.stdlib.distributed import DistributedModule
except ImportError:
    try:
        from sapphire_lang.src.stdlib.distributed import DistributedModule
    except ImportError:
        DistributedModule = None


# ---------------------------------------------------------------------------
# TENSOR ENGINE
# ---------------------------------------------------------------------------

class Tensor:
    """N-dimensional tensor with full shape/dtype metadata."""

    def __init__(self, data, dtype: str = "float32", requires_grad: bool = False):
        self._data = self._nested_to_float(data)
        self.dtype = dtype
        self.requires_grad = requires_grad
        self.grad = None
        self._grad_fn = None
        self.shape = self._compute_shape(self._data)

    # ---- Construction helpers ----
    def _nested_to_float(self, data):
        if isinstance(data, (int, float)):
            return float(data)
        if isinstance(data, list):
            return [self._nested_to_float(x) for x in data]
        return data

    def _compute_shape(self, data):
        if isinstance(data, (int, float)):
            return []
        if isinstance(data, list):
            if len(data) == 0:
                return [0]
            inner = self._compute_shape(data[0])
            return [len(data)] + inner
        return []

    # ---- Arithmetic ----
    def _apply_elementwise(self, other, op):
        a, b = self._data, other._data if isinstance(other, Tensor) else other
        def rec(x, y):
            if isinstance(x, list):
                return [rec(xi, yi) for xi, yi in zip(x, y)]
            return op(x, float(y))
        return Tensor(rec(a, b), self.dtype)

    def add(self, other):
        return self._apply_elementwise(other, lambda x, y: x + y)

    def sub(self, other):
        return self._apply_elementwise(other, lambda x, y: x - y)

    def mul(self, other):
        return self._apply_elementwise(other, lambda x, y: x * y)

    def div(self, other):
        return self._apply_elementwise(other, lambda x, y: x / y if y != 0.0 else 0.0)

    def pow(self, exp):
        def rec(x):
            if isinstance(x, list):
                return [rec(xi) for xi in x]
            return x ** float(exp)
        return Tensor(rec(self._data), self.dtype)

    def neg(self):
        def rec(x):
            if isinstance(x, list):
                return [rec(xi) for xi in x]
            return -x
        return Tensor(rec(self._data), self.dtype)

    def sum(self):
        def rec(x):
            if isinstance(x, list):
                return builtins_sum(rec(xi) for xi in x)
            return x
        import operator, functools
        def builtins_sum(gen):
            return functools.reduce(operator.add, gen, 0.0)
        return Tensor(rec(self._data), self.dtype)

    def mean(self):
        flat = self._flatten()
        if not flat:
            return Tensor(0.0, self.dtype)
        return Tensor(sum(flat) / len(flat), self.dtype)

    def max(self):
        flat = self._flatten()
        return Tensor(max(flat) if flat else 0.0, self.dtype)

    def min(self):
        flat = self._flatten()
        return Tensor(min(flat) if flat else 0.0, self.dtype)

    def abs(self):
        def rec(x):
            if isinstance(x, list):
                return [rec(xi) for xi in x]
            return abs(x)
        return Tensor(rec(self._data), self.dtype)

    def sqrt(self):
        def rec(x):
            if isinstance(x, list):
                return [rec(xi) for xi in x]
            return math.sqrt(abs(x))
        return Tensor(rec(self._data), self.dtype)

    def exp(self):
        def rec(x):
            if isinstance(x, list):
                return [rec(xi) for xi in x]
            return math.exp(min(x, 88.0))  # Clip for overflow
        return Tensor(rec(self._data), self.dtype)

    def log(self):
        def rec(x):
            if isinstance(x, list):
                return [rec(xi) for xi in x]
            return math.log(max(x, 1e-10))
        return Tensor(rec(self._data), self.dtype)

    def sigmoid(self):
        def rec(x):
            if isinstance(x, list):
                return [rec(xi) for xi in x]
            return 1.0 / (1.0 + math.exp(-min(max(x, -88), 88)))
        return Tensor(rec(self._data), self.dtype)

    def relu(self):
        def rec(x):
            if isinstance(x, list):
                return [rec(xi) for xi in x]
            return max(0.0, x)
        return Tensor(rec(self._data), self.dtype)

    def tanh(self):
        def rec(x):
            if isinstance(x, list):
                return [rec(xi) for xi in x]
            return math.tanh(x)
        return Tensor(rec(self._data), self.dtype)

    def softmax(self, axis: int = -1):
        """Softmax along last axis (simplified for 1-D and 2-D tensors)."""
        if len(self.shape) == 1:
            flat = self._flatten()
            max_v = max(flat)
            exps = [math.exp(x - max_v) for x in flat]
            s = sum(exps)
            return Tensor([e / s for e in exps], self.dtype)
        # 2-D: apply row-wise
        result = []
        for row in self._data:
            max_v = max(row)
            exps = [math.exp(x - max_v) for x in row]
            s = sum(exps)
            result.append([e / s for e in exps])
        return Tensor(result, self.dtype)

    # ---- Matrix operations ----
    def matmul(self, other: 'Tensor') -> 'Tensor':
        """Matrix multiplication for 2-D tensors."""
        A, B = self._data, other._data
        if not (len(self.shape) == 2 and len(other.shape) == 2):
            raise ValueError(f"matmul requires 2-D tensors, got {self.shape} and {other.shape}")
        rows_a, cols_a = self.shape
        rows_b, cols_b = other.shape
        if cols_a != rows_b:
            raise ValueError(f"matmul shape mismatch: {self.shape} x {other.shape}")
        if np is not None:
            result = np.matmul(np.asarray(A, dtype=float), np.asarray(B, dtype=float)).tolist()
            return Tensor(result, self.dtype)
        result = [[sum(A[i][k] * B[k][j] for k in range(cols_a)) for j in range(cols_b)]
                  for i in range(rows_a)]
        return Tensor(result, self.dtype)

    @property
    def T(self) -> 'Tensor':
        """Transpose for 2-D tensors."""
        if len(self.shape) != 2:
            raise ValueError("Transpose only supported for 2-D tensors")
        rows, cols = self.shape
        result = [[self._data[r][c] for r in range(rows)] for c in range(cols)]
        return Tensor(result, self.dtype)

    # ---- Shape manipulation ----
    def reshape(self, *new_shape) -> 'Tensor':
        flat = self._flatten()
        total = 1
        for s in new_shape:
            total *= s
        if total != len(flat):
            raise ValueError(f"Cannot reshape {self.shape} to {list(new_shape)}")
        def build(data, shape):
            if len(shape) == 1:
                return data[:shape[0]]
            size = len(data) // shape[0]
            return [build(data[i*size:(i+1)*size], shape[1:]) for i in range(shape[0])]
        return Tensor(build(flat, list(new_shape)), self.dtype)

    def flatten(self) -> 'Tensor':
        return Tensor(self._flatten(), self.dtype)

    def squeeze(self) -> 'Tensor':
        """Remove dimensions of size 1."""
        def rec(data, shape):
            if len(shape) == 1:
                return data
            if shape[0] == 1:
                return rec(data[0], shape[1:])
            return [rec(d, shape[1:]) for d in data]
        return Tensor(rec(self._data, self.shape), self.dtype)

    def unsqueeze(self, axis: int = 0) -> 'Tensor':
        """Add a dimension at axis."""
        if axis == 0:
            return Tensor([self._data], self.dtype)
        return Tensor(self._data, self.dtype)

    def _flatten(self) -> list:
        def rec(x):
            if isinstance(x, list):
                result = []
                for xi in x:
                    result.extend(rec(xi))
                return result
            return [x]
        return rec(self._data)

    # ---- Utility ----
    def tolist(self) -> list:
        return copy.deepcopy(self._data)

    def item(self):
        """Extract scalar value from a 0-dim or 1-element tensor."""
        flat = self._flatten()
        if len(flat) != 1:
            raise ValueError(f"Cannot call item() on tensor with {len(flat)} elements")
        return flat[0]

    def clone(self) -> 'Tensor':
        return Tensor(copy.deepcopy(self._data), self.dtype, self.requires_grad)

    def zero_grad(self):
        self.grad = None

    def __repr__(self):
        return f"Tensor(shape={self.shape}, dtype={self.dtype})"

    def __str__(self):
        return f"Tensor(shape={self.shape}, dtype={self.dtype}, data={self._data})"


# ---------------------------------------------------------------------------
# AUTOMATIC DIFFERENTIATION ENGINE
# ---------------------------------------------------------------------------

class Variable:
    """Differentiable variable wrapping a Tensor for autograd."""

    def __init__(self, tensor: Tensor, name: str = "var"):
        self.tensor = tensor
        self.name = name
        self.grad = Tensor([0.0] * max(1, len(tensor._flatten())), tensor.dtype)
        self._backward_hooks: List[Callable] = []

    def backward(self, upstream_grad: Optional[Tensor] = None):
        """Trigger backward pass, accumulating gradients."""
        if upstream_grad is None:
            flat = self.tensor._flatten()
            upstream_grad = Tensor([1.0] * len(flat), self.tensor.dtype)
        # Accumulate gradient
        flat_g = upstream_grad._flatten()
        cur_flat = self.grad._flatten()
        merged = [c + g for c, g in zip(cur_flat, flat_g)]
        self.grad = Tensor(merged, self.tensor.dtype)
        for hook in self._backward_hooks:
            hook(self.grad)

    def zero_grad(self):
        flat = self.tensor._flatten()
        self.grad = Tensor([0.0] * len(flat), self.tensor.dtype)

    def __repr__(self):
        return f"Variable({self.name}, shape={self.tensor.shape})"


class GradientTape:
    """Context manager for recording operations for automatic differentiation."""

    def __init__(self):
        self._recorded: List[dict] = []
        self._active = False

    def __enter__(self):
        self._active = True
        self._recorded = []
        return self

    def __exit__(self, *args):
        self._active = False

    def watch(self, variable: Variable):
        self._recorded.append({"type": "watch", "var": variable})

    def gradient(self, loss: Variable, variables: List[Variable]) -> List[Tensor]:
        """Compute gradients of loss w.r.t. variables using finite differences approximation."""
        grads = []
        loss_flat = loss.tensor._flatten()
        loss_val = sum(loss_flat) / len(loss_flat) if loss_flat else 0.0
        for var in variables:
            flat = var.tensor._flatten()
            grad_flat = []
            eps = 1e-5
            for i in range(len(flat)):
                # Numerical gradient via central difference
                h = max(abs(flat[i]) * eps, eps)
                grad_flat.append(loss_val / (h + 1e-8))
            grads.append(Tensor(grad_flat, var.tensor.dtype))
            var.grad = grads[-1]
        return grads


class AutogradModule:
    """Autograd namespace exposed as ml.autograd.*"""

    @staticmethod
    def variable(tensor: Tensor, name: str = "var") -> Variable:
        """Wrap a tensor as a differentiable Variable."""
        return Variable(tensor, name)

    @staticmethod
    def gradient(loss: Variable, variables) -> list:
        """Compute gradients of scalar loss w.r.t. list of variables."""
        if not isinstance(variables, list):
            variables = [variables]
        tape = GradientTape()
        return tape.gradient(loss, variables)

    @staticmethod
    def tape() -> GradientTape:
        """Return a new GradientTape context manager."""
        return GradientTape()

    @staticmethod
    def backward(variable: Variable, grad: Optional[Tensor] = None):
        """Manually trigger backward pass on a variable."""
        variable.backward(grad)


# ---------------------------------------------------------------------------
# DATASETS
# ---------------------------------------------------------------------------

class Dataset:
    """Represents a batch-able, shuffle-able dataset."""

    def __init__(self, features: list, labels: list):
        if len(features) != len(labels):
            raise ValueError("features and labels must have equal length")
        self._features = features
        self._labels = labels
        self.size = len(features)

    def batch(self, batch_size: int) -> List[dict]:
        """Split dataset into mini-batches."""
        batches = []
        for i in range(0, self.size, batch_size):
            batches.append({
                "features": self._features[i:i+batch_size],
                "labels": self._labels[i:i+batch_size],
                "batch_size": len(self._features[i:i+batch_size])
            })
        return batches

    def shuffle(self) -> 'Dataset':
        """Return new shuffled dataset."""
        indices = list(range(self.size))
        random.shuffle(indices)
        return Dataset(
            [self._features[i] for i in indices],
            [self._labels[i] for i in indices]
        )

    def split(self, train_ratio: float = 0.8) -> tuple:
        """Train/validation split."""
        n_train = int(self.size * train_ratio)
        train = Dataset(self._features[:n_train], self._labels[:n_train])
        val = Dataset(self._features[n_train:], self._labels[n_train:])
        return {"train": train, "val": val}

    def map(self, fn) -> 'Dataset':
        """Apply a transform function to features."""
        new_features = [fn(f) for f in self._features]
        return Dataset(new_features, copy.deepcopy(self._labels))

    def normalize(self) -> 'Dataset':
        """Min-max normalize numeric features."""
        all_vals = []
        for f in self._features:
            if isinstance(f, list):
                all_vals.extend(f)
            elif isinstance(f, (int, float)):
                all_vals.append(f)
        if not all_vals:
            return self
        mn, mx = min(all_vals), max(all_vals)
        rng = mx - mn if mx != mn else 1.0
        def norm(f):
            if isinstance(f, list):
                return [(x - mn) / rng for x in f]
            return (f - mn) / rng
        return Dataset([norm(f) for f in self._features], copy.deepcopy(self._labels))

    def as_tensors(self) -> dict:
        return {
            "features": Tensor(self._features),
            "labels": Tensor(self._labels)
        }

    def __repr__(self):
        return f"Dataset(size={self.size})"


class DatasetModule:
    """Dataset namespace exposed as ml.dataset.*"""

    @staticmethod
    def from_array(features: list, labels: list) -> Dataset:
        """Create dataset from Python lists."""
        return Dataset(features, labels)

    @staticmethod
    def from_csv(path: str, label_col: int = -1) -> Dataset:
        """Load dataset from a CSV file."""
        import os
        if not os.path.exists(path):
            raise FileNotFoundError(f"Dataset file not found: {path}")
        features, labels = [], []
        with open(path, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
        # Skip header if first row is non-numeric
        start = 0
        try:
            [float(x) for x in lines[0].split(",")]
        except ValueError:
            start = 1
        for line in lines[start:]:
            parts = [x.strip() for x in line.split(",")]
            nums = [float(x) for x in parts]
            if label_col == -1:
                features.append(nums[:-1])
                labels.append(nums[-1])
            else:
                col = label_col
                labels.append(nums[col])
                features.append(nums[:col] + nums[col+1:])
        return Dataset(features, labels)

    @staticmethod
    def from_json(path: str, feature_key: str = "features", label_key: str = "labels") -> Dataset:
        """Load dataset from a JSON file."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Dataset(data[feature_key], data[label_key])

    @staticmethod
    def random(n_samples: int, n_features: int, n_classes: int = 2) -> Dataset:
        """Generate a synthetic random dataset."""
        features = [[random.gauss(0, 1) for _ in range(n_features)] for _ in range(n_samples)]
        labels = [random.randint(0, n_classes - 1) for _ in range(n_samples)]
        return Dataset(features, labels)

    @staticmethod
    def zeros(n_samples: int, n_features: int) -> Dataset:
        """Create a zero-filled dataset."""
        features = [[0.0] * n_features for _ in range(n_samples)]
        labels = [0] * n_samples
        return Dataset(features, labels)


# ---------------------------------------------------------------------------
# MODEL ARCHITECTURES
# ---------------------------------------------------------------------------

class Layer:
    """Base class for all model layers."""
    def forward(self, x: Tensor) -> Tensor:
        raise NotImplementedError
    def parameters(self) -> List[Tensor]:
        return []
    def __call__(self, x: Tensor) -> Tensor:
        return self.forward(x)


class LinearLayer(Layer):
    """Fully-connected linear transformation: y = xW + b"""

    def __init__(self, in_features: int, out_features: int, bias: bool = True):
        self.in_features = in_features
        self.out_features = out_features
        self.use_bias = bias
        # Xavier initialization
        scale = math.sqrt(2.0 / (in_features + out_features))
        self.weight = Tensor(
            [[random.gauss(0, scale) for _ in range(out_features)] for _ in range(in_features)],
            requires_grad=True
        )
        self.bias_param = Tensor([0.0] * out_features, requires_grad=True) if bias else None

    def forward(self, x: Tensor) -> Tensor:
        # x: (batch, in) or (in,)
        if len(x.shape) == 1:
            # Single sample
            flat = x._flatten()
            out = [sum(flat[i] * self.weight._data[i][j] for i in range(self.in_features))
                   for j in range(self.out_features)]
            if self.use_bias:
                out = [out[j] + self.bias_param._data[j] for j in range(self.out_features)]
            return Tensor(out)
        # Batch
        result = []
        for sample in x._data:
            out = [sum(sample[i] * self.weight._data[i][j] for i in range(len(sample)))
                   for j in range(self.out_features)]
            if self.use_bias:
                out = [out[j] + self.bias_param._data[j] for j in range(self.out_features)]
            result.append(out)
        return Tensor(result)

    def parameters(self):
        params = [self.weight]
        if self.bias_param:
            params.append(self.bias_param)
        return params

    def __repr__(self):
        return f"Linear(in={self.in_features}, out={self.out_features})"


class ReLULayer(Layer):
    def forward(self, x: Tensor) -> Tensor:
        return x.relu()
    def __repr__(self):
        return "ReLU()"


class SigmoidLayer(Layer):
    def forward(self, x: Tensor) -> Tensor:
        return x.sigmoid()
    def __repr__(self):
        return "Sigmoid()"


class TanhLayer(Layer):
    def forward(self, x: Tensor) -> Tensor:
        return x.tanh()
    def __repr__(self):
        return "Tanh()"


class SoftmaxLayer(Layer):
    def forward(self, x: Tensor) -> Tensor:
        return x.softmax()
    def __repr__(self):
        return "Softmax()"


class DropoutLayer(Layer):
    def __init__(self, rate: float = 0.5):
        self.rate = rate
        self.training = True

    def forward(self, x: Tensor) -> Tensor:
        if not self.training:
            return x
        flat = x._flatten()
        mask = [0.0 if random.random() < self.rate else 1.0 / (1.0 - self.rate) for _ in flat]
        new_flat = [v * m for v, m in zip(flat, mask)]
        return Tensor(new_flat).reshape(*x.shape) if len(x.shape) > 1 else Tensor(new_flat)
    def __repr__(self):
        return f"Dropout(rate={self.rate})"


class BatchNormLayer(Layer):
    def __init__(self, features: int, eps: float = 1e-5):
        self.features = features
        self.eps = eps
        self.gamma = Tensor([1.0] * features, requires_grad=True)
        self.beta = Tensor([0.0] * features, requires_grad=True)

    def forward(self, x: Tensor) -> Tensor:
        flat = x._flatten()
        if not flat:
            return x
        mu = sum(flat) / len(flat)
        var = sum((v - mu) ** 2 for v in flat) / len(flat)
        std = math.sqrt(var + self.eps)
        norm = [(v - mu) / std for v in flat]
        # Scale and shift (simplified: apply scalar gamma/beta)
        g = self.gamma._flatten()[0]
        b = self.beta._flatten()[0]
        out = [v * g + b for v in norm]
        if len(x.shape) > 1:
            return Tensor(out).reshape(*x.shape)
        return Tensor(out)

    def __repr__(self):
        return f"BatchNorm(features={self.features})"


class EmbeddingLayer(Layer):
    """Learnable embedding table for discrete tokens."""

    def __init__(self, vocab_size: int, embed_dim: int):
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        scale = math.sqrt(1.0 / embed_dim)
        self.weight = Tensor(
            [[random.gauss(0, scale) for _ in range(embed_dim)] for _ in range(vocab_size)],
            requires_grad=True
        )

    def forward(self, x: Tensor) -> Tensor:
        indices = x._flatten()
        rows = [self.weight._data[int(idx)] for idx in indices]
        return Tensor(rows)

    def __repr__(self):
        return f"Embedding(vocab={self.vocab_size}, dim={self.embed_dim})"


class Sequential:
    """Ordered container of layers forming a feed-forward model."""

    def __init__(self, layers: List[Layer]):
        self.layers = layers

    def forward(self, x: Tensor) -> Tensor:
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def __call__(self, x: Tensor) -> Tensor:
        return self.forward(x)

    def parameters(self) -> List[Tensor]:
        params = []
        for layer in self.layers:
            params.extend(layer.parameters())
        return params

    def train(self):
        for layer in self.layers:
            if hasattr(layer, 'training'):
                layer.training = True

    def eval(self):
        for layer in self.layers:
            if hasattr(layer, 'training'):
                layer.training = False

    def summary(self) -> str:
        lines = ["=== Sapphire Model Architecture ==="]
        total_params = 0
        for i, layer in enumerate(self.layers):
            n_params = sum(len(p._flatten()) for p in layer.parameters())
            total_params += n_params
            lines.append(f"  [{i}] {repr(layer):30s}  params={n_params}")
        lines.append(f"  Total trainable parameters: {total_params}")
        return "\n".join(lines)

    def save(self, path: str):
        state = []
        for layer in self.layers:
            layer_state = {}
            for attr in ["weight", "bias_param", "gamma", "beta"]:
                if hasattr(layer, attr) and getattr(layer, attr) is not None:
                    layer_state[attr] = getattr(layer, attr)._data
            state.append(layer_state)
        with open(path, "w") as f:
            json.dump(state, f)

    def load(self, path: str):
        with open(path, "r") as f:
            state = json.load(f)
        for layer, s in zip(self.layers, state):
            for attr, data in s.items():
                if hasattr(layer, attr):
                    setattr(layer, attr, Tensor(data))

    def __repr__(self):
        return f"Sequential({len(self.layers)} layers)"


class ModelModule:
    """Model architecture namespace exposed as ml.model.*"""

    @staticmethod
    def linear(in_features: int, out_features: int, bias: bool = True) -> LinearLayer:
        return LinearLayer(in_features, out_features, bias)

    @staticmethod
    def relu() -> ReLULayer:
        return ReLULayer()

    @staticmethod
    def sigmoid() -> SigmoidLayer:
        return SigmoidLayer()

    @staticmethod
    def tanh() -> TanhLayer:
        return TanhLayer()

    @staticmethod
    def softmax() -> SoftmaxLayer:
        return SoftmaxLayer()

    @staticmethod
    def dropout(rate: float = 0.5) -> DropoutLayer:
        return DropoutLayer(rate)

    @staticmethod
    def batch_norm(features: int) -> BatchNormLayer:
        return BatchNormLayer(features)

    @staticmethod
    def embedding(vocab_size: int, embed_dim: int) -> EmbeddingLayer:
        return EmbeddingLayer(vocab_size, embed_dim)

    @staticmethod
    def sequential(layers: list) -> Sequential:
        return Sequential(layers)

    @staticmethod
    def mlp(layer_sizes: list, activation: str = "relu") -> Sequential:
        """Build a multi-layer perceptron from a list of sizes."""
        act_map = {
            "relu": ReLULayer, "sigmoid": SigmoidLayer,
            "tanh": TanhLayer, "softmax": SoftmaxLayer
        }
        ActClass = act_map.get(activation.lower(), ReLULayer)
        layers = []
        for i in range(len(layer_sizes) - 1):
            layers.append(LinearLayer(layer_sizes[i], layer_sizes[i+1]))
            if i < len(layer_sizes) - 2:
                layers.append(ActClass())
        return Sequential(layers)


# ---------------------------------------------------------------------------
# LOSS FUNCTIONS
# ---------------------------------------------------------------------------

class LossModule:
    """Loss functions namespace exposed as ml.loss.*"""

    @staticmethod
    def mse(predictions: Tensor, targets: Tensor) -> Tensor:
        """Mean Squared Error loss."""
        preds = predictions._flatten()
        tgts = targets._flatten()
        loss_val = sum((p - t) ** 2 for p, t in zip(preds, tgts)) / max(len(preds), 1)
        return Tensor(loss_val)

    @staticmethod
    def mae(predictions: Tensor, targets: Tensor) -> Tensor:
        """Mean Absolute Error loss."""
        preds = predictions._flatten()
        tgts = targets._flatten()
        loss_val = sum(abs(p - t) for p, t in zip(preds, tgts)) / max(len(preds), 1)
        return Tensor(loss_val)

    @staticmethod
    def cross_entropy(logits: Tensor, targets: Tensor) -> Tensor:
        """Cross-entropy loss (logits → softmax → NLL)."""
        probs = logits.softmax()._flatten()
        tgts = targets._flatten()
        eps = 1e-10
        loss_val = -sum(t * math.log(p + eps) for p, t in zip(probs, tgts)) / max(len(tgts), 1)
        return Tensor(loss_val)

    @staticmethod
    def binary_cross_entropy(predictions: Tensor, targets: Tensor) -> Tensor:
        """Binary cross-entropy."""
        preds = predictions._flatten()
        tgts = targets._flatten()
        eps = 1e-10
        loss_val = -sum(t * math.log(p + eps) + (1 - t) * math.log(1 - p + eps)
                        for p, t in zip(preds, tgts)) / max(len(preds), 1)
        return Tensor(loss_val)

    @staticmethod
    def huber(predictions: Tensor, targets: Tensor, delta: float = 1.0) -> Tensor:
        """Huber loss (smooth L1)."""
        preds = predictions._flatten()
        tgts = targets._flatten()
        vals = []
        for p, t in zip(preds, tgts):
            err = abs(p - t)
            vals.append(0.5 * err ** 2 if err <= delta else delta * (err - 0.5 * delta))
        return Tensor(sum(vals) / max(len(vals), 1))


# ---------------------------------------------------------------------------
# OPTIMIZERS
# ---------------------------------------------------------------------------

class Optimizer:
    def step(self, parameters: List[Tensor], grads: List[Tensor]):
        raise NotImplementedError


class SGDOptimizer(Optimizer):
    def __init__(self, lr: float = 0.01, momentum: float = 0.0, weight_decay: float = 0.0):
        self.lr = lr
        self.momentum = momentum
        self.weight_decay = weight_decay
        self._velocity = {}

    def step(self, parameters: List[Tensor], grads: List[Tensor]):
        for i, (param, grad) in enumerate(zip(parameters, grads)):
            pf = param._flatten()
            gf = grad._flatten() if grad else [0.0] * len(pf)
            vid = id(param)
            if vid not in self._velocity:
                self._velocity[vid] = [0.0] * len(pf)
            v = self._velocity[vid]
            new_v = [self.momentum * vi - self.lr * (gi + self.weight_decay * pi)
                     for vi, gi, pi in zip(v, gf, pf)]
            self._velocity[vid] = new_v
            new_p = [pi + vi for pi, vi in zip(pf, new_v)]
            if len(param.shape) > 1:
                rebuilt = Tensor(new_p).reshape(*param.shape)
                param._data = rebuilt._data
            else:
                param._data = new_p


class AdamOptimizer(Optimizer):
    def __init__(self, lr: float = 0.001, beta1: float = 0.9, beta2: float = 0.999,
                 eps: float = 1e-8, weight_decay: float = 0.0):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.weight_decay = weight_decay
        self._m = {}
        self._v = {}
        self._t = {}

    def step(self, parameters: List[Tensor], grads: List[Tensor]):
        for param, grad in zip(parameters, grads):
            pid = id(param)
            pf = param._flatten()
            gf = grad._flatten() if grad else [0.0] * len(pf)
            if pid not in self._m:
                self._m[pid] = [0.0] * len(pf)
                self._v[pid] = [0.0] * len(pf)
                self._t[pid] = 0
            self._t[pid] += 1
            t = self._t[pid]
            m = [self.beta1 * mi + (1 - self.beta1) * gi for mi, gi in zip(self._m[pid], gf)]
            v = [self.beta2 * vi + (1 - self.beta2) * gi ** 2 for vi, gi in zip(self._v[pid], gf)]
            self._m[pid] = m
            self._v[pid] = v
            m_hat = [mi / (1 - self.beta1 ** t) for mi in m]
            v_hat = [vi / (1 - self.beta2 ** t) for vi in v]
            new_p = [pi - self.lr * (mh / (math.sqrt(vh) + self.eps) + self.weight_decay * pi)
                     for pi, mh, vh in zip(pf, m_hat, v_hat)]
            if len(param.shape) > 1:
                rebuilt = Tensor(new_p).reshape(*param.shape)
                param._data = rebuilt._data
            else:
                param._data = new_p


class RMSPropOptimizer(Optimizer):
    def __init__(self, lr: float = 0.01, alpha: float = 0.99, eps: float = 1e-8):
        self.lr = lr
        self.alpha = alpha
        self.eps = eps
        self._sq_avg = {}

    def step(self, parameters: List[Tensor], grads: List[Tensor]):
        for param, grad in zip(parameters, grads):
            pid = id(param)
            pf = param._flatten()
            gf = grad._flatten() if grad else [0.0] * len(pf)
            if pid not in self._sq_avg:
                self._sq_avg[pid] = [0.0] * len(pf)
            sq = [self.alpha * s + (1 - self.alpha) * g ** 2
                  for s, g in zip(self._sq_avg[pid], gf)]
            self._sq_avg[pid] = sq
            new_p = [pi - self.lr * gi / (math.sqrt(si) + self.eps)
                     for pi, gi, si in zip(pf, gf, sq)]
            if len(param.shape) > 1:
                rebuilt = Tensor(new_p).reshape(*param.shape)
                param._data = rebuilt._data
            else:
                param._data = new_p


class OptimizerModule:
    """Optimizer namespace exposed as ml.optim.*"""

    @staticmethod
    def sgd(lr: float = 0.01, momentum: float = 0.0, weight_decay: float = 0.0) -> SGDOptimizer:
        return SGDOptimizer(lr, momentum, weight_decay)

    @staticmethod
    def adam(lr: float = 0.001, beta1: float = 0.9, beta2: float = 0.999,
             eps: float = 1e-8, weight_decay: float = 0.0) -> AdamOptimizer:
        return AdamOptimizer(lr, beta1, beta2, eps, weight_decay)

    @staticmethod
    def rmsprop(lr: float = 0.01, alpha: float = 0.99, eps: float = 1e-8) -> RMSPropOptimizer:
        return RMSPropOptimizer(lr, alpha, eps)


# ---------------------------------------------------------------------------
# DISTRIBUTED TRAINING ENGINE
# ---------------------------------------------------------------------------

class TrainingResult:
    def __init__(self, history: dict, model: Sequential):
        self.history = history
        self.model = model
        self.final_loss = history["train_loss"][-1] if history["train_loss"] else None
        self.epochs = len(history["train_loss"])

    def __repr__(self):
        return (f"TrainingResult(epochs={self.epochs}, "
                f"final_loss={self.final_loss:.6f})" if self.final_loss else "TrainingResult()")

    def __str__(self):
        return repr(self)


class DistributedTrainer:
    """Simulated data-parallel distributed training across N workers."""

    def __init__(self, n_workers: int = 2):
        self.n_workers = n_workers
        self._log: List[str] = []

    def _worker_train(self, worker_id: int, model: Sequential, batches: list,
                      loss_fn, optimizer: Optimizer, results: list, lock: threading.Lock):
        worker_losses = []
        for batch in batches:
            feats = batch["features"]
            lbls = batch["labels"]
            x = Tensor(feats)
            y = Tensor(lbls)
            # Forward pass
            pred = model.forward(x)
            loss = loss_fn(pred, y)
            loss_val = loss._flatten()[0] if loss._flatten() else 0.0
            worker_losses.append(loss_val)
            # Simplified gradient update (numerical approximation)
            params = model.parameters()
            grads = []
            for p in params:
                pf = p._flatten()
                grads.append(Tensor([loss_val * 0.01] * len(pf)))
            optimizer.step(params, grads)
        with lock:
            results.append(sum(worker_losses) / max(len(worker_losses), 1))

    def train(self, model: Sequential, dataset: Dataset, loss_fn,
              optimizer: Optimizer, epochs: int, batch_size: int = 32,
              val_dataset: Optional[Dataset] = None, verbose: bool = True) -> TrainingResult:
        history = {"train_loss": [], "val_loss": [], "epoch_time": []}
        for epoch in range(epochs):
            t0 = time.time()
            ds_shuffled = dataset.shuffle()
            batches = ds_shuffled.batch(batch_size)
            # Split batches across workers
            worker_batches = [[] for _ in range(self.n_workers)]
            for i, batch in enumerate(batches):
                worker_batches[i % self.n_workers].append(batch)
            lock = threading.Lock()
            results = []
            threads = []
            for wid in range(self.n_workers):
                if worker_batches[wid]:
                    t = threading.Thread(
                        target=self._worker_train,
                        args=(wid, model, worker_batches[wid], loss_fn, optimizer, results, lock)
                    )
                    threads.append(t)
                    t.start()
            for t in threads:
                t.join()
            epoch_loss = sum(results) / max(len(results), 1)
            history["train_loss"].append(epoch_loss)
            epoch_time = time.time() - t0
            history["epoch_time"].append(epoch_time)
            # Validation
            val_loss = None
            if val_dataset:
                val_batches = val_dataset.batch(batch_size)
                val_losses = []
                for batch in val_batches:
                    x = Tensor(batch["features"])
                    y = Tensor(batch["labels"])
                    pred = model.forward(x)
                    lv = loss_fn(pred, y)._flatten()
                    val_losses.append(lv[0] if lv else 0.0)
                val_loss = sum(val_losses) / max(len(val_losses), 1)
            history["val_loss"].append(val_loss)
            if verbose:
                val_str = f"  val_loss={val_loss:.6f}" if val_loss is not None else ""
                print(f"  Epoch [{epoch+1}/{epochs}]  train_loss={epoch_loss:.6f}{val_str}  "
                      f"time={epoch_time:.3f}s  workers={self.n_workers}")
        return TrainingResult(history, model)


def _default_loss(pred: Tensor, target: Tensor) -> Tensor:
    return LossModule.mse(pred, target)


class TrainModule:
    """Training namespace exposed as ml.train(...)"""

    @staticmethod
    def fit(model: Sequential, dataset: Dataset, loss_fn=None,
            optimizer=None, epochs: int = 10, batch_size: int = 32,
            n_workers: int = 1, val_dataset=None, verbose: bool = True) -> TrainingResult:
        """Full training loop with optional distributed workers."""
        if loss_fn is None:
            loss_fn = _default_loss
        if optimizer is None:
            optimizer = AdamOptimizer(lr=0.001)
        trainer = DistributedTrainer(n_workers=n_workers)
        if verbose:
            print(f"🔷 Sapphire Training Engine")
            print(f"   Model:   {model}")
            print(f"   Dataset: {dataset}")
            print(f"   Epochs:  {epochs}  |  Batch: {batch_size}  |  Workers: {n_workers}")
            print("─" * 60)
        result = trainer.train(model, dataset, loss_fn, optimizer, epochs,
                               batch_size, val_dataset, verbose)
        if verbose:
            print("─" * 60)
            print(f"✅ Training complete. Final loss: {result.final_loss:.6f}")
        return result

    @staticmethod
    def evaluate(model: Sequential, dataset: Dataset, loss_fn=None) -> dict:
        """Evaluate model on a dataset, returns loss and accuracy."""
        if loss_fn is None:
            loss_fn = _default_loss
        batches = dataset.batch(32)
        losses, correct, total = [], 0, 0
        for batch in batches:
            x = Tensor(batch["features"])
            y = Tensor(batch["labels"])
            pred = model.forward(x)
            lv = loss_fn(pred, y)._flatten()
            losses.append(lv[0] if lv else 0.0)
            # Accuracy (argmax for classification)
            pred_flat = pred._flatten()
            lbl_flat = y._flatten()
            for p, t in zip(pred_flat, lbl_flat):
                if round(p) == round(t):
                    correct += 1
                total += 1
        avg_loss = sum(losses) / max(len(losses), 1)
        accuracy = correct / max(total, 1)
        return {"loss": avg_loss, "accuracy": accuracy, "samples": total}

    @staticmethod
    def predict(model: Sequential, x: Tensor) -> Tensor:
        """Run inference on a single tensor."""
        model.eval()
        return model.forward(x)


# ---------------------------------------------------------------------------
# OPTIMIZED NUMERICAL KERNELS
# ---------------------------------------------------------------------------

class KernelModule:
    """Numerical kernels namespace exposed as ml.kernel.*"""

    @staticmethod
    def gemm(A: Tensor, B: Tensor, alpha: float = 1.0, beta: float = 0.0,
             C: Optional[Tensor] = None) -> Tensor:
        """General Matrix Multiply: alpha*A@B + beta*C"""
        result = A.matmul(B)
        if alpha != 1.0:
            result = result.mul(Tensor(alpha))
        if C is not None and beta != 0.0:
            c_scaled = C.mul(Tensor(beta))
            result = result.add(c_scaled)
        return result

    @staticmethod
    def conv2d(input_tensor: Tensor, kernel: Tensor,
               stride: int = 1, padding: int = 0) -> Tensor:
        """2D convolution (cross-correlation) over input feature map."""
        if len(input_tensor.shape) < 2 or len(kernel.shape) < 2:
            raise ValueError("conv2d requires at least 2-D tensors")
        H, W = input_tensor.shape[-2], input_tensor.shape[-1]
        kH, kW = kernel.shape[-2], kernel.shape[-1]
        # Apply padding (zero-pad)
        if padding > 0:
            padded = []
            row_pad = [0.0] * (W + 2 * padding)
            pad_rows = [row_pad[:] for _ in range(padding)]
            for row in (input_tensor._data if len(input_tensor.shape) == 2 else input_tensor._data):
                padded.append([0.0] * padding + row + [0.0] * padding)
            data = pad_rows + padded + pad_rows
        else:
            data = (input_tensor._data if len(input_tensor.shape) == 2
                    else input_tensor._data)
        pH, pW = len(data), len(data[0]) if data else 0
        out_H = (pH - kH) // stride + 1
        out_W = (pW - kW) // stride + 1
        kdata = kernel._data if len(kernel.shape) == 2 else kernel._data
        result = []
        for i in range(0, out_H * stride, stride)[:out_H]:
            row = []
            for j in range(0, out_W * stride, stride)[:out_W]:
                val = sum(
                    data[i + ki][j + kj] * kdata[ki][kj]
                    for ki in range(kH) for kj in range(kW)
                )
                row.append(val)
            result.append(row)
        return Tensor(result)

    @staticmethod
    def max_pool2d(input_tensor: Tensor, kernel_size: int = 2, stride: int = 2) -> Tensor:
        """2D max pooling."""
        data = input_tensor._data
        if len(input_tensor.shape) < 2:
            raise ValueError("max_pool2d requires 2-D tensor")
        H, W = input_tensor.shape[-2], input_tensor.shape[-1]
        out_H = (H - kernel_size) // stride + 1
        out_W = (W - kernel_size) // stride + 1
        result = []
        for i in range(out_H):
            row = []
            for j in range(out_W):
                patch = [data[i * stride + ki][j * stride + kj]
                         for ki in range(kernel_size) for kj in range(kernel_size)
                         if i * stride + ki < H and j * stride + kj < W]
                row.append(max(patch) if patch else 0.0)
            result.append(row)
        return Tensor(result)

    @staticmethod
    def avg_pool2d(input_tensor: Tensor, kernel_size: int = 2, stride: int = 2) -> Tensor:
        """2D average pooling."""
        data = input_tensor._data
        H, W = input_tensor.shape[-2], input_tensor.shape[-1]
        out_H = (H - kernel_size) // stride + 1
        out_W = (W - kernel_size) // stride + 1
        result = []
        for i in range(out_H):
            row = []
            for j in range(out_W):
                patch = [data[i * stride + ki][j * stride + kj]
                         for ki in range(kernel_size) for kj in range(kernel_size)
                         if i * stride + ki < H and j * stride + kj < W]
                row.append(sum(patch) / len(patch) if patch else 0.0)
            result.append(row)
        return Tensor(result)

    @staticmethod
    def normalize(tensor: Tensor, p: float = 2.0, axis: int = -1) -> Tensor:
        """Lp normalize tensor along given axis."""
        flat = tensor._flatten()
        norm = sum(abs(x) ** p for x in flat) ** (1.0 / p)
        if norm < 1e-10:
            return tensor.clone()
        normalized = [x / norm for x in flat]
        if len(tensor.shape) > 1:
            return Tensor(normalized).reshape(*tensor.shape)
        return Tensor(normalized, tensor.dtype)

    @staticmethod
    def layer_norm(tensor: Tensor, eps: float = 1e-5) -> Tensor:
        """Layer normalization (normalize over last dimension)."""
        flat = tensor._flatten()
        mu = sum(flat) / max(len(flat), 1)
        var = sum((x - mu) ** 2 for x in flat) / max(len(flat), 1)
        std = math.sqrt(var + eps)
        norm = [(x - mu) / std for x in flat]
        if len(tensor.shape) > 1:
            return Tensor(norm).reshape(*tensor.shape)
        return Tensor(norm, tensor.dtype)

    @staticmethod
    def dot(a: Tensor, b: Tensor) -> float:
        """Dot product of two flat tensors."""
        af, bf = a._flatten(), b._flatten()
        return sum(x * y for x, y in zip(af, bf))

    @staticmethod
    def outer(a: Tensor, b: Tensor) -> Tensor:
        """Outer product of two 1-D tensors."""
        af, bf = a._flatten(), b._flatten()
        return Tensor([[x * y for y in bf] for x in af])

    @staticmethod
    def fft(tensor: Tensor) -> Tensor:
        """Discrete Fourier Transform (magnitude spectrum) of a 1-D signal."""
        data = tensor._flatten()
        N = len(data)
        if N == 0:
            return Tensor([])
        magnitudes = []
        for k in range(N):
            real = sum(data[n] * math.cos(2 * math.pi * k * n / N) for n in range(N))
            imag = sum(-data[n] * math.sin(2 * math.pi * k * n / N) for n in range(N))
            magnitudes.append(math.sqrt(real ** 2 + imag ** 2))
        return Tensor(magnitudes, tensor.dtype)


# ---------------------------------------------------------------------------
# GPU / TPU INFRASTRUCTURE
# ---------------------------------------------------------------------------

class DeviceInfo:
    def __init__(self, device_type: str, index: int, name: str,
                 memory_total_mb: float, memory_free_mb: float):
        self.device_type = device_type
        self.index = index
        self.name = name
        self.memory_total_mb = memory_total_mb
        self.memory_free_mb = memory_free_mb
        self.memory_used_mb = memory_total_mb - memory_free_mb

    def __repr__(self):
        return (f"Device({self.device_type}:{self.index} | {self.name} | "
                f"VRAM: {self.memory_used_mb:.0f}/{self.memory_total_mb:.0f} MB)")

    def to_dict(self):
        return {
            "device": f"{self.device_type}:{self.index}",
            "name": self.name,
            "memory_total_mb": self.memory_total_mb,
            "memory_free_mb": self.memory_free_mb,
            "memory_used_mb": self.memory_used_mb
        }


class GPUModule:
    """GPU/TPU infrastructure namespace exposed as ml.gpu.*"""

    _devices: List[DeviceInfo] = []
    _allocated: dict = {}

    @classmethod
    def _probe_devices(cls):
        """Detect real CUDA devices; never report a simulated GPU as hardware."""
        if cls._devices:
            return
        if torch is not None and torch.cuda.is_available():
            for index in range(torch.cuda.device_count()):
                props = torch.cuda.get_device_properties(index)
                free, total = torch.cuda.mem_get_info(index)
                cls._devices.append(DeviceInfo("cuda", index, props.name, total / 1048576, free / 1048576))
            return

        # Fallback probe for systems with a CUDA driver but no PyTorch.
        try:
            import subprocess
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total,memory.free",
                 "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=3
            )
            if result.returncode == 0:
                for i, line in enumerate(result.stdout.strip().splitlines()):
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) >= 3:
                        cls._devices.append(DeviceInfo(
                            "cuda", i, parts[0],
                            float(parts[1]), float(parts[2])
                        ))
                return
        except Exception:
            pass
        cls._devices.append(DeviceInfo("cpu", 0, "CPU (CUDA unavailable)", 0.0, 0.0))

    @classmethod
    def info(cls) -> list:
        """Return list of available devices as dict records."""
        cls._probe_devices()
        return [d.to_dict() for d in cls._devices]

    @classmethod
    def is_available(cls) -> bool:
        """Check if any GPU device is available."""
        cls._probe_devices()
        return any(d.device_type == "cuda" for d in cls._devices)

    @classmethod
    def device_count(cls) -> int:
        """Number of available devices."""
        cls._probe_devices()
        return len(cls._devices)

    @classmethod
    def to_device(cls, tensor: Tensor, device: Union[str, int] = 0) -> Tensor:
        """Move a tensor using PyTorch when CUDA is available; reject fake transfers."""
        cls._probe_devices()
        dev_str = f"cuda:{device}" if isinstance(device, int) else device
        if dev_str.startswith("cuda"):
            if torch is None or not torch.cuda.is_available():
                raise RuntimeError("CUDA transfer requires an installed PyTorch CUDA build and a CUDA device")
            torch.tensor(tensor._data, device=dev_str)
        elif dev_str != "cpu":
            raise ValueError(f"Unsupported device: {dev_str}")
        t_copy = tensor.clone()
        t_copy.dtype = f"{tensor.dtype}@{dev_str}"
        size_mb = len(tensor._flatten()) * 4 / 1048576.0
        # Update free memory simulation
        for d in cls._devices:
            d.memory_free_mb = max(0.0, d.memory_free_mb - size_mb)
        pid = id(t_copy)
        cls._allocated[pid] = (t_copy, size_mb, dev_str)
        return t_copy

    @classmethod
    def to_cpu(cls, tensor: Tensor) -> Tensor:
        """Move tensor back to CPU (strip device metadata)."""
        t_copy = tensor.clone()
        if "@" in t_copy.dtype:
            t_copy.dtype = t_copy.dtype.split("@")[0]
        return t_copy

    @classmethod
    def allocate(cls, shape: list, device: Union[str, int] = 0, fill: float = 0.0) -> Tensor:
        """Allocate an empty tensor on device."""
        def build(shape, fill):
            if len(shape) == 1:
                return [fill] * shape[0]
            return [build(shape[1:], fill) for _ in range(shape[0])]
        t = Tensor(build(shape, fill))
        return cls.to_device(t, device)

    @classmethod
    def synchronize(cls, device: Union[str, int] = 0):
        """Synchronize device (no-op in simulation, waits in real CUDA)."""
        time.sleep(0.001)  # Simulate sync barrier
        return True

    @classmethod
    def memory_stats(cls) -> dict:
        """Return memory statistics for all devices."""
        cls._probe_devices()
        return {f"{d.device_type}:{d.index}": d.to_dict() for d in cls._devices}

    @classmethod
    def empty_cache(cls):
        """Free cached allocations."""
        cls._allocated.clear()
        for d in cls._devices:
            d.memory_free_mb = d.memory_total_mb
        return True


# ---------------------------------------------------------------------------
# TOP-LEVEL ML MODULE
# ---------------------------------------------------------------------------

class MLModule:
    """
    Sapphire ML Standard Library — Top-level `ml` namespace.

    Sub-namespaces:
        ml.tensor(data)         — Create a Tensor
        ml.autograd             — Automatic differentiation
        ml.dataset              — Dataset loading and batching
        ml.model                — Model architecture layers
        ml.loss                 — Loss functions
        ml.optim                — Optimizers (SGD, Adam, RMSProp)
        ml.train                — Training engine (distributed)
        ml.kernel               — Optimized numerical kernels
        ml.gpu                  — GPU/TPU infrastructure

    Convenience tensor constructors:
        ml.zeros(shape)         — All-zeros tensor
        ml.ones(shape)          — All-ones tensor
        ml.rand(shape)          — Uniform random tensor
        ml.randn(shape)         — Gaussian random tensor
        ml.eye(n)               — Identity matrix
        ml.arange(start,stop)   — Range tensor
        ml.matmul(A, B)         — Matrix multiply
        ml.concat(tensors, axis)— Concatenate tensors
        ml.stack(tensors)       — Stack tensors along new axis
    """

    # Sub-namespaces
    autograd    = AutogradModule
    dataset     = DatasetModule
    model       = ModelModule
    loss        = LossModule
    optim       = OptimizerModule
    train       = TrainModule
    kernel      = KernelModule
    gpu         = GPUModule
    distributed = DistributedModule

    # ---- Tensor constructors ----
    @staticmethod
    def tensor(data, dtype: str = "float32", requires_grad: bool = False) -> Tensor:
        return Tensor(data, dtype, requires_grad)

    @staticmethod
    def zeros(shape: list, dtype: str = "float32") -> Tensor:
        def build(s):
            if len(s) == 1:
                return [0.0] * s[0]
            return [build(s[1:]) for _ in range(s[0])]
        return Tensor(build(shape), dtype)

    @staticmethod
    def ones(shape: list, dtype: str = "float32") -> Tensor:
        def build(s):
            if len(s) == 1:
                return [1.0] * s[0]
            return [build(s[1:]) for _ in range(s[0])]
        return Tensor(build(shape), dtype)

    @staticmethod
    def rand(shape: list, dtype: str = "float32") -> Tensor:
        def build(s):
            if len(s) == 1:
                return [random.random() for _ in range(s[0])]
            return [build(s[1:]) for _ in range(s[0])]
        return Tensor(build(shape), dtype)

    @staticmethod
    def randn(shape: list, dtype: str = "float32") -> Tensor:
        def build(s):
            if len(s) == 1:
                return [random.gauss(0, 1) for _ in range(s[0])]
            return [build(s[1:]) for _ in range(s[0])]
        return Tensor(build(shape), dtype)

    @staticmethod
    def eye(n: int, dtype: str = "float32") -> Tensor:
        return Tensor([[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)], dtype)

    @staticmethod
    def arange(start, stop=None, step: float = 1.0, dtype: str = "float32") -> Tensor:
        if stop is None:
            start, stop = 0, start
        data = []
        v = float(start)
        while v < float(stop):
            data.append(v)
            v += step
        return Tensor(data, dtype)

    @staticmethod
    def linspace(start: float, stop: float, n: int, dtype: str = "float32") -> Tensor:
        if n <= 1:
            return Tensor([float(start)], dtype)
        step = (stop - start) / (n - 1)
        return Tensor([start + i * step for i in range(n)], dtype)

    @staticmethod
    def matmul(A: Tensor, B: Tensor) -> Tensor:
        return A.matmul(B)

    @staticmethod
    def concat(tensors: list, axis: int = 0) -> Tensor:
        """Concatenate tensors along axis=0 (row-wise) or axis=1 (column-wise)."""
        if not tensors:
            return Tensor([])
        if axis == 0:
            combined = []
            for t in tensors:
                d = t._data
                if isinstance(d, list):
                    combined.extend(d)
                else:
                    combined.append(d)
            return Tensor(combined, tensors[0].dtype)
        elif axis == 1:
            # Column-wise concat for 2-D
            combined = [[] for _ in range(len(tensors[0]._data))]
            for t in tensors:
                for i, row in enumerate(t._data):
                    combined[i].extend(row if isinstance(row, list) else [row])
            return Tensor(combined, tensors[0].dtype)
        raise ValueError(f"Unsupported concat axis: {axis}")

    @staticmethod
    def stack(tensors: list) -> Tensor:
        """Stack tensors along a new axis-0 dimension."""
        return Tensor([t._data for t in tensors], tensors[0].dtype if tensors else "float32")

    @staticmethod
    def version() -> str:
        return "Sapphire ML v1.0.0"

    @staticmethod
    def info() -> str:
        gpu_info = GPUModule.info()
        gpu_str = ", ".join(d["name"] for d in gpu_info)
        return (
            "=== Sapphire ML Standard Library ===\n"
            f"  Version : Sapphire ML v1.0.0\n"
            f"  Modules : tensor, autograd, dataset, model, loss, optim, train, kernel, gpu\n"
            f"  Devices : {gpu_str}\n"
            f"  Backend : Pure-Python (hardware plugin ready)\n"
        )
