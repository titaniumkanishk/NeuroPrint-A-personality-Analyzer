# NeuroPrint — Advanced Psycholinguistic Behavioral Intelligence System

#### Video Demo:  <PASTE YOUR VIDEO URL HERE>

#### Description:

NeuroPrint is a terminal-based psycholinguistic behavioral analysis system developed completely in Python as my CS50P final project. The main goal of this project is to analyze a user’s communication behavior, emotional response patterns, decision-making style, and stress handling tendencies through carefully designed psychological questions and linguistic analysis techniques.

Unlike a basic sentiment analysis program, NeuroPrint attempts to simulate behavioral inference through language patterns. The system does not simply classify text as positive or negative. Instead, it evaluates how a person communicates, reacts to uncertainty, handles emotional situations, and explains reasoning processes. The project combines rule-based behavioral scoring with psycholinguistic analysis concepts to generate a detailed behavioral report.

The project contains two assessment modes. The first mode is the Full Behavioral Assessment, where users answer open-ended reflective questions in detail. These questions are designed to evaluate reasoning style, emotional regulation, ambiguity handling, strategic thinking, and communication patterns. The second mode is the Rapid Behavioral Assessment, which uses scenario-based multiple choice questions for faster analysis. Each option in the rapid assessment contains hidden behavioral weights that influence dimensions such as stress response, confidence level, emotional stability, social orientation, cognitive flexibility, and decision behavior.

One of the major design goals of this project was to make the analysis feel psychologically reasoned rather than random. To achieve this, the project internally uses multiple behavioral dictionaries. These dictionaries contain Indian-English conversational phrases and emotional markers related to stress, confidence, uncertainty, emotional exhaustion, resilience, and social relationships. For example, phrases such as “mentally drained”, “full pressure”, “mood off”, and “overthinking too much” are treated as stress indicators. Similarly, phrases like “I can handle it”, “definitely”, and “I will manage” increase confidence-related scores.

The program also includes contradiction detection logic. If a user claims calmness in one response but repeatedly uses panic-oriented language elsewhere, the system generates observations about emotional inconsistency. I added this feature because I wanted the final report to feel more dynamic and behaviorally realistic instead of using repetitive fixed summaries.

The main file of the project is `project.py`. This file contains all major components of the system, including the terminal interface, question handling, behavioral scoring logic, psycholinguistic analysis functions, contradiction detection system, report generation engine, and report saving functionality. I decided to keep most of the logic inside a single file because the CS50 project requirements encourage having the required custom functions in `project.py`.

The `test_project.py` file contains unit tests written using `pytest`. These tests validate important functions such as the progress bar generator, communication style detector, and writing fingerprint analyzer. I included testing because it improves reliability and also satisfies the CS50 requirement of testing custom functions.

The `requirements.txt` file contains the external Python libraries required to run the project. Currently, the project mainly uses the `textblob` library for lightweight text analysis and `pytest` for testing.

---

## How to Clone and Run the Project

### 1. Clone the Repository
```bash
git clone <YOUR_GITHUB_REPOSITORY_LINK>
```

### 2. Move into the Project Folder
```bash
cd NeuroPrint
```

### 3. Create a Virtual Environment
```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

#### Windows
```bash
source .venv/Scripts/activate
```

#### Mac/Linux
```bash
source .venv/bin/activate
```

### 5. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 6. Run the Project
```bash
python project.py
```

### 7. Run Tests
```bash
pytest test_project.py
```

---

## Requirements
- Python 3.10 or above
- Internet connection only required during initial package installation

---

## Project Notes
- The project is fully terminal-based.
- Generated reports are automatically saved inside the `reports/` folder.
- NeuroPrint does not provide medical or psychiatric diagnosis.
- The behavioral insights are generated using rule-based psycholinguistic analysis.
