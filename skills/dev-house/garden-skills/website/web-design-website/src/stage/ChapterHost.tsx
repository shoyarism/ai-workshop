import { useEffect, useRef, useState } from 'react';
import { chapters } from '../chapters';
import { useStep } from '../store/useStep';

/**
 * 装载当前章节，并处理章节间的极轻交叉转场。
 * 转场只在 chapterIndex 切换时发生；同章节内的 step 变化由章节自己负责。
 */
export function ChapterHost() {
  const { chapterIndex, localStep, direction } = useStep();
  const Current = chapters[chapterIndex];

  const [renderedIdx, setRenderedIdx] = useState(chapterIndex);
  const [phase, setPhase] = useState<'in' | 'out'>('in');
  const pendingRef = useRef<number | null>(null);

  useEffect(() => {
    if (chapterIndex === renderedIdx) return;
    pendingRef.current = chapterIndex;
    setPhase('out');
    const t = setTimeout(() => {
      setRenderedIdx(pendingRef.current!);
      setPhase('in');
    }, 220);
    return () => clearTimeout(t);
  }, [chapterIndex, renderedIdx]);

  const Active = chapters[renderedIdx] ?? Current;
  const themeClass = Active.theme === 'ink' ? 'theme-ink' : '';
  const Component = Active.Component;

  return (
    <div
      className={`chapter-host ${themeClass}`}
      data-phase={phase}
      data-chapter-id={Active.id}
      style={{
        position: 'absolute',
        inset: 0,
        background: 'var(--bg)',
        color: 'var(--fg)',
        opacity: phase === 'in' ? 1 : 0,
        transform: phase === 'in' ? 'translateY(0)' : 'translateY(8px)',
        transition: 'opacity 220ms var(--ease-exit), transform 220ms var(--ease-exit), background 480ms var(--ease-enter), color 480ms var(--ease-enter)',
      }}
    >
      <Component
        localStep={renderedIdx === chapterIndex ? localStep : Active.steps - 1}
        steps={Active.steps}
        direction={direction}
      />
    </div>
  );
}
