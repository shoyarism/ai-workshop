import { useEffect, useState } from 'react';

/** 不停跳动的实时时间（HH:MM:SS） */
export function LiveClock({ className }: { className?: string }) {
  const [now, setNow] = useState(() => new Date());
  useEffect(() => {
    const id = window.setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(id);
  }, []);
  const pad = (n: number) => String(n).padStart(2, '0');
  return (
    <span className={className} style={{ fontVariantNumeric: 'tabular-nums' }}>
      {pad(now.getHours())}:{pad(now.getMinutes())}:{pad(now.getSeconds())}
    </span>
  );
}

/** 持续微抖的小数（模拟实时报价末位变化） */
export function FlickerNumber({
  base,
  amplitude = 0.05,
  decimals = 2,
  className,
  prefix = '',
  suffix = '',
  intervalMs = 1100,
}: {
  base: number;
  amplitude?: number;
  decimals?: number;
  className?: string;
  prefix?: string;
  suffix?: string;
  intervalMs?: number;
}) {
  const [v, setV] = useState(base);
  useEffect(() => {
    const id = window.setInterval(() => {
      const noise = (Math.random() * 2 - 1) * amplitude;
      setV(base + noise);
    }, intervalMs);
    return () => clearInterval(id);
  }, [base, amplitude, intervalMs]);
  return (
    <span className={className} style={{ fontVariantNumeric: 'tabular-nums' }}>
      {prefix}{v.toFixed(decimals)}{suffix}
    </span>
  );
}
