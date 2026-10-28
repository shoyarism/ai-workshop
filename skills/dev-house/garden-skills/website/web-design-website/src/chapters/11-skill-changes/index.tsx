import type { ReactNode } from 'react';
import type { ChapterContext, ChapterDef } from '../types';
import { Reveal } from '../../shared/Reveal';
import { SceneFade } from '../../shared/SceneFade';
import './SkillChanges.css';

/**
 * Chapter 11 · Skill 的关键改动（重做版）
 *
 * 口播原顺序（严格对齐 article/口播稿.md）：
 *   "这个 Skill 大概 400 行，首先我把 Claude Design 中特有工具和环境的描述剥离了出去，
 *    只保留了其中能通用的、最有价值的部分，然后在这个基础上我还优化了几个地方："
 *   ① 写代码之前必须先用自然语言把设计系统说清楚 — 配色、字体、间距，全列出来。
 *   ② 要求它尽早拿出一个带假设和占位符的最小版本（v0）。
 *   ③ 在 Claude Design 的基础上，补充了更多的去除 AI 味的条目。
 *   ④ 加了几套经过验证的配色 × 字体的配对参考表 —— 给 AI 一个靠谱的起点。
 *
 * 节奏（8 步 / step 0..7）：
 *  0  Skill 全貌 —— 文件目录树（SKILL.md ≈ 400 行 / references ≈ 520 行）
 *  1  SKILL.md 真原文滚动展示（虚假的编辑器持续 scroll）
 *  2  第一刀：剥离 —— 工具/环境 vs 通用精华
 *  3  + 改动 01 · 先宣告设计系统  + SKILL.md L79-91 原文摘录（关键高亮 / 上下文虚化）
 *  4  + 改动 02 · v0 半成品先出  + SKILL.md L93-101 原文摘录
 *  5  + 改动 03 · 反 AI 味扩展  + SKILL.md L200-219 原文摘录
 *  6  + 改动 04 · 配色 × 字体配对  + advanced-patterns.md L505-516 原文摘录
 *  7  收尾："给 AI 一个靠谱的起点 —— 比让它自由发挥稳定"
 */

/* ──────────────────────────────────────────────────────────────────
 * 复用：原文摘录代码面板（关键行高亮、上下文虚化模糊）
 * ────────────────────────────────────────────────────────────────── */

interface CodeLine {
  /** 真实行号（用于左侧 gutter） */
  n: number;
  /** 行内容 */
  text: ReactNode;
  /** 是否高亮（不模糊、不弱化） */
  hi?: boolean;
  /** 行视觉缩进（每级 16px） */
  indent?: number;
}

interface ExcerptProps {
  filePath: string;
  range: string;
  caption?: ReactNode;
  lines: CodeLine[];
  /** delay before highlight pulse */
  pulseDelay?: number;
}

function Excerpt({ filePath, range, caption, lines, pulseDelay = 600 }: ExcerptProps) {
  return (
    <div className="sk__ex">
      <div className="sk__ex-bar">
        <span className="sk__ex-bar-dot" />
        <span className="sk__ex-bar-dot" />
        <span className="sk__ex-bar-dot" />
        <span className="sk__ex-bar-path">{filePath}</span>
        <span className="sk__ex-bar-range">{range}</span>
      </div>
      <div className="sk__ex-body">
        {lines.map((l, i) => (
          <div
            key={`${l.n}-${i}`}
            className={`sk__ex-line ${l.hi ? 'is-hi' : ''}`}
            style={{
              ['--ex-indent' as string]: `${(l.indent ?? 0) * 16}px`,
              animationDelay: l.hi ? `${pulseDelay + i * 40}ms` : undefined,
            }}
          >
            <span className="sk__ex-num">{l.n}</span>
            <span className="sk__ex-text">{l.text}</span>
          </div>
        ))}
      </div>
      {caption && <div className="sk__ex-caption">{caption}</div>}
    </div>
  );
}

