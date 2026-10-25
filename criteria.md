# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Overall accuracy

Overall accuracy is at least **0.65** on the held-out test split, in all three
seeds.

**Why this target:**

Guessing gets 33%, and always predicting my biggest label (`technique`, 85 of
200) gets 42.5%. A useful model has to beat that clearly, and 0.65 is more than
20 points above it. The test split is only 30 comments, so each one is worth
about 3 points: 0.65 means getting 20 of 30 right in the worst of the three
seeds.

---

## 2. Per-label: `technique`

`technique` has an F1 of at least **0.70** on the test split, in all three
seeds.

**Why this target:**

It's the label the tool exists for: separating comments that teach from ones
that don't. It's also my biggest label (about 13 comments in each test split),
and it has the clearest surface signals, like instructions ("Cut the top and
bottom off"), quantities and ingredient lists. If the model can't find it
reliably, nothing else matters. So it gets the strictest target.

---

## 3. Per-label: no label falls apart

Every label has an F1 of at least **0.45** on the test split, in all three
seeds.

**Why this target:**

This is set by `opinion`, my smallest label: 41 comments, so only about 6 per
test split, and one wrong guess moves its F1 by 0.1 or more. It's also the
label whose definition changed during labelling (it started as `hot_take`), and
its boundary with `technique` was the one the two AI labellers disagreed on
most. A label that's 20% of the data would get an F1 of about 0.2 by guessing,
so 0.45 still means the model learned something. A strict target here would
just measure which seed got lucky.

---

## 4. Consistency

When I label the 30 staff posts under the staff taxonomy, I agree with the staff
labels on at least **80%** (24 of 30), measured with `agreement.py`.

**Why this target:**

Building my own dataset showed where labelling breaks down: ChatGPT kept my
pre-labels on 157 of 200 comments (78.5%), and almost every disagreement was
on one boundary, a tip versus an opinion or a joke. The staff taxonomy has the
same kind of boundary (`analysis` versus `hot_take`). If I can't apply a
written rule at least 80% of the time, the model's mistakes can't be separated
from mine.

---

## 5. Confidence

The model's most-confident third of test predictions is at least **0.15** more
accurate than its least-confident third, in all three seeds.

**Why this target:**

My data has easy and hard comments. Short compliments ("That sounds
delicious!") and step-by-step recipes should be easy calls, while stories with
a tip buried inside, and jokes that mention an ingredient, are genuinely hard,
even for me. If the model's confidence means anything, it should be right more
often on the first kind. Each third is only about 10 comments, so 0.15 means a
gap of at least 2 comments, small enough that one swing doesn't decide it.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
