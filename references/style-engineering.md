# Style Field Engineering Reference

Suno's Style field weighs early descriptors most strongly. Treating the Style field as structured production engineering—rather than a bag of adjectives—dramatically improves genre accuracy, vocal character, mix clarity, and arrangement coherence.

---

## The 12-Slot Front-Loaded Architecture (Hard Limit: 1,000 chars)

Put **Slots 1–5 inside the first ~200 characters**. Use comma-separated English production descriptors (never prose paragraphs, never sung lyrics, never artist/label/song names). **8–14 strong descriptors beat 30 weak adjectives.** Treat 1,000 characters as a ceiling, never a quota to pad.

| Slot | Content | Example |
| :---: | :--- | :--- |
| **1. Genre** | Primary genre + subgenre | `melodic deep house` / `traditional Brazilian forro` / `1970s classic hard rock` |
| **2. Tempo** | Exact BPM | `122 BPM` |
| **3. Key** | Musical key | `key of Em` |
| **4. Vocal Persona** | 8–15 word persona (register, timbre, mic proximity, phrasing, restraint/power) OR `"instrumental only, no vocals"` | `airy dream-pop soprano with close-mic intimacy melting into wide reverb halos` |
| **5. Mood & Energy** | Emotional color + energy level | `bittersweet longing, building tension, lush atmospheric lift` |
| **6. Signature Instruments & Roles** | 2–4 concrete instruments + what they **DO** | `rolling analog sub bass locking with kick, warm Rhodes 7th chords, cascading synth arpeggios answering the vocal` |
| **7. Groove / Rhythm Feel** | Drum/percussion pattern & pocket | `crisp 4/4 kick with shuffled open hi-hats, gentle sidechain breath` |
| **8. Harmony** | Chord movement or modal character | `minor-7th Dorian modal progression with suspended tension` |
| **9. Production & Mastering** | Mix direction suited to aesthetic | `warm analog tape saturation, clear lead vocal separation, wide stereo imaging, controlled low end` |
| **10. Arrangement Arc & Ending** | Structure + ending behavior | `concise radio arc with quiet bridge before escalated final chorus, clean resolved ending after last sung word` |
| **11. Hook DNA** | Earworm / motif directive | `sticky 4-word chorus mantra, 1-beat anticipation gap before drop` |
| **12. Atmosphere & Sonic Twist** | Spatial room + 1 unexpected genre-compatible detail | `late-night coastal skyline ambience, delicate plucked kalimba counterpoint in breakdown` |

### Ending Cue Rules
- **Complete vocal songs (`create`, `radio`, `acoustic`, `live`)**: Finish all sung words before a concise instrumental tail and end clearly.
- **Short clips (`tiktok`)**: Keep intro absent and outro brief.
- **Club / Extended (`extended`, `beatport_club`)**: Preserve DJ-friendly intro and mix-out outro space.
- **Continuation / Partial / Texture (`extend`, `replace_section`, `sounds`)**: Do **not** force a final ending cue.
- **Instrumental tracks**: Describe musical resolution purely in orchestration/harmonic terms with zero vocal cues.

---

## Rich Vocal Personas ("Build a Persona, Not a Gender")

Never write just `"female vocal"` or `"male vocal"`. Specify register, tone, microphone proximity, phrasing, and dynamic control:

### Electronic & Crossover Personas
- `ethereal_female`: *Young dream-pop soprano with an airy tone, close-mic intimacy melting into wide reverb halos, never forcing tension.*
- `sensual_whisper_female`: *Seductive close-mic breathy female singer delivering soft melodic lines in a warm 3 a.m. style, rich in delicate phrasing and intimacy.*
- `pop_crossover_female`: *Breathy pop alto with polished crossover clarity, effortless upper mid-register, selling the chorus without straining.*
- `vintage_alto`: *Sultry vintage-pop alto carrying dark melancholic chest tones with lush reverb halos and slow, breathy cinematic delivery.*
- `intimate_soprano`: *Intimate high-register soprano delivering soft, airy lines with restrained emotional weight and controlled dynamics.*
- `deep_alto`: *Warm deep alto projecting controlled, relaxed studio clarity and grounded emotional presence.*
- `falsetto`: *Crystalline upper-register male falsetto on the edge of break, rising expressively on key emotional phrases.*
- `whispered_asmr`: *Ultra-close-mic hushed singing with soft breathy diction, barely above a whisper so the listener leans in.*
- `indie_folk_male`: *Vulnerable acoustic-folk male storyteller tone, conversational and close, never pushing above mezzo-forte.*
- `duet_male_female`: *Alternating male and female leads moving from intimate solo verses into unified layered chorus harmonies.*

