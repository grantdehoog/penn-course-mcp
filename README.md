# penn-course-mcp

An [MCP](https://modelcontextprotocol.io) server for **University of Pennsylvania
course planning**, built on the open-source [Penn Courses](https://github.com/pennlabs/penn-courses)
(Penn Course Plan / Penn Course Review) public API.

It lets an LLM (Claude Desktop, Claude Code, or any MCP client) search the Penn
course catalog, inspect sections and meeting times, read ratings, and do real
planning work — detecting schedule conflicts, assembling a weekly schedule, and
comparing courses side by side.

- ✅ **Works with zero configuration** against the public Penn Courses API.
- 🔓 **Optional auth** unlocks detailed Penn Course Review breakdowns; everything
  degrades gracefully when no credentials are set.
- 🔌 Runs over **stdio** (local clients) or **streamable HTTP** (hosted).

## Tools

| Tool | What it does |
| --- | --- |
| `get_current_semester` | Active term code (e.g. `2026C`) and review-auth status |
| `search_courses` | Search catalog by code or keyword; returns summaries + ratings |
| `get_course_details` | Full course info: description, prereqs, attributes, sections, meeting times |
| `list_course_sections` | Sections with formatted meeting times/instructors; filter by status/activity |
| `get_course_ratings` | Public aggregate ratings (quality, difficulty, workload) |
| `get_course_reviews` | Detailed PCR reviews when authenticated; falls back to aggregates otherwise |
| `find_courses_by_attribute` | Courses carrying a given attribute / Gen-Ed code |
| `find_courses_by_requirement` | Courses fulfilling a requirement (by code/name) |
| `check_schedule_conflicts` | Detect time conflicts among a set of section ids |
| `build_schedule` | Weekly grid, total credits, conflicts, missing-companion warnings |
| `compare_courses` | Side-by-side ratings / difficulty / workload / prereqs |
| `recommend_courses` | Search and rank by quality, difficulty, or workload |

Course codes look like `CIS-1200`; section ids look like `CIS-1200-001`.

## Installation

```bash
# with uv (recommended)
uv pip install -e ".[dev]"

# or with pip
pip install -e ".[dev]"
```

## Running

```bash
# stdio (default) — for Claude Desktop / Claude Code
penn-course-mcp

# streamable HTTP — serves http://127.0.0.1:8000/mcp
penn-course-mcp --transport http --port 8000

# dev / MCP Inspector
fastmcp dev src/penn_course_mcp/server.py
```

### Claude Desktop / Claude Code config

```json
{
  "mcpServers": {
    "penn-course": {
      "command": "uvx",
      "args": ["penn-course-mcp"],
      "env": {
        "PENN_COURSES_SESSION_COOKIE": ""
      }
    }
  }
}
```

(Use `"command": "penn-course-mcp"` instead if you installed it into a venv on your PATH.)

## Configuration

All environment variables are optional (see [`.env.example`](.env.example)):

| Variable | Default | Purpose |
| --- | --- | --- |
| `PENN_COURSES_BASE_URL` | `https://penncoursereview.com` | API base URL |
| `PENN_COURSES_SEMESTER` | `current` | Default semester (`current` auto-resolves) |
| `PENN_COURSES_CACHE_TTL` | `3600` | Cache TTL (seconds) for catalog/detail data |
| `PENN_COURSES_TIMEOUT` | `20.0` | HTTP timeout (seconds) |
| `PENN_COURSES_USER_AGENT` | `penn-course-mcp/<ver>` | Sent with every request |
| `PENN_COURSES_SESSION_COOKIE` | _(unset)_ | Enables detailed reviews (see below) |
| `PENN_COURSES_TRANSPORT` / `--transport` | `stdio` | `stdio` or `http` |
| `PENN_COURSES_HOST` / `--host` | `127.0.0.1` | HTTP host |
| `PENN_COURSES_PORT` / `--port` | `8000` | HTTP port |

### Optional: detailed reviews

The public API already exposes **aggregate** ratings (course/instructor quality,
difficulty, work required) — no auth needed. The detailed per-instructor Penn
Course Review breakdowns require a logged-in Penn session. To enable them, log in
to penncoursereview.com in your browser, copy your session cookie, and set:

```bash
export PENN_COURSES_SESSION_COOKIE="sessionid=..."
```

Without it, `get_course_reviews` returns the public aggregate ratings plus a note
— it never errors.

## Development

```bash
uv pip install -e ".[dev]"
pytest          # pure planning logic + mocked client + tool tests
ruff check .
```

The planning logic (`src/penn_course_mcp/planning.py`) is pure and network-free —
schedule-conflict detection, time formatting, and comparison are fully unit-tested.

## Notes & data quirks

- Meeting times use Penn's `HH.MM` encoding (`10.15` = 10:15, `15.3` = 15:30); the
  server always renders them as readable `HH:MM` ranges.
- Day codes are `M/T/W/R/F` (`R` = Thursday).
- Back-to-back meetings (one ending exactly when the next starts) are **not** flagged
  as conflicts.
- This is an unofficial tool that consumes the public Penn Courses API. Please use
  it respectfully (it caches responses and caps concurrency).

## License

MIT
