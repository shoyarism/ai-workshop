"use client";

import { useState, type ReactNode } from "react";
import type { Skin } from "@/lib/registry";

type Props = {
  preview: ReactNode;
  skins: Skin[];
};

const STORAGE_KEY = "styleseed-gallery-skin";

export function PreviewFrame({ preview, skins }: Props) {
  const [active, setActive] = useState<string>(() => {
    if (typeof window === "undefined") return "toss";
    return window.localStorage.getItem(STORAGE_KEY) || "toss";
  });

  const onSelect = (id: string) => {
    setActive(id);
    if (typeof window !== "undefined") {
      window.localStorage.setItem(STORAGE_KEY, id);
    }
  };

  return (
    <div className="overflow-hidden rounded-xl border border-gray-200">
      <div className="flex flex-wrap items-center gap-1 border-b border-gray-200 bg-gray-50 px-2 py-2">
        {skins.map((s) => (
          <button
            key={s.id}
            onClick={() => onSelect(s.id)}
            className={
              "flex items-center gap-1.5 rounded-md px-2.5 py-1 text-xs font-medium transition-colors " +
              (active === s.id
                ? "bg-white shadow-sm text-gray-900"
                : "text-gray-600 hover:text-gray-900")
            }
          >
            {s.brand && (
              <span
                className="size-2.5 rounded-full"
                style={{ background: s.brand }}
                aria-hidden
              />
            )}
            {s.name}
          </button>
        ))}
      </div>
      <div
        data-skin={active}
        className="flex min-h-[200px] items-center justify-center p-8"
        style={{ background: "var(--background)" }}
      >
        {preview}
      </div>
    </div>
  );
}
