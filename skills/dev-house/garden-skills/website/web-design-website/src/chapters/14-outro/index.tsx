import type { ChapterContext, ChapterDef } from '../types';
import { Reveal } from '../../shared/Reveal';
import { SceneFade } from '../../shared/SceneFade';
import './Outro.css';

/**
 * Chapter 14 · Outro · 项目预告 + 三连
 *
 * 口播原顺序（严格对齐 article/口播稿.md L284-295）：
 *   1. "Skill 的完整代码、原始参考的 Claude Design 的提示词、几个 DEMO 网站，
 *       我都已经打包到一起开源了。大家需要的可以到简介和评论区自取。"
 *   2. "最后推荐下我最近在做的 Easy Agent 开源项目。"
 *   3. "做这个项目的目的是 —— 学习 Claude Code 的 Harness 是如何做的，
 *       最终完整跟下来的同学都能具备从零开发企业级 Agent 的能力。"
 *   4. "如果本期教程对你有所帮助，希望得到一个免费的三连 ——"
 *   5. "我们下期见。"
 *
 * 节奏（5 步 / step 0..4）：
 *  0  开源资源卡 · "已打包开源" + 三个内容标签卡（Skill / Prompt / DEMOs）
 *  1  Easy Agent · 项目大字 hero + 副 "从零复刻 Claude Code · Harness"
 *  2  项目目标 · "完整跟下来 → 企业级 Agent 开发能力"
 *  3  三连 CTA · 自绘几何 like / star / follow（无 emoji）
 *  4  下期见 · 大字告别
 */

interface Resource {
  id: string;
  num: string;
  name: string;
  cn: string;
  desc: string;
}

const RESOURCES: Resource[] = [
  { id: 'skill',  num: '01', name: 'web-design-engineer',         cn: 'Skill 完整代码',  desc: '本期主角 · SKILL.md + references' },
  { id: 'prompt', num: '02', name: 'claude-design / system.md',   cn: '原始参考 Prompt', desc: 'Claude Design 系统提示词原文 · ≈ 420 行' },
  { id: 'demo',   num: '03', name: 'demos /',                     cn: '几个 DEMO 网站',  desc: '本期演示用到的所有产物站点' },
];

/* ──────────────────────────────────────────────────────────────────
 * 自绘几何三连图标（line-art · 不用 emoji）
 *   - like:   拇指（圆角矩形 + 半圆）
 *   - star:   五角星
 *   - follow: 圆 + 内嵌 +
 * ────────────────────────────────────────────────────────────────── */

function IconLike() {
  return (
    <svg className="ot__icon" viewBox="0 0 64 64" aria-hidden>
      <path
        d="M22 28 L22 56 L46 56 C50 56 52 53 52 50 L54 36 C54.5 33 52.5 31 50 31 L40 31 L42 22 C43 18 41 14 37 14 C35 14 34 15 33 17 L26 28 Z"
        fill="none"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinejoin="round"
        strokeLinecap="round"
      />
      <rect
        x="10" y="28" width="10" height="28"
        rx="1.5"
        fill="none"
        stroke="currentColor"
        strokeWidth="2.5"
      />
    </svg>
  );
}

function IconStar() {
  return (
    <svg className="ot__icon" viewBox="0 0 64 64" aria-hidden>
      <path
        d="M32 8 L40 24 L58 26.5 L45 39 L48 56 L32 47.5 L16 56 L19 39 L6 26.5 L24 24 Z"
        fill="none"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinejoin="round"
        strokeLinecap="round"
      />
    </svg>
  );
}

function IconFollow() {
  return (
    <svg className="ot__icon" viewBox="0 0 64 64" aria-hidden>
      <circle
        cx="32" cy="32" r="22"
        fill="none"
        stroke="currentColor"
        strokeWidth="2.5"
      />
      <path
        d="M32 21 L32 43 M21 32 L43 32"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
      />
    </svg>
  );
}

const TRIPLE = [
  { id: 'like',   icon: <IconLike   />, label: '点赞', mono: 'LIKE'    },
  { id: 'star',   icon: <IconStar   />, label: '收藏', mono: 'COLLECT' },
  { id: 'follow', icon: <IconFollow />, label: '关注', mono: 'FOLLOW'  },
];

