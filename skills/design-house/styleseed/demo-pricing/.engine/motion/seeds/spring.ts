import type { SeedConfig } from "../contexts";

/**
 * Spring — bouncy, energetic, playful.
 *
 * Use for: CTA buttons, success states, anything that should feel alive.
 * Inspirations: Arc, Toss (primary CTA), Discord.
 */
export const spring: SeedConfig = {
  name: "Spring",
  vibe: "bouncy, energetic, playful",
  entrance: {
    initial: { opacity: 0, y: 16, scale: 0.96 },
    animate: {
      opacity: 1,
      y: 0,
      scale: 1,
      transition: { type: "spring", stiffness: 300, damping: 18, mass: 1 },
    },
  },
  exit: {
    exit: {
      opacity: 0,
      y: -8,
      scale: 0.98,
      transition: { type: "spring", stiffness: 400, damping: 30, mass: 0.8 },
    },
  },
  hover: {
    whileHover: {
      scale: 1.04,
      y: -2,
      transition: { type: "spring", stiffness: 300, damping: 20 },
    },
  },
  press: {
    whileTap: {
      scale: 0.96,
      transition: { type: "spring", stiffness: 500, damping: 30 },
    },
  },
  layout: {
    layout: true,
    transition: { type: "spring", stiffness: 300, damping: 20, mass: 0.8 },
  },
};
