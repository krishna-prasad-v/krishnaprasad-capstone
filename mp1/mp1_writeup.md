# MP1 Writeup

## 1. Which strategy won, and on what dimension? (Accuracy? Parse rate? Cost?)

From these results, **Few-Shot** seems to be the best strategy. The LLM strictly follows the example output format. If we provide few-shot examples that illustrate edge cases, the LLM performs the extraction accurately.

---

## 2. What surprised you? Either a strategy worked better than expected, or worse, or a specific snippet failed in a way you didn't predict.

* **Observation 1:**
  Sometimes `"Northwind Ltd."` is extracted by the LLM as `"Northwind Ltd"`. The Golden dataset records this as `"Northwind Ltd"`. Consequently, deterministic evaluation can fail here. However, I observed that the Judge LLM does not fail—it correctly (or leniently, depending on the requirement) marks the evaluation as passed. For evaluating string extraction, Judge LLM evals would generally be better and more flexible than strict deterministic evaluation.

* **Observation 2:**
  For the Judge model, we must provide precise context, system prompts, and instructions. If instructions are insufficient or do not cover various edge-case evaluation scenarios, the Judge LLM can yield incorrect evaluation scores.

* **Observation 3:**
  **Chain of Thought (CoT)** exhibits higher latency and costs more than the other prompt strategies—primarily because the model must think aloud and generate intermediate reasoning tokens before arriving at the answer.

---

## 3. For *your* capstone domain, which strategy would you reach for first? Justify in 2-3 sentences.

For structured JSON extraction, these prompt-only strategies are largely superseded. The modern standard is to use **structured outputs**—either by forcing a tool call or leveraging the API's native structured output format. Modern LLMs (such as Anthropic Claude or OpenAI) support this natively, where the JSON schema is compiled into a grammar that constrains token generation at decoding time, ensuring the output is guaranteed valid JSON rather than relying on probabilistic compliance.

---

## 4. If you had another day, what would you try next? (Different model? More snippets? Different prompts?)

As mentioned above, I would implement a grammar-constrained approach using forced tool calling or native structured output formats.
