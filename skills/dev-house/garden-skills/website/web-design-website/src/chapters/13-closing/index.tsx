import { useEffect, useRef, useState } from 'react';
import type { ChapterContext, ChapterDef } from '../types';
import { Reveal } from '../../shared/Reveal';
import { SceneFade } from '../../shared/SceneFade';
import './Closing.css';

/**
 * Chapter 13 · 收尾 · 85 → 95 分
 *
 * 口播原顺序（严格对齐 article/口播稿.md L274-281）：
 *   1. "没 Skill 的版本说实话本身已经不错了。
 *       Opus 4.7 裸跑出来的东西，比现在大多数程序员手写的都强。"
 *   2. "Skill 带来的提升，大概就是 85 分到 95 分的差距。"
 *   3. "从能用到好看，从完整到精致，从合格到有风格。"
 *   4. "这 10 的差距？就是 Skill 里那些看起来很琐碎的规则。"
 *   5. "每一条效果不大，但加在一起，就会产生质变了。"
 *
 * 节奏（5 步 / step 0..4）：
 *  0  公允声明 · "没 Skill 的版本 —— 本身已经不错"
 *  1  hero · 大字 85 → 95 数字 ticker（中央醒目动画）
 *  2  三组词对比 · 能用 → 好看 / 完整 → 精致 / 合格 → 有风格
 *  3  +10 分的差距 · 10+ 个"琐碎规则"chip 飞入聚拢
 *  4  量变 → 质变 · 大字收尾
 */

/* ──────────────────────────────────────────────────────────────────
 * NumberTicker: 数字从 from → to 平滑插值（视觉中央"跳分"）
 * 仅在挂载/active 切换时跑一次
 * ────────────────────────────────────────────────────────────────── */

interface TickerProps {
  from: number;
  to: number;
  duration?: number;
  delay?: number;
  /** 是否处于活动场景；切换时 reset */
  active: boolean;
}