/* ──────────────────────────────────────────────────────────────────
 * SKILL.md 假滚动用的内容片段（接近真实，用于动态滚动展示）
 * ────────────────────────────────────────────────────────────────── */

const SCROLL_LINES: { t: ReactNode; hi?: boolean; mute?: boolean }[] = [
  { t: '---', mute: true },
  { t: 'name: web-design-engineer', hi: true },
  { t: 'description: |' },
  { t: '  Build high-quality visual Web artifacts using HTML / CSS / JS / React —' },
  { t: '  web pages, dashboards, prototypes, slide decks, animated demos, …' },
  { t: '  Use this skill whenever the request involves a visual deliverable.' },
  { t: '---', mute: true },
  { t: '' },
  { t: '# Web Design Engineer', hi: true },
  { t: '' },
  { t: 'Core philosophy: the bar is "stunning," not "functional".' },
  { t: 'Every pixel is intentional. Every interaction is deliberate.' },
  { t: '' },
  { t: '## Workflow', hi: true },
  { t: '' },
  { t: '### Step 1 · Understand the Requirements' },
  { t: '### Step 2 · Gather Design Context' },
  { t: '### Step 3 · Declare the Design System Before Writing Code', hi: true },
  { t: '### Step 4 · Show a v0 Draft Early', hi: true },
  { t: '### Step 5 · Full Build' },
  { t: '### Step 6 · Verification' },
  { t: '' },
  { t: '## Technical Specifications' },
  { t: '' },
  { t: '#### Three Non-negotiable Hard Rules', hi: true },
  { t: '1. Never use `const styles = {...}`' },
  { t: '2. Separate <script type="text/babel"> blocks do not share scope' },
  { t: '3. Do not use `scrollIntoView`' },
  { t: '' },
  { t: '## Design Principles' },
  { t: '' },
  { t: '### Avoid AI-Style Clichés', hi: true },
  { t: '- Overuse of gradient backgrounds' },
  { t: '- Cookie-cutter gradient buttons + large-radius cards' },
  { t: '- Overreliance on Inter / Roboto / Arial / Fraunces' },
  { t: '- Meaningless stats / numbers / icon spam' },
  { t: '- Fabricated customer logo walls' },
  { t: '' },
  { t: '### Emoji Rules' },
  { t: '**No emoji by default.** Only when the brand itself uses them.' },
  { t: '' },
  { t: '### Placeholder Philosophy' },
  { t: 'A placeholder signals "real material needed here."' },
  { t: 'A fake signals "I cut corners."', hi: true },
  { t: '' },
  { t: '### Content Principles' },
  { t: '- No filler content — every element must earn its place', hi: true },
  { t: '- Less is more — "1,000 no\'s for every yes"' },
  { t: '- Whitespace is design' },
  { t: '' },
  { t: '## Pre-delivery Checklist', hi: true },
  { t: '- [ ] Browser console shows no errors, no warnings' },
  { t: '- [ ] All colors come from the declared design system' },
  { t: '- [ ] No `scrollIntoView`' },
  { t: '- [ ] No AI clichés (purple-pink gradients, Inter/Roboto, …)' },
  { t: '- [ ] No filler content, no fabricated data' },
  { t: '- [ ] Visual quality at Dribbble / Behance showcase level', hi: true },
  { t: '' },
  { t: '## Further Reference', hi: true },
  { t: '- references/advanced-patterns.md → full code template library' },
  { t: '' },
];

