import type { SeedConfig } from "../contexts";

/**
 * Pulse — rhythmic, alive, punchy.
 *
 * Use for: notifications, live feeds, anything that should feel like a
 * heartbeat. Tight spring (low mass, high stiffness) for quick, percussive
 * motion that doesn't overstay its welcome.
 * Inspirations: Discord, music apps, status indicators.
 */
export const pulse: SeedConfig = {
  name: "Pulse",
  vibe: "rhythmic, alive, punchy",
  entrance: {
    initial: { opacity: 0, scale: 0.9 },
    animate: {
      opacity: 1,
      scale: 1,
      transition: { type: "spring", stiffness: 500, damping: 25, mass: 0.6 },
    },
  },
  exit: {
    exit: {
      opacity: 0,
      scale: 0.95,
      transition: { type: "spring", stiffness: 400, damping: 30, mass: 0.6 },
    },
  },
  hover: {
    whileHover: {
      scale: 1.02,
      transition: { type: "spring", stiffness: 500, damping: 25, mass: 0.6 },
    },
  },
  press: {
    whileTap: {
      scale: 0.94,
      transition: { type: "spring", stiffness: 600, damping: 28, mass: 0.6 },
    },
  },
  layout: {
    layout: true,
    transition: { type: "spring", stiffness: 500, damping: 25, mass: 0.6 },
  },
};
