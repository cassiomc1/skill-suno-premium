#!/usr/bin/env python3
"""Zero-dependency Suno AI Custom Mode song validator, sanitizer, and helper.

Part of `skill-suno-premium` (MIT License).
Requires only Python 3.10+ standard library.

Usage:
  python3 scripts/validate_song.py --arrangement radio --workflow create < song.json
  python3 scripts/validate_song.py --arrangement radio --fix < song.json
  python3 scripts/validate_song.py --instrumental < instrumental.json
  python3 scripts/validate_song.py --recommend --style melodic_deep --intensity dopamine
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
import math
import re
import sys
from typing import Any
import unicodedata


# ── Engineering Ceilings ───────────────────────────────────────────────
TITLE_LIMIT = 100
STYLE_FIELD_LIMIT = 1000
LYRICS_LIMIT = 5000
EXCLUDE_STYLES_LIMIT = 600

ARRANGEMENTS = frozenset({
    "radio", "extended", "beatport_club", "full_8min", "tiktok",
    "acoustic", "live", "aaba", "blues12", "through_composed",
})

WORKFLOWS = frozenset({
    "create", "upload_audio", "add_vocals", "remix_cover", "extend",
    "replace_section", "stem_extraction", "inspire", "sounds",
})


# ── Anti-Cliché & Stopword Lists ───────────────────────────────────────
STOCK_PHRASES: dict[str, tuple[str, ...]] = {
    "english": (
        "feel the beat", "hands in the air", "party all night", "lose control",
        "we own the night", "electric love", "shadows dancing", "ignite the spark",
        "dancing tonight", "turn it up", "let the music take you", "under the stars",
        "feel alive", "into the night", "dance the night away", "raise your hands",
        "feel the music", "lose yourself", "the night is young", "one more time",
        "tonight we are free", "neon dreams", "city of lights", "heartbeat of the night",
    ),
    "portuguese": (
        "sentir a batida", "mãos para o alto", "dançar a noite inteira",
        "perder o controle", "nosso amor é infinito", "você é meu destino",
        "meu coração dispara", "teu abraço é meu lugar",
    ),
    "spanish": (
        "siente el ritmo", "manos arriba", "bailar toda la noche",
        "perder el control", "nuestro amor es infinito", "eres mi destino",
        "mi corazón se acelera", "tu abrazo es mi hogar",
    ),
}

_STOPWORDS = frozenset("""
a an the and or of to in on at by for from with as is are was were be been
i me my mine you your we us our it its this that these those he she his her they their
o os a as e ou de do da dos das em no na nos nas um uma uns umas eu me meu minha
voce teu tua seu sua nos nosso nossa que se por para pra com sem ao aos so mais
el la los las y o de del en un una unos unas yo mi mis tu tus su sus nosotros
que se por para con sin al es son soy somos lo le les me te ha nao no not
""".split())


# ── Trademark / Artist & AI-Slop Sanitization ──────────────────────────
_ARTIST_REPLACEMENTS: list[tuple[str, str]] = [
    ("Maceo Plex / Ellum", "underground emotional techno-deep"),
    ("Maceo Plex", "underground emotional techno-deep"),
    ("Ellum", "underground"),
    ("Dusky / Aus Music", "UK warm deep house"),
    ("Aus Music", "UK warm deep house"),
    ("Dusky", "UK warm deep house"),
    ("DJ Koze / Pampa", "quirky organic lo-fi house"),
    ("DJ Koze", "quirky organic"),
    ("Pampa Records", "lo-fi eclectic"),
    ("Pampa", "lo-fi eclectic"),
    ("Defected Records", "melodic warm UK house"),
    ("Defected", "melodic warm UK house"),
    ("Innervisions / Dixon", "Berlin progressive hypnotic"),
    ("Innervisions", "Berlin progressive hypnotic"),
    ("Dixon/Ame", "progressive deep"),
    ("Dixon / Ame", "progressive deep"),
    ("Dixon", "progressive deep"),
    ("Ame", "progressive deep"),
    ("Anjunadeep", "cinematic melodic euphoric"),
    ("Hot Creations / Jamie Jones", "tropical vocal-chop house"),
    ("Hot Creations", "tropical vocal-chop house"),
    ("Jamie Jones", "tropical vocal-chop"),
    ("Purple Disco Machine / OFF Spin", "filtered disco-house"),
    ("Purple Disco Machine", "filtered disco-house"),
    ("OFF Spin", "filtered disco"),
    ("London Grammar-style", "airy breathy indie-pop"),
    ("London Grammar", "airy breathy indie-pop"),
    ("Jorja Smith", "smooth airy"),
    ("Candi Staton Hallelujah", "anthemic house"),
    ("Candi Staton", "anthemic house"),
    ("The Avener rework style", "acoustic indie-folk crossover"),
    ("The Avener", "acoustic indie-folk crossover"),
    ("Henry Krinkle Stay-style", "viral pitched-hook"),
    ("Henry Krinkle", "viral pitched-hook"),
    ("Paradise aesthetic", "tropical Ibiza aesthetic"),
    ("Paradise bright energy", "tropical Ibiza bright energy"),
]

_SLOP_REPLACEMENTS: list[tuple[str, str]] = [
    (r"\bcircuits\b", "rhythms"),
    (r"\bcircuit\b", "rhythm"),
    (r"\bwires\b", "cords"),
    (r"\bwire\b", "cord"),
    (r"\bdigital void\b", "quiet space"),
    (r"\bvoid\b", "space"),
    (r"\bghost in the machine\b", "soul in the sound"),
    (r"\bghosts\b", "echoes"),
    (r"\bghost\b", "echo"),
    (r"\bneon lights\b", "dim lights"),
    (r"\bneon glow\b", "soft glow"),
    (r"\bneon\b", "dark"),
    (r"\bvelvet sky\b", "dark sky"),
    (r"\bvelvet\b", "smooth"),
    (r"\bhologram\b", "shadow"),
    (r"\bholograms\b", "shadows"),
    (r"\bmatrix\b", "grid"),
]

_REDUNDANCY_CLEANUP: list[tuple[str, str]] = [
    (r"label aesthetic", "aesthetic"),
    (r"label signature", "signature"),
    (r"label warmth", "warmth"),
    (r"label sound", "sound"),
    (r"label-style", "signature"),
    (r"\b([A-Za-z-]+)\s+\1\b", r"\1"),
    (r",\s*,", ","),
    (r"\s+,", ","),
    (r"[^\S\r\n]{2,}", " "),
]

_INSTRUCTION_LINE = re.compile(
    r"^(?:"
    r"(?:system|assistant|user|prompt|instruction|instructions|request|music brief)"
    r"\s*:"
    r"|(?:write|generate|create)\s+(?:a|the|this)\s+(?:song|lyrics?|style)"
    r"|(?:escreva|gere|crie|faça)\s+(?:uma?|a)\s+(?:música|letra|style)"
    r")",
    re.IGNORECASE,
)


# ── Phonetic Polish Rules ──────────────────────────────────────────────
_PHONETIC_PATTERNS: list[tuple[str, str]] = [
    (r"\b24/7/365\b", "twenty four seven three sixty five"),
    (r"\b24/7\b", "twenty four seven"),
    (r"\b1am\b", "one a m"),
    (r"\b2am\b", "two a m"),
    (r"\b3am\b", "three a m"),
    (r"\b4am\b", "four a m"),
    (r"\b5am\b", "five a m"),
    (r"\b6am\b", "six a m"),
    (r"\b7am\b", "seven a m"),
    (r"\b8am\b", "eight a m"),
    (r"\b9am\b", "nine a m"),
    (r"\b10am\b", "ten a m"),
    (r"\b11am\b", "eleven a m"),
    (r"\b12am\b", "twelve a m"),
    (r"\b1pm\b", "one p m"),
    (r"\b2pm\b", "two p m"),
    (r"\b3pm\b", "three p m"),
    (r"\b4pm\b", "four p m"),
    (r"\b5pm\b", "five p m"),
    (r"\b6pm\b", "six p m"),
    (r"\b7pm\b", "seven p m"),
    (r"\b8pm\b", "eight p m"),
    (r"\b9pm\b", "nine p m"),
    (r"\b10pm\b", "ten p m"),
    (r"\b11pm\b", "eleven p m"),
    (r"\b12pm\b", "twelve p m"),
    (r"\b1/2\b", "one half"),
]

_PHONETIC_ACRONYMS = frozenset({
    "AI", "ATM", "BPM", "CD", "CPU", "DVD", "FM", "GPS",
    "HD", "ID", "LCD", "LED", "PC", "SMS", "TV", "USB",
    "VIP", "VR", "VHS",
})


# ── Section Parsing ────────────────────────────────────────────────────
_SECTIONS = re.compile(
    r"\[(Intro|Verse(?:\s+\d+)?|Pre-Chorus|Chorus|Drop|Build(?:-up)?|Breakdown|Bridge|"
    r"Final Chorus|Final Drop|Outro|Instrumental Break|DJ Intro|DJ Outro|A[123]|B|Section [ABC])\]",
    re.IGNORECASE,
)


# ── Exclude Styles & Energy Maps ───────────────────────────────────────
_ELECTRONIC_DEEP_STYLES = frozenset({
    "classic_deep", "melodic_deep", "organic_house", "atmospheric_house",
    "club_deep", "sunset_house", "emotional_deep", "underground_deep",
    "tech_house", "downtempo_deep", "indie_dance", "edm",
    "uplifting_trance", "progressive_house",
})

_ELECTRONIC_BASE_EXCLUDES: list[str] = [
    "EDM big-room drops",
    "future bass synth pluck drops",
    "modern dubstep wobbles",
    "trap hi-hat rolls",
    "country guitar",
    "metalcore breakdowns",
    "auto-tuned rap delivery",
    "pop punk power chords",
    "screaming",
    "shouting",
    "strained vocals",
    "harsh vocals",
    "aggressive singing",
    "overacting",
    "rock-style vocals",
    "belting",
]

_STYLE_EXTRA_EXCLUDES: dict[str, list[str]] = {
    "classic_deep": ["aggressive techno kicks", "180 BPM hardstyle"],
    "melodic_deep": ["lo-fi tape hiss", "spoken-word rap"],
    "organic_house": ["heavily synthesised supersaws", "EDM festival risers"],
    "atmospheric_house": ["aggressive distortion", "fast 4-to-the-floor punk"],
    "club_deep": ["lo-fi tape character", "ambient drone"],
    "sunset_house": ["dark industrial kicks", "Berlin techno hardness"],
    "emotional_deep": ["happy hardcore", "comedic chiptune"],
    "underground_deep": ["pop chart vocals", "tropical house plucks"],
    "tech_house": ["dreamy ambient pads", "orchestral score"],
    "downtempo_deep": ["fast techno kicks", "EDM festival drops"],
    "indie_dance": ["heavy bass-music subs", "metalcore breakdowns"],
    "edm": [
        "slow lofi hip-hop", "acoustic folk guitar",
        "heavy industrial techno", "aggressive hardstyle kicks",
        "distorted rawstyle drops",
    ],
    "synthwave": [
        "modern trap", "heavy metal", "acoustic folk", "trap beat",
        "reggaeton dembow", "dubstep", "country", "drill", "hyperpop", "lo-fi hip hop",
    ],
}

_BASE_ARCS: dict[str, list[tuple[str, int]]] = {
    "radio": [
        ("Intro", 2), ("Verse 1", 5), ("Pre-Chorus", 7), ("Chorus", 9),
        ("Verse 2", 5), ("Pre-Chorus", 7), ("Chorus", 9), ("Bridge", 4),
        ("Final Chorus", 10), ("Outro", 3),
    ],
    "extended": [
        ("DJ Intro", 3), ("Intro Swell", 4), ("Verse 1", 5), ("Pre-Chorus", 7),
        ("Chorus", 9), ("Drop", 9), ("Verse 2", 6), ("Build-up", 8),
        ("Chorus", 9), ("Drop", 10), ("Bridge", 4), ("Final Drop", 10), ("DJ Outro", 3),
    ],
    "tiktok": [
        ("Build-up", 7), ("Drop", 10), ("Chorus", 9), ("Outro", 3),
    ],
    "beatport_club": [
        ("DJ Intro", 3), ("Intro Swell", 4), ("Verse 1", 5), ("Pre-Chorus", 7),
        ("Chorus", 9), ("Drop", 9), ("Breakdown", 4), ("Build-up", 8),
        ("Final Drop", 10), ("DJ Outro", 3),
    ],
    "full_8min": [
        ("DJ Intro", 2), ("Intro Swell", 3), ("Verse 1", 5), ("Pre-Chorus", 7),
        ("Chorus", 8), ("Drop", 9), ("Breakdown", 4), ("Verse 2", 6),
        ("Build-up", 8), ("Second Drop", 9), ("Bridge", 4), ("Final Build", 9),
        ("Final Drop", 10), ("DJ Outro", 3),
    ],
}

_INTENSITY_BIAS: dict[str, int] = {
    "subtle": -2,
    "building": 0,
    "peak": 1,
    "raw": 1,
    "dopamine": 1,
}


# ── Text Normalization & Sanitization ──────────────────────────────────
def words(text: str) -> list[str]:
    text = unicodedata.normalize("NFKD", text.casefold())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.findall(r"[^\W\d_]+", text)


def normalized(text: str) -> str:
    return " ".join(words(text))


def sung_lines(text: str) -> list[str]:
    text = re.sub(r"\([^)]*\)|\[[^]]*\]", "", text)
    return [normalized(line) for line in text.splitlines() if normalized(line)]


def sanitize_for_suno(text: str | None) -> str:
    """Strip known artist/label trademark names and AI slop from Style prompts."""
    if not text:
        return ""
    out = text
    for needle, replacement in _ARTIST_REPLACEMENTS:
        out = re.sub(rf"\b{re.escape(needle)}\b", replacement, out, flags=re.IGNORECASE)
    for pattern, replacement in _SLOP_REPLACEMENTS:
        out = re.sub(pattern, replacement, out, flags=re.IGNORECASE)
    for pattern, replacement in _REDUNDANCY_CLEANUP:
        out = re.sub(pattern, replacement, out, flags=re.IGNORECASE)
    return out.strip(" ,")


def sanitize_lyrics(text: str | None) -> str:
    """Remove known artist/label references without rewriting story imagery."""
    if not text:
        return ""
    out = text
    for needle, replacement in _ARTIST_REPLACEMENTS:
        out = re.sub(rf"\b{re.escape(needle)}\b", replacement, out, flags=re.IGNORECASE)
    return out.strip()


def remove_instruction_lines(lyrics: str) -> str:
    """Keep section tags, performance cues, and sung lines; drop leaked prompt lines."""
    kept = []
    for line in (lyrics or "").splitlines():
        visible = line.strip().lstrip("-*# ").strip()
        if visible and _INSTRUCTION_LINE.match(visible):
            continue
        kept.append(line)
    return "\n".join(kept).strip()


def apply_phonetic_polish(lyrics: str) -> str:
    """Spell out common numeric/time expressions and space known acronyms outside [tags]."""
    if not lyrics:
        return ""
    out_lines: list[str] = []
    for line in lyrics.splitlines():
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            out_lines.append(line)
            continue
        segments = re.split(r"(\[[^\]]*\])", line)
        for idx, seg in enumerate(segments):
            if seg.startswith("[") and seg.endswith("]"):
                continue
            new_seg = seg
            for pattern, replacement in _PHONETIC_PATTERNS:
                new_seg = re.sub(pattern, replacement, new_seg, flags=re.IGNORECASE)

            def _acronym_sub(match: re.Match[str]) -> str:
                token = match.group(1)
                return " ".join(token) if token in _PHONETIC_ACRONYMS else token

            new_seg = re.sub(r"\b([A-Z]{2,3})\b", _acronym_sub, new_seg)
            segments[idx] = new_seg
        out_lines.append("".join(segments))
    return "\n".join(out_lines)


def preserve_refinement_lyrics(instruction: str) -> bool:
    """Detect explicit lyric-preservation or strictly production-only edits (EN/PT/ES)."""
    lyrical_target_pattern = (
        r"\b(?:lyrics?|words?|letras?|verses?|versos?|chorus|refrão|estribillo|"
        r"story|história|historia|narrative|narrativa|hook|ponte|bridge|song|canção|música|canción|"
        r"sing|cantar|lines?|linhas?|líneas?)\b"
    )
    explicit = re.search(
        r"(?:^|[.,;:!?\n]\s*|\b(?:and|e|y)\s+)(?:(?:keep|leave)\s+(?:all\s+)?(?:the\s+)?lyrics\s+(?:unchanged|intact)|"
        r"preserve\s+(?:all\s+)?(?:the\s+)?lyrics|não\s+(?:altere|modifique)\s+a\s+letra|"
        r"mantenha\s+a\s+letra\s+(?:intacta|inalterada)|no\s+(?:cambies|modifiques)\s+la\s+letra)"
        r"(?=\s*(?:[.,!;:?\n]|$|\b(?:and|while|e|enquanto|y|mientras|but|mas|pero)\b))",
        instruction,
        re.IGNORECASE,
    )
    if explicit:
        remainder = instruction[explicit.end():]
        exception = re.search(r"\b(?:except|unless|exceto|salvo|excepto|menos)\b", remainder, re.IGNORECASE)
        lyrical_contrast = (
            re.search(r"\b(?:but|mas|pero)\b", remainder, re.IGNORECASE)
            and re.search(lyrical_target_pattern, remainder, re.IGNORECASE)
        )
        if not exception and not lyrical_contrast:
            return True

    only = re.search(r"\b(?:only|just|apenas|somente|só|solo|sólo)\b", instruction, re.IGNORECASE)
    production = re.search(
        r"\b(?:piano|guitars?|guitarras?|drums?|bateria|batería|bass|baixo|bajo|"
        r"synths?|sintetizador|bpm|tempo|reverb|reverberação|reverberación|"
        r"mix|mastering|equaliz[ae]\w*|instruments?|instrumentos?|production|produção|producción)\b",
        instruction,
        re.IGNORECASE,
    )
    lyrical_target = re.search(lyrical_target_pattern, instruction, re.IGNORECASE)
    return bool(only and production and not lyrical_target)


# ── Recommendations (Sliders, Exclusions, Energy Map) ──────────────────
def recommended_sliders(
    intensity_id: str = "dopamine",
    weirdness: int | None = None,
    style_influence: int | None = None,
    audio_influence: int | None = None,
    has_audio_ref: bool = False,
    arrangement_id: str = "radio",
) -> dict[str, Any]:
    presets = {
        "subtle": {"weirdness": 35, "style_influence": 82, "audio_influence": 0},
        "building": {"weirdness": 55, "style_influence": 75, "audio_influence": 0},
        "peak": {"weirdness": 50, "style_influence": 80, "audio_influence": 0},
        "raw": {"weirdness": 65, "style_influence": 70, "audio_influence": 0},
        "dopamine": {"weirdness": 58, "style_influence": 78, "audio_influence": 0},
    }
    base = dict(presets.get(intensity_id, presets["dopamine"]))
    if arrangement_id == "tiktok":
        base["weirdness"] = min(70, base["weirdness"] + 5)
        base["style_influence"] = max(70, base["style_influence"] - 3)
    if arrangement_id == "full_8min":
        base["style_influence"] = min(90, base["style_influence"] + 5)

    if weirdness is not None:
        base["weirdness"] = max(0, min(100, int(weirdness)))
    if style_influence is not None:
        base["style_influence"] = max(0, min(100, int(style_influence)))
    if audio_influence is not None:
        base["audio_influence"] = max(0, min(100, int(audio_influence)))
    elif has_audio_ref:
        base["audio_influence"] = 40

    return {
        **base,
        "suno_v6_variety": 0,
        "label": (
            f"Weirdness {base['weirdness']}% · "
            f"Style Influence {base['style_influence']}% · "
            f"Audio Influence {base['audio_influence']}%"
        ),
    }


def suggest_exclude_styles(
    style_id: str = "",
    user_excludes: str = "",
    instrumental: bool = False,
) -> str:
    items: list[str] = list(_ELECTRONIC_BASE_EXCLUDES) if style_id in _ELECTRONIC_DEEP_STYLES else []
    if style_id == "edm":
        items = [item for item in items if item != "future bass synth pluck drops"]
    items.extend(_STYLE_EXTRA_EXCLUDES.get(style_id, []))
    if instrumental:
        items.extend(["vocals", "singing", "spoken word"])

    deduped: list[str] = []
    seen: set[str] = set()
    for chunk in [*items, *re.split(r"[,;\n]+", user_excludes or "")]:
        clean = chunk.strip()
        if clean and clean.casefold() not in seen:
            deduped.append(clean)
            seen.add(clean.casefold())
    return ", ".join(deduped)[:EXCLUDE_STYLES_LIMIT].rstrip(" ,")


def build_performance_map(
    arrangement_id: str = "radio",
    intensity_id: str = "dopamine",
) -> list[tuple[str, int]]:
    arc = list(_BASE_ARCS.get(arrangement_id, _BASE_ARCS["radio"]))
    bias = _INTENSITY_BIAS.get(intensity_id, 0)
    result: list[tuple[str, int]] = []
    for name, energy in arc:
        if energy <= 4:
            shift = 0 if bias == 0 else (1 if bias > 0 else -1)
        else:
            shift = bias
        result.append((name, max(1, min(10, energy + shift))))
    return result


def format_performance_map_inline(arc: list[tuple[str, int]]) -> str:
    return " -> ".join(f"{name}({energy})" for name, energy in arc)


# ── Structural, Diversity & Novelty Validation ─────────────────────────
def lyric_sections(lyrics: str) -> list[tuple[str, str]]:
    matches = list(_SECTIONS.finditer(lyrics))
    return [
        (
            match.group(1),
            lyrics[match.end():matches[i + 1].start() if i + 1 < len(matches) else len(lyrics)].strip(),
        )
        for i, match in enumerate(matches)
    ]


def _sections_sung(lyrics: str) -> list[tuple[str, list[str]]]:
    return [(name.casefold(), sung_lines(body)) for name, body in lyric_sections(lyrics)]


def lyric_creativity(lyrics: str, arrangement: str = "radio") -> dict[str, Any]:
    errors: list[str] = []
    all_words = words(" ".join(sung_lines(lyrics)))
    verse_lines: list[str] = []
    duplicated = 0
    seen_verses: set[str] = set()

    for name, lines in _sections_sung(lyrics):
        is_verse = name.startswith("verse")
        if not is_verse and name not in {"bridge", "section a", "section b", "section c"}:
            continue
        if is_verse:
            verse_lines.extend(lines)
        body = " ".join(lines)
        if arrangement not in {"aaba", "blues12"} and len(words(body)) >= 12:
            if body in seen_verses:
                errors.append(f"[{name}] copies another verse; add a new event or consequence")
            seen_verses.add(body)
        counts = Counter(lines)
        if is_verse:
            duplicated += len(lines) - len(counts)
        if len(lines) >= 4 and max(counts.values(), default=0) >= 3 and len(counts) / len(lines) < 0.6:
            errors.append(f"[{name}] repeats too many whole lines; develop new story details")
        tokens = words(" ".join(lines))
        content = [w for w in tokens if w not in _STOPWORDS]
        if len(content) >= 24 and Counter(content).most_common(1)[0][1] / len(content) > 0.4:
            errors.append(f"[{name}] overuses one content word; vary vocabulary outside the refrain")
        if any(re.search(r"\b(\w+)(?: \1){3,}\b", line) for line in lines):
            errors.append(f"[{name}] loops the same word; keep repeated hooks in refrain sections")

    if re.search(r"\bneon(?:s|es)?\b", " ".join(all_words)):
        errors.append("Rewrite neon imagery with a story-specific image, not a fixed synonym")

    text = " " + " ".join(all_words) + " "
    stock = [
        phrase
        for phrases in STOCK_PHRASES.values()
        for phrase in phrases
        if " " + normalized(phrase) + " " in text
    ]
    if len(stock) >= 3:
        errors.append("Replace accumulated stock phrases with specific imagery: " + ", ".join(stock[:4]))

    return {
        "token_count": len(all_words),
        "lexical_diversity": round(len(set(all_words)) / len(all_words), 3) if all_words else None,
        "verse_duplicate_lines": duplicated,
        "verse_lines": len(verse_lines),
        "stock_phrases": stock,
        "errors": list(dict.fromkeys(errors)),
    }


def _ngrams(text: str, size: int = 5) -> set[tuple[str, ...]]:
    tokens = words(" ".join(sung_lines(text)))
    return {tuple(tokens[i:i + size]) for i in range(len(tokens) - size + 1)}


def _sung_text(text: str) -> str:
    return " ".join(sung_lines(text))


def novelty_errors(
    song: dict[str, Any],
    history: list[dict[str, Any]],
    *,
    lyric_foundation: str = "",
    requested_idea: str = "",
    requested_hook: str = "",
) -> list[str]:
    errors: list[str] = []
    title = normalized(song.get("track_title", "")).replace(" ", "")
    protected = _ngrams(lyric_foundation) | _ngrams(" ".join([requested_hook] * 3))
    grams = _ngrams(song.get("lyrics", "")) - protected
    candidate_sung = _sung_text(song.get("lyrics", ""))
    foundation = _sung_text(lyric_foundation)
    hook = normalized(requested_hook)
    hook_tokens = hook.split()

    def only_requested_hook() -> bool:
        if not hook_tokens or not candidate_sung:
            return False
        candidate_tokens = candidate_sung.split()
        repeats, remainder = divmod(len(candidate_tokens), len(hook_tokens))
        return not remainder and candidate_tokens == hook_tokens * repeats

    def covered_by_foundation() -> bool:
        if not foundation or not candidate_sung:
            return False
        candidate_tokens = candidate_sung.split()
        position = 0
        for token in foundation.split():
            if token == candidate_tokens[position]:
                position += 1
                if position == len(candidate_tokens):
                    return True
        return False

    choruses = {
        " ".join(lines)
        for name, lines in _sections_sung(song.get("lyrics", ""))
        if "chorus" in name and len(words(" ".join(lines))) >= 6
    }

    for previous in history:
        if title and title == normalized(previous.get("track_title", "")).replace(" ", ""):
            errors.append("Choose a different title image; this title already exists in recent creations")
        previous_sung = _sung_text(previous.get("lyrics", ""))
        if (
            candidate_sung
            and candidate_sung == previous_sung
            and not covered_by_foundation()
            and not only_requested_hook()
        ):
            errors.append("This lyric repeats a recent creation in full; rewrite the sung material")
        old_grams = _ngrams(previous.get("lyrics", ""))
        if len(grams) >= 8 and len(grams & old_grams) / len(grams) >= 0.55:
            errors.append("Too much wording matches a recent creation; rewrite the verses and hook")
        old_choruses = {
            " ".join(lines)
            for name, lines in _sections_sung(previous.get("lyrics", ""))
            if "chorus" in name
            and len(words(" ".join(lines))) >= 6
            and not (hook and all(line == hook for line in lines))
        }
        old_choruses = {c for c in old_choruses if c not in foundation}
        if choruses & old_choruses:
            errors.append("Invent a different refrain; this chorus already exists in recent creations")

    title_frequency: Counter[str] = Counter()
    for previous in history:
        title_frequency.update({
            w for w in words(previous.get("track_title", ""))
            if w not in _STOPWORDS and len(w) > 3
        })
    recurring = {
        w for w, count in title_frequency.items()
        if count >= max(3, math.ceil(len(history) * 0.25))
    }
    reused = (set(words(song.get("track_title", ""))) & recurring) - set(words(requested_idea))
    if reused:
        errors.append("Choose a fresh title motif instead of recurring title vocabulary: " + ", ".join(sorted(reused)))

    return list(dict.fromkeys(errors))


def song_quality_errors(
    song: dict[str, Any],
    arrangement: str = "radio",
    workflow: str = "create",
    instrumental: bool = False,
    *,
    check_creativity: bool = True,
) -> list[str]:
    errors: list[str] = []

    for field, limit in (
        ("track_title", TITLE_LIMIT),
        ("style_field", STYLE_FIELD_LIMIT),
        ("lyrics", LYRICS_LIMIT),
    ):
        value = song.get(field)
        if not isinstance(value, str):
            errors.append(f"{field} must be a string")
        elif len(value) > limit:
            errors.append(f"{field} exceeds {limit} characters; shorten while preserving the ending and hook")
        elif not value.strip() and not (field == "lyrics" and (workflow == "sounds" or instrumental)):
            errors.append(f"{field} is empty")

    exclude_styles = song.get("exclude_styles", "")
    if not isinstance(exclude_styles, str):
        errors.append("exclude_styles must be a string")
    elif len(exclude_styles) > EXCLUDE_STYLES_LIMIT:
        errors.append(f"exclude_styles exceeds {EXCLUDE_STYLES_LIMIT} characters")

    # Check trademark leaks in Style/Title/Lyrics
    for field in ("track_title", "style_field", "lyrics"):
        val = song.get(field)
        if isinstance(val, str):
            for needle, _ in _ARTIST_REPLACEMENTS:
                if re.search(rf"\b{re.escape(needle)}\b", val, flags=re.IGNORECASE):
                    errors.append(f"{field} contains artist/label reference '{needle}'; replace with pure sonic descriptors")

    lyrics = song.get("lyrics")
    if not isinstance(lyrics, str):
        return list(dict.fromkeys(errors))

    if instrumental:
        if lyrics.strip():
            errors.append("instrumental lyrics must be an empty string; keep all musical instructions in Style")
        return list(dict.fromkeys(errors))

    if workflow == "sounds":
        return list(dict.fromkeys(errors))

    for line in lyrics.splitlines():
        visible = line.strip().lstrip("-*# ").strip()
        if visible and _INSTRUCTION_LINE.match(visible):
            errors.append("lyrics contain a leaked prompt/instruction line; remove meta-instructions")
            break

    if check_creativity:
        errors.extend(lyric_creativity(lyrics, arrangement)["errors"])

    sections = lyric_sections(lyrics)
    names = [name.lower() for name, _ in sections]
    if not sections:
        errors.append("lyrics need populated English bracketed section tags")

    for name, content in sections:
        if not re.search(r"[a-z]", re.sub(r"\[[^]]*\]", "", content), re.IGNORECASE):
            errors.append(f"[{name}] is empty")
        if "verse" in name.lower() or "chorus" in name.lower():
            sung = re.sub(r"\([^)]*\)|\[[^]]*\]", "", content)
            if not re.search(r"[a-z]", sung, re.IGNORECASE):
                errors.append(f"[{name}] needs sung lines, not only performance cues")

    if workflow in {"extend", "replace_section"}:
        return list(dict.fromkeys(errors))

    if arrangement in {"aaba", "blues12", "through_composed"}:
        required = {
            "aaba": ["verse 1", "verse 2", "bridge", "verse 3", "outro"],
            "blues12": ["verse 1", "verse 2", "verse 3", "outro"],
            "through_composed": ["verse 1", "verse 2", "verse 3", "outro"],
        }[arrangement]
        if any(r not in names for r in required) or [n for n in names if n in required] != required:
            errors.append("selected form needs its populated sections in order: " + " -> ".join(required))
        return list(dict.fromkeys(errors))

    if arrangement == "tiktok":
        if not names or names[0] not in {"chorus", "drop", "build", "build-up", "pre-chorus"}:
            errors.append("tiktok arrangement must open with a hook or immediate build, not an intro or verse")
    elif not any(name.startswith("verse") for name in names):
        errors.append("full song needs at least one verse")

    if not any(name in {"chorus", "drop"} for name in names):
        errors.append("song needs a chorus or drop hook")

    if arrangement != "tiktok" and not any(name in {"final chorus", "final drop"} for name in names):
        errors.append("full song needs a [Final Chorus] or [Final Drop] payoff")

    if arrangement != "tiktok" and any(name.startswith("verse") for name in names):
        first_verse = next(i for i, name in enumerate(names) if name.startswith("verse"))
        finals = [i for i, name in enumerate(names) if name in {"final chorus", "final drop"}]
        if finals and finals[-1] < first_verse:
            errors.append("final payoff must follow the verses")

    if not names or names[-1] not in {"outro", "dj outro"}:
        errors.append("song must finish with a populated [Outro] or [DJ Outro]")

    return list(dict.fromkeys(errors))


def validate_package(
    song: dict[str, Any],
    *,
    arrangement: str = "radio",
    workflow: str = "create",
    instrumental: bool = False,
    fix: bool = False,
    history: list[dict[str, Any]] | None = None,
    lyric_foundation: str = "",
    requested_idea: str = "",
    requested_hook: str = "",
) -> dict[str, Any]:
    working = dict(song)
    if fix:
        if isinstance(working.get("track_title"), str):
            working["track_title"] = sanitize_lyrics(working["track_title"])
        if isinstance(working.get("style_field"), str):
            working["style_field"] = sanitize_for_suno(working["style_field"])
        if isinstance(working.get("lyrics"), str):
            if instrumental:
                working["lyrics"] = ""
            else:
                working["lyrics"] = apply_phonetic_polish(
                    remove_instruction_lines(sanitize_lyrics(working["lyrics"]))
                )

    errors = song_quality_errors(
        working,
        arrangement=arrangement,
        workflow=workflow,
        instrumental=instrumental,
    )
    if history and workflow not in {"extend", "replace_section", "sounds"} and not instrumental:
        errors.extend(
            novelty_errors(
                working,
                history,
                lyric_foundation=lyric_foundation,
                requested_idea=requested_idea,
                requested_hook=requested_hook,
            )
        )

    lyrics = working.get("lyrics", "") if isinstance(working.get("lyrics"), str) else ""
    diversity = lyric_creativity(lyrics, arrangement) if (lyrics and not instrumental) else None
    report: dict[str, Any] = {
        "valid": len(errors) == 0,
        "errors": list(dict.fromkeys(errors)),
        "stats": {
            "title_chars": len(working.get("track_title", "")) if isinstance(working.get("track_title"), str) else 0,
            "style_chars": len(working.get("style_field", "")) if isinstance(working.get("style_field"), str) else 0,
            "lyrics_chars": len(lyrics),
            "exclude_chars": len(working.get("exclude_styles", "")) if isinstance(working.get("exclude_styles"), str) else 0,
            "sections": [name for name, _ in lyric_sections(lyrics)] if lyrics else [],
            "lexical_diversity": diversity["lexical_diversity"] if diversity else None,
            "token_count": diversity["token_count"] if diversity else 0,
        },
    }
    if fix:
        report["cleaned_song"] = working
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate, polish, or configure Suno AI Custom Mode song packages."
    )
    parser.add_argument("--input", help="Path to JSON song file (defaults to stdin)")
    parser.add_argument("--arrangement", default="radio", choices=sorted(ARRANGEMENTS))
    parser.add_argument("--workflow", default="create", choices=sorted(WORKFLOWS))
    parser.add_argument("--instrumental", action="store_true", help="Validate as instrumental (lyrics must be empty)")
    parser.add_argument("--fix", action="store_true", help="Apply sanitization & phonetic polish before validating")
    parser.add_argument("--history", help="Path to JSON list of previous song dicts for novelty checking")
    parser.add_argument("--requested-idea", default="", help="User seed idea (exempts explicit words from recurring-title check)")
    parser.add_argument("--requested-hook", default="", help="User-requested hook phrase (exempted from novelty overlap)")
    parser.add_argument("--recommend", action="store_true", help="Print recommended sliders, exclude styles, and energy map")
    parser.add_argument("--style", default="", help="Genre/style ID for --recommend (e.g. melodic_deep, forro, blues)")
    parser.add_argument("--intensity", default="dopamine", choices=["subtle", "building", "peak", "raw", "dopamine"])
    parser.add_argument("--has-audio-ref", action="store_true", help="Indicate uploaded audio reference for slider target")
    args = parser.parse_args(argv)

    if args.recommend:
        arc = build_performance_map(args.arrangement, args.intensity)
        payload = {
            "style_id": args.style or "generic",
            "arrangement": args.arrangement,
            "intensity": args.intensity,
            "instrumental": args.instrumental,
            "sliders": recommended_sliders(
                intensity_id=args.intensity,
                has_audio_ref=args.has_audio_ref,
                arrangement_id=args.arrangement,
            ),
            "exclude_styles": suggest_exclude_styles(args.style, instrumental=args.instrumental),
            "performance_map": format_performance_map_inline(arc),
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    try:
        raw = open(args.input, "r", encoding="utf-8").read() if args.input else sys.stdin.read()
        song = json.loads(raw)
        if not isinstance(song, dict):
            raise ValueError("Input must be a JSON object")
    except Exception as exc:
        print(json.dumps({"valid": False, "errors": [f"Failed to parse input JSON: {exc}"]}, indent=2))
        return 1

    history: list[dict[str, Any]] = []
    if args.history:
        with open(args.history, "r", encoding="utf-8") as fh:
            loaded = json.load(fh)
            if isinstance(loaded, list):
                history = [item for item in loaded if isinstance(item, dict)]

    report = validate_package(
        song,
        arrangement=args.arrangement,
        workflow=args.workflow,
        instrumental=args.instrumental,
        fix=args.fix,
        history=history,
        requested_idea=args.requested_idea,
        requested_hook=args.requested_hook,
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
