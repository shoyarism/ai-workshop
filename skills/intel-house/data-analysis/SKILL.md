---
name: data-analysis
description: "Use when the user wants to analyze data from spreadsheets, databases, or APIs. Covers statistical analysis, data cleaning, pivot tables, trend analysis, correlation detection, forecasting, and visualization. Also use when the user mentions 'analyze this data', 'data analysis', 'statistical analysis', 'find trends', 'correlation', 'forecast', 'pivot table', or 'data insights'. Supports .xlsx, .csv, .json, SQL databases, and API data sources."
argument-hint: "[data_source] [analysis_type] [output_format]"
metadata:
  category: office-productivity
  tools: pandas, numpy, scipy, statsmodels, sklearn
---

# Data Analysis Skill

## Triggers
- "Analyze this data..."
- "Find trends in..."
- "Statistical analysis of..."
- "Correlation between..."
- "Forecast next quarter..."
- "Pivot table for..."
- "Data cleaning..."
- "Identify outliers..."

## Analysis Types

| Analysis Type | Use Case | Tools |
|--------------|----------|-------|
| Descriptive | Summarize data | mean, median, std, count |
| Diagnostic | Find causes | correlation, segmentation |
| Predictive | Forecast future | regression, ML models |
| Prescriptive | Recommend actions | optimization, simulation |

## Implementation: Python Data Analyzer

```python
import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DataAnalyzer:
    def __init__(self, data_source, data_type='auto'):
        """
        Initialize analyzer with data source
        data_source: path to file, DataFrame, or SQL query
        data_type: 'csv', 'xlsx', 'json', 'sql', 'auto'
        """
        self.df = self._load_data(data_source, data_type)
        self.original_df = self.df.copy()
        self.analysis_results = {}
    
    def _load_data(self, source, data_type):
        """Load data from various sources"""
        if isinstance(source, pd.DataFrame):
            return source
        
        if data_type == 'auto':
            if isinstance(source, str):
                if source.endswith('.csv'):
                    return pd.read_csv(source)
                elif source.endswith('.xlsx'):
                    return pd.read_excel(source)
                elif source.endswith('.json'):
                    return pd.read_json(source)
                elif source.startswith('SELECT') or source.startswith('select'):
                    # SQL query - would need connection string
                    return pd.read_sql(source, self._get_connection())
        
        return pd.read_csv(source) if data_type == 'csv' else pd.read_excel(source)
    
    def summary(self):
        """Generate comprehensive data summary"""
        summary = {
            'rows': len(self.df),
            'columns': len(self.df.columns),
            'column_names': list(self.df.columns),
            'dtypes': self.df.dtypes.to_dict(),
            'missing_values': self.df.isnull().sum().to_dict(),
            'missing_pct': (self.df.isnull().sum() / len(self.df) * 100).round(2).to_dict(),
            'memory_usage_mb': round(self.df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
        }
        
        # Numeric columns
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            summary['numeric_summary'] = self.df[numeric_cols].describe().to_dict()
        
        # Categorical columns
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            summary['categorical_summary'] = {}
            for col in categorical_cols:
                summary['categorical_summary'][col] = {
                    'unique_count': self.df[col].nunique(),
                    'top_values': self.df[col].value_counts().head(5).to_dict()
                }
        
        self.analysis_results['summary'] = summary
        return summary
    
    def clean(self, strategies=None):
        """Clean data with configurable strategies"""
        if strategies is None:
            strategies = {
                'missing_numeric': 'median',
                'missing_categorical': 'mode',
                'duplicates': 'drop',
                'outliers': 'iqr',
                'whitespace': 'strip',
            }
        
        cleaned_df = self.df.copy()
        changes = []
        
        # Handle missing values
        for col in cleaned_df.columns:
            missing = cleaned_df[col].isnull().sum()
            if missing > 0:
                if strategies.get('missing_numeric') == 'median' and cleaned_df[col].dtype in [np.float64, np.int64]:
                    cleaned_df[col].fillna(cleaned_df[col].median(), inplace=True)
                    changes.append(f'Filled {missing} missing values in {col} with median')
                elif strategies.get('missing_categorical') == 'mode' and cleaned_df[col].dtype == 'object':
                    cleaned_df[col].fillna(cleaned_df[col].mode()[0], inplace=True)
                    changes.append(f'Filled {missing} missing values in {col} with mode')
        
        # Drop duplicates
        if strategies.get('duplicates') == 'drop':
            dupes = cleaned_df.duplicated().sum()
            if dupes > 0:
                cleaned_df.drop_duplicates(inplace=True)
                changes.append(f'Dropped {dupes} duplicate rows')
        
        # Handle outliers
        if strategies.get('outliers') == 'iqr':
            for col in cleaned_df.select_dtypes(include=[np.number]).columns:
                Q1 = cleaned_df[col].quantile(0.25)
                Q3 = cleaned_df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR
                outliers = ((cleaned_df[col] < lower) | (cleaned_df[col] > upper)).sum()
                if outliers > 0:
                    cleaned_df[col] = cleaned_df[col].clip(lower, upper)
                    changes.append(f'Winsorized {outliers} outliers in {col}')
        
        # Strip whitespace from strings
        if strategies.get('whitespace') == 'strip':
            for col in cleaned_df.select_dtypes(include=['object']).columns:
                cleaned_df[col] = cleaned_df[col].str.strip()
        
        self.df = cleaned_df
        self.analysis_results['cleaning'] = changes
        return changes
    
    def correlate(self, method='pearson', top_n=10):
        """Find correlations between numeric columns"""
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if numeric_df.shape[1] < 2:
            return {'message': 'Need at least 2 numeric columns for correlation'}
        
        corr_matrix = numeric_df.corr(method=method)
        
        # Find top correlations
        correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr = corr_matrix.iloc[i, j]
                correlations.append({
                    'column1': corr_matrix.columns[i],
                    'column2': corr_matrix.columns[j],
                    'correlation': round(corr, 4),
                    'r_squared': round(corr**2, 4)
                })
        
        correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)
        
        self.analysis_results['correlations'] = {
            'top_correlations': correlations[:top_n],
            'all_correlations': correlations,
            'matrix': corr_matrix.to_dict()
        }
        return self.analysis_results['correlations']['top_correlations']
    
    def segment(self, column, agg_columns=None, agg_funcs='mean'):
        """Segment data by a column and aggregate"""
        if agg_columns is None:
            agg_columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        agg_dict = {col: agg_funcs for col in agg_columns if col in self.df.columns}
        
        if agg_dict:
            segments = self.df.groupby(column).agg(agg_dict).round(2)
        else:
            segments = self.df.groupby(column).size().reset_index(name='count')
        
        self.analysis_results['segments'] = segments
        return segments
    
    def forecast(self, target_column, periods=5, method='linear'):
        """Simple time series forecasting"""
        if not pd.api.types.is_datetime64_any_dtype(self.df.index):
            self.df.index = pd.to_datetime(self.df.index)
        
        target = self.df[target_column].dropna()
        
        if method == 'linear':
            # Linear regression forecast
            x = np.arange(len(target))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, target.values)
            
            forecast_values = [intercept + slope * (len(target) + i) for i in range(periods)]
            
            return {
                'forecast': forecast_values,
                'r_squared': round(r_value**2, 4),
                'trend': 'increasing' if slope > 0 else 'decreasing',
                'slope': round(slope, 4)
            }
        
        elif method == 'moving_average':
            window = min(5, len(target) // 2)
            forecast = [target.iloc[-window:].mean()] * periods
            return {'forecast': [round(v, 2) for v in forecast], 'method': 'moving_average'}
        
        elif method == 'exponential':
            alpha = 0.3
            forecast = [target.iloc[-1]]
            for _ in range(periods - 1):
                forecast.append(forecast[-1] * alpha + forecast[-1] * (1 - alpha))
            return {'forecast': [round(v, 2) for v in forecast], 'method': 'exponential'}
    
    def pivot(self, rows, cols, values, aggfunc='sum'):
        """Create pivot table"""
        pivot = pd.pivot_table(
            self.df,
            values=values,
            index=rows,
            columns=cols,
            aggfunc=aggfunc,
            fill_value=0,
            margins=True
        )
        self.analysis_results['pivot'] = pivot
        return pivot
    
    def find_anomalies(self, column, method='zscore', threshold=3):
        """Find anomalous values"""
        if method == 'zscore':
            z_scores = np.abs(stats.zscore(self.df[column].dropna()))
            anomalies = self.df[np.abs(stats.zscore(self.df[column])) > threshold]
        elif method == 'iqr':
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            anomalies = self.df[(self.df[column] < Q1 - 1.5*IQR) | (self.df[column] > Q3 + 1.5*IQR)]
        
        self.analysis_results['anomalies'] = {
            'column': column,
            'method': method,
            'count': len(anomalies),
            'anomalies': anomalies.head(20)
        }
        return self.analysis_results['anomalies']
    
    def report(self, output_path=None):
        """Generate analysis report"""
        report = {
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_source': str(self.original_df),
            'summary': self.summary(),
            'cleaning': self.analysis_results.get('cleaning', []),
            'correlations': self.analysis_results.get('correlations', {}).get('top_correlations', []),
            'anomalies': self.analysis_results.get('anomalies', {}),
        }
        
        if output_path:
            import json
            # Convert any numpy types to Python native types
            def convert(obj):
                if isinstance(obj, (np.integer,)):
                    return int(obj)
                elif isinstance(obj, (np.floating,)):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, pd.DataFrame):
                    return obj.to_dict()
                return obj
            
            report_json = json.dumps(report, default=convert, indent=2)
            with open(output_path, 'w') as f:
                f.write(report_json)
            return output_path
        
        return report
```