function NumberTicker({ from, to, duration = 2200, delay = 0, active }: TickerProps) {
  const [val, setVal] = useState(from);
  const rafRef = useRef<number | null>(null);

  useEffect(() => {
    if (!active) {
      setVal(from);
      return;
    }
    let start = 0;
    const startTimer = window.setTimeout(() => {
      const step = (ts: number) => {
        if (!start) start = ts;
        const t = Math.min((ts - start) / duration, 1);
        // easeOutCubic
        const eased = 1 - Math.pow(1 - t, 3);
        setVal(from + (to - from) * eased);
        if (t < 1) {
          rafRef.current = requestAnimationFrame(step);
        }
      };
      rafRef.current = requestAnimationFrame(step);
    }, delay);
    return () => {
      window.clearTimeout(startTimer);
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, [from, to, duration, delay, active]);

  return <span>{Math.round(val)}</span>;
}

/* ──────────────────────────────────────────────────────────────────
 * 第 3 步用：10 条"琐碎规则" chip 列表
 * ────────────────────────────────────────────────────────────────── */

const SMALL_RULES = [
  { id: 'inter',    text: '不用 Inter / Roboto' },
  { id: 'oklch',    text: 'oklch 配色' },
  { id: 'system',   text: '先宣告设计系统' },
  { id: 'v0',       text: 'v0 半成品先出' },
  { id: 'restraint', text: '内容克制' },
  { id: 'placeholder', text: '占位符 > 假图' },
  { id: 'whitespace', text: '留白 = 设计' },
  { id: 'nograd',   text: '禁紫粉蓝渐变' },
  { id: 'noemoji',  text: '禁 emoji 当 icon' },
  { id: 'verify',   text: 'fork 子 Agent 验证' },
];

function Closing({ localStep }: ChapterContext) {
  const sceneFair    = localStep <= 0;
  const sceneJump    = localStep === 1;
  const sceneTrio    = localStep === 2;
  const sceneRules   = localStep === 3;
  const sceneClose   = localStep >= 4;

  return (
    <section className="cl">
      {/* ════════ Scene FAIR（step 0）—— 公允声明 ════════ */}
      <SceneFade active={sceneFair} exitMs={420} enterDelayMs={120}>
        <div className="cl__fair">
          <Reveal kind="fade" duration={620} delay={80} className="cl__fair-eyebrow">
            最后总结一下 ——
          </Reveal>

          <Reveal kind="rise" duration={1100} delay={300} className="cl__fair-line" as="h1">
            没 Skill 的版本 —— <em>本身已经不错</em>
          </Reveal>

          <Reveal kind="fade" duration={780} delay={1300} className="cl__fair-cap" as="p">
            Opus 4.7 裸跑出来的东西<br />
            <em>比现在大多数程序员手写的都强</em>
          </Reveal>
        </div>
      </SceneFade>

      {/* ════════ Scene JUMP（step 1）—— 85 → 95 大字 ════════ */}
      <SceneFade active={sceneJump} exitMs={420} enterDelayMs={420}>
        <div className="cl__jump">
          <Reveal kind="fade" duration={620} delay={80} className="cl__jump-eyebrow">
            Skill 带来的提升 ——
          </Reveal>

          <div className="cl__jump-row">
            <Reveal kind="rise" duration={1100} delay={300} className="cl__jump-num cl__jump-num--from">
              <span className="cl__jump-num-figure">
                <NumberTicker from={70} to={85} duration={1100} delay={400} active={sceneJump} />
              </span>
              <span className="cl__jump-num-tag">无 Skill</span>
            </Reveal>

            <Reveal kind="fade" duration={780} delay={1500} className="cl__jump-arrow" as="span">
              →
            </Reveal>

            <Reveal kind="rise" duration={1100} delay={1700} className="cl__jump-num cl__jump-num--to">
              <span className="cl__jump-num-figure cl__jump-num-figure--big">
                <NumberTicker from={85} to={95} duration={1500} delay={1900} active={sceneJump} />
              </span>
              <span className="cl__jump-num-tag cl__jump-num-tag--alt">有 Skill</span>
            </Reveal>
          </div>

          <Reveal kind="fade" duration={780} delay={3100} className="cl__jump-meta">
            <span className="cl__jump-meta-plus">+ 10</span>
            <span className="cl__jump-meta-text">分</span>
            <span className="cl__jump-meta-dot" />
            <span className="cl__jump-meta-text">从合格到惊艳</span>
          </Reveal>
        </div>
      </SceneFade>

      {/* ════════ Scene TRIO（step 2）—— 三组词对比 ════════ */}
      <SceneFade active={sceneTrio} exitMs={420} enterDelayMs={420}>
        <div className="cl__trio">
          <Reveal kind="fade" duration={620} delay={80} className="cl__trio-eyebrow">
            这 10 分到底是什么 ——
          </Reveal>

          <div className="cl__trio-rows">
            {[
              { from: '能用', to: '好看', delay: 260 },
              { from: '完整', to: '精致', delay: 720 },
              { from: '合格', to: '有风格', delay: 1180 },
            ].map((r) => (
              <div
                key={r.from}
                className="cl__trio-row"
                style={{ ['--d' as string]: `${r.delay}ms` }}
              >
                <span className="cl__trio-from">{r.from}</span>
                <span className="cl__trio-arrow">→</span>
                <span className="cl__trio-to">{r.to}</span>
              </div>
            ))}
          </div>
        </div>
      </SceneFade>

      {/* ════════ Scene RULES（step 3）—— 10 条琐碎规则飞入 ════════ */}
      <SceneFade active={sceneRules} exitMs={420} enterDelayMs={420}>
        <div className="cl__rules">
          <Reveal kind="fade" duration={620} delay={80} className="cl__rules-eyebrow">
            这 10 分 ——<em>来自</em>
          </Reveal>

          <Reveal kind="rise" duration={1100} delay={260} className="cl__rules-title" as="h2">
            一条条<em>看似琐碎</em>的规则
          </Reveal>

          <div className="cl__rules-cloud">
            {SMALL_RULES.map((r, i) => (
              <span
                key={r.id}
                className={`cl__rules-chip cl__rules-chip--${i % 4}`}
                style={{
                  animationDelay: `${500 + i * 110}ms`,
                  ['--rot' as string]: `${(i % 5 - 2) * 1.6}deg`,
                  ['--shift' as string]: `${(i % 3 - 1) * 18}px`,
                }}
              >
                <span className="cl__rules-chip-mark">+</span>
                {r.text}
              </span>
            ))}
          </div>

          <Reveal kind="fade" duration={780} delay={2100} className="cl__rules-foot">
            每一条 —— 单看效果不大
          </Reveal>
        </div>
      </SceneFade>

      {/* ════════ Scene CLOSE（step 4）—— 量变 → 质变 ════════ */}
      <SceneFade active={sceneClose} exitMs={420} enterDelayMs={420}>
        <div className="cl__close">
          <Reveal kind="rise" duration={1100} delay={120} className="cl__close-l1" as="h1">
            但加在一起 ——
          </Reveal>
          <Reveal kind="rise" duration={1300} delay={780} className="cl__close-l2" as="h1">
            <em>量变</em> → <em>质变</em>
          </Reveal>
          <Reveal kind="fade" duration={780} delay={1700} className="cl__close-cap" as="p">
            从「<em>合格</em>」到「<em>有风格</em>」
          </Reveal>
        </div>
      </SceneFade>
    </section>
  );
}

const def: ChapterDef = {
  id: 'closing',
  title: '收尾 · 85 → 95 分',
  eyebrow: '13',
  steps: 5,
  theme: 'light',
  Component: Closing,
};

export default def;
