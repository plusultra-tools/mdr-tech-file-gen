# Kill-gate — mdr-tech-file-gen

**Decision date:** d+30 from public launch (PyPI publish + Show HN + `r/medicaldevices` post + OpenRegulatory Slack drop + LinkedIn regulatory-affairs post).

**Continue if any of:**

1. **≥50 GitHub stars** on the repo (proxy: discovered outside the operator's network; MDR tooling is a niche so the bar is lower than broader dev-tool stars).
2. **≥3 real-affiliation GitHub issues** opened — issues whose author's profile shows a digital-health startup, a med-device manufacturer, a regulatory consultancy, or a Notified Body (not the operator, not generic accounts, not Linkedin spam).
3. **≥10 `pip install` per pypistats** in the trailing 14 days (proxy: someone is actually trying to scaffold a technical file).
4. **≥1 inbound** — DM, email, or LinkedIn message asking about hosted validation, custom Notified Body templates, MDR consultancy partnership, or Class IIb/III extensions.
5. **≥1 fork** of the repo with non-trivial commits (someone is integrating it into their own CI).

**Kill if none of the above.** Move to `archive/mdr-tech-file-gen/` with a post-mortem covering:
- Which distribution channel produced zero engagement (HN? `r/medicaldevices`? OpenRegulatory Slack? LinkedIn?).
- Whether the target audience (solo-founder SaMD shops) reads the channels we tried.
- Whether OpenRegulatory's free Word templates are "good enough" to suppress demand for a structured/CI-friendly alternative.
- Whether MDR-burdened founders default to consultants regardless of price, killing the bottom of the market.

**Half-life check at d+14:** if the trajectory is <25% of the d+30 thresholds (e.g., <12 stars, 0 issues, <2 installs), do not double down on distribution — preserve calories for the rest of the wave and reallocate effort to the next venture in the portfolio.

**What does NOT count:**

- Operator-created accounts / sock-puppet stars.
- Stars from the personal network (LinkedIn 1st-degree).
- Bot traffic from PyPI mirrors.
- Vague "interesting project" comments without a concrete use case or affiliation.

**What buys time without continuing:**

- A specific Notified Body (TÜV SÜD, BSI, DEKRA, etc.) saying "we'd accept output from your tool as a starting skeleton in a Class IIa submission" — that's a fork-point, not a kill, but it changes the roadmap (v0.2 brought forward, NB-specific templates added).
- An OpenRegulatory maintainer offering to integrate the schema-driven output as their git-native distribution path — that's a partnership exit, not a kill.
- A regulatory consultancy offering to white-label the hosted validator for their clients — that's an enterprise pivot, not a kill.

**What kills immediately (regardless of metrics):**

- A Notified Body publishing an explicit "we do not accept tool-generated technical files" statement.
- A clear MDCG guidance against schema-driven documentation (currently no such signal).
- A competing OSS project shipping the same scope with materially better adoption — fold and contribute, don't compete.
