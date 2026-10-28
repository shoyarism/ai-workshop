---
name: azure-functions
description: Expert patterns for Azure Functions development including isolated
  worker model, Durable Functions orchestration, cold start optimization, and
  production patterns. Covers .NET, Python, and Node.js programming models.
risk: none
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Azure Functions

Expert patterns for Azure Functions development including isolated worker model,
Durable Functions orchestration, cold start optimization, and production patterns.
Covers .NET, Python, and Node.js programming models.

## Patterns

### Isolated Worker Model (.NET)

Modern .NET execution model with process isolation

**When to use**: Building new .NET Azure Functions apps

### Template

// Program.cs - Isolated Worker Model
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var host = new HostBuilder()
    .ConfigureFunctionsWorkerDefaults()
    .ConfigureServices(services =>
    {
        // Add Application Insights
        services.AddApplicationInsightsTelemetryWorkerService();
        services.ConfigureFunctionsApplicationInsights();

        // Add HttpClientFactory (prevents socket exhaustion)
        services.AddHttpClient();

        // Add your services
        services.AddSingleton<IMyService, MyService>();
    })
    .Build();

host.Run();

// HttpTriggerFunction.cs
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Http;
using Microsoft.Extensions.Logging;

public class HttpTriggerFunction
{
    private readonly ILogger<HttpTriggerFunction> _logger;
    private readonly IMyService _service;

    public HttpTriggerFunction(
        ILogger<HttpTriggerFunction> logger,
        IMyService service)
    {
        _logger = logger;
        _service = service;
    }

    [Function("HttpTrigger")]
    public async Task<HttpResponseData> Run(