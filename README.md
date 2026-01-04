# Clover Theater Automation Script (Legacy Prototype)

> An early-stage Python automation script for the Android game *Clover Theater* (四叶草剧场), utilizing ADB, OpenCV, and OCR for autonomous dungeon clearing.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![OpenCV](https://img.shields.io/badge/Computer_Vision-OpenCV-green)
![Status](https://img.shields.io/badge/Status-Prototype-orange)

## 📖 Background
This project represents the **initial prototype** of my research into game automation. It served as the foundation for my later work on **Finite State Machine (FSM)** based agents. While the logic here is procedural, it implements key technologies like **ADB-based control**, **Template Matching**, and **Cloud OCR** for decision making.

*Note: This repository is archived for educational purposes and demonstrates the evolution of my automation frameworks.*

## ⚙️ Core Mechanics

### 1. Computer Vision Navigation
Instead of relying on fixed coordinates, the script dynamically locates interactive elements (Battle nodes, Elite bosses, Chests) using **OpenCV Template Matching**.
- **Multi-Scale Search:** Implemented `match_tpl_loc_multi` to handle different rendering scales.
- **Color Verification:** Combined Grayscale matching with RGB verification to reduce false positives in complex UI environments.

### 2. Intelligent Event Handling (OCR)
The script integrates **Baidu OCR API** to read dynamic text events in the game (e.g., "Unknown Crystal" events).
- **Process:** Screenshot -> Text Recognition -> JSON Config Lookup -> Optimal Choice Selection.
- This allows the bot to make "smart" decisions rather than random clicking.

### 3. ADB Control Wrapper
Uses a custom `ADBShell` wrapper to communicate with Android emulators, handling touch events, swipes, and screen capturing efficiently.

## 🛠️ Tech Stack
* **Python 3.x**
* **OpenCV (cv2):** Image recognition and template matching.
* **ADB (Android Debug Bridge):** Device interaction.
* **Baidu OCR API:** Text extraction for event logic.
* **NumPy:** Image array processing.

## 📂 Project Structure
```text
├── CloverYggdrasill.py  # Main logic loop (Navigation, Battle, Loot)
├── ADBShell.py          # Wrapper for ADB commands (Touch, Swipe, Screencap)
├── img_utils.py         # OpenCV helper functions
├── baidu_ocr.py         # Cloud OCR implementation
├── find_coordinate.py   # Helper script to find UI coordinates on emulator 
├── config/              # Configuration files (Templates, Event logic JSON)
└── resource/            # Image templates for UI matching
```

## 🚀 Evolution

This script utilizes a **procedural `while-loop` architecture** to handle game states.

> **Evolution:** In my subsequent projects, this logic was refactored into a **Finite State Machine (FSM)** pattern to handle more complex, non-linear workflows and exception handling (Self-Healing), as seen in my [Visual Automation & RPA Framework](https://github.com/ChineseBeanLin/python-automation-portfolio).

---

*Author: Han Lin*