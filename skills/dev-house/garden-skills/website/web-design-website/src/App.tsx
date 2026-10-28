import { Stage } from './stage/Stage';
import { ChapterHost } from './stage/ChapterHost';
import { ProgressBar } from './stage/ProgressBar';
import { useHotKeys } from './stage/useHotKeys';
import { stepStore, useStep } from './store/useStep';
import { chapters } from './chapters';

function App() {
  useHotKeys();
  const { chapterIndex } = useStep();
  const theme = chapters[chapterIndex]?.theme ?? 'light';

  return (
    <div
      onClick={(e) => {
        // 任何带 data-no-step 的祖先都不触发推进
        const target = e.target as HTMLElement;
        if (target.closest('[data-no-step]')) return;
        stepStore.next();
      }}
    >
      <Stage theme={theme}>
        <ChapterHost />
      </Stage>
      <div data-no-step>
        <ProgressBar />
      </div>
    </div>
  );
}

export default App;
