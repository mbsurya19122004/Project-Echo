# Project Echo

Project Echo is an AI-powered desktop assistant built with **Python** and **LangChain** that allows you to control your computer using natural language. It can execute terminal commands, automate tasks, manage files, and perform intelligent tool-based actions while maintaining conversational context and applying safety checks for sensitive operations.

> **Current Status:** Early Development

---

## ✨ Features

- 🤖 Natural language desktop assistant
- 🐍 Built with Python and LangChain
- 🧠 Powered by **Gemma 4** via **Ollama**
- 💻 Execute terminal commands through AI
- 📂 File and system management
- 🛡️ Safety checks for potentially dangerous operations
- 🧠 Conversational context and tool-based reasoning
- 🐧 Optimized for **Hyprland** (currently the primary supported platform)

---

## 🚀 Planned Features

- 🎤 Voice interaction
- 📱 Mobile companion app
- 🪟 Windows support
- 🖥️ Support for additional Linux desktop environments (GNOME, KDE, XFCE, Cinnamon, etc.)
- 🧩 Plugin system
- 🧠 Persistent memory
- ⚡ More desktop automation tools
- 🌐 RAG / Knowledge integration

---

# 📋 Requirements

- Python **3.10+**
- Git
- **Ollama**
- **Gemma 4** model

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/mbsurya19122004/Project-Echo.git
cd Project-Echo
```

---

## 2. Install Ollama

### Linux

Install Ollama:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

```bash
ollama pull gemma4
```

Verify the installation:

```bash
ollama list
```

You should see:

```
gemma4
```

---

## 3. Create a virtual environment

```bash
python -m venv venv
```

---

## 4. Activate the virtual environment

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 6. Run Project Echo

```bash
python main.py
```

---

# 🏗️ Architecture

Project Echo combines several technologies to provide intelligent desktop automation.

- **LangChain** for agent reasoning
- **Gemma 4** running locally through **Ollama**
- **Python tool system** for desktop control
- **Conversation memory** for contextual interactions

---

# 🖥️ Platform Support

| Platform | Status |
|----------|--------|
| Hyprland | ✅ Fully Supported |
| Other Linux Desktop Environments | 🚧 Planned |
| Windows | 🚧 Planned |
| macOS | ❌ Not Planned |

---

# ⚠️ Disclaimer

Project Echo can execute system commands and interact with your operating system.

Although safety checks are implemented for potentially destructive actions, AI-generated commands may still produce unintended results. Always review commands before allowing them to execute.

**Use Project Echo at your own risk.**

---

# 📌 Roadmap

- [x] LangChain-based desktop assistant
- [x] Hyprland support
- [ ] Voice interaction
- [ ] Wake word detection
- [ ] Mobile companion application
- [ ] Windows support
- [ ] Support for additional Linux desktop environments
- [ ] Plugin system
- [ ] Persistent memory
- [ ] Additional automation tools
- [ ] RAG / Knowledge integration
- [ ] Improved long-term context handling

---

# 🤝 Contributing

Contributions are welcome!

If you'd like to contribute:

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push your branch.
5. Open a Pull Request.

Bug reports, feature requests, and ideas are always appreciated.

---

# 📄 License

This project is licensed under the **MIT License**.

See the **LICENSE** file for more information.

---

## ⭐ Support

If you find Project Echo useful, consider giving the repository a ⭐ on GitHub.

It helps others discover the project and motivates future development.
