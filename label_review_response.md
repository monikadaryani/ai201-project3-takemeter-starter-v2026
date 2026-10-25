# Response to the ChatGPT label review

**Reviewer:** Claude (the same model that pre-labelled the data, so this is not
an independent opinion either)
**Reviewed:** `label_review_summary.md`, `labels_review_audit.csv`,
`labels_reviewed.csv`
**Row numbers** count comments in `labels.csv` from 1, excluding the header.
They match the `source_row` column in ChatGPT's audit.

## Verdict

The review is careful and found one real flaw in the taxonomy. Its output
file should not be used for training.

- **Right about the definitions.** `hot_take` required "no reasoning," but
  food opinions almost always come with a quick reason. Read literally, the
  label could only hold bare verdicts. This led to renaming the label
  `opinion` (see below).
- **Right about parent context.** Some short replies only make sense next to
  the comment they answer. The model never sees that comment, so these rows
  can't be labelled reliably.
- **Wrong to hold rather than resolve.** It set aside 33 of 200 rows, mostly
  reasoned opinions. In its accepted copy, `hot_take` falls to 16 of 167
  (9.6%), which is too few to train on. Holding rows exposed the problem
  without fixing it.
- **Inconsistent on humor.** It adopted the README's rule that jokes stay
  `reaction`, then relabelled several jokes as `technique` because they
  mention an ingredient (rows 89, 108, 114).
- **Not a human check.** The review says this itself. AI review of AI labels
  doesn't replace the labeller checking each row, and every row except 7
  remains unchecked.

## What changed because of the review (already applied)

| Change | Where |
|---|---|
| `hot_take` renamed `opinion`, defined as "a judgment or preference about food or cooking in general, with or without reasons, that gives no method someone could follow" | README, `label_definitions.txt`, `labels.csv`, notebook `LABELS` |
| `technique` tightened to "gives a method someone could follow, or explains why something happens when you cook". The old word "reason" overlapped with reasoned opinions | README, `label_definitions.txt` |
| New rule: reasons for *liking* something don't make a comment `technique` | README decision rule |
| New rule: a judgment about food in general is `opinion`; a response to this post is `reaction` | README decision rule |
| 7 rows relabelled `opinion`: 73, 81, 84, 92, 95, 151, 166 | `labels.csv` |

Label counts are now technique 81, reaction 77, opinion 42.

## ChatGPT's 10 label changes

| Row | Comment (start) | ChatGPT | My view |
|---|---|---|---|
| 32 | "our family gatherings were always buffet style…" | reaction → technique | **Disagree.** It's a family story. Buffet style is described, not recommended. |
| 39 | "airfryers don't do well with battered food… might as well pan fry" | hot_take → technique | **Disagree.** "Might as well pan fry" is a verdict, not a method. Now `opinion`. |
| 63 | "ignore that first impulse to mess with it…" | reaction → technique | **Agree.** It's advice to leave food alone. |
| 81 | "this sounds way better… not much harder" | reaction → hot_take | **Agree.** Applied as `opinion`. |
| 89 | "My friend makes them from Fruity Pebbles. THC infused butter but still…" | reaction → technique | **Disagree.** It's a joke. The README's humor rule applies. |
| 100 | "Sweetened chili seems to be a midwestern thing…" | hot_take → reaction | **Agree.** It's mostly a story about one person's chili. |
| 108 | "Chilis ironically make really good chili" | reaction → technique | **Disagree.** It's a joke reply, not a tip. |
| 109 | "I have been using Ancho chili powder… going to get dried chilis" | reaction → technique | **Disagree.** It describes a plan, not a method someone could follow. |
| 114 | "if I want to top noodles with chili and parmesan… I will lol" | hot_take → technique | **Disagree.** It defends a preference. Now `opinion`. |
| 126 | "Most cooking you have to do by taste as you go anyways…" | hot_take → technique | **Disagree.** It's a general opinion about cooking. Now `opinion`. |

**I agree with 3 of the 10 (63, 81, 100).** Row 81 is applied; rows 63 and
100 are not yet.

## The 28 held rows: how the new rules resolve them

**Reasoned opinions become `opinion` (17 rows).** These are judgments or
preferences with reasons and no method: 2, 15, 23, 44, 46, 52, 58, 113, 139,
144, 145, 146, 147, 157, 159, 160, 165.

Row 113 ("DO NOT add noodles…") is a purity verdict, not a recipe step. Row
44 (avoid recipes from random websites) is a judgment about sources, not a
kitchen method.

**Context-only replies are dropped (7 rows).** Proposed rule: label from the
comment text alone, and drop it if the text has no clear meaning without its
parent comment.

| Row | Comment | Problem |
|---|---|---|
| 18 | "This is why I always microwave mine first." | Microwave what, and why? |
| 24 | "Depends if youre going for competition cuts or not" | Depends on what? |
| 71 | "if you want to use it for layering in a sandwich, then yes." | Use what? |
| 111 | "Ground coffee will also do the trick." | What trick? |
| 150 | "Its because of the layer of basil leaves right under the cheese." | What is "it"? |
| 186 | "Parsley tea can do the same thing IIRC" | Same as what? |
| 191 | "7UP and pears dawg my wife korean" | For what purpose? |

**Other held rows (4).**

| Row | Comment (start) | Resolution |
|---|---|---|
| 76 | "I like this idea! Plus it avoids double dipping…" | `reaction`. It reads on its own as enthusiasm plus a catering anecdote |
| 95 | "Assorted cookie tray, something for everyone." | Already relabelled `opinion` |
| 121 | "It's like the most popular dish in Mumbai…" | Drop as food trivia, consistent with the earlier trivia rule |
| 158 | "I made a really good spinach/creamy pesto sauce pasta…" | `reaction`. A personal meal story with no method |

## ChatGPT's 5 exclusions

| Row | Comment (start) | My view |
|---|---|---|
| 28 | "You were raised right." | Agree. Side comment about etiquette |
| 29 | "Friend is kind of a dick, though." | Agree. Side comment |
| 42 | "if you cant be bothered to write a proper comment…" | Agree. Argument between commenters |
| 45 | "the website is mentioned up there why you ranting…" | Agree. Argument between commenters |
| 184 | "Papain… carries a risk of miscarriage…" | Agree. A health claim, not cooking |

## If the remaining proposals are applied

| Step | Rows |
|---|---|
| Current | 200 |
| Drop ChatGPT's 5 exclusions | −5 |
| Drop 7 context-only replies | −7 |
| Drop row 121 (trivia) | −1 |
| **Result** | **187** |

That's above the 150 minimum but below the 200 the brief asks for. Saving 1–2
more threads would close the gap. Relabelling the 17 reasoned opinions changes
no counts, because they are already `opinion` after the rename.

## What neither review replaces

1. **The labeller's own check of every row.** 193 rows are still marked
   `pre-labelled by Claude, unchecked`.
2. **An independent agreement check.** `agreement.py` compares labels against
   the staff set. Two AI models agreeing or disagreeing doesn't measure
   whether the labels are right.
3. **Thread IDs.** Comments from the same thread can land in both the
   training and test splits. The saved files in `data/raw/` could be used to
   record each row's thread if leakage needs checking.
