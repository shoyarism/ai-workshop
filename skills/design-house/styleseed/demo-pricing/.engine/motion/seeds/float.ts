import type { SeedConfig } from "../contexts";

/**
 * Float — weightless, gentle, dreamy.
 *
 * Use for: marketing surfaces, hero sections, anything that should feel
 * like content drifting in from elsewhere. Long durations, soft easing,
 * larger displacements than Silk. Reads as "this place takes its time."
 * Inspirations: Apple product pages, editorial sites, ambient UIs.
 */
export const float: SeedConfig = {
  name: "Float",
  vibe: "weightless, gentle, dreamy",
  entrance: {
    initial: { opacity: 0, y: 24 },
    animate: {
      opacity: 1,
      y: 0,
      transition: { ease: [0.22, 1, 0.36, 1], duration: 0.7 },
    },
  },
  exit: {
    exit: {
      opacity: 0,
      y: -20,
      transition: { ease: [0.4, 0, 1, 1], duration: 0.5 },
    },
  },
  hover: {
    whileHover: {
      y: -3,
      transition: { ease: [0.22, 1, 0.36, 1], duration: 0.5 },
    },
  },
  press: {
    whileTap: {
      scale: 0.97,
      y: 1,
      transition: { ease: [0.4, 0, 0.2, 1], duration: 0.3 },
    },
  },
  layout: {
    layout: true,
    transition: { ease: [0.22, 1, 0.36, 1], duration: 0.55 },
  },
};
