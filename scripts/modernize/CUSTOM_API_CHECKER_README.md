# PyPylon Custom API Compatibility Checker

A comprehensive, custom-built API compatibility checking system specifically designed for pypylon. This system replaces pidiff with a solution that's more reliable and tailored to pypylon's specific needs. Uses **uv** for environment management to ensure consistent Python versions.

## 🎯 Overview

This toolkit provides three main components:

1. **pypylon_api_dumper.py** - Extracts comprehensive API information from pypylon installations
2. **pypylon_api_differ.py** - Compares two API dumps and identifies all differences
3. **pypylon_compatibility_checker.py** - Main orchestrator that manages the entire workflow using uv

## 🚀 Quick Start

### Basic Usage

```bash
# Quick compatibility check against latest PyPI version (both using Python 3.14)
python pypylon_compatibility_checker.py --quick-check

# Full check with HTML report
python pypylon_compatibility_checker.py --full-check

# Compare with specific pypylon version
python pypylon_compatibility_checker.py --full-check --pypylon-version 4.0.0

# Use different Python version
python pypylon_compatibility_checker.py --quick-check --python-version 3.11
```

### Creating API Dumps

```bash
# Create API dump from current environment
python pypylon_api_dumper.py --output current_api.json

# Create API dump from specific Python environment
python pypylon_api_dumper.py --python-env ~/.pyenv/versions/3.11.0/bin/python --output reference_api.json

# Create compressed API dump
python pypylon_api_dumper.py --output api_dump.json --compress
```

### Comparing API Dumps

```bash
# Compare two API dumps with HTML report
python pypylon_api_differ.py reference_api.json current_api.json --output report.html

# Generate text-only report
python pypylon_api_differ.py old_api.json new_api.json --text-only

# Compare and save to specific file
python pypylon_api_differ.py ref.json cur.json --output compatibility_report.txt --text-only
```

## 📋 Features

### Comprehensive API Analysis

The system analyzes every aspect of the pypylon API:

- **Modules**: All public modules and submodules
- **Classes**: Complete class hierarchies, inheritance, abstract classes
- **Functions**: All public functions with full signatures
- **Methods**: Instance, class, and static methods
- **Properties**: Getters, setters, and deleters
- **Documentation**: Docstrings, parameter docs, return docs
- **Type Annotations**: Parameter types, return types
- **Constants**: Module-level constants and variables

### Detailed Difference Detection

The differ identifies changes in:

- **API Structure**: Added/removed modules, classes, functions
- **Function Signatures**: Parameter changes, defaults, types
- **Documentation**: Changed docstrings, parameter descriptions
- **Inheritance**: Base class changes, MRO modifications
- **Properties**: Getter/setter availability changes
- **Type Annotations**: Type hint modifications

### Severity Classification

All differences are classified by severity:

- **Major**: Breaking changes (signature changes, removed APIs)
- **Minor**: Non-breaking changes (new APIs, enhanced docs)
- **Patch**: Cosmetic changes (docstring formatting, etc.)

### Rich Reporting

Multiple output formats are supported:

- **HTML Reports**: Beautiful, interactive reports with filtering and search
- **Text Reports**: Command-line friendly text output
- **JSON Data**: Machine-readable API dumps for programmatic use

### Environment Management with uv

The system uses **uv** for reliable environment management:

- **Consistent Python versions**: Both environments use the same Python version (default: 3.14)
- **Isolated environments**: Clean, isolated environments for each comparison
- **Fast installation**: uv provides fast package installation
- **Reliable dependency resolution**: No conflicts between environments

## 🔧 Detailed Usage

### API Dumper (`pypylon_api_dumper.py`)

#### Basic Usage
```bash
python pypylon_api_dumper.py --output pypylon_api.json
```

#### Options
- `--python-env PATH`: Python executable to use for extraction
- `--output FILE`: Output JSON file path (default: timestamped)
- `--compress`: Compress output with gzip
- `--verbose`: Enable detailed output

