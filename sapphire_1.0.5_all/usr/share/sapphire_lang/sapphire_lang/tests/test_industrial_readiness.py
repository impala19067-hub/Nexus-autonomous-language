import os
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from industrial import AgentLoop, CodebaseIndex, LocalCluster, PersistentStore, RetryPolicy, SandboxViolation, SemanticMemory, WorkspaceSandbox
from src.stdlib.agent_mod import AgentModule, PlanningModule, ToolsModule
from src.stdlib.ml_mod import GPUModule, Tensor, TorchTrainingModule


class IndustrialReadinessTests(unittest.TestCase):
    def test_planning_uses_ai_generated_steps(self):
        response = json.dumps({"steps": [
            {"description": "Inspect deployment logs", "tool": "fs"},
            {"description": "Run health checks", "tool": "os"},
            {"description": "Publish the incident report", "tool": "notify"},
        ]})
        with patch("src.stdlib.ai_mod.AIModule.prompt", return_value=response):
            plan = PlanningModule.create_plan("respond to incident")
        self.assertEqual(plan.source, "AI-generated")
        self.assertEqual([task.description for task in plan.tasks], [
            "Inspect deployment logs", "Run health checks", "Publish the incident report"
        ])
        self.assertEqual([task.tool_name for task in plan.tasks], ["fs", "os", "notify"])

    def test_agent_executes_registered_tool(self):
        calls = []
        ToolsModule.register("test_tool", "records execution", lambda **kwargs: calls.append(kwargs) or "ok")
        plan_response = json.dumps({"steps": [{"description": "perform test", "tool": "test_tool"}]})
        action_response = json.dumps({"thought": "Use the test tool", "action": "test_tool", "args": {"value": 7}})
        with patch("src.stdlib.ai_mod.AIModule.prompt", side_effect=[plan_response, action_response]):
            agent = AgentModule.autonomy.create_agent("test", "verify tool execution")
            report = agent.run(1)
        self.assertEqual(calls, [{"value": 7}])
        self.assertTrue(report["finished"])
        self.assertEqual(agent.plan.tasks[0].result, "ok")

    def test_agent_marks_tool_failure(self):
        ToolsModule.register("failing_tool", "fails", lambda **_kwargs: (_ for _ in ()).throw(ValueError("tool down")))
        plan_response = json.dumps({"steps": [{"description": "perform failing test", "tool": "failing_tool"}]})
        action_response = json.dumps({"thought": "Use the failing tool", "action": "failing_tool", "args": {}})
        with patch("src.stdlib.ai_mod.AIModule.prompt", side_effect=[plan_response, action_response]):
            agent = AgentModule.autonomy.create_agent("test", "verify failure")
            report = agent.run(1)
        self.assertFalse(report["finished"])
        self.assertEqual(agent.plan.tasks[0].status, "failed")
        self.assertIn("tool down", agent.plan.tasks[0].result)

    def test_tensor_matmul_returns_correct_result(self):
        result = Tensor([[1, 2], [3, 4]]).matmul(Tensor([[5, 6], [7, 8]]))
        self.assertEqual(result.tolist(), [[19.0, 22.0], [43.0, 50.0]])

    def test_cuda_transfer_does_not_fake_availability(self):
        if not GPUModule.is_available():
            with self.assertRaises(RuntimeError):
                GPUModule.to_device(Tensor([1, 2]), "cuda:0")

    def test_sandbox_resolves_workspace_file(self):
        with tempfile.TemporaryDirectory() as directory:
            sandbox = WorkspaceSandbox(directory)
            self.assertEqual(sandbox.resolve('logs/app.txt').parent, Path(directory).resolve() / 'logs')

    def test_sandbox_rejects_parent_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(SandboxViolation):
                WorkspaceSandbox(directory).resolve('../outside.txt')

    def test_sandbox_rejects_absolute_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(SandboxViolation):
                WorkspaceSandbox(directory).resolve(str(Path(directory).parent / 'outside.txt'))

    def test_sandbox_writes_and_reads_utf8(self):
        with tempfile.TemporaryDirectory() as directory:
            sandbox = WorkspaceSandbox(directory)
            sandbox.write_text('data/result.txt', 'Sapphire ✓')
            self.assertEqual(sandbox.read_text('data/result.txt'), 'Sapphire ✓')

    def test_sandbox_allows_explicit_command(self):
        with tempfile.TemporaryDirectory() as directory:
            result = WorkspaceSandbox(directory, [sys.executable]).run(sys.executable, ['-c', 'print("ok")'])
            self.assertEqual(result.stdout.strip(), 'ok')
            self.assertEqual(result.returncode, 0)

    def test_sandbox_denies_unlisted_command(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(SandboxViolation):
                WorkspaceSandbox(directory, ['definitely-not-allowed']).run(sys.executable, ['-c', 'pass'])

    def test_persistent_store_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / 'state.sqlite'
            with PersistentStore(database) as store:
                store.put('config', {'retries': 3, 'enabled': True})
            with PersistentStore(database) as reopened:
                self.assertEqual(reopened.get('config'), {'retries': 3, 'enabled': True})

    def test_persistent_store_default_and_delete(self):
        with tempfile.TemporaryDirectory() as directory, PersistentStore(Path(directory) / 'state.sqlite') as store:
            self.assertEqual(store.get('missing', 42), 42)
            store.put('key', 'value')
            self.assertTrue(store.delete('key'))
            self.assertFalse(store.delete('key'))
            self.assertIsNone(store.get('key'))

    def test_persistent_store_updates_atomically(self):
        with tempfile.TemporaryDirectory() as directory, PersistentStore(Path(directory) / 'state.sqlite') as store:
            store.put('counter', 1)
            store.put('counter', 2)
            self.assertEqual(store.get('counter'), 2)

    def test_memory_retrieves_relevant_document(self):
        with tempfile.TemporaryDirectory() as directory, SemanticMemory(Path(directory) / 'memory.sqlite') as memory:
            memory.remember('incident', 'database connection timeout during backup', 'severity=high')
            memory.remember('deploy', 'frontend deployment completed successfully', 'severity=low')
            self.assertEqual(memory.retrieve('database timeout')[0]['key'], 'incident')

    def test_memory_builds_context(self):
        with tempfile.TemporaryDirectory() as directory, SemanticMemory(Path(directory) / 'memory.sqlite') as memory:
            memory.remember('one', 'disk capacity warning')
            self.assertIn('disk capacity warning', memory.context('disk warning'))

    def test_memory_forget_removes_document(self):
        with tempfile.TemporaryDirectory() as directory, SemanticMemory(Path(directory) / 'memory.sqlite') as memory:
            memory.remember('incident', 'service outage')
            memory.forget('incident')
            self.assertEqual(memory.retrieve('outage'), [])

    def test_agent_recovers_then_succeeds(self):
        state = {'attempts': 0, 'recoveries': 0}

        def action():
            state['attempts'] += 1
            if state['attempts'] < 3:
                raise ValueError('temporary')
            return 'done'

        def recover(_error, _attempt):
            state['recoveries'] += 1

        loop = AgentLoop(RetryPolicy(3, 0))
        result = loop.run(action, recover)
        self.assertEqual(result, 'done')
        self.assertEqual(state['recoveries'], 2)
        self.assertEqual([event['event'] for event in loop.events], ['attempt', 'failure', 'attempt', 'failure', 'attempt', 'success'])

    def test_agent_failure_is_bounded(self):
        with self.assertRaises(RuntimeError):
            AgentLoop(RetryPolicy(2, 0)).run(lambda: (_ for _ in ()).throw(ValueError('permanent')))

    def test_agent_rejects_invalid_policy(self):
        with self.assertRaises(ValueError):
            AgentLoop(RetryPolicy(0))

    def test_local_cluster_executes_ordered_work(self):
        cluster = LocalCluster(workers=2)
        self.assertEqual(cluster.map(lambda value: value * 2, [3, 1, 2]), [6, 2, 4])
        self.assertEqual(cluster.status()["distributed"], False)

    def test_local_cluster_rejects_invalid_worker_count(self):
        with self.assertRaises(ValueError):
            LocalCluster(workers=-1)

    def test_torch_backend_reports_optional_availability(self):
        self.assertIsInstance(TorchTrainingModule.available(), bool)

    def test_codebase_index_returns_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "service.sp"
            path.write_text("fn backup_database() { print(\"backup\"); }", encoding="utf-8")
            index = CodebaseIndex(directory)
            self.assertGreater(index.rebuild(), 0)
            result = index.search("backup database")
            self.assertEqual(result[0]["source"], "service.sp")
            self.assertIn("backup_database", result[0]["content"])


if __name__ == '__main__':
    unittest.main()
