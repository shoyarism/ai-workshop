---
name: chart-generator
description: "Use when the user wants to create data visualizations, charts, graphs, and infographics. Covers bar charts, line charts, pie charts, scatter plots, heatmaps, pivot tables, dashboard creation, and export to multiple formats. Also use when the user mentions 'chart', 'graph', 'visualization', 'plot', 'dashboard', 'infographic', 'data viz', or 'create a chart'. Supports PNG, SVG, PDF, and interactive HTML output."
argument-hint: "[chart_type] [data_source] [output_format]"
metadata:
  category: office-productivity
  tools: matplotlib, plotly, seaborn, altair, chart.js, excel-master
---

# Chart Generator Skill

## Triggers
- "Create a chart showing..."
- "Generate a visualization of..."
- "Make a graph for..."
- "Create a dashboard..."
- "Plot this data..."
- "Chart type for..."
- "Infographic for..."
- "Data visualization..."

## Chart Selection Guide

| Data Type | Best Chart | Use Case |
|-----------|-----------|----------|
| Comparison | Bar chart | Compare categories |
| Trend over time | Line chart | Time series data |
| Part-to-whole | Pie/Donut chart | Proportions (%) |
| Correlation | Scatter plot | Two variables relationship |
| Distribution | Histogram | Data frequency distribution |
| Multi-variable | Heatmap | Matrix of values |
| Geographic | Map/Choropleth | Regional data |
| Flow | Sankey diagram | Process flow |
| Performance | Gauge/Speedometer | KPI tracking |
| Hierarchy | Tree map | Nested categories |

