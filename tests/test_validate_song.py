"""Unit tests for scripts/validate_song.py."""

from __future__ import annotations

import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_song as vs  # noqa: E402


VALID_RADIO_SONG = {
    "track_title": "Salt on Glass",
    "style_field": (
        "melodic deep house, 122 BPM, key of Em, young dream-pop soprano with close-mic intimacy, "
        "bittersweet sunrise lift, rolling sub bass locking with punchy 4/4 kick, warm Rhodes chords, "
        "concise radio arc with clean resolved ending"
    ),
    "exclude_styles": "EDM big-room drops, metalcore breakdowns, screaming",
    "lyrics": """[Intro]
(filtered Rhodes minor seventh swell, soft 4/4 kick rising)

[Verse 1]
(close mic, breathy)
Badge still clipped to my collar at five a m
Wipers pushing silver mist across the bend
Paper cup cooling in the dashboard tray
Harbor cranes waking in the salt and gray

[Pre-Chorus]
(build intensity)
Windows down, cold air on my wrist
Every red brake light turns to gold ahead
(hold silence)

[Chorus]
(open soaring melody)
Salt on glass, I made it home
Salt on glass, the coast is mine
Tide rolls in and takes the weight
Salt on glass, I'm wide awake

[Verse 2]
(locked rolling bass)
Gravel hums beneath the tires past the pier
Bakery steam drifting down the quiet lane
Keys in my palm still warm from all night long
Sunlight cuts across the steering wheel in gold

[Chorus]
(harmonies, wide stereo synths)
Salt on glass, I made it home
Salt on glass, the coast is mine
Tide rolls in and takes the weight
Salt on glass, I'm wide awake

[Bridge]
(whispered, stripped to Rhodes)
One deep breath... before the front door turns
Shoes by the threshold, let the morning burn

[Final Chorus]
(stacked doubles, octave harmonies)
Salt on glass, I made it home
Salt on glass, the coast is mine
Tide rolls in and takes the weight
Salt on glass, I'm wide awake

[Outro]
(distant reverb vocal fading cleanly)
Salt on glass... wide awake
""",
}


