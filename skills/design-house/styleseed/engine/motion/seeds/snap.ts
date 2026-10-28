import type { SeedConfig } from "../contexts";

/**
 * Snap — instant, decisive, precise.
 *
 * Use for: power-user tools, keyboard-driven UIs, anything that should
 * feel like a terminal command landing. Short durations, sharp easing,
 * no bounce. The interaction is over before you notice the animation.
 * Inspirations: Raycast, Linear, command palettes.
 */
export const snap: SeedConfig = {
  name: "Snap",
  vibe: "instant, decisive, precise",
  entrance: {
    initial: { opacity: 0 },
    animate: {
      opacity: 1,
      transition: { ease: [0, 0, 0.2, 1], duration: 0.18 },
    },
  },
  exit: {
    exit: {
      opacity: 0,
      transition: { ease: [0.4, 0, 1, 1], duration: 0.12 },
    },
  },
  hover: {
    whileHover: {
      filter: "brightness(1.08)",
      transition: { ease: [0.4, 0, 0.2, 1], duration: 0.1 },
    },
  },
  press: {
    whileTap: {
      scale: 0.97,
      transition: { ease: [0.4, 0, 0.2, 1], duration: 0.06 },
    },
  },
  layout: {
    layout: true,
    transition: { ease: [0.4, 0, 0.2, 1], duration: 0.18 },
  },
};
