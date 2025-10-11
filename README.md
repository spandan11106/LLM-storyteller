# 🎭 Welcome to LLM Storyteller! 🐉

✨ **Your Personal AI Dungeon Master Awaits!** ✨

Ever dreamed of having your very own Dungeon Master who never forgets a detail, creates amazing adventures on the fly, and brings NPCs to life with realistic emotions? Well, dream no more! 🌟

This magical application is like having a brilliant storyteller living in your computer - one who uses cutting-edge AI to weave incredible tales just for you. Whether you're a seasoned adventurer or completely new to storytelling games, this friendly AI will guide you through unforgettable journeys! 🗺️

## 📸 **See the Magic in Action!** ✨

<div align="center">

### 🎮 **Beautiful GUI Interface**
![LLM Storyteller GUI](demo/Photos/3.png)
*Experience storytelling through our gorgeous, modern interface with character tracking and immersive chat!*

### 🧠 **Memory System in Action** 
![Memory System Demo](demo/Photos/2.png)
*Watch as our legendary memory palace remembers every detail of your adventure!*

### 🎭 **Character & NPC Management**
![Character Management](demo/Photos/1.png)
*Create amazing characters and watch NPCs come to life with real emotions and relationships!*

</div>

## 🎬 **Watch the Demo Video!**

[![Watch the demo](https://img.shields.io/badge/Watch%20Demo%20Video-Click%20Here-blue?style=for-the-badge)](demo/Video/Video1.mp4)

*See LLM Storyteller in action with a full walkthrough of the magical interface and features!* 

---

## 🌟 What Makes This Adventure Special?

🎨 **Beautiful & Intuitive Interface**: A gorgeous, modern design that feels like stepping into a fantasy tavern! Built with love using customtkinter, featuring a cozy chat window and a magical sidebar that shows your character's journey.

🧙‍♂️ **Your AI Dungeon Master**: Powered by incredibly smart AI (Groq's llama-3.1-8b-instant) that creates stories so engaging, you'll forget you're talking to a computer! Every response is crafted just for your unique adventure.

🧠 **Never-Forget Memory System** (The Secret Sauce!):
    * 💭 **Recent Memory**: Keeps track of what just happened - like a sharp-eyed adventurer!
    * 🎬 **Scene Memory**: Automatically notices when scenes change and remembers the important bits
    * 🏛️ **Legendary Memory**: Like an ancient library, it remembers EVERYTHING important from your entire journey - no detail is ever truly lost!

💝 **Living, Breathing NPCs**: Every character you meet has real emotions and remembers how you treat them! Be kind to the tavern keeper, and they might give you a discount. Cross a merchant, and word might spread... The AI even notices when new characters appear and starts caring about them too!

⚔️ **Simple Yet Engaging Adventures**: No complicated dice rolls or confusing stats - just pure storytelling magic! Your character can be Healthy or Wounded, and quests unfold naturally through the power of narrative.

## 📋 What You'll Need for This Adventure

🐍 **Python 3.10 or newer** - Don't worry, it's free and easy to install!
📦 **A few magical dependencies** - We've made it super simple with our [`requirements.txt`](requirements.txt) spell book:
    * `groq` - The brain that powers your AI Dungeon Master
    * `python-dotenv` - Keeps your API key safe and sound
    * `customtkinter` - Makes everything look absolutely gorgeous
    * `networkx` - Helps track relationships between characters
    * `sentence-transformers` - The secret sauce for understanding context

## 🚀 Ready to Start Your First Adventure?

Don't worry - we'll guide you through every step! Even if you've never used Python before, you'll be adventuring in no time! 🎉

### Step 1: 🏠 Set up your adventure headquarters
This creates a cozy little space just for your storytelling app:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### Step 2: 📚 Gather your magical components
This installs all the special ingredients needed for the magic to work:
```bash
pip install -r requirements.txt
```

### Step 3: 🗝️ Get your secret key
Create a special file called `.env` in your project folder and add your Groq API key (don't worry, we'll help you get one!):
```text
GROQ_API_KEY=your_groq_api_key_here
```
💡 **Pro tip**: You can get a free Groq API key from https://groq.com - it's quick and totally free!

### Step 4: 🎪 Let the adventure begin!
```bash
python main.py
```
🎉 **That's it!** Your personal AI Dungeon Master is now ready to create amazing stories with you!

## 🧪 Testing the Magic (For the Curious Adventurers!)

We've built some really cool tests to make sure everything works perfectly! Think of these as quality assurance spells that verify our AI Dungeon Master is working at peak performance! 🎯

Our test suite is like a comprehensive adventure journal that checks:
- 🧠 **Memory Magic**: Including legendary "needle in haystack" tests where we hide important details in long stories to see if the AI remembers them!
- 😊 **NPC Heart & Soul**: Making sure every character's emotions and relationships feel real and consistent
- 📖 **Story Weaving**: Ensuring your adventures flow naturally and characters stay true to themselves  
- ⚡ **Lightning-Fast Performance**: Keeping response times snappy so the magic never breaks

### 🎭 Test All the Magic at Once
```bash
source venv/bin/activate
python run_tests.py all
```

### 🎯 Focus on Specific Enchantments
```bash
python run_tests.py memory      # Test the legendary memory system
python run_tests.py npc         # Check NPC emotions and relationships  
python run_tests.py story       # Verify story consistency magic
python run_tests.py performance # Ensure everything runs like lightning
```

📚 **Want the full testing spellbook?** Check out [`tests/README.md`](tests/README.md) for all the magical details!

## 🗺️ Your Adventure Map (Project Structure)

Here's where all the magic lives! A clean, at-a-glance map of the realm: 🔍

```text
LLM-storyteller/
├─ main.py
├─ storyteller/
│  ├─ core/
│  │  ├─ engine.py
│  │  ├─ character.py
│  │  ├─ memory.py
│  │  └─ npc.py
│  ├─ ui/
│  │  └─ gui.py
│  ├─ utils/
│  │  └─ llm.py
│  └─ config.py
├─ tests/
│  ├─ test_memory.py
│  ├─ test_npc_emotions.py
│  ├─ test_story_consistency.py
│  ├─ test_performance.py
│  └─ run_all_tests.py
├─ demo/
│  ├─ simple_proof.py
│  ├─ selection_proof.py
│  └─ terminal_memory_proof.py
├─ requirements.txt
└─ LICENSE
```

<details>
<summary><strong>Quick links to key files</strong> (click to expand)</summary>

- 🎪 [`main.py`](main.py) — Your gateway to adventure
- 🧠 [`storyteller/core/engine.py`](storyteller/core/engine.py) — Adventure orchestrator
- 🎨 [`storyteller/ui/gui.py`](storyteller/ui/gui.py) — Beautiful CustomTkinter interface
- 🛠️ [`storyteller/utils/llm.py`](storyteller/utils/llm.py) — LLM client bridge
- 🧪 [`tests/README.md`](tests/README.md) — Testing spellbook
- 🎯 [`run_tests.py`](run_tests.py) — Friendly test launcher
- 🎭 Demos: [`demo/simple_proof.py`](demo/simple_proof.py) · [`demo/selection_proof.py`](demo/selection_proof.py) · [`demo/terminal_memory_proof.py`](demo/terminal_memory_proof.py)

</details>

## 📜 Legal Scroll (License)

This entire magical kingdom is shared under the MIT License! That means you're free to use it, share it, modify it, and even build your own storytelling empire on top of it! Check out the [`LICENSE`](LICENSE) file for all the official details. 🤝✨