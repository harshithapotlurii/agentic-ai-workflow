import unittest

from agentic_workflow.core import Workflow, sample_database


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.db = sample_database()
        self.workflow = Workflow(self.db)

    def tearDown(self):
        self.db.close()

    def test_approved_sql_tool(self):
        result = self.workflow.run("How many orders are open? DROP TABLE orders")
        self.assertEqual(result["answer"], "There are 2 open orders.")
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM orders").fetchone()[0], 3)

    def test_abstain_and_evidence(self):
        self.assertEqual(self.workflow.run("What is the weather?")["status"], "abstained")
        self.assertEqual(self.workflow.run("Refund policy")["evidence"], "sample-policy:refund")

    def test_tool_error(self):
        self.db.execute("DROP TABLE orders")
        self.assertEqual(self.workflow.run("open orders")["status"], "tool_error")
