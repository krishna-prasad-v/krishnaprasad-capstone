# MP2 Reflection

## What worked
TARGET_CHUNK_SIZE = 500 characters and CHUNK_OVERLAP = 80 or 100 gave answers that provided a correct explanation for the questions (Q1- Who was the assistant...? and Q2 - What killed Julia Stoner..? ). The answers provided a complete messsage. The "facts matched" measure was less than the expected measure for these results because some of the facts were presented by the LLM by re-phrasing the source text, so a strict string comparison failed for some of the markers, even though the LLM included the relevant marker strings in slightly rephrased way. 

## What didn't work
TARGET_CHUNK_SIZE = 1000 characters and CHUNK_OVERLAP = 300 also gave similar results as TARGET_CHUNK_SIZE = 500 characters and CHUNK_OVERLAP = 100, and do not justify the increase in token costs.

TARGET_CHUNK_SIZE = 300 characters and CHUNK_OVERLAP = 80 did not work at all. Even if k = 5 is used, the context was not enough for the LLM to give a proper answer. 

Example: Q: What killed Julia Stoner at Stoke Moran? 

The LLM even said "The excerpts do not provide a direct answer to what killed Julia Stoner or how the method was discovered. Therefore, I cannot provide that information based on the provided excerpts." 

But if k = 10 is used, correct results are returned similar to (500,80, k=3) configuration, since a lot of the context pieces are getting retrieved. But this would incur more token costs and latency due to extensive overlap for 10 retrieved chunks.

## What I'd change
For this demo dataset, I would not change any configuration like chunk size, k value etc. Correct chunks are already getting retrieved when using the configuration (500, 80, k=3). Recommendations for this demo data set are:

### Enhance the user prompt
From what I observed, the "facts matched" KPI gives lower results due to determinstic string search of "expected facts" data points in the LLM answers. If I add "Give full details" in the user prompt, along with the question, I get higher values for the "Facts Matched" KPI. The LLM includes all available details relevant to the asked question and almost all the "expected facts" strings occur in the answer given by the LLM.

### Semantic evaluation of LLM response
Instead of exact string matches, I would calculate the "Facts matched" KPI through a semantic evaluation of the LLM answer with the retrieved text (or a manually extracted, "golden" chunks from the corpus). This can be done in 2 ways:

#### LLM as a judge
Send the retrieved chunks and the LLM answer to a judge LLM (Ex: Sonnet, Opus) and return a structured output with parameters like semantic resemblance levels, number of relevant data points in the corpus/retrieved chunks, number of missed data points in the answer, accept/reject flag for the answer etc. The "Facts matched" KPI calculated using these would give a better reflection of the answer quality.

#### Decision model as a judge
Send the retrieved chunks and the LLM answer to a decision model like Jev with the same structured output as above, instead of expensive judge models like Claude Opus. This will greatly reduce the cost of calculating the "Facts matched" KPI. This can even be added as a permanent KPI calculator in the program workflow, rather than just using it for evals.

## One surprise
(Anything from the build that genuinely surprised you. Could be technical —
"text-embedding-3-small was way better than I expected on rare names" —
or pedagogical — "I didn't realise how much hybrid retrieval was helping
until I tried dense-only here.")
