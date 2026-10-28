import type { ChapterContext, ChapterDef } from '../types';
import { Reveal } from '../../shared/Reveal';
import { NumberTicker } from '../../shared/NumberTicker';
import { LiveClock, FlickerNumber } from '../../shared/LiveTicker';
import { SceneFade } from '../../shared/SceneFade';
import './Opening.css';

/**
 * Chapter 01 · Opening 「一则崩盘」
 *
 * 4 幕 × 14 个 step：
 *  Scene A · Crash      (0..3)  Figma 股价崩盘
 *  Scene B · Victims    (4..8)  Anthropic 历次带崩列表
 *  Scene C · Reveal     (9..11) Claude Design 揭幕
 *  Scene D · Skill      (12..13) 我把它做成了 Skill
 *
 * 真实数据：LegalZoom -20% / CRCL -20% / CrowdStrike -7% / Figma -7%
 *
 * 设计原则：
 *  - 没有任何"网页 chrome"（没有顶部章节标记 / 底部 footer / 永久 hint）
 *  - 每幕通过 SceneFade 优雅交叉淡入淡出，不会有重叠 bug
 *  - 每个 step 推进只增加 1 个新视觉元素
 */

const VICTIMS = [
  { product: 'Claude Cowork',        company: 'LegalZoom',       ticker: 'LZ',   drop: -20.0, field: '法律服务' },
  { product: 'Claude Code Security', company: 'Circle Internet', ticker: 'CRCL', drop: -20.0, field: '云安全' },
  { product: 'Claude Mythos',        company: 'CrowdStrike',     ticker: 'CRWD', drop: -7.0,  field: '终端安全' },
  { product: 'Claude Design',        company: 'Figma',           ticker: 'FIG',  drop: -7.0,  field: '设计协作', current: true },
];

