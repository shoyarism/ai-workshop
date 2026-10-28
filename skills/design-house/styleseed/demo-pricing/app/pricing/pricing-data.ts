export type Skin = "toss" | "raycast" | "arc";

export const SKINS: { id: Skin; label: string }[] = [
  { id: "toss", label: "Toss" },
  { id: "raycast", label: "Raycast" },
  { id: "arc", label: "Arc" },
];

export type Tier = {
  name: string;
  monthly: number;
  yearly: number;
  tagline: string;
  features: string[];
  highlighted?: boolean;
  cta: string;
};

export const TIERS: Tier[] = [
  {
    name: "Starter",
    monthly: 0,
    yearly: 0,
    tagline: "For solo builders kicking the tires.",
    features: [
      "1 project",
      "Community support",
      "Up to 1k MAU",
      "Basic analytics",
    ],
    cta: "Start free",
  },
  {
    name: "Pro",
    monthly: 24,
    yearly: 19,
    tagline: "Everything serious teams need to ship fast.",
    features: [
      "Unlimited projects",
      "Priority support",
      "Up to 100k MAU",
      "Advanced analytics",
      "Custom domains",
      "Team seats included",
    ],
    highlighted: true,
    cta: "Start 14-day trial",
  },
  {
    name: "Scale",
    monthly: 99,
    yearly: 79,
    tagline: "When uptime, SSO, and SLAs are non-negotiable.",
    features: [
      "Everything in Pro",
      "SSO + SAML",
      "99.99% uptime SLA",
      "Dedicated CSM",
      "Audit logs",
      "Custom contracts",
    ],
    cta: "Talk to sales",
  },
];
