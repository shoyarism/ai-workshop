import type { ChapterContext, ChapterDef } from '../types';
import { Reveal } from '../../shared/Reveal';
import { SceneFade } from '../../shared/SceneFade';
import './References.css';

/**
 * Chapter 12 · References 文件 · 高级模板库
 *
 * 口播原文（article/口播稿.md L218）：
 *   "Skill 还附带一个 references 文件，里面包含了一些典型的代码模板，
 *    这里的灵感来源于 Claude Design 的 `copy_starter_component` 。"
 *
 * 节奏（4 步 / step 0..3）：
 *  0  hero · references / advanced-patterns.md 文件名大字 + 路径标签
 *  1  7 大模板分类 · 卡片瀑布依次浮入
 *  2  灵感来源 · Claude Design 的 copy_starter_component
 *  3  收尾："给 AI 提供高质量的起点脚手架 —— 而非从零硬画"
 */

interface Tpl {
  id: string;
  num: string;
  name: string;
  cn: string;
  desc: string;
  glyph: string;
}

const TEMPLATES: Tpl[] = [
  { id: 'slide',  num: '01', name: 'Responsive Slide Engine',     cn: '响应式幻灯片引擎', desc: '1920×1080 自适应缩放 / 1-indexed 标号 / localStorage 续播', glyph: '▭' },
  { id: 'frame',  num: '02', name: 'Device Simulation Frames',    cn: '设备模拟外框',     desc: 'iPhone / Android / 浏览器窗口 —— 让原型像在真机里', glyph: '▢' },
  { id: 'tweak',  num: '03', name: 'Tweaks Panel',                cn: '运行时参数面板',   desc: '右下角浮动面板：主题 / 字号 / 暗色 / 间距 一键切', glyph: '⚙' },
  { id: 'time',   num: '04', name: 'Animation Timeline Engine',   cn: '动画时间线引擎',   desc: 'useTime + Easing + interpolate —— 时间轴可拖拽', glyph: '⌁' },
  { id: 'canvas', num: '05', name: 'Design Canvas',               cn: '多方案对比画布',   desc: '把 N 个变体并排铺开，让用户一眼挑出来', glyph: '◫' },
  { id: 'dark',   num: '06', name: 'Dark Mode Toggle',            cn: '暗色模式切换',     desc: 'prefers-color-scheme + 手动覆盖，token 一键翻面', glyph: '◐' },
  { id: 'data',   num: '07', name: 'Data Visualization',          cn: '数据可视化模板',   desc: 'Chart.js / D3 / oklch palette —— data-ink 比优先', glyph: '◢' },
];

