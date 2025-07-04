#!/usr/bin/env python3
"""
PyPylon API Differ

Compares two pypylon API dumps and identifies all differences including:
- Added/removed modules, classes, functions, methods, properties
- Changed function signatures, parameter names, defaults
- Documentation changes
- Type annotation changes

Usage:
    python pypylon_api_differ.py reference.json current.json --output diff_report.html
    python pypylon_api_differ.py pypylon_v4.2.0.json pypylon_local.json --text-only
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Set, Optional, Union, Tuple
from datetime import datetime
import difflib
import html
import hashlib


class APIItem:
    """Represents a single API item (function, class, method, etc.)"""
    
    def __init__(self, name: str, data: Dict[str, Any], path: str = ""):
        self.name = name
        self.data = data
        self.path = path
        self.type = data.get("type", "unknown")
    
    def get_signature(self) -> str:
        """Get signature string for comparison"""
        if self.type in ["function", "method"]:
            return self.data.get("signature_str", "")
        elif self.type == "property":
            parts = []
            if self.data.get("has_getter"): parts.append("getter")
            if self.data.get("has_setter"): parts.append("setter") 
            if self.data.get("has_deleter"): parts.append("deleter")
            return f"property({', '.join(parts)})"
        elif self.type == "class":
            bases = self.data.get("bases", [])
            if bases:
                return f"class {self.name}({', '.join(bases)})"
            return f"class {self.name}"
        else:
            return str(self.data.get("value", ""))
    
    def get_parameters(self) -> Dict[str, Any]:
        """Get parameter information"""
        return self.data.get("parameters", {})
    
    def get_doc(self) -> str:
        """Get documentation string"""
        return self.data.get("doc", "") or ""
    
    def get_comparable_info(self) -> Dict[str, Any]:
        """Get information for comparison"""
        info = {
            "name": self.name,
            "type": self.type,
            "signature": self.get_signature(),
            "doc": self.get_doc(),
            "doc_length": len(self.get_doc()),
            "parameters": self.get_parameters()
        }
        
        # Add type-specific information
        if self.type == "function":
            info.update({
                "callable": self.data.get("callable", False),
                "is_builtin": self.data.get("is_builtin", False),
                "is_coroutine": self.data.get("is_coroutine", False),
                "parameter_count": self.data.get("parameter_count", 0),
                "has_return_annotation": self.data.get("has_return_annotation", False),
                "return_annotation": self.data.get("return_annotation")
            })
        elif self.type == "class":
            info.update({
                "bases": self.data.get("bases", []),
                "mro": self.data.get("mro", []),
                "is_abstract": self.data.get("is_abstract", False),
                "method_count": self.data.get("stats", {}).get("total_methods", 0),
                "property_count": self.data.get("stats", {}).get("total_properties", 0)
            })
        elif self.type == "property":
            info.update({
                "has_getter": self.data.get("has_getter", False),
                "has_setter": self.data.get("has_setter", False),
                "has_deleter": self.data.get("has_deleter", False)
            })
        
        return info


class APIDifference:
    """Represents a difference between two API items"""
    
    def __init__(self, diff_type: str, path: str, name: str, 
                 old_item: Optional[APIItem] = None, 
                 new_item: Optional[APIItem] = None,
                 details: Dict[str, Any] = None):
        self.diff_type = diff_type  # added, removed, changed
        self.path = path
        self.name = name
        self.old_item = old_item
        self.new_item = new_item
        self.details = details or {}
        
    def get_severity(self) -> str:
        """Get severity level of this difference"""
        if self.diff_type == "added":
            # Adding new APIs is generally minor (non-breaking)
            if self.new_item.type == "module":
                # Adding submodules is minor - they can still be imported the same way
                return "minor"
            elif self.new_item.type == "constant":
                # Adding constants is minor - doesn't break existing code
                return "minor"
            else:
                # Adding other items (classes, functions) could be minor or major depending on context
                return "minor"
        elif self.diff_type == "removed":
            # Removing APIs is always major (breaking)
            return "major"
        elif self.diff_type == "changed":
            # Check what changed - order matters!
            if "signature" in self.details or "parameters" in self.details:
                return "major"
            elif "inheritance" in self.details or "method_count" in self.details:
                return "major"
            elif any(key in self.details for key in ["has_return_annotation", "return_annotation", "parameter_count"]):
                return "major"
            elif any(key in self.details for key in ["has_getter", "has_setter", "has_deleter"]):
                return "major"
            elif "documentation" in self.details:  # Fixed: was "doc", should be "documentation"
                return "patch"  # Documentation changes are cosmetic, not even minor
            else:
                return "patch"
        return "unknown"
    
    def get_description(self) -> str:
        """Get human-readable description"""
        if self.diff_type == "added":
            return f"Added {self.new_item.type}: {self.name}"
        elif self.diff_type == "removed":
            return f"Removed {self.old_item.type}: {self.name}"
        elif self.diff_type == "changed":
            changes = list(self.details.keys())
            return f"Changed {self.old_item.type}: {self.name} ({', '.join(changes)})"
        return f"Unknown difference in {self.name}"


class PylonAPIDiffer:
    """Comprehensive API differ for pypylon packages"""
    
    def __init__(self):
        self.differences: List[APIDifference] = []
        self.stats = {
            "added": 0,
            "removed": 0, 
            "changed": 0,
            "major": 0,
            "minor": 0,
            "patch": 0
        }
    
    def compare_apis(self, reference_data: Dict[str, Any], 
                    current_data: Dict[str, Any]) -> List[APIDifference]:
        """Compare two API dumps and return differences"""
        self.differences = []
        
        # Compare modules
        ref_modules = reference_data.get("modules", {})
        cur_modules = current_data.get("modules", {})
        
        self._compare_modules(ref_modules, cur_modules, "")
        
        # Compare pydoc documentation
        ref_pydoc = reference_data.get("pydoc_documentation", {})
        cur_pydoc = current_data.get("pydoc_documentation", {})
        self._compare_pydoc_documentation(ref_pydoc, cur_pydoc)
        
        # Calculate statistics
        self._calculate_stats()
        
        return self.differences
    
    def _compare_modules(self, ref_modules: Dict[str, Any], 
                        cur_modules: Dict[str, Any], 
                        base_path: str) -> None:
        """Compare modules recursively"""
        
        all_module_names = set(ref_modules.keys()) | set(cur_modules.keys())
        
        for module_name in all_module_names:
            module_path = f"{base_path}.{module_name}" if base_path else module_name
            
            ref_module = ref_modules.get(module_name)
            cur_module = cur_modules.get(module_name)
            
            if ref_module is None:
                # Module added
                if cur_module.get("type") == "module":
                    self.differences.append(APIDifference(
                        "added", module_path, module_name,
                        new_item=APIItem(module_name, cur_module, module_path)
                    ))
            elif cur_module is None:
                # Module removed
                if ref_module.get("type") == "module":
                    self.differences.append(APIDifference(
                        "removed", module_path, module_name,
                        old_item=APIItem(module_name, ref_module, module_path)
                    ))
            else:
                # Module exists in both - compare contents
                if ref_module.get("type") == "module" and cur_module.get("type") == "module":
                    self._compare_module_contents(ref_module, cur_module, module_path)
    
    def _compare_module_contents(self, ref_module: Dict[str, Any], 
                               cur_module: Dict[str, Any], 
                               module_path: str) -> None:
        """Compare the contents of two modules"""
        
        # Compare different types of module contents
        content_types = ["classes", "functions", "constants", "exceptions", "submodules"]
        
        for content_type in content_types:
            ref_items = ref_module.get(content_type, {})
            cur_items = cur_module.get(content_type, {})
            
            if content_type == "submodules":
                self._compare_modules(ref_items, cur_items, module_path)
            else:
                self._compare_items(ref_items, cur_items, f"{module_path}.{content_type}")
    
    def _compare_items(self, ref_items: Dict[str, Any], 
                      cur_items: Dict[str, Any], 
                      base_path: str) -> None:
        """Compare collections of API items"""
        
        all_item_names = set(ref_items.keys()) | set(cur_items.keys())
        
        for item_name in all_item_names:
            item_path = f"{base_path}.{item_name}"
            
            ref_item = ref_items.get(item_name)
            cur_item = cur_items.get(item_name)
            
            if ref_item is None:
                # Item added
                self.differences.append(APIDifference(
                    "added", item_path, item_name,
                    new_item=APIItem(item_name, cur_item, item_path)
                ))
            elif cur_item is None:
                # Item removed
                self.differences.append(APIDifference(
                    "removed", item_path, item_name,
                    old_item=APIItem(item_name, ref_item, item_path)
                ))
            else:
                # Item exists in both - compare details
                self._compare_item_details(
                    APIItem(item_name, ref_item, item_path),
                    APIItem(item_name, cur_item, item_path)
                )
    
    def _compare_item_details(self, ref_item: APIItem, cur_item: APIItem) -> None:
        """Compare details of two API items"""
        
        if ref_item.type != cur_item.type:
            # Type changed (very rare but possible)
            self.differences.append(APIDifference(
                "changed", ref_item.path, ref_item.name,
                old_item=ref_item, new_item=cur_item,
                details={"type": {"old": ref_item.type, "new": cur_item.type}}
            ))
            return
        
        # Get comparable information
        ref_info = ref_item.get_comparable_info()
        cur_info = cur_item.get_comparable_info()
        
        changes = {}
        
        # Compare signature
        if ref_info["signature"] != cur_info["signature"]:
            changes["signature"] = {
                "old": ref_info["signature"],
                "new": cur_info["signature"]
            }
        
        # Compare parameters (detailed)
        if ref_item.type in ["function", "method"]:
            param_changes = self._compare_parameters(ref_info["parameters"], cur_info["parameters"])
            if param_changes:
                changes["parameters"] = param_changes
        
        # Compare documentation
        if ref_info["doc"] != cur_info["doc"]:
            changes["documentation"] = {
                "old_length": ref_info["doc_length"],
                "new_length": cur_info["doc_length"],
                "old_doc": ref_info["doc"],
                "new_doc": cur_info["doc"],
                "changed": True
            }
            # Add diff preview for docs
            if ref_info["doc"] and cur_info["doc"]:
                doc_diff = list(difflib.unified_diff(
                    ref_info["doc"].splitlines(),
                    cur_info["doc"].splitlines(),
                    lineterm='',
                    n=3
                ))
                if doc_diff:
                    changes["documentation"]["diff_preview"] = doc_diff[:20]  # First 20 lines
        
        # Compare class-specific details
        if ref_item.type == "class":
            if ref_info["bases"] != cur_info["bases"]:
                changes["inheritance"] = {
                    "old_bases": ref_info["bases"],
                    "new_bases": cur_info["bases"]
                }
            
            if ref_info["method_count"] != cur_info["method_count"]:
                changes["method_count"] = {
                    "old": ref_info["method_count"],
                    "new": cur_info["method_count"]
                }
            
            # Compare class members recursively
            self._compare_class_members(ref_item, cur_item)
        
        # Compare function-specific details
        if ref_item.type == "function":
            func_specific = ["has_return_annotation", "return_annotation", "parameter_count"]
            for attr in func_specific:
                if ref_info.get(attr) != cur_info.get(attr):
                    changes[attr] = {
                        "old": ref_info.get(attr),
                        "new": cur_info.get(attr)
                    }
        
        # Compare property-specific details
        if ref_item.type == "property":
            prop_attrs = ["has_getter", "has_setter", "has_deleter"]
            for attr in prop_attrs:
                if ref_info.get(attr) != cur_info.get(attr):
                    changes[attr] = {
                        "old": ref_info.get(attr),
                        "new": cur_info.get(attr)
                    }
        
        # If any changes found, record the difference
        if changes:
            self.differences.append(APIDifference(
                "changed", ref_item.path, ref_item.name,
                old_item=ref_item, new_item=cur_item,
                details=changes
            ))
    
    def _compare_parameters(self, ref_params: Dict[str, Any], 
                           cur_params: Dict[str, Any]) -> Dict[str, Any]:
        """Compare function parameters in detail"""
        changes = {}
        
        ref_names = set(ref_params.keys())
        cur_names = set(cur_params.keys())
        
        # Parameter name changes
        if ref_names != cur_names:
            changes["parameter_names"] = {
                "added": list(cur_names - ref_names),
                "removed": list(ref_names - cur_names)
            }
        
        # Compare existing parameters
        common_params = ref_names & cur_names
        param_changes = {}
        
        for param_name in common_params:
            ref_param = ref_params[param_name]
            cur_param = cur_params[param_name]
            
            param_diff = {}
            
            # Compare parameter attributes
            for attr in ["kind", "has_default", "default_value", "has_annotation", "annotation"]:
                if ref_param.get(attr) != cur_param.get(attr):
                    param_diff[attr] = {
                        "old": ref_param.get(attr),
                        "new": cur_param.get(attr)
                    }
            
            if param_diff:
                param_changes[param_name] = param_diff
        
        if param_changes:
            changes["parameter_details"] = param_changes
        
        return changes
    
    def _compare_class_members(self, ref_class: APIItem, cur_class: APIItem) -> None:
        """Compare class members (methods, properties, etc.)"""
        
        member_types = ["methods", "properties", "class_attributes", "static_methods", 
                       "class_methods", "special_methods", "nested_classes"]
        
        for member_type in member_types:
            ref_members = ref_class.data.get(member_type, {})
            cur_members = cur_class.data.get(member_type, {})
            
            member_path = f"{ref_class.path}.{member_type}"
            
            if member_type == "nested_classes":
                # Handle nested classes recursively
                self._compare_items(ref_members, cur_members, member_path)
            else:
                self._compare_items(ref_members, cur_members, member_path)
    
    def _compare_pydoc_documentation(self, ref_pydoc: Dict[str, Any], 
                                   cur_pydoc: Dict[str, Any]) -> None:
        """Compare pydoc documentation between reference and current"""
        
        all_module_names = set(ref_pydoc.keys()) | set(cur_pydoc.keys())
        
        for module_name in all_module_names:
            ref_doc = ref_pydoc.get(module_name)
            cur_doc = cur_pydoc.get(module_name)
            
            if ref_doc is None:
                # Documentation added
                if cur_doc and cur_doc.get("success"):
                    self.differences.append(APIDifference(
                        "added", f"pydoc.{module_name}", module_name,
                        new_item=APIItem(module_name, {
                            "type": "pydoc_documentation",
                            "doc": cur_doc.get("documentation", ""),
                            "doc_length": cur_doc.get("doc_length", 0),
                            "doc_lines": cur_doc.get("doc_lines", 0)
                        }, f"pydoc.{module_name}")
                    ))
            elif cur_doc is None:
                # Documentation removed
                if ref_doc and ref_doc.get("success"):
                    self.differences.append(APIDifference(
                        "removed", f"pydoc.{module_name}", module_name,
                        old_item=APIItem(module_name, {
                            "type": "pydoc_documentation",
                            "doc": ref_doc.get("documentation", ""),
                            "doc_length": ref_doc.get("doc_length", 0),
                            "doc_lines": ref_doc.get("doc_lines", 0)
                        }, f"pydoc.{module_name}")
                    ))
            else:
                # Documentation exists in both - compare content
                if ref_doc.get("success") and cur_doc.get("success"):
                    ref_doc_text = ref_doc.get("documentation", "")
                    cur_doc_text = cur_doc.get("documentation", "")
                    
                    if ref_doc_text != cur_doc_text:
                        # Create diff for documentation
                        doc_diff = list(difflib.unified_diff(
                            ref_doc_text.splitlines(),
                            cur_doc_text.splitlines(),
                            lineterm='',
                            n=3
                        ))
                        
                        self.differences.append(APIDifference(
                            "changed", f"pydoc.{module_name}", module_name,
                            old_item=APIItem(module_name, {
                                "type": "pydoc_documentation",
                                "doc": ref_doc_text,
                                "doc_length": ref_doc.get("doc_length", 0),
                                "doc_lines": ref_doc.get("doc_lines", 0)
                            }, f"pydoc.{module_name}"),
                            new_item=APIItem(module_name, {
                                "type": "pydoc_documentation",
                                "doc": cur_doc_text,
                                "doc_length": cur_doc.get("doc_length", 0),
                                "doc_lines": cur_doc.get("doc_lines", 0)
                            }, f"pydoc.{module_name}"),
                            details={
                                "documentation": {
                                    "old_length": ref_doc.get("doc_length", 0),
                                    "new_length": cur_doc.get("doc_length", 0),
                                    "old_lines": ref_doc.get("doc_lines", 0),
                                    "new_lines": cur_doc.get("doc_lines", 0),
                                    "diff_preview": doc_diff[:50]  # First 50 lines of diff
                                }
                            }
                        ))
    
    def _calculate_stats(self) -> None:
        """Calculate summary statistics"""
        self.stats = {
            "added": 0,
            "removed": 0,
            "changed": 0,
            "major": 0,
            "minor": 0,
            "patch": 0
        }
        
        for diff in self.differences:
            self.stats[diff.diff_type] += 1
            self.stats[diff.get_severity()] += 1
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of differences"""
        return {
            "total_differences": len(self.differences),
            "statistics": self.stats,
            "breakdown_by_type": {
                diff_type: len([d for d in self.differences if d.diff_type == diff_type])
                for diff_type in ["added", "removed", "changed"]
            },
            "breakdown_by_severity": {
                severity: len([d for d in self.differences if d.get_severity() == severity])
                for severity in ["major", "minor", "patch"]
            }
        }


