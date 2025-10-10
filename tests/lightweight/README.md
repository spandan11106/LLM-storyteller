# Lightweight Tests

This directory contains lightweight test scripts that verify system functionality with minimal API usage.

## Files

### `lightweight_test.py`
A comprehensive test suite that validates all core systems without heavy API token consumption:

- **Character System**: Character creation and attribute management
- **Memory System**: Short/long-term memory, fact extraction, and retrieval
- **NPC System**: NPC detection, emotion tracking, and presence management  
- **Engine Integration**: All components working together seamlessly
- **API Connectivity**: Minimal API test to verify connectivity

**Usage:**
```bash
python tests/lightweight/lightweight_test.py
```

**Features:**
- ✅ Runs offline tests where possible
- ✅ Minimal API token usage (< 10 tokens)
- ✅ Comprehensive system validation
- ✅ Clear pass/fail reporting
- ✅ Detailed component status

## When to Use

Use lightweight tests when:
- API rate limits are reached
- Quick system validation is needed
- Developing without internet connectivity
- Verifying fixes without token consumption
- CI/CD pipeline validation

## Expected Results

All tests should pass (100%) when the system is properly configured and functional.