function Opening({ localStep }: ChapterContext) {
  const at = (n: number) => localStep >= n;
  const between = (a: number, b: number) => localStep >= a && localStep <= b;

  const sceneCrash = localStep <= 3;
  const sceneVictims = between(4, 8);
  const sceneReveal = between(9, 11);
  const sceneSkill = at(12);

  return (
    <section className="opening">
      {/* ============== SCENE A · Crash (0..3) ============== */}
      <SceneFade active={sceneCrash}>
        <div className="opening__sceneA">
          {/* LIVE 报价条 —— 仅在崩盘场景中作为"市场环境"出现 */}
          <div className="opening__live">
            <span className="opening__live-dot" />
            <span className="opening__live-label">NASDAQ · LIVE</span>
            <LiveClock className="opening__live-clock" />
            <span className="opening__live-sep">|</span>
            <span className="opening__live-quote">
              <span className="opening__live-quote-tag">FIG</span>
              <FlickerNumber base={48.32} amplitude={0.18} className="opening__live-quote-val" />
              <span className="opening__live-quote-d">−7.0%</span>
            </span>
          </div>

          {/* "FIGMA" 巨字背景 —— step 2 才显形 */}
          {at(2) && (
            <Reveal kind="blur" duration={1200} delay={120}>
              <div className="opening__crash-mega">FIGMA</div>
            </Reveal>
          )}

          {/* 引子小字 —— step 1 */}
          {at(1) && (
            <Reveal kind="rise" duration={620} className="opening__crash-intro">
              <span className="opening__crash-intro-tag">2026 · 04 · 17 · NASDAQ CLOSE</span>
              <span className="opening__crash-intro-text">就在前两天 ——</span>
            </Reveal>
          )}

          {/* 折线图 —— step 1 开始绘制历史 / step 2 崩盘 */}
          <CrashChart phase={localStep} />

          {/* 中文 headline —— step 2 */}
          {at(2) && (
            <Reveal kind="rise" duration={780} delay={620} className="opening__crash-headline">
              <span className="opening__crash-line">Figma</span>
              <em className="opening__crash-emph">的股价崩了。</em>
            </Reveal>
          )}

          {/* −7.0% 大数字 —— step 3 */}
          {at(3) && (
            <Reveal kind="rise" duration={520} className="opening__crash-stat">
              <div className="opening__crash-stat-num">
                <span className="opening__crash-stat-sign">−</span>
                <NumberTicker
                  to={7.0}
                  from={0}
                  duration={1200}
                  decimals={1}
                  delay={120}
                />
                <span className="opening__crash-stat-pct">%</span>
              </div>
              <div className="opening__crash-stat-label">单日跌幅 · 收盘</div>
            </Reveal>
          )}
        </div>
      </SceneFade>

      {/* ============== SCENE B · Victims (4..8) ============== */}
      <SceneFade active={sceneVictims}>
        <div className="opening__sceneB">
          <div className="opening__vics-eyebrow">
            <Reveal kind="rise" duration={680} className="opening__vics-eyebrow-inner">
              <span>这已经是</span>
              <em className="opening__vics-em">第 N 次</em>
              <span>了 ——</span>
            </Reveal>
            <Reveal kind="fade" duration={520} delay={520} className="opening__vics-by">
              <span className="opening__vics-by-tag">CRASHED · BY</span>
              <span className="opening__vics-by-name">ANTHROPIC</span>
            </Reveal>
          </div>

          <div className="opening__vics-table">
            <div className="opening__vics-thead">
              <span>ANTHROPIC PRODUCT</span>
              <span>AFFECTED COMPANY</span>
              <span>TICKER</span>
              <span>SECTOR</span>
              <span style={{ textAlign: 'right' }}>DAY DROP</span>
            </div>

            {VICTIMS.map((v, i) => {
              const showAt = 5 + i;
              if (!at(showAt)) return null;
              return (
                <Reveal
                  key={v.company}
                  kind="wipe-r"
                  duration={780}
                  delay={i === 0 ? 80 : 0}
                >
                  <VictimRow v={v} animate={localStep === showAt} />
                </Reveal>
              );
            })}
          </div>
        </div>
      </SceneFade>

      {/* ============== SCENE C · Claude Design 揭幕 (9..11) ============== */}
      <SceneFade active={sceneReveal}>
        <div className="opening__sceneC">
          <Reveal kind="fall" duration={700} className="opening__reveal-meta">
            <span>ANTHROPIC</span>
            <span className="dot" />
            <span>NEW PRODUCT</span>
            <span className="dot" />
            <span>2026 · 04 · 17</span>
          </Reveal>

          <h1 className="opening__reveal-title">
            <Reveal
              kind="blur"
              duration={1100}
              delay={120}
              className="opening__reveal-word"
            >
              Claude
            </Reveal>
            {at(10) && (
              <Reveal
                kind="blur"
                duration={1100}
                className="opening__reveal-word opening__reveal-word--em"
              >
                Design
              </Reveal>
            )}
          </h1>

          {at(10) && (
            <Reveal kind="rise" duration={720} delay={680} className="opening__reveal-sub">
              <span className="opening__reveal-tilde">——</span>
              <span>设计师的 Claude Code</span>
            </Reveal>
          )}

          {at(11) && (
            <div className="opening__reveal-tags">
              <Reveal kind="rise" duration={520}>
                <span>Powered by Opus 4.7</span>
              </Reveal>
              <Reveal kind="rise" duration={520} delay={120}>
                <span>Pro · Max · Team · Enterprise</span>
              </Reveal>
              <Reveal kind="rise" duration={520} delay={240}>
                <span>左侧聊天 · 右侧画布</span>
              </Reveal>
            </div>
          )}
        </div>
      </SceneFade>

      {/* ============== SCENE D · Skill (12..13) ============== */}
      <SceneFade active={sceneSkill}>
        <div className="opening__sceneD">
          <Reveal kind="rise" duration={620} className="opening__pivot-eyebrow">
            <span className="opening__pivot-eyebrow-bar" />
            <span>于是 ——</span>
          </Reveal>

          <h2 className="opening__pivot-title">
            <Reveal kind="blur" duration={900} delay={120}>
              我把它做成了一个
            </Reveal>
            <Reveal
              kind="blur"
              duration={900}
              delay={520}
              className="opening__pivot-em"
            >
              人人都能用的 Skill。
            </Reveal>
          </h2>

          {at(13) && (
            <div className="opening__pivot-row">
              <Reveal kind="wipe-r" duration={900} delay={80}>
                <SkillCard />
              </Reveal>
              <Reveal kind="rise" duration={720} delay={520} className="opening__pivot-aside">
                <span className="opening__pivot-aside-q">"</span>
                <span>人人都能成为</span>
                <em>顶级网站设计师。</em>
              </Reveal>
            </div>
          )}
        </div>
      </SceneFade>
    </section>
  );
}

/* ────────────── 子组件 ────────────── */

