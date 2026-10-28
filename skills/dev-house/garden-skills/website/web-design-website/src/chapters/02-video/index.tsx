import { useEffect, useRef } from 'react';
import type { ChapterContext, ChapterDef } from '../types';
import { Reveal } from '../../shared/Reveal';
import './Video.css';

/**
 * Chapter 02 · Anthropic 官方宣传片嵌入
 *
 * 浅色纸感背景 + 虚拟电视外框 + 16:9 视频。视频源：/video.mp4
 *
 * 仅保留电视外框 —— 不放任何文案 / eyebrow / caption。
 * - 进入时静音自动播放（绕过浏览器策略），用户可通过 controls 解除静音 / 暂停
 * - TV + 底座 data-no-step，操作 controls 不会推进
 * - 点击 TV 之外的留白才会推进到 Ch03
 */
function VideoChapter(_: ChapterContext) {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const v = videoRef.current;
    if (!v) return;
    v.currentTime = 0;
    const play = v.play();
    if (play && typeof play.catch === 'function') {
      play.catch(() => {/* 用户必须自行点击播放 */});
    }
    return () => {
      v.pause();
    };
  }, []);

  return (
    <section className="vid">
      <Reveal kind="rise" duration={900} delay={120} className="vid__tv-wrap">
        <div className="vid__tv" data-no-step>
          {/* 角注 4 颗螺丝 */}
          <span className="vid__screw vid__screw--tl" />
          <span className="vid__screw vid__screw--tr" />
          <span className="vid__screw vid__screw--bl" />
          <span className="vid__screw vid__screw--br" />

          {/* 顶部状态条 */}
          <div className="vid__topstrip">
            <span className="vid__led" />
            <span>ON · CH · 02</span>
            <span className="vid__topstrip-spacer" />
            <span>SIGNAL · STABLE</span>
          </div>

          {/* 屏幕 */}
          <div className="vid__screen">
            <div className="vid__scanlines" aria-hidden />
            <video
              ref={videoRef}
              src="/video.mp4"
              className="vid__video"
              controls
              playsInline
              muted
              autoPlay
            />
          </div>

          {/* 底部品牌条 */}
          <div className="vid__brandstrip">
            <span className="vid__brand-mark" />
            <span className="vid__brand-name">ANTHROPIC</span>
          </div>
        </div>

        {/* 底座 */}
        <div className="vid__stand" data-no-step>
          <span className="vid__stand-neck" />
          <span className="vid__stand-base" />
        </div>
      </Reveal>
    </section>
  );
}

const def: ChapterDef = {
  id: 'video',
  title: '官方宣传片',
  eyebrow: '02',
  steps: 1,
  theme: 'light',
  Component: VideoChapter,
};

export default def;