class ValidateSongTests(unittest.TestCase):
    def test_valid_radio_song_passes(self) -> None:
        report = vs.validate_package(VALID_RADIO_SONG, arrangement="radio", workflow="create")
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual(report["errors"], [])
        self.assertGreater(report["stats"]["token_count"], 50)

    def test_instrumental_requires_empty_lyrics(self) -> None:
        ok_song = {
            "track_title": "Thaw at Dawn",
            "style_field": "cinematic instrumental, 88 BPM, key of Dm, instrumental only, no vocals, felt piano and orchestral strings",
            "exclude_styles": "vocals, singing, spoken word",
            "lyrics": "",
        }
        self.assertTrue(vs.validate_package(ok_song, instrumental=True)["valid"])

        bad_song = dict(ok_song, lyrics="[Verse 1]\nSome accidental sung words")
        report = vs.validate_package(bad_song, instrumental=True)
        self.assertFalse(report["valid"])
        self.assertTrue(any("empty string" in err for err in report["errors"]))

    def test_tiktok_requires_immediate_hook(self) -> None:
        bad_report = vs.validate_package(VALID_RADIO_SONG, arrangement="tiktok")
        self.assertFalse(bad_report["valid"])
        self.assertTrue(any("tiktok" in err.lower() for err in bad_report["errors"]))

        good_tiktok = {
            "track_title": "Salt on Glass",
            "style_field": VALID_RADIO_SONG["style_field"],
            "exclude_styles": "",
            "lyrics": "[Chorus]\nSalt on glass, I made it home\nSalt on glass, the coast is mine\n\n[Outro]\n(clean fade)\nSalt on glass",
        }
        self.assertTrue(vs.validate_package(good_tiktok, arrangement="tiktok")["valid"])

    def test_non_pop_forms_without_chorus(self) -> None:
        blues = {
            "track_title": "Rust on the Rail",
            "style_field": "blues, 82 BPM, key of E, expressive raspy blues lead, shuffling twelve-bar blues feel, electric guitar bends and harmonica",
            "exclude_styles": "EDM drops, dubstep",
            "lyrics": (
                "[Verse 1]\nLeft my coat on the platform in the pouring rain\n"
                "Left my coat on the platform in the pouring rain\n"
                "Engine whistled south and never called my name\n\n"
                "[Verse 2]\nPocket full of silver and a ticket torn in two\n"
                "Pocket full of silver and a ticket torn in two\n"
                "Every mile I walk keeps leading back to you\n\n"
                "[Verse 3]\nDawn is breaking cold across the iron bridge\n"
                "Dawn is breaking cold across the iron bridge\n"
                "Guitar answering softly from the canyon ridge\n\n"
                "[Outro]\n(harmonica bend resolving over final E7 chord)"
            ),
        }
        self.assertTrue(vs.validate_package(blues, arrangement="blues12")["valid"])

        aaba = {
            "track_title": "Second Street Waltz",
            "style_field": "acoustic jazz, 110 BPM, key of F, intimate jazz lead, swung ride cymbal, upright bass and piano voicings",
            "exclude_styles": "EDM drops",
            "lyrics": (
                "[Verse 1]\nBrass lamp flickering above the cedar bar\nGlasses chiming slow beside the cellar door\n\n"
                "[Verse 2]\nRain taps easy rhythm on the awning frame\nStrangers trade a smile without a spoken name\n\n"
                "[Bridge]\nMidnight leans its shoulder on the upright bass\nEvery hurried hour slows to half its pace\n\n"
                "[Verse 3]\nBrass lamp flickering above the cedar bar\nWalking home lighter than we were before\n\n"
                "[Outro]\n(soft brushed snare and final major seventh piano chord)"
            ),
        }
        self.assertTrue(vs.validate_package(aaba, arrangement="aaba")["valid"])

    def test_partial_workflows_skip_full_arc(self) -> None:
        fragment = {
            "track_title": "Salt on Glass",
            "style_field": VALID_RADIO_SONG["style_field"],
            "exclude_styles": "",
            "lyrics": "[Bridge]\nOne deep breath before the front door turns\nShoes by the threshold as the morning burns",
        }
        self.assertTrue(vs.validate_package(fragment, workflow="replace_section")["valid"])
        self.assertTrue(vs.validate_package(fragment, workflow="extend")["valid"])

        sound_fx = {
            "track_title": "Analog Warm Swell",
            "style_field": "warm analog pad swell in E minor, gentle tape flutter, 4-bar cinematic texture",
            "exclude_styles": "vocals",
            "lyrics": "",
        }
        self.assertTrue(vs.validate_package(sound_fx, workflow="sounds")["valid"])

    def test_neon_ban_and_multilingual_cliches(self) -> None:
        neon_song = dict(
            VALID_RADIO_SONG,
            lyrics=VALID_RADIO_SONG["lyrics"].replace("silver mist", "néon glow"),
        )
        neon_report = vs.validate_package(neon_song)
        self.assertFalse(neon_report["valid"])
        self.assertTrue(any("neon" in err.lower() for err in neon_report["errors"]))

        cliche_song = dict(
            VALID_RADIO_SONG,
            lyrics=VALID_RADIO_SONG["lyrics"].replace(
                "Badge still clipped to my collar at five a m\nWipers pushing silver mist across the bend\nPaper cup cooling in the dashboard tray",
                "Feel the beat tonight\nHands in the air until dawn\nParty all night long",
            ),
        )
        cliche_report = vs.validate_package(cliche_song)
        self.assertFalse(cliche_report["valid"])
        self.assertTrue(any("stock phrases" in err.lower() for err in cliche_report["errors"]))

    def test_duplicate_verse_and_word_loop_rejected(self) -> None:
        dup_verse = (
            "[Intro]\n(warm synth)\n\n"
            "[Verse 1]\nBadge clipped to my collar at five in the morning watching fog roll off the dock\n\n"
            "[Chorus]\nSalt on glass, I made it home\n\n"
            "[Verse 2]\nBadge clipped to my collar at five in the morning watching fog roll off the dock\n\n"
            "[Final Chorus]\n(harmonies)\nSalt on glass, I made it home\n\n"
            "[Outro]\n(fade)\nHome"
        )
        dup_report = vs.validate_package(dict(VALID_RADIO_SONG, lyrics=dup_verse))
        self.assertFalse(dup_report["valid"])
        self.assertTrue(any("copies another verse" in err for err in dup_report["errors"]))

        loop_song = dict(
            VALID_RADIO_SONG,
            lyrics=VALID_RADIO_SONG["lyrics"].replace(
                "Badge still clipped to my collar at five a m",
                "Drive drive drive drive down the road",
            ),
        )
        loop_report = vs.validate_package(loop_song)
        self.assertFalse(loop_report["valid"])
        self.assertTrue(any("loops the same word" in err for err in loop_report["errors"]))

    def test_phonetic_polish_and_trademark_sanitization(self) -> None:
        polished = vs.apply_phonetic_polish("[Verse 1]\nWorking 24/7 until 3am with AI and VIP passes\n[DJ Outro]\nFade")
        self.assertIn("twenty four seven", polished)
        self.assertIn("three a m", polished)
        self.assertIn("A I", polished)
        self.assertIn("V I P", polished)
        self.assertIn("[Verse 1]", polished)
        self.assertIn("[DJ Outro]", polished)

        cleaned_style = vs.sanitize_for_suno("Anjunadeep melodic deep house, Dixon style, neon lights, digital void")
        self.assertNotIn("Anjunadeep", cleaned_style)
        self.assertNotIn("Dixon", cleaned_style)
        self.assertNotIn("neon", cleaned_style.lower())
        self.assertNotIn("void", cleaned_style.lower())

        dirty_song = dict(
            VALID_RADIO_SONG,
            style_field="Anjunadeep " + VALID_RADIO_SONG["style_field"],
            lyrics="System: write a song\n" + VALID_RADIO_SONG["lyrics"],
        )
        self.assertFalse(vs.validate_package(dirty_song)["valid"])
        fixed = vs.validate_package(dirty_song, fix=True)
        self.assertTrue(fixed["valid"], fixed["errors"])
        self.assertNotIn("Anjunadeep", fixed["cleaned_song"]["style_field"])
        self.assertNotIn("System:", fixed["cleaned_song"]["lyrics"])

    def test_novelty_history_checks_and_exemptions(self) -> None:
        errors = vs.novelty_errors(VALID_RADIO_SONG, [VALID_RADIO_SONG])
        self.assertTrue(any("title already exists" in e for e in errors))
        self.assertTrue(any("repeats a recent creation" in e for e in errors))

        exempt = vs.novelty_errors(
            dict(VALID_RADIO_SONG, track_title="Fresh Morning Harbor"),
            [VALID_RADIO_SONG],
            lyric_foundation=VALID_RADIO_SONG["lyrics"],
        )
        self.assertEqual(exempt, [])

    def test_preserve_refinement_lyrics_multilingual(self) -> None:
        self.assertTrue(vs.preserve_refinement_lyrics("Only change the drums and BPM to 124"))
        self.assertTrue(vs.preserve_refinement_lyrics("Keep the lyrics unchanged and add warmer Rhodes"))
        self.assertTrue(vs.preserve_refinement_lyrics("Mantenha a letra intacta e deixe o baixo mais quente"))
        self.assertTrue(vs.preserve_refinement_lyrics("Apenas mude a bateria e o reverb"))
        self.assertFalse(vs.preserve_refinement_lyrics("Keep the lyrics unchanged except rewrite the chorus"))
        self.assertFalse(vs.preserve_refinement_lyrics("Make Verse 2 sadder and slower"))

    def test_sliders_and_genre_aware_exclusions(self) -> None:
        sliders = vs.recommended_sliders(intensity_id="dopamine", arrangement_id="tiktok", has_audio_ref=True)
        self.assertEqual(sliders["weirdness"], 63)
        self.assertEqual(sliders["style_influence"], 75)
        self.assertEqual(sliders["audio_influence"], 40)
        self.assertEqual(sliders["suno_v6_variety"], 0)

        deep_ex = vs.suggest_exclude_styles("melodic_deep")
        self.assertIn("EDM big-room drops", deep_ex)
        self.assertIn("lo-fi tape hiss", deep_ex)

        forro_ex = vs.suggest_exclude_styles("forro")
        self.assertEqual(forro_ex, "")

        inst_ex = vs.suggest_exclude_styles("classical", instrumental=True)
        self.assertIn("vocals", inst_ex)
        self.assertIn("spoken word", inst_ex)


if __name__ == "__main__":
    unittest.main()