function Outro({ localStep }: ChapterContext) {
  const sceneOpen     = localStep <= 0;
  const sceneEasy     = localStep === 1;
  const sceneGoal     = localStep === 2;
  const sceneTriple   = localStep === 3;
  const sceneBye      = localStep >= 4;

  return (
    <section className="ot">
      {/* ════════ Scene OPEN（step 0）—— 开源资源卡 ════════ */}
      <SceneFade active={sceneOpen} exitMs={420} enterDelayMs={120}>
        <div className="ot__open">
          <Reveal kind="fade" duration={620} delay={80} className="ot__open-eyebrow">
            最后 ——
          </Reveal>

          <Reveal kind="rise" duration={1100} delay={300} className="ot__open-title" as="h1">
            <em>已打包开源</em> · 简介 / 评论区 自取
          </Reveal>

          <div className="ot__open-grid">
            {RESOURCES.map((r, i) => (
              <div
                key={r.id}
                className="ot__open-card"
                style={{ animationDelay: `${700 + i * 160}ms` }}
              >
                <div className="ot__open-card-num">{r.num}</div>
                <div className="ot__open-card-name">{r.name}</div>
                <div className="ot__open-card-cn">{r.cn}</div>
                <div className="ot__open-card-desc">{r.desc}</div>
                <div className="ot__open-card-foot">
                  <span className="ot__open-card-foot-arrow">↗</span>
                  <span className="ot__open-card-foot-text">open</span>
                </div>
              </div>
            ))}
          </div>

          <Reveal kind="fade" duration={780} delay={1500} className="ot__open-foot">
            一键打包 —— 不用四处找
          </Reveal>
        </div>
      </SceneFade>

      {/* ════════ Scene EASY（step 1）—— Easy Agent 项目预告 ════════ */}
      <SceneFade active={sceneEasy} exitMs={420} enterDelayMs={420}>
        <div className="ot__easy">
          <Reveal kind="fade" duration={620} delay={80} className="ot__easy-eyebrow">
            <span className="ot__src-bracket">[</span>
            <span className="ot__src-label">还在做的 · 开源项目</span>
            <span className="ot__src-bracket">]</span>
          </Reveal>

          <Reveal kind="rise" duration={1100} delay={260} className="ot__easy-pre" as="p">
            最后推荐 ——
          </Reveal>

          <Reveal kind="rise" duration={1300} delay={620} className="ot__easy-name" as="h1">
            <em>Easy Agent</em>
          </Reveal>

          <Reveal kind="rise" duration={1100} delay={1300} className="ot__easy-sub" as="h2">
            从零复刻 Claude Code 的 <em>Harness</em>
          </Reveal>

          <Reveal kind="fade" duration={780} delay={1900} className="ot__easy-meta">
            <span>open source</span>
            <span className="ot__easy-meta-dot" />
            <span>step-by-step</span>
            <span className="ot__easy-meta-dot" />
            <span>企业级 Agent</span>
          </Reveal>
        </div>
      </SceneFade>

      {/* ════════ Scene GOAL（step 2）—— 项目目标 ════════ */}
      <SceneFade active={sceneGoal} exitMs={420} enterDelayMs={420}>
        <div className="ot__goal">
          <Reveal kind="fade" duration={620} delay={80} className="ot__goal-eyebrow">
            完整跟下来 ——
          </Reveal>

          <div className="ot__goal-flow">
            <Reveal kind="rise" duration={780} delay={260} className="ot__goal-step ot__goal-step--from">
              <div className="ot__goal-step-tag">YOU · 现在</div>
              <div className="ot__goal-step-line">想 转 AI Agent 开发</div>
            </Reveal>

            <Reveal kind="fade" duration={780} delay={620} className="ot__goal-arrow" as="span">
              <span className="ot__goal-arrow-line" />
              <span className="ot__goal-arrow-text">Easy Agent</span>
              <span className="ot__goal-arrow-head">→</span>
            </Reveal>

            <Reveal kind="rise" duration={780} delay={900} className="ot__goal-step ot__goal-step--to">
              <div className="ot__goal-step-tag ot__goal-step-tag--alt">YOU · 之后</div>
              <div className="ot__goal-step-line">具备<em>企业级</em> Agent 开发能力</div>
            </Reveal>
          </div>

          <Reveal kind="fade" duration={780} delay={1500} className="ot__goal-foot">
            "AI 转型 —— <em>不容错过</em>"
          </Reveal>
        </div>
      </SceneFade>

      {/* ════════ Scene TRIPLE（step 3）—— 自绘三连 ════════ */}
      <SceneFade active={sceneTriple} exitMs={420} enterDelayMs={420}>
        <div className="ot__triple">
          <Reveal kind="fade" duration={620} delay={80} className="ot__triple-eyebrow">
            如果本期对你有帮助 ——
          </Reveal>

          <Reveal kind="rise" duration={1100} delay={260} className="ot__triple-title" as="h1">
            希望得到一个 <em>免费的三连</em>
          </Reveal>

          <div className="ot__triple-row">
            {TRIPLE.map((t, i) => (
              <div
                key={t.id}
                className="ot__triple-card"
                style={{ animationDelay: `${600 + i * 200}ms` }}
              >
                <div className="ot__triple-icon-wrap">
                  {t.icon}
                </div>
                <div className="ot__triple-label">{t.label}</div>
                <div className="ot__triple-mono">{t.mono}</div>
              </div>
            ))}
          </div>

          <Reveal kind="fade" duration={780} delay={1700} className="ot__triple-foot">
            后续 —— 持续分享更多<em>有价值的 AI 教程</em>
          </Reveal>
        </div>
      </SceneFade>

      {/* ════════ Scene BYE（step 4）—— 下期见 ════════ */}
      <SceneFade active={sceneBye} exitMs={420} enterDelayMs={420}>
        <div className="ot__bye">
          <Reveal kind="fade" duration={780} delay={120} className="ot__bye-eyebrow">
            感谢观看 ——
          </Reveal>
          <Reveal kind="rise" duration={1300} delay={500} className="ot__bye-line" as="h1">
            我们 <em>下期见</em>
            <span className="ot__bye-arrow">↗</span>
          </Reveal>
          <Reveal kind="fade" duration={780} delay={1500} className="ot__bye-sig">
            <span className="ot__bye-sig-bar" />
            <span className="ot__bye-sig-text">claude-design / web-design-engineer</span>
            <span className="ot__bye-sig-bar" />
          </Reveal>
        </div>
      </SceneFade>
    </section>
  );
}

const def: ChapterDef = {
  id: 'outro',
  title: 'Outro · 项目预告 + 三连',
  eyebrow: '14',
  steps: 5,
  theme: 'light',
  Component: Outro,
};

export default def;
