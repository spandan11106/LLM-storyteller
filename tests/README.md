# Storytelling Engine Test Suite

A comprehensive test suite for the AI-powered storytelling engine with long-term memory, NPC emotions, and story consistency features.

## Directory Structure

### Main Test Suites
- `test_memory.py` - Memory system tests
- `test_npc_emotions.py` - NPC emotion and relationship tests  
- `test_story_consistency.py` - Story coherence tests
- `test_performance.py` - Performance benchmarks
- `test_utils.py` - Shared testing utilities

### Specialized Tests
- `domain_test.py` - Quick domain verification tests
- `lightweight/` - Lightweight test suite for minimal API usage
  - `lightweight_test.py` - Comprehensive offline testing
  - `README.md` - Lightweight testing documentation

### Test Runners
- `run_all_tests.py` - Main test runner for all domains

## Test Suites

### 1. Memory Tests (`test_memory.py`)
Tests the memory system's ability to store, retrieve, and maintain conversational context.

**Key Tests:**
- **Short-term Memory**: Tests recent conversation recall
- **Needle in Haystack**: 🔍 Tests long-term memory by hiding important information among 75+ conversations and attempting retrieval
- **Fact Extraction**: Tests automatic extraction of important facts from conversations
- **Memory Persistence**: Tests if memory survives application restarts
- **Search Accuracy**: Tests precision of memory search functionality

### 2. NPC Emotion Tests (`test_npc_emotions.py`)
Tests the NPC emotion tracking and relationship system.

**Key Tests:**
- **Emotion Detection**: Tests if NPCs are detected and emotions tracked
- **Relationship Progression**: Tests relationship score changes over multiple interactions
- **Emotion Consistency**: Tests if emotions align with relationship scores
- **Multiple NPC Interactions**: Tests handling of multiple NPCs simultaneously
- **Memory Integration**: Tests if NPC states integrate with the memory system

### 3. Story Consistency Tests (`test_story_consistency.py`)
Tests narrative coherence and character behavior consistency.

**Key Tests:**
- **Character Trait Consistency**: Tests if character traits remain consistent
- **Narrative Continuity**: Tests story continuity across interactions
- **World State Consistency**: Tests for contradictions in world facts
- **Dialogue Consistency**: Tests NPC personality consistency in dialogue
- **Consequence Tracking**: Tests if actions have remembered consequences

### 4. Performance Tests (`test_performance.py`)
Tests system performance, timing, and scalability.

**Key Tests:**
- **Response Time Consistency**: Tests if response times remain stable
- **Memory Operation Performance**: Tests speed of memory operations
- **Scalability**: Tests performance degradation with conversation count
- **NPC Processing Overhead**: Tests computational cost of NPC processing
- **Memory Usage Growth**: Tests memory consumption patterns

## Running Tests

### Run All Tests
```bash
# Activate virtual environment
source venv/bin/activate

# Run comprehensive test suite
python run_tests.py all

# Or use the detailed runner
python -m tests.run_all_tests
```

### Run Individual Test Suites
```bash
# Memory tests only
python run_tests.py memory

# NPC emotion tests only
python run_tests.py npc

# Story consistency tests only
python run_tests.py story

# Performance tests only
python run_tests.py performance
```

### Run Without Saving Results
```bash
python run_tests.py all --no-save
```

## Test Results

### Output Files
- `test_results_YYYYMMDD_HHMMSS.json`: Detailed results in JSON format
- `test_report_YYYYMMDD_HHMMSS.txt`: Human-readable comprehensive report

### Interpreting Results

**Overall Score**: Percentage of tests passed
- **90%+**: ✅ Excellent
- **70-89%**: 🟡 Good
- **50-69%**: ⚠️ Needs Improvement
- **<50%**: ❌ Critical Issues

**Key Metrics:**

**Memory Tests:**
- Needle retrieval success rate (should find hidden information)
- Fact extraction count (should automatically extract key facts)
- Search accuracy percentage (should return relevant results)

**NPC Tests:**
- Emotion detection rate (should recognize NPCs in text)
- Relationship logic accuracy (should track sentiment correctly)
- Emotion-score alignment (emotions should match relationship scores)

**Story Tests:**
- Character trait consistency (should maintain personality)
- Narrative continuity (should remember previous events)
- World state consistency (should avoid contradictions)

**Performance Tests:**
- Average response time (should be under 10 seconds)
- Memory per conversation (should be under 1MB per conversation)
- Scalability trends (performance shouldn't degrade significantly)

## Needle in Haystack Test

The signature test of long-term memory capability:

1. **Setup**: Creates 75+ conversations with filler content
2. **Needle Insertion**: Hides important information (e.g., "Crystal of Eternal Flame") at a random position
3. **Haystack Building**: Adds more filler conversations after the needle
4. **Retrieval Test**: Attempts to find the needle using:
   - Direct keyword search
   - Semantic search
   - Conversational queries about magical items

**Success Criteria**: System should be able to retrieve the needle information despite being buried in many irrelevant conversations.

## API Rate Limiting

⚠️ **Important**: Tests make many API calls to Groq. If you encounter 429 (Too Many Requests) errors:

1. **Wait**: Groq has rate limits - wait a few minutes between test runs
2. **Reduce Scale**: Modify `haystack_size` in `test_memory.py` (line 74) to a smaller number
3. **Mock Mode**: For development, consider implementing mock responses

## Test Configuration

### Environment Variables
- `GROQ_API_KEY`: Required for LLM functionality
- `MEMORY_SAVE_PATH`: Directory for test memory storage (automatically managed)

### Memory Configuration
Tests create isolated temporary directories to avoid contaminating production memory.

### Performance Thresholds
Configurable in individual test files:
- Response time: 10 seconds
- Memory per conversation: 1MB
- Search accuracy: 70%
- Consistency rates: 60-70% depending on test

## Adding New Tests

### Test Structure
```python
def test_new_feature(self, engine):
    """Test description"""
    
    def actual_test():
        # Test implementation
        result = perform_test_actions()
        return {
            'metric1': value1,
            'metric2': value2,
            'success_condition': condition_met
        }
    
    self.results['test_name'] = run_test_safely(actual_test)
```

### Best Practices
1. Use `run_test_safely()` wrapper for error handling
2. Return structured results with metrics
3. Include success/failure conditions
4. Use small delays (`time.sleep(0.01)`) between API calls
5. Clean up resources in test teardown

## Troubleshooting

### Common Issues

**Import Errors**: Ensure virtual environment is activated and packages installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
pip install psutil  # For performance tests
```

**API Key Issues**: Ensure `.env` file contains valid `GROQ_API_KEY`

**Rate Limiting**: Reduce test scale or wait between runs

**Memory Errors**: Increase system memory or reduce conversation count in tests

**Timeout Errors**: Increase timeout values in `storyteller/utils/llm.py`

### Debug Mode
Add debug prints in test files to trace execution:
```python
print(f"Debug: Current state = {engine.get_npc_states()}")
```

## Contributing

When adding new features to the storytelling engine:

1. **Add corresponding tests** in the appropriate test file
2. **Update success criteria** if performance characteristics change
3. **Test edge cases** and error conditions
4. **Document expected behavior** in test docstrings
5. **Run full test suite** before committing changes

The test suite ensures the storytelling engine maintains quality across:
- 🧠 Memory and context management
- 😊 NPC emotional intelligence
- 📖 Story coherence and consistency  
- ⚡ Performance and scalability