## Implementation: Python Chart Generator

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class ChartGenerator:
    def __init__(self, title="Chart"):
        self.title = title
        self.fig = None
    
    def bar_chart(self, categories, values, title=None, colors=None, 
                  horizontal=False, show_values=True):
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if horizontal:
            bars = ax.barh(categories, values, color=colors or plt.cm.viridis(np.linspace(0,1,len(categories))))
            ax.set_xlabel('Value')
        else:
            bars = ax.bar(categories, values, color=colors or plt.cm.viridis(np.linspace(0,1,len(categories))))
            ax.set_ylabel('Value')
            plt.xticks(rotation=45, ha='right')
        
        if title:
            ax.set_title(title, fontsize=14, fontweight='bold')
        elif self.title:
            ax.set_title(self.title, fontsize=14, fontweight='bold')
        
        if show_values:
            for bar, val in zip(bars, values):
                height = bar.get_height() if not horizontal else bar.get_width()
                xy = (bar.get_x() + bar.get_width()/2, height) if not horizontal else (height, bar.get_y() + bar.get_height()/2)
                ax.annotate(f'{val:.1f}', xy=xy, xytext=(0, 3) if not horizontal else (3, 0),
                           textcoords="offset points", ha='center' if not horizontal else 'left', va='bottom')
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        return fig, ax
    
    def line_chart(self, x_data, y_data, labels=None, title=None, 
                   markers=False, multi_series=None):
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if multi_series:
            for label, y in multi_series.items():
                ax.plot(x_data, y, label=label, marker='o' if markers else None, linewidth=2)
            ax.legend()
        else:
            ax.plot(x_data, y_data, marker='o' if markers else None, linewidth=2)
            if labels and len(labels) == len(x_data):
                for x, y in zip(x_data, y_data):
                    ax.annotate(f'{y:.1f}', (x, y), textcoords="offset points", xytext=(0,10), ha='center')
        
        if title:
            ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('X Axis' if not isinstance(x_data[0], datetime) else 'Date')
        ax.set_ylabel('Y Axis')
        
        if isinstance(x_data[0], datetime):
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_major_locator(mdates.WeekdayLocator())
            plt.xticks(rotation=45)
        
        ax.grid(True, alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        return fig, ax
    
    def pie_chart(self, values, labels, title=None, explode=None, 
                  autopct='%1.1f%%', colors=None):
        fig, ax = plt.subplots(figsize=(8, 8))
        
        wedges, texts, autotexts = ax.pie(values, labels=labels, explode=explode or [0]*len(values),
                                          autopct=autopct, colors=colors or plt.cm.tab10.colors,
                                          startangle=90)
        
        for autotext in autotexts:
            autotext.set_fontsize(12)
            autotext.set_fontweight('bold')
        
        if title:
            ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        ax.axis('equal')
        return fig, ax
    
    def scatter_plot(self, x_data, y_data, labels=None, title=None, 
                     sizes=None, colors=None, trend_line=False):
        fig, ax = plt.subplots(figsize=(10, 8))
        
        scatter = ax.scatter(x_data, y_data, s=sizes or 80, c=colors or plt.cm.viridis(np.linspace(0,1,len(x_data))),
                            alpha=0.7, edgecolors='white', linewidth=1)
        
        if trend_line:
            z = np.polyfit(x_data, y_data, 1)
            p = np.poly1d(z)
            ax.plot(sorted(x_data), p(sorted(x_data)), "r--", alpha=0.6, label='Trend Line')
        
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Value')
        
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        if title:
            ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        return fig, ax
    
    def heatmap(self, data, labels=None, title=None, cmap='RdYlBu_r'):
        fig, ax = plt.subplots(figsize=(10, 8))
        
        im = ax.imshow(data, cmap=cmap, aspect='auto')
        
        if labels:
            ax.set_xticks(range(len(labels[0])))
            ax.set_yticks(range(len(labels)))
            ax.set_xticklabels(labels[0], rotation=45, ha='right')
            ax.set_yticklabels(labels)
        
        plt.colorbar(im, ax=ax, label='Value')
        
        for i in range(len(data)):
            for j in range(len(data[0])):
                text = ax.text(j, i, f'{data[i][j]:.1f}', ha='center', va='center', 
                              color="white" if abs(data[i][j]) > np.max(np.abs(data))/2 else "black")
        
        if title:
            ax.set_title(title, fontsize=14, fontweight='bold')
        return fig, ax
    
    def interactive_plotly(self, x_data, y_data, chart_type='bar', title=None):
        if chart_type == 'bar':
            fig = go.Figure(data=[go.Bar(x=x_data, y=y_data, marker_color='steelblue')])
        elif chart_type == 'line':
            fig = go.Figure(data=[go.Scatter(x=x_data, y=y_data, mode='lines+markers')])
        elif chart_type == 'pie':
            fig = go.Figure(data=[go.Pie(labels=x_data, values=y_data)])
        elif chart_type == 'scatter':
            fig = go.Figure(data=[go.Scatter(x=x_data, y=y_data, mode='markers')])
        
        if title:
            fig.update_layout(title=title, showlegend=True)
        return fig
    
    def save(self, fig, path, dpi=150):
        fig.savefig(path, dpi=dpi, bbox_inches='tight', facecolor='white')
        plt.close(fig)
        return path
    
    def export_html_dashboard(self, charts_config, output_path):
        """Export interactive charts as HTML dashboard"""
        import plotly.io as pio
        html_parts = ['<html><head><title>Dashboard</title><style>']
        html_parts.append('.chart-container { display: inline-block; margin: 20px; }')
        html_parts.append('.chart { width: 500px; height: 400px; }')
        html_parts.append('</style></head><body>')
        
        for chart in charts_config:
            fig = self.interactive_plotly(chart['x'], chart['y'], chart['type'], chart.get('title'))
            html_parts.append(f'<div class="chart-container"><h3>{chart.get("title", "Chart")}</h3>')
            html_parts.append(pio.to_html(fig, full_html=False, include_plotlyjs='cdn'))
            html_parts.append('</div>')
        
        html_parts.append('</body></html>')
        
        with open(output_path, 'w') as f:
            f.write('\n'.join(html_parts))
        return output_path
```

## Common Workflows

### Workflow: Business Report Charts
1. Collect data from source (Excel, database, API)
2. Select appropriate chart types for each metric
3. Generate static PNG/PDF for reports
4. Generate interactive HTML for web dashboards
5. Apply consistent styling/theme

### Workflow: Data Exploration
1. Load dataset
2. Generate multiple chart types for quick exploration
3. Identify patterns, outliers, correlations
4. Export best visualizations for presentation

### Workflow: Executive Dashboard
1. Define KPIs and metrics
2. Create gauge charts for target vs actual
3. Create trend charts for time-series data
4. Create bar charts for comparison metrics
5. Combine into interactive HTML dashboard

## Chart Types by Business Use Case

### Financial
- Revenue trend (line chart)
- Profit margin by quarter (bar chart)
- Expense breakdown (pie chart)
- Budget vs actual (grouped bar)
- Cash flow waterfall (waterfall chart)

### Sales
- Sales by region (map/choropleth)
- Sales pipeline (funnel chart)
- Conversion rates (stacked bar)
- Customer acquisition cost (bar chart)
- Monthly recurring revenue (line chart)

### Marketing
- Campaign performance (bar chart)
- Social media engagement (line chart)
- Funnel conversion (funnel chart)
- A/B test results (bar chart with significance)
- Content performance (table with highlights)

### Operations
- Throughput/timeline (Gantt chart)
- Resource utilization (heatmap)
- Defect rate (control chart)
- Cycle time distribution (histogram)
- Bottleneck identification (Sankey)

## Integration with Other Skills
- `excel-master` — create charts directly in Excel files
- `xlsx` — generate charts in spreadsheet files
- `pptx` — embed charts in presentations
- `docx` — include charts in Word documents
- `pdf` — export charts as PDF
- `chart-generator` — for advanced/custom chart types
