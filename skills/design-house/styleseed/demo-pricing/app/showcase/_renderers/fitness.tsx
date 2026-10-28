"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import {
  Activity,
  ChevronRight,
  Flame,
  Footprints,
  Heart,
  Play,
  Timer,
} from "lucide-react";
import { seeds, type SeedId } from "@engine/motion";
import type { EntranceRecipe } from "@engine/motion/contexts";

function delayed(recipe: EntranceRecipe, delay: number): EntranceRecipe {
  const animate = recipe.animate as Record<string, unknown>;
  const transition = (animate.transition as Record<string, unknown> | undefined) ?? {};
  return {
    initial: recipe.initial,
    animate: { ...animate, transition: { ...transition, delay } } as EntranceRecipe["animate"],
  };
}

const RINGS = [
  { label: "Move", value: 540, goal: 600, unit: "kcal", color: "#FF4E6A", r: 56 },
  { label: "Exercise", value: 38, goal: 45, unit: "min", color: "#9BFF3C", r: 42 },
  { label: "Stand", value: 10, goal: 12, unit: "hrs", color: "#3CE0FF", r: 28 },
];

const HISTORY = [
  { day: "Mon", emoji: "🏃", name: "Morning Run", detail: "5.2 km · 28 min", kcal: 412 },
  { day: "Sun", emoji: "🚴", name: "Cycling", detail: "18 km · 52 min", kcal: 638 },
  { day: "Sat", emoji: "🧘", name: "Yoga Flow", detail: "30 min", kcal: 145 },
  { day: "Fri", emoji: "🏋️", name: "Strength", detail: "45 min", kcal: 320 },
];

