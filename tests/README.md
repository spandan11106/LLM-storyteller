# 🧪 Welcome to Our Magical Test Laboratory! ✨

🎭 **- **🌊 Narrative Continuity**: "Does the story flow naturally from one scene to the next?"
- **🌍 World State Consistency**: "Are there any magical contradictions in the world facts?"
- **💬 Dialogue Consistency**: "Do NPCs stay true to their personalities when they speak?"
- **⚖️ Consequence Tracking**: "Do actions have lasting effects that are remembered later?"

### 4. ⚡ Lightning Performance Tests (`test_performance.py`)
*Making sure the magic happens fast and efficiently!*

**🌟 Speed & Efficiency Tests:**
- **⏱️ Response Time Consistency**: "Are you always quick to respond, even during long adventures?"
- **💾 Memory Operation Speed**: "How fast can you search through thousands of memories?"
- **📈 Scalability Magic**: "Do you stay fast even with hundreds of conversations?"
- **👥 NPC Processing Efficiency**: "Does tracking multiple NPCs slow things down?"
- **🧠 Memory Usage Patterns**: "Are you efficient with computer memory as adventures grow?"uality Assurance Spellbook for Your AI Dungeon Master!** 🎭

Think of this as your personal quality inspector - a collection of magical tests that make sure your AI storyteller is working at peak performance! Every feature gets thoroughly tested to ensure your adventures are always amazing! 🌟

Whether you're a curious adventurer wanting to see how the magic works, or a fellow wizard contributing to the codebase, this guide will help you understand and use our comprehensive testing system! 🪄

## 🗺️ Your Test Adventure Map (Directory Structure)

### 🏛️ Main Test Palaces
- 🧠 `test_memory.py` - Tests the legendary memory palace (our secret sauce!)
- 💝 `test_npc_emotions.py` - Makes sure every NPC's heart beats true  
- 📖 `test_story_consistency.py` - Ensures your stories flow like epic novels
- ⚡ `test_performance.py` - Keeps everything lightning-fast and responsive
- 🛠️ `test_utils.py` - The magical toolkit that helps all other tests work

### 🎯 Specialized Test Chambers
- 🔍 `domain_test.py` - Quick health checks to make sure basics are working
- 🪶 `lightweight/` - Super efficient tests that barely use any API calls
  - `lightweight_test.py` - Complete testing without heavy internet usage
  - `README.md` - Guide to lightweight testing magic

### 🎪 Test Conductors
- 🎭 `run_all_tests.py` - The grand orchestrator of all test adventures

## 🎪 Test Adventure Suites (What Magic We're Testing!)

### 1. 🧠 Memory Palace Tests (`test_memory.py`)
*Testing the legendary three-tier memory system that never forgets!*

**🌟 Magical Tests Include:**
- **📝 Short-term Memory**: "Did you remember what just happened?" 
- **🔍 Needle in Haystack**: The famous test! We hide important details among 75+ conversations and see if our AI can find them later (this is our secret sauce!)
- **💎 Fact Extraction**: "Can you automatically spot the important stuff in conversations?"
- **💾 Memory Persistence**: "Do you remember everything when you wake up from sleep?"
- **🎯 Search Accuracy**: "When I ask for something specific, do you find exactly what I need?"

### 2. 💝 NPC Heart & Soul Tests (`test_npc_emotions.py`)  
*Making sure every character feels real and remembers how you treat them!*

**🌟 Emotional Intelligence Tests:**
- **😊 Emotion Detection**: "Do you notice new NPCs and start caring about them?"
- **💕 Relationship Growth**: "Do relationships change based on how players treat NPCs?"
- **🎭 Emotion Consistency**: "Do angry NPCs act angry, and friendly ones act friendly?"
- **👥 Multiple NPC Juggling**: "Can you track several characters' emotions at once?"
- **🧠 Memory Integration**: "Do NPCs remember past interactions through the memory system?"

### 3. 📖 Epic Story Consistency Tests (`test_story_consistency.py`)
*Ensuring your adventures flow like masterfully written novels!*

