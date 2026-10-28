import { useEffect } from 'react';
import { stepStore } from '../store/useStep';

/**
 * 全局快捷键 + 点击驱动 step。
 * - 点击 stage 任意空白处：next
 * - Space / →：next
 * - ←：prev
 * - Backspace：归零（debug）
 * - 1..9：跳到对应章节（章节序号 1-indexed）
 *
 * 进度条 / 任意 [data-no-step] 元素的 click 必须 stopPropagation。
 *
 * 注意：使用 capture 阶段监听 + stopImmediatePropagation，
 * 否则一旦 <video> / <audio> 等媒体元素拿到焦点，原生控件会优先吃掉
 * Space / ← / → 等键，导致全局快捷键失效。
 */
export function useHotKeys() {
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      // 真正的输入框 / 可编辑区放过
      const tgt = e.target as HTMLElement | null;
      if (
        tgt instanceof HTMLInputElement ||
        tgt instanceof HTMLTextAreaElement ||
        (tgt && (tgt as HTMLElement).isContentEditable)
      ) {
        return;
      }

      let handled = false;

      switch (e.key) {
        case ' ':
        case 'Spacebar':
        case 'Enter':
        case 'ArrowRight':
          stepStore.next();
          handled = true;
          break;
        case 'ArrowLeft':
          stepStore.prev();
          handled = true;
          break;
        case 'Backspace':
          stepStore.goToGlobal(0);
          handled = true;
          break;
        default: {
          if (/^[1-9]$/.test(e.key)) {
            stepStore.goToChapter(parseInt(e.key, 10) - 1);
            handled = true;
          }
        }
      }

      if (handled) {
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        // 关键：把焦点从 <video>/<audio> 等媒体元素夺回来，
        // 否则下一次按键又会被原生控件吃掉。
        if (
          tgt instanceof HTMLVideoElement ||
          tgt instanceof HTMLAudioElement ||
          tgt instanceof HTMLButtonElement
        ) {
          tgt.blur();
        }
      }
    };
    // capture 阶段：抢在 video / audio 原生快捷键之前
    window.addEventListener('keydown', onKey, { capture: true });
    return () => window.removeEventListener('keydown', onKey, { capture: true } as EventListenerOptions);
  }, []);
}
