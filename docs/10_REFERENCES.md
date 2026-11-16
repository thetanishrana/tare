# References

Collected while planning, on 2026-10-10 to 2026-10-12. Secondary sources are marked. Check anything that drives a decision.

## Closest prior work
- Yan & Zhang (Merck), *Eliminating QC Programming Duplication Through Claude AI-Assisted Independent Code Generation*, PharmaSUG 2026 AI-201. https://pharmasug.org/proceedings/2026/AI/PharmaSUG-2026-AI-201.pdf
- Yan, *ClinAgent: A Five-Layer Architecture for Autonomous Clinical Trial Statistical Programming*, medRxiv 2026. https://www.medrxiv.org/content/10.64898/2026.01.09.26343542v1.full.pdf
- *ClinAgent: AI-assisted methodology for clinical trial data processing and statistical programming* (PMC). https://www.ncbi.nlm.nih.gov/pmc/articles/PMC13555824/
- Liu & Ci (Yesod AI), *AI-Powered Multiple-Agent Pipeline for Automating ADaM Dataset Generation*, PharmaSUG 2026 AI-431. https://pharmasug.org/proceedings/2026/AI/PharmaSUG-2026-AI-431.pdf
- Tatikonda et al. (Takeda), *Enhancing ADaM Specification Validation and Generation of SAS Codes Using LLM through Amazon Bedrock*, PharmaSUG 2026 AI-125. https://pharmasug.org/proceedings/2026/AI/PharmaSUG-2026-AI-125.pdf
- Xia & Du (Merck), *A Human-in-the-Loop AI-Assisted Framework for ADaM Standardization*, PharmaSUG 2026 AI-332. https://pharmasug.org/proceedings/2026/AI/PharmaSUG-2026-AI-332.pdf
- Yan (Merck), *Schema-Preserving Generation of Clinical TLF Templates and Executable R Code via Iterative LLM-Guided Debugging*, PharmaSUG 2026 AP-211. https://pharmasug.org/proceedings/2026/AP/PharmaSUG-2026-AP-211.pdf
- *Closing the Loop: Validating AI-Generated SDTM Mappings using CDISC CORE*, PharmaSUG 2026 SS-261. https://pharmasug.org/proceedings/2026/SS/PharmaSUG-2026-SS-261.pdf
- *Friction to Flow: LLM-Based Automation of Clinical Data Workflows*, PharmaSUG 2026 DS-196. https://pharmasug.org/proceedings/2026/DS/PharmaSUG-2026-DS-196.pdf
- *CAVE-Onc: Graph-constrained agentic validation for cross-domain contradictions in CDISC oncology submissions*, PLOS ONE 2026. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC13475866/
- *Evidence Behind the Automation of Clinical Trial Statistical Programming: A Scoping Review*, medRxiv. https://www.medrxiv.org/content/10.64898/2025.12.24.25342988.full.pdf

## QC practice
- *Does SDTM Validation Really Require Double Programming?*, PharmaSUG 2025 MM-227. https://pharmasug.org/proceedings/2025/MM/PharmaSUG-2025-MM-227.pdf
- Datanovia, *Agentic Clinical Programming* (course; the silent safety-population example). https://www.datanovia.com/learn/pharma-clinical/08-agentic-clinical-programming/

## Data, packages and tools
- pharmaversesdtm reference manual. https://cran.nics.utk.edu/cran/web/packages/pharmaversesdtm/refman/pharmaversesdtm.html
- pharmaverseadam reference manual. https://cran.nics.utk.edu/cran/web/packages/pharmaverseadam/refman/pharmaverseadam.html
- pharmaverseadam README (how datasets are regenerated). https://cran.ms.unimelb.edu.au/web/packages/pharmaverseadam/readme/README.html
- admiral vignette, *Creating ADSL*. https://cran.ms.unimelb.edu.au/web/packages/admiral/vignettes/adsl.html
- admiralmetabolic vignette (use_ad_template, list_all_templates). https://cran.nics.utk.edu/cran/web/packages/admiralmetabolic/vignettes/admiralmetabolic.html
- diffdf vignette. https://cran.nics.utk.edu/cran/web/packages/diffdf/vignettes/diffdf-basic.Rmd
- cdisc-rules-engine on PyPI. https://pypi.org/project/cdisc-rules-engine
- CDISC and Microsoft on CORE (2021). https://www.businesswire.com/news/home/20210601005147/en
- CDISC and FDA on CORE business rules (2024). https://www.businesswire.com/news/home/20240116117632/en

## LLM evaluation and agents
- Kim et al., *Correlated Errors in Large Language Models*, ICML 2025. https://proceedings.mlr.press/v267/kim25e.html
- Gloaguen et al., *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?*, ICLR 2026. https://iclr.cc/virtual/2026/10018749
- Addy Osmani, *Agent Harness Engineering*. https://addyosmani.com/blog/agent-harness-engineering/
- Anthropic Engineering, *Code execution with MCP*. https://www.anthropic.com/engineering/code-execution-with-mcp
- Chroma, *Context Rot*. https://research.trychroma.com/context-rot

## Local models, hardware and training
- Apple ML Research, *Exploring LLMs with MLX on M5*. https://machinelearning.apple.com/research/exploring-llms-mlx-m5
- Morph, *Best Ollama Models (2026)* (secondary; tags and sizes need checking). https://www.morphllm.com/best-ollama-models
- BestLLMFor, *Best LLMs for a 32 GB Mac* (secondary). https://bestllmfor.com/meilleur-llm/mac-32gb/
- mlx-lm-lora. https://github.com/Goekdeniz-Guelmez/mlx-lm-lora
- Unsloth fine-tuning guide. https://unsloth.ai/docs/get-started/fine-tuning-llms-guide
- Free GPU options, including Kaggle quotas (secondary). https://www.gmicloud.ai/en/blog/best-free-gpu-cloud-options-for-ai-startups-and-researchers

## Terms and pricing
- Claude Code, *Legal and compliance* (authentication and credential use). https://code.claude.com/docs/en/legal-and-compliance.md
- Claude Code, *Run Claude Code programmatically* (headless and bare mode). https://code.claude.com/docs/en/headless.md
- Claude Code, *Authentication*. https://code.claude.com/docs/en/authentication.md
- OpenAI Codex, *Authentication*. https://learn.chatgpt.com/docs/auth
- CostBench, *Claude API pricing* (secondary, checked 2026-10-10). https://www.costbench.com/software/llm-api-providers/claude-api/