**🌟 Storytelling Magic Tests:**
- **🎭 Character Trait Consistency**: "Does the brave knight stay brave? Does the sneaky rogue stay sneaky?"
- **🌊 Narrative Continuity**: "Does the story flow naturally from one scene to the next?"
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

## 🚀 Ready to Run Some Tests? (Let's Test the Magic!)

### 🎭 Run All the Amazing Tests at Once
```bash
# Wake up your magical environment
source venv/bin/activate

# Test ALL the magic in one epic run!
python run_tests.py all

# Or use the detailed test conductor
python -m tests.run_all_tests
```

### 🎯 Focus on Specific Magic Schools
```bash
# Test just the legendary memory palace
python run_tests.py memory

# Test only NPC hearts and emotions
python run_tests.py npc

# Test only the epic story consistency
python run_tests.py story

# Test only lightning-fast performance
python run_tests.py performance
```

### 🌟 Quick Testing (Just Show Me Results!)
```bash
python run_tests.py all --no-save
```

## 📊 Test Results (Understanding Your Magic Report Card!)

### 📝 What You'll Get
- 📄 `test_results_YYYYMMDD_HHMMSS.json`: All the detailed results in computer-friendly format
- 📖 `test_report_YYYYMMDD_HHMMSS.txt`: Beautiful human-readable report that tells the whole story

### 🎯 Decoding Your Adventure Report Card

**🏆 Overall Magic Score**: How much of your magic is working perfectly
- **90%+**: ✅ **LEGENDARY!** Your AI is absolutely magnificent!
- **70-89%**: 🟡 **EXCELLENT!** Working beautifully with minor quirks
- **50-69%**: ⚠️ **GOOD!** Solid foundation, some areas need attention
- **<50%**: ❌ **NEEDS LOVE!** Time for some magical debugging

**🔍 Important Magic Metrics to Watch:**

