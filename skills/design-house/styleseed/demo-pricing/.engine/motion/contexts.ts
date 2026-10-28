/**
 * Motion seed types — five named animation feels, each with five reusable contexts.
 *
 * A seed is a complete personality (Spring, Silk, Snap, Float, Pulse).
 * A context is where that personality lands: entrance, exit, hover, press, layout.
 * Each context returns props you can spread directly onto a `<motion.X>` — and
 * multiple contexts compose because every transition is embedded inside its
 * own state object (animate / exit / whileHover / whileTap) rather than
 * sitting at the top level where it would collide.
 *
 * Example:
 *   <motion.button {...spring.hover} {...spring.press}>Save</motion.button>
 *   <AnimatePresence>
 *     {open && <motion.div {...silk.entrance} {...silk.exit} />}
 *   </AnimatePresence>
 */

import type { MotionProps } from "framer-motion";

/** The five contexts every seed defines. */
export type SeedContext = "entrance" | "exit" | "hover" | "press" | "layout";

/** Shape spread onto a `<motion.X>` for an entrance animation. */
export type EntranceRecipe = Required<Pick<MotionProps, "initial" | "animate">>;

/** Shape for an exit animation. Pair with `<AnimatePresence>`. */
export type ExitRecipe = Required<Pick<MotionProps, "exit">>;

/** Shape for a hover interaction. */
export type HoverRecipe = Required<Pick<MotionProps, "whileHover">>;

/** Shape for a tap/press interaction. */
export type PressRecipe = Required<Pick<MotionProps, "whileTap">>;

/** Shape for FLIP-style layout animations. Layout transition stays top-level
 *  because framer-motion only reads it there. */
export type LayoutRecipe = Required<Pick<MotionProps, "layout" | "transition">>;

/** A complete seed: one personality across all five contexts. */
export type SeedConfig = {
  /** The seed name as it appears in vocab/docs. */
  readonly name: string;
  /** One-line vibe description for the LLM and UI. */
  readonly vibe: string;
  readonly entrance: EntranceRecipe;
  readonly exit: ExitRecipe;
  readonly hover: HoverRecipe;
  readonly press: PressRecipe;
  readonly layout: LayoutRecipe;
};

/** Convenience: pull every recipe for a single seed. */
export type SeedRecipes = Pick<SeedConfig, SeedContext>;
