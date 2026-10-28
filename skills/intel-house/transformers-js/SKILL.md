---
source: "https://github.com/huggingface/skills/tree/main/skills/transformers-js"
name: transformers-js
description: Run Hugging Face models in JavaScript or TypeScript with Transformers.js in Node.js or the browser.
license: Apache-2.0
risk: unknown
metadata:
  author: huggingface
  version: "3.8.1"
  category: machine-learning
  repository: https://github.com/huggingface/transformers.js
compatibility: Requires Node.js 18+ or modern browser with ES modules support. WebGPU support requires compatible browser/environment. Internet access needed for downloading models from Hugging Face Hub (optional if using local models).
---

# Transformers.js - Machine Learning for JavaScript

Transformers.js enables running state-of-the-art machine learning models directly in JavaScript, both in browsers and Node.js environments, with no server required.

## When to Use This Skill

Use this skill when you need to:
- Run ML models for text analysis, generation, or translation in JavaScript
- Perform image classification, object detection, or segmentation
- Implement speech recognition or audio processing
- Build multimodal AI applications (text-to-image, image-to-text, etc.)
- Run models client-side in the browser without a backend

## Installation

### NPM Installation
```bash
npm install @huggingface/transformers
```

### Browser Usage (CDN)
```javascript