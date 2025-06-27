[![Upload Python Package](https://github.com/5bhuv4n35h/telegram_analysis/actions/workflows/python-publish.yml/badge.svg)](https://github.com/5bhuv4n35h/telegram_analysis/actions/workflows/python-publish.yml)
# Telegram Analyzer

A Python toolkit for analyzing and visualizing Telegram chat exports.

## Features

- Process Telegram export JSON files
- Analyze chat statistics (message count, activity patterns, user behavior)
- Generate visual representations of chat data
- Create HTML reports with analysis results
- Extract sentiment and content metrics

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/telegram-analyzer.git
cd telegram-analyzer

# Install the package
pip install -e .
```

## Usage

### Command Line

```bash
telegram-analyzer path/to/export.json --output-dir analysis_results
```

### As a Library

```python
from telegram_analyzer.parser import TelegramDataParser
from telegram_analyzer.analyzer import ChatAnalyzer
from telegram_analyzer.visualizer import Visualizer
from telegram_analyzer.report import ReportGenerator

# Parse data
parser = TelegramDataParser('path/to/export.json')
messages_df = parser.process_messages()

# Analyze data
analyzer = ChatAnalyzer(messages_df)
stats = analyzer.get_all_stats()

# Generate visualizations
visualizer = Visualizer(messages_df, 'output_directory')
visualizer.generate_all_visualizations()

# Generate report
report_gen = ReportGenerator(stats, 'output_directory')
report_gen.generate_html_report()
```

## Requirements

- Python 3.7+
- pandas
- matplotlib
- seaborn
- nltk
- wordcloud
- emoji
- textblob
- plotly
- networkx
- tqdm
- pillow

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