export function FitnessPage({ skin, seed: seedId }: { skin: string; seed: SeedId }) {
  const m = seeds[seedId];
  const [tab, setTab] = useState(0);

  const page = "var(--surface-page, var(--background, #0A0A0A))";
  const card = "var(--card, #161616)";
  const text = "var(--text-primary, var(--foreground, #F5F5F5))";
  const textSecondary = "var(--text-secondary, var(--muted-foreground, #B8B8B8))";
  const textTertiary = "var(--text-tertiary, var(--muted-foreground, #888888))";
  const brand = "var(--brand, #FF4E8B)";
  const brandFg = "var(--brand-foreground, #ffffff)";
  const shadow = "0 1px 2px rgba(0,0,0,0.3), 0 8px 24px rgba(0,0,0,0.4)";
  const radius = "20px";

  return (
    <div
      key={seedId}
      style={{
        background: page,
        color: text,
        minHeight: 640,
        padding: "40px 20px",
        fontFamily: "var(--font-display, var(--font-inter), Inter, system-ui, sans-serif)",
      }}
      className="flex items-start justify-center"
    >
      <div className="flex w-[400px] flex-col gap-4">
        {/* Header */}
        <motion.header {...m.entrance} className="flex items-center justify-between px-1">
          <div>
            <div className="text-[13px]" style={{ color: textTertiary }}>
              Thursday, May 29
            </div>
            <div className="text-[24px] font-bold tracking-tight">Summary</div>
          </div>
          <div
            className="flex h-10 w-10 items-center justify-center text-[14px] font-bold"
            style={{ background: brand, color: brandFg, borderRadius: 999 }}
          >
            SC
          </div>
        </motion.header>

        {/* Activity rings card */}
        <motion.section
          {...delayed(m.entrance, 0.05)}
          {...m.hover}
          className="flex items-center gap-6 p-6"
          style={{ background: card, borderRadius: radius, boxShadow: shadow }}
        >
          <Rings />
          <div className="flex-1 space-y-3">
            {RINGS.map((ring) => (
              <div key={ring.label}>
                <div className="text-[12px] font-semibold" style={{ color: textSecondary }}>
                  {ring.label}
                </div>
                <div className="flex items-baseline gap-1">
                  <span className="text-[20px] font-bold leading-none" style={{ color: ring.color }}>
                    {ring.value}
                  </span>
                  <span className="text-[12px]" style={{ color: textTertiary }}>
                    /{ring.goal} {ring.unit}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </motion.section>

        {/* Quick stats */}
        <div className="grid grid-cols-3 gap-3">
          {[
            { icon: Footprints, label: "Steps", value: "8,420", color: "#3CE0FF" },
            { icon: Flame, label: "Calories", value: "540", color: "#FF4E6A" },
            { icon: Heart, label: "Avg BPM", value: "72", color: "#9BFF3C" },
          ].map((s, i) => (
            <motion.div
              key={s.label}
              {...delayed(m.entrance, 0.1 + i * 0.05)}
              {...m.hover}
              className="p-4"
              style={{ background: card, borderRadius: 16, boxShadow: shadow }}
            >
              <s.icon size={16} style={{ color: s.color }} />
              <div className="mt-2 text-[18px] font-bold leading-none">{s.value}</div>
              <div className="mt-1 text-[11px]" style={{ color: textTertiary }}>
                {s.label}
              </div>
            </motion.div>
          ))}
        </div>

        {/* Start workout CTA */}
        <motion.button
          {...delayed(m.entrance, 0.25)}
          {...m.press}
          {...m.hover}
          type="button"
          className="flex items-center justify-center gap-2 py-4 text-[15px] font-bold"
          style={{ background: brand, color: brandFg, borderRadius: radius, boxShadow: shadow }}
        >
          <Play size={16} className="fill-current" />
          Start a workout
        </motion.button>

        {/* Tabs */}
        <motion.div {...delayed(m.entrance, 0.3)} className="flex gap-1 rounded-full p-1" style={{ background: "rgba(255,255,255,0.06)" }}>
          {["History", "Trends"].map((t, i) => (
            <button
              key={t}
              type="button"
              onClick={() => setTab(i)}
              className="relative flex-1 rounded-full py-1.5 text-[13px] font-bold"
              style={{ color: tab === i ? brandFg : textTertiary }}
            >
              {tab === i && (
                <motion.span
                  layoutId="fitness-tab"
                  transition={{ type: "spring", stiffness: 500, damping: 30 }}
                  className="absolute inset-0 rounded-full"
                  style={{ background: brand }}
                />
              )}
              <span className="relative z-10">{t}</span>
            </button>
          ))}
        </motion.div>

        {/* History list */}
        <div className="space-y-2">
          {HISTORY.map((h, i) => (
            <motion.div
              key={h.name}
              {...delayed(m.entrance, 0.35 + i * 0.05)}
              {...m.hover}
              className="flex items-center gap-3 p-3"
              style={{ background: card, borderRadius: 16, boxShadow: shadow, cursor: "pointer" }}
            >
              <div
                className="flex h-11 w-11 items-center justify-center text-[20px]"
                style={{ background: "rgba(255,255,255,0.06)", borderRadius: 12 }}
              >
                {h.emoji}
              </div>
              <div className="min-w-0 flex-1">
                <div className="text-[14px] font-bold">{h.name}</div>
                <div className="text-[11px]" style={{ color: textTertiary }}>
                  {h.day} · {h.detail}
                </div>
              </div>
              <div className="flex items-center gap-1 text-[13px] font-bold" style={{ color: brand }}>
                <Flame size={12} />
                {h.kcal}
              </div>
              <ChevronRight size={14} style={{ color: textTertiary }} />
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}

/** Concentric activity rings, drawn with SVG strokes. */
function Rings() {
  const size = 132;
  const center = size / 2;
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      {RINGS.map((ring) => {
        const circumference = 2 * Math.PI * ring.r;
        const pct = Math.min(1, ring.value / ring.goal);
        return (
          <g key={ring.label} transform={`rotate(-90 ${center} ${center})`}>
            <circle
              cx={center}
              cy={center}
              r={ring.r}
              fill="none"
              stroke={ring.color}
              strokeOpacity={0.18}
              strokeWidth={9}
            />
            <motion.circle
              cx={center}
              cy={center}
              r={ring.r}
              fill="none"
              stroke={ring.color}
              strokeWidth={9}
              strokeLinecap="round"
              strokeDasharray={circumference}
              initial={{ strokeDashoffset: circumference }}
              animate={{ strokeDashoffset: circumference * (1 - pct) }}
              transition={{ type: "spring", stiffness: 60, damping: 18, delay: 0.2 }}
            />
          </g>
        );
      })}
    </svg>
  );
}