def load_api_dump(file_path: Path) -> Dict[str, Any]:
    """Load API dump from JSON file"""
    if not file_path.exists():
        raise FileNotFoundError(f"API dump file not found: {file_path}")
    
    if file_path.suffix == '.gz':
        import gzip
        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            return json.load(f)
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)


def load_documentation_files(api_data: Dict[str, Any], base_path: Path) -> Dict[str, str]:
    """Load documentation files referenced in API dump"""
    doc_files = {}
    
    metadata = api_data.get("metadata", {})
    doc_file_info = metadata.get("documentation_files", {})
    
    for module_name, file_info in doc_file_info.items():
        if isinstance(file_info, dict) and "path" in file_info:
            try:
                doc_file_path = base_path.parent / file_info["path"]
                if doc_file_path.exists():
                    with open(doc_file_path, 'r', encoding='utf-8') as f:
                        doc_files[module_name] = f.read()
                    print(f"📄 Loaded documentation: {module_name} ({len(doc_files[module_name])} chars)")
                else:
                    print(f"⚠️  Documentation file not found: {doc_file_path}")
            except Exception as e:
                print(f"⚠️  Failed to load documentation for {module_name}: {e}")
    
    return doc_files


def generate_side_by_side_diff_html(ref_text: str, cur_text: str, module_name: str) -> str:
    """Generate HTML for side-by-side diff view of documentation using diff2html"""
    
    print(f"📝 generate_side_by_side_diff_html called:")
    print(f"   module_name: {module_name}")
    print(f"   ref_text length: {len(ref_text)}")
    print(f"   cur_text length: {len(cur_text)}")
    
    # Create a unique container ID
    container_id = f"diff-{module_name.replace('.', '-').replace('_', '-')}"
    print(f"   container_id: {container_id}")
    
    # Use json.dumps for safe JS string embedding
    ref_text_escaped = json.dumps(ref_text)
    cur_text_escaped = json.dumps(cur_text)
    
    print(f"   ref_text_escaped length: {len(ref_text_escaped)}")
    print(f"   cur_text_escaped length: {len(cur_text_escaped)}")
    print(f"   cur_text_escaped value: {cur_text_escaped[:100]}...")
    
    html_parts = []
    html_parts.append(f"""
    <div class="side-by-side-diff">
        <div class="diff-header">
            <h3>📚 Documentation Comparison: {html.escape(module_name)}</h3>
            <div class="diff-stats">
                <span class="stat">Reference: {len(ref_text.splitlines())} lines, {len(ref_text)} chars</span>
                <span class="stat">Current: {len(cur_text.splitlines())} lines, {len(cur_text)} chars</span>
            </div>
        </div>
        <div class="diff-controls">
            <button class="active" onclick="toggleDiffMode('{container_id}', 'side-by-side')">Side by Side</button>
            <button onclick="toggleDiffMode('{container_id}', 'unified')">Unified</button>
            <button onclick="toggleDiffContext('{container_id}', 3)" class="context-btn active">Compact (3 lines)</button>
            <button onclick="toggleDiffContext('{container_id}', 10)" class="context-btn">More Context (10 lines)</button>
            <button onclick="toggleDiffContext('{container_id}', 0)" class="context-btn">Full View</button>
            <div class="diff-mode">Professional diff viewer</div>
        </div>
        <div id="{container_id}" class="diff-container">
            <!-- Diff2Html will render here -->
        </div>
        <script type="application/json" id="{container_id}-data">{{
            "oldText": {ref_text_escaped},
            "newText": {cur_text_escaped},
            "fileName": "{html.escape(module_name)}.txt"
        }}</script>
    </div>
    """)
    
    return '\n'.join(html_parts)


