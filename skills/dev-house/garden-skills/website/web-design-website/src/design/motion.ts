/**
 * 全局动效语言 —— 与 tokens.css 中的 --ease-* / --d-* 保持同步
 */

export const ease = {
  enter: 'cubic-bezier(.2, .8, .2, 1)',
  exit: 'cubic-bezier(.4, 0, 1, 1)',
  emphasized: 'cubic-bezier(.6, -0.05, .2, 1.2)',
} as const;

export const dur = {
  micro: 200,
  base: 480,
  hero: 900,
  epic: 1600,
} as const;

export type EaseName = keyof typeof ease;
export type DurName = keyof typeof dur;
