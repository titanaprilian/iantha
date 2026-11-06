# Projects

*Updated: 2026-11-06 15:23*

Outcomes requiring more than one physical step. Each Active project links to an unblocked action in `next-actions.md`; replace that link when the action is completed. Put projects blocked by others On Hold and track the blocker in `waiting-for.md`.

## Unclarified

Projects captured and staged from `/clarify` that await task breakdown via `/project`.




## Active

### P01 — Strengthen Go Engineering Skills
- **Outcome / Done:** Build a Go CLI that checks URLs concurrently, handles cancellation and timeouts, reports errors clearly, and passes tests under the race detector.
- **Status:** Active
- **Next Action ID/Name:** A04 · Define CLI behavior and initialize module (two sessions)
- **Tasks:**
  - A04 · Define the CLI's inputs, output, and error behavior; initialize the Go module and package structure across two 50-minute sessions.
  - A05 · Implement sequential URL checking with `net/http`, request timeouts, and wrapped errors.
  - A06 · Add a bounded worker pool with cancellation and predictable result reporting.
  - A07 · Test success, HTTP errors, timeouts, and cancellation with `httptest`; run the race detector.
  - A08 · Benchmark sequential versus concurrent checks against a local test server; record the results.

### P02 — Learn Mock Interview Software Engineer
- **Outcome / Done:** Complete one timed coding mock and one mock covering project explanation and behavioral questions; review both and record three specific improvement actions.
- **Status:** Active
- **Next Action ID/Name:** A09 · Prepare coding interview explanation checklist
- **Tasks:**
  - A09 · Select one coding interview problem and prepare a short checklist for explaining your approach, complexity, and trade-offs aloud.
  - A10 · Complete a timed mock: solve the selected problem while explaining your reasoning aloud; note what went well and what stalled.
  - A11 · Record a five-minute explanation of one project, covering its design, trade-offs, and one challenge; review it and note improvements.
  - A12 · Draft and practice concise STAR answers to five common behavioral questions.
  - A13 · Run a timed mock covering coding, project explanation, and behavioral questions; write three specific improvement actions.

### P03 — Read The Pragmatic Programming Book
- **Outcome / Done:** Finish the book and produce concise notes with at least five practices to apply to current Go or interview-preparation work.
- **Status:** Active
- **Next Action ID/Name:** A14 · Set up reading log
- **Tasks:**
  - A14 · Set up a reading log and note the book's sections; choose a comfortable reading format and place.
  - A15 · Read the first portion of the book and record three ideas or questions in the log.
  - A16 · Read the next portion and add three ideas or questions; note a practice relevant to Go work.
  - A17 · Finish the book and capture key takeaways in the reading log.
  - A18 · Choose five practices from the notes and write one concrete application for the Go project or interview preparation.

### P04 — Learn maximizing AI Agents workflow
- **Outcome / Done:** Compare two AI-agent workflow approaches, build a small agent-assisted workflow reusable in the Go project, and document what worked, limitations, and when to use it.
- **Status:** Active
- **Next Action ID/Name:** A19 · Find and save workflow references
- **Tasks:**
  - A19 · Find and save the specific “poteto” and Matt Pocock workflow references; write down what to learn from each.
  - A20 · Study the first workflow and document its steps, tools, and one use case for the Go project.
  - A21 · Study the second workflow and document its steps, tools, and one use case for the Go project.
  - A22 · Apply one approach to a bounded Go task; record the prompt/context, review steps, and result.
  - A23 · Compare the approaches and write a reusable checklist covering suitable tasks, verification, and limitations.
## On Hold

## Completed
