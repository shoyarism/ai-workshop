import type { SeedConfig } from "../contexts";

/**
 * Silk — smooth, elegant, continuous.
 *
 * Use for: editorial layouts, financial dashboards, anything that should
 * feel composed and quiet. No bounce, no overshoot, just calibrated easing.
 * Inspirations: Stripe, Linear (modals), Notion.
 */
export const silk: SeedConfig = {
  name: "Silk",
  vibe: "smooth, elegant, continuous",
  entrance: {
    initial: { opacity: 0, y: 12 },
    animate: {
      opacity: 1,
      y: 0,
      transition: { ease: [0.32, 0.72, 0, 1], duration: 0.45 },
    },
  },
  exit: {
    exit: {
      opacity: 0,
      y: -6,
      transition: { ease: [0.4, 0, 1, 1], duration: 0.3 },
    },
  },
  hover: {
    whileHover: {
      y: -1,
      filter: "brightness(1.03)",
      transition: { ease: [0.32, 0.72, 0, 1], duration: 0.25 },
    },
  },
  press: {
    whileTap: {
      scale: 0.98,
      transition: { ease: [0.4, 0, 0.2, 1], duration: 0.15 },
    },
  },
  layout: {
    layout: true,
    transition: { ease: [0.32, 0.72, 0, 1], duration: 0.4 },
  },
};
