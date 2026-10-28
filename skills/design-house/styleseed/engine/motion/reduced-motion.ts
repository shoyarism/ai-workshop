"use client";

import { useEffect, useState } from "react";

/**
 * Subscribes to `prefers-reduced-motion: reduce` and returns the current value.
 *
 * Use this to swap any seed recipe for a near-instant variant when the user
 * has asked the OS to dampen motion. Server-side rendering returns `false`
 * (no reduction), then hydration updates if needed.
 */
export function usePrefersReducedMotion(): boolean {
  const [reduced, setReduced] = useState(false);

  useEffect(() => {
    if (typeof window === "undefined" || !window.matchMedia) return;
    const mql = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReduced(mql.matches);
    const handler = (e: MediaQueryListEvent) => setReduced(e.matches);
    mql.addEventListener("change", handler);
    return () => mql.removeEventListener("change", handler);
  }, []);

  return reduced;
}

/**
 * A flat-instant transition. Use as a replacement for any seed transition
 * when the user prefers reduced motion.
 */
export const REDUCED_TRANSITION = { duration: 0.01 } as const;
