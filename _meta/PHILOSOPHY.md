# Why This Exists

I got tired of repeating myself to AI agents.

Every project, every session, I'd say the same things: commit and push after every change, don't suggest when I tell you to fix, write in plain English, don't stop until the job is done. I'd correct the same mistakes: agents silently changing UI when I asked for a refactor, making up business logic instead of asking, leaving three dev servers running on different ports.

So I built this. One place where all my rules live. One bootstrap script to stamp them into every new project. Agents follow my workflow from the first commit.

The rules come from real experience -- hundreds of hours of AI-assisted development across Python/Flask, React Native, Next.js, and more. They evolved from corrections I made in actual sessions, patterns I noticed in my chat histories, and mistakes I got tired of seeing.

This is not a framework. It's not a philosophy manifesto. It's practical rules that make agents work the way I want them to.

**Ponytail** ([DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail), MIT) is the always-on coding posture. Tier 1 integrations: [unslop](https://github.com/MohamedAbdallah-14/unslop) anti-slop, [codegraph](https://github.com/colbymchenry/codegraph), [babysitter](https://github.com/a5c-ai/babysitter) gate discipline — all baked into rules, no extra npm. Protocols still own scope, gates, and multi-agent rigor. When they disagree, agents surface options instead of silently picking -- see `_meta/RULE-CONFLICTS.md` and README § Rule Preferences in each project.