#### Examples
```bash
# Extract from current environment
python pypylon_api_dumper.py --output current_pypylon.json

# Extract from specific Python installation
python pypylon_api_dumper.py --python-env /usr/bin/python3.11 --output pypylon_3.11.json

# Extract with compression
python pypylon_api_dumper.py --output pypylon_api.json --compress

# Extract to timestamped file (automatic naming)
python pypylon_api_dumper.py
```

### API Differ (`pypylon_api_differ.py`)

#### Basic Usage
```bash
python pypylon_api_differ.py reference.json current.json --output report.html
```

#### Options
- `reference`: Reference API dump file (JSON)
- `current`: Current API dump file (JSON)
- `--output FILE`: Output report file (HTML or TXT)
- `--text-only`: Generate text report instead of HTML
- `--verbose`: Enable detailed output

#### Examples
```bash
# HTML report (default)
python pypylon_api_differ.py old_api.json new_api.json --output compatibility.html

# Text report
python pypylon_api_differ.py old_api.json new_api.json --text-only

# Save text report to file
python pypylon_api_differ.py old_api.json new_api.json --output diff.txt --text-only

# Console output only
python pypylon_api_differ.py ref.json cur.json --text-only
```

### Main Checker (`pypylon_compatibility_checker.py`)

#### Action Options

1. **Quick Check**
   ```bash
   python pypylon_compatibility_checker.py --quick-check
   ```
   Compares current environment against latest PyPI version using Python 3.14 for both.

2. **Full Check**
   ```bash
   python pypylon_compatibility_checker.py --full-check
   ```
   Complete compatibility analysis with detailed reporting.

3. **Compare Existing Dumps**
   ```bash
   python pypylon_compatibility_checker.py --compare ref.json cur.json
   ```
   Compare two existing API dump files.

4. **Dump Only**
   ```bash
   python pypylon_compatibility_checker.py --dump-only --output my_api.json
   ```
   Create API dump without comparison.

5. **List Dumps**
   ```bash
   python pypylon_compatibility_checker.py --list-dumps
   ```
   Show available API dumps in work directory.

#### Configuration Options

- `--python-version VERSION`: Python version to use for both environments (default: 3.14)
- `--pypylon-version VERSION`: PyPylon version for reference (default: latest)
- `--work-dir DIR`: Working directory for temporary files
- `--output FILE`: Output file path
- `--format {html,text}`: Output format (default: html)
- `--cleanup`: Clean up temporary files after completion
- `--verbose`: Enable verbose output

#### Advanced Examples

```bash
# Compare against specific pypylon version
python pypylon_compatibility_checker.py --full-check --pypylon-version 4.0.0

# Use specific Python environments
python pypylon_compatibility_checker.py --full-check \
    --reference-env ~/.pyenv/versions/3.11.0/bin/python \
    --current-env ~/.pyenv/versions/3.14.0b3/bin/python

# Custom work directory with cleanup
python pypylon_compatibility_checker.py --quick-check \
    --work-dir /tmp/pypylon_check \
    --cleanup

# Generate text report
python pypylon_compatibility_checker.py --full-check \
    --format text \
    --output compatibility_report.txt
```

## 📊 Understanding Reports

### HTML Reports

HTML reports provide:
- **Executive Summary**: Total differences and severity breakdown
- **Severity Sections**: Grouped by Major/Minor/Patch changes
- **Detailed Differences**: Complete change information
- **Interactive Features**: Hover effects, clear formatting
- **Search and Navigation**: Easy to find specific changes

### Text Reports

Text reports include:
- **Summary Statistics**: Total counts by type and severity
- **Grouped Sections**: Changes organized by severity
- **Detailed Descriptions**: What changed and how
- **Console Friendly**: Perfect for CI/CD integration

### Severity Levels

- **Major (Breaking Changes)**
  - Removed APIs (functions, classes, methods)
  - Changed function signatures
  - Modified parameter requirements
  - Changed inheritance hierarchies

- **Minor (Non-Breaking Changes)**  
  - Added new APIs
  - Enhanced documentation
  - New optional parameters
  - Additional type annotations

- **Patch (Cosmetic Changes)**
  - Docstring formatting changes
  - Comment modifications
  - Non-functional improvements

## 🔍 API Dump Format

