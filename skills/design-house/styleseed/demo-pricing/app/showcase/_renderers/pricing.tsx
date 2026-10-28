"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Check, Sparkles } from "lucide-react";
import { seeds, type SeedId } from "@engine/motion";
import type { EntranceRecipe } from "@engine/motion/contexts";
import { TIERS } from "../../pricing/pricing-data";

function delayed(recipe: EntranceRecipe, delay: number): EntranceRecipe {
  const animate = recipe.animate as Record<string, unknown>;
  const transition = (animate.transition as Record<string, unknown> | undefined) ?? {};
  return {
    initial: recipe.initial,
    animate: { ...animate, transition: { ...transition, delay } } as EntranceRecipe["animate"],
  };
}

/**
 * Pricing showcase — three-tier grid with billing toggle.
 *
 * Reuses TIERS from pricing/pricing-data.ts. The highlighted tier
 * uses the active skin's `--gradient-brand` so it adapts per brand.
 */
export function PricingPage({ skin, seed: seedId }: { skin: string; seed: SeedId }) {
  const m = seeds[seedId];
  const [annual, setAnnual] = useState(true);

  const surfacePage = "var(--surface-page, var(--background, #fafafa))";
  const card = "var(--card, #ffffff)";
  const text = "var(--text-primary, var(--foreground, #1a1a1a))";
  const textMuted = "var(--text-secondary, var(--muted-foreground, #6a6a6a))";
  const textTertiary = "var(--text-tertiary, var(--muted-foreground, #7a7a7a))";
  const border = "var(--border, rgba(0,0,0,0.08))";
  const brand = "var(--brand, #3182F6)";
  const brandFg = "var(--brand-foreground, #ffffff)";
  const brandTint = "var(--brand-tint, rgba(49,130,246,0.08))";
  const gradient = "var(--gradient-brand, var(--brand, #3182F6))";
  const radius = "var(--radius, 16px)";
  const shadow = "var(--shadow-card, 0 1px 3px rgba(0,0,0,0.04))";

  return (
    <div
      key={seedId}
      style={{
        background: surfacePage,
        color: text,
        minHeight: 640,
        fontFamily: "var(--font-display, var(--font-inter), Inter, system-ui, sans-serif)",
      }}
      className="px-8 py-12"
    >
      <div className="mx-auto max-w-5xl">
        {/* Header */}
        <motion.div {...m.entrance} className="text-center">
          <div
            className="inline-flex items-center gap-1.5 px-3 py-1 text-[11px] font-semibold uppercase tracking-widest"
            style={{ background: brandTint, color: brand, borderRadius: 999 }}
          >
            <Sparkles size={11} />
            <span>{skin.toUpperCase()} pricing</span>
          </div>
          <h1
            className="mt-4 text-[40px] font-bold leading-tight tracking-tight"
            style={{ color: text }}
          >
            Pricing that scales with you
          </h1>
          <p
            className="mx-auto mt-3 max-w-md text-[15px] leading-relaxed"
            style={{ color: textMuted }}
          >
            Same component, three brand DNAs. Start free, upgrade when the team grows past tinkering.
          </p>
        </motion.div>

        {/* Billing toggle */}
        <motion.div
          {...delayed(m.entrance, 0.1)}
          className="mt-6 flex justify-center"
        >
          <div
            className="inline-flex items-center gap-1 p-1"
            style={{ background: card, border: `1px solid ${border}`, borderRadius: 999 }}
          >
            <ToggleOption motion={m} active={!annual} onPick={() => setAnnual(false)}>
              Monthly
            </ToggleOption>
            <ToggleOption motion={m} active={annual} onPick={() => setAnnual(true)}>
              <span className="flex items-center gap-2">
                Annual
                <span
                  className="rounded-md px-1.5 py-0.5 text-[10px] font-bold uppercase"
                  style={{
                    background: brandTint,
                    color: brand,
                    letterSpacing: "0.05em",
                  }}
                >
                  Save 20%
                </span>
              </span>
            </ToggleOption>
          </div>
        </motion.div>

        {/* Tier cards */}
        <div className="mt-10 grid grid-cols-1 gap-4 md:grid-cols-3">
          {TIERS.map((tier, i) => (
            <motion.div
              key={tier.name}
              {...delayed(m.entrance, 0.15 + i * 0.08)}
              {...m.hover}
              className="relative flex flex-col overflow-hidden"
              style={{
                background: card,
                border: `1px solid ${tier.highlighted ? "transparent" : border}`,
                borderRadius: radius,
                boxShadow: tier.highlighted
                  ? "0 12px 40px rgba(0,0,0,0.12)"
                  : shadow,
                padding: 28,
              }}
            >
              {tier.highlighted && (
                <>
                  <div
                    aria-hidden
                    className="absolute inset-x-0 top-0 h-[3px]"
                    style={{ background: gradient }}
                  />
                  <div
                    className="absolute right-5 top-5 px-2 py-0.5 text-[10px] font-bold uppercase"
                    style={{
                      background: gradient,
                      color: brandFg,
                      borderRadius: 999,
                      letterSpacing: "0.06em",
                    }}
                  >
                    Popular
                  </div>
                </>
              )}

              <div className="text-[12px] font-semibold uppercase tracking-widest" style={{ color: textMuted }}>
                {tier.name}
              </div>
              <p className="mt-1 text-[13px]" style={{ color: textTertiary }}>
                {tier.tagline}
              </p>

              <div className="mt-6 flex items-baseline gap-1">
                <span className="text-[36px] font-bold leading-none tracking-tight">
                  ${annual ? tier.yearly : tier.monthly}
                </span>
                <span className="text-[12px]" style={{ color: textTertiary }}>
                  /mo
                </span>
              </div>
              {annual && tier.monthly > 0 && (
                <div className="mt-1 text-[11px]" style={{ color: textTertiary }}>
                  Billed yearly at ${tier.yearly * 12}
                </div>
              )}

              <ul className="mt-6 space-y-2 text-[13px]">
                {tier.features.map((f) => (
                  <li key={f} className="flex items-start gap-2">
                    <Check size={14} style={{ color: brand, marginTop: 3 }} />
                    <span style={{ color: text }}>{f}</span>
                  </li>
                ))}
              </ul>

              <motion.button
                type="button"
                {...m.hover}
                {...m.press}
                className="mt-7 w-full py-2.5 text-[13px] font-bold"
                style={{
                  background: tier.highlighted ? gradient : "transparent",
                  color: tier.highlighted ? brandFg : brand,
                  border: tier.highlighted ? "none" : `1px solid ${brand}`,
                  borderRadius: "var(--radius-md, 10px)",
                }}
              >
                {tier.cta}
              </motion.button>
            </motion.div>
          ))}
        </div>

        <motion.p
          {...delayed(m.entrance, 0.45)}
          className="mt-10 text-center text-[12px]"
          style={{ color: textTertiary }}
        >
          All plans include the StyleSeed engine. No credit card for Starter. Cancel anytime.
        </motion.p>
      </div>
    </div>
  );
}

function ToggleOption({
  motion: m,
  active,
  onPick,
  children,
}: {
  motion: (typeof seeds)[SeedId];
  active: boolean;
  onPick: () => void;
  children: React.ReactNode;
}) {
  return (
    <motion.button
      type="button"
      onClick={onPick}
      {...m.press}
      className="rounded-full px-4 py-1.5 text-[12px] font-bold transition-colors"
      style={{
        background: active ? "var(--brand, #3182F6)" : "transparent",
        color: active ? "var(--brand-foreground, #fff)" : "var(--text-secondary, var(--muted-foreground, #6a6a6a))",
      }}
    >
      {children}
    </motion.button>
  );
}
