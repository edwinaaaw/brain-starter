# Brain Starter

**AI can do the work. So why are we still unable to start?**

**Most productivity tools help you plan the work. Brain Starter helps you begin it.**

Brain Starter is a Codex skill for the difficult gap between knowing and doing. It identifies what is blocking the first real action, takes over the mechanical resistance, and guides the user into one observable ten-minute start.

**AI takes over the resistance, not the growth.**

## The problem

AI can research, summarize, draft, organize, and plan. But being capable of doing the work is not the same as helping a person begin it.

When someone is stuck, another detailed plan can become another thing to process. The immediate barrier may be scattered material, low energy, perfectionism, decision overload, a missing dependency, or the friction of the first physical action.

Brain Starter intervenes at that moment. It does not wait for the user to produce a polished brief, and it does not turn every difficult start into a lesson about discipline.

## What it does

1. Detects the resistance blocking the current task.
2. Chooses the lowest effective level of AI intervention.
3. Handles mechanical preparation when tools and context allow it.
4. Preserves the part that requires the user's judgment, learning, consent, or authorship.
5. Produces one observable ten-minute start.

No motivational lecture. No full-day productivity system. No reward for planning without acting.

## Example

**User**

> I don't want to write my weekly report.

**Brain Starter**

> The report is clear; gathering and structuring the evidence is blocking the start. I can organize the materials you provide into decisions and progress, while you verify the facts and final wording.
>
> **Do only this now**  
> Review the first decision item in the draft.  
>
> **AI has completed**  
> Grouped the supplied notes into decisions and progress.  
>
> **You need to complete**  
> Confirm whether the first decision item is accurate.  
>
> **10-minute success criterion**  
> The first decision item is verified and editable.  
>
> **If you get stuck**  
> Say: “I'm stuck.”

The output is not a better intention. It is a visible change in the real task.

## Tested in real life

Brain Starter has been used in three qualitative, real-world tests:

- **Weekly reporting:** organized scattered source material and surfaced decisions, leaving factual verification and final communication to the user.
- **Business development:** clarified channel requirements, reduced research ambiguity, and helped the user reach a real outreach action.
- **Exercise:** replaced an abstract workout commitment with walking home as the first safe step; the user later completed an at-home training session.

These are early product tests, not clinical evidence or a guarantee that every user will start.

## How it works

Brain Starter routes each situation through a small set of reusable rules:

- **Resistance patterns:** identify the dominant block without labeling the user.
- **Intervention levels:** use the least AI help that makes action possible.
- **Attention warm-ups:** embed a short re-entry into the real task instead of assigning a separate lesson.
- **Field patterns:** adapt the start to work, study, administration, creation, exercise, and everyday life.
- **Momentum:** reward reported or observable action, never chat time, planning, or perfect streaks.

After interruption, Brain Starter returns to the last visible state and offers one action possible within 30 seconds. Returning is treated as part of the process, not as failure.

## Install

### Install as a Codex skill

From this repository's root:

```bash
mkdir -p ~/.codex/skills
cp -R skills/brain-starter ~/.codex/skills/brain-starter
```

Restart Codex, then start a new task with a real block:

```text
Use Brain Starter. I know what I need to do, but I cannot start.
```

You can also invoke it explicitly with `$brain-starter` when your Codex surface supports skill mentions.

### Install as a local Codex plugin

The repository also includes `.codex-plugin/plugin.json`. Import the repository folder as a local plugin in a Codex environment that supports local plugin installation. Keep it as a separate plugin; it does not need to replace another skill.

## Try it

Use a task that exists today rather than inventing one for the test:

```text
I know I need to write this, but I do not want to start.
```

```text
My head is crowded. I have two hours and low energy. Help me choose what to begin.
```

```text
I was interrupted. Take me back to the last real step.
```

```text
Give me a two-minute attention refuel, then move me into the actual task.
```

## Momentum without punishment

Brain Starter can record minimal session metadata with the included local script. It awards momentum only for real action:

- start a real action: **+2**;
- reach the observable ten-minute result: **+2**;
- begin another block: **+1**.

It never deducts momentum and does not reward chat volume, time spent in Codex, planning without action, or streak maintenance. The current release provides text-based momentum feedback only. A visual Brain Station is a future concept, not an implemented feature.

## Boundaries

Brain Starter is not:

- a diagnostic or treatment tool;
- a replacement for appropriate medical or mental-health care;
- a general long-range planner;
- a system for outsourcing consequential judgment or bodily consent;
- a detached brain-training game.

External actions such as sending messages or changing shared calendar events still require confirmation at the point of execution.

## Development

Run the tests from the repository root:

```bash
python3 -m unittest discover -s tests -v
```

## License

[MIT](LICENSE)