The JSON API dumps contain comprehensive information:

```json
{
  "metadata": {
    "extraction_time": "2024-01-15T10:30:00",
    "extractor_version": "2.0.0",
    "system_info": {...}
  },
  "modules": {
    "pypylon": {
      "name": "pypylon",
      "type": "module",
      "doc": "PyPylon documentation...",
      "classes": {
        "InstantCamera": {
          "name": "InstantCamera",
          "type": "class",
          "doc": "Camera class documentation...",
          "methods": {...},
          "properties": {...},
          "stats": {...}
        }
      },
      "functions": {...},
      "constants": {...}
    }
  },
  "global_stats": {
    "total_modules": 4,
    "total_classes": 156,
    "total_functions": 89,
    "total_methods": 1247,
    "total_properties": 234
  }
}
```

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors**
   ```
   ❌ Failed to import required modules
   ```
   **Solution**: Ensure all three Python files are in the same directory.

2. **Python Environment Not Found**
   ```
   ❌ Reference Python not found
   ```
   **Solution**: Check Python path, ensure pyenv is properly configured.

3. **PyPylon Installation Issues**
   ```
   ❌ Failed to install pypylon
   ```
   **Solution**: Check network connection, verify PyPI access, try specific version.

4. **Permission Errors**
   ```
   ❌ Permission denied
   ```
   **Solution**: Ensure write permissions for work directory.

### Debugging

Enable verbose output for detailed debugging:

```bash
python pypylon_compatibility_checker.py --quick-check --verbose
```

Check available API dumps:

```bash
python pypylon_compatibility_checker.py --list-dumps
```

Test API extraction manually:

```bash
python pypylon_api_dumper.py --output test_api.json --verbose
```

## 🔧 Integration

### CI/CD Integration

For automated compatibility checking in CI/CD:

```bash
#!/bin/bash
# compatibility_check.sh

set -e

echo "Running pypylon compatibility check..."

# Run quick check with text output
python scripts/modernize/pypylon_compatibility_checker.py \
    --quick-check \
    --format text \
    --work-dir /tmp/pypylon_check \
    --cleanup

# Check exit code
if [ $? -eq 0 ]; then
    echo "✅ Compatibility check passed"
    exit 0
else
    echo "❌ Compatibility check failed"
    exit 1
fi
```

### Programmatic Usage

```python
from pypylon_compatibility_checker import PylonCompatibilityChecker

# Create checker
checker = PylonCompatibilityChecker()

# Run compatibility check
report_file, summary = checker.run_compatibility_check()

# Check results
if summary['statistics']['major'] > 0:
    print("Breaking changes detected!")
    
# Clean up
checker.cleanup()
```

## 📈 Performance

### Typical Performance Metrics

- **API Extraction**: 30-60 seconds per environment
- **API Comparison**: 5-15 seconds for large APIs
- **Report Generation**: 2-5 seconds
- **Total Quick Check**: 1-2 minutes end-to-end

### Optimization Tips

1. **Reuse API Dumps**: Create dumps once, compare multiple times
2. **Use Compression**: Enable `--compress` for large API dumps
3. **Clean Work Directory**: Use `--cleanup` to save disk space
4. **Text Reports**: Use `--text-only` for faster report generation

## 🤝 Contributing

### Adding New Features

The system is modular and extensible:

- **New Analysis**: Add methods to `PylonAPIExtractor`
- **New Comparisons**: Extend `PylonAPIDiffer._compare_item_details()`
- **New Reports**: Create new format handlers in `pypylon_api_differ.py`

### Code Structure

```
scripts/modernize/
├── pypylon_api_dumper.py       # API extraction engine
├── pypylon_api_differ.py       # Comparison and reporting
├── pypylon_compatibility_checker.py  # Main orchestrator
└── CUSTOM_API_CHECKER_README.md      # This documentation
```

## 📝 License

This tool is part of the pypylon project and follows the same licensing terms.

## 🆘 Support

For issues, questions, or contributions:

1. Check this README for common solutions
2. Enable `--verbose` output for debugging
3. Create API dumps manually to isolate issues
4. Report bugs with full error output and system information 