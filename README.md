
<div align="center">

### ⚖️ Intelligent Indian Penal Code Query Resolution Engine
*Describe an incident in plain language — get the exact IPC sections that apply.*

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Gemini API](https://img.shields.io/badge/Gemini-API-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)


</div>


## Overview

**IPC Legal** bridges the gap between everyday language and complex legal statutes. Instead of manually sifting through hundreds of IPC sections, you describe what happened — in your own words — and the system identifies the precise legal provisions that apply, powered by Google Gemini's NLP capabilities.

Whether you're a law student, a legal professional doing quick lookups, or a citizen trying to understand your rights, IPC Legal translates human stories into legal references instantly.

![image](https://github.com/user-attachments/assets/20a362b6-4794-4832-bb6d-1040aa996435)


## ✨ Key Features

| Feature | Description |
|---|---|
| 🧠 **AI Summarization** | Gemini API condenses verbose incident descriptions into legal-grade summaries |
| 📖 **Section Matching** | Semantically matches summaries against the full IPC dataset |
| 🔗 **Direct References** | Each result links to the full section text for deeper reading |
| 📊 **Multi-Section Results** | One query can surface multiple applicable sections simultaneously |
| ⚡ **Fast Lookup** | Near-instant results from a structured CSV-backed knowledge base |



## 🗂️ Dataset

The backbone of this system is `sections_desc.csv` — a structured collection of all IPC sections.

```
sections_desc.csv
├── Title       → Human-readable section name
├── Link        → External reference URL (devgan.in)
├── Section     → IPC section number (e.g., "Section 441")
└── Description → Full statutory description of the section
```

**Coverage:** All IPC sections from Section 1 through to the end of the code, giving the system complete legal breadth.



## 🔄 How It Works

<img width="1332" height="568" alt="Screenshot 2026-05-26 110843" src="https://github.com/user-attachments/assets/ccd7bb5a-3af0-43e2-8a5e-d0f2a001994f" />

**Step-by-step:**

1. **Input** — User submits a natural-language incident description
2. **Summarize** — Gemini API extracts the core legal actions from the narrative
3. **Match** — The summary is semantically compared against all IPC section descriptions
4. **Rank & Return** — The most relevant sections are surfaced with titles and reference links

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- A valid [Google Gemini API key](https://ai.google.dev)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/ipc-legal.git
cd ipc-legal

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your Gemini API key
export GEMINI_API_KEY="your_api_key_here"
# On Windows:
set GEMINI_API_KEY=your_api_key_here
```

### Run

```bash
python main.py
```

---

## 💡 Example

**Input Query:**

```
A man forcefully entered his neighbor's house, broke a window to gain entry,
and stole valuable jewelry while the owner was away. The victim suffered
emotional distress.
```

**Generated Summary:**

```
Burglary: forced entry, property damage, theft — resulting in victim distress.
```

**Matched IPC Sections:**

| Section | Offence | Description | Reference |
|---------|---------|-------------|-----------|
| § 441 | Criminal Trespass | Unauthorized entry into property with intent to commit an offence or intimidate the occupant. | [View](http://devgan.in/ipc/section/441/) |
| § 378 | Theft | Dishonest intention to take moveable property out of another person's possession without consent. | [View](http://devgan.in/ipc/section/378/) |
| § 425 | Mischief | Causing destruction or damage to property, diminishing its value or utility. | [View](http://devgan.in/ipc/section/425/) |

---

## 📁 Project Structure

```
ipc-legal/
│
├── main.py                 # Entry point — handles user input & output
├── query_processor.py      # Core NLP + matching logic
├── gemini_client.py        # Gemini API integration layer
├── sections_desc.csv       # IPC sections dataset
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 🛠️ Tech Stack

- **Language:** Python
- **NLP Engine:** Google Gemini API
- **Data Layer:** CSV (Pandas)
- **Matching:** Semantic similarity via NLP embeddings

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve the matching accuracy, expand the dataset, or add new features:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-idea`)
3. Commit your changes
4. Open a Pull Request

---

