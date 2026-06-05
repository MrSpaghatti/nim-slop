# Deep Research Report: Nim Training Data Acquisition
**Objective:** Acquire genuinely useful Nim programming language training data for fine-tuning Qwen3.5-9B (with LoRA, max 32GB VRAM limit on AMD ROCm).

This report outlines actionable sources and methods, prioritized for immediate execution.

## 1. Dataset Discovery on Hugging Face / GitHub
*   **The Stack v2 (BigCode):** We verified that The Stack v2 contains a dedicated subset for Nim.
    *   **Source:** `bigcode/the-stack-v2` path: `data/Nim/train-00000-of-00001.parquet`
    *   **Estimated Size:** ~30MB parquet file.
    *   **Quality Signals:** Deduplicated, though raw. Will require AST-based length filtering and compile-verification.
    *   **Effort:** Low.
    *   **Next Steps:** Download this specific parquet file using `huggingface-cli` or `datasets` library. Extract `.nim` files, filter out empty/trivial files (e.g. `wc -c < 200`), and run `nim check` across the extracted files.
*   **Other HF Datasets:** We found several Nim-related small datasets (`nimaster/autonlp-data-devign_raw_test`, `nadhifikbarw/id_ner_nimas`), but these seem highly specialized (NER, Vulnerability Detection) rather than broad code generation. No major standalone fine-tuning corpus exists on HF specifically for Nim besides The Stack.

## 2. Additional Active Nim Repositories
We queried GitHub for `language:Nim` sorted by stars and recent updates.
*   **Top Uncovered Candidates:**
    *   `zedeus/nitter` (13K stars, actively updated) - Complex web application.
    *   `dom96/jester` (1.6K stars) - Highly used web framework.
    *   `karaxnim/karax` (1.1K stars) - Single-page application framework.
    *   `mratsim/Arraymancer` (1.4K stars) - Scientific computing / ML tensor library.
    *   `yglukhov/nimpy` (1.5K stars) - Python/Nim bridge.
    *   `HapticX/happyx` (650+ stars) - Web framework.
*   **Estimated Size:** Thousands of high-quality `.nim` files across these repos.
*   **Quality Signals:** High stars, active maintenance (updated within the last month), real-world complexity (networking, math, UI).
*   **Effort:** Low.
    *   **Next Steps:** Run a script to clone these specific repositories. Recursively search for `.nim` files, filter out tests if pure implementation is desired, and append to the training corpus.

## 3. Compile-time Verification Pipelines
*   **Concept:** To ensure high quality, every source file should theoretically compile. However, compiling whole repos is hard due to missing dependencies (`nimble install` required).
*   **Actionable Pipeline (`nim check`):**
    *   Instead of full compilation, use `nim check --threads:off <file.nim>`. This performs syntax and semantic checking without generating a binary or requiring all C linking dependencies to be perfectly aligned.
    *   **Scale / Distributed:** Nim's compiler is extremely fast. A single thread can check hundreds of files per second. For 100K files, simple Python `multiprocessing.Pool` or GNU `parallel` is more than sufficient on a local machine.
    *   **Effort:** Low/Medium.
    *   **Next Steps:** Write a Python script using `subprocess.run(["nim", "check", "--threads:off", filepath], capture_output=True)`. Discard files that return non-zero exit codes or emit `Error:` in stderr.

## 4. Test-suite Mining
*   **Targets:** Standard library tests are often too simple.
*   **Better Targets:**
    *   `status-im/nimbus-eth2` (Ethereum 2.0 client) - Known for rigorous testing.
    *   The `nim-lang/Nim` compiler test suite (already ingested, but ensure `tests/` directory was fully mined).
*   **Extraction Method:**
    *   Tests in Nim often use the `unittest` module (`suite`, `test`, `check`).
    *   We can use simple regex or Python AST/Tree-sitter (Tree-sitter has a Nim grammar available via community extensions) to extract the `test "description":` block as the *prompt* (e.g., "Write a test for..."), and the block body as the *code*.
*   **Effort:** Medium.
    *   **Next Steps:** Clone `nimbus-eth2`. Run a regex parser `(?s)test "(.*?)":\n(.*?)(?=\ntest|\z)` to extract test pairs.

## 5. Synthetic Data Generation Alternatives
*   **Distillation Models:**
    *   With an R9700 (32GB VRAM), you can run models up to ~32B parameters using 4-bit quantization (Q4_K_M in llama.cpp or AWQ/GPTQ in vLLM).
    *   **Best Local Model:** `Qwen2.5-Coder-32B-Instruct` (Quantized to 4-bit fits in ~20GB VRAM) or `DeepSeek-Coder-V2-Lite` (16B MoE fits easily).
*   **Self-Play / Expert Iteration:**
    *   You can set up a local pipeline: prompt Qwen2.5-Coder to generate Nim code for a specific algorithm -> run `nim check` -> if fails, prompt model with the compiler error to fix it -> save successful generations.
*   **Effort:** Medium/High (Requires setting up vLLM/llama.cpp and orchestration script).
    *   **Next Steps (This Week):** Use `llama.cpp` server with `Qwen2.5-Coder-32B-Instruct-GGUF`. Write a Python script that feeds algorithms from RosettaCode, asks for Nim implementation, and loops with `nim check` feedback until it passes.

## 6. Parallel Code / Translation Data
*   **Rosetta Code:** Rosetta Code explicitly has a "Nim" category with hundreds of algorithms already implemented, often paired with Python/C++ implementations.
*   **Python Bridges:** Repos like `Pebaz/nimporter` (compile Nim extensions for Python) often contain paired examples of Python code and the equivalent Nim code for speedup.
*   **Translation via LLM:**
    *   Take high-quality Python snippets from existing datasets (e.g., CodeAlpaca).
    *   Use the local quantized LLM to translate Python -> Nim.
    *   Filter aggressively using `nim check`.
*   **Effort:** Low (Rosetta Code scraping) to Medium (LLM translation).
    *   **Next Steps:** Scrape the Rosetta Code website for tasks in both Python and Nim. Create instruction pairs: "Translate this Python code to Nim: [Python Code]" -> "[Nim Code]".

## 7. Documentation-to-Code Alignment
*   **Official Sources:**
    *   `nim-by-example` (`flaviut/nim-by-example` on GitHub).
    *   Nim Manual (`doc/` in the Nim compiler repo).
*   **Extraction:**
    *   These are usually written in Markdown or Nim's RST format, with code embedded in ````nim ... ```` blocks immediately following an explanatory paragraph.
*   **Effort:** Low.
    *   **Next Steps:** Clone `flaviut/nim-by-example`. Write a Python script to parse the Markdown/RST. Extract the heading/paragraph immediately preceding a ```nim block as the "thinking" or "instruction", and the block itself as the "nim_code".
