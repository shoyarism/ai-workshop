import { createElement, type CSSProperties, type ReactNode } from 'react';
import './Reveal.css';

type RevealKind =
  | 'rise'      // 默认：下方 24px + opacity
  | 'fall'      // 顶部 -24px + opacity
  | 'fade'      // 仅 opacity
  | 'blur'      // blur 16px → 0
  | 'wipe-r'    // 自左 wipe
  | 'tight'     // letter-spacing 0.4em → 0
  ;

type AsTag = 'div' | 'span' | 'h1' | 'h2' | 'h3' | 'p' | 'em' | 'strong';

interface Props {
  children: ReactNode;
  delay?: number;          // ms
  duration?: number;       // ms，默认 720
  kind?: RevealKind;
  className?: string;
  style?: CSSProperties;
  as?: AsTag;
}

/**
 * 入场动画包装 —— 通过 React 条件挂载触发每次重新进入时重播。
 * 配合上层 `localStep >= n && <Reveal>...</Reveal>` 即可。
 */
export function Reveal({
  children,
  delay = 0,
  duration = 720,
  kind = 'rise',
  className = '',
  style,
  as = 'div',
}: Props) {
  return createElement(
    as,
    {
      className: `reveal reveal--${kind} ${className}`.trim(),
      style: {
        animationDelay: `${delay}ms`,
        animationDuration: `${duration}ms`,
        ...style,
      },
    },
    children,
  );
}
