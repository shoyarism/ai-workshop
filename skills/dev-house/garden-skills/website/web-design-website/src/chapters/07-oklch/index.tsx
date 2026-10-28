import type { ChapterContext, ChapterDef } from '../types';
import { Reveal } from '../../shared/Reveal';
import { SceneFade } from '../../shared/SceneFade';
import './Oklch.css';

/**
 * Chapter 07 · 第四部分：oklch 配色
 *
 * 口播原顺序（严格对齐）：
 *   1. "他的配色策略分成了：优先用品牌色；不够就用 oklch 派生衍生色；绝对不要凭空编新色。"
 *   2. "为什么是 oklch 呢？"
 *   3. "传统的 HSL色彩空间有个大问题 — 感知不均匀。"
 *      "同样的亮度值，黄色看着比蓝色亮一大截。"
 *   4. "oklch 是感知均匀的色彩空间。保持亮度和色度不变，只转色相角，出来的颜色自然就和谐。"
 *   5. "这个细节看着小，但网页端高级感一下就上来了。"
 *
 * 节奏（5 步 / step 0..4）：
 *  0  原文 prompt（L41-43）三段被逐句"点亮" —— 引出策略原文
 *  1  三层策略卡：① 品牌色 ② oklch 派生 ③ 禁止凭空造色
 *  2  pivot 大字 "为什么是 oklch ？" + 副："HSL 有个大问题 —— 感知不均匀"
 *  3  HSL vs OKLCH 双色相条对比 + 感知亮度曲线 + 黄色 spotlight
 *  4  收尾："网页端 高级感 ↑"
 */

const HUES = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330];

