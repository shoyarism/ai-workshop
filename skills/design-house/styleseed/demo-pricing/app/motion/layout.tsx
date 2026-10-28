import type { Metadata } from "next";
import { MOTION_LIBRARY } from "@engine/motion";

const BASE = "https://styleseed-demo.vercel.app";

// Keyword-positioned for how people actually search for this: framer-motion
// presets, named animation recipes, AI/vibe-coding motion, React micro-
// interactions — in both English and Korean.
const KEYWORDS = [
  "framer motion presets",
  "named animation presets",
  "react motion library",
  "framer motion examples",
  "micro interactions react",
  "ui animation recipes",
  "copy paste framer motion",
  "vibe coding animations",
  "AI motion design system",
  "tailwind motion presets",
  "toggle animation react",
  "프레이머 모션 프리셋",
  "리액트 애니메이션 라이브러리",
  "AI 모션 디자인",
  "바이브코딩 애니메이션",
  "UI 인터랙션 모음",
];

const description =
  "A named motion vocabulary for AI-assisted UI: 14+ distinct, copy-paste " +
  "framer-motion recipes (toggle-flip, toggle-curtain, reveal-blur, pop-in, " +
  "shimmer…). Click to preview, copy the snippet, or say the keyword while " +
  "vibe coding and the same animation lands in your code.";

export const metadata: Metadata = {
  title: "Motion Keywords — copy-paste framer-motion presets for vibe coding",
  description,
  keywords: KEYWORDS,
  alternates: { canonical: `${BASE}/motion` },
  openGraph: {
    type: "website",
    url: `${BASE}/motion`,
    title: "Motion Keywords — name the motion, drop it in, ship the feel",
    description,
    siteName: "StyleSeed",
    images: [{ url: `${BASE}/og/motion.png`, width: 1280, height: 640 }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Motion Keywords — copy-paste framer-motion presets",
    description,
    images: [`${BASE}/og/motion.png`],
  },
};

// ItemList JSON-LD so search engines see every named motion keyword as a
// discrete, indexable item — strengthens long-tail "toggle-flip framer
// motion"-style queries.
function jsonLd() {
  return {
    "@context": "https://schema.org",
    "@type": "ItemList",
    name: "StyleSeed Motion Keywords",
    description,
    url: `${BASE}/motion`,
    numberOfItems: MOTION_LIBRARY.length,
    itemListElement: MOTION_LIBRARY.map((m, i) => ({
      "@type": "ListItem",
      position: i + 1,
      name: m.key,
      description: m.vibe,
    })),
  };
}

export default function MotionLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd()) }}
      />
      {children}
    </>
  );
}
