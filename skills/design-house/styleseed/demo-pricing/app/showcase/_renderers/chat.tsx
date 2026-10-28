"use client";

import { motion } from "framer-motion";
import { ArrowUp, FileCode, Plus, Sparkles, Wrench } from "lucide-react";
import { seeds, type SeedId } from "@engine/motion";
import type { EntranceRecipe } from "@engine/motion/contexts";
import { MESSAGES } from "../../chat-data";

function delayed(recipe: EntranceRecipe, delay: number): EntranceRecipe {
  const animate = recipe.animate as Record<string, unknown>;
  const transition = (animate.transition as Record<string, unknown> | undefined) ?? {};
  return {
    initial: recipe.initial,
    animate: { ...animate, transition: { ...transition, delay } } as EntranceRecipe["animate"],
  };
}

/**
 * AI Chat showcase — phone-shell preview of a coding conversation.
 *
 * Reuses MESSAGES from chat-data.ts so the content stays in sync with
 * the existing `/` route. Skin variables drive the visual; the seed
 * drives the message stagger and composer feedback.
 */
export function ChatPage({ skin, seed: seedId }: { skin: string; seed: SeedId }) {
  const m = seeds[seedId];
  const surfacePage = "var(--surface-page, var(--background, #fafafa))";
  const card = "var(--card, #ffffff)";
  const text = "var(--text-primary, var(--foreground, #1a1a1a))";
  const textMuted = "var(--text-secondary, var(--muted-foreground, #6a6a6a))";
  const border = "var(--border, rgba(0,0,0,0.08))";
  const brand = "var(--brand, #3182F6)";
  const brandTint = "var(--brand-tint, rgba(49,130,246,0.08))";

  return (
    <div
      key={seedId}
      style={{
        background: "linear-gradient(180deg, #18181b 0%, #0a0a0a 100%)",
        minHeight: 640,
        padding: 40,
      }}
      className="flex items-center justify-center"
    >
      {/* Phone frame */}
      <motion.div
        {...m.entrance}
        className="relative flex flex-col overflow-hidden"
        style={{
          width: 400,
          height: 700,
          background: surfacePage,
          color: text,
          borderRadius: 36,
          boxShadow: "0 30px 80px rgba(0,0,0,0.45), 0 0 0 8px rgba(255,255,255,0.06)",
          fontFamily: "var(--font-display, var(--font-inter), Inter, system-ui, sans-serif)",
        }}
      >
        {/* Status bar */}
        <div
          className="flex items-center justify-between px-6 pt-3 pb-1 text-[11px]"
          style={{ color: text }}
        >
          <span className="font-semibold">9:41</span>
          <div className="flex items-center gap-1 opacity-80">
            <span>5G</span>
            <span>·</span>
            <span>100%</span>
          </div>
        </div>

        {/* App header */}
        <header
          className="flex items-center justify-between px-5 py-3"
          style={{ borderBottom: `1px solid ${border}` }}
        >
          <div className="flex items-center gap-2">
            <div
              className="flex h-7 w-7 items-center justify-center"
              style={{ background: brandTint, color: brand, borderRadius: 8 }}
            >
              <Sparkles size={14} />
            </div>
            <div>
              <div className="text-[13px] font-bold tracking-tight">AI Assist</div>
              <div className="text-[10px]" style={{ color: textMuted }}>
                Pricing component refactor
              </div>
            </div>
          </div>
          <button
            type="button"
            className="flex h-7 w-7 items-center justify-center"
            style={{ color: textMuted, borderRadius: 8 }}
          >
            <Plus size={14} />
          </button>
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-4 py-4 space-y-3">
          {MESSAGES.map((msg, i) => (
            <motion.div
              key={msg.id}
              {...delayed(m.entrance, 0.05 + i * 0.08)}
              className={msg.role === "user" ? "flex justify-end" : "flex flex-col gap-1.5"}
            >
              {msg.role === "user" ? (
                <div
                  className="max-w-[80%] rounded-2xl px-3.5 py-2.5 text-[13px] leading-snug"
                  style={{ background: brand, color: "var(--brand-foreground, #fff)" }}
                >
                  {msg.text}
                </div>
              ) : (
                <>
                  <div
                    className="max-w-[88%] rounded-2xl px-3.5 py-2.5 text-[13px] leading-snug"
                    style={{ background: card, color: text, border: `1px solid ${border}` }}
                  >
                    {msg.text}
                  </div>
                  {msg.toolCall && (
                    <div
                      className="ms-1 flex items-center gap-1.5 text-[11px]"
                      style={{ color: textMuted }}
                    >
                      <Wrench size={10} />
                      <span className="font-mono">
                        {msg.toolCall.name}({msg.toolCall.detail})
                      </span>
                      <span style={{ color: "var(--success, #6B9B7A)" }}>✓</span>
                    </div>
                  )}
                  {msg.code && (
                    <div
                      className="ms-1 max-w-[88%] overflow-hidden rounded-xl"
                      style={{
                        background: "#0f0f10",
                        color: "#e2e2e6",
                        border: "1px solid rgba(255,255,255,0.06)",
                      }}
                    >
                      <div
                        className="flex items-center gap-1.5 px-3 py-1.5 text-[10px]"
                        style={{
                          background: "rgba(255,255,255,0.04)",
                          color: "rgba(255,255,255,0.6)",
                        }}
                      >
                        <FileCode size={10} />
                        <span className="font-mono uppercase tracking-wider">
                          {msg.code.lang}
                        </span>
                      </div>
                      <pre
                        className="overflow-x-auto px-3 py-2 font-mono text-[10px] leading-snug"
                        style={{ whiteSpace: "pre" }}
                      >
                        {msg.code.body}
                      </pre>
                    </div>
                  )}
                </>
              )}
            </motion.div>
          ))}
        </div>

        {/* Composer */}
        <div
          className="flex items-center gap-2 px-4 py-3"
          style={{ borderTop: `1px solid ${border}`, background: card }}
        >
          <div
            className="flex flex-1 items-center px-3 py-2 text-[13px]"
            style={{
              background: surfacePage,
              border: `1px solid ${border}`,
              borderRadius: 14,
              color: textMuted,
            }}
          >
            Reply…
          </div>
          <motion.button
            type="button"
            {...m.hover}
            {...m.press}
            className="flex h-9 w-9 items-center justify-center"
            style={{ background: brand, color: "var(--brand-foreground, #fff)", borderRadius: 12 }}
          >
            <ArrowUp size={16} />
          </motion.button>
        </div>
      </motion.div>
    </div>
  );
}
