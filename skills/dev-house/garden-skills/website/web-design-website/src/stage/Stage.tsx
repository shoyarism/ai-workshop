import { useEffect, useRef, useState, type ReactNode } from 'react';
import './Stage.css';

const STAGE_W = 1920;
const STAGE_H = 1080;

/** 舞台四周保留的最小留白（视口像素）—— 防止贴边 */
const SAFE_PAD = 24;

interface Props {
  children: ReactNode;
  /** 主题：light = 米底，ink = 深墨底 */
  theme?: 'light' | 'ink';
}

/**
 * 16:9 固定 1920×1080 舞台 —— 通过 CSS transform 缩放贴合视口，
 * 外层用 flex 居中 + 中心 origin 缩放，避免 translate% × scale 复合造成的偏移。
 */
export function Stage({ children, theme = 'light' }: Props) {
  const wrapRef = useRef<HTMLDivElement>(null);
  const [scale, setScale] = useState(1);

  useEffect(() => {
    const compute = () => {
      const vw = window.innerWidth - SAFE_PAD * 2;
      const vh = window.innerHeight - SAFE_PAD * 2;
      setScale(Math.min(vw / STAGE_W, vh / STAGE_H));
    };
    compute();
    window.addEventListener('resize', compute);
    return () => window.removeEventListener('resize', compute);
  }, []);

  return (
    <div className="stage-letterbox" ref={wrapRef}>
      <div
        className={`stage ${theme === 'ink' ? 'theme-ink' : ''}`}
        style={{
          width: STAGE_W,
          height: STAGE_H,
          transform: `scale(${scale})`,
        }}
      >
        {children}
      </div>
    </div>
  );
}
