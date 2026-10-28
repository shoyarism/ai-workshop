import type { ChapterContext, ChapterDef } from '../types';
import { Reveal } from '../../shared/Reveal';
import { SceneFade } from '../../shared/SceneFade';
import { NumberTicker } from '../../shared/NumberTicker';
import './CorePoint.css';

/**
 * Chapter 03 · 核心观点
 *
 * 口播主旨：
 *  「Claude Design 之所以强，一半靠 Opus 4.7，另一半靠精心设计的提示词。
 *   上线不到 24 小时，完整系统提示词被扒出来。下面，我们逐条拆解。」
 *
 * 节奏（6 步 / step 0..5）：
 *  0  环境（深墨底 + 网格氛围，一行小标 eyebrow）
 *  1  hero 问句："Claude Design · 为什么这么强？"
 *  2  答案展开：50/50 分屏，左 OPUS 4.7 / 右 SYSTEM PROMPT
 *  3  右侧"提示词从天而降"——真实片段逐条落入文档预览
 *  4  leaked 事件徽章："< 24 HOURS · LEAKED"
 *  5  转场指引："下面，我们逐条拆解 ↓"
 */

const PROMPT_LINES: string[] = [
  'You are an expert designer working with the user as a manager.',
  'You produce design artifacts on behalf of the user using HTML.',
  'HTML is your tool, but your medium and output format vary.',
  'You must embody an expert in that domain:',
  '  animator, UX designer, slide designer, prototyper, etc.',
  'Avoid web design tropes and conventions',
  '  unless you are making a web page.',
  '## Your workflow',
  '1. Understand user needs. Ask clarifying questions ...',
  '2. Explore provided resources. Read the design system ...',
];

