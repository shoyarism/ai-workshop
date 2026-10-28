# @styleseed/motion

Five named animation seeds for AI-assisted UI work. Spread a recipe onto any `<motion.X>` to apply a seed in one of five standard contexts.

```tsx
import { spring, silk } from "@styleseed/motion"
import { motion } from "framer-motion"

<motion.button {...spring.hover} {...spring.press}>Save</motion.button>

<AnimatePresence>
  {open && <motion.div {...silk.entrance} {...silk.exit} />}
</AnimatePresence>
```

## The five seeds

| Seed | Vibe | Use for |
|---|---|---|
| **Spring** | bouncy, energetic, playful | CTAs, success states, anything alive |
| **Silk** | smooth, elegant, continuous | editorial layouts, financial dashboards |
| **Snap** | instant, decisive, precise | power tools, keyboard UIs, command palettes |
| **Float** | weightless, gentle, dreamy | marketing surfaces, hero sections, ambient UIs |
| **Pulse** | rhythmic, alive, punchy | notifications, live feeds, status indicators |

## The five contexts

| Context | What it returns | How to use |
|---|---|---|
| `entrance` | `{ initial, animate, transition }` | mount-in motion |
| `exit` | `{ exit, transition }` | unmount-out motion (pair with `<AnimatePresence>`) |
| `hover` | `{ whileHover, transition }` | mouse hover |
| `press` | `{ whileTap, transition }` | tap / click |
| `layout` | `{ layout: true, transition }` | FLIP-style layout reflow |

5 seeds × 5 contexts = **25 ready-to-spread variants**.

## Vibe vocabulary

`VIBE_TO_SEED` maps natural-language vibe words to seed ids. Used by the `/ss-motion` slash skill so LLMs can translate "make this card spring on hover" into the correct spread.

| Words | Seed |
|---|---|
| bouncy, springy, playful, energetic, alive | Spring |
| smooth, silky, fluid, elegant, composed, continuous | Silk |
| snappy, quick, instant, decisive, sharp, precise | Snap |
| floaty, gentle, weightless, dreamy, ambient, drifting | Float |
| rhythmic, punchy, pulsing, heartbeat, beat | Pulse |

## Motion by use-case (a light rule)

`MOTION_BY_USECASE` maps a common UI moment to the seed or keyword that fits — a
*starting point*, not a mandate. Powers the "which motion when" cheat on `/motion`
and the recommend mode in `/ss-motion`.

| Use case | Reach for | Why |
|---|---|---|
| Primary button / CTA press | `spring · press` | tactile, confident |
| Modal / dialog / sheet enter | `silk · entrance` | smooth; never bounce serious content |
| Dropdown / popover / menu | `snap · entrance` | instant, precise |
| Toast / notification | `spring · entrance` | friendly, non-blocking |
| List / feed items appearing | `stagger-cascade` | choreograph order |
| Marketing card hover | `tilt-3d` | depth/flair on content-light surfaces |
| Dashboard / data card hover | `snap · hover` | a subtle lift; keep dense UI calm |
| Like / favorite | `like-burst` | celebratory one-shot |
| Live / online dot | `pulse-beat` | looping "alive" |
| Loading / skeleton | `shimmer` | calm progress |
| Success | `pop-in` | positive "done" |
| Toggle / tab switch | `toggle-flip` | distinctive switch |
| Page transition | `silk · entrance` | smooth, minimal |
| Number / balance / price reveal | **none** | never animate the payload — it must read instantly |

**Two anti-rules override the table:** (1) **one seed per product** — keep one
personality; (2) **never delay the payload** — don't animate a balance, price, or
search result into view. Motion is for affordance, not content.

## Brand → seed defaults

`BRAND_DEFAULT_SEED` ships a sensible motion default per StyleSeed skin. Users may override per page or per element.

| Skin | Default seed |
|---|---|
| toss, arc | Spring |
| stripe, notion | Silk |
| linear, raycast, vercel | Snap |

## Accessibility

`usePrefersReducedMotion()` exports a React hook over `matchMedia("(prefers-reduced-motion: reduce)")`. Use it to swap any seed transition for `REDUCED_TRANSITION` (`{ duration: 0.01 }`) when the OS asks for reduced motion. The seeds themselves are static configs — wiring respect to the user's preference is the caller's job, by design, so that page transitions, list animations, and one-shot moments can be tuned independently.

## Relationship to `engine/components/ui/motion.tsx`

`motion.tsx` ships a small set of opinionated wrappers (`FadeIn`, `FadeUp`, `Stagger`, etc.) that pre-compose framer-motion for common cases. Those wrappers continue to work; the seeds are a finer-grained, vibe-named layer below them. New components should reach for seeds directly when context matters; existing components keep using the wrappers.

Cross-reference: `engine/DESIGN-LANGUAGE.md` Rule 59 (Animation Wrapper Rules) and `engine/METHODOLOGY.md` Chapter 8 (Motion Vibe Vocabulary).
