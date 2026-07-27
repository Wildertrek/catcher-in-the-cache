# Coupling prior, independent replication (2026-07-27)

Re-runs the name-only condition on the same 20 synthetic characters, same prompt, same
three backends, fresh sampling. Pre-registered in `SPEC.md` before the run.

| | r(H, A_HEX) | 95% CI |
|---|---|---|
| published (2026) | +0.83 | [0.72, 0.93] |
| **this replication** | **+0.910** | **[0.799, 0.960]** |
| gemini-2.5-flash alone | +0.921 | [0.730, 0.976] |
| gpt-4o-mini alone | +0.831 | [0.696, 0.918] |

180 calls (3 backends x 20 characters x 3 personas), 121 parsed.

## The refusal, which is part of the result

`claude-haiku-4-5-20251001` returned a rating in **1 of 60** calls, otherwise stating it
had no reliable information about the character. The published run has the same pinned
model rating these characters, so this is a change in serving behaviour, not a change in
the finding: the effect replicates and strengthens on the two raters that answer.

Declining is the behaviour the account predicts when there is nothing to retrieve. The
fusion is what raters that answer anyway produce.

## Reproducing

`python run_name_only_25.py --replicate` (needs ANTHROPIC/OPENAI/GOOGLE keys in `.env`).
Prompt parity with the original `holistic_probe.py` is essential; the script documents
the three ways an earlier draft broke it.