**🧠 Memory Palace Performance:**
- 🎯 Needle retrieval success rate (Can find hidden treasures in long conversations?)
- 💎 Fact extraction count (Automatically spots important details?)
- 🔍 Search accuracy percentage (Finds exactly what you're looking for?)

**💝 NPC Heart Monitoring:**
- 😊 Emotion detection rate (Notices new NPCs and starts caring about them?)
- 💕 Relationship logic accuracy (Tracks how NPCs feel about players?)
- 🎭 Emotion-score alignment (Happy NPCs act happy, grumpy ones act grumpy?)

**📖 Epic Story Quality:**
- 🎭 Character trait consistency (Heroes stay heroic, villains stay villainous?)
- 🌊 Narrative continuity (Story flows like a great novel?)
- 🌍 World state consistency (No magical contradictions in the world?)

**⚡ Lightning Performance:**
- ⏱️ Average response time (Should be under 10 seconds for great user experience)
- 💾 Memory per conversation (Should be under 1MB per chat for efficiency)
- 📈 Scalability trends (Should stay fast even with lots of conversations)

## 🔍 The Famous "Needle in Haystack" Test (Our Signature Challenge!)

*The ultimate test of long-term memory magic - can your AI find a tiny detail hidden in a mountain of conversations?*

🎯 **How This Epic Challenge Works:**

1. **🏗️ Building the Haystack**: Creates 75+ normal conversations full of everyday adventure stuff
2. **💎 Hiding the Needle**: Sneaks in something super important (like "Crystal of Eternal Flame") at a random spot
3. **📚 Adding More Hay**: Piles on even more conversations to really bury that precious detail
4. **🔍 The Great Search**: Tests three different ways to find the needle:
   - 🎯 Direct keyword hunting ("Find the crystal!")
   - 🧠 Smart semantic searching (understanding meaning, not just words)
   - 💬 Natural conversation ("Tell me about any magical items you remember")

**🏆 Victory Condition**: Your AI should find that needle no matter how deep it's buried! This proves your memory system is truly legendary! ✨

## ⚠️ API Rate Limiting (Important Note for Fellow Wizards!)

**🚨 Heads up!** Our tests are thorough, which means they chat with the AI a LOT! If you see 429 (Too Many Requests) errors:

1. **⏰ Take a Magic Break**: Groq has rate limits - grab some coffee and wait a few minutes between test runs
2. **📏 Scale Down the Challenge**: Modify `haystack_size` in `test_memory.py` (line 74) to a smaller number for faster testing
3. **🎭 Mock Mode**: For development, consider implementing pretend responses to avoid API calls entirely

## ⚙️ Test Configuration (Setting Up Your Testing Magic!)

### 🔑 Environment Variables (Your Secret Ingredients)
- `GROQ_API_KEY`: Required for LLM functionality (get yours free at groq.com!)
- `MEMORY_SAVE_PATH`: Where test memories live (we handle this automatically, no worries!)

### 🧠 Memory Configuration (Smart Isolation)
Tests create their own little memory worlds so they don't mess with your real adventures!

### 📏 Performance Thresholds (What "Good" Looks Like)
You can adjust these in individual test files:
- ⏱️ Response time: 10 seconds (fast enough for great user experience)
- 💾 Memory per conversation: 1MB (efficient storage)
- 🎯 Search accuracy: 70% (finds what you're looking for most of the time)
- 📊 Consistency rates: 60-70% depending on test (pretty darn consistent!)

## 🛠️ Adding New Tests (For Fellow Wizards Who Want to Contribute!)

### 🏗️ Test Structure (The Magic Pattern)
```python
def test_new_feature(self, engine):
    """🎯 Test description - what amazing thing are we checking?"""
    
    def actual_test():
        # ✨ The actual test magic happens here
        result = perform_test_actions()
        return {
            'metric1': value1,
            'metric2': value2,
            'success_condition': condition_met
        }
    
    self.results['test_name'] = run_test_safely(actual_test)
```

### 🌟 Best Practices (How to Write Legendary Tests)
1. 🛡️ Use `run_test_safely()` wrapper for error handling magic
2. 📊 Return structured results with meaningful metrics
3. ✅ Include clear success/failure conditions
4. ⏱️ Use small delays (`time.sleep(0.01)`) between API calls to be nice
5. 🧹 Clean up resources in test teardown (leave no trace!)

## 🔧 Troubleshooting (When Magic Goes Wonky!)

### 😅 Common Magical Mishaps

**📦 Import Errors**: Your magical environment needs to be awakened properly:
```bash
source venv/bin/activate
pip install -r requirements.txt
pip install psutil  # Special ingredient for performance tests
```

**🔑 API Key Issues**: Make sure your `.env` file has a valid `GROQ_API_KEY` (get one free at groq.com!)

**⏰ Rate Limiting**: The AI is popular! Reduce test scale or wait between runs

**💾 Memory Errors**: Your computer needs more memory, or reduce conversation count in tests

**⏱️ Timeout Errors**: Increase timeout values in `storyteller/utils/llm.py` for patience

### 🐛 Debug Mode (For Detective Work)
Add magical debug prints in test files to trace what's happening:
```python
print(f"🔍 Debug: Current state = {engine.get_npc_states()}")
```

## 🤝 Contributing (Join Our Circle of Testing Wizards!)

When adding new magical features to the storytelling engine:

1. **✨ Add Corresponding Tests** - Every new spell needs a test to prove it works!
2. **📏 Update Success Criteria** - If performance changes, update what "good" looks like
3. **🧪 Test Edge Cases** - What happens when things go wrong? Test those scenarios too!
4. **📚 Document Expected Behavior** - Write clear descriptions of what tests should do
5. **🌟 Run Full Test Suite** - Make sure your changes don't break existing magic before sharing

Our test suite ensures the storytelling engine maintains its legendary quality across:
- 🧠 **Memory and Context Magic** - Never forgetting important details
- 😊 **NPC Emotional Intelligence** - Every character feels real and alive
- 📖 **Story Coherence and Consistency** - Adventures that flow like masterful novels
- ⚡ **Performance and Scalability** - Fast, responsive magic that scales beautifully

🎉 **Welcome to the adventure!** Your contributions help make storytelling magic even more amazing! ✨