function References({ localStep }: ChapterContext) {
  const sceneHero    = localStep <= 0;
  const sceneList    = localStep === 1;
  const sceneOrigin  = localStep === 2;
  const sceneClose   = localStep >= 3;

  return (
    <section className="rf">
      {/* ════════ Scene HERO（step 0）════════ */}
      <SceneFade active={sceneHero} exitMs={420} enterDelayMs={120}>
        <div className="rf__hero">
          <Reveal kind="fade" duration={620} delay={80} className="rf__hero-eyebrow">
            <span className="rf__src-bracket">[</span>
            <span className="rf__src-label">SKILL · 附带文件</span>
            <span className="rf__src-bracket">]</span>
          </Reveal>

          <Reveal kind="rise" duration={1100} delay={260} className="rf__hero-pre" as="p">
            Skill 还附带一个 ——
          </Reveal>

          <Reveal kind="rise" duration={1300} delay={620} className="rf__hero-name" as="h1">
            <span className="rf__hero-dim">references / </span>
            <em>advanced-patterns.md</em>
          </Reveal>

          <Reveal kind="rise" duration={780} delay={1300} className="rf__hero-meta">
            <span>≈ 520 行</span>
            <span className="rf__hero-meta-dot" />
            <span>7 大模板</span>
            <span className="rf__hero-meta-dot" />
            <span>开箱即用</span>
          </Reveal>
        </div>
      </SceneFade>

      {/* ════════ Scene LIST（step 1）—— 7 大模板瀑布 ════════ */}
      <SceneFade active={sceneList} exitMs={420} enterDelayMs={420}>
        <div className="rf__list-scene">
          <Reveal kind="fade" duration={620} delay={80} className="rf__list-cap">
            7 套<em>典型代码模板</em> · 给 AI 起点脚手架
          </Reveal>

          <div className="rf__grid">
            {TEMPLATES.map((t, i) => (
              <div
                key={t.id}
                className={`rf__card rf__card--${t.id}`}
                style={{ animationDelay: `${260 + i * 110}ms` }}
              >
                <div className="rf__card-num">
                  <span>{t.num}</span>
                  <span className="rf__card-glyph">{t.glyph}</span>
                </div>
                <div className="rf__card-name">{t.name}</div>
                <div className="rf__card-cn">{t.cn}</div>
                <div className="rf__card-desc">{t.desc}</div>
                <div className="rf__card-foot">
                  <span className="rf__card-foot-mono">references/advanced-patterns.md</span>
                  <span className="rf__card-foot-arrow">→</span>
                </div>
              </div>
            ))}

            {/* 第 8 格补一个"摘自原始 Skill"的小标签 */}
            <div
              className="rf__card rf__card--hint"
              style={{ animationDelay: `${260 + 7 * 110}ms` }}
            >
              <div className="rf__card-hint-eyebrow">+ 还在更新</div>
              <div className="rf__card-hint-line">
                每个模板都是<em>真实项目验证过</em>的，<br />
                不是"AI 自由发挥"出来的。
              </div>
            </div>
          </div>
        </div>
      </SceneFade>

      {/* ════════ Scene ORIGIN（step 2）—— 灵感来源 ════════ */}
      <SceneFade active={sceneOrigin} exitMs={420} enterDelayMs={420}>
        <div className="rf__origin">
          <Reveal kind="fade" duration={620} delay={80} className="rf__origin-eyebrow">
            灵感来源 ——
          </Reveal>

          <div className="rf__origin-row">
            {/* 左：Claude Design 原始函数 */}
            <Reveal kind="rise" duration={780} delay={300} className="rf__origin-card rf__origin-card--src">
              <div className="rf__origin-card-tag">
                <span className="rf__src-bracket">[</span>
                <span className="rf__src-label">CLAUDE DESIGN · TOOL</span>
                <span className="rf__src-bracket">]</span>
              </div>
              <div className="rf__origin-card-fn">
                <span className="rf__origin-card-fn-name">copy_starter_component</span>
                <span className="rf__origin-card-fn-paren">()</span>
              </div>
              <div className="rf__origin-card-desc">
                给 Agent 提供<em>高质量的起点脚手架</em> ——<br />
                而不是让它从零开始 <em>"自由发挥"</em>。
              </div>
            </Reveal>

            {/* 中：箭头 */}
            <Reveal kind="fade" duration={780} delay={780} className="rf__origin-arrow" as="span">
              <span className="rf__origin-arrow-line" />
              <span className="rf__origin-arrow-text">提炼</span>
              <span className="rf__origin-arrow-head">→</span>
            </Reveal>

            {/* 右：references */}
            <Reveal kind="rise" duration={780} delay={900} className="rf__origin-card rf__origin-card--dst">
              <div className="rf__origin-card-tag rf__origin-card-tag--dst">
                <span className="rf__src-bracket">[</span>
                <span className="rf__src-label">SKILL · references/</span>
                <span className="rf__src-bracket">]</span>
              </div>
              <div className="rf__origin-card-fn">
                <span className="rf__origin-card-fn-name">advanced-patterns.md</span>
              </div>
              <div className="rf__origin-card-desc">
                7 套<em>开箱即用</em>的代码模板 ——<br />
                Claude Code · Cursor · Codex 都能直接 import。
              </div>
            </Reveal>
          </div>

          <Reveal kind="fade" duration={780} delay={1500} className="rf__origin-foot">
            把 Anthropic 的<em>独家秘籍</em>，搬到任何工具里都能用
          </Reveal>
        </div>
      </SceneFade>

      {/* ════════ Scene CLOSE（step 3）════════ */}
      <SceneFade active={sceneClose} exitMs={420} enterDelayMs={420}>
        <div className="rf__close">
          <Reveal kind="rise" duration={1100} delay={120} className="rf__close-l1" as="h1">
            高质量的<em>起点脚手架</em>
          </Reveal>
          <Reveal kind="rise" duration={1100} delay={780} className="rf__close-l2" as="h2">
            ——&nbsp; 比让 AI <em>从零硬画</em>，强得多
          </Reveal>
        </div>
      </SceneFade>
    </section>
  );
}

const def: ChapterDef = {
  id: 'references',
  title: 'references · 高级模板库',
  eyebrow: '12',
  steps: 4,
  theme: 'light',
  Component: References,
};

export default def;
