import type { ChapterContext, ChapterDef } from '../types';
import { Reveal } from '../../shared/Reveal';
import { SceneFade } from '../../shared/SceneFade';
import './ToSkill.css';

/**
 * Chapter 10 · 过渡到 Skill
 *
 * 口播原顺序（严格对齐）：
 *   1. "以上就是 Claude Design 提示词里最核心的东西。"
 *   2. "但有个现实问题 — Anthropic 的产品在国内用起来都非常的难。"
 *      "我自己被封了三个号，彻底放弃官方渠道了。"
 *      "而且没有 API，没法接到自己的工作流里。"
 *   3. "不过好消息是：它的提示词已经泄出来了。
 *       Claude Design 厉害的另一半，主要就这套提示词里。"
 *   4. "所以我做了个 Skill，叫 web-design-engineer，
 *       把这套提示词的精华提炼了出来。"
 *   5. "Claude Code、Cursor、Codex 都能直接用，人人都能成为顶级网页设计师。"
 *
 * 节奏（6 步 / step 0..5）：
 *  0  回顾："以上 —— 提示词原文最核心的东西" + 五块小钩
 *  1  转折大字 "但..." + "Anthropic 在国内 —— 难"
 *  2  三张账号卡片依次倒下 + BANNED 红章 + "没 API"小注
 *  3  Pivot："好消息 —— 提示词 已经泄出来了"
 *  4  Skill 卡：web-design-engineer 终端式呈现 + 三个适用工具
 *  5  收尾大字 "人人都能成为 顶级网页设计师"
 */

const RECAP_POINTS = [
  '角色定位',
  '工作流',
  '去 AI 味',
  'oklch 配色',
  '内容克制',
  '验证闭环',
];

const TOOLS = [
  { id: 'cc', name: 'Claude Code', mono: 'claude.code' },
  { id: 'cu', name: 'Cursor',      mono: 'cursor.sh'   },
  { id: 'cx', name: 'Codex',       mono: 'codex.cli'   },
];

