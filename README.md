# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter sorts comments from r/Cooking, a public subreddit where home cooks
share dishes, ask for help, and argue about methods. Each comment is labelled
`technique` (a method you could follow, or why something happens when you
cook), `opinion` (a judgment or preference about food, with or without
reasons, but no method), or `reaction` (a compliment, joke, personal story,
or feeling about the post). The goal is to separate comments that teach
something from ones that only judge or react.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `technique`

**Definition:** Gives a method someone could follow in the kitchen, or
explains why something happens when you cook.

**Example 1:**
> Cut the top and bottom off. Cut one side off. Run your knife along the
> inside to separate the fleash from the seeds. Bam. Cutting through the seeds
> causes them to go everywhere.

**Example 2:**
> The best advice on browning beef is LISTEN. You will hear the sound go from
> a hiss (steaming) to a crackle (frying) and that is when it starts to go from
> gray to brown.

### `opinion`

**Definition:** A judgment or preference about food or cooking in general,
with or without reasons, that gives no method someone could follow.

**Example 1:**
> Air fryers aren't real fryers. I think the recipe creator lied to you.

**Example 2:**
> Puttanesca!
>
> I loveeee olives and it’s just such a delicious and simple pasta.

*Renamed from `hot_take`.* The first version required "no reasoning," but
food opinions almost always come with a quick reason ("I love olives", "it
never comes out dry"). Under that rule only bare verdicts qualified, and an
annotation review held back most of the label. Either reasoned opinions got
their own route or they had to be excluded; excluding them would have left
about 16 examples, so the label was broadened and renamed.

### `reaction`

**Definition:** A compliment, joke, personal story, or emotional response to
the post that gives no advice and makes no argument.

**Example 1:**
> These sound delicious!!

**Example 2:**
> Learned this one only a few weeks ago. My lord have I cooked many meals with
> boiled ground beef 😭

### The hardest boundary

**Which two labels:** `technique` and `opinion`

**The post that sits between them:**
> The core of great chili con carne is dried chiles, lots of onion and cubed
> (not ground) meat.
>
> Dried Chiles, toasted, rehydrated and blended to make a sauce are the real
> key.

**The decision rule I used every time:**
<!-- e.g. "If the post names a specific checkable fact, it's `analysis`, even
     if the tone is heated." -->
If the comment tells you something concrete to do or explains why something
happens ("Don't crowd your pan.", "…because they soak up water and won't
brown"), it's `technique`, even if it's phrased as a strong opinion. If it
passes judgment, saying something is good, bad, better, or overrated, it's
`opinion`, even when it gives reasons. Reasons for *liking* something ("it's
so simple", "I love olives") don't make it `technique`; only a method you
could follow or an explanation of what happens in the pan does.

More rules I applied every time:

- **Opinion vs. reaction: general or personal?** A judgment about food or
  cooking in general ("Can't go wrong with Chef John") is `opinion`. A
  response to this post or this person ("These sound delicious!!") is
  `reaction`.
- **A usable tip wins.** If a story or compliment contains real cooking
  guidance someone could follow ("I shared it with the instruction to use a
  sh!t-ton more garlic than it calls for"), it's `technique`. Jokes and
  sarcasm stay `reaction` even when they mention a method ("don't stew
  pineapple in a copper pot with an aluminum lid, that's called a battery").
- **Off-topic comments are dropped, not forced into a label.** Hosting
  etiquette arguments, food-history trivia, and side arguments between
  commenters were removed from the dataset.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

> **This section describes the original 200-row dataset** that the unit 5
> training run and the "before" results used. As part of the improvement in
> unit 6, it was expanded to 400 rows. See [The Improvement](#the-improvement).

**Where the posts came from:** Public comments from 12 r/Cooking threads,
saved on 22 October 2026 and extracted with `extract_comments.py` (at most 30
comments per thread). The threads mix question posts ("Why is cooked celery
not a more common ingredient?"), "I made this" posts, and opinion threads.
320 comments were collected and cut to 200:

- 69 dropped as out of scope: link-only, replies that only make sense next to
  their parent comment, hosting-etiquette arguments, food trivia, and side
  arguments between commenters.
- 51 trimmed for size: comments over 100 words (the model truncates at 128
  tokens) and near-duplicate suggestions. 4 of these were added back to reach
  200.
- 4 more dropped during review because they couldn't be labelled without
  their parent comment.

**How I labelled them:** <!-- Cold first? Pre-labelled with AI and corrected?
Say so plainly — the disclosure is required, not penalised. -->
Pre-labelled with AI, then reviewed. Claude pre-labelled all comments. A
second model, ChatGPT, reviewed every label. I personally checked and decided
52 rows: every row where the two models disagreed, every row ChatGPT held
back as unclear, the rows added back, and a few I checked at the start. The other 148 labels are ones both
models agreed on and I did not change. The taxonomy was revised during review:
`hot_take` became `opinion` when reasoned opinions turned out not to fit
anywhere.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `technique` | 85 | 42.5% |
| `reaction` | 74 | 37% |
| `opinion` | 41 | 20.5% |
| **Total** | 200 | 100% |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* "Yep. Chilis ironically make really good chili"
>
> *Could have been:* `reaction` (a joke reply) or `technique`
>
> *I chose, because:* `technique`. Under the joke there's a sincere, usable
> idea: build chili on real chiles, not just chili powder. The two models
> split on this one.

**2.**
> *The post:* "My friend makes them from Fruity Pebbles. THC infused butter
> but still...."
>
> *Could have been:* `technique` (an ingredient swap) or `reaction`
>
> *I chose, because:* `reaction`. It names ingredients, but the point is the
> joke, not a suggestion anyone is meant to follow. Next to case 1, this
> shows where my joke-versus-tip line sits.

**3.**
> *The post:* "Whatever you do DO NOT add noodles or serve with a peanut
> butter sandwich. Jesus, midwesterners scare the shit outta me. Folks should
> remember us western folks blessed you with the perfection proper chili
> is...."
>
> *Could have been:* `technique` (a literal instruction about what not to
> add) or `opinion`
>
> *I chose, because:* `opinion`. It's phrased as an instruction, but it's a
> verdict on what "proper" chili is, not a method. The rest of the comment
> is regional gatekeeping, not cooking guidance.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

> **This section describes the unit 5 run on the original 200 rows.** The
> settings stay the same for the improvement run. The 400-row split sizes are
> in [The Improvement](#the-improvement).

**Base model:** `distilbert-base-uncased`

**Settings:** <!-- epochs, learning rate, batch size, seed -->
3 epochs, learning rate 2e-5, batch size 16, seed 42, max length 128 tokens.
Trained on an Apple Silicon GPU (MPS), torch 2.14.1.

**Anything I changed from the defaults, and why:** Only `LABELS`, set to my
three labels. The training settings are the defaults for the unit 5 run and
for the improvement run. A separate stretch run changed epochs from 3 to 8;
see [Stretch Goals](#stretch-goals). Max length stayed at
128. I measured every comment with the `distilbert-base-uncased` tokenizer:
the longest is 124 tokens including the special tokens, so nothing gets
truncated. That holds for the 400-row dataset as well. (An earlier version of
this line said that removing comments over 100 words guaranteed this, but a
word count can't prove it. The tokenizer measurement does.)

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->

| Label | Train | Val | Test |
|---|---|---|---|
| `technique` | 59 | 13 | 13 |
| `reaction` | 51 | 12 | 11 |
| `opinion` | 29 | 6 | 6 |
| **Total** | 139 | 31 | 30 |

`opinion` has only **6** examples in the test split, under the roughly 8
where scores stop jumping around. Its F1 will swing a lot between seeds, which
is why criterion 3 sets a looser target for it.


---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1: choosing the community**

- *What I asked for:* Help picking a public community. I started with
  r/GirlDinnerDiaries, which I read a lot, and pasted a real thread into
  Claude.
- *What came back:* Claude said the thread was almost all sympathy comments,
  the sub's "be kind" rules remove hot takes, and the posts were too personal
  (a child's diagnosis, a pregnancy decision) to quote in a README. It
  suggested r/Cooking or r/personalfinance instead.
- *What I changed:* I tried staying with r/GirlDinnerDiaries anyway, then
  dropped it myself because the posts didn't teach anything. I switched to
  r/Cooking, chose the 12 threads, and saved them from my browser, since
  Reddit blocked script access.

**Moment 2: a second model reviewing the labels**

- *What I asked for:* I gave ChatGPT my label definitions and Claude's
  pre-labels and asked it to review every row.
- *What came back:* It agreed with most labels but held back 28 rows. Most
  were opinions with a reason attached ("Puttanesca! I love olives…"), which
  the old `hot_take` definition ("no reasoning") didn't allow. It also
  relabelled several jokes as `technique` because they mentioned an
  ingredient.
- *What I changed:* I renamed `hot_take` to `opinion` and broadened it to
  allow reasons, rather than throwing out the held rows. Then I decided every
  disputed row myself. Sometimes I sided with ChatGPT ("Chilis ironically
  make really good chili" → `technique`), sometimes with Claude ("THC infused
  butter but still…" stayed `reaction`), and sometimes with neither (the
  chili-on-noodles defence → `opinion`, where both models said
  `technique`).

**Moment 3 (unit 6): choosing the improvement**

- *What I asked for:* Which single improvement would do the most to meet my
  criteria.
- *What came back:* Claude first recommended training longer (3 → 10
  epochs). Its reasoning: 139 training examples at batch size 16 is only 27
  training steps, and seed 7's collapse looked like undertraining. I asked
  whether more data would beat that, and about changing the learning rate.
  Claude compared the three: epochs were the cheapest and cleanest
  experiment; a higher learning rate risked making the seed-to-seed swings
  worse; more `opinion` examples were the stronger fix for `opinion` but
  more work. Once I shared the course's three improvement options, it
  switched to recommending about 30 more `opinion` examples, because that
  matched my diagnosis for criterion 3.
- *What I changed:* I went further than either suggestion. Instead of 30
  `opinion` rows, I saved two opinion-heavy threads and doubled the dataset
  to 400 rows with the three labels balanced, also bringing back comments
  that had been trimmed earlier. I kept epochs and learning rate unchanged,
  so the improvement stayed data-only and the before/after comparison
  measures that one change.

**Pre-labelling disclosure:**

*Unit 5 (the original 200 rows).* Claude pre-labelled all the comments, and
ChatGPT reviewed every label. I personally decided 52 rows: every row where
the two models disagreed, every row ChatGPT held back, 4 rows added back
late, and a few I checked at the start. The other 148 rows carry labels that
both models agreed on, and I did not re-read each of those individually.

*Unit 6 (the improvement, 211 new rows).* Claude labelled every new comment.
ChatGPT reviewed the full 400-row file twice. I decided every change those
reviews raised: 8 relabels, 26 drops (including 11 from the original 200),
and the 4 disputed rows in the second review. I did not personally re-read
every new row. The ones I didn't check carry labels Claude assigned that
ChatGPT's review did not dispute.

*Staff agreement set.* Claude labelled the 30 staff posts, not me, so the
100% agreement rate measures Claude (see the Agreement Report).

*Other AI help.* Claude wrote `extract_comments.py`, ran the baseline
script, ran the 8-epoch stretch training run (reusing the notebook's own
code, with only `EPOCHS` changed), and drafted most of this README and `criteria.md` from my decisions
and the result files: the Run Logs, diagnoses, the Improvement write-up, and
What's Still Broken. I reviewed and directed those drafts. The labelling
decisions listed above, the choice of community, the choice of improvement,
and the calls on disputed rows were mine.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Baseline-names-only | Trained | Difference |
|---|---|---|---|---|
| Overall accuracy | 0.467 | 0.500 | 0.667 | +0.200 |
| Macro F1 | 0.262 | 0.496 | 0.496 | +0.234 |
| F1 — `opinion` | 0.000 | 0.667 | 0.000 | 0.000 |
| F1 — `technique` | 0.619 | 0.250 | 0.727 | +0.108 |
| F1 — `reaction` | 0.167 | 0.571 | 0.762 | +0.595 |

Baseline is `facebook/bart-large-mnli` zero-shot with `label_definitions.txt`;
Baseline-names-only is the same model given only the three label names.
Trained is seed 42. Difference is Trained minus Baseline. All three are scored
on the same 30 held-out posts from the original 200-row dataset. These files
are kept as `baseline_results_before.json`, `baseline_names_only_before.json`,
`results_before.json` and `test_split_before.csv`. The same comparison on the
400-row dataset is in [The Improvement](#the-improvement).

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->
Trained accuracy around **0.75**, about 8 points above the baseline's 0.667.
`technique` and `reaction` will roughly match the baseline (within about
0.05), because it's already strong on them (0.727 and 0.762). The fine-tuned
model learned from only 139 examples, so it may not beat a much bigger model
there. The big change will be `opinion`: the baseline never got one right
(F1 0.000). I expect the trained model to get it off zero, but stay **below
0.45**, because it has only 29 training examples and 6 test examples. If the
trained model only ties the baseline overall, the gain will come almost
entirely from `opinion`.

> **Note:** When I wrote this, my Baseline column mistakenly held the trained
> seed-42 numbers, so the figures above are trained results, not the baseline
> (real baseline: 0.467 accuracy).

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.65 | 0.667 | 0.467 | 0.667 | MISSED |
| 2. F1 on `technique` | ≥ 0.70 | 0.727 | 0.619 | 0.722 | MISSED |
| 3. Every label F1 | ≥ 0.45 | 0.000 | 0.000 | 0.000 | MISSED |
| 4. Agreement with staff labels | ≥ 80% | 100% | 100% | 100% | MET |
| 5. Confidence gap (most-sure third minus least-sure third) | ≥ 0.15 | 0.10 | 0.40 | 0.30 | MISSED |

Notes on the table:

- **Criterion 1 and 2:** both missed only because of seed 7. Seeds 42 and
  2024 clear the target.
- **Criterion 3:** each value is the lowest F1 of the three labels. It's
  `opinion` every time: the model never predicted `opinion` in any seed.
- **Criterion 4:** agreement doesn't depend on the seed. It's one measurement
  of 30 staff posts, repeated in each column. Those posts were labelled by
  Claude, not me (see the Agreement Report).
- **Criterion 5:** the per-seed gaps are 0.80 − 0.70, 0.60 − 0.20, and
  0.90 − 0.60. Missed on seed 42.

Accuracy moved 0.200 across seeds (0.467 to 0.667), more than the 10 points
the notebook treats as a stable measure. Seed 7 collapsed: it called 29 of
30 posts `technique`.

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

Seed 42, 30 held-out posts.

| true \ predicted | opinion | technique | reaction |
|---|---|---|---|
| **opinion** | 0 | 5 | 1 |
| **technique** | 0 | 12 | 1 |
| **reaction** | 0 | 3 | 8 |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->
5 real `opinion` posts were called `technique`, and none went the other way.
The whole `opinion` column is zero: the model never predicts `opinion` at all,
in any seed. So it didn't learn the `opinion`/`technique` boundary, and it
fails in one direction only: opinions get absorbed into `technique`. That's
the same boundary that was hardest to label. My opinions are full of dish and
ingredient names ("Pasta alla zozzona… cured pork… tomatoes"), and with only
29 training examples, the model seems to treat food words as a sign of
`technique` instead of looking for an actual method.


---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.65 | MISSED | Seed 7 scored 0.467. Seeds 42 and 2024 scored 0.667 |
| 2 | F1 on `technique` | ≥ 0.70 | MISSED | Seed 7 scored 0.619. Seeds 42 and 2024 scored 0.727 and 0.722 |
| 3 | Every label F1 | ≥ 0.45 | MISSED | `opinion` scored 0.000 in all three seeds |
| 4 | Agreement with staff labels | ≥ 80% | MET | 30/30 = 100%, from one measurement that doesn't vary by seed |
| 5 | Confidence gap | ≥ 0.15 | MISSED | Seed 42 gap was 0.10. Seeds 7 and 2024 were 0.40 and 0.30 |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

**What the agreement report can and can't tell me.** The 30 staff posts were
pre-labelled by Claude, the same model that pre-labelled my 200 comments. Matching
staff 30/30 shows that this labeller applies a tight, written rule
consistently. So my labelling method isn't random noise. It doesn't show that
my own rules were tight. The evidence on that points the other way: Claude and
ChatGPT agreed on only about 79% of my 200 labels, and almost every
disagreement was on `technique` vs `opinion`. That gap between 100% on a
well-written rule and about 79% on mine is what separates a labelling problem
from a model problem in the diagnoses below.

What the agreement report can't tell me about is training. It says nothing
about whether the model got enough training to learn the labels. Where it rules
out labelling, the cause is on the model side, and on that side the clearest
problem is how little training the model got. With 139 training examples and
batch size 16, each epoch is only 9 steps, so 3 epochs is 27 steps in total,
at a learning rate of 2e-5. That's very little for a model to move away from
guessing the most common label.

**Criteria 1 and 2 (accuracy, `technique` F1): a model that can't reach a
stable answer from this much data.** Both missed only because of seed 7, which
predicted `technique` for 29 of 30 posts. Its scores (0.467 accuracy, 0.619
`technique` F1) are what you'd get by guessing the biggest label almost every
time. This isn't a labelling problem: the labels are identical in every seed,
and on seeds 42 and 2024 the same data trained a model that separates
`technique` from `reaction` well (F1 around 0.72 and 0.76–0.78). The cause is
undertraining: 27 training steps in total (see above). That's few enough
that the outcome depends on the split. Two seeds got far enough to learn the
labels; seed 7 never moved past "say `technique`," which is where an
undertrained model starts.

**Criterion 3 (every label F1): too few examples, on a boundary I didn't apply
consistently.** `opinion` scored 0.000 in every seed. The model never predicted
it once, and nearly every real `opinion` was called `technique` (5 of 6 in seed
42, 6 of 6 in seeds 7 and 2024). Three pieces of evidence:

- **Too few examples.** Only 29 `opinion` comments in training, against 59
  `technique`. My opinions are full of dish and ingredient names, so to a model
  with this little data they look like `technique`.
- **A labelling problem, not only a model problem.** The agreement contrast
  above says my `technique`/`opinion` line was the least consistent part of my
  data: it's where the two labellers disagreed most, and the label was
  redefined partway through (`hot_take` became `opinion`). A rule that two
  careful labellers split on about one time in five gives the model mixed
  signals.
- **My definition made it harder, not easier.** The zero-shot baseline also
  scored 0.000 on `opinion` when given my written definitions, but 0.667 when
  given only the bare label names. A much bigger model found the word
  "opinion" clearer than my definition of it. That points at the definition,
  not just the amount of data.

**Criterion 5 (confidence gap): a measurement too small to be stable.** Each
third of the test split is only 10 posts, so one post moves the accuracy by
0.10. Seed 42 missed by exactly one post: it scored 0.80 vs 0.70, and one
more right answer in the top third (0.90) or one fewer in the bottom third
(0.60) would have cleared it. Seeds 7 and 2024 cleared it easily (0.40 and
0.30). This says more about how small the test set is than about whether the
model's confidence means anything. It's not a labelling problem.


---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** 30 / 30 = 100%


<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

None. Every one of the 30 matched staff.

**What the pattern in my disagreements tells me:**

With no disagreements there's no pattern to read. The real question is
whether the set was easy or the rule is tight. I think it's mostly the set,
with tight rules helping.

- **The set was easy.** The posts were separable at a glance. Every
  `analysis` post builds its argument on a number (split times, eleven weeks
  of sleep data, a remeasured route). Every `hot_take` is a one-line verdict.
  Every `reaction` is about the last few hours of the writer's own life. No
  post mixed two of these the way my r/Cooking comments did, where a story
  with a tip buried in it was normal.
- **The likely traps were covered word for word by the rules.** "Times are
  down about 3%… so obviously the shoes are the whole story" (sp_014) has a
  statistic, but it's almost the exact worked example under rule 1 (a
  statistic used as decoration is a `hot_take`). "Four minutes off. FOUR."
  (sp_021) has a time in it, but rule 3 settles it: it's a `reaction` about a
  feeling, not an argument. When the hard cases come with worked examples,
  matching staff tests reading more than judgment.
- **My own taxonomy is not this tight.** On my 200 r/Cooking comments, Claude
  and ChatGPT agreed on only about 79% of labels, and almost every
  disagreement was on one boundary (`technique` vs `opinion`, or a joke vs a
  tip). The staff rules each come with worked examples; most of mine were
  written after the disagreements turned up. A 100% here doesn't show my own
  labels are 100% consistent. It shows the gap between a rule with worked
  examples and one without.


---

## The Improvement

**What I changed:** I added more data and balanced the labels. The dataset
doubled from 200 to 400 rows, and the three labels went from lopsided (85
`technique`, 74 `reaction`, 41 `opinion`) to roughly equal (134 / 135 / 131).
Most of the new rows went to the thinnest label, `opinion` (41 → 131), but
every label grew. Everything below is part of this improvement. The Unit 5 sections above still
describe the original 200 rows.

*Where the new rows came from.* I saved two opinion-heavy r/Cooking threads,
"Your ACTUAL unpopular food opinion" and "What is your favorite dish that
others hate". I also used comments from the original 12 threads that were
never extracted (the first pass took at most 30 per thread) or were trimmed
earlier only to reduce the count. Across 14 threads there were 1,069
comments. New rows follow the same rules as the first batch: at most 100
words, and no link-only posts, context-only replies, trivia, health claims,
side arguments, or food-etiquette debates.

*How they were labelled and checked.* Claude labelled the new comments.
ChatGPT then reviewed the whole 400-row file twice. Its first review found
6 clear errors, 3 story-with-a-tip rows, and 14 context, trivia, or
etiquette rows in the new batch. It also flagged 11 rows in the original 200
that broke my own drop rules. I decided every change: 8 rows relabelled
`technique`, 15 new rows dropped, and the 11 original rows dropped. Claude
then labelled 26 replacements, and ChatGPT's second review checked them. I
decided its 4 disputed rows: 263 → `reaction`, 384 → `technique`, and 372
and 392 kept. I did not personally re-read every one of the 211 new rows.
The labels I didn't individually check are ones Claude assigned and
ChatGPT's review did not dispute.

*Final dataset.* 189 of the original 200 rows were kept and 211 are new.

| Label | Before (200 rows) | After (400 rows) |
|---|---|---|
| `technique` | 85 | 134 |
| `reaction` | 74 | 135 |
| `opinion` | 41 | 131 |

Seed-42 split of the 400 rows (train / val / test): 279 / 61 / 60. `opinion`
now has 20 test examples instead of 6, so its F1 should jump around much
less between seeds.

*Rules made explicit during the improvement.* Reviewing the new batch
exposed boundaries the original rules didn't settle. These were applied to
the new rows:

- **Praising a combination vs. teaching one.** "I love liverwurst with red
  onions and mustard… it just hits" is `opinion`. Telling someone how to make
  or change a dish ("reconstituted and chopped into small bits or blended")
  is `technique`. A food or ingredient name alone doesn't decide the label.
- **Preference vs. personal story.** If the comment is mainly a preference,
  it's `opinion`. If it's mainly a story ("My mom always kept liverwurst in
  the fridge when I was growing up…"), it's `reaction`, even when it mentions
  a combination.
- **Clearly implied corrections count as `technique`.** "Until recently I
  crushed garlic after I peeled it" and "Never salted pasta water for years.
  Bland noodles." teach a fix without stating it.
- **Jokes stay `reaction` unless there's a sincere, usable tip inside.** This
  replaces the blanket humour rule above, which conflicted with hard case 1
  (the chili joke I labelled `technique`).
- **Judging someone else's suggestion is `reaction`.** "That sounds
  unnecessarily complicated/messy" responds to another comment rather than
  saying something about food in general.

*What this changes about the comparison.* Adding rows changes which posts
land in every split. The "after" test splits contain 60 posts, not 30, and
mostly different ones. Before and after are scored on different posts, so
the comparison is between two datasets, not two models on the same data.

*Limitation.* 81 of the new `opinion` rows come from the two opinion threads.
The model may partly learn "sounds like those threads" rather than "is an
opinion".

**Which diagnosis pointed at it:** All three of the "before" diagnoses point
at too little, lopsided data:

- **Criteria 1 and 2 (accuracy, `technique` F1):** the diagnosis was a model
  that can't reach a stable answer from this much data. Seed 7 collapsed into
  calling 29 of 30 posts `technique`, the biggest label. Doubling the data
  gives the model twice as many examples, and twice the training steps per
  epoch (about 18 instead of 9) at the same settings. Balancing takes away
  the "guess the biggest label" shortcut that the collapsed seed fell into.
- **Criterion 3 (every label F1):** `opinion` scored 0.000 in all three seeds,
  and the diagnosis named too few examples first: 29 in training and 6 in
  test. Balancing gives it as many examples as the other labels.

The training settings (epochs, learning rate, batch size) were not changed.
That keeps this a data-only improvement.

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.65 | 0.583 | 0.600 | 0.617 | MISSED |
| 2. F1 on `technique` | ≥ 0.70 | 0.622 | 0.750 | 0.756 | MISSED |
| 3. Every label F1 | ≥ 0.45 | 0.370 | 0.400 | 0.345 | MISSED |
| 4. Agreement with staff labels | ≥ 80% | 100% | 100% | 100% | MET |
| 5. Confidence gap (most-sure third minus least-sure third) | ≥ 0.15 | 0.15 | 0.45 | 0.20 | MET |

Notes: 400 rows, 60 test posts per seed (20 per label). Criterion 3's lowest
label is `opinion` in every seed. Criterion 4 wasn't re-measured, since the
staff check doesn't depend on my data. Criterion 5's seed-42 gap is exactly
0.15 (14/20 − 11/20), which meets "at least 0.15" with nothing to spare.

**Confusion matrix after (seed 42, 60 held-out posts)**

| true \ predicted | opinion | technique | reaction |
|---|---|---|---|
| **opinion** | 5 | 9 | 6 |
| **technique** | 0 | 14 | 6 |
| **reaction** | 2 | 2 | 16 |

**Before and after, side by side**

| Criterion | Target | Before (42 / 7 / 2024) | Before | After (42 / 7 / 2024) | After |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.65 | 0.667 / 0.467 / 0.667 | MISSED | 0.583 / 0.600 / 0.617 | MISSED |
| 2. F1 on `technique` | ≥ 0.70 | 0.727 / 0.619 / 0.722 | MISSED | 0.622 / 0.750 / 0.756 | MISSED |
| 3. Every label F1 | ≥ 0.45 | 0.000 / 0.000 / 0.000 | MISSED | 0.370 / 0.400 / 0.345 | MISSED |
| 4. Staff agreement | ≥ 80% | 100% | MET | 100% | MET |
| 5. Confidence gap | ≥ 0.15 | 0.10 / 0.40 / 0.30 | MISSED | 0.15 / 0.45 / 0.20 | MET |
| *Macro F1 (not a criterion)* | | 0.496 / 0.262 / 0.500 | | 0.553 / 0.582 / 0.584 | |
| *Accuracy spread across seeds* | | 0.200 | | 0.034 | |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->

**Partly. It fixed what it was aimed at, but it didn't get any missed
criterion over the line except criterion 5, and overall accuracy went down.**

- **`opinion` came off zero, which balancing was meant to do.** F1 went from
  0.000 in every seed to 0.35–0.40. The model now predicts `opinion` at all
  (7, 15 and 9 times across the three seeds, against 0 before). That's still
  under criterion 3's 0.45, so the criterion is still missed. This matches my
  prediction: "off zero, but below 0.45."
- **The model got much more stable.** Accuracy spread across seeds fell from
  0.200 to 0.034. No seed collapsed: before, seed 7 called 29 of 30 posts
  `technique`. Macro F1 rose in every seed, from about 0.26–0.50 to about
  0.55–0.58. The model is better at all three labels at once, not just the
  biggest one.
- **Criterion 5 flipped to MET,** though seed 42 met it exactly at the line.
- **Overall accuracy went down in two seeds (0.667 → 0.583 and 0.617), and I
  don't think that means the model got worse.** Before, only a fifth of the
  test posts were `opinion` (6 of 30), and the model never predicted it. It
  got its accuracy by leaning on the biggest label. Now the test
  set is balanced (20 of each), so the old "say `technique`" strategy can't
  score well, and the model has to tell all three apart. Macro F1, which
  weights each label equally, went up everywhere. That's the fairer
  comparison here.
- **The caveat:** before and after were scored on different test posts (30
  vs 60, with different splits), because adding rows changes every split. So
  this compares two datasets, not one model before and after on the same
  posts. The direction of the changes is consistent across all three seeds,
  which is why I trust it more than any single number.

**Baseline vs. trained, after the improvement.** Because the data changed,
the test split changed too. So I re-ran both baselines on the new 60 held-out
posts (`test_split.csv`, seed 42 of the 400 rows), and compared them with the
trained seed-42 model (`results.json`) on exactly those posts.

| Measure | Baseline | Baseline-names-only | Trained | Difference |
|---|---|---|---|---|
| Overall accuracy | 0.383 | 0.483 | 0.583 | +0.200 |
| Macro F1 | 0.287 | 0.415 | 0.553 | +0.266 |
| F1 — `opinion` | 0.174 | 0.457 | 0.370 | +0.196 |
| F1 — `technique` | 0.507 | 0.174 | 0.622 | +0.116 |
| F1 — `reaction` | 0.182 | 0.613 | 0.667 | +0.485 |

Difference is Trained minus Baseline (with definitions). The trained model
now beats the baseline on every measure, by 0.20 accuracy and 0.27 macro F1.
Before the improvement it was level on `opinion` (both 0.000). One thing
carried over from before: the baseline still does better *without* my
definitions (0.483 vs 0.383 accuracy). On `opinion`, names-only (0.457) even
beats the trained model (0.370). The bare word "opinion" still tells a
general model more than my definition does. That points at the definition
wording, not the amount of data.

**What's still wrong:** `opinion` is still the weak label, and the error has
the same direction as before. In seed 42, 9 of 20 real opinions were called
`technique` and 6 were called `reaction`. Opinions full of dish and
ingredient names still read as `technique` to the model, and opinions told
as stories read as `reaction`. More examples got the model to notice the
label; it hasn't yet learned the boundary.



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->

Three criteria are still missed after the improvement. I made one change on
purpose: more data, balanced across the labels. With a single change, the
before/after
comparison says what that change did. Each fix below would be a second change,
and running them together would make it impossible to tell which one helped.

**Criterion 1: overall accuracy (0.583 / 0.600 / 0.617, target 0.65).**
*What I'd do:* train longer, raising `EPOCHS` from 3 to about 8 while
watching the validation score each epoch for overfitting. The diagnosis for
this criterion was undertraining. The extra rows doubled the steps per epoch
(9 → 18), but 3 epochs is still only about 54 training steps. *Why I
stopped:* it's a training change, and I'd already changed the data in this
round. Doing both at once would make it impossible to say what moved the
numbers. *Update:* I tested this afterwards as a separate stretch run. With 8
epochs, criterion 1 is met in all three seeds (0.683 / 0.767 / 0.667). See
[Stretch Goals](#stretch-goals).

**Criterion 2: F1 on `technique` (0.622 / 0.750 / 0.756, target 0.70).**
Only seed 42 missed. In that seed, 6 of 20 real `technique` comments were
called `reaction`. These are tips told as stories ("Never salted pasta water
for years. Bland noodles."), which my "a usable tip wins" rule labels
`technique` but which read like personal stories. *What I'd do:* add more
story-shaped tips to training, so the model sees that a story can still
teach. More epochs would likely help as well. *Why I stopped:* same as above.
It's another data change on top of the one being measured.

**Criterion 3: every label F1 at least 0.45 (`opinion` 0.370 / 0.400 /
0.345).** More examples got `opinion` off zero, but not to the target. The
strongest clue is the baseline: the zero-shot model scored 0.457 on
`opinion` given only the word "opinion," but 0.174 given my definition. My
definition is harder to apply than the plain word. *What I'd do:* rewrite
the `opinion` definition around what the model gets wrong: "a judgment
about a food or dish, even when it names ingredients." Then relabel the
`opinion`/`technique` boundary under the reworded rule, and add opinions from
more varied threads. 81 of the new opinions came from just two threads, so the
model may have learned those threads' style rather than the label. *Why I
stopped:* rewording the definition means relabelling and reviewing the
boundary again. That's a bigger job than the one improvement this unit asks
for, and it's the next step. *Update:* the 8-epoch stretch run also met this
criterion (lowest label F1 0.650 / 0.737 / 0.529). The `opinion` boundary was
learnable with more training, though seed 2024 (0.529) shows it's still the
least stable label.

**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->
I meant `opinion` to capture any judgment about food and `technique` anything
that teaches, but the model learned surface cues instead: in seed 42, 9 of 20
real opinions were called `technique` because they name dishes and
ingredients, and 6 were called `reaction` because they're written in the
first person. The same cue works the other way too, with 6 of 20 tips told
as stories called `reaction`, so the model learned what a comment *sounds*
like (food words → `technique`, "I" and "my" → `reaction`), not whether it
teaches, judges, or reacts.


---

## Stretch Goals

**Stretch 1: 50+ extra examples for the thinnest label (done).** `opinion`
was my thinnest label, with 41 examples and an F1 of 0.000 in every seed. I
added **90 more** (41 → 131), well past the 50 the stretch asks for. The new
examples came from two opinion-heavy r/Cooking threads ("Your ACTUAL
unpopular food opinion", "What is your favorite dish that others hate"),
plus 11 opinions from other threads so the label isn't tied to two
discussions. They follow the same rules as the original batch: the
broadened `opinion` definition, no context-only replies, at most 100 words.
This was part of the main improvement (see [The Improvement](#the-improvement)
for how the rows were labelled and checked). Effect: `opinion` F1 went from
0.000 to 0.35–0.40 across the three seeds.

**Stretch 2: second training run with a changed hyperparameter (done).**
I changed one setting: **epochs from 3 to 8.** Everything else was identical
to the "after" run: the same 400 rows, the same three seeds and therefore the
same splits and test posts, learning rate 2e-5, batch size 16. Both runs are
scored on exactly the same 60 posts per seed, so this is a clean
one-variable comparison. The diagnosis for criteria 1 and 2 pointed here:
undertraining. 3 epochs on 279 training rows is only about 54 steps.
Results: `results_three_seeds_epochs8.json`.

| Criterion | Target | 3 epochs (42 / 7 / 2024) | Verdict | 8 epochs (42 / 7 / 2024) | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.65 | 0.583 / 0.600 / 0.617 | MISSED | 0.683 / 0.767 / 0.667 | **MET** |
| 2. F1 on `technique` | ≥ 0.70 | 0.622 / 0.750 / 0.756 | MISSED | 0.684 / 0.737 / 0.727 | MISSED |
| 3. Every label F1 (lowest) | ≥ 0.45 | 0.370 / 0.400 / 0.345 | MISSED | 0.650 / 0.737 / 0.529 | **MET** |
| 4. Staff agreement | ≥ 80% | 100% | MET | 100% | MET |
| 5. Confidence gap | ≥ 0.15 | 0.15 / 0.45 / 0.20 | MET | 0.15 / 0.45 / 0.20 | MET |
| *Macro F1* | | 0.553 / 0.582 / 0.584 | | 0.683 / 0.764 / 0.657 | |
| *`opinion` F1* | | 0.370 / 0.400 / 0.345 | | 0.714 / 0.737 / 0.529 | |

Confusion matrix, 8 epochs, seed 42:

| true \ predicted | opinion | technique | reaction |
|---|---|---|---|
| **opinion** | 15 | 3 | 2 |
| **technique** | 2 | 13 | 5 |
| **reaction** | 5 | 2 | 13 |

**Did it help? Yes, clearly.** Four of five criteria are now met, up from
two. Macro F1 rose by 0.07–0.18 in every seed. The biggest change is
`opinion`: 15 of 20 real opinions are now caught in seed 42, against 5
before, and only 3 are called `technique`, against 9. So the
undertraining diagnosis was right. With 3 epochs the model hadn't trained
long enough to learn the `opinion` boundary that the extra data made
learnable. The two changes worked together: balancing gave `opinion` enough
examples, and more epochs gave the model time to use them.

**What it didn't fix:** criterion 2 is still missed, by seed 42 only (0.684
against 0.70). There, 5 of 20 `technique` comments were still called
`reaction`: tips told as stories, the same weakness as before. The confidence
gaps are unchanged (seed 42 still exactly 0.15), even though the model is
much more confident overall: average confidence on correct answers rose from
about 0.47 to about 0.74. I didn't tune epochs any further. Trying many
values and keeping the best would mean tuning on the test set.

*Caveat:* this is a stretch run on top of the improvement, not part of it.
The "after" Run Log above is still the official improvement result. The
8-epoch run shows what the remaining training headroom was.

**Not attempted: a fourth label.** My three labels already split on the
`technique`/`opinion` boundary, so a fourth label would have added another
boundary before the existing one was learned.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
