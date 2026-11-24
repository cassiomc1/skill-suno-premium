# Suno Workflows, Creative Sliders, Reference Fusion & Occasions

Use this reference to adapt any song package to the exact Suno Custom Mode workflow, calibrate Creative Sliders, translate artist references cleanly without trademark leaks, fuse dual references, perform surgical refinements, or start from occasion briefs.

---

## 1. All 9 Suno Custom Mode Workflows

| Workflow ID | Purpose | Style & Lyrics Strategy |
| :--- | :--- | :--- |
| `create` | Generate a complete track from scratch | Paste `Title` + front-loaded `Style` + complete `Lyrics` + `Exclude Styles`. Preserve ending cleanly. |
| `upload_audio` | Transform an uploaded 6–60s audio clip | Focus `Style` on the **transformation direction** (new genre/arrangement/mood). Set **Audio Influence 25–50%** (default 40%) so the upload guides without rigid cloning. |
| `add_vocals` | Add vocals to an existing instrumental | Provide complete lyrics with clear section tags. Focus `Style` on vocal persona, phrasing, and leaving mix space for the existing instrumental bed. |
| `remix_cover` | Reimagine an existing track in a new style | Describe the **NEW arrangement**, not the original. Put the original genre's unwanted clichés into `Exclude Styles`. |
| `extend` | Continue an existing track seamlessly | Write **only the continuation lyrics** (do not restart from `[Intro]`). Match existing key/BPM/groove in `Style`. Do not force a premature ending unless this extension closes the track. |
| `replace_section` | Regenerate a single section in Song Editor | Write **only the self-contained replacement section(s)** (e.g., `[Bridge]` + `[Final Chorus]`) with matching BPM/key/vocal persona so the splice stays seamless. |
| `stem_extraction` | Produce a track intended for later stem splitting | Describe clean, separable layers in `Style` (`distinct kick, isolated bassline, clean pads, clear lead vocal`) and avoid muddy overlapping distortion. |
| `inspire` | Generate inspired by a user's own playlist DNA | Express the shared sonic/mood/instrumentation DNA in `Style`—never cite other artists' names. |
| `sounds` | Generate a one-shot sample, loop, or sonic texture | Keep `Style` concise and concrete (timbre, tempo/pitch if relevant, acoustic/synth character). Leave `Lyrics` empty (no full song arc). |

---

## 2. Target Suno Model & Creative Sliders

### Model Guidance
- **Suno v6 (Default)**: Supports long-form tracks (up to ~8 minutes) and rich Custom Mode prompt adherence. Recommend **`Variety = 0`** whenever the user wants Suno to preserve the crafted `Style` field verbatim without rewriting it.
- **Suno v5 (Legacy Compatibility)**: Use only when the user explicitly asks to prepare or audit legacy v5 prompts.

### Creative Slider Presets (Paste Targets — Suggestions, Not Guarantees)

| Intensity | Weirdness | Style Influence | Audio Influence |
| :--- | :---: | :---: | :---: |
| `subtle` | **35%** | **82%** | 0% |
| `building` | **55%** | **75%** | 0% |
| `peak` | **50%** | **80%** | 0% |
| `raw` | **65%** | **70%** | 0% |
| `dopamine` | **58%** | **78%** | 0% |

**Automatic Modifiers**:
- `tiktok` arrangement: `+5%` Weirdness (cap 70%), `-3%` Style Influence (floor 70%).
- `full_8min` arrangement: `+5%` Style Influence (cap 90%).
- Audio reference uploaded (`upload_audio`, `remix_cover`, etc.): set **Audio Influence = 40%** (recommended range 25–50%).

---

## 3. Trademark-Free Artist-to-Sonic-DNA Translation

When a user says *"make it sound like [Artist / Producer / Label / Track]"*:

1. **Decompose into Pure Sound Attributes**:
   - Closest catalog `style_id`, realistic `bpm` (clamped to genre range), and typical `key`
   - Compatible `vocal_style`, `vibe`, and `atmosphere`
   - `aesthetic_description`: 1–2 concise comma-separated production phrases (drums, synths/instruments, room tone, groove feel)
   - `mastering_description`: 1 concise mix/mastering phrase (tape warmth, transient punch, stereo width, low-end character)
2. **Scrub Every Trademark Token**: Never allow the named artist, any related artist, record label, club venue, or song title to appear in `Title`, `Style`, `Lyrics`, or `Exclude Styles` (also strip space-stripped, hyphenated, and underscored variants).
3. **Examples of Safe Translation**:
   - *Underground Berlin melodic/deep club sound* → `Berlin progressive hypnotic, warm analog sub bass, crisp 909 percussion, wide stereo pads`
   - *Filtered retro disco-house sound* → `filtered disco-house, funky slapped electric bass, shimmering string stabs, crisp four-on-the-floor groove`
   - *Acoustic folk-house crossover* → `acoustic indie-folk crossover, fingerpicked nylon guitar, warm melodic bass, airy intimate vocal`
   - *Classic 1970s funk pioneer feel* → `1960s and 1970s American funk, strong accents on the one, syncopated bass and muted rhythm guitar, clavinet, short brass stabs`