function ToSkill({ localStep }: ChapterContext) {
  const at = (n: number) => localStep >= n;
  void at;

  const sceneRecap   = localStep <= 0;
  const sceneProb    = localStep === 1;
  const sceneBanned  = localStep === 2;
  const scenePivot   = localStep === 3;
  const sceneSkill   = localStep === 4;
  const sceneClose   = localStep >= 5;

  return (
    <section className="ts">
      {/* ════════ Scene RECAP（step 0）════════ */}
      <SceneFade active={sceneRecap} exitMs={420} enterDelayMs={120}>
        <div className="ts__recap">
          <Reveal kind="rise" duration={1100} delay={120} className="ts__recap-title" as="h1">
            以上 —— 提示词里<br />
            <em>最核心</em>的东西
          </Reveal>

          <div className="ts__recap-list">
            {RECAP_POINTS.map((p, i) => (
              <div
                key={p}
                className="ts__recap-item"
                style={{ animationDelay: `${640 + i * 120}ms` }}
              >
                <span className="ts__recap-num">0{i + 1}</span>
                <span className="ts__recap-name">{p}</span>
                <span className="ts__recap-tick">✓</span>
              </div>
            ))}
          </div>
        </div>
      </SceneFade>

      {/* ════════ Scene PROBLEM（step 1）—— "但..." ════════ */}
      <SceneFade active={sceneProb} exitMs={420} enterDelayMs={420}>
        <div className="ts__prob">
          <Reveal kind="rise" duration={1100} delay={120} className="ts__prob-but" as="h1">
            但 ——
          </Reveal>

          <Reveal kind="rise" duration={1100} delay={680} className="ts__prob-line" as="h2">
            Anthropic 的产品 ——<br />
            在国内 <em>真的难用</em>
          </Reveal>

          <Reveal kind="fade" duration={780} delay={1500} className="ts__prob-meta">
            <span>无官方支付</span>
            <span className="ts__prob-meta-dot" />
            <span>无 API</span>
            <span className="ts__prob-meta-dot" />
            <span>账号易被封</span>
          </Reveal>
        </div>
      </SceneFade>

      {/* ════════ Scene BANNED（step 2）—— 三张账号倒下 ════════ */}
      <SceneFade active={sceneBanned} exitMs={420} enterDelayMs={420}>
        <div className="ts__banned-scene">
          <Reveal kind="fade" duration={620} delay={80} className="ts__banned-cap">
            "我自己被封了 <em>三个号</em>，彻底放弃官方渠道了。"
          </Reveal>

          <div className="ts__banned-row">
            {[1, 2, 3].map((n, i) => (
              <div
                key={n}
                className={`ts__card ts__card--n${n}`}
                style={{ animationDelay: `${i * 320 + 380}ms` }}
              >
                <div className="ts__card-bar">
                  <span className="ts__card-bar-dot" />
                  <span className="ts__card-bar-dot" />
                  <span className="ts__card-bar-dot" />
                  <span className="ts__card-bar-name">claude.ai / account</span>
                </div>
                <div className="ts__card-body">
                  <div className="ts__card-avatar">{['F', 'G', 'H'][i]}</div>
                  <div className="ts__card-info">
                    <div className="ts__card-name">花园老师 #{n}</div>
                    <div className="ts__card-mail">flower-{i + 1}@anthropic.user</div>
                    <div className="ts__card-plan">
                      <span className="ts__card-plan-tag">Pro</span>
                      <span>activated · 2026.0{i + 1}</span>
                    </div>
                  </div>
                </div>
                {/* BANNED 印章 */}
                <div className="ts__stamp" aria-hidden>
                  <span className="ts__stamp-text">BANNED</span>
                  <span className="ts__stamp-sub">violation · #{n}</span>
                </div>
              </div>
            ))}
          </div>

          <Reveal kind="fade" duration={780} delay={1700} className="ts__banned-foot">
            <span className="ts__banned-foot-x">×</span>
            而且 —— <em>没有 API</em>，接不进自己的工作流
          </Reveal>
        </div>
      </SceneFade>

      {/* ════════ Scene PIVOT（step 3）—— "好消息" ════════ */}
      <SceneFade active={scenePivot} exitMs={420} enterDelayMs={420}>
        <div className="ts__pivot">
          <Reveal kind="fade" duration={620} delay={120} className="ts__pivot-eyebrow">
            不过 ——
          </Reveal>

          <Reveal kind="rise" duration={1100} delay={320} className="ts__pivot-good" as="h1">
            <em>好消息</em>是：
          </Reveal>

          <Reveal kind="rise" duration={1100} delay={920} className="ts__pivot-line" as="h2">
            提示词 —— <em>已经泄出来了</em>
          </Reveal>

          <Reveal kind="fade" duration={780} delay={1700} className="ts__pivot-cap">
            "Claude Design 厉害的另一半，主要就<em>这套提示词</em>里。"
          </Reveal>
        </div>
      </SceneFade>

      {/* ════════ Scene SKILL（step 4）—— web-design-engineer ════════ */}
      <SceneFade active={sceneSkill} exitMs={420} enterDelayMs={420}>
        <div className="ts__skill-scene">
          <Reveal kind="fade" duration={620} delay={80} className="ts__skill-eyebrow">
            <span className="ts__src-bracket">[</span>
            <span className="ts__src-label">SKILL · OPEN SOURCE</span>
            <span className="ts__src-bracket">]</span>
          </Reveal>

          <Reveal kind="rise" duration={1100} delay={300} className="ts__skill-card">
            <div className="ts__skill-bar">
              <span className="ts__skill-bar-dot" />
              <span className="ts__skill-bar-dot" />
              <span className="ts__skill-bar-dot" />
              <span className="ts__skill-bar-path">.claude / skills / web-design-engineer / SKILL.md</span>
            </div>
            <div className="ts__skill-body">
              <div className="ts__skill-tag">SKILL.md</div>
              <h2 className="ts__skill-name">web-design-engineer</h2>
              <p className="ts__skill-desc">
                把 Claude Design 提示词的精华，<br />
                提炼成一个<em>可复用</em>的 Skill
              </p>
              <div className="ts__skill-meta">
                <span>≈ 400 行</span>
                <span className="ts__skill-meta-dot" />
                <span>开源</span>
                <span className="ts__skill-meta-dot" />
                <span>免费</span>
              </div>
            </div>
          </Reveal>

          <Reveal kind="fade" duration={620} delay={1100} className="ts__tools-cap">
            <span>适用于 ——</span>
          </Reveal>

          <div className="ts__tools-row">
            {TOOLS.map((t, i) => (
              <div
                key={t.id}
                className="ts__tool"
                style={{ animationDelay: `${1300 + i * 180}ms` }}
              >
                <div className="ts__tool-glyph">[ {t.id} ]</div>
                <div className="ts__tool-name">{t.name}</div>
                <div className="ts__tool-mono">{t.mono}</div>
              </div>
            ))}
          </div>
        </div>
      </SceneFade>

      {/* ════════ Scene CLOSE（step 5）════════ */}
      <SceneFade active={sceneClose} exitMs={420} enterDelayMs={420}>
        <div className="ts__close">
          <Reveal kind="rise" duration={1100} delay={120} className="ts__close-l1" as="h1">
            人人都能成为
          </Reveal>
          <Reveal kind="rise" duration={1300} delay={760} className="ts__close-l2" as="h1">
            <em>顶级网页设计师</em>
          </Reveal>
        </div>
      </SceneFade>
    </section>
  );
}

const def: ChapterDef = {
  id: 'to-skill',
  title: '过渡 · Skill 是怎么来的',
  eyebrow: '10',
  steps: 6,
  theme: 'light',
  Component: ToSkill,
};

export default def;
