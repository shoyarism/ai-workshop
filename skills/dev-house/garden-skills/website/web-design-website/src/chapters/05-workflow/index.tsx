import type { ChapterContext, ChapterDef } from '../types';
import { Reveal } from '../../shared/Reveal';
import { SceneFade } from '../../shared/SceneFade';
import './Workflow.css';

/**
 * Chapter 05 · 第二部分：工作流
 *
 * 口播主旨：
 *   - 六步流程：理解需求 → 探索资源 → 制定计划 → 搭建结构 → 完成验证 → 极简总结
 *   - 细节①：什么时候问 / 什么时候直接干 —— 信息够就干，不够才问
 *       用户: "做个 PPT"               → AI 先问几个问题
 *       用户: "做个 PPT, 工程全员 All Hands, 10 min" → AI 直接动手
 *   - 细节②：极简总结 —— "Summarize EXTREMELY BRIEFLY"
 *
 * 节奏（7 步 / step 0..6）：
 *  0  环境（eyebrow）
 *  1  原文 prompt block + 六站流水线（空）
 *  2  点亮第 1-3 站（line 推进）
 *  3  点亮第 4-6 站
 *  4  pivot：细节① "何时问 vs 何时干"
 *  5  双栏对话气泡对比
 *  6  细节② "Summarize EXTREMELY BRIEFLY" 原文 + 反例 / 正例对比
 */

interface Station {
  no: string;
  en: string;
  cn: string;
}

const STATIONS: Station[] = [
  { no: '1', en: 'Understand',  cn: '理解需求' },
  { no: '2', en: 'Explore',     cn: '探索资源' },
  { no: '3', en: 'Plan',        cn: '制定计划' },
  { no: '4', en: 'Build',       cn: '搭建结构' },
  { no: '5', en: 'Verify',      cn: '完成验证' },
  { no: '6', en: 'Brief',       cn: '极简总结' },
];

