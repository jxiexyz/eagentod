# X Action & Follow: Use x_native.py (rettiwt-api is DEPRECATED)

⚠️ **`rettiwt-api` is DEAD** because X permanently removed REST API v1.1. Do NOT use `new Rettiwt()` in Node.js.

## The Modern Solution: `x_native.py`

Execute follows directly via terminal or MCP tool:

### 1. Via MCP Tool (in Agent SOP)
```python
x_action(action="follow", target_id="username_or_numeric_id")
```

### 2. Via CLI (Python)
```bash
python3 ~/.hermes/scripts/x_native.py follow <target_username_or_id>
```

### 3. Verification
```bash
python3 ~/.hermes/scripts/x_native.py whoami
```