import { useEffect, useRef, useState } from 'react';

interface Props {
  to: number;
  from?: number;
  duration?: number;       // ms
  decimals?: number;
  prefix?: string;
  suffix?: string;
  /** 出场延迟 */
  delay?: number;
  className?: string;
  /** 是否显示符号位（如 + / -） */
  signed?: boolean;
}

const easeOutQuart = (t: number) => 1 - Math.pow(1 - t, 4);

/**
 * RAF 驱动的数字 count-up，default easeOutQuart。
 * 数字使用 tabular-nums 防止抖动。
 */
export function NumberTicker({
  to,
  from = 0,
  duration = 1400,
  decimals = 1,
  prefix = '',
  suffix = '',
  delay = 0,
  className,
  signed = false,
}: Props) {
  const [val, setVal] = useState(from);
  const startedRef = useRef(false);

  useEffect(() => {
    let raf = 0;
    let timer = 0;
    const start = () => {
      const t0 = performance.now();
      const tick = (now: number) => {
        const t = Math.min(1, (now - t0) / duration);
        const eased = easeOutQuart(t);
        setVal(from + (to - from) * eased);
        if (t < 1) raf = requestAnimationFrame(tick);
      };
      raf = requestAnimationFrame(tick);
    };
    if (delay > 0) {
      timer = window.setTimeout(start, delay);
    } else {
      start();
    }
    startedRef.current = true;
    return () => {
      cancelAnimationFrame(raf);
      clearTimeout(timer);
    };
  }, [to, from, duration, delay]);

  const display = (() => {
    const abs = Math.abs(val).toFixed(decimals);
    if (!signed) return abs;
    if (val < 0) return `−${abs}`;
    if (val > 0) return `+${abs}`;
    return abs;
  })();

  return (
    <span
      className={className}
      style={{ fontVariantNumeric: 'tabular-nums', display: 'inline-block' }}
    >
      {prefix}{display}{suffix}
    </span>
  );
}
