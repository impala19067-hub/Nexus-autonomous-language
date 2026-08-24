"""
Sapphire Distributed LLM & Cluster Specifications
Defines:
- Transformer: Frontier LLM Architecture (Dense & MoE)
- MoE: Mixture-of-Experts Architecture
- Parameter count, FLOPs per token, and activation memory equations
"""

import math
from typing import Dict, Any, Optional

class Transformer:
    """
    Frontier Transformer LLM Architecture Specification in Sapphire.
    Supports Dense Transformers and Sparse Mixture-of-Experts (MoE).
    """
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            kwargs = {**args[0], **kwargs}

        self.layers = int(kwargs.get("layers", args[0] if len(args) > 0 and not isinstance(args[0], dict) else 32))
        self.hidden = int(kwargs.get("hidden", args[1] if len(args) > 1 else 4096))
        self.heads = int(kwargs.get("heads", args[2] if len(args) > 2 else 32))
        kv_h = kwargs.get("kv_heads", args[3] if len(args) > 3 else None)
        self.kv_heads = int(kv_h) if kv_h is not None else self.heads
        self.head_dim = self.hidden // self.heads
        self.vocab = int(kwargs.get("vocab", args[4] if len(args) > 4 else 32000))
        self.seq_len = int(kwargs.get("seq_len", args[5] if len(args) > 5 else 4096))
        inter_dim = kwargs.get("intermediate_dim", args[6] if len(args) > 6 else None)
        self.intermediate_dim = int(inter_dim) if inter_dim is not None else int(8 * self.hidden // 3)
        self.moe_experts = int(kwargs.get("moe_experts", args[7] if len(args) > 7 else 1))
        self.moe_top_k = int(kwargs.get("moe_top_k", args[8] if len(args) > 8 else 1))
        self.moe_shared_experts = int(kwargs.get("moe_shared_experts", 0))
        self.rotary_base = float(kwargs.get("rotary_base", 500000.0))
        self.qk_norm = bool(kwargs.get("qk_norm", True))
        self.tie_embeddings = bool(kwargs.get("tie_embeddings", False))
        self.activation = str(kwargs.get("activation", "swiglu"))

        # Compute architecture metrics
        self.is_moe = self.moe_experts > 1
        self.total_params = self._calculate_total_params()
        self.active_params = self._calculate_active_params()
        self.flops_per_token = self._calculate_flops_per_token()

    def _calculate_total_params(self) -> int:
        """Calculates exact parameter count of the full model."""
        embed_params = self.vocab * self.hidden
        q_params = self.hidden * self.hidden
        k_params = self.hidden * (self.kv_heads * self.head_dim)
        v_params = self.hidden * (self.kv_heads * self.head_dim)
        out_params = self.hidden * self.hidden
        attn_per_layer = q_params + k_params + v_params + out_params

        ffn_per_expert = 3 * self.hidden * self.intermediate_dim
        if self.is_moe:
            router_params = self.hidden * self.moe_experts
            moe_routed_params = self.moe_experts * ffn_per_expert
            shared_expert_params = self.moe_shared_experts * ffn_per_expert
            ffn_per_layer = router_params + moe_routed_params + shared_expert_params
        else:
            ffn_per_layer = ffn_per_expert

        norms_per_layer = 2 * self.hidden
        layer_params = attn_per_layer + ffn_per_layer + norms_per_layer
        total_layers = self.layers * layer_params

        final_norm = self.hidden
        lm_head = 0 if self.tie_embeddings else (self.hidden * self.vocab)

        return embed_params + total_layers + final_norm + lm_head

    def _calculate_active_params(self) -> int:
        """Calculates active parameter count per forward token (for MoE)."""
        if not self.is_moe:
            return self.total_params

        embed_params = self.vocab * self.hidden
        attn_per_layer = 2 * self.hidden * self.hidden + 2 * self.hidden * (self.kv_heads * self.head_dim)
        
        ffn_per_expert = 3 * self.hidden * self.intermediate_dim
        active_ffn_per_layer = (self.moe_top_k + self.moe_shared_experts) * ffn_per_expert + (self.hidden * self.moe_experts)
        norms_per_layer = 2 * self.hidden

        active_per_layer = attn_per_layer + active_ffn_per_layer + norms_per_layer
        lm_head = 0 if self.tie_embeddings else (self.hidden * self.vocab)
        return embed_params + (self.layers * active_per_layer) + self.hidden + lm_head

    def _calculate_flops_per_token(self) -> int:
        """Calculates theoretical FLOPs per token for backward+forward passes."""
        linear_flops = 6 * self.active_params
        attn_context_flops = 12 * self.layers * self.hidden * self.seq_len
        return linear_flops + attn_context_flops

    def activation_memory_bytes_per_token(self, precision_bytes: int = 2) -> int:
        """Estimates activation memory footprint in bytes per token per layer."""
        bytes_per_layer = precision_bytes * (
            (self.hidden * 4) +
            (self.intermediate_dim * 3) +
            (self.hidden * 2)
        )
        return bytes_per_layer * self.layers

    def summary(self) -> Dict[str, Any]:
        return {
            "layers": self.layers,
            "hidden": self.hidden,
            "heads": self.heads,
            "kv_heads": self.kv_heads,
            "vocab": self.vocab,
            "seq_len": self.seq_len,
            "intermediate_dim": self.intermediate_dim,
            "is_moe": self.is_moe,
            "moe_experts": self.moe_experts,
            "moe_top_k": self.moe_top_k,
            "total_params": self.total_params,
            "total_params_billion": round(self.total_params / 1e9, 2),
            "active_params_billion": round(self.active_params / 1e9, 2),
            "flops_per_token": self.flops_per_token,
            "flops_per_token_tflops": round(self.flops_per_token / 1e12, 4)
        }

    def __repr__(self) -> str:
        s = self.summary()
        moe_str = f", MoE={self.moe_experts}E(top-{self.moe_top_k})" if self.is_moe else ""
        return (
            f"💎 Sapphire.Transformer({s['total_params_billion']}B params, "
            f"layers={self.layers}, hidden={self.hidden}, heads={self.heads}{moe_str})"
        )
