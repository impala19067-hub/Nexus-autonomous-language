"""
Sapphire AI Agent Architecture Standard Library
Covers: Memory, Planning, Tools, Autonomy, Permissions, and Multi-Agent Orchestration
"""
import time
import json
import math
import fnmatch
import re
from typing import List, Dict, Any, Optional, Callable


# ---------------------------------------------------------------------------
# 1. MEMORY ARCHITECTURE (Short-Term & Long-Term Vector/KV Store)
# ---------------------------------------------------------------------------

class ShortTermMemory:
    """Buffer for conversation history and active reasoning trace."""
    def __init__(self, max_capacity: int = 50):
        self.max_capacity = max_capacity
        self._history: List[Dict[str, str]] = []

    def push(self, role: str, content: str):
        self._history.append({"role": role, "content": content, "timestamp": time.time()})
        if len(self._history) > self.max_capacity:
            self._history.pop(0)

    def get_history(self) -> List[Dict[str, str]]:
        return list(self._history)

    def clear(self):
        self._history.clear()

    def __repr__(self):
        return f"ShortTermMemory(entries={len(self._history)})"


class LongTermVectorStore:
    """Key-value and vector similarity store for persistent agent knowledge."""
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}

    def _text_to_vector(self, text: str) -> List[float]:
        """Simple bag-of-words character n-gram pseudo embedding vector."""
        vec = [0.0] * 32
        for i, char in enumerate(text.lower()):
            idx = ord(char) % 32
            vec[idx] += 1.0
        # Normalize vector
        norm = math.sqrt(sum(v * v for v in vec))
        if norm > 0:
            vec = [v / norm for v in vec]
        return vec

    def _cosine_sim(self, vec1: List[float], vec2: List[float]) -> float:
        return sum(v1 * v2 for v1, v2 in zip(vec1, vec2))

    def store(self, key: str, value: Any, metadata: Optional[dict] = None):
        text_rep = f"{key} {value} {json.dumps(metadata) if metadata else ''}"
        vec = self._text_to_vector(text_rep)
        self._store[key] = {
            "key": key,
            "value": value,
            "metadata": metadata or {},
            "vector": vec,
            "timestamp": time.time()
        }
        return True

    def get(self, key: str) -> Any:
        entry = self._store.get(key)
        return entry["value"] if entry else None

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Vector similarity search."""
        q_vec = self._text_to_vector(query)
        scored = []
        for key, item in self._store.items():
            sim = self._cosine_sim(q_vec, item["vector"])
            scored.append({"key": key, "value": item["value"], "similarity": sim, "metadata": item["metadata"]})
        scored.sort(key=lambda x: x["similarity"], reverse=True)
        return scored[:top_k]

    def delete(self, key: str) -> bool:
        if key in self._store:
            del self._store[key]
            return True
        return False

    def clear(self):
        self._store.clear()

    def __repr__(self):
        return f"LongTermStore(keys={len(self._store)})"


class MemoryModule:
    """Agent Memory sub-namespace exposed as agent.memory.*"""
    short_term = ShortTermMemory()
    long_term = LongTermVectorStore()

    @classmethod
    def remember(cls, key: str, value: Any, metadata: Optional[dict] = None):
        return cls.long_term.store(key, value, metadata)

    @classmethod
    def recall(cls, query: str, top_k: int = 3):
        return cls.long_term.search(query, top_k)

    @classmethod
    def get(cls, key: str):
        return cls.long_term.get(key)

    @classmethod
    def push_chat(cls, role: str, content: str):
        cls.short_term.push(role, content)

    @classmethod
    def history(cls):
        return cls.short_term.get_history()

    @classmethod
    def clear(cls):
        cls.short_term.clear()
        cls.long_term.clear()


class ContextEngine:
    """Assemble bounded retrieval and recent interaction context."""

    @classmethod
    def build(cls, query: str, max_chars: int = 4000, workspace: Optional[str] = None) -> str:
        memories = [f"memory[{item['key']}]: {item['value']}" for item in MemoryModule.recall(query, 5)]
        history = [f"{item['role']}: {item['content']}" for item in MemoryModule.history()[-5:]]
        sources = []
        if workspace:
            from industrial import CodebaseIndex
            index = CodebaseIndex(workspace)
            index.rebuild()
            sources = [f"file[{item['source']}#{item['chunk']}]: {item['content']}" for item in index.search(query, 5)]
        return "\n".join(memories + sources + history)[:max_chars]


# ---------------------------------------------------------------------------
# 2. PLANNING & REASONING (Decomposition, ReAct, Tree of Thought)
# ---------------------------------------------------------------------------

class PlanTask:
    def __init__(self, step_id: int, description: str, tool_name: Optional[str] = None):
        self.step_id = step_id
        self.description = description
        self.tool_name = tool_name
        self.status = "pending"  # "pending", "running", "completed", "failed"
        self.result = None

    def to_dict(self):
        return {
            "step_id": self.step_id,
            "description": self.description,
            "tool_name": self.tool_name,
            "status": self.status,
            "result": self.result
        }


class Plan:
    def __init__(self, goal: str, tasks: List[PlanTask], source: str = "model"):
        self.goal = goal
        self.tasks = tasks
        self.source = source
        self.created_at = time.time()

    def next_task(self) -> Optional[PlanTask]:
        for t in self.tasks:
            if t.status == "pending":
                return t
        return None

    def mark_complete(self, step_id: int, result: Any):
        for t in self.tasks:
            if t.step_id == step_id:
                t.status = "completed"
                t.result = result
                break

    def is_finished(self) -> bool:
        return all(t.status == "completed" for t in self.tasks)

    def summary(self) -> str:
        lines = [f"=== Sapphire Plan ({self.source}): {self.goal} ==="]
        for t in self.tasks:
            icon = "✅" if t.status == "completed" else ("⏳" if t.status == "running" else "📌")
            lines.append(f"  {icon} Step {t.step_id}: {t.description} [{t.status}]")
        return "\n".join(lines)


class PlanningModule:
    """Agent Planning sub-namespace exposed as agent.planning.*"""

    @staticmethod
    def create_plan(goal: str, context: Optional[str] = None) -> Plan:
        """Generate and validate an actionable plan from the configured AI backend."""
        from src.stdlib.ai_mod import AIModule
        prompt = (
            "Decompose the following goal into 3 to 8 actionable execution steps. "
            "Return ONLY valid JSON, with this exact shape: "
            '{"steps":[{"description":"...","tool":"optional tool name"}]}. '
            f"Goal: {goal}. Context: {context or 'None'}"
        )
        res = AIModule.prompt(prompt)
        tasks = PlanningModule._parse_model_plan(res)
        if tasks:
            return Plan(goal, tasks, source="AI-generated")
        return Plan(goal, [PlanTask(1, f"Review and execute the goal: {goal}")], source="fallback")

    @staticmethod
    def _parse_model_plan(response: Any) -> List[PlanTask]:
        if not isinstance(response, str) or not response.strip():
            return []
        text = response.strip()
        fenced = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.IGNORECASE | re.DOTALL)
        candidates = [fenced.group(1)] if fenced else [text]
        candidates.append(text)
        for candidate in candidates:
            try:
                payload = json.loads(candidate)
            except json.JSONDecodeError:
                continue
            raw_steps = payload.get("steps") if isinstance(payload, dict) else payload
            if not isinstance(raw_steps, list):
                continue
            tasks = []
            for item in raw_steps:
                if isinstance(item, str):
                    description, tool = item.strip(), None
                elif isinstance(item, dict):
                    description = str(item.get("description", item.get("step", ""))).strip()
                    tool = item.get("tool", item.get("tool_name"))
                    tool = str(tool).strip() if tool else None
                else:
                    continue
                if description:
                    tasks.append(PlanTask(len(tasks) + 1, description, tool))
            if tasks:
                return tasks

        numbered_tasks = []
        for line in text.splitlines():
            match = re.match(r"^\s*(?:\d+[.)]|[-*])\s+(.*?)(?:\s*\[tool:\s*([^\]]+)\])?\s*$", line, re.IGNORECASE)
            if match and match.group(1).strip():
                numbered_tasks.append(PlanTask(len(numbered_tasks) + 1, match.group(1).strip(), match.group(2)))
        return numbered_tasks

    @staticmethod
    def react_step(goal: str, plan: Plan, observation: str) -> dict:
        """Ask the configured AI backend to choose the next executable action."""
        task = plan.next_task()
        if not task:
            return {"thought": "All tasks completed.", "action": "finish", "finished": True}
        from src.stdlib.ai_mod import AIModule
        prompt = (
            "Choose the next action. Return ONLY JSON with keys thought, action, and args. "
            "Action must be a registered tool name or os, ml, notify. "
            f"Goal: {goal}. Task: {task.description}. Observation: {observation}"
        )
        decision = PlanningModule._parse_action(AIModule.prompt(prompt))
        thought = decision.get("thought") or f"Observed '{observation}'. Executing: {task.description}."
        action = decision.get("action") or task.tool_name
        if not action:
            description = task.description.lower()
            action = "notify" if any(word in description for word in ("notify", "alert")) else (
                "ml" if any(word in description for word in ("train", "tensor", "model", "gpu")) else "os"
            )
        return {
            "thought": thought,
            "action": action,
            "args": decision.get("args", {}),
            "task_id": task.step_id,
            "finished": False
        }

    @staticmethod
    def _parse_action(response: Any) -> dict:
        if not isinstance(response, str):
            return {}
        text = response.strip()
        fenced = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.IGNORECASE | re.DOTALL)
        for candidate in (fenced.group(1), text) if fenced else (text,):
            try:
                value = json.loads(candidate)
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict):
                return value
        return {}


# ---------------------------------------------------------------------------
# 3. TOOLS & EXTENSIBILITY FRAMEWORK
# ---------------------------------------------------------------------------

class Tool:
    def __init__(self, name: str, description: str, fn: Callable, schema: Optional[dict] = None):
        self.name = name
        self.description = description
        self.fn = fn
        self.schema = schema or {}

    def execute(self, *args, **kwargs) -> Any:
        return self.fn(*args, **kwargs)

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "schema": self.schema
        }


class ToolsModule:
    """Agent Tools registry sub-namespace exposed as agent.tools.*"""
    _registry: Dict[str, Tool] = {}

    @classmethod
    def register(cls, name: str, description: str, fn: Callable, schema: Optional[dict] = None) -> bool:
        cls._registry[name] = Tool(name, description, fn, schema)
        return True

    @classmethod
    def execute(cls, name: str, *args, **kwargs) -> Any:
        if name not in cls._registry:
            raise KeyError(f"Tool '{name}' is not registered in Sapphire Tools registry")
        # Check permissions before tool execution
        PermissionsModule.check("tool_execute", name)
        return cls._registry[name].execute(*args, **kwargs)

    @classmethod
    def list_tools(cls) -> List[dict]:
        return [t.to_dict() for t in cls._registry.values()]

    @classmethod
    def has_tool(cls, name: str) -> bool:
        return name in cls._registry


# ---------------------------------------------------------------------------
# 4. PERMISSIONS & SECURITY BOUNDARIES
# ---------------------------------------------------------------------------

class PermissionsModule:
    """Agent Security & Permission Policies exposed as agent.permissions.*"""
    policy = "permissive"  # "strict", "interactive", "permissive"
    allowed_paths: List[str] = ["*"]
    allowed_commands: List[str] = ["*"]
    allowed_hosts: List[str] = ["*"]

    @classmethod
    def set_policy(cls, mode: str):
        if mode not in ("strict", "interactive", "permissive"):
            raise ValueError("Policy mode must be 'strict', 'interactive', or 'permissive'")
        cls.policy = mode
        return True

    @classmethod
    def allow_path(cls, pattern: str):
        cls.allowed_paths.append(pattern)

    @classmethod
    def allow_command(cls, pattern: str):
        cls.allowed_commands.append(pattern)

    @classmethod
    def allow_host(cls, pattern: str):
        cls.allowed_hosts.append(pattern)

    @classmethod
    def check(cls, action_type: str, target: str) -> bool:
        if cls.policy == "permissive":
            return True

        if action_type == "file_write" or action_type == "file_delete":
            for p in cls.allowed_paths:
                if p == "*" or fnmatch.fnmatch(target, p):
                    return True
            if cls.policy == "strict":
                raise PermissionError(f"Sapphire Security: Action '{action_type}' denied for path '{target}' under strict policy.")
            
        elif action_type == "cmd_exec":
            for c in cls.allowed_commands:
                if c == "*" or fnmatch.fnmatch(target, c):
                    return True
            if cls.policy == "strict":
                raise PermissionError(f"Sapphire Security: Command '{target}' denied under strict policy.")

        return True


# ---------------------------------------------------------------------------
# 5. AUTONOMOUS AGENT EXECUTION LOOP
# ---------------------------------------------------------------------------

class AutonomousAgent:
    """
    Complete Sapphire Autonomous Agent:
    Data → Training → Model → Reasoning → Memory → Planning → Tool use → Autonomous execution
    """
    def __init__(self, name: str, goal: str, model_name: str = "default", context: Optional[str] = None):
        self.name = name
        self.goal = goal
        self.model_name = model_name
        self.memory = MemoryModule()
        self.context = context or ContextEngine.build(goal)
        self.plan = PlanningModule.create_plan(goal, self.context)
        self.logs: List[str] = []

    def log(self, message: str):
        st = f"[{self.name} | {time.strftime('%H:%M:%S')}] {message}"
        self.logs.append(st)
        print(st)

    def run(self, max_steps: int = 10) -> dict:
        self.log(f"🚀 Starting Autonomous Agent Execution Loop for goal: '{self.goal}'")
        self.memory.push_chat("system", f"Agent initialized with goal: {self.goal}")
        self.memory.remember(f"{self.name}_goal", self.goal, {"type": "goal"})

        step = 0
        while not self.plan.is_finished() and step < max_steps:
            step += 1
            task = self.plan.next_task()
            if not task:
                break
            
            self.log(f"📌 [Step {task.step_id}/{len(self.plan.tasks)}] {task.description}")

            # 1. Reasoning & Planning
            observation = getattr(self, "_last_observation", f"Preparing step {task.step_id}")
            step_eval = PlanningModule.react_step(self.goal, self.plan, observation)
            self.memory.remember(f"step_{task.step_id}_thought", step_eval["thought"])

            task.status = "running"
            try:
                result = self._execute_action(step_eval["action"], step_eval.get("args", {}), task.description)
                self._last_observation = f"Action {step_eval['action']} returned: {result!r}"
                self.plan.mark_complete(task.step_id, result)
                self.memory.remember(f"{self.name}_step_{task.step_id}_result", self._last_observation, {"type": "observation"})
                self.memory.push_chat("assistant", self._last_observation)
                self.log(f"✅ Finished step {task.step_id} using {step_eval['action']}")
            except Exception as error:
                task.status = "failed"
                task.result = str(error)
                self.memory.push_chat("system", f"Step {task.step_id} failed: {error}")
                self.log(f"❌ Step {task.step_id} failed: {error}")
                break

        finished = self.plan.is_finished()
        self.log(f"✨ Autonomous Execution {'Completed Successfully' if finished else 'Paused'}")
        return {
            "agent": self.name,
            "goal": self.goal,
            "finished": finished,
            "steps_completed": step,
            "plan_summary": self.plan.summary()
        }

    def _execute_action(self, action: str, args: dict, description: str):
        if not isinstance(args, dict):
            raise TypeError("Agent action args must be a JSON object")
        if ToolsModule.has_tool(action):
            return ToolsModule.execute(action, **args)
        if action == "os":
            PermissionsModule.check("os_read", "system_info")
            from src.stdlib.os_mod import OSModule
            return OSModule.system_info()
        if action == "ml":
            PermissionsModule.check("ml_execute", "runtime")
            from src.stdlib.ml_mod import MLModule
            return MLModule.info()
        if action == "notify":
            PermissionsModule.check("notify", "Sapphire Agent")
            from src.stdlib.os_mod import OSModule
            return OSModule.notify("Sapphire Agent", description)
        raise RuntimeError(f"No executable tool registered for action '{action}'")


class AutonomyModule:
    """Agent Autonomy sub-namespace exposed as agent.autonomy.*"""

    @staticmethod
    def create_agent(name: str, goal: str, workspace: Optional[str] = None) -> AutonomousAgent:
        return AutonomousAgent(name, goal, context=ContextEngine.build(goal, workspace=workspace))

    @staticmethod
    def run_loop(goal: str, max_steps: int = 10) -> dict:
        agent = AutonomousAgent("SapphireAgent", goal)
        return agent.run(max_steps)


# ---------------------------------------------------------------------------
# 6. MULTI-AGENT ORCHESTRATION & SWARM
# ---------------------------------------------------------------------------

class AgentOrchestrator:
    """Coordinates multiple autonomous Sapphire agents in a swarm."""

    def __init__(self):
        self._agents: Dict[str, AutonomousAgent] = {}

    def spawn(self, name: str, goal: str) -> AutonomousAgent:
        agent = AutonomousAgent(name, goal)
        self._agents[name] = agent
        return agent

    def run_all(self, max_steps: int = 5) -> dict:
        results = {}
        for name, agent in self._agents.items():
            results[name] = agent.run(max_steps)
        return results

    def status(self) -> dict:
        return {name: agent.plan.is_finished() for name, agent in self._agents.items()}


class OrchestrationModule:
    """Agent Orchestration sub-namespace exposed as agent.orchestration.*"""
    _orchestrator = AgentOrchestrator()

    @classmethod
    def spawn(cls, name: str, goal: str) -> AutonomousAgent:
        return cls._orchestrator.spawn(name, goal)

    @classmethod
    def run_swarm(cls, max_steps: int = 5) -> dict:
        return cls._orchestrator.run_all(max_steps)

    @classmethod
    def status(cls) -> dict:
        return cls._orchestrator.status()


# ---------------------------------------------------------------------------
# TOP-LEVEL AGENT MODULE
# ---------------------------------------------------------------------------

class AgentModule:
    """
    Sapphire AI Agent Architecture Standard Library — Top-level `agent` namespace.

    Sub-namespaces:
        agent.memory        — Short-term context & long-term vector/KV store
        agent.planning      — Plan decomposition & ReAct reasoning
        agent.tools         — Tool registration & security execution
        agent.permissions   — Security policies (strict, interactive, permissive)
        agent.autonomy      — Autonomous execution loop runner
        agent.orchestration — Multi-agent swarm coordinator
    """
    memory        = MemoryModule
    context       = ContextEngine
    planning      = PlanningModule
    tools         = ToolsModule
    permissions   = PermissionsModule
    autonomy      = AutonomyModule
    orchestration = OrchestrationModule

    @staticmethod
    def run(goal: str) -> dict:
        """Run full autonomous agent pipeline for a goal."""
        return AutonomyModule.run_loop(goal)

    @staticmethod
    def info() -> str:
        return (
            "=== Sapphire AI Agent Architecture ===\n"
            "  Pipelines    : Data → Training → Model → Reasoning → Memory → Planning → Tools → Autonomy\n"
            "  Sub-modules  : memory, planning, tools, permissions, autonomy, orchestration\n"
            "  LLM Backends : Ollama (Local), Groq API (Cloud Fallback), Offline Heuristics\n"
        )
