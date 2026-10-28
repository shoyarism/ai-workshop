import type { ComponentType } from 'react';

/** 单个章节的运行时上下文：传入到章节组件 props 中 */
export interface ChapterContext {
  /** 当前章节内的局部 step（0..steps-1） */
  localStep: number;
  /** 当前章节的总 step 数 */
  steps: number;
  /** 进入 / 离开方向（用于转场，正向 1 / 反向 -1） */
  direction: 1 | -1;
}

export interface ChapterDef {
  /** 唯一标识（用于 URL hash / 调试） */
  id: string;
  /** 中文标题（用于进度条 tooltip） */
  title: string;
  /** 英文 / 编号 eyebrow（视觉用） */
  eyebrow?: string;
  /** 章节内 step 数量（必须 >= 1） */
  steps: number;
  /** 主题：light = 米底，ink = 深墨底 */
  theme?: 'light' | 'ink';
  /** 章节组件 */
  Component: ComponentType<ChapterContext>;
}