function CorePoint({ localStep }: ChapterContext) {
  const at = (n: number) => localStep >= n;

  // 场景：1+ 进入分析；2 之前是单独 hero 居中
  const sceneHero = localStep <= 1;
  const sceneSplit = localStep >= 2;

  return (
    <section className="cp">
      {/* 装饰性背景网格 + 角落坐标 */}
      <div className="cp__grid" aria-hidden />
      <div className="cp__cornerTL" aria-hidden>
        <span /><span />
      </div>
      <div className="cp__cornerBR" aria-hidden>
        <span /><span />
      </div>

      {/* ───────── Scene HERO（step 0..1）───────── */}
      <SceneFade active={sceneHero} exitMs={420} enterDelayMs={120}>
        <div className="cp__hero">
          <Reveal kind="fade" duration={700} delay={120} className="cp__hero-eyebrow">
            <span className="cp__hero-eyebrow-bar" />
            <span>03 · 核心观点</span>
            <span className="cp__hero-eyebrow-bar" />
          </Reveal>

          {at(1) && (
            <Reveal kind="rise" duration={1100} delay={80} className="cp__hero-title" as="h1">
              Claude Design<br />
              <em className="cp__hero-em">为什么这么强？</em>
            </Reveal>
          )}
        </div>
      </SceneFade>

      {/* ───────── Scene SPLIT（step 2..5）───────── */}
      <SceneFade active={sceneSplit} exitMs={420} enterDelayMs={420}>
        <div className="cp__split">
          {/* 顶部留下问句的小回响（不再是大字） */}
          <Reveal kind="fade" duration={620} delay={120} className="cp__split-eyebrow">
            <span>为什么这么强？</span>
            <span className="cp__split-eyebrow-arrow">→</span>
            <span>答案是</span>
          </Reveal>

          {/* 中央分隔线 */}
          <Reveal kind="fade" duration={900} delay={300} className="cp__split-divider">
            <span className="cp__split-divider-line" />
            <span className="cp__split-divider-knob">+</span>
            <span className="cp__split-divider-line" />
          </Reveal>

          <div className="cp__columns">
            {/* —— 左：OPUS 4.7 —— */}
            <Reveal kind="rise" duration={900} delay={420} className="cp__col cp__col--left">
              <div className="cp__col-pct">
                <NumberTicker to={50} duration={1100} decimals={0} />
                <span className="cp__col-pct-sign">%</span>
              </div>
              <div className="cp__col-kicker">MODEL</div>
              <h2 className="cp__col-title">Opus 4.7</h2>
              <p className="cp__col-desc">
                Anthropic 当前旗舰模型 ——<br />
                决策力、品味、长链推理与代码能力的综合上限
              </p>

              <div className="cp__col-meter">
                <div className="cp__col-meter-bar" style={{ width: at(2) ? '50%' : '0%' }} />
                <div className="cp__col-meter-ticks">
                  <span /><span /><span /><span /><span />
                </div>
              </div>

              <div className="cp__col-tags">
                <span>reasoning</span>
                <span>taste</span>
                <span>code</span>
              </div>
            </Reveal>

            {/* —— 右：SYSTEM PROMPT —— */}
            <Reveal kind="rise" duration={900} delay={560} className="cp__col cp__col--right">
              <div className="cp__col-pct">
                <NumberTicker to={50} duration={1100} delay={140} decimals={0} />
                <span className="cp__col-pct-sign">%</span>
              </div>
              <div className="cp__col-kicker">SYSTEM PROMPT</div>
              <h2 className="cp__col-title">提示词工程</h2>
              <p className="cp__col-desc">
                ~420 行专家级 system prompt ——<br />
                对模型的"角色 / 流程 / 边界 / 品味"做了极强约束
              </p>

              {/* 文档预览 */}
              <div className="cp__doc">
                <div className="cp__doc-bar">
                  <span className="cp__doc-bar-dot" />
                  <span className="cp__doc-bar-dot" />
                  <span className="cp__doc-bar-dot" />
                  <span className="cp__doc-bar-name">claude-design.system.md</span>
                </div>
                <div className="cp__doc-body">
                  {at(3) && PROMPT_LINES.map((line, i) => (
                    <Reveal
                      key={`pl-${i}-${localStep}`}
                      kind="fall"
                      duration={520}
                      delay={i * 90}
                      className="cp__doc-line"
                    >
                      <span className="cp__doc-line-no">{String(i + 1).padStart(2, '0')}</span>
                      <span className="cp__doc-line-text">{line}</span>
                    </Reveal>
                  ))}
                  {at(3) && (
                    <Reveal kind="fade" duration={400} delay={PROMPT_LINES.length * 90 + 200}>
                      <span className="cp__doc-cursor">▍</span>
                    </Reveal>
                  )}
                </div>
              </div>
            </Reveal>
          </div>

          {/* leaked 徽章 */}
          {at(4) && (
            <Reveal kind="rise" duration={780} className="cp__leaked">
              <div className="cp__leaked-stamp">
                <span className="cp__leaked-stamp-dot" />
                LEAKED
              </div>
              <div className="cp__leaked-meta">
                <div className="cp__leaked-meta-time">
                  <span className="cp__leaked-meta-lt">&lt;</span>
                  <NumberTicker to={24} duration={900} decimals={0} />
                  <span className="cp__leaked-meta-unit">HOURS</span>
                </div>
                <div className="cp__leaked-meta-text">
                  上线不到 24 小时，完整系统提示词被扒出，<br />
                  在安全 / 提示词圈广为流传
                </div>
              </div>
            </Reveal>
          )}

          {/* 转场指引 */}
          {at(5) && (
            <Reveal kind="rise" duration={760} delay={120} className="cp__pivot">
              <span className="cp__pivot-arrow" />
              <span className="cp__pivot-text">下面，我们逐条拆解这套提示词</span>
            </Reveal>
          )}
        </div>
      </SceneFade>
    </section>
  );
}

const def: ChapterDef = {
  id: 'core-point',
  title: '核心观点',
  eyebrow: '03',
  steps: 6,
  theme: 'ink',
  Component: CorePoint,
};

export default def;
