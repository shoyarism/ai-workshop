import type { ChapterDef } from './types';
import Opening from './01-opening';
import Video from './02-video';
import CorePoint from './03-core-point';
import Role from './04-role';
import Workflow from './05-workflow';
import AntiAi from './06-anti-ai';
import Oklch from './07-oklch';
import Restraint from './08-restraint';
import Verification from './09-verification';
import ToSkill from './10-to-skill';
import SkillChanges from './11-skill-changes';
import References from './12-references';
import Closing from './13-closing';
import Outro from './14-outro';

/**
 * 章节注册表 —— 顺序即播放顺序。
 * 后续每写一章，append 到这里即可，绝不修改既有章节文件。
 */
export const chapters: ChapterDef[] = [
  Opening,
  Video,
  CorePoint,
  Role,
  Workflow,
  AntiAi,
  Oklch,
  Restraint,
  Verification,
  ToSkill,
  SkillChanges,
  References,
  Closing,
  Outro,
];
