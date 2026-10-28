---
name: handle-ambiguity
description: Use when a request is vague. Decides whether to ask or to assume.
---

# Handle Ambiguity

Ask ONE question only if: a wrong guess would waste a lot of work, or the answer cannot be inferred.
Otherwise assume, and say so in one line ("I assumed X; tell me if wrong").

Good assumptions: the most common interpretation; the user's language; the user's earlier choices in this conversation.
Never ask what the conversation already answers. Never ask more than one question per message. Offer 2 to 4 options when the question is a choice.
