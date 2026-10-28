---
name: discord-bot-architect
description: Specialized skill for building production-ready Discord bots.
  Covers Discord.js (JavaScript) and Pycord (Python), gateway intents, slash
  commands, interactive components, rate limiting, and sharding.
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Discord Bot Architect

Specialized skill for building production-ready Discord bots.
Covers Discord.js (JavaScript) and Pycord (Python), gateway intents,
slash commands, interactive components, rate limiting, and sharding.

## Principles

- Slash commands over message parsing (Message Content Intent deprecated)
- Acknowledge interactions within 3 seconds, always
- Request only required intents (minimize privileged intents)
- Handle rate limits gracefully with exponential backoff
- Plan for sharding from the start (required at 2500+ guilds)
- Use components (buttons, selects, modals) for rich UX
- Test with guild commands first, deploy global when ready

## Patterns

### Discord.js v14 Foundation

Modern Discord bot setup with Discord.js v14 and slash commands

**When to use**: Building Discord bots with JavaScript/TypeScript,Need full gateway connection with events,Building bots with complex interactions

```javascript
// src/index.js
const { Client, Collection, GatewayIntentBits, Events } = require('discord.js');
const fs = require('node:fs');
const path = require('node:path');
require('dotenv').config();

// Create client with minimal required intents
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    // Add only what you need:
    // GatewayIntentBits.GuildMessages,
    // GatewayIntentBits.MessageContent,  // PRIVILEGED - avoid if possible
  ]
});

// Load commands
client.commands = new Collection();
const commandsPath = path.join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath).filter(f => f.endsWith('.js'));

for (const file of commandFiles) {