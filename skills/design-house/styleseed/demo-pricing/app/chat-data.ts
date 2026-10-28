export type Skin = "toss" | "raycast" | "arc";

export const SKINS: { id: Skin; label: string }[] = [
  { id: "toss", label: "Toss" },
  { id: "raycast", label: "Raycast" },
  { id: "arc", label: "Arc" },
];

export type Conversation = {
  id: string;
  title: string;
  preview: string;
  time: string;
  unread?: boolean;
};

export const CONVERSATIONS: Conversation[] = [
  {
    id: "1",
    title: "Refactor pricing component",
    preview: "Sure — let me extract the tier card...",
    time: "now",
    unread: true,
  },
  {
    id: "2",
    title: "Tailwind v4 migration",
    preview: "The @theme block replaces tailwind.config.ts...",
    time: "2h",
  },
  {
    id: "3",
    title: "Framer Motion layout bug",
    preview: "Try wrapping it in LayoutGroup with a stable key.",
    time: "yesterday",
  },
  {
    id: "4",
    title: "shadcn/ui dark mode",
    preview: "Add the dark variant to your CSS variables...",
    time: "2d",
  },
  {
    id: "5",
    title: "Vercel deploy fails",
    preview: "Looks like the build is missing an env var.",
    time: "3d",
  },
];

export type ToolCall = {
  type: "tool";
  name: string;
  detail: string;
  status: "running" | "done";
};

export type Message =
  | { id: string; role: "user"; text: string }
  | { id: string; role: "assistant"; text: string; toolCall?: ToolCall; code?: { lang: string; body: string } };

export const MESSAGES: Message[] = [
  {
    id: "m1",
    role: "user",
    text: "Refactor my pricing card so each tier highlights its CTA differently. Use the brand gradient for the popular one.",
  },
  {
    id: "m2",
    role: "assistant",
    text: "On it. I'll extract a `TierCard` component and route the highlighted tier through the StyleSeed brand gradient token. One sec — checking your existing setup.",
    toolCall: {
      type: "tool",
      name: "Read",
      detail: "app/pricing/page.tsx",
      status: "done",
    },
  },
  {
    id: "m3",
    role: "assistant",
    text: "Found it. Here's the cleaned-up component — gradient is wired to `var(--gradient-brand)` so it morphs automatically when you swap skins:",
    code: {
      lang: "tsx",
      body: `<motion.button
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.98 }}
  className="w-full py-3 font-semibold"
  style={{
    background: tier.highlighted
      ? "var(--gradient-brand)"
      : "var(--card)",
    color: tier.highlighted
      ? "var(--brand-foreground)"
      : "var(--brand)",
    borderRadius: "var(--radius-lg)",
  }}
>
  {tier.cta}
</motion.button>`,
    },
  },
  {
    id: "m4",
    role: "user",
    text: "Perfect. Can you also add a hover lift?",
  },
];

export const STREAMING_REPLY =
  "Yes — wrapping the card in a motion.div with whileHover y:-6 will give you a nice springy lift. I'll match the duration to your skin's --duration-normal so it feels native to whichever brand you're previewing.";
