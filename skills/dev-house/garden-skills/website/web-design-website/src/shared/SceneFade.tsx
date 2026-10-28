import { useEffect, useRef, useState, type ReactNode } from 'react';

interface Props {
  active: boolean;
  /** 退出渐隐时长（ms） */
  exitMs?: number;
  /** 进入前的等待时长，留给上一幕退出（ms） */
  enterDelayMs?: number;
  children: ReactNode;
  className?: string;
}

/**
 * 场景级渐入渐出 + 延迟卸载。
 *
 * - active 为 true 时立刻挂载（默认延迟 enterDelayMs 后再淡入），让上一幕先 fade out
 * - active 为 false 时先淡出 exitMs 再卸载
 *
 * 用于章节内多幕之间的优雅切换，避免硬切 / 重叠。
 */
export function SceneFade({
  active,
  exitMs = 360,
  enterDelayMs = 220,
  children,
  className = '',
}: Props) {
  const [mounted, setMounted] = useState(active);
  const [shown, setShown] = useState(false);
  const timerRef = useRef<number | null>(null);

  useEffect(() => {
    if (timerRef.current) {
      clearTimeout(timerRef.current);
      timerRef.current = null;
    }
    if (active) {
      setMounted(true);
      // 让上一幕先开始 fade out，再淡入本幕
      timerRef.current = window.setTimeout(() => setShown(true), enterDelayMs);
    } else {
      setShown(false);
      timerRef.current = window.setTimeout(() => setMounted(false), exitMs);
    }
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, [active, exitMs, enterDelayMs]);

  if (!mounted) return null;

  return (
    <div
      className={`scene-fade ${className}`}
      data-shown={shown}
      style={{
        position: 'absolute',
        inset: 0,
        opacity: shown ? 1 : 0,
        transition: `opacity ${shown ? enterDelayMs + 80 : exitMs}ms cubic-bezier(.4,0,1,1)`,
        pointerEvents: shown ? 'auto' : 'none',
      }}
    >
      {children}
    </div>
  );
}
