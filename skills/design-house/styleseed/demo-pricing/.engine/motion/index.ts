/**
 * @styleseed/motion — five named animation seeds for AI-assisted UI work.
 *
 * Spread a recipe onto any `<motion.X>` to apply that seed in one of five
 * standard contexts: entrance, exit, hover, press, layout.
 *
 *   import { spring, silk } from "@styleseed/motion"
 *
 *   <motion.button {...spring.hover} {...spring.press}>Save</motion.button>
 *   <motion.div {...silk.entrance} {...silk.exit} layout {...silk.layout}>
 *
 * See README.md for vibe vocabulary and brand→seed default mapping.
 */

import { spring } from "./seeds/spring";
import { silk } from "./seeds/silk";
import { snap } from "./seeds/snap";
import { float } from "./seeds/float";
import { pulse } from "./seeds/pulse";

export { spring, silk, snap, float, pulse };
/** REDUCED_TRANSITION is data, safe in any context. */
export { REDUCED_TRANSITION } from "./reduced-motion";
/** Named, copy-pasteable motion keyword library (shared by /motion + /ss-motion). */
export {
  MOTION_LIBRARY,
  MOTION_BY_KEY,
  MOTION_CATEGORIES,
  MOTION_BY_USECASE,
  type MotionKeyword,
  type MotionCategory,
  type MotionUseCase,
} from "./library";
// usePrefersReducedMotion is a React hook — import directly from
// "@engine/motion/reduced-motion" inside a "use client" file to keep
// this barrel safe to import from Server Components.
export type {
  SeedContext,
  SeedConfig,
  SeedRecipes,
  EntranceRecipe,
  ExitRecipe,
  HoverRecipe,
  PressRecipe,
  LayoutRecipe,
} from "./contexts";

/** All seeds keyed by name. Useful for iteration in showcase pages. */
export const seeds = { spring, silk, snap, float, pulse } as const;

/** Discriminated union of seed ids. */
export type SeedId = keyof typeof seeds;

/** Brand → recommended default seed. Users may override per page or per element. */
export const BRAND_DEFAULT_SEED: Record<string, SeedId> = {
  toss: "spring",
  stripe: "silk",
  linear: "snap",
  raycast: "snap",
  arc: "spring",
  notion: "silk",
  vercel: "snap",
};

/** Vibe word → seed lookup. Used by /ss-motion to translate prompts. */
export const VIBE_TO_SEED: Record<string, SeedId> = {
  // Spring
  bouncy: "spring",
  springy: "spring",
  playful: "spring",
  energetic: "spring",
  alive: "spring",
  // Silk
  smooth: "silk",
  silky: "silk",
  fluid: "silk",
  elegant: "silk",
  composed: "silk",
  continuous: "silk",
  // Snap
  snappy: "snap",
  quick: "snap",
  instant: "snap",
  decisive: "snap",
  sharp: "snap",
  precise: "snap",
  // Float
  floaty: "float",
  gentle: "float",
  weightless: "float",
  dreamy: "float",
  ambient: "float",
  drifting: "float",
  // Pulse
  rhythmic: "pulse",
  punchy: "pulse",
  pulsing: "pulse",
  heartbeat: "pulse",
  beat: "pulse",
};
