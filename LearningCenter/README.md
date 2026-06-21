# LearningCenter
LearningCenter/ contains lightweight educational material that helps readers understand the ideas behind retrieval-augmented generation (RAG) and how those ideas connect to RADIANT_LLM.
## Included Notebook
[RAG_Agent_Workshop.ipynb](RAG_Agent_Workshop.ipynb) is a compact walkthrough that demonstrates:
- loading a PDF knowledge source
- extracting and chunking text
- embedding chunks and indexing them with FAISS
- retrieving relevant context for a query
- generating grounded answers from retrieved context
- wrapping the RAG workflow as a simple tool-driven agent
By default, the notebook uses the repository's own supplementary material PDF:
- [radiant-llm-supplementary-material.pdf](https://github.com/SmartLabNuclear/RADIANT_LLM/blob/main/radiant-llm-evaluation/radiant-llm-supplementary-material.pdf)
This keeps the tutorial aligned with the methodology and evaluation context described in the main repository.
## Prerequisites
- Python environment with the notebook dependencies installed
- An OPENAI_API_KEY for embeddings and response generation
- Optional: Google Colab or Jupyter for interactive execution
For the broader project context, installation options, Docker usage, and evaluation materials, see the main [README.md](https://github.com/SmartLabNuclear/RADIANT_LLM/blob/main/README.md).
## Citation
If this repository, the LearningCenter notebook, or the accompanying evaluation materials support your work, please cite the RADIANT-LLM paper.
- Citation metadata: [CITATION.cff](https://github.com/SmartLabNuclear/RADIANT_LLM/blob/main/CITATION.cff)
- Preprint: https://arxiv.org/abs/2604.22755


