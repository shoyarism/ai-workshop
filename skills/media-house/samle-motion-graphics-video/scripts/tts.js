#!/usr/bin/env node
// scripts/tts.js — Neural TTS synthesis with sentence-level timestamps
// Usage: node scripts/tts.js --script ../sample/script.md --output audio.mp3

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

const args = process.argv.slice(2);
const scriptIdx = args.indexOf('--script');
const outputIdx = args.indexOf('--output');

const scriptFile = scriptIdx >= 0 ? args[scriptIdx + 1] : null;
const outputFile = outputIdx >= 0 ? args[outputIdx + 1] : 'audio.mp3';

if (!scriptFile) {
  console.error('Usage: node scripts/tts.js --script <script.md> --output <audio.mp3>');
  process.exit(1);
}

const script = fs.readFileSync(scriptFile, 'utf-8');
const sentences = script
  .split('\n')
  .map(line => line.replace(/^##\s+/, '').trim())
  .filter(line => line && !line.startsWith('SCENE') && !line.startsWith('#'));

// Generate SRT subtitles with edge-tts
const srtLines = [];
let index = 1;
let startTime = 0;

for (const sentence of sentences) {
  const duration = Math.max(2, Math.ceil(sentence.split(' ').length * 0.35));
  const endTime = startTime + duration;

  const fmtTime = (t) => {
    const h = Math.floor(t / 3600);
    const m = Math.floor((t % 3600) / 60);
    const s = Math.floor(t % 60);
    const ms = Math.floor((t % 1) * 1000);
    return `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')},${String(ms).padStart(3,'0')}`;
  };

  srtLines.push(`${index}\n${fmtTime(startTime)} --> ${fmtTime(endTime)}\n${sentence}\n`);
  index++;
  startTime = endTime + 0.3; // pause between sentences
}

fs.writeFileSync(outputFile.replace('.mp3', '.srt'), srtLines.join('\n'));
console.log(`Generated: ${outputFile.replace('.mp3', '.srt')}`);
console.log(`Sentences: ${sentences.length}, Duration: ~${startTime}s`);

// Try edge-tts synthesis
try {
  console.log('Synthesizing with edge-tts...');
  const voice = 'en-US-GuyNeural';
  const rate = '-10%';
  execSync(`edge-tts --voice ${voice} --rate ${rate} -f "${outputFile.replace('.mp3', '.srt')}" -w "${outputFile.replace('.mp3', '_tmp.mp3')}"`, { stdio: 'inherit' });
  fs.renameSync(outputFile.replace('.mp3', '_tmp.mp3'), outputFile);
  console.log(`Audio: ${outputFile}`);
} catch (e) {
  console.warn('edge-tts not available, generating silent audio placeholder...');
  // Create a silent audio file as placeholder
  try {
    execSync(`ffmpeg -y -f lavfi -i anullsrc=r=44100:cl=stereo -t ${startTime} -b:a 128k "${outputFile}"`, { stdio: 'pipe' });
    console.log(`Silent placeholder: ${outputFile}`);
  } catch (e2) {
    console.warn('FFmpeg not available either. Create audio manually.');
  }
}