function SkillChanges({ localStep }: ChapterContext) {
  const sceneTree   = localStep <= 0;
  const sceneScroll = localStep === 1;
  const sceneStrip  = localStep === 2;
  const sceneA      = localStep === 3;
  const sceneB      = localStep === 4;
  const sceneC      = localStep === 5;
  const sceneD      = localStep === 6;
  const sceneClose  = localStep >= 7;

  return (
    <section className="sk">
      {/* ════════ Scene TREE（step 0）—— 文件目录全貌 ════════ */}
      <SceneFade active={sceneTree} exitMs={420} enterDelayMs={120}>
        <div className="sk__tree-scene">
          <Reveal kind="fade" duration={620} delay={80} className="sk__tree-eyebrow">
            <span className="sk__src-bracket">[</span>
            <span className="sk__src-label">SKILL · OPEN SOURCE</span>
            <span className="sk__src-bracket">]</span>
          </Reveal>

          <Reveal kind="rise" duration={1100} delay={260} className="sk__tree-title" as="h1">
            Skill 全貌 ——
          </Reveal>

          <Reveal kind="rise" duration={780} delay={620} className="sk__tree-card">
            <div className="sk__tree-bar">
              <span className="sk__tree-bar-dot" />
              <span className="sk__tree-bar-dot" />
              <span className="sk__tree-bar-dot" />
              <span className="sk__tree-bar-path">~ / .claude / skills / web-design-engineer</span>
            </div>
            <div className="sk__tree-body">
              <div className="sk__tree-row sk__tree-row--dir" style={{ animationDelay: '900ms' }}>
                <span className="sk__tree-glyph">▾</span>
                <span className="sk__tree-name">web-design-engineer<span className="sk__tree-slash">/</span></span>
                <span className="sk__tree-meta">root</span>
              </div>
              <div className="sk__tree-row sk__tree-row--file sk__tree-row--main" style={{ animationDelay: '1080ms' }}>
                <span className="sk__tree-pipe">├──</span>
                <span className="sk__tree-name sk__tree-name--md">SKILL.md</span>
                <span className="sk__tree-tag">主文件</span>
                <span className="sk__tree-meta sk__tree-meta--em">≈ 400 行</span>
              </div>
              <div className="sk__tree-row sk__tree-row--dir sk__tree-row--sub" style={{ animationDelay: '1260ms' }}>
                <span className="sk__tree-pipe">└──</span>
                <span className="sk__tree-glyph">▾</span>
                <span className="sk__tree-name">references<span className="sk__tree-slash">/</span></span>
                <span className="sk__tree-tag">高级模板</span>
              </div>
              <div className="sk__tree-row sk__tree-row--file sk__tree-row--child" style={{ animationDelay: '1440ms' }}>
                <span className="sk__tree-pipe sk__tree-pipe--child">└──</span>
                <span className="sk__tree-name sk__tree-name--md">advanced-patterns.md</span>
                <span className="sk__tree-tag">起点脚手架</span>
                <span className="sk__tree-meta sk__tree-meta--em">≈ 520 行</span>
              </div>
            </div>
          </Reveal>

          <Reveal kind="fade" duration={780} delay={1700} className="sk__tree-foot">
            两个文件，加起来 <em>≈ 920 行</em> —— 给 AI 全套<em>设计师手册</em>
          </Reveal>
        </div>
      </SceneFade>

      {/* ════════ Scene SCROLL（step 1）—— SKILL.md 假滚动 ════════ */}
      <SceneFade active={sceneScroll} exitMs={420} enterDelayMs={420}>
        <div className="sk__scroll-scene">
          <Reveal kind="fade" duration={620} delay={80} className="sk__scroll-eyebrow">
            <span className="sk__src-bracket">[</span>
            <span className="sk__src-label">FILE · SKILL.md</span>
            <span className="sk__src-sep">·</span>
            <span className="sk__src-line">≈ 400 行</span>
            <span className="sk__src-bracket">]</span>
          </Reveal>

          <Reveal kind="fade" duration={620} delay={260} className="sk__scroll-cap">
            原文 ——「核心理念 / 工作流 / 反 AI 味 / 校验清单」<em>全在里面</em>
          </Reveal>

          <Reveal kind="rise" duration={780} delay={460} className="sk__scroll-card">
            <div className="sk__scroll-bar">
              <span className="sk__scroll-bar-dot" />
              <span className="sk__scroll-bar-dot" />
              <span className="sk__scroll-bar-dot" />
              <span className="sk__scroll-bar-path">SKILL.md</span>
              <span className="sk__scroll-bar-meta">utf-8 · markdown · readonly</span>
            </div>
            <div className="sk__scroll-frame">
              <div className="sk__scroll-stream">
                {/* 重复两遍以做无缝循环 */}
                {[0, 1].map((loop) => (
                  <div key={loop} className="sk__scroll-block">
                    {SCROLL_LINES.map((l, i) => (
                      <div
                        key={`${loop}-${i}`}
                        className={`sk__scroll-line ${l.hi ? 'is-hi' : ''} ${l.mute ? 'is-mute' : ''}`}
                      >
                        <span className="sk__scroll-num">{String(i + 1).padStart(3, '0')}</span>
                        <span className="sk__scroll-text">{l.t || '\u00A0'}</span>
                      </div>
                    ))}
                  </div>
                ))}
              </div>
              {/* 顶/底渐隐遮罩、扫描线由 CSS 提供 */}
              <div className="sk__scroll-cursor" aria-hidden />
            </div>
          </Reveal>

          <Reveal kind="fade" duration={780} delay={1100} className="sk__scroll-foot">
            <span>下面把 ——</span>
            <em>第一刀 · 4 个改动</em>
            <span>—— 一一拆开看</span>
          </Reveal>
        </div>
      </SceneFade>

      {/* ════════ Scene STRIP（step 2）—— 第一刀：剥离 ════════ */}
      <SceneFade active={sceneStrip} exitMs={420} enterDelayMs={420}>
        <div className="sk__strip-scene">
          <Reveal kind="fade" duration={620} delay={80} className="sk__chg-num">
            第一刀
          </Reveal>
          <Reveal kind="rise" duration={1100} delay={240} className="sk__chg-title" as="h2">
            <em>剥离</em> —— Claude Design 特有的工具 / 环境
          </Reveal>

          <div className="sk__strip">
            {/* 左：留下 */}
            <Reveal kind="rise" duration={780} delay={500} className="sk__strip-col sk__strip-col--keep">
              <div className="sk__strip-head">
                <span className="sk__strip-mark sk__strip-mark--keep">✓</span>
                <span>KEEP · 通用精华</span>
              </div>
              <ul className="sk__strip-list">
                {[
                  '动态角色 · 设计师身份切换',
                  '六步工作流',
                  '反 AI 味清单',
                  'oklch 配色',
                  '内容克制原则',
                  '验证闭环',
                ].map((t, i) => (
                  <li
                    key={t}
                    className="sk__strip-row sk__strip-row--keep"
                    style={{ animationDelay: `${700 + i * 80}ms` }}
                  >
                    <span className="sk__strip-row-glyph">+</span>
                    {t}
                  </li>
                ))}
              </ul>
            </Reveal>

            {/* 中间 X */}
            <div className="sk__strip-sep" aria-hidden>
              <span className="sk__strip-sep-line" />
              <span className="sk__strip-sep-knob">×</span>
              <span className="sk__strip-sep-line" />
            </div>

            {/* 右：摘掉 */}
            <Reveal kind="rise" duration={780} delay={680} className="sk__strip-col sk__strip-col--drop">
              <div className="sk__strip-head">
                <span className="sk__strip-mark sk__strip-mark--drop">×</span>
                <span>DROP · 特有工具 / 环境</span>
              </div>
              <ul className="sk__strip-list">
                {[
                  'show_html()',
                  'show_to_user()',
                  'fork_verifier_agent()',
                  'iframe sandbox',
                  'tweaks panel · runtime',
                  'pptx export',
                  'GitHub 集成',
                  'snip 工具',
                ].map((t, i) => (
                  <li
                    key={t}
                    className="sk__strip-row sk__strip-row--drop"
                    style={{ animationDelay: `${900 + i * 70}ms` }}
                  >
                    <span className="sk__strip-row-glyph">−</span>
                    <code>{t}</code>
                  </li>
                ))}
              </ul>
            </Reveal>
          </div>
        </div>
      </SceneFade>

      {/* ════════ Scene CHANGE 01（step 3）—— 先宣告设计系统 ════════ */}
      <SceneFade active={sceneA} exitMs={420} enterDelayMs={420}>
        <div className="sk__chg-scene">
          <Reveal kind="fade" duration={620} delay={80} className="sk__chg-num">+ 改动 01</Reveal>
          <Reveal kind="rise" duration={1100} delay={240} className="sk__chg-title" as="h2">
            写代码之前 —— 先<em>宣告设计系统</em>
          </Reveal>

          <div className="sk__split">
            {/* 左：流程对比 */}
            <Reveal kind="rise" duration={720} delay={500} className="sk__split-left">
              <div className="sk__chg-flow">
                <div className="sk__chg-flow-col sk__chg-flow-col--bad">
                  <div className="sk__chg-flow-tag">
                    <span className="sk__chg-flow-mark sk__chg-flow-mark--bad">×</span>
                    之前
                  </div>
                  <div className="sk__chg-flow-step">需求</div>
                  <span className="sk__chg-flow-arrow">↓</span>
                  <div className="sk__chg-flow-step sk__chg-flow-step--code">直接 写代码</div>
                  <span className="sk__chg-flow-arrow">↓</span>
                  <div className="sk__chg-flow-step sk__chg-flow-step--out">完整页面</div>
                  <div className="sk__chg-flow-tip">方向不对 → <em>推翻重来</em></div>
                </div>

                <div className="sk__chg-flow-col sk__chg-flow-col--good">
                  <div className="sk__chg-flow-tag">
                    <span className="sk__chg-flow-mark sk__chg-flow-mark--good">✓</span>
                    改动后
                  </div>
                  <div className="sk__chg-flow-step">需求</div>
                  <span className="sk__chg-flow-arrow">↓</span>
                  <div className="sk__chg-flow-step sk__chg-flow-step--system">
                    <div className="sk__chg-system">
                      <div className="sk__chg-system-row"><span>palette</span><b>oklch · 暖棕</b></div>
                      <div className="sk__chg-system-row"><span>fonts</span><b>Newsreader + Sora</b></div>
                      <div className="sk__chg-system-row"><span>spacing</span><b>4 / 8 / 16 / 32</b></div>
                      <div className="sk__chg-system-row"><span>radius</span><b>0 / 2 / 4</b></div>
                    </div>
                  </div>
                  <span className="sk__chg-flow-arrow">↓</span>
                  <div className="sk__chg-flow-step sk__chg-flow-step--code">写代码</div>
                  <div className="sk__chg-flow-tip">方向不对 → <em>提前纠偏</em></div>
                </div>
              </div>
            </Reveal>

            {/* 右：原文 excerpt */}
            <Reveal kind="rise" duration={780} delay={760} className="sk__split-right">
              <Excerpt
                filePath="SKILL.md"
                range="L79 — L91"
                pulseDelay={1000}
                lines={[
                  { n: 77, text: '', },
                  { n: 78, text: '---' },
                  { n: 79, text: <><b>### Step 3:</b> Declare the Design System <em>Before</em> Writing Code</>, hi: true },
                  { n: 80, text: '' },
                  { n: 81, text: <><b>Before writing the first line of code</b>, articulate the design system in</>, hi: true },
                  { n: 82, text: 'Markdown and let the user confirm before proceeding:' , hi: true },
                  { n: 83, text: '' },
                  { n: 84, text: '```markdown' },
                  { n: 85, text: 'Design Decisions:' },
                  { n: 86, text: '- Color palette: [primary / secondary / neutral / accent]', hi: true, indent: 0 },
                  { n: 87, text: '- Typography: [heading font / body font / code font]', hi: true, indent: 0 },
                  { n: 88, text: '- Spacing system: [base unit and multiples]', hi: true, indent: 0 },
                  { n: 89, text: '- Border-radius strategy / Shadow / Motion …' },
                  { n: 90, text: '```' },
                  { n: 91, text: '' },
                  { n: 92, text: '### Step 4: Show a v0 Draft Early' },
                  { n: 93, text: '' },
                ]}
                caption={<>"在写第一行代码之前 —— 先<em>说清楚</em>"</>}
              />
            </Reveal>
          </div>
        </div>
      </SceneFade>

      {/* ════════ Scene CHANGE 02（step 4）—— v0 半成品 ════════ */}
      <SceneFade active={sceneB} exitMs={420} enterDelayMs={420}>
        <div className="sk__chg-scene">
          <Reveal kind="fade" duration={620} delay={80} className="sk__chg-num">+ 改动 02</Reveal>
          <Reveal kind="rise" duration={1100} delay={240} className="sk__chg-title" as="h2">
            尽早拿出 —— <em>v0 半成品</em>
          </Reveal>

          <div className="sk__split">
            <Reveal kind="rise" duration={720} delay={500} className="sk__split-left">
              <div className="sk__v">
                <div className="sk__v-card sk__v-card--v0">
                  <div className="sk__v-tag">
                    <span className="sk__v-mark sk__v-mark--good">✓</span>
                    v0 · 粗糙但<em>方向看得见</em>
                  </div>
                  <div className="sk__v-mock">
                    <span className="sk__v-mock-bar sk__v-mock-bar--w70" />
                    <span className="sk__v-mock-bar sk__v-mock-bar--w50" />
                    <div className="sk__v-mock-grid">
                      <span /><span /><span />
                    </div>
                    <span className="sk__v-mock-bar sk__v-mock-bar--w40" />
                  </div>
                  <div className="sk__v-foot">假设 + 占位符 → 用户能<em>立刻反馈</em></div>
                </div>

                <div className="sk__v-vs" aria-hidden>vs</div>

                <div className="sk__v-card sk__v-card--v1">
                  <div className="sk__v-tag">
                    <span className="sk__v-mark sk__v-mark--bad">×</span>
                    精雕细琢的 v1
                  </div>
                  <div className="sk__v-mock sk__v-mock--full">
                    <span className="sk__v-mock-h">Build the Future. Today.</span>
                    <span className="sk__v-mock-sub">Modern. Fast. Powerful.</span>
                    <div className="sk__v-mock-grid sk__v-mock-grid--full">
                      <span><b>★</b></span><span><b>↗</b></span><span><b>◷</b></span>
                    </div>
                    <span className="sk__v-mock-cta">Get Started →</span>
                  </div>
                  <div className="sk__v-foot">花 3 倍时间打磨 → 方向错了 <em>全推翻</em></div>
                  <div className="sk__v-strike" aria-hidden>
                    <span className="sk__v-strike-line" />
                  </div>
                </div>
              </div>
            </Reveal>

            <Reveal kind="rise" duration={780} delay={760} className="sk__split-right">
              <Excerpt
                filePath="SKILL.md"
                range="L93 — L101"
                pulseDelay={1000}
                lines={[
                  { n: 91, text: '' },
                  { n: 92, text: '---' },
                  { n: 93, text: <><b>### Step 4:</b> Show a <em>v0 Draft</em> Early</>, hi: true },
                  { n: 94, text: '' },
                  { n: 95, text: <><b>Don\'t hold back a big reveal.</b> Before writing full components, put</>, hi: true },
                  { n: 96, text: 'together a "viewable v0" using placeholders + key layout +', hi: true },
                  { n: 97, text: 'the declared design system:' },
                  { n: 98, text: '' },
                  { n: 99, text: '- The goal of v0: let the user course-correct early' },
                  { n: 100, text: '- Includes: core structure + tokens + key placeholders' },
                  { n: 101, text: '- Does NOT include: content details, complete components' },
                  { n: 102, text: '' },
                  { n: 103, text: <>A v0 with placeholders is more valuable than a "perfect v1"</>, hi: true },
                  { n: 104, text: <>that took <em>3x the time</em> — if direction is wrong, scrapped.</>, hi: true },
                  { n: 105, text: '' },
                ]}
                caption={<>"粗糙的 v0 → 用户能立刻看见<em>方向</em>"</>}
              />
            </Reveal>
          </div>
        </div>
      </SceneFade>

      {/* ════════ Scene CHANGE 03（step 5）—— 反 AI 味扩展 ════════ */}
      <SceneFade active={sceneC} exitMs={420} enterDelayMs={420}>
        <div className="sk__chg-scene">
          <Reveal kind="fade" duration={620} delay={80} className="sk__chg-num">+ 改动 03</Reveal>
          <Reveal kind="rise" duration={1100} delay={240} className="sk__chg-title" as="h2">
            <em>更狠</em>的去 AI 味 —— 扩展条目
          </Reveal>

          <div className="sk__split">
            <Reveal kind="rise" duration={720} delay={500} className="sk__split-left">
              <div className="sk__cd-col">
                <div className="sk__cd-tag">
                  <span className="sk__cd-mark">+ 新增</span>
                  常见 AI 味 · 一刀切
                </div>
                <ul className="sk__cd-anti">
                  {[
                    '紫粉蓝渐变背景',
                    '渐变按钮 + 大圆角卡片组合',
                    '凭空 logo 墙 / 假好评 / 假数据',
                    '无意义 stats / 数字 / 图标堆砌',
                    'emoji 当 icon 替身',
                    '老掉牙字体 Inter / Roboto / Arial',
                  ].map((t, i) => (
                    <li
                      key={t}
                      className="sk__cd-anti-row"
                      style={{ animationDelay: `${700 + i * 100}ms` }}
                    >
                      <span className="sk__cd-anti-x">×</span>
                      {t}
                    </li>
                  ))}
                </ul>
              </div>
            </Reveal>

            <Reveal kind="rise" duration={780} delay={760} className="sk__split-right">
              <Excerpt
                filePath="SKILL.md"
                range="L200 — L219"
                pulseDelay={1000}
                lines={[
                  { n: 198, text: '---' },
                  { n: 199, text: '' },
                  { n: 200, text: <><b>### Avoid AI-Style Clichés</b></>, hi: true },
                  { n: 201, text: '' },
                  { n: 202, text: 'Actively avoid these telltale "obviously AI" patterns:' },
                  { n: 203, text: '' },
                  { n: 204, text: '- Overuse of gradient backgrounds (purple-pink-blue)', hi: true },
                  { n: 205, text: '- Rounded cards with a colored left-border accent' },
                  { n: 206, text: '- Cookie-cutter gradient buttons + large-radius cards', hi: true },
                  { n: 207, text: '- Overreliance on Inter / Roboto / Arial / Fraunces', hi: true },
                  { n: 208, text: '- Meaningless stats / numbers / icon spam ("data slop")', hi: true },
                  { n: 209, text: '- Fabricated customer logo walls / fake testimonial counts', hi: true },
                  { n: 210, text: '' },
                  { n: 211, text: '### Emoji Rules' },
                  { n: 212, text: '' },
                  { n: 213, text: <><b>No emoji by default.</b> Only when the brand uses them.</>, hi: true },
                  { n: 214, text: '' },
                  { n: 215, text: '- × Using emoji as icon substitutes' },
                  { n: 216, text: '- × Using emoji as decorative filler' },
                ]}
                caption={<>把 Claude Design 没明说的"AI 味"<em>列具体了</em></>}
              />
            </Reveal>
          </div>
        </div>
      </SceneFade>

      {/* ════════ Scene CHANGE 04（step 6）—— 配色 × 字体配对 ════════ */}
      <SceneFade active={sceneD} exitMs={420} enterDelayMs={420}>
        <div className="sk__chg-scene">
          <Reveal kind="fade" duration={620} delay={80} className="sk__chg-num">+ 改动 04</Reveal>
          <Reveal kind="rise" duration={1100} delay={240} className="sk__chg-title" as="h2">
            <em>配色 × 字体</em> 配对参考表
          </Reveal>

          <div className="sk__split">
            <Reveal kind="rise" duration={720} delay={500} className="sk__split-left">
              <div className="sk__cd-col">
                <div className="sk__cd-tag">
                  <span className="sk__cd-mark">+ 新增</span>
                  经过验证 · 5 套起点
                </div>
                <div className="sk__pairs">
                  {[
                    { tag: '优雅杂志风',  color: 'oklch 暖棕',   font: 'Newsreader + Outfit' },
                    { tag: '高端品牌',    color: 'oklch 近黑',   font: 'Sora + Plus Jakarta Sans' },
                    { tag: '极简专业',    color: 'oklch 青蓝',   font: 'Outfit + Space Grotesk' },
                    { tag: '活泼消费',    color: 'oklch 珊瑚',   font: 'Plus Jakarta Sans + Outfit' },
                    { tag: '手作温度',    color: 'oklch 焦糖',   font: 'Caveat + Newsreader' },
                  ].map((p, i) => (
                    <div
                      key={p.tag}
                      className="sk__pair"
                      style={{ animationDelay: `${700 + i * 110}ms` }}
                    >
                      <span className="sk__pair-tag">{p.tag}</span>
                      <span className="sk__pair-color">{p.color}</span>
                      <span className="sk__pair-x">×</span>
                      <span className="sk__pair-font">{p.font}</span>
                    </div>
                  ))}
                </div>
              </div>
            </Reveal>

            <Reveal kind="rise" duration={780} delay={760} className="sk__split-right">
              <Excerpt
                filePath="references / advanced-patterns.md"
                range="L505 — L516"
                pulseDelay={1000}
                lines={[
                  { n: 503, text: '## Color × Font Pairing Reference', },
                  { n: 504, text: '' },
                  { n: 505, text: <>| Style | Primary (oklch) | Font Pairing | Best For |</>, hi: true },
                  { n: 506, text: '|---|---|---|---|' },
                  { n: 507, text: <>| Modern tech | <em>oklch(0.55 0.25 250)</em> | Space Grotesk + Inter | SaaS, AI |</> },
                  { n: 508, text: <>| <b>Elegant editorial</b> | oklch(0.35 0.10 30) warm brown | <em>Newsreader + Outfit</em> | Content, blogs |</>, hi: true },
                  { n: 509, text: <>| <b>Premium brand</b> | oklch(0.20 0.02 250) near-black | <em>Sora + Plus Jakarta Sans</em> | Luxury, finance |</>, hi: true },
                  { n: 510, text: <>| Lively consumer | oklch(0.70 0.20 30) coral | Plus Jakarta Sans + Outfit | E-commerce |</>, hi: true },
                  { n: 511, text: <>| <b>Minimal pro</b> | oklch(0.50 0.15 200) teal-blue | <em>Outfit + Space Grotesk</em> | Data, B2B |</>, hi: true },
                  { n: 512, text: <>| <b>Artisan warmth</b> | oklch(0.55 0.15 80) caramel | <em>Caveat + Newsreader</em> | Food, education |</>, hi: true },
                  { n: 513, text: '' },
                  { n: 514, text: '> 这些配对的核心：给 AI 一个有品位的<em>起点</em>。', hi: true, },
                  { n: 515, text: '' },
                ]}
                caption={<>给 AI 一个<em>靠谱</em>的起点 → 比让它自由发挥稳定</>}
              />
            </Reveal>
          </div>
        </div>
      </SceneFade>

      {/* ════════ Scene CLOSE（step 7）════════ */}
      <SceneFade active={sceneClose} exitMs={420} enterDelayMs={420}>
        <div className="sk__close">
          <Reveal kind="rise" duration={1100} delay={120} className="sk__close-l1" as="h1">
            给 AI 一个<em>靠谱的起点</em>
          </Reveal>
          <Reveal kind="rise" duration={1100} delay={780} className="sk__close-l2" as="h2">
            比让它<em>自由发挥</em> —— 稳得多
          </Reveal>
        </div>
      </SceneFade>
    </section>
  );
}

const def: ChapterDef = {
  id: 'skill-changes',
  title: 'Skill 的关键改动',
  eyebrow: '11',
  steps: 8,
  theme: 'light',
  Component: SkillChanges,
};

export default def;