function CrashChart({ phase }: { phase: number }) {
  const showHistory = phase >= 1;
  const showCrash = phase >= 2;
  const showFill = phase >= 2;
  const showEnd = phase >= 2;

  return (
    <svg
      className="opening__chart"
      viewBox="0 0 1760 540"
      preserveAspectRatio="none"
      aria-hidden
    >
      <defs>
        <linearGradient id="crashGrad" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stopColor="oklch(0.560 0.200 22)" stopOpacity="0.5" />
          <stop offset="100%" stopColor="oklch(0.560 0.200 22)" stopOpacity="0" />
        </linearGradient>
      </defs>

      <g className="opening__chart-grid">
        {[0, 1, 2, 3].map((i) => (
          <line key={i} x1="0" x2="1760" y1={120 + i * 110} y2={120 + i * 110} />
        ))}
      </g>

      {showHistory && (
        <path
          className="opening__chart-history"
          d="M 0 290 L 110 285 L 220 296 L 330 282 L 440 290 L 550 276 L 660 286 L 770 270 L 880 280 L 990 264 L 1100 272 L 1210 258"
          fill="none"
          strokeWidth="2.5"
        />
      )}

      {showCrash && (
        <path
          className="opening__chart-crash"
          d="M 1210 258 L 1290 320 L 1380 400 L 1500 470 L 1760 510"
          fill="none"
          strokeWidth="3"
        />
      )}

      {showFill && (
        <path
          className="opening__chart-fill"
          d="M 1210 258 L 1290 320 L 1380 400 L 1500 470 L 1760 510 L 1760 540 L 1210 540 Z"
          fill="url(#crashGrad)"
        />
      )}

      {showEnd && (
        <g className="opening__chart-end">
          <line x1="0" y1="258" x2="1760" y2="258" strokeDasharray="2 8" strokeWidth="1" />
          <circle cx="1760" cy="510" r="6" />
          <text x="1740" y="245" textAnchor="end">前日收盘 51.95</text>
          <text x="1740" y="495" textAnchor="end">今日收盘 48.32</text>
        </g>
      )}
    </svg>
  );
}

interface VictimRowProps {
  v: typeof VICTIMS[number];
  animate: boolean;
}

function VictimRow({ v, animate }: VictimRowProps) {
  return (
    <div className={`opening__vic ${v.current ? 'is-current' : ''}`}>
      <span className="opening__vic-product">{v.product}</span>
      <span className="opening__vic-company">{v.company}</span>
      <span className="opening__vic-ticker">${v.ticker}</span>
      <span className="opening__vic-field">{v.field}</span>
      <span className="opening__vic-drop">
        {animate ? (
          <NumberTicker
            to={Math.abs(v.drop)}
            decimals={1}
            duration={900}
            delay={220}
            prefix="−"
            suffix="%"
          />
        ) : (
          <span style={{ fontVariantNumeric: 'tabular-nums' }}>
            −{Math.abs(v.drop).toFixed(1)}%
          </span>
        )}
      </span>
      {v.current && <span className="opening__vic-flag">CURRENT</span>}
    </div>
  );
}

function SkillCard() {
  return (
    <div className="opening__skill-card">
      <div className="opening__skill-card-deco" />
      <div className="opening__skill-card-head">
        <span className="opening__skill-card-tag">SKILL · v1</span>
        <span className="opening__skill-card-name">web-design-engineer</span>
      </div>
      <div className="opening__skill-card-body">
        <div className="opening__skill-card-row">
          <span className="opening__skill-card-k">支持环境</span>
          <span className="opening__skill-card-v">Cursor · Claude Code · Codex</span>
        </div>
        <div className="opening__skill-card-row">
          <span className="opening__skill-card-k">体量</span>
          <span className="opening__skill-card-v">≈ 400 行 · 含模板库 ≈ 520 行</span>
        </div>
        <div className="opening__skill-card-row">
          <span className="opening__skill-card-k">来源</span>
          <span className="opening__skill-card-v">Claude Design 系统提示词 · 提炼 + 改良</span>
        </div>
        <div className="opening__skill-card-row">
          <span className="opening__skill-card-k">效果</span>
          <span className="opening__skill-card-v">85 → 95 分</span>
        </div>
      </div>
      <div className="opening__skill-card-foot">
        <span className="opening__skill-card-pulse" />
        <span>READY · open-source</span>
      </div>
    </div>
  );
}

const def: ChapterDef = {
  id: 'opening',
  title: '开场 · 一则崩盘',
  eyebrow: '01',
  steps: 14,
  theme: 'ink',
  Component: Opening,
};

export default def;
