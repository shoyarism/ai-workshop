import type { Metadata } from "next";

const BASE = "https://styleseed-demo.vercel.app";

const description =
  "A live pricing page built with StyleSeed — themeable across brand skins with " +
  "animated billing toggle and motion seeds. See how a design-system-driven " +
  "pricing UI looks across Toss, Stripe, and Linear styles.";

export const metadata: Metadata = {
  title: "Pricing — themeable pricing page demo",
  description,
  keywords: [
    "pricing page design",
    "pricing page template react",
    "saas pricing ui",
    "billing toggle animation",
    "tailwind pricing component",
    "design system pricing",
  ],
  alternates: { canonical: `${BASE}/pricing` },
  openGraph: {
    type: "website",
    url: `${BASE}/pricing`,
    title: "Pricing — themeable pricing page demo · StyleSeed",
    description,
    siteName: "StyleSeed",
    images: [{ url: `${BASE}/showcase-hero/pricing.png`, width: 1440, height: 900 }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Pricing — themeable pricing page demo · StyleSeed",
    description,
    images: [`${BASE}/showcase-hero/pricing.png`],
  },
};

export default function PricingLayout({ children }: { children: React.ReactNode }) {
  return children;
}
