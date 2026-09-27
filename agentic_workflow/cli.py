import json
import sys

from agentic_workflow.core import Workflow, sample_database


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python -m agentic_workflow.cli 'question'", file=sys.stderr)
        return 2
    db = sample_database()
    try:
        print(json.dumps(Workflow(db).run(sys.argv[1]), indent=2))
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
