"use client";

import { useState } from "react";
import { motion, AnimatePresence, LayoutGroup } from "framer-motion";
import { Check, Sparkles } from "lucide-react";
import { SKINS, TIERS, type Skin, type Tier } from "./pricing-data";

export default function Page() {
  const [skin, setSkin] = useState<Skin>("toss");
  const [yearly, setYearly] = useState(false);

  return (
    <div
      data-skin={skin}
      className="min-h-screen w-full"
      style={{
        background: "var(--background)",
        color: "var(--foreground)",
      }}
    >
      <div className="mx-auto max-w-6xl px-6 py-16 sm:py-24">
        <SkinSwitcher skin={skin} setSkin={setSkin} />

        <motion.div
          key={skin + "-header"}
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: [0.34, 1.56, 0.64, 1] }}
          className="mt-12 text-center"
        >
          <BrandBadge />
          <h1
            className="mt-6 text-5xl sm:text-6xl font-semibold tracking-tight"
            style={{ letterSpacing: "-0.02em" }}
          >
            Pricing that scales with you
          </h1>
          <p
            className="mt-5 text-lg max-w-xl mx-auto"
            style={{ color: "var(--text-secondary)" }}
          >
            Same component, three brand DNAs. Powered by{" "}
            <span style={{ color: "var(--brand)", fontWeight: 600 }}>
              StyleSeed
            </span>
            .
          </p>
        </motion.div>

        <BillingToggle yearly={yearly} setYearly={setYearly} />

        <LayoutGroup>
          <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {TIERS.map((tier, i) => (
              <TierCard
                key={tier.name}
                tier={tier}
                yearly={yearly}
                index={i}
                skin={skin}
              />
            ))}
          </div>
        </LayoutGroup>

        <p
          className="mt-16 text-center text-sm"
          style={{ color: "var(--text-secondary)" }}
        >
          No credit card required. Cancel anytime.
        </p>
      </div>
    </div>
  );
}