---

## 4. Dual-Reference Fusion Engine

When the user supplies **both** an Artist sonic aesthetic **and** a Reference Track (e.g., chord progression, BPM, key, or Spotify/Tunebat audio features like energy, danceability, valence/happiness, acousticness):

1. **Synthesize—Never Pick Only One Side**:
   - **Artist Side → Production DNA**: Drums, mix/mastering character, groove pocket, and instrument palette.
   - **Reference Track Side → Melodic & Emotional DNA**: Hook contour, harmonic intervals/chords, and emotional atmosphere.
2. **BPM Bridge**: `target_bpm = round((bpm_artist + bpm_reference) / 2)`, clamped to a musical tempo fitting the chosen genre.
3. **Key / Modal Bridge**: If keys differ, lean modal—reuse the reference track's harmonic motion voiced inside the target genre's preferred key/mode.
4. **Audio-Feature Translation** (if numerical reference features are provided):
   - `energy >= 70` → `high energy drive`; `energy <= 40` → `restrained dynamics`; else `balanced energy`
   - `danceability >= 65` → `danceable groove`
   - `happiness <= 40` → `melancholic color`; `happiness >= 65` → `uplifting lift`; else `bittersweet tone`
   - `acousticness >= 55` → `organic acoustic texture`
5. **Strict Originality Rule**: Never copy the reference song's melody, lyrics, title, or artist identity—and never override the user's chosen genre, vocal mode, or lyric language with those of the reference.

---

## 5. Surgical Refinement Protocol (Editing an Existing Song)

When the user asks to revise a previously generated Suno package:

1. **Merge, Never Regenerate from Scratch**: Keep everything the user did **not** ask to change (genre, BPM, key, vocal persona, arrangement, intact verses/hooks, lyric language).
2. **Classify Refinement Intent First**:
   - **Lyrics-only edit** (e.g., *"change Verse 2 to mention the train station"*, *"make the chorus hook shorter"*): Keep `Style` unchanged (unless a new vocal cue requires it) and surgically edit only the requested lines/sections.
   - **Style / Production-only edit** (e.g., *"keep the lyrics unchanged, make it 124 BPM with warmer Rhodes and punchier drums"*, *"only change the mix to lo-fi tape"*): **Preserve every single sung lyric line verbatim.** Update only `Style`, `Exclude Styles`, and sliders.
   - **Tempo / Mood shift**: Adjust BPM, key/harmony cues, atmosphere, and energy tags coherently across `Style` (and lyrics only if requested).
   - **Arrangement change** (e.g., *"turn this radio song into a TikTok clip"* or *"make it a 12-bar blues"*): Adopt the new arrangement's exact section contract and update `Style` arc cues.
3. **Refresh Derived Metadata**: Recompute character counts, BPM/key summary, and section flow from the **accepted edited output**, never from stale pre-edit notes.

---

## 6. 15 Ready-to-Use Occasion Starting Briefs

Use these as editable starting templates when a user asks for an occasion song (personalize with names, memories, and chosen language):

1. **Birthday**: Warm celebratory song highlighting specific personal memories, shared jokes, and wishes for the year ahead.
2. **Wedding**: Intimate romantic song tracing how the couple met, small everyday rituals, and a grounded vow for the future.
3. **Tribute / Memorial**: Tender, respectful tribute capturing concrete traits, voice/gestures, and lasting legacy without melodrama.
4. **Gospel / Worship**: Uplifting faith and gratitude anthem moving from quiet reflection to a communal choir-backed chorus.
5. **Children's Song**: Playful, concrete sing-along (`kids` profile) with friendly acoustic instruments, simple rhythms, and joyful age-appropriate discovery.
6. **Brand / Event Jingle**: Ultra-concise (`tiktok` form, immediate hook in first 8 bars) memorable sonic tagline with clean ending.
7. **Carnival**: High-energy syncopated celebration (`samba`, `pagode`, `forro`, or `afro_house`) with communal call-and-response percussion.
8. **New Year**: Hopeful reflection leaving behind the past year's lessons and stepping into a bright new chapter.
9. **Easter**: Themes of renewal, spring light, gratitude, and quiet rebirth.
10. **Christmas**: Cozy warm-home gathering, nostalgia, shared table details, and winter/holiday warmth.
11. **Mother's Day**: Concrete everyday moments of care, strength, and gratitude without generic greeting-card clichés.
12. **Father's Day**: Grounded tribute to guidance, quiet presence, shared routines, and enduring lessons.
13. **Independence Day / National Celebration**: Anthemic outdoor summer celebration with communal chorus energy.
14. **Thanksgiving**: Warm acoustic gathering celebrating gratitude, reunion, and shared table stories.
15. **Instrumental Soundtrack**: Pure **instrumental mode** (`Lyrics: ""`) cinematic score with a clear opening motif, dynamic orchestral/hybrid build, contrasting quiet passage, and resolved ending.
