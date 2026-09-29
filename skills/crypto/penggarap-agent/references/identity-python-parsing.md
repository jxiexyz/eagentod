# Parsing Airdrop Identity File (`airdrop_identity.py`)

## The Pitfall
Attempting to read `airdrop_identity.py` as JSON will fail because it contains Python dictionary syntax, not pure JSON. For example, trying to load it with `json.load(open("/home/ubuntu/airdrop_identity.py", "r").read())` or `cat airdrop_identity.py | jq` will break due to trailing commas, single quotes, or Python comments.

## The Solution
Treat `airdrop_identity.py` as a Python module, not a JSON file.

Import the `IDENTITY` dictionary from it dynamically:

```python
import sys
sys.path.append("/home/ubuntu")
from airdrop_identity import IDENTITY

print(IDENTITY["main"]["evm_wallet"])
print(IDENTITY["main"]["x_handle"])
```

**Key Fields Available in `IDENTITY["main"]`:**
- `evm_wallet` (NOT `evm_address`)
- `x_handle`
- `sol_wallet`
- `email`