function SkinSwitcher({
  skin,
  setSkin,
}: {
  skin: Skin;
  setSkin: (s: Skin) => void;
}) {
  return (
    <div className="flex justify-center">
      <div
        className="inline-flex items-center gap-1 p-1.5 rounded-full"
        style={{
          background: "var(--muted)",
          border: "1px solid var(--border)",
        }}
      >
        {SKINS.map((s) => {
          const active = skin === s.id;
          return (
            <button
              key={s.id}
              onClick={() => setSkin(s.id)}
              className="relative px-5 py-2 text-sm font-medium rounded-full transition-colors"
              style={{
                color: active ? "var(--brand-foreground)" : "var(--foreground)",
              }}
            >
              {active && (
                <motion.span
                  layoutId="skin-pill"
                  className="absolute inset-0 rounded-full"
                  style={{ background: "var(--gradient-brand)" }}
                  transition={{ type: "spring", stiffness: 380, damping: 32 }}
                />
              )}
              <span className="relative z-10">{s.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}

function BrandBadge() {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.4, delay: 0.1 }}
      className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-sm font-medium"
      style={{
        background: "var(--brand-tint)",
        color: "var(--brand)",
        border: "1px solid var(--border)",
      }}
    >
      <Sparkles size={14} />
      <span>Built with StyleSeed</span>
    </motion.div>
  );
}

function BillingToggle({
  yearly,
  setYearly,
}: {
  yearly: boolean;
  setYearly: (b: boolean) => void;
}) {
  return (
    <div className="mt-10 flex items-center justify-center gap-4">
      <span
        className="text-sm font-medium"
        style={{
          color: yearly ? "var(--text-secondary)" : "var(--foreground)",
        }}
      >
        Monthly
      </span>
      <button
        onClick={() => setYearly(!yearly)}
        className="relative h-7 w-14 rounded-full transition-colors box-content"
        style={{
          background: yearly ? "var(--gradient-brand)" : "var(--muted)",
          border: "1px solid var(--border)",
        }}
        aria-label="Toggle billing"
      >
        <motion.span
          className="absolute top-1 left-1 h-5 w-5 rounded-full bg-white shadow-md"
          animate={{ x: yearly ? 28 : 0 }}
          transition={{ type: "spring", stiffness: 500, damping: 30 }}
        />
      </button>
      <span
        className="text-sm font-medium flex items-center gap-2"
        style={{
          color: yearly ? "var(--foreground)" : "var(--text-secondary)",
        }}
      >
        Yearly
        <span
          className="text-xs px-2 py-0.5 rounded-full font-semibold"
          style={{
            background: "var(--brand-tint)",
            color: "var(--brand)",
          }}
        >
          –20%
        </span>
      </span>
    </div>
  );
}

function TierCard({
  tier,
  yearly,
  index,
  skin,
}: {
  tier: Tier;
  yearly: boolean;
  index: number;
  skin: Skin;
}) {
  const price = yearly ? tier.yearly : tier.monthly;

  return (
    <motion.div
      layout
      key={skin + tier.name}
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.5,
        delay: index * 0.08,
        ease: [0.34, 1.56, 0.64, 1],
      }}
      whileHover={{ y: -6 }}
      className="relative p-8 flex flex-col"
      style={{
        background: "var(--card)",
        color: "var(--card-foreground)",
        border: "1px solid var(--border)",
        borderRadius: "var(--radius-xl)",
        boxShadow: tier.highlighted
          ? "var(--shadow-card-hover)"
          : "var(--shadow-card)",
      }}
    >
      {tier.highlighted && (
        <div
          className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full text-xs font-semibold whitespace-nowrap"
          style={{
            background: "var(--gradient-brand)",
            color: "var(--brand-foreground)",
            boxShadow: "var(--shadow-button)",
          }}
        >
          Most popular
        </div>
      )}

      <div className="flex items-baseline justify-between">
        <h3 className="text-xl font-semibold">{tier.name}</h3>
      </div>
      <p
        className="mt-2 text-sm min-h-[40px]"
        style={{ color: "var(--text-secondary)" }}
      >
        {tier.tagline}
      </p>

      <div className="mt-6 flex items-baseline gap-1">
        <span className="text-sm" style={{ color: "var(--text-secondary)" }}>
          $
        </span>
        <AnimatePresence mode="popLayout">
          <motion.span
            key={price}
            initial={{ y: 16, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: -16, opacity: 0 }}
            transition={{ duration: 0.25, ease: "easeOut" }}
            className="text-5xl font-bold tracking-tight tabular-nums"
          >
            {price}
          </motion.span>
        </AnimatePresence>
        <span
          className="ml-1 text-sm"
          style={{ color: "var(--text-secondary)" }}
        >
          /mo
        </span>
      </div>

      <ul className="mt-8 space-y-3 flex-1">
        {tier.features.map((f, i) => (
          <motion.li
            key={f}
            initial={{ opacity: 0, x: -8 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 + i * 0.05 }}
            className="flex items-start gap-3 text-sm"
          >
            <span
              className="mt-0.5 flex h-5 w-5 items-center justify-center rounded-full shrink-0"
              style={{
                background: "var(--brand-tint)",
                color: "var(--brand)",
              }}
            >
              <Check size={12} strokeWidth={3} />
            </span>
            <span>{f}</span>
          </motion.li>
        ))}
      </ul>

      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        className="mt-8 w-full py-3 px-4 font-semibold text-sm transition-all"
        style={{
          background: tier.highlighted
            ? "var(--gradient-brand)"
            : "var(--card)",
          color: tier.highlighted ? "var(--brand-foreground)" : "var(--brand)",
          border: tier.highlighted
            ? "1px solid transparent"
            : "1px solid var(--border)",
          borderRadius: "var(--radius-lg)",
          boxShadow: tier.highlighted ? "var(--shadow-button)" : "none",
        }}
      >
        {tier.cta}
      </motion.button>
    </motion.div>
  );
}
