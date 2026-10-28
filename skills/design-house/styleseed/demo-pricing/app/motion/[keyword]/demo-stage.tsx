"use client";

import { useState } from "react";
import { Check, Copy, RefreshCw } from "lucide-react";
import { DEMOS, FallbackDemo } from "../_demos";

export function DemoStage({
  keyword,
  accent,
  snippet,
}: {
  keyword: string;
  accent: string;
  snippet: string;
}) {
  const [trigger, setTrigger] = useState(0);
  const [copied, setCopied] = useState(false);
  const Demo = DEMOS[keyword] ?? FallbackDemo;

  async function copy() {
    try {
      await navigator.clipboard.writeText(snippet);
      setCopied(true);
      setTimeout(() => setCopied(false), 1400);
    } catch {
      /* clipboard blocked */
    }
  }

  return (
    <>
      <div
        role="button"
        tabIndex={0}
        onClick={() => setTrigger((t) => t + 1)}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") setTrigger((t) => t + 1);
        }}
        className="relative flex h-64 items-center justify-center rounded-2xl bg-white"
        style={{ cursor: "pointer", boxShadow: "0 1px 2px rgba(0,0,0,0.04), 0 6px 18px rgba(0,0,0,0.06)" }}
        aria-label={`Replay ${keyword} motion`}
      >
        <Demo trigger={trigger} accent={accent} />
        <span className="pointer-events-none absolute bottom-3 right-4 text-[11px] font-medium uppercase tracking-wider text-neutral-300">
          tap / hover to play
        </span>
      </div>

      {/* code */}
      <div className="relative mt-5">
        <button
          type="button"
          onClick={copy}
          className="absolute right-3 top-3 z-10 inline-flex items-center gap-1.5 rounded-lg bg-white/10 px-2.5 py-1.5 text-[12px] font-semibold text-neutral-200 transition-colors hover:bg-white/20"
        >
          {copied ? (
            <>
              <Check size={14} style={{ color: "#34D399" }} /> Copied
            </>
          ) : (
            <>
              <Copy size={14} /> Copy
            </>
          )}
        </button>
        <pre className="overflow-x-auto rounded-2xl bg-neutral-900 p-5 text-[13px] leading-relaxed text-neutral-100">
          <code>{snippet}</code>
        </pre>
      </div>

      <button
        type="button"
        onClick={() => setTrigger((t) => t + 1)}
        className="mt-3 inline-flex items-center gap-1.5 text-[12px] font-semibold text-neutral-500 hover:text-neutral-900"
      >
        <RefreshCw size={12} /> replay the demo
      </button>
    </>
  );
}