## Common Analysis Workflows

### Workflow: Exploratory Data Analysis (EDA)
1. Load data from source
2. Run summary statistics
3. Check for missing values and outliers
4. Clean data (impute, drop, transform)
5. Explore correlations and patterns
6. Generate visualizations
7. Export findings

### Workflow: Sales Analysis
1. Load sales data (by region, product, time)
2. Calculate key metrics (revenue, growth, margin)
3. Segment by dimensions (region, product, customer)
4. Identify top performers and underperformers
5. Forecast future sales
6. Generate actionable insights

### Workflow: Customer Analysis
1. Load customer data
2. Segment customers (RFM analysis)
3. Calculate lifetime value
4. Identify churn risks
5. Forecast retention
6. Recommend actions

### Workflow: Financial Analysis
1. Load financial data
2. Calculate ratios (profitability, liquidity, leverage)
3. Trend analysis over time
4. Benchmark against industry
5. Forecast financials
6. Generate investment recommendations

## Key Metrics to Calculate

### Descriptive Statistics
- Count, mean, median, mode
- Standard deviation, variance
- Min, max, range
- Quartiles, percentiles

### Correlation Analysis
- Pearson correlation (linear)
- Spearman correlation (rank)
- Covariance matrix

### Time Series
- Moving averages
- Exponential smoothing
- Trend detection
- Seasonality decomposition

### Segmentation
- RFM (Recency, Frequency, Monetary)
- Customer clustering
- Performance grouping

## Integration with Other Skills
- `excel-master` — export analysis to Excel
- `xlsx` — read/write Excel files
- `chart-generator` — visualize analysis results
- `pdf` — export reports as PDF
- `data-analysis` — for advanced statistical methods
