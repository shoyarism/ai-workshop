"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import {
  Heart,
  ListMusic,
  Pause,
  Play,
  Repeat,
  Shuffle,
  SkipBack,
  SkipForward,
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

const QUEUE = [
  { id: 1, title: "Midnight City", artist: "M83", len: "4:03", art: "linear-gradient(135deg,#FF6B6B,#FFD93D)" },
  { id: 2, title: "Redbone", artist: "Childish Gambino", len: "5:27", art: "linear-gradient(135deg,#6C5CE7,#A8E6CF)" },
  { id: 3, title: "Nightcall", artist: "Kavinsky", len: "4:18", art: "linear-gradient(135deg,#2C3E50,#FD746C)" },
  { id: 4, title: "Instant Crush", artist: "Daft Punk", len: "5:37", art: "linear-gradient(135deg,#4ECDC4,#556270)" },
];

export function MusicPage({ skin, seed: seedId }: { skin: string; seed: SeedId }) {
  const m = seeds[seedId];
  const [playing, setPlaying] = useState(true);
  const [liked, setLiked] = useState(true);
  const [progress] = useState(38);

  const page = "var(--surface-page, var(--background, #ffffff))";
  const card = "var(--card, #ffffff)";
  const text = "var(--text-primary, var(--foreground, #1a1a1a))";
  const textSecondary = "var(--text-secondary, var(--muted-foreground, #6a6a6a))";
  const textTertiary = "var(--text-tertiary, var(--muted-foreground, #9a9a9a))";
  const brand = "var(--brand, #1a1a1a)";
  const muted = "var(--surface-muted, rgba(0,0,0,0.08))";
  const shadow = "0 1px 2px rgba(0,0,0,0.03), 0 6px 16px rgba(0,0,0,0.05)";
  const heroArt = "linear-gradient(135deg, #FF6B6B 0%, #FFD93D 100%)";

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
      <div className="flex w-[400px] flex-col gap-5">
        {/* Header */}
        <motion.header {...m.entrance} className="flex items-center justify-between px-1">
          <div className="text-[12px] font-semibold uppercase tracking-widest" style={{ color: textTertiary }}>
            Now Playing
          </div>
          <ListMusic size={18} style={{ color: textSecondary }} />
        </motion.header>

        {/* Album art */}
        <motion.div
          {...delayed(m.entrance, 0.05)}
          {...m.hover}
          className="aspect-square w-full"
          style={{ background: heroArt, borderRadius: 24, boxShadow: "0 20px 50px rgba(255,107,107,0.3)" }}
        />

        {/* Track meta + like */}
        <motion.div {...delayed(m.entrance, 0.1)} className="flex items-center justify-between px-1">
          <div className="min-w-0">
            <div className="truncate text-[22px] font-bold tracking-tight">Midnight City</div>
            <div className="truncate text-[14px]" style={{ color: textSecondary }}>
              M83 · Hurry Up, We&rsquo;re Dreaming
            </div>
          </div>
          <motion.button
            type="button"
            {...m.press}
            onClick={() => setLiked((l) => !l)}
            className="flex h-10 w-10 shrink-0 items-center justify-center"
          >
            <motion.span animate={liked ? { scale: [1, 1.3, 1] } : { scale: 1 }} transition={{ type: "spring", stiffness: 400, damping: 14 }}>
              <Heart size={22} className={liked ? "fill-rose-500 text-rose-500" : ""} style={liked ? {} : { color: textSecondary }} />
            </motion.span>
          </motion.button>
        </motion.div>

        {/* Progress */}
        <motion.div {...delayed(m.entrance, 0.15)} className="px-1">
          <div className="h-1.5 w-full overflow-hidden rounded-full" style={{ background: muted }}>
            <div className="h-full rounded-full" style={{ width: `${progress}%`, background: brand }} />
          </div>
          <div className="mt-1.5 flex justify-between text-[11px]" style={{ color: textTertiary }}>
            <span>1:32</span>
            <span>4:03</span>
          </div>
        </motion.div>

        {/* Transport */}
        <motion.div {...delayed(m.entrance, 0.2)} className="flex items-center justify-between px-2">
          <Shuffle size={18} style={{ color: textTertiary }} />
          <SkipBack size={26} className="fill-current" style={{ color: text }} />
          <motion.button
            type="button"
            {...m.press}
            {...m.hover}
            onClick={() => setPlaying((p) => !p)}
            className="flex h-16 w-16 items-center justify-center"
            style={{ background: brand, color: "var(--card, #fff)", borderRadius: 999, boxShadow: shadow }}
          >
            {playing ? <Pause size={26} className="fill-current" /> : <Play size={26} className="fill-current" />}
          </motion.button>
          <SkipForward size={26} className="fill-current" style={{ color: text }} />
          <Repeat size={18} style={{ color: textTertiary }} />
        </motion.div>

        {/* Up next */}
        <motion.div {...delayed(m.entrance, 0.28)} className="pt-2">
          <div className="mb-2 flex items-baseline justify-between px-1">
            <div className="text-[14px] font-bold">Up next</div>
            <button type="button" className="text-[12px] font-bold" style={{ color: textTertiary }}>
              Clear
            </button>
          </div>
          <div
            className="overflow-hidden"
            style={{ background: card, borderRadius: 18, boxShadow: shadow }}
          >
            {QUEUE.map((q, i) => (
              <motion.div
                key={q.id}
                {...delayed(m.entrance, 0.3 + i * 0.04)}
                {...m.hover}
                className="flex items-center gap-3 px-3 py-2.5"
                style={{ cursor: "pointer" }}
              >
                <div className="h-10 w-10 shrink-0" style={{ background: q.art, borderRadius: 10 }} />
                <div className="min-w-0 flex-1">
                  <div className="truncate text-[13px] font-bold">{q.title}</div>
                  <div className="truncate text-[11px]" style={{ color: textTertiary }}>
                    {q.artist}
                  </div>
                </div>
                <span className="text-[11px] tabular-nums" style={{ color: textTertiary }}>
                  {q.len}
                </span>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