def generate_text_report(differences: List[APIDifference], 
                        summary: Dict[str, Any],
                        reference_file: str,
                        current_file: str) -> str:
    """Generate text report of API differences"""
    
    report = []
    report.append("=" * 80)
    report.append("PyPylon API Compatibility Report")
    report.append("=" * 80)
    report.append(f"Reference: {reference_file}")
    report.append(f"Current:   {current_file}")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Summary
    report.append("SUMMARY")
    report.append("-" * 40)
    report.append(f"Total differences: {summary['total_differences']}")
    report.append("")
    
    stats = summary['statistics']
    report.append(f"By type:")
    report.append(f"  Added:   {stats['added']}")
    report.append(f"  Removed: {stats['removed']}")
    report.append(f"  Changed: {stats['changed']}")
    report.append("")
    
    report.append(f"By severity:")
    report.append(f"  Major:   {stats['major']} (breaking changes)")
    report.append(f"  Minor:   {stats['minor']} (non-breaking changes)")
    report.append(f"  Patch:   {stats['patch']} (cosmetic changes)")
    report.append("")
    
    # Group differences by severity
    by_severity = {
        "major": [d for d in differences if d.get_severity() == "major"],
        "minor": [d for d in differences if d.get_severity() == "minor"],
        "patch": [d for d in differences if d.get_severity() == "patch"]
    }
    
    for severity in ["major", "minor", "patch"]:
        diffs = by_severity[severity]
        if not diffs:
            continue
        
        report.append(f"{severity.upper()} CHANGES ({len(diffs)})")
        report.append("-" * 40)
        
        for diff in diffs:
            report.append(f"📍 {diff.path}")
            report.append(f"   {diff.get_description()}")
            
            if diff.details:
                for change_type, change_data in diff.details.items():
                    if change_type == "signature":
                        report.append(f"   Signature: {change_data['old']} → {change_data['new']}")
                    elif change_type == "parameters":
                        if "parameter_names" in change_data:
                            param_names = change_data["parameter_names"]
                            if param_names.get("added"):
                                report.append(f"   Added parameters: {', '.join(param_names['added'])}")
                            if param_names.get("removed"):
                                report.append(f"   Removed parameters: {', '.join(param_names['removed'])}")
                    elif change_type == "documentation":
                        old_len = change_data['old_length']
                        new_len = change_data['new_length']
                        report.append(f"   Documentation: {old_len} → {new_len} characters")
            
            report.append("")
    
    return "\n".join(report)


