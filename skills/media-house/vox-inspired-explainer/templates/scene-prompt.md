# Scene & Beat Generator Prompt Template

Generate the production asset and motion code for **Beat {{beat_id}}** of the explainer video.

---

## Beat Specification

- **Narrative Stage:** `{{narrative_stage}}`
- **Timecode Window:** `{{timecode_in}}s` to `{{timecode_out}}s` (Duration: `{{duration}}s`)
- **Spoken Narration:** "{{narration}}"
- **Visual Mode:** `{{visual_mode}}`
- **Visual Job:** {{visual_job}}
- **Focal Subject:** {{focal_subject}}
- **Composition Layout:** {{composition}}
- **Camera Movement:** {{camera}}
- **Synchronized Motion:** {{motion}}

---

## On-Screen Text Specification

- **Eyebrow Label:** "{{on_screen_text.eyebrow}}" (Color: `#D62828` or `#737D8C`, Font: Monospace uppercase, `letter-spacing: 0.14em`)
- **Headline:** "{{on_screen_text.headline}}" (Color: `#121417`, Font: Inter/Barlow Black 900)
- **Subhead:** "{{on_screen_text.subhead}}" (Color: `#4A5260`)
- **Highlighter Target Words:** `{{on_screen_text.highlighter_target_words}}`
  - Stroke style: Felt Marker Yellow `#FFE500`, opacity `0.85`, blend mode `multiply`
  - Timing: Wipes from left to right exactly at the spoken audio timestamp

---

## Motion Code Contract (GSAP / Remotion)

```javascript
// Register beat timeline within master timeline
const beatTl = gsap.timeline();

// 1. Entrance (0.0s - 0.4s)
beatTl.fromTo(".scene-container", 
  { opacity: 0, y: 15 }, 
  { opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }
);

// 2. Camera Ken Burns slow drift (throughout entire duration)
beatTl.to(".camera-rig", 
  { scale: 1.03, duration: {{duration}}, ease: "none" }, 
  0
);

// 3. Spoken Keyword Highlighter Stroke
beatTl.to(".highlighter-stroke", 
  { width: "100%", duration: 0.5, ease: "power1.inOut" }, 
  {{highlighter_timestamp_offset}}
);

// 4. Annotation Draw / Reticle Reveal
beatTl.fromTo(".accent-line", 
  { strokeDashoffset: 400 }, 
  { strokeDashoffset: 0, duration: 0.8, ease: "power2.out" }, 
  {{annotation_timestamp_offset}}
);
```
