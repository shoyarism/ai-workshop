"use client";

import { useEffect, useRef, useState } from "react";
import {
  AnimatePresence,
  motion,
  useMotionValue,
  useTransform,
  animate,
} from "framer-motion";
import {
  Check,
  Heart,
  Image as ImageIcon,
  Mail,
  Plus,
  RefreshCw,
  Share2,
  Trash2,
} from "lucide-react";
import type { SeedId } from "@engine/motion";

const SILK_IN = { ease: [0.32, 0.72, 0, 1] as const, duration: 0.45 };

/* ============================================================
   Gallery shell
   ============================================================ */

type Demo = {
  id: string;
  title: string;
  blurb: string;
  seed: SeedId;
  Component: () => React.ReactNode;
};

const DEMOS: Demo[] = [
  { id: "toast", title: "Toast", blurb: "Slide-in notification that auto-dismisses.", seed: "spring", Component: ToastDemo },
  { id: "bottom-sheet", title: "Bottom sheet", blurb: "Draggable sheet that snaps to dismiss.", seed: "silk", Component: BottomSheetDemo },
  { id: "fab", title: "Speed-dial FAB", blurb: "Floating button that fans out actions.", seed: "spring", Component: FabDemo },
  { id: "skeleton", title: "Skeleton → content", blurb: "Loading placeholder swaps to real content.", seed: "silk", Component: SkeletonDemo },
  { id: "counter", title: "Number counter", blurb: "Value animates up on demand.", seed: "snap", Component: CounterDemo },
  { id: "swipe", title: "Swipe to delete", blurb: "Drag a row left to reveal delete.", seed: "snap", Component: SwipeDemo },
  { id: "segmented", title: "Segmented control", blurb: "Sliding indicator via shared layout.", seed: "spring", Component: SegmentedDemo },
  { id: "like", title: "Like burst", blurb: "Heart pops with a particle burst.", seed: "spring", Component: LikeDemo },
];

export function InteractionsGallery() {
  return (
    <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
      {DEMOS.map((d) => (
        <div
          key={d.id}
          className="flex flex-col overflow-hidden rounded-2xl border border-neutral-200 bg-white"
        >
          <div className="flex items-baseline justify-between border-b border-neutral-100 px-5 py-3.5">
            <div>
              <h3 className="text-[14px] font-bold tracking-tight text-neutral-900">
                {d.title}
              </h3>
              <p className="mt-0.5 text-[12px] text-neutral-500">{d.blurb}</p>
            </div>
            <span className="rounded-md bg-neutral-100 px-1.5 py-0.5 font-mono text-[10px] font-bold text-neutral-500">
              {d.seed}
            </span>
          </div>
          <div className="flex min-h-[220px] flex-1 items-center justify-center bg-neutral-50 p-6">
            <d.Component />
          </div>
        </div>
      ))}
    </div>
  );
}

/* ============================================================
   1. Toast
   ============================================================ */