def generate_html_report(differences: List[APIDifference], 
                        summary: Dict[str, Any],
                        reference_file: str,
                        current_file: str,
                        reference_stats: Dict[str, Any] = None,
                        current_stats: Dict[str, Any] = None,
                        reference_data: Dict[str, Any] = None,
                        current_data: Dict[str, Any] = None) -> str:
    """Generate HTML report of API differences"""
    
    # HTML template
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PyPylon API Compatibility Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               line-height: 1.6; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; 
                     border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   color: white; padding: 30px; border-radius: 8px 8px 0 0; }}
        .content {{ padding: 30px; }}
        h1 {{ margin: 0; font-size: 2.5em; }}
        h2 {{ color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        h3 {{ color: #666; margin-top: 30px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                    gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: #f8f9fa; border-radius: 8px; padding: 20px; text-align: center; }}
        .stat-number {{ font-size: 2em; font-weight: bold; color: #667eea; margin-bottom: 5px; }}
        .stat-label {{ color: #666; text-transform: uppercase; font-size: 0.9em; }}
        .difference {{ border: 1px solid #ddd; border-radius: 6px; margin: 15px 0; 
                      overflow: hidden; transition: box-shadow 0.2s; }}
        .difference:hover {{ box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .diff-header {{ padding: 15px; background: #f8f9fa; border-bottom: 1px solid #eee; }}
        .diff-path {{ font-family: monospace; font-size: 0.9em; color: #666; }}
        .diff-type {{ font-weight: bold; text-transform: uppercase; font-size: 0.8em; 
                     padding: 3px 8px; border-radius: 12px; margin-left: 10px; }}
        .diff-type.added {{ background: #d4edda; color: #155724; }}
        .diff-type.removed {{ background: #f8d7da; color: #721c24; }}
        .diff-type.changed {{ background: #fff3cd; color: #856404; }}
        .severity {{ float: right; font-size: 0.8em; padding: 2px 6px; border-radius: 10px; }}
        .severity.major {{ background: #dc3545; color: white; }}
        .severity.minor {{ background: #ffc107; color: #212529; }}
        .severity.patch {{ background: #28a745; color: white; }}
        .diff-details {{ padding: 15px; }}
        .change-item {{ margin: 10px 0; }}
        .change-label {{ font-weight: bold; color: #495057; }}
        .code {{ background: #f8f9fa; padding: 3px 6px; border-radius: 3px; 
                 font-family: monospace; font-size: 0.9em; }}
        .old {{ background: #f8d7da; }}
        .new {{ background: #d4edda; }}
        .meta {{ color: #666; font-size: 0.9em; margin-top: 20px; }}
        pre {{ background: #f8f9fa; padding: 10px; border-radius: 4px; overflow-x: auto; }}
        .doc-diff {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px; }}
        .doc-side {{ border: 1px solid #ddd; border-radius: 6px; overflow: hidden; }}
        .doc-header {{ background: #f8f9fa; padding: 10px; font-weight: bold; border-bottom: 1px solid #ddd; }}
        .doc-content {{ margin: 0; padding: 15px; background: white; max-height: 400px; overflow-y: auto; 
                       font-family: 'Courier New', monospace; font-size: 0.85em; line-height: 1.4; }}
        
        /* Tab styles */
        .tabs {{ display: flex; border-bottom: 2px solid #eee; margin-bottom: 20px; }}
        .tab {{ padding: 12px 24px; background: #f8f9fa; border: none; cursor: pointer; 
                border-radius: 6px 6px 0 0; margin-right: 4px; font-weight: 500; }}
        .tab.active {{ background: #667eea; color: white; }}
        .tab:hover:not(.active) {{ background: #e9ecef; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        
        /* Pydoc diff styles */
        .pydoc-diff {{ background: #f8f9fa; border-radius: 6px; margin: 15px 0; overflow: hidden; }}
        .pydoc-diff-header {{ background: #e9ecef; padding: 15px; border-bottom: 1px solid #ddd; }}
        .pydoc-diff-content {{ padding: 20px; }}
        .pydoc-module {{ margin-bottom: 30px; }}
        .pydoc-module h4 {{ color: #495057; margin-bottom: 15px; }}
        .pydoc-stats {{ display: flex; gap: 20px; margin-bottom: 15px; }}
        .pydoc-stat {{ background: white; padding: 10px; border-radius: 4px; text-align: center; }}
        .pydoc-stat-number {{ font-size: 1.2em; font-weight: bold; color: #667eea; }}
        .pydoc-stat-label {{ font-size: 0.8em; color: #666; }}
        .pydoc-text-diff {{ background: white; border: 1px solid #ddd; border-radius: 4px; overflow: hidden; }}
        .pydoc-text-diff pre {{ margin: 0; padding: 15px; max-height: 500px; overflow-y: auto; 
                                font-family: 'Courier New', monospace; font-size: 0.85em; line-height: 1.4; }}
        .diff-line {{ padding: 2px 0; }}
        .diff-line.added {{ background: #d4edda; }}
        .diff-line.removed {{ background: #f8d7da; }}
        .diff-line.context {{ background: #f8f9fa; }}
        
        /* Side-by-side diff styles */
        .side-by-side-diff {{ margin: 20px 0; border: 1px solid #ddd; border-radius: 6px; overflow: hidden; }}
        .side-by-side-diff .diff-header {{ background: #f8f9fa; padding: 15px; border-bottom: 1px solid #ddd; }}
        .side-by-side-diff .diff-header h3 {{ margin: 0 0 10px 0; color: #495057; }}
        .side-by-side-diff .diff-stats {{ display: flex; gap: 20px; }}
        .side-by-side-diff .diff-stats .stat {{ background: white; padding: 5px 10px; border-radius: 4px; font-size: 0.9em; color: #666; }}
        
        /* Diff2Html styles */
        .d2h-wrapper {{ margin: 0; }}
        .d2h-file-header {{ background: #e9ecef; padding: 10px 15px; border-bottom: 1px solid #ddd; }}
        .d2h-file-header h2 {{ margin: 0; font-size: 1.2em; color: #495057; }}
        .d2h-diff-table {{ border: 1px solid #ddd; border-radius: 0 0 6px 6px; overflow: hidden; }}
        .d2h-files-diff {{ margin: 0; }}
        .d2h-file-side-diff {{ margin: 0; }}
        .d2h-diff-tbody {{ font-family: 'Courier New', monospace; font-size: 0.85em; line-height: 1.4; }}
        .d2h-code-line {{ padding: 2px 15px; }}
        .d2h-code-line.d2h-del {{ background: #f8d7da; }}
        .d2h-code-line.d2h-ins {{ background: #d4edda; }}
        .d2h-code-line.d2h-cntx {{ background: white; }}
        
        /* Custom diff controls */
        .diff-controls {{ background: #f8f9fa; padding: 10px 15px; border-bottom: 1px solid #ddd; display: flex; gap: 10px; align-items: center; }}
        .diff-controls button {{ padding: 5px 10px; border: 1px solid #ddd; border-radius: 4px; background: white; cursor: pointer; font-size: 0.9em; }}
        .diff-controls button:hover {{ background: #e9ecef; }}
        .diff-controls button.active {{ background: #667eea; color: white; border-color: #667eea; }}
        .diff-controls .context-btn {{ background: #e9ecef; color: #495057; }}
        .diff-controls .context-btn.active {{ background: #28a745; color: white; border-color: #28a745; }}
        .diff-controls .diff-mode {{ margin-left: auto; font-size: 0.8em; color: #666; }}
        .diff-container {{ margin: 0; min-height: 200px; }}
        .diff-side {{ border: 1px solid #ddd; }}
        .diff-side-header {{ background: #f8f9fa; padding: 10px; font-weight: bold; border-bottom: 1px solid #ddd; }}
        .diff-content {{ padding: 15px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 PyPylon API Compatibility Report</h1>
            <p>Comprehensive analysis of API differences</p>
        </div>
        
        <div class="content">
            <div class="meta">
                <strong>Reference:</strong> {reference_file}<br>
                <strong>Current:</strong> {current_file}<br>
                <strong>Generated:</strong> {timestamp}
            </div>
            
            <h2>📊 Summary</h2>
            <div class="summary">
                {summary_cards}
            </div>
            
            {api_overview_html}
            
            <!-- Tabs -->
            <div class="tabs">
                <button class="tab active" onclick="showTab('api-diff')">API Differences</button>
                <button class="tab" onclick="showTab('pydoc-diff')">Pydoc Documentation</button>
            </div>
            
            <!-- API Differences Tab -->
            <div id="api-diff" class="tab-content active">
                <h2>🔍 Detailed API Differences</h2>
                {differences_html}
            </div>
            
            <!-- Pydoc Documentation Tab -->
            <div id="pydoc-diff" class="tab-content">
                <h2>📚 Pydoc Documentation Differences</h2>
                {pydoc_differences_html}
            </div>
        </div>
    </div>
    
    <!-- Diff libraries -->
    <script src="https://cdn.jsdelivr.net/npm/diff@5.1.0/dist/diff.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/diff2html@3.4.42/bundles/js/diff2html.min.js"></script>
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/diff2html@3.4.42/bundles/css/diff2html.min.css" />
    
    <script>
    // All functions defined globally
    function createDiff2HtmlViewer(containerId, oldText, newText, fileName, contextLines) {{
        try {{
            // Use custom context lines or default to 3
            if (typeof contextLines === 'undefined') contextLines = 3;
            
            console.log('Creating diff for container:', containerId, 'with context:', contextLines);
            console.log('Old text length:', oldText.length, 'New text length:', newText.length);
            
            // Check if texts are identical
            if (oldText === newText) {{
                document.getElementById(containerId).innerHTML = '<p style="padding: 20px; color: #666; text-align: center;">📋 No differences found - documentation is identical.</p>';
                return;
            }}
            
            // Handle empty texts
            if (!oldText && !newText) {{
                document.getElementById(containerId).innerHTML = '<p style="padding: 20px; color: #666; text-align: center;">📋 No documentation available for either version.</p>';
                return;
            }}
            
            // Create a compact line-by-line diff with context
            var oldLines = (oldText || '').split('\\n');
            var newLines = (newText || '').split('\\n');
            // contextLines parameter controls how much context to show (0 = full view)
            
            // Find all changed lines
            var maxLines = Math.max(oldLines.length, newLines.length);
            var changedLines = [];
            var diffFound = false;
            
            for (var i = 0; i < maxLines; i++) {{
                var oldLine = oldLines[i] || '';
                var newLine = newLines[i] || '';
                if (oldLine !== newLine) {{
                    changedLines.push(i);
                    diffFound = true;
                }}
            }}
            
            if (!diffFound) {{
                document.getElementById(containerId).innerHTML = '<p style="padding: 20px; color: #666; text-align: center;">📋 No differences found - documentation is identical.</p>';
                return;
            }}
            
            // Build hunks (groups of changes with context)
            var hunks = [];
            var currentHunk = null;
            
            if (contextLines === 0) {{
                // Full view - show everything
                hunks = [{{ start: 0, end: maxLines - 1 }}];
            }} else {{
                // Compact view - build hunks around changes
                changedLines.forEach(function(lineNum) {{
                    var hunkStart = Math.max(0, lineNum - contextLines);
                    var hunkEnd = Math.min(maxLines - 1, lineNum + contextLines);
                    
                    if (!currentHunk || hunkStart > currentHunk.end + 1) {{
                        // Start new hunk
                        if (currentHunk) hunks.push(currentHunk);
                        currentHunk = {{ start: hunkStart, end: hunkEnd }};
                    }} else {{
                        // Extend current hunk
                        currentHunk.end = Math.max(currentHunk.end, hunkEnd);
                    }}
                }});
                if (currentHunk) hunks.push(currentHunk);
            }}
            
            // Generate HTML for hunks
            var leftContent = [];
            var rightContent = [];
            
            hunks.forEach(function(hunk, hunkIndex) {{
                if (hunkIndex > 0 && contextLines > 0) {{
                    // Add separator between hunks (only in compact view)
                    leftContent.push('<div style="background: #f0f0f0; color: #666; text-align: center; padding: 10px; margin: 5px 0; border: 1px dashed #ccc;">⋮⋮⋮ Lines ' + (hunks[hunkIndex-1].end + 2) + ' to ' + hunk.start + ' unchanged ⋮⋮⋮</div>');
                    rightContent.push('<div style="background: #f0f0f0; color: #666; text-align: center; padding: 10px; margin: 5px 0; border: 1px dashed #ccc;">⋮⋮⋮ Lines ' + (hunks[hunkIndex-1].end + 2) + ' to ' + hunk.start + ' unchanged ⋮⋮⋮</div>');
                }}
                
                for (var i = hunk.start; i <= hunk.end; i++) {{
                    var oldLine = oldLines[i] || '';
                    var newLine = newLines[i] || '';
                    var isChanged = oldLine !== newLine;
                    var lineNum = i + 1;
                    
                    var lineStyle = isChanged ? 
                        'background: #ffebee; border-left: 3px solid #f44336; padding: 2px 5px; margin: 1px 0;' : 
                        (contextLines > 0 ? 'background: #f8f8f8; padding: 2px 5px; margin: 1px 0; color: #666;' : 'background: transparent; padding: 2px 5px; margin: 1px 0;');
                    var lineStyleNew = isChanged ? 
                        'background: #e8f5e8; border-left: 3px solid #4caf50; padding: 2px 5px; margin: 1px 0;' : 
                        (contextLines > 0 ? 'background: #f8f8f8; padding: 2px 5px; margin: 1px 0; color: #666;' : 'background: transparent; padding: 2px 5px; margin: 1px 0;');
                    
                    var lineNumStyle = 'display: inline-block; width: 40px; text-align: right; margin-right: 8px; color: #999; font-size: 0.8em;';
                    
                    leftContent.push('<div style="' + lineStyle + '"><span style="' + lineNumStyle + '">' + lineNum + '</span>' + (oldLine ? oldLine.replace(/</g, '&lt;').replace(/>/g, '&gt;') : '&nbsp;') + '</div>');
                    rightContent.push('<div style="' + lineStyleNew + '"><span style="' + lineNumStyle + '">' + lineNum + '</span>' + (newLine ? newLine.replace(/</g, '&lt;').replace(/>/g, '&gt;') : '&nbsp;') + '</div>');
                }}
            }});
            
            // Create a highlighted side-by-side diff
            var targetElement = document.getElementById(containerId);
            targetElement.innerHTML = `
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1px; border: 1px solid #ddd; border-radius: 6px; overflow: hidden;">
                    <div style="background: #f8f9fa; padding: 10px; font-weight: bold; border-bottom: 1px solid #ddd; color: #dc3545;">Reference Version</div>
                    <div style="background: #f8f9fa; padding: 10px; font-weight: bold; border-bottom: 1px solid #ddd; color: #28a745;">Current Version</div>
                    <div style="max-height: 500px; overflow-y: auto; padding: 10px; font-family: 'Courier New', monospace; font-size: 0.85em; line-height: 1.4; background: #fafafa;">` + leftContent.join('') + `</div>
                    <div style="max-height: 500px; overflow-y: auto; padding: 10px; font-family: 'Courier New', monospace; font-size: 0.85em; line-height: 1.4; background: #fafafa;">` + rightContent.join('') + `</div>
                </div>
            `;
            
            // Check if libraries are loaded (original code kept for later)
            if (typeof Diff2Html === 'undefined' || typeof Diff === 'undefined') {{
                console.error('Diff libraries not loaded, using fallback');
                // Fallback already handled above
                return;
            }}
            
            // Convert to unified diff format with context (compact view by default)
            var contextLines = 3; // Number of context lines to show
            var unifiedDiff = '';
            var oldLineNum = 1;
            var newLineNum = 1;
            unifiedDiff += '--- ' + fileName + '\\n';
            unifiedDiff += '+++ ' + fileName + '\\n';

            // Build hunks: each hunk is a group of changes with context
            var hunks = [];
            var currentHunk = null;
            var unchangedBuffer = [];
            var oldLine = 1;
            var newLine = 1;
            function flushHunk() {{
                if (currentHunk) {{
                    // Add trailing context
                    currentHunk.lines = currentHunk.lines.concat(unchangedBuffer.slice(0, contextLines));
                    currentHunk.oldLines += unchangedBuffer.slice(0, contextLines).filter(l => l[0] !== '+').length;
                    currentHunk.newLines += unchangedBuffer.slice(0, contextLines).filter(l => l[0] !== '-').length;
                    hunks.push(currentHunk);
                    currentHunk = null;
                }}
                unchangedBuffer = [];
            }}
            
            var diffResult = Diff.diffLines(oldText, newText, {{
                ignoreWhitespace: false,
                newlineIsToken: true
            }});
            
            diffResult.forEach(function(part, idx) {{
                var lines = part.value.split('\\n');
                if (lines[lines.length-1] === '') lines.pop();
                if (!part.added && !part.removed) {{
                    // Unchanged
                    if (currentHunk) {{
                        unchangedBuffer = unchangedBuffer.concat(lines.map(l => ' ' + l));
                        // If buffer is too big, flush hunk
                        if (unchangedBuffer.length > 2 * contextLines) {{
                            flushHunk();
                        }}
                    }}
                    oldLine += lines.length;
                    newLine += lines.length;
                }} else {{
                    // Change: flush buffer as context
                    if (!currentHunk) {{
                        // Start new hunk, include leading context
                        var leadingContext = unchangedBuffer.slice(-contextLines);
                        currentHunk = {{
                            oldStart: oldLine - leadingContext.length,
                            newStart: newLine - leadingContext.length,
                            oldLines: leadingContext.filter(l => l[0] !== '+').length,
                            newLines: leadingContext.filter(l => l[0] !== '-').length,
                            lines: leadingContext.slice()
                        }};
                    }}
                    if (part.added) {{
                        lines.forEach(function(l) {{
                            currentHunk.lines.push('+' + l);
                            currentHunk.newLines++;
                            newLine++;
                        }});
                    }} else if (part.removed) {{
                        lines.forEach(function(l) {{
                            currentHunk.lines.push('-' + l);
                            currentHunk.oldLines++;
                            oldLine++;
                        }});
                    }}
                    unchangedBuffer = [];
                }}
            }});
            flushHunk();
            // Output hunks
            hunks.forEach(function(hunk) {{
                unifiedDiff += '@@ -' + hunk.oldStart + ',' + hunk.oldLines + ' +' + hunk.newStart + ',' + hunk.newLines + ' @@\\n';
                hunk.lines.forEach(function(line) {{
                    unifiedDiff += line + '\\n';
                }});
            }});
            
            // Use Diff2Html to render
            var diffHtml = Diff2Html.html(unifiedDiff, {{
                drawFileList: false,
                matching: 'lines',
                outputFormat: 'side-by-side'
            }});
            
            var targetElement = document.getElementById(containerId);
            targetElement.innerHTML = diffHtml;
            
            // Store the unified diff data for mode switching
            var diffWrapper = targetElement.querySelector('.d2h-wrapper');
            if (diffWrapper) {{
                diffWrapper.setAttribute('data-unified-diff', unifiedDiff);
                diffWrapper.setAttribute('data-old-text', oldText);
                diffWrapper.setAttribute('data-new-text', newText);
                diffWrapper.setAttribute('data-file-name', fileName);
            }}
            
        }} catch (error) {{
            console.error('Error creating diff viewer:', error);
            // Fallback to simple text comparison
            var targetElement = document.getElementById(containerId);
            targetElement.innerHTML = `
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; border: 1px solid #ddd; border-radius: 6px; overflow: hidden;">
                    <div style="background: #f8f9fa; padding: 10px; font-weight: bold; border-bottom: 1px solid #ddd;">Reference Version</div>
                    <div style="background: #f8f9fa; padding: 10px; font-weight: bold; border-bottom: 1px solid #ddd;">Current Version</div>
                    <div style="max-height: 400px; overflow-y: auto; padding: 15px; font-family: monospace; font-size: 0.85em; white-space: pre-wrap; background: #f8d7da;">` + oldText + `</div>
                    <div style="max-height: 400px; overflow-y: auto; padding: 15px; font-family: monospace; font-size: 0.85em; white-space: pre-wrap; background: #d4edda;">` + newText + `</div>
                </div>
            `;
        }}
    }}
    function toggleDiffMode(containerId, mode) {{
        var container = document.getElementById(containerId);
        var buttons = container.parentElement.querySelectorAll('.diff-controls button:not(.context-btn)');
        
        // Update button states
        buttons.forEach(btn => btn.classList.remove('active'));
        event.target.classList.add('active');
        
        // Get stored data from JSON script tag
        var dataScript = document.getElementById(containerId + '-data');
        if (!dataScript) {{
            console.error('No data script found for container:', containerId);
            return;
        }}
        
        var data;
        try {{
            data = JSON.parse(dataScript.textContent);
        }} catch (e) {{
            console.error('Failed to parse JSON data for container:', containerId, e);
            return;
        }}
        
        var oldText = data.oldText;
        var newText = data.newText;
        var fileName = data.fileName;
        
        if (oldText && newText && fileName) {{
            // For now, our simple diff viewer only supports side-by-side mode
            // Just recreate the diff viewer
            createDiff2HtmlViewer(containerId, oldText, newText, fileName, 3);
        }}
    }}
    function toggleDiffContext(containerId, contextLines) {{
        var container = document.getElementById(containerId);
        var buttons = container.parentElement.querySelectorAll('.context-btn');
        
        // Update button states
        buttons.forEach(btn => btn.classList.remove('active'));
        event.target.classList.add('active');
        
        // Get stored data from JSON script tag
        var dataScript = document.getElementById(containerId + '-data');
        if (!dataScript) {{
            console.error('No data script found for container:', containerId);
            return;
        }}
        
        var data;
        try {{
            data = JSON.parse(dataScript.textContent);
        }} catch (e) {{
            console.error('Failed to parse JSON data for container:', containerId, e);
            return;
        }}
        
        var oldText = data.oldText;
        var newText = data.newText;
        var fileName = data.fileName;
        
        if (oldText && newText && fileName) {{
            // Recreate the diff viewer with the new context
            createDiff2HtmlViewer(containerId, oldText, newText, fileName, contextLines);
        }}
         }}
    function showTab(tabId) {{
        // Hide all tab contents
        document.querySelectorAll('.tab-content').forEach(function(content) {{
            content.classList.remove('active');
        }});
        // Remove active class from all tabs
        document.querySelectorAll('.tab').forEach(function(tab) {{
            tab.classList.remove('active');
        }});
        // Show selected tab content
        document.getElementById(tabId).classList.add('active');
        // Mark selected tab as active
        event.target.classList.add('active');
    }}
    document.addEventListener('DOMContentLoaded', function() {{
        console.log('DOM loaded, initializing diff viewers');
        // For each .diff-container, call createDiff2HtmlViewer with data attributes
        var containers = document.querySelectorAll('.diff-container');
        console.log('Found', containers.length, 'diff containers');
        
        containers.forEach(function(container) {{
            // Read data from JSON script tag
            var dataScript = document.getElementById(container.id + '-data');
            if (!dataScript) {{
                console.error('No data script found for container:', container.id);
                return;
            }}
            
            var data;
            try {{
                data = JSON.parse(dataScript.textContent);
            }} catch (e) {{
                console.error('Failed to parse JSON data for container:', container.id, e);
                return;
            }}
            
            var oldText = data.oldText;
            var newText = data.newText;
            var fileName = data.fileName;
            
            console.log('Processing container:', container.id, 'fileName:', fileName);
            console.log('Has old text:', !!oldText, 'Has new text:', !!newText);
            console.log('Old text length:', oldText ? oldText.length : 0);
            console.log('New text length:', newText ? newText.length : 0);
            
            if (oldText && newText && fileName) {{
                // Handle case where JSON.parse resulted in empty string
                oldText = oldText || "";
                newText = newText || "";
                console.log('Calling createDiff2HtmlViewer for:', fileName);
                createDiff2HtmlViewer(container.id, oldText, newText, fileName, 3);
            }} else {{
                console.log('Missing data for container:', container.id);
                console.log('  oldText is null:', oldText === null);
                console.log('  newText is null:', newText === null);
                console.log('  fileName is null:', fileName === null);
                container.innerHTML = '<p style="padding: 20px; color: #666;">❌ Missing diff data</p>';
            }}
        }});
    }});
    </script>
</body>
</html>
    """
    
    # Generate summary cards
    stats = summary['statistics']
    summary_cards = []
    
    summary_cards.append(f"""
        <div class="stat-card">
            <div class="stat-number">{summary['total_differences']}</div>
            <div class="stat-label">Total Differences</div>
        </div>
    """)
    
    for label, value in [("Added", stats['added']), ("Removed", stats['removed']), ("Changed", stats['changed'])]:
        summary_cards.append(f"""
            <div class="stat-card">
                <div class="stat-number">{value}</div>
                <div class="stat-label">{label}</div>
            </div>
        """)
    
    for label, value in [("Major", stats['major']), ("Minor", stats['minor']), ("Patch", stats['patch'])]:
        summary_cards.append(f"""
            <div class="stat-card">
                <div class="stat-number">{value}</div>
                <div class="stat-label">{label}</div>
            </div>
        """)
    
    # Generate API overview section
    api_overview_html = ""
    if reference_stats and current_stats:
        api_overview_html = f"""
            <h2>📈 API Overview</h2>
            <div class="summary">
                <div class="stat-card">
                    <div class="stat-number">{reference_stats.get('total_modules', 0)}</div>
                    <div class="stat-label">Reference Modules</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{current_stats.get('total_modules', 0)}</div>
                    <div class="stat-label">Current Modules</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{reference_stats.get('total_classes', 0)}</div>
                    <div class="stat-label">Reference Classes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{current_stats.get('total_classes', 0)}</div>
                    <div class="stat-label">Current Classes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{reference_stats.get('total_functions', 0)}</div>
                    <div class="stat-label">Reference Functions</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{current_stats.get('total_functions', 0)}</div>
                    <div class="stat-label">Current Functions</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{reference_stats.get('total_methods', 0)}</div>
                    <div class="stat-label">Reference Methods</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{current_stats.get('total_methods', 0)}</div>
                    <div class="stat-label">Current Methods</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{reference_stats.get('total_properties', 0)}</div>
                    <div class="stat-label">Reference Properties</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{current_stats.get('total_properties', 0)}</div>
                    <div class="stat-label">Current Properties</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{reference_stats.get('total_api_items', 0)}</div>
                    <div class="stat-label">Reference Total API Items</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{current_stats.get('total_api_items', 0)}</div>
                    <div class="stat-label">Current Total API Items</div>
                </div>
            </div>
        """
    
    # Generate differences HTML
    differences_html = []
    
    # Group by severity
    by_severity = {
        "major": [d for d in differences if d.get_severity() == "major"],
        "minor": [d for d in differences if d.get_severity() == "minor"],
        "patch": [d for d in differences if d.get_severity() == "patch"]
    }
    
    for severity in ["major", "minor", "patch"]:
        diffs = by_severity[severity]
        if not diffs:
            continue
        
        differences_html.append(f"<h3>{severity.upper()} Changes ({len(diffs)})</h3>")
        
        for diff in diffs:
            diff_html = f"""
            <div class="difference">
                <div class="diff-header">
                    <span class="diff-path">{html.escape(diff.path)}</span>
                    <span class="diff-type {diff.diff_type}">{diff.diff_type}</span>
                    <span class="severity {diff.get_severity()}">{diff.get_severity()}</span>
                </div>
                <div class="diff-details">
                    <div><strong>{html.escape(diff.get_description())}</strong></div>
            """
            
            # Add detailed change information
            if diff.details:
                for change_type, change_data in diff.details.items():
                    if change_type == "signature":
                        diff_html += f"""
                        <div class="change-item">
                            <div class="change-label">Signature Change:</div>
                            <div><span class="code old">{html.escape(str(change_data['old']))}</span></div>
                            <div><span class="code new">{html.escape(str(change_data['new']))}</span></div>
                        </div>
                        """
                    elif change_type == "documentation":
                        old_len = change_data['old_length']
                        new_len = change_data['new_length']
                        old_doc = change_data.get('old_doc', '')
                        new_doc = change_data.get('new_doc', '')
                        
                        # Create side-by-side diff view
                        diff_html += f"""
                        <div class="change-item">
                            <div class="change-label">Documentation:</div>
                            <div>Length: {old_len} → {new_len} characters</div>
                            <div class="doc-diff">
                                <div class="doc-side">
                                    <div class="doc-header">Reference Version</div>
                                    <pre class="doc-content">{html.escape(old_doc)}</pre>
                                </div>
                                <div class="doc-side">
                                    <div class="doc-header">Current Version</div>
                                    <pre class="doc-content">{html.escape(new_doc)}</pre>
                                </div>
                            </div>
                        </div>
                        """
                    elif change_type == "parameters":
                        diff_html += """<div class="change-item"><div class="change-label">Parameters:</div>"""
                        if "parameter_names" in change_data:
                            param_names = change_data["parameter_names"]
                            if param_names.get("added"):
                                diff_html += f"<div>Added: {', '.join(param_names['added'])}</div>"
                            if param_names.get("removed"):
                                diff_html += f"<div>Removed: {', '.join(param_names['removed'])}</div>"
                        diff_html += "</div>"
            
            diff_html += """
                </div>
            </div>
            """
            differences_html.append(diff_html)
    
    # Generate pydoc differences HTML
    pydoc_differences_html = generate_pydoc_differences_html(
        reference_data, current_data, differences, reference_file, current_file
    )
    
    # Generate final HTML
    return html_template.format(
        reference_file=html.escape(reference_file),
        current_file=html.escape(current_file),
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        summary_cards='\n'.join(summary_cards),
        api_overview_html=api_overview_html,
        differences_html='\n'.join(differences_html),
        pydoc_differences_html=pydoc_differences_html
    )


def generate_pydoc_differences_html(reference_data: Dict[str, Any], 
                                  current_data: Dict[str, Any],
                                  differences: List[APIDifference],
                                  reference_file: str = None,
                                  current_file: str = None) -> str:
    """Generate HTML for pydoc documentation differences using side-by-side diff view"""
    
    if not reference_data or not current_data:
        return "<p>No pydoc documentation data available for comparison.</p>"
    
    html_parts = []
    
    # Load documentation files if available
    ref_docs = {}
    cur_docs = {}
    
    if reference_file:
        try:
            ref_docs = load_documentation_files(reference_data, Path(reference_file))
        except Exception as e:
            print(f"⚠️  Failed to load reference documentation files: {e}")
    
    if current_file:
        try:
            cur_docs = load_documentation_files(current_data, Path(current_file))
        except Exception as e:
            print(f"⚠️  Failed to load current documentation files: {e}")
    
    # Get all available modules
    all_modules = set(ref_docs.keys()) | set(cur_docs.keys())
    
    if not all_modules:
        return "<p>No documentation files found for comparison.</p>"
    
    html_parts.append("<h3>📚 Documentation Comparison</h3>")
    html_parts.append("<p>Side-by-side comparison of pydoc documentation for each module:</p>")
    
    for module_name in sorted(all_modules):
        ref_text = ref_docs.get(module_name, "")
        cur_text = cur_docs.get(module_name, "")
        
        print(f"🔍 Processing module: {module_name}")
        print(f"   Reference text length: {len(ref_text)}")
        print(f"   Current text length: {len(cur_text)}")
        
        if ref_text and cur_text:
            # Both versions available - show side-by-side diff
            print(f"   → Generating diff: both versions available")
            html_parts.append(generate_side_by_side_diff_html(ref_text, cur_text, module_name))
        elif ref_text:
            # Only reference available - use empty string for current
            print(f"   → Generating diff: reference only")
            html_parts.append(generate_side_by_side_diff_html(ref_text, "", module_name))
        elif cur_text:
            # Only current available - use empty string for reference
            print(f"   → Generating diff: current only")
            html_parts.append(generate_side_by_side_diff_html("", cur_text, module_name))
        else:
            print(f"   → Skipping: no documentation found")
    
    return '\n'.join(html_parts)


def compare_api_dumps(reference_file: str, current_file: str, 
                     output_file: str = None, text_only: bool = False) -> None:
    """Compare two API dumps and generate a report"""
    
    print(f"🔍 Loading reference API: {reference_file}")
    reference_data = load_api_dump(Path(reference_file))
    
    print(f"🔍 Loading current API: {current_file}")
    current_data = load_api_dump(Path(current_file))
    
    print("⚖️  Comparing APIs...")
    differ = PylonAPIDiffer()
    differences = differ.compare_apis(reference_data, current_data)
    summary = differ.get_summary()
    
    print(f"✅ Found {len(differences)} differences")
    
    # Generate reports
    if text_only or not output_file:
        # Generate text report
        text_report = generate_text_report(differences, summary, reference_file, current_file)
        
        if output_file:
            output_path = Path(output_file)
            if output_path.suffix.lower() != '.txt':
                output_path = output_path.with_suffix('.txt')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text_report)
            print(f"📄 Text report saved to: {output_path}")
        else:
            print("\n" + text_report)
    else:
        # Extract global statistics from API dumps
        reference_stats = reference_data.get("global_stats", {})
        current_stats = current_data.get("global_stats", {})
        
        # Generate HTML report
        html_report = generate_html_report(
            differences, summary, reference_file, current_file,
            reference_stats, current_stats, reference_data, current_data
        )
        
        output_path = Path(output_file)
        if output_path.suffix.lower() not in ['.html', '.htm']:
            output_path = output_path.with_suffix('.html')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_report)
        print(f"📄 HTML report saved to: {output_path}")
    
    # Print summary to console
    print(f"\n📊 Summary:")
    print(f"   Total differences: {summary['total_differences']}")
    print(f"   Added: {summary['statistics']['added']}")
    print(f"   Removed: {summary['statistics']['removed']}")
    print(f"   Changed: {summary['statistics']['changed']}")
    print(f"   Major: {summary['statistics']['major']} | Minor: {summary['statistics']['minor']} | Patch: {summary['statistics']['patch']}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Compare pypylon API dumps and identify differences",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compare two API dumps with HTML report
  python pypylon_api_differ.py reference.json current.json --output report.html
  
  # Generate text-only report
  python pypylon_api_differ.py old_api.json new_api.json --text-only
  
  # Save text report to file
  python pypylon_api_differ.py old_api.json new_api.json --output diff.txt --text-only
        """
    )
    
    parser.add_argument("reference", help="Reference API dump file (JSON)")
    parser.add_argument("current", help="Current API dump file (JSON)")
    parser.add_argument("--output", "-o", help="Output report file (HTML or TXT)")
    parser.add_argument("--text-only", action="store_true", help="Generate text report instead of HTML")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    try:
        compare_api_dumps(
            reference_file=args.reference,
            current_file=args.current,
            output_file=args.output,
            text_only=args.text_only
        )
        
        print(f"\n✅ API comparison completed successfully!")
        
    except Exception as e:
        print(f"❌ Error comparing APIs: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 
