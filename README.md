# skill-suno-premium

A universal, harness-agnostic **Agent Skill** for creating release-ready songs, Style prompts, lyrics, instrumental blueprints, and sound fusions for **Suno AI Custom Mode (v6 / v5)**.

Built around the open [Agent Skills (`SKILL.md`) specification](https://agentskills.io), `skill-suno-premium` works across **Claude Code, Cursor, OpenAI Codex, Google Antigravity, Gemini CLI, GitHub Copilot, Windsurf, Cline, Roo Code, OpenCode, Hermes Agent**, and plain LLM chat interfaces—with a zero-dependency Python 3 validator included.

---

## What Is Inside

- **81+ Curated Genre & Subgenre Profiles across 12 Musical Families**: Electronic (36), Synthwave (5), Country & Sertanejo (3), Brazilian Rhythms (7), Pop/Rock/Indie (8), Hip-Hop/Rap/Trap (5), Funk/Soul/R&B (4), Latin/Reggae/Afrobeats (7), Jazz/Blues (2), Classical/Instrumental (2), Gospel (1), and Children's Music (1)—each with authentic BPM ranges, keys, rhythms, ensembles, harmonies, and control defaults.
- **Genre Sovereignty**: Prevents electronic defaults (4/4 kicks, sidechain pumping, DJ intros, festival risers) from contaminating acoustic, roots, jazz, classical, rock, or Latin tracks unless a fusion is explicitly requested.
- **12-Slot Front-Loaded Style Architecture**: Prioritizes genre, BPM, key, rich vocal personas (8–15 words), mood, active instrument roles, groove, harmony, mastering signature, arrangement arc, hook DNA, and sonic twist within Suno's 1,000-character budget.
- **Addictive Songcraft & Lyric Diversity Engine**:
  - 3-candidate divergent concept planning with rotating narrative viewpoints and sensory lenses
  - 8 earworm laws (hook gravity, tension → gap → payoff, escalation without copy-paste, prosody)
  - **Classic** vs **ReMi** writing modes
  - 10 arrangement contracts (`radio`, `extended`, `beatport_club`, `full_8min`, `tiktok`, `acoustic`, `live`, `aaba`, `blues12`, `through_composed`)
  - Multilingual lyric separation (write sung lyrics in English, Portuguese, Spanish, French, Arabic, etc., while keeping Style, exclusions, section tags, and performance cues in English)
  - Phonetic polish for AI singers (spelled-out numbers/times, spaced acronyms, vowel stretching, breath ellipses)
  - Anti-slop and multilingual anti-cliché filtering
- **Emotional & Compositional DNA**: 8 emotional themes, 5 intensity tiers (`subtle`, `building`, `peak`, `raw`, `dopamine`), 10 weighted emotional microstates, compositional grammar (anti-escalation, negative space, evolving loops, fragile dynamics), section × instrument vocabulary, and spatial/binaural arcs.
- **All 9 Suno Workflows + Creative Sliders**: Ready-to-paste guidance for `create`, `upload_audio`, `add_vocals`, `remix_cover`, `extend`, `replace_section`, `stem_extraction`, `inspire`, and `sounds`, plus calibrated `Weirdness` / `Style Influence` / `Audio Influence` targets and Suno v6 `Variety = 0` fidelity advice.
- **Trademark-Free Reference Translation & Dual-Reference Fusion**: Convert artist references into pure sonic descriptors (zero artist/label/song leaks) and fuse an artist's production DNA with a reference track's harmonic/melodic DNA.
- **Zero-Dependency Deterministic Validator (`scripts/validate_song.py`)**: Validates ceilings, section contracts, instrumental rules, verse repetition, content-word dominance, AI clichés, trademark leaks, instruction leaks, phonetic readiness, and session-history novelty.

---

## Repository Structure

```text
skill-suno-premium/
├── SKILL.md                                     # Core universal skill entrypoint
├── README.md                                    # Documentation & installation guide
├── LICENSE                                      # MIT License
├── references/
│   ├── genre-catalog.md                         # 81+ genre profiles across 12 families
│   ├── style-engineering.md                     # 12-slot Style formula, personas, mastering, 80s kit, exclusions
│   ├── songwriting-and-craft.md                 # Earworm craft, Classic/ReMi, forms, energy maps, phonetics
│   ├── emotional-and-dna-architecture.md        # Emotions, intensities, microstates, grammar, spatial arcs
│   ├── workflows-and-fusion.md                  # 9 Suno workflows, sliders, artist DNA, fusion, refinement, occasions
│   └── quality-and-validation.md                # Deterministic QA, lexical novelty, semantic rubric, repair
├── scripts/
│   └── validate_song.py                         # Zero-dependency Python 3 CLI validator & polisher
├── examples/
│   └── example-packages.md                      # 3 complete showcase Suno packages
└── tests/
    └── test_validate_song.py                    # Automated unit test suite
```

---

## Installation (Any Harness)

### Universal CLI (`npx skills`)

Install directly into Claude Code, Cursor, Codex, Antigravity, Gemini CLI, Windsurf, Copilot, OpenCode, and more:

```bash
npx skills add cassiomc1/skill-suno-premium
```

Install globally across all projects:

```bash
npx skills add cassiomc1/skill-suno-premium -g
```

### Manual Installation by Harness

Clone the repository into your harness's skill directory:

| Harness | Project-Level Path | Global Path |
| :--- | :--- | :--- |
| **Claude Code** | `.claude/skills/skill-suno-premium` | `~/.claude/skills/skill-suno-premium` |
| **Cursor** | `.cursor/skills/skill-suno-premium` | `~/.cursor/skills/skill-suno-premium` |
| **OpenAI Codex** | `.codex/skills/skill-suno-premium` | `~/.codex/skills/skill-suno-premium` |
| **Google Antigravity** | `.agents/skills/skill-suno-premium` | `~/.gemini/config/skills/skill-suno-premium` |
| **GitHub Copilot** | `.github/skills/skill-suno-premium` | — |
| **Windsurf / Roo Code** | `.windsurf/skills/skill-suno-premium` | — |

Example manual clone:

```bash
git clone https://github.com/cassiomc1/skill-suno-premium.git ~/.claude/skills/skill-suno-premium
```

### Plain Chat / Custom GPT / Claude Projects

Upload `SKILL.md` plus any needed files from `references/` as project knowledge. The skill requires no runtime dependencies or external APIs.

---

## Using the Built-In Validator CLI

Validate any generated Suno song package locally with Python 3 (standard library only):

```bash
python3 scripts/validate_song.py --arrangement radio --workflow create < song.json
```

Useful flags:

```bash
# Auto-sanitize trademarks & apply phonetic polish, outputting cleaned JSON + audit report
python3 scripts/validate_song.py --arrangement radio --fix < song.json

# Validate an instrumental track (verifies lyrics are empty)
python3 scripts/validate_song.py --instrumental < instrumental.json

# Check novelty against previous songs in a session
python3 scripts/validate_song.py --history recent_songs.json < song.json

# Compute recommended Creative Sliders & Exclude Styles for a genre/intensity
python3 scripts/validate_song.py --recommend --style melodic_deep --intensity dopamine --arrangement radio
```

### Run the Test Suite

```bash
python3 -m unittest discover -s tests -v
```

---

## Example Prompts to Trigger the Skill

- *"Create a Suno v6 melodic deep house track at 122 BPM in E minor about driving home at sunrise after a night shift—dopamine intensity, airy female vocal, radio edit."*
- *"Write a traditional Brazilian forró in Portuguese with zabumba, accordion, and triangle for a summer hometown reunion."*
- *"Build a 12-bar blues in E major with harmonica and raspy vocals—strictly AAB stanzas, no pop chorus."*
- *"Translate a moody late-night underground Berlin house aesthetic and fuse it with an F# minor acoustic guitar progression at 118 BPM—zero artist names."*
- *"Refine my existing song: keep every single lyric unchanged, only make the drums tighter, drop BPM from 126 to 120, and add warm Rhodes chords."*
- *"Generate a cinematic instrumental orchestral soundtrack for a short film trailer—leave lyrics empty and give me Suno v6 sliders."*

---

## License

[MIT](LICENSE)
