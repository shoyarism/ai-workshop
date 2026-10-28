"use client";

import { useState } from "react";
import { Check, Copy } from "lucide-react";

/**
 * A copyable vibe-coding prompt. The whole point of the guide: paste these
 * into Claude Code / Cursor and the named seeds + keywords resolve to real
 * framer-motion code from one registry.
 */
export function PromptCard({ prompt, maps }: { prompt: string; maps?: string }) {
  const [copied, setCopied] = useState(false);
  async function copy() {
    try {
      await navigator.clipboard.writeText(prompt);
      setCopied(true);
      setTimeout(() => setCopied(false), 1400);
    } catch {
      /* clipboard blocked */
    }
  }
  return (
    <div
      className="flex items-start gap-3 rounded-2xl bg-white p-4"
      style={{ boxShadow: "0 1px 2px rgba(0,0,0,0.04), 0 6px 18px rgba(0,0,0,0.06)" }}
    >
      <div className="flex-1">
        <p className="text-[14px] leading-relaxed text-neutral-800">
          <span className="mr-1 select-none text-neutral-300">&ldquo;</span>
          {prompt}
          <span className="ml-0.5 select-none text-neutral-300">&rdquo;</span>
        </p>
        {maps ? (
          <p className="mt-2 text-[12px] text-neutral-400">
            → resolves to <code className="font-semibold text-neutral-500">{maps}</code>
          </p>
        ) : null}
      </div>
      <button
        type="button"
        onClick={copy}
        className="flex shrink-0 items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-[12px] font-semibold text-neutral-600 transition-colors hover:bg-neutral-100"
      >
        {copied ? (
          <>
            <Check size={14} style={{ color: "#10B981" }} /> Copied
          </>
        ) : (
          <>
            <Copy size={14} /> Copy
          </>
        )}
      </button>
    </div>
  );
}