function Workflow({ localStep }: ChapterContext) {
  const at = (n: number) => localStep >= n;

  // —— 三幕 ——
  const scenePipe    = localStep <= 3;
  const sceneDecide  = localStep === 4 || localStep === 5;
  const sceneSummary = localStep >= 6;

  // 流水线点亮进度 0..6
  const litCount = (() => {
    if (localStep < 1) return 0;
    if (localStep === 1) return 0;
    if (localStep === 2) return 3;
    return 6;
  })();
  const linePct = (litCount / 6) * 100;

  return (
    <section className="wf">
      {/* ════════════ Scene PIPELINE（step 0..3）════════════ */}
      <SceneFade active={scenePipe} exitMs={420} enterDelayMs={120}>
        <div className="wf__pipe-scene">
          {at(1) && (
            <Reveal kind="rise" duration={780} delay={80} className="wf__excerpt">
              <div className="wf__excerpt-head">
                <span className="wf__src-bracket">[</span>
                <span className="wf__src-label">SYSTEM PROMPT</span>
                <span className="wf__src-sep">·</span>
                <span className="wf__src-line">L17-23</span>
                <span className="wf__src-sep">/</span>
                <span className="wf__src-mute">原文</span>
                <span className="wf__src-bracket">]</span>
              </div>
              <div className="wf__excerpt-body">
                <div className="wf__excerpt-title">## Your workflow</div>
                <div className="wf__excerpt-list">
                  <span><b>1.</b> Understand user needs ...</span>
                  <span><b>2.</b> Explore provided resources ...</span>
                  <span><b>3.</b> Plan and/or make a todo list.</span>
                  <span><b>4.</b> Build folder structure ...</span>
                  <span><b>5.</b> Finish: call <code>done</code> ...</span>
                  <span><b>6.</b> Summarize <em>EXTREMELY BRIEFLY</em> — caveats and next steps only.</span>
                </div>
              </div>
            </Reveal>
          )}

          {at(1) && (
            <Reveal kind="rise" duration={900} delay={520} className="wf__pipeline">
              {/* 底部基线 */}
              <div className="wf__line">
                <div className="wf__line-fill" style={{ width: `${linePct}%` }} />
              </div>

              {/* 6 站 */}
              <div className="wf__stations">
                {STATIONS.map((s, i) => {
                  const lit = i < litCount;
                  return (
                    <div
                      key={s.no}
                      className={`wf__station ${lit ? 'is-lit' : ''}`}
                      style={{ transitionDelay: `${i * 90}ms` }}
                    >
                      <div className="wf__station-cn">{s.cn}</div>
                      <div className="wf__station-node">
                        <span className="wf__station-no">{s.no}</span>
                        <span className="wf__station-pulse" />
                      </div>
                      <div className="wf__station-en">{s.en}</div>
                    </div>
                  );
                })}
              </div>
            </Reveal>
          )}
        </div>
      </SceneFade>

      {/* ════════════ Scene DECIDE（step 4..5）════════════ */}
      <SceneFade active={sceneDecide} exitMs={420} enterDelayMs={420}>
        <div className="wf__decide-scene">
          <Reveal kind="rise" duration={780} delay={80} className="wf__decide-head">
            <span className="wf__decide-num">细节①</span>
            <h2 className="wf__decide-title">
              什么时候<em>问</em>？什么时候<em className="wf__decide-do">直接干</em>？
            </h2>
            <div className="wf__decide-rule">
              <span className="wf__src-bracket">[</span>
              <span className="wf__src-label">RULE</span>
              <span className="wf__src-bracket">]</span>
              <span className="wf__decide-rule-text">信息充足就干 · 信息不足才问</span>
            </div>
          </Reveal>

          <div className="wf__decide-grid">
            {/* —— 左：模糊请求 → 反复问 —— */}
            <Reveal kind="rise" duration={780} delay={260} className="wf__chat wf__chat--ask">
              <div className="wf__chat-tag">
                <span className="wf__chat-tag-dot" />
                AMBIGUOUS · 模糊请求
              </div>

              <div className="wf__bubble wf__bubble--user">
                <span className="wf__bubble-meta">USER</span>
                <p>帮我做个 PPT</p>
              </div>

              <div className="wf__bubble wf__bubble--ai">
                <span className="wf__bubble-meta">CLAUDE</span>
                <p>受众？时长？正式度？品牌？数据有吗？...</p>
                <div className="wf__qmarks">
                  <span style={{ animationDelay: '0ms'   }}>?</span>
                  <span style={{ animationDelay: '180ms' }}>?</span>
                  <span style={{ animationDelay: '360ms' }}>?</span>
                  <span style={{ animationDelay: '540ms' }}>?</span>
                </div>
              </div>

              <div className="wf__chat-verdict wf__chat-verdict--ask">
                → ASK QUESTIONS
              </div>
            </Reveal>

            {/* —— 中央分隔 —— */}
            <div className="wf__decide-vs">
              <span className="wf__decide-vs-line" />
              <span className="wf__decide-vs-knob">vs</span>
              <span className="wf__decide-vs-line" />
            </div>

            {/* —— 右：详细请求 → 直接动手 —— */}
            {at(5) && (
              <Reveal kind="rise" duration={780} delay={120} className="wf__chat wf__chat--do">
                <div className="wf__chat-tag">
                  <span className="wf__chat-tag-dot wf__chat-tag-dot--do" />
                  ENOUGH INFO · 信息够
                </div>

                <div className="wf__bubble wf__bubble--user">
                  <span className="wf__bubble-meta">USER</span>
                  <p>帮我做个 PPT，工程全员 All Hands，10&nbsp;分钟</p>
                </div>

                <div className="wf__bubble wf__bubble--ai">
                  <span className="wf__bubble-meta">CLAUDE</span>
                  <p>好的，开始 ——</p>
                  <div className="wf__action">
                    <span className="wf__action-bar" />
                    <span className="wf__action-bar" />
                    <span className="wf__action-bar" />
                  </div>
                </div>

                <div className="wf__chat-verdict wf__chat-verdict--do">
                  → NO QUESTIONS · GO BUILD
                </div>
              </Reveal>
            )}
          </div>
        </div>
      </SceneFade>

      {/* ════════════ Scene SUMMARY（step 6）════════════ */}
      <SceneFade active={sceneSummary} exitMs={420} enterDelayMs={420}>
        <div className="wf__sum-scene">
          <Reveal kind="fade" duration={620} delay={80} className="wf__sum-num">
            细节②
          </Reveal>

          <Reveal kind="rise" duration={1100} delay={180} className="wf__sum-hero" as="h1">
            <span className="wf__sum-hero-en">Summarize <em>EXTREMELY BRIEFLY</em></span>
            <span className="wf__sum-hero-cn">只说 <em>注意事项</em> 与 <em>下一步</em>。</span>
          </Reveal>

          <Reveal kind="rise" duration={780} delay={520} className="wf__sum-source">
            <span className="wf__src-bracket">[</span>
            <span className="wf__src-label">SYSTEM PROMPT</span>
            <span className="wf__src-sep">·</span>
            <span className="wf__src-line">L23</span>
            <span className="wf__src-bracket">]</span>
            <span className="wf__sum-source-quote">
              &ldquo;Summarize EXTREMELY BRIEFLY — caveats and next steps only.&rdquo;
            </span>
          </Reveal>

          <Reveal kind="rise" duration={780} delay={760} className="wf__sum-grid">
            {/* 反例 */}
            <div className="wf__sum-card wf__sum-card--bad">
              <div className="wf__sum-card-tag">
                <span className="wf__sum-x">×</span> 复述自己干了什么
              </div>
              <div className="wf__sum-card-body">
                我先创建了 <s>Header.tsx</s>，然后又新增了 <s>Hero.tsx</s>，
                接着把样式拆分到 <s>theme.ts</s>，又给按钮加了 hover ...
              </div>
              <div className="wf__sum-strike" />
            </div>

            {/* 正例 */}
            <div className="wf__sum-card wf__sum-card--good">
              <div className="wf__sum-card-tag">
                <span className="wf__sum-check">✓</span> 注意事项 + 下一步
              </div>
              <div className="wf__sum-card-body">
                <p><b>caveats</b> — 暂未做响应式 / 文案为占位</p>
                <p><b>next</b> — 加 hover 状态 / 替换真实文案</p>
              </div>
            </div>
          </Reveal>
        </div>
      </SceneFade>
    </section>
  );
}

const def: ChapterDef = {
  id: 'workflow',
  title: '第二部分 · 工作流',
  eyebrow: '05',
  steps: 7,
  theme: 'ink',
  Component: Workflow,
};

export default def;
