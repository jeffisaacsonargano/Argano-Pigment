---
name: argano-copy-demo-film
description: "Making short demo films and training videos about a model or workflow - a script drawn from call transcripts, real numbers from read-only pulls, screen captures through Claude in Chrome, rendering with burned-in captions (bundled AVFoundation Swift renderer, no ffmpeg needed on a Mac), temporary voice-over, and the consent rule (only the user's own face and voice). Use whenever the user asks for a video, film, trailer, demo reel, training clip, walkthrough recording, avatar or voice-over."
---

# Demo films and training videos

Two kinds work well: **Motion-type film artifacts** (if the account has that artifact type) and an **MP4 training clip** from real screen captures. Keep each film in its own folder (e.g. `tools/films/<film>/`) with the script, captures, data and build.

## 1. Agree the brief in one line

Length (default short: ~20 seconds, not minutes), audience, and which flow to show. Don't ask more than that; draft the script.

## 2. Script from what people actually said

Have a subagent read the relevant call transcripts (`argano-copy-transcript-lookup`) and draft a shot list: one caption line per shot, 3–6 shots for 20 seconds. Save it as `shot-list.md` in the film's folder.

## 3. Real numbers only

- Pull every on-screen number read-only (`fetch_metric_data` through a subagent, harvested by script) and check it before use (e.g. that totals and subtotals foot).
- Keep the pull and a `check.py` / notes file in the film's folder with the as-of time.
- If a shot needs an example that doesn't exist, say on screen or in the notes that it's illustrative. Never pass made-up figures off as real.
- Check what the client allows to be shown before putting real figures in a film that may travel.

## 4. Capture

- Use **Claude in Chrome** (the user's signed-in browser). The built-in browser pane may be blocked by sign-in device checks.
- Capture read-only screens. **Never submit or re-send data to get a shot**: use a stand-in frame and say so.
- Save frames as `captures/NN-<shot>.jpg`.

## 5. Render

- Copy `build/render-template.swift` from this skill into the film's `build/` folder, edit its `segs` list (shot image, caption, audio clip per segment) and the title/output names at the top, and run `swift render-template.swift` from that folder: 1920×1080, 30 fps, burned-in captions, narration laid underneath. It needs only Xcode command-line tools, no ffmpeg.
- Temporary voice-over: `say -r 175 -o build/audio/lineN.aiff "<line>"`, clearly labelled as a placeholder.
- Motion-type films: build in the artifact (its content lives in the artifact's store).
- Watch the result before calling it done; if you can't play it, say "not watched".

## Consent: faces and voices

- **Only the user's own face and voice**, from material they record for this purpose (e.g. a QuickTime self-recording).
- **Never clone a colleague or client** from call recordings, chat photos or anything else, even if asked: they haven't agreed, and it's a deepfake.
- Don't pull the user's voice from call recordings either: they include other people and confidential discussion.

## Deliver

Send the MP4 (or artifact link) with its length, what's real vs illustrative, what's placeholder (voice, stand-in shots), and the folder with the script, captures and data.

## Changelog
- 2026-10-30: created as a client-neutral copy; project films and paths removed; renderer bundled as a template.