/** HSL 感知亮度（粗略 sRGB BT.709 相对亮度） */
function hslPerceived(h: number): number {
  const s = 0.7;
  const l = 0.6;
  const c = (1 - Math.abs(2 * l - 1)) * s;
  const hh = h / 60;
  const x = c * (1 - Math.abs((hh % 2) - 1));
  let r = 0, g = 0, b = 0;
  if      (hh < 1) { r = c; g = x; }
  else if (hh < 2) { r = x; g = c; }
  else if (hh < 3) { g = c; b = x; }
  else if (hh < 4) { g = x; b = c; }
  else if (hh < 5) { r = x; b = c; }
  else             { r = c; b = x; }
  const m = l - c / 2;
  r += m; g += m; b += m;
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function Oklch({ localStep }: ChapterContext) {
  const at = (n: number) => localStep >= n;

  const sceneSrc     = localStep <= 0;
  const sceneRules   = localStep === 1;
  const scenePivot   = localStep === 2;
  const sceneCompare = localStep === 3;
  const sceneClose   = localStep >= 4;

  return (
    <section className="ok">
      {/* ════════ Scene SOURCE（step 0）—— 原文先出 ════════ */}
      <SceneFade active={sceneSrc} exitMs={420} enterDelayMs={120}>
        <div className="ok__src-scene">
          <Reveal kind="fade" duration={620} delay={80} className="ok__src-eyebrow">
            <span className="ok__src-bracket">[</span>
            <span className="ok__src-label">SYSTEM PROMPT</span>
            <span className="ok__src-sep">·</span>
            <span className="ok__src-line">L41-43</span>
            <span className="ok__src-sep">/</span>
            <span className="ok__src-mute">Color Strategy 原文</span>
            <span className="ok__src-bracket">]</span>
          </Reveal>

          <Reveal kind="rise" duration={1100} delay={280} className="ok__src-block">
            <div className="ok__src-line-row ok__src-line-row--1">
              <span className="ok__src-num">L41</span>
              <span className="ok__src-text">
                Color usage: try to use colors from{' '}
                <em className="ok__src-h ok__src-h--1">brand / design system</em>.
              </span>
            </div>
            <div className="ok__src-line-row ok__src-line-row--2">
              <span className="ok__src-num">L42</span>
              <span className="ok__src-text">
                If too restrictive, use{' '}
                <em className="ok__src-h ok__src-h--2">oklch</em>{' '}
                to define harmonious colors that match.
              </span>
            </div>
            <div className="ok__src-line-row ok__src-line-row--3">
              <span className="ok__src-num">L43</span>
              <span className="ok__src-text">
                <em className="ok__src-h ok__src-h--3">Avoid inventing</em>{' '}
                new colors from scratch.
              </span>
            </div>
          </Reveal>

          <Reveal kind="fade" duration={780} delay={2200} className="ok__src-foot">
            三段 —— 一套<em>分层</em>的配色策略
          </Reveal>
        </div>
      </SceneFade>

      {/* ════════ Scene RULES（step 1）—— 三层策略 ════════ */}
      <SceneFade active={sceneRules} exitMs={420} enterDelayMs={420}>
        <div className="ok__rules-scene">
          <Reveal kind="rise" duration={780} delay={80} className="ok__rules-head" as="h2">
            配色策略 —— <em>三层防线</em>
          </Reveal>

          <div className="ok__rules">
            {/* 第 1 层 */}
            <Reveal kind="rise" duration={780} delay={220} className="ok__rule ok__rule--good">
              <div className="ok__rule-num">01</div>
              <div className="ok__rule-body">
                <div className="ok__rule-title">优先品牌色</div>
                <div className="ok__rule-desc">已有 design system → 直接复用，别"再创造"</div>
                <div className="ok__rule-swatches">
                  <span style={{ background: 'oklch(0.965 0.018 78)' }} />
                  <span style={{ background: 'oklch(0.700 0.170 42)' }} />
                  <span style={{ background: 'oklch(0.275 0.012 60)' }} />
                </div>
              </div>
              <div className="ok__rule-mark ok__rule-mark--good">✓</div>
            </Reveal>

            {/* 第 2 层 */}
            <Reveal kind="rise" duration={780} delay={420} className="ok__rule ok__rule--ok">
              <div className="ok__rule-num">02</div>
              <div className="ok__rule-body">
                <div className="ok__rule-title">不够用？<em>oklch 派生</em></div>
                <div className="ok__rule-desc">L / C 不变，h 旋转 —— 自动得到和谐衍生色</div>
                <div className="ok__rule-swatches">
                  {[42, 90, 150, 200, 260, 320].map((h) => (
                    <span key={h} style={{ background: `oklch(0.70 0.15 ${h})` }} />
                  ))}
                </div>
              </div>
              <div className="ok__rule-mark ok__rule-mark--good">✓</div>
            </Reveal>

            {/* 第 3 层 */}
            <Reveal kind="rise" duration={780} delay={620} className="ok__rule ok__rule--bad">
              <div className="ok__rule-num">03</div>
              <div className="ok__rule-body">
                <div className="ok__rule-title">禁止凭空造色</div>
                <div className="ok__rule-desc">"我觉得这个紫色挺好看" —— 这就是 AI 味的源头</div>
                <div className="ok__rule-swatches">
                  <span style={{ background: '#a78bfa' }} />
                  <span style={{ background: '#f0abfc' }} />
                  <span style={{ background: '#67e8f9' }} />
                  <span style={{ background: '#fda4af' }} />
                </div>
              </div>
              <div className="ok__rule-mark ok__rule-mark--bad">×</div>
            </Reveal>
          </div>
        </div>
      </SceneFade>

      {/* ════════ Scene PIVOT（step 2）—— 大字提问 ════════ */}
      <SceneFade active={scenePivot} exitMs={420} enterDelayMs={420}>
        <div className="ok__pivot">
          <Reveal kind="rise" duration={1100} delay={120} className="ok__pivot-q" as="h1">
            为什么是 <em className="ok__pivot-em">oklch</em> ？
          </Reveal>

          <Reveal kind="rise" duration={780} delay={780} className="ok__pivot-sub" as="p">
            <span className="ok__pivot-strike">HSL</span>
            &nbsp;有个大问题 ——
          </Reveal>

          <Reveal kind="tight" duration={1100} delay={1200} className="ok__pivot-issue" as="h2">
            感知<em>不均匀</em>
          </Reveal>
        </div>
      </SceneFade>

      {/* ════════ Scene COMPARE（step 3）—— 双色相条 + 曲线 ════════ */}
      <SceneFade active={sceneCompare} exitMs={420} enterDelayMs={420}>
        <div className="ok__cmp-scene">
          <Reveal kind="fade" duration={620} delay={80} className="ok__cmp-cap">
            同一组亮度 / 饱和度 · 12 个色相 —— 看人眼对哪种更<em>舒服</em>
          </Reveal>

          <div className="ok__cmp-grid">
            {/* HSL 行 */}
            <div className="ok__cmp-row">
              <div className="ok__cmp-row-head">
                <span className="ok__cmp-row-tag ok__cmp-row-tag--bad">HSL · 老</span>
                <span className="ok__cmp-row-formula">hsl(h, 70%, 60%)</span>
              </div>
              <div className="ok__cmp-strip">
                {HUES.map((h, i) => (
                  <div
                    key={`hsl-${h}`}
                    className={`ok__cmp-swatch ${h === 60 ? 'is-spot' : ''}`}
                    style={{
                      background: `hsl(${h} 70% 60%)`,
                      animationDelay: `${i * 60}ms`,
                    }}
                  >
                    <span className="ok__cmp-swatch-tick">{h}°</span>
                  </div>
                ))}
              </div>
              <svg
                className="ok__cmp-curve ok__cmp-curve--bad"
                viewBox="0 0 1200 80"
                preserveAspectRatio="none"
              >
                <path
                  d={
                    'M0 80 ' +
                    HUES.map((h, i) => {
                      const x = (i / (HUES.length - 1)) * 1200;
                      const y = 78 - hslPerceived(h) * 70;
                      return `L${x.toFixed(1)} ${y.toFixed(1)}`;
                    }).join(' ') +
                    ' L1200 80 Z'
                  }
                  fill="var(--crimson)"
                  fillOpacity="0.12"
                  stroke="var(--crimson)"
                  strokeWidth="2"
                />
              </svg>
              <div className="ok__cmp-callout ok__cmp-callout--bad">
                <span className="ok__cmp-callout-arrow">↑</span>
                <span>同 60% 亮度 —— 黄色看着像被打了灯</span>
              </div>
            </div>

            {/* OKLCH 行 */}
            <div className="ok__cmp-row">
              <div className="ok__cmp-row-head">
                <span className="ok__cmp-row-tag ok__cmp-row-tag--good">OKLCH · 新</span>
                <span className="ok__cmp-row-formula">oklch(0.70 0.15 h)</span>
              </div>
              <div className="ok__cmp-strip">
                {HUES.map((h, i) => (
                  <div
                    key={`ok-${h}`}
                    className="ok__cmp-swatch"
                    style={{
                      background: `oklch(0.70 0.15 ${h})`,
                      animationDelay: `${i * 60 + 220}ms`,
                    }}
                  >
                    <span className="ok__cmp-swatch-tick">{h}°</span>
                  </div>
                ))}
              </div>
              <svg
                className="ok__cmp-curve ok__cmp-curve--good"
                viewBox="0 0 1200 80"
                preserveAspectRatio="none"
              >
                <path
                  d={'M0 80 L0 30 L1200 30 L1200 80 Z'}
                  fill="var(--accent)"
                  fillOpacity="0.10"
                  stroke="var(--accent)"
                  strokeWidth="2"
                />
              </svg>
              <div className="ok__cmp-callout ok__cmp-callout--good">
                <span className="ok__cmp-callout-arrow">→</span>
                <span>L / C 不变，只转 h —— 亮度自动一致</span>
              </div>
            </div>
          </div>
        </div>
      </SceneFade>

      {/* ════════ Scene CLOSE（step 4）════════ */}
      <SceneFade active={sceneClose} exitMs={420} enterDelayMs={420}>
        <div className="ok__close">
          <Reveal kind="fade" duration={780} delay={120} className="ok__close-eyebrow">
            细节看着小 ——
          </Reveal>

          <Reveal kind="rise" duration={1300} delay={460} className="ok__close-line" as="h1">
            网页端<em>高级感</em>
          </Reveal>

          <Reveal kind="rise" duration={1100} delay={1080} className="ok__close-arrow" as="span">
            ↑
          </Reveal>

          <Reveal kind="fade" duration={780} delay={1500} className="ok__close-caption" as="p">
            一下就上来了
          </Reveal>
        </div>
      </SceneFade>
    </section>
  );
}

const def: ChapterDef = {
  id: 'oklch',
  title: '第四部分 · oklch 配色',
  eyebrow: '07',
  steps: 5,
  theme: 'light',
  Component: Oklch,
};

export default def;
