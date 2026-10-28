import { useSyncExternalStore } from 'react';
import { chapters } from '../chapters';

/**
 * 全局 step 状态 —— 一个轻量手写 store。
 *
 * - globalStep: 跨章节累加索引。0 = 第 1 章 step 0。
 * - 点击 / Space / →：next() → globalStep + 1
 * - ←：prev() → globalStep - 1
 * - 1-9：goToChapter(i)
 * - 进度条拖动：goToGlobal(n)
 */

type Listener = () => void;

interface Snapshot {
  globalStep: number;
  totalSteps: number;
  chapterIndex: number;
  localStep: number;
  direction: 1 | -1;
}

let listeners = new Set<Listener>();

const totalSteps = () =>
  chapters.reduce((acc, c) => acc + c.steps, 0);

/** 给定 globalStep，求章节 index 与 localStep */
function locate(global: number): { chapterIndex: number; localStep: number } {
  let acc = 0;
  for (let i = 0; i < chapters.length; i++) {
    const next = acc + chapters[i].steps;
    if (global < next) return { chapterIndex: i, localStep: global - acc };
    acc = next;
  }
  // 越界 → 最后一章最后一步
  const last = chapters.length - 1;
  return { chapterIndex: last, localStep: chapters[last].steps - 1 };
}

/** 求章节起始 globalStep */
export function chapterStartGlobal(chapterIndex: number): number {
  let acc = 0;
  for (let i = 0; i < chapterIndex; i++) acc += chapters[i].steps;
  return acc;
}

let snapshot: Snapshot = {
  globalStep: 0,
  totalSteps: totalSteps(),
  chapterIndex: 0,
  localStep: 0,
  direction: 1,
};

function emit() {
  listeners.forEach((l) => l());
}

function set(globalStep: number, direction: 1 | -1) {
  const total = totalSteps();
  const clamped = Math.max(0, Math.min(total - 1, globalStep));
  if (clamped === snapshot.globalStep) return;
  const loc = locate(clamped);
  snapshot = {
    globalStep: clamped,
    totalSteps: total,
    chapterIndex: loc.chapterIndex,
    localStep: loc.localStep,
    direction,
  };
  emit();
}

export const stepStore = {
  subscribe(l: Listener) {
    listeners.add(l);
    return () => listeners.delete(l);
  },
  getSnapshot() {
    return snapshot;
  },
  next() { set(snapshot.globalStep + 1, 1); },
  prev() { set(snapshot.globalStep - 1, -1); },
  goToGlobal(n: number) {
    const dir: 1 | -1 = n >= snapshot.globalStep ? 1 : -1;
    set(n, dir);
  },
  goToChapter(chapterIndex: number) {
    const target = chapterStartGlobal(chapterIndex);
    const dir: 1 | -1 = target >= snapshot.globalStep ? 1 : -1;
    set(target, dir);
  },
};

export function useStep(): Snapshot {
  return useSyncExternalStore(stepStore.subscribe, stepStore.getSnapshot, stepStore.getSnapshot);
}
