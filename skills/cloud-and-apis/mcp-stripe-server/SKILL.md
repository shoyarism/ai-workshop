---
name: mcp-stripe-server
description: Build an MCP (Model Context Protocol) server for Stripe — payment intents, customers, subscriptions, invoices, checkout sessions, and webhook handling. Use when the user wants to expose Stripe payment operations to AI agents via a standardized MCP interface. Triggers on: mcp, model context protocol, stripe, payments, payment intents, subscriptions, invoices, checkout, webhook, mcp server, payment processing.
---

# MCP Stripe Server

Build a Model Context Protocol server that exposes Stripe payment operations to AI agents. Agents can create payment intents, manage customers, handle subscriptions, generate invoices, and process webhooks through a standardized tool interface.

## When to trigger

- User wants AI agents to create or manage Stripe payments
- User needs to expose billing operations via MCP to Claude Code, Cursor, or other MCP clients
- User is building a Stripe-integrated agent workflow (subscriptions, invoices, checkout)
- User wants secure, tool-based access to Stripe API instead of raw API calls

## Prerequisites

```bash
pip install mcp stripe python-dotenv
```

Environment variables:

```bash
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

## Basic MCP server structure

```python
# stripe_mcp_server.py
import os
import stripe
from mcp.server.fastmcp import FastMCP

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
mcp = FastMCP("stripe-server")

@mcp.tool()
def create_payment_intent(amount: int, currency: str = "usd", customer_id: str | None = None):
    """Create a Stripe PaymentIntent for collecting payment."""
    params = {
        "amount": amount,
        "currency": currency,
        "automatic_payment_methods": {"enabled": True}
    }
    if customer_id:
        params["customer"] = customer_id
    intent = stripe.PaymentIntent.create(**params)
    return {
        "id": intent.id,
        "client_secret": intent.client_secret,
        "status": intent.status,
        "amount": intent.amount
    }

@mcp.tool()
def create_customer(email: str, name: str | None = None, phone: str | None = None):
    """Create a Stripe Customer."""
    params = {"email": email}
    if name:
        params["name"] = name
    if phone:
        params["phone"] = phone
    customer = stripe.Customer.create(**params)
    return {
        "id": customer.id,
        "email": customer.email,
        "name": customer.name
    }

@mcp.tool()
def get_customer(customer_id: str):
    """Retrieve a Stripe Customer by ID."""
    customer = stripe.Customer.retrieve(customer_id)
    return {
        "id": customer.id,
        "email": customer.email,
        "name": customer.name,
        "created": customer.created
    }

@mcp.tool()
def create_subscription(customer_id: str, price_id: str, trial_period_days: int | None = None):
    """Create a Stripe Subscription for a customer."""
    params = {
        "customer": customer_id,
        "items": [{"price": price_id}],
        "payment_behavior": "default_incomplete",
        "expand": ["latest_invoice.payment_intent"]
    }
    if trial_period_days:
        params["trial_period_days"] = trial_period_days
    subscription = stripe.Subscription.create(**params)
    return {
        "id": subscription.id,
        "status": subscription.status,
        "customer": subscription.customer,
        "current_period_start": subscription.current_period_start,
        "current_period_end": subscription.current_period_end
    }

@mcp.tool()
def create_invoice(customer_id: str, auto_advance: bool = True):
    """Create a Stripe Invoice for a customer."""
    invoice = stripe.Invoice.create(
        customer=customer_id,
        auto_advance=auto_advance
    )
    return {
        "id": invoice.id,
        "status": invoice.status,
        "customer": invoice.customer,
        "amount_due": invoice.amount_due
    }

@mcp.tool()
def finalize_invoice(invoice_id: str):
    """Finalize a Stripe Invoice."""
    invoice = stripe.Invoice.finalize_invoice(invoice_id)
    return {
        "id": invoice.id,
        "status": invoice.status,
        "amount_paid": invoice.amount_paid
    }

@mcp.tool()
def create_checkout_session(price_id: str, success_url: str, cancel_url: str, customer_email: str | None = None):
    """Create a Stripe Checkout Session for one-time payments."""
    params = {
        "mode": "payment",
        "line_items": [{"price": price_id, "quantity": 1}],
        "success_url": success_url,
        "cancel_url": cancel_url
    }
    if customer_email:
        params["customer_email"] = customer_email
    session = stripe.checkout.Session.create(**params)
    return {
        "id": session.id,
        "url": session.url,
        "payment_status": session.payment_status
    }

if __name__ == "__main__":
    mcp.run()
```

## MCP client configuration

Add to your MCP client config (e.g., `.mcp.json` or OpenCode `opencode.json`):

```json
{
  "mcpServers": {
    "stripe": {
      "command": "python",
      "args": ["/path/to/stripe_mcp_server.py"],
      "env": {
        "STRIPE_SECRET_KEY": "sk_test_...",
        "STRIPE_WEBHOOK_SECRET": "whsec_..."
      }
    }
  }
}
```

## Webhook handling (separate endpoint)

Stripe webhooks require an HTTP endpoint, separate from the stdio MCP server. Use FastAPI or similar:

```python
# webhook_handler.py
from fastapi import FastAPI, Request, HTTPException
import stripe
import os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
app = FastAPI()

@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        raise HTTPException(status_code=400)
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400)

    if event.type == "payment_intent.succeeded":
        intent = event.data.object
        print(f"Payment succeeded: {intent.id}")
    elif event.type == "customer.subscription.created":
        sub = event.data.object
        print(f"Subscription created: {sub.id}")
    return {"status": "received"}
```

## Security practices

- Never log `client_secret` or full card details
- Use `sk_test_` keys in development; `sk_live_` only in production
- Verify webhook signatures with `STRIPE_WEBHOOK_SECRET`
- Scope API keys with minimal required permissions

## Related Workshop skills

- `mcp-resend-email` — email MCP server companion
- `mcp-linear-server` — project management MCP server (planned)
- `mcp-builder` — general MCP server authoring patterns
- `mcp-server-patterns` — MCP design patterns and best practices