### Multi-Genre Vocal Personas
- `natural_female` / `natural_male`: *Natural lead with clear diction and expressive genre-appropriate phrasing.*
- `country_duet`: *Two lead voices in close country/sertanejo harmonies with conversational storytelling.*
- `roots_lead`: *Earthy roots lead with direct storytelling and an unforced natural tone.*
- `samba_lead`: *Rhythmically agile samba lead with warm communal call-and-response chorus.*
- `rock_lead`: *Expressive rock lead with controlled rasp and dynamic band projection.*
- `rap_lead`: *Articulate rhythmic rap delivery with internal rhymes and deliberate breath placement.*
- `melodic_rap`: *Melodic rap with rhythmic verses and a clear sung refrain.*
- `mc_lead`: *Rhythmic MC lead with percussive articulation and crowd call-and-response.*
- `soul_lead`: *Soulful expressive lead with supported dynamics and tasteful melodic ornaments.*
- `funk_lead`: *Rhythmic soulful lead with percussive phrasing, dynamic accents, and tight backing-vocal responses.*
- `rnb_lead`: *Smooth melodic soulful lead with tasteful melisma, intimate phrasing, and stacked backing harmonies.*
- `choir`: *Balanced choir harmonies with clear diction and responsive ensemble dynamics.*
- `jazz_lead`: *Intimate jazz lead with flexible swing phrasing and subtle melodic variation.*
- `blues_lead`: *Expressive blues lead with blue-note inflections, gentle grit, and conversational call-and-response.*
- `classical_lead`: *Classically supported lyrical voice with clear diction and acoustic hall projection.*
- `friendly_lead`: *Warm, clearly articulated sing-along lead in a comfortable age-appropriate range (children's music).*
- `group_pop`: *Contrasting pop group leads with tight harmonies and rhythmic unison hooks.*

---

## Mastering Signatures (Trademark-Free)

| ID | Descriptor for Style Field | Best For |
| :--- | :--- | :--- |
| `natural_dynamic` | natural acoustic balance, preserved transients, expressive dynamic range | Acoustic, jazz, folk, MPB, singer-songwriter |
| `warm_band` | warm live-band balance, clear midrange, controlled low end | Rock, country, soul, funk, Latin bands |
| `vocal_clear` | intelligible lead vocals, natural sibilance, balanced accompaniment | Gospel, R&B, ballads, children's songs |
| `punchy_modern` | controlled modern impact, clear transients, no harsh clipping | Contemporary pop, hip-hop, trap, reggaeton, modern sertanejo |
| `orchestral_dynamic` | natural orchestral soundstage, wide expressive dynamic range | Classical chamber, cinematic orchestral scores |
| `warm_soulful` | warm analog tape saturation, smooth high-end roll-off at 16 kHz, rich midrange | Classic/UK deep house, soulful house |
| `wide_berlin` | ultra-wide stereo imaging, surgical low end below 80 Hz, spacious reverb tails | Melodic techno, progressive house, Berlin deep |
| `deep_melodic` | deep sub-bass focused mix, dark polished low end, cinematic peak compression | Melodic/emotional deep house, underground house |
| `cinematic_wide` | cinematic wide soundstage, pristine vocal clarity, lush reverb preservation | Atmospheric house, film cues, dreamwave |
| `bright_tropical` | bright punchy transients, crisp high-end sheen, energetic dancefloor snap | Sunset/tropical house, upbeat dance |
| `lofi_organic` | lo-fi tape character compression, gentle harmonic warmth, softened transients | Lo-fi chillhop, 90s boom-bap, organic house, synthwave |

---

## Rhythm Feels, Harmony Controls & Atmospheres

### Rhythm Feels
- `genre`: preserve the selected subgenre's authentic rhythm
- `laid_back`: laid-back behind-the-beat phrasing
- `driving`: forward-moving energetic pulse
- `syncopated`: emphasized syncopated accents within the chosen tradition
- `swing` / `shuffle`: supple swung subdivision / rolling triplet shuffle
- `half_time`: half-time rhythmic feel at the selected BPM
- `rubato`: expressive rubato with breathing phrases (no rigid drum grid)
- `straight`: clear even subdivision and stable pulse
- Specialized pockets: `old_school_breakbeat`, `east_coast_boom_bap`, `west_coast_gfunk`, `southern_bounce`, `rap_rnb_pocket`, `funk_on_one` (strong accents on beat 1), `neo_soul_pocket` (organic behind-the-beat live pocket)

### Harmony Controls
- `genre`: genre-authentic harmony
- `simple_tonal`: clear functional tonal harmony and singable contour
- `extended`: 7ths, 9ths, 11ths, and smooth voice-led extensions
- `modal`: hypnotic modal color and sustained tonal centers
- `blues`: dominant-7th `I–IV–V` with blue-note inflections
- `loop`: coherent repeated harmonic loop supporting rhythmic phrasing
- `classical`: functional harmonic development and thematic counterpoint
- `dominant_vamp`: short dominant-7th vamp with rhythmic ensemble variation

### Atmospheres (Match to Genre)
- **Acoustic / Live**: `recording_room`, `small_stage`, `concert_hall`, `arena`, `warm_home`, `countryside`, `roda` (communal circle gathering), `worship_space`, `playroom`, `street`, `cinematic_natural`
- **Electronic / Nocturnal**: `sunset_beach`, `rooftop`, `underground_club`, `late_night_drive`, `oceanic`, `luxury_lounge`, `ibiza` (sunrise beach-club energy), `rainy_urban`, `cinematic`, `abandoned_warehouse`, `forest_at_dawn`, `empty_subway`, `desert_midnight`

---

## Neutral Instrument Accents (No Accidental Genre Drift)

Adding an instrument must never drag the song into an unrelated cultural stereotype (for example, adding accordion to Brazilian forró must not create a French waltz). Always phrase accents neutrally so character comes from the primary genre:
- *Strings/Plucked*: `acoustic guitar`, `nylon-string guitar`, `electric guitar`, `seven-string acoustic guitar`, `cavaquinho`, `viola caipira`, `pedal steel guitar`, `requinto guitar`, `banjo`, `ukulele`, `harp`, `sitar`, `violin`, `cello`, `string quartet`, `upright bass`, `electric bass`
- *Keys/Synths*: `acoustic piano`, `grand piano`, `Rhodes electric piano`, `Hammond organ`, `clavinet`, `accordion`, `analog pads`, `FM electric piano`, `rave piano`, `arpeggiator`, `granular textures`, `distorted synth bass`
- *Winds/Brass*: `saxophone`, `trumpet`, `brass section`, `short horn stabs`, `woodwinds`, `harmonica`
- *Percussion/Production*: `live acoustic drums`, `brushed drums`, `808 bass`, `rolling trap hi-hats`, `1980s drum machine`, `gated-reverb snare`, `turntable scratches`, `chopped breakbeats`, `pandeiro`, `tantan`, `zabumba`, `triangle`, `congas`, `timbales`, `bongos`, `guira`, `guiro`, `dembow`, `tamborzao`, `hand percussion`, `tabla`, `marimba`, `xylophone`, `kalimba`, `steelpan`, `vibraphone`, `handclaps`, `dub echo`, `tape saturation`, `vinyl texture`, `sidechain pumping`, `8D spatial audio (centered kick and sub, orbiting stereo FX)`
- *Vocal Accents (vocal mode only — omit in instrumental mode)*: `soul/R&B backing harmonies`, `gospel choir`, `rhythmic vocal chops`

---

## Specialized 80s / Synthwave Tag Toolkit

When building 1980s Synthwave / Retrowave tracks, front-load tags in this exact bucket order:
`styles` → `electronic` → `energy/melancholic/dark` → `instruments` → `vocals` → `moods`.

| Preset | BPM Hint | Core Tags |
| :--- | :---: | :--- |
| `classic` | 105–120 | `80s synthwave, retro electronic, analog synths, gated reverb drums, pulsing bassline, cinematic pads, midnight highway, night drive, emotional vocal, anthemic chorus` |
| `high_energy` | 118–128 | `outrun synthwave, high energy synthwave, driving synthwave, 80s drum machine, aggressive synth bass, arpeggiated synths, retro racing energy, anthemic chorus` |
| `melancholic` | 95–110 | `melancholic synthwave, dreamwave, soft analog synths, slow pulsing bassline, 80s drum machine, lonely night drive, breathy female vocal, emotional vocal` |
| `dark_cyberpunk` | 100–118 | `dark synthwave, dystopian synthwave, heavy synth bass, arpeggiated synths, gated reverb drums, noir electronic, deep male vocal` |
| `synthpop` | 108–122 | `80s synthpop, new wave, bright analog synths, clean drum machine, romantic synthwave, catchy vocal melody, glossy production, emotional female vocal` |

> Note: Keep retro city/skyline mood descriptors in the **Style** field only if relevant, and keep the word `neon` completely out of **sung lyrics**.

---

## Exclude Styles Matrix (Hard Limit: 600 chars)

**Never apply one blanket Exclude list to every genre.** Match exclusions to the genre family:

1. **Deep House / Melodic / Organic / Atmospheric / Tech / Underground Electronic Baseline**:
   `EDM big-room drops, future bass synth pluck drops, modern dubstep wobbles, trap hi-hat rolls, country guitar, metalcore breakdowns, auto-tuned rap delivery, pop punk power chords, screaming, shouting, strained vocals, harsh vocals, aggressive singing, overacting, rock-style vocals, belting`
   - Per-subgenre additions:
     - `classic_deep`: `+ aggressive techno kicks, 180 BPM hardstyle`
     - `melodic_deep`: `+ lo-fi tape hiss, spoken-word rap`
     - `organic_house`: `+ heavily synthesised supersaws, EDM festival risers`
     - `atmospheric_house`: `+ aggressive distortion, fast 4-to-the-floor punk`
     - `club_deep`: `+ lo-fi tape character, ambient drone`
     - `sunset_house`: `+ dark industrial kicks, Berlin techno hardness`
     - `emotional_deep`: `+ happy hardcore, comedic chiptune`
     - `underground_deep`: `+ pop chart vocals, tropical house plucks`
     - `tech_house`: `+ dreamy ambient pads, orchestral score`
     - `downtempo_deep`: `+ fast techno kicks, EDM festival drops`
     - `indie_dance`: `+ heavy bass-music subs, metalcore breakdowns`
     - `edm` (2000s vocal trance): remove `future bass synth pluck drops` from baseline; add `slow lofi hip-hop, acoustic folk guitar, heavy industrial techno, aggressive hardstyle kicks, distorted rawstyle drops`
2. **80s Synthwave / Retrowave**:
   `modern trap, heavy metal, acoustic folk, trap beat, reggaeton dembow, dubstep, country, drill, hyperpop, lo-fi hip hop`
3. **Acoustic, Roots, Brazilian, Rock, Hip-Hop, Funk/Soul/R&B, Latin, Jazz/Blues, Classical, Gospel, Children's**:
   Start from an **empty** baseline and exclude only genuine clashes (e.g., for acoustic jazz/classical/country/samba: `EDM drops, heavy sidechain pumping, auto-tuned rap, dubstep wobbles, aggressive metal distortion`; for boom-bap rap: `four-on-the-floor EDM, country fiddle, heavy metal screaming`; for children's music: `dark industrial, aggressive screaming, heavy metal distortion, explicit club drops`).
4. **Instrumental Mode (ANY Genre)**:
   Always append: `vocals, singing, spoken word`.
