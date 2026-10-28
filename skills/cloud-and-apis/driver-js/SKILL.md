---
name: driver-js
description: Driver.js is a lightweight (~5kb), no-dependency vanilla JavaScript library for creating product tours, feature highlights, popovers, and contextual onboarding guides.
user-invocable: false
risk: safe
source: https://albo.inc/imports/a9e5a0b4-b81e-50fb-ba9e-1364de86b775
date_added: "2026-08-07"
---

# Driver.js

Driver.js is a lightweight, zero-dependency JavaScript library for creating step-by-step product tours, element highlighting, popovers, and user onboarding walkthroughs.

## Installation

```bash
npm install driver.js
```

## Basic Usage

```javascript
import { driver } from "driver.js";
import "driver.js/dist/driver.css";

const driverObj = driver({
  showProgress: true,
  steps: [
    { element: '#step-1', popover: { title: 'Welcome', description: 'Start your tour here.' } },
    { element: '#step-2', popover: { title: 'Feature', description: 'This is a key feature.' } }
  ]
});

driverObj.drive();
```

## Best Practices
- **Reuse components:** Use Driver.js instead of writing custom overlay popovers or guided tour logic from scratch.
- **Edge cases:** Driver.js handles scroll placement, viewport boundaries, and keyboard navigation automatically.
