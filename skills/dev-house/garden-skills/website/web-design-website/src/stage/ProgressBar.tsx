import { useEffect, useRef, useState } from 'react';
import { chapters } from '../chapters';
import { stepStore, useStep, chapterStartGlobal } from '../store/useStep';
import './ProgressBar.css';

/**
 * 隐形进度条
 * - 默认完全透明、占据底部 12px 热区
 * - 鼠标进入热区后淡入；离开 1.2s 后淡出
 * - 点击 / 拖动可跳转 globalStep
 * - 顶部细线 + 章节刻度 + 当前章节 tooltip
 *
 * 注意：录屏时只要鼠标不靠近底部，就完全不可见。
 */
export function ProgressBar() {
  const { globalStep, totalSteps, chapterIndex } = useStep();
  const [visible, setVisible] = useState(false);
  const draggingRef = useRef(false);
  const hideTimerRef = useRef<number | null>(null);
  const barRef = useRef<HTMLDivElement>(null);

  const show = () => {
    if (hideTimerRef.current) {
      clearTimeout(hideTimerRef.current);
      hideTimerRef.current = null;
    }
    setVisible(true);
  };

  const scheduleHide = () => {
    if (draggingRef.current) return;
    if (hideTimerRef.current) clearTimeout(hideTimerRef.current);
    hideTimerRef.current = window.setTimeout(() => setVisible(false), 1200);
  };

  const seekFromEvent = (clientX: number) => {
    const el = barRef.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const ratio = Math.max(0, Math.min(1, (clientX - rect.left) / rect.width));
    const target = Math.round(ratio * (totalSteps - 1));
    stepStore.goToGlobal(target);
  };

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      if (draggingRef.current) seekFromEvent(e.clientX);
    };
    const onUp = () => {
      draggingRef.current = false;
      scheduleHide();
    };
    window.addEventListener('mousemove', onMove);
    window.addEventListener('mouseup', onUp);
    return () => {
      window.removeEventListener('mousemove', onMove);
      window.removeEventListener('mouseup', onUp);
    };
  }, [totalSteps]);

  // 章节刻度（每章起始 globalStep 的归一化位置）
  const ticks = chapters.map((_, i) => chapterStartGlobal(i) / Math.max(1, totalSteps - 1));
  const progress = totalSteps > 1 ? globalStep / (totalSteps - 1) : 0;
  const currentChapter = chapters[chapterIndex];

  return (
    <div
      className={`progress-zone ${visible ? 'is-visible' : ''}`}
      onMouseEnter={show}
      onMouseLeave={scheduleHide}
      onClick={(e) => e.stopPropagation()}
    >
      <div className="progress-meta">
        <span className="progress-meta__num">
          {String(chapterIndex + 1).padStart(2, '0')}
        </span>
        <span className="progress-meta__title">{currentChapter.title}</span>
        <span className="progress-meta__count">
          {globalStep + 1} / {totalSteps}
        </span>
      </div>

      <div
        className="progress-bar"
        ref={barRef}
        onMouseDown={(e) => {
          draggingRef.current = true;
          seekFromEvent(e.clientX);
        }}
      >
        <div className="progress-bar__track" />
        <div
          className="progress-bar__fill"
          style={{ transform: `scaleX(${progress})` }}
        />
        {ticks.map((r, i) => (
          <button
            key={i}
            className={`progress-bar__tick ${i === chapterIndex ? 'is-current' : ''}`}
            style={{ left: `${r * 100}%` }}
            title={chapters[i].title}
            onClick={(e) => {
              e.stopPropagation();
              stepStore.goToChapter(i);
            }}
          />
        ))}
      </div>
    </div>
  );
}
