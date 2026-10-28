import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { InteractionsGallery } from "./interactions-gallery";

export const metadata = {
  title: "Interaction Gallery — live micro-interactions",
  description:
    "Live, copy-ready micro-interaction patterns: toast, bottom sheet, speed-dial FAB, skeleton loading, number counter, swipe-to-delete, segmented control, and like burst. Built with framer-motion and StyleSeed motion seeds.",
};

export default function InteractionsPage() {
  return (
    <main className="min-h-screen bg-white text-neutral-900">
      <div className="mx-auto max-w-6xl px-6 py-12">
        <header className="mb-12">
          <Link
            href="/"
            className="inline-flex items-center gap-1 text-sm text-neutral-500 hover:text-neutral-900"
          >
            <ArrowLeft size={14} />
            StyleSeed home
          </Link>
          <h1 className="mt-4 text-4xl font-bold tracking-tight">Interaction gallery</h1>
          <p className="mt-3 max-w-2xl text-lg text-neutral-600">
            The micro-interactions that make an app feel alive — toasts, sheets, swipes, counters.
            Each one is live: click, drag, and tap to feel it. Built on framer-motion and
            StyleSeed&rsquo;s motion seeds, so every pattern carries a consistent personality.
          </p>
          <div className="mt-4 flex gap-3 text-sm">
            <Link
              href="/showcase"
              className="rounded-md bg-neutral-100 px-3 py-1.5 font-semibold text-neutral-700 hover:bg-neutral-200"
            >
              Showcase →
            </Link>
            <Link
              href="/motion"
              className="rounded-md bg-neutral-100 px-3 py-1.5 font-semibold text-neutral-700 hover:bg-neutral-200"
            >
              Motion seeds →
            </Link>
          </div>
        </header>

        <InteractionsGallery />

        <footer className="mt-16 border-t border-neutral-200 pt-6 text-sm text-neutral-500">
          Every interaction here is plain framer-motion plus a StyleSeed seed. Read the source on{" "}
          <a
            href="https://github.com/bitjaru/styleseed"
            className="font-semibold text-neutral-700 hover:text-neutral-900"
            target="_blank"
            rel="noreferrer"
          >
            GitHub
          </a>
          .
        </footer>
      </div>
    </main>
  );
}
