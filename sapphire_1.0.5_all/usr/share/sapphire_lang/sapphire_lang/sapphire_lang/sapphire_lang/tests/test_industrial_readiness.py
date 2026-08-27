import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from industrial import AgentLoop, PersistentStore, RetryPolicy, SandboxViolation, SemanticMemory, WorkspaceSandbox


class IndustrialReadinessTests(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
