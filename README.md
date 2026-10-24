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

**Base model:**

**Settings:** <!-- epochs, learning rate, batch size, seed -->

**Anything I changed from the defaults, and why:**

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Pre-labelling disclosure:**

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

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

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



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
