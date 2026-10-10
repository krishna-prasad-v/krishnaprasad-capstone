# krishnaprasad-capstone

This repository contains the capstone project and weekly assignments.

## 📂 Repository Structure

```text
krishnaprasad-capstone/
│
├── .venv/                  # Python Virtual Environment (ignored by Git)
├── .gitignore              # Files and folders ignored by Git
├── README.md               # Main repository documentation
├── requirements.txt        # Project dependencies
│
├── Week1/          
│   ├── src/
│   └── runs/
│
├── Week2/
│   ├── data/
│   ├── Logs/
│   └── src/
│
├── Week4/
│   ├── data/
│   ├── logs/
│   └── src/
│
├── mp1/
│   ├── data/
│   ├── docs/
│   ├── src/
│   ├── mp1_comparison.md
│   └── mp1_writeup.md
│
└── Week6/
    ├── corpus_files/
    ├── runs/
    └── src/
```

### requirements.txt
* mp1 -> `mp1/docs/requirements.txt`
* rest of the repo -> `requirements.txt`

### .env file
#### Week 1, Week 2, Week 4
```text
ANTHROPIC_API_KEY=<KEY>
```
#### Week 6
```text
ANTHROPIC_API_KEY=<KEY>
VOYAGE_API_KEY=<KEY>
```
#### mp1
```text
OPENAI_API_KEY=<KEY>
OPENAI_BASE_URL=<Vocareum_URL>
```

## 📝 Technologies Used
* **Language:**                 Python 3.14.3
* **LLM**                       Anthropic Claude 
* **Embedding Model for RAG**   Voyage AI 
* **SDK:**                      Anthropic SDK, Voyage AI SDK
* **Version Control:**          Git & GitHub
* **Environment Management:**   Python .venv

Note: for mp1:
* **LLM**                       Open AI
* **SDK:**                      OpenAI SDK

---
*Created and maintained by Krishna Prasad.*