function ToastDemo() {
  const [toasts, setToasts] = useState<number[]>([]);
  const nextId = useRef(0);

  const push = () => {
    const id = nextId.current++;
    setToasts((t) => [...t, id]);
    setTimeout(() => setToasts((t) => t.filter((x) => x !== id)), 2600);
  };

  return (
    <div className="relative flex h-full w-full flex-col items-center justify-center">
      <button
        type="button"
        onClick={push}
        className="rounded-lg bg-neutral-900 px-4 py-2 text-[13px] font-bold text-white"
      >
        Show toast
      </button>
      <div className="pointer-events-none absolute inset-x-0 bottom-0 flex flex-col items-center gap-2">
        <AnimatePresence>
          {toasts.map((id) => (
            <motion.div
              key={id}
              layout
              initial={{ opacity: 0, y: 20, scale: 0.9 }}
              animate={{ opacity: 1, y: 0, scale: 1, transition: { type: "spring", stiffness: 400, damping: 28 } }}
              exit={{ opacity: 0, y: 10, scale: 0.95, transition: { duration: 0.18 } }}
              className="flex items-center gap-2 rounded-xl bg-neutral-900 px-3.5 py-2.5 text-[12px] font-semibold text-white shadow-lg"
            >
              <span className="flex h-5 w-5 items-center justify-center rounded-full bg-emerald-500">
                <Check size={12} />
              </span>
              Saved to your library
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
}

/* ============================================================
   2. Bottom sheet
   ============================================================ */

function BottomSheetDemo() {
  const [open, setOpen] = useState(false);

  return (
    <div className="relative h-[200px] w-[260px] overflow-hidden rounded-2xl border border-neutral-200 bg-white">
      <div className="flex h-full items-center justify-center">
        <button
          type="button"
          onClick={() => setOpen(true)}
          className="rounded-lg bg-neutral-900 px-4 py-2 text-[13px] font-bold text-white"
        >
          Open sheet
        </button>
      </div>

      <AnimatePresence>
        {open && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setOpen(false)}
              className="absolute inset-0 bg-black/30"
            />
            <motion.div
              initial={{ y: "100%" }}
              animate={{ y: 0, transition: SILK_IN }}
              exit={{ y: "100%", transition: { duration: 0.25 } }}
              drag="y"
              dragConstraints={{ top: 0, bottom: 0 }}
              dragElastic={{ top: 0, bottom: 0.6 }}
              onDragEnd={(_, info) => {
                if (info.offset.y > 60) setOpen(false);
              }}
              className="absolute inset-x-0 bottom-0 rounded-t-2xl bg-white p-4 shadow-2xl"
            >
              <div className="mx-auto mb-3 h-1 w-10 rounded-full bg-neutral-300" />
              <div className="text-[13px] font-bold text-neutral-900">Share this page</div>
              <div className="mt-3 flex justify-around">
                {[Mail, Share2, ImageIcon].map((Icon, i) => (
                  <button key={i} type="button" className="flex flex-col items-center gap-1.5 text-[11px] text-neutral-600">
                    <span className="flex h-10 w-10 items-center justify-center rounded-full bg-neutral-100">
                      <Icon size={16} />
                    </span>
                  </button>
                ))}
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
}

/* ============================================================
   3. Speed-dial FAB
   ============================================================ */

function FabDemo() {
  const [open, setOpen] = useState(false);
  const actions = [Mail, ImageIcon, Share2];

  return (
    <div className="relative h-[200px] w-[200px]">
      <div className="absolute bottom-4 right-4">
        <AnimatePresence>
          {open &&
            actions.map((Icon, i) => (
              <motion.button
                key={i}
                type="button"
                initial={{ opacity: 0, y: 0, scale: 0.5 }}
                animate={{
                  opacity: 1,
                  y: -(i + 1) * 52,
                  scale: 1,
                  transition: { type: "spring", stiffness: 400, damping: 22, delay: i * 0.04 },
                }}
                exit={{ opacity: 0, y: 0, scale: 0.5, transition: { duration: 0.12 } }}
                className="absolute bottom-0 right-0 flex h-11 w-11 items-center justify-center rounded-full bg-white text-neutral-700 shadow-lg"
              >
                <Icon size={16} />
              </motion.button>
            ))}
        </AnimatePresence>
        <motion.button
          type="button"
          onClick={() => setOpen((o) => !o)}
          whileTap={{ scale: 0.9 }}
          animate={{ rotate: open ? 45 : 0 }}
          transition={{ type: "spring", stiffness: 400, damping: 20 }}
          className="relative flex h-14 w-14 items-center justify-center rounded-full bg-neutral-900 text-white shadow-xl"
        >
          <Plus size={22} />
        </motion.button>
      </div>
    </div>
  );
}

/* ============================================================
   4. Skeleton → content
   ============================================================ */

function SkeletonDemo() {
  const [loading, setLoading] = useState(true);

  const reload = () => {
    setLoading(true);
    setTimeout(() => setLoading(false), 1400);
  };

  useEffect(() => {
    const t = setTimeout(() => setLoading(false), 1400);
    return () => clearTimeout(t);
  }, []);

  return (
    <div className="w-[240px]">
      <div className="rounded-xl border border-neutral-200 bg-white p-4">
        <AnimatePresence mode="wait">
          {loading ? (
            <motion.div
              key="skeleton"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex items-center gap-3"
            >
              <div className="h-10 w-10 shrink-0 animate-pulse rounded-full bg-neutral-200" />
              <div className="flex-1 space-y-2">
                <div className="h-3 w-3/4 animate-pulse rounded bg-neutral-200" />
                <div className="h-3 w-1/2 animate-pulse rounded bg-neutral-200" />
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="content"
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex items-center gap-3"
            >
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-blue-500 text-[13px] font-bold text-white">
                SC
              </div>
              <div>
                <div className="text-[13px] font-bold text-neutral-900">Sam Choi</div>
                <div className="text-[11px] text-neutral-500">Product designer</div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
      <button
        type="button"
        onClick={reload}
        className="mt-3 flex w-full items-center justify-center gap-1.5 rounded-lg bg-neutral-900 px-3 py-2 text-[12px] font-bold text-white"
      >
        <RefreshCw size={12} />
        Reload
      </button>
    </div>
  );
}

/* ============================================================
   5. Number counter
   ============================================================ */

function CounterDemo() {
  const count = useMotionValue(0);
  const rounded = useTransform(count, (v) => Math.round(v).toLocaleString());
  const [display, setDisplay] = useState("0");

  useEffect(() => {
    const unsub = rounded.on("change", setDisplay);
    return unsub;
  }, [rounded]);

  const run = () => {
    count.set(0);
    animate(count, 128400, { duration: 1.2, ease: [0.22, 1, 0.36, 1] });
  };

  return (
    <div className="flex flex-col items-center">
      <div className="text-[11px] font-bold uppercase tracking-widest text-neutral-500">
        Followers
      </div>
      <div className="mt-1 text-[40px] font-bold tabular-nums leading-none tracking-tight text-neutral-900">
        {display}
      </div>
      <button
        type="button"
        onClick={run}
        className="mt-5 rounded-lg bg-neutral-900 px-4 py-2 text-[13px] font-bold text-white"
      >
        Count up
      </button>
    </div>
  );
}

/* ============================================================
   6. Swipe to delete
   ============================================================ */

function SwipeDemo() {
  const [rows, setRows] = useState([
    { id: 1, name: "Northstar Studio", amount: "$842" },
    { id: 2, name: "Maple & Stone", amount: "$199" },
    { id: 3, name: "Glacier Labs", amount: "$49" },
  ]);

  return (
    <div className="w-[260px] space-y-2">
      <AnimatePresence>
        {rows.map((row) => (
          <SwipeRow
            key={row.id}
            row={row}
            onDelete={() => setRows((r) => r.filter((x) => x.id !== row.id))}
          />
        ))}
      </AnimatePresence>
      {rows.length === 0 && (
        <button
          type="button"
          onClick={() =>
            setRows([
              { id: Date.now(), name: "Northstar Studio", amount: "$842" },
              { id: Date.now() + 1, name: "Maple & Stone", amount: "$199" },
              { id: Date.now() + 2, name: "Glacier Labs", amount: "$49" },
            ])
          }
          className="w-full rounded-lg bg-neutral-900 px-3 py-2 text-[12px] font-bold text-white"
        >
          Reset rows
        </button>
      )}
    </div>
  );
}

function SwipeRow({
  row,
  onDelete,
}: {
  row: { id: number; name: string; amount: string };
  onDelete: () => void;
}) {
  const x = useMotionValue(0);

  return (
    <motion.div
      layout
      exit={{ opacity: 0, height: 0, transition: { duration: 0.2 } }}
      className="relative overflow-hidden rounded-xl"
    >
      <div className="absolute inset-y-0 right-0 flex w-20 items-center justify-center bg-red-500 text-white">
        <Trash2 size={16} />
      </div>
      <motion.div
        drag="x"
        style={{ x }}
        dragConstraints={{ left: -80, right: 0 }}
        dragElastic={0.1}
        onDragEnd={(_, info) => {
          if (info.offset.x < -50) {
            animate(x, -300, { duration: 0.2 }).then(onDelete);
          } else {
            animate(x, 0, { type: "spring", stiffness: 400, damping: 30 });
          }
        }}
        className="relative flex cursor-grab items-center justify-between bg-white px-4 py-3 active:cursor-grabbing"
      >
        <span className="text-[13px] font-bold text-neutral-900">{row.name}</span>
        <span className="text-[13px] font-bold text-neutral-900">{row.amount}</span>
      </motion.div>
    </motion.div>
  );
}

/* ============================================================
   7. Segmented control
   ============================================================ */

function SegmentedDemo() {
  const options = ["Day", "Week", "Month"];
  const [active, setActive] = useState(1);

  return (
    <div className="inline-flex rounded-xl bg-neutral-200 p-1">
      {options.map((opt, i) => (
        <button
          key={opt}
          type="button"
          onClick={() => setActive(i)}
          className="relative px-5 py-1.5 text-[13px] font-bold"
          style={{ color: active === i ? "#0a0a0a" : "#737373" }}
        >
          {active === i && (
            <motion.span
              layoutId="segmented-indicator"
              transition={{ type: "spring", stiffness: 400, damping: 32 }}
              className="absolute inset-0 rounded-lg bg-white shadow-sm"
            />
          )}
          <span className="relative z-10">{opt}</span>
        </button>
      ))}
    </div>
  );
}

/* ============================================================
   8. Like burst
   ============================================================ */

function LikeDemo() {
  const [liked, setLiked] = useState(false);

  return (
    <button
      type="button"
      onClick={() => setLiked((l) => !l)}
      className="relative flex h-20 w-20 items-center justify-center"
    >
      {/* particle burst */}
      <AnimatePresence>
        {liked &&
          Array.from({ length: 6 }).map((_, i) => {
            const angle = (i / 6) * Math.PI * 2;
            return (
              <motion.span
                key={i}
                initial={{ x: 0, y: 0, opacity: 1, scale: 1 }}
                animate={{
                  x: Math.cos(angle) * 34,
                  y: Math.sin(angle) * 34,
                  opacity: 0,
                  scale: 0.4,
                  transition: { duration: 0.5, ease: "easeOut" },
                }}
                className="absolute h-2 w-2 rounded-full bg-rose-400"
              />
            );
          })}
      </AnimatePresence>
      <motion.span
        animate={liked ? { scale: [1, 1.4, 1] } : { scale: 1 }}
        transition={{ type: "spring", stiffness: 400, damping: 14 }}
      >
        <Heart
          size={40}
          strokeWidth={2}
          className={liked ? "fill-rose-500 text-rose-500" : "text-neutral-400"}
        />
      </motion.span>
    </button>
  );
}
