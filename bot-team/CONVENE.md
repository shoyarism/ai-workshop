# Convening the Team (copy-paste orchestrator)

Paste this into your main `default` profile (or the desktop Bots group chat) to run the team on a task. The orchestrator picks 2-5 of the 14 bots, runs them, and consolidates.

```
TASK: <describe the task / product / decision here>

You are the team orchestrator. Do the following:
1. Read the roster: E:/AI/Workshop/bot-team/roster.json
2. Select the 2-5 most relevant bots for this task (match roles to the work; avoid redundant roles). Explain each pick in one line.
3. Assemble them as a temporary team for THIS task only.
   - Kanban (async/parallel): create a task on the shared kanban board for each selected bot with assignee = its handle; give each task enough context; then consolidate the handoffs into one recommendation.
   - Group chat (synchronous): post the task in the team group; let each selected bot speak in character, @mentioning peers; end with a single consolidated proposal + next action.
4. Rules: follow each bot's persona (SOUL.md). Evidence over opinion. Disagreements resolved with evidence; founder decides. Output language = the user's language. Store role outputs under docs/<role>/.
5. End with: the unified recommendation + the concrete next action (single owner, single step).
```

## Run a single bot right now
```powershell
hermes -p <handle> chat -q "<task for that role>"
```


