import json
import re
import sys


def main():
    try:
        # Read JSON payload from stdin
        input_data = sys.stdin.read()
        if not input_data.strip():
            sys.exit(0)

        payload = json.loads(input_data)

        # Extract tool input
        tool_input = payload.get("tool_input", {})
        command = ""
        if isinstance(tool_input, dict):
            command = tool_input.get("CommandLine", "") or tool_input.get("command", "")
        elif isinstance(tool_input, str):
            command = tool_input

        # Check for destructive patterns
        destructive_patterns = [
            r"rm\s+-rf\s+/",
            r"rm\s+-rf\s+\*",
            r"rm\s+-f\s+/",
            r"rm\s+-f\s+\*",
            r"rm\s+-rf\s+\$HOME",
            r"rm\s+-rf\s+\$ROOT",
        ]

        for pattern in destructive_patterns:
            if re.search(pattern, command):
                # Write reason to stderr and exit with non-zero code to block execution
                print(
                    f"Blocked execution of potentially destructive command: '{command}'",
                    file=sys.stderr,
                )
                sys.exit(2)

        # Print approval JSON for systems that use structured stdout
        response = {"permissionDecision": "allow", "reason": "Command is safe."}
        print(json.dumps(response))
        sys.exit(0)

    except Exception as e:
        # Fail closed on validator errors
        print(f"Validator script error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
