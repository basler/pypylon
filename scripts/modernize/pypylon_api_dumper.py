#!/usr/bin/env python3
"""
PyPylon API Dumper

Extracts comprehensive API information from pypylon and saves it to JSON format.
This creates a complete snapshot of the public API for compatibility checking.

Usage:
    python pypylon_api_dumper.py --output pypylon_api_v4.2.0.json
    python pypylon_api_dumper.py --python-env /path/to/venv/bin/python --output pypylon_local.json
"""

import argparse
import json
import subprocess
import sys
import inspect
import types
import warnings
from pathlib import Path
from typing import Dict, Any, List, Optional, Union, Set
import hashlib
from datetime import datetime
import os
import io
import pydoc

# Always disable pagers for pydoc
os.environ["PAGER"] = "cat"

# Suppress warnings during introspection
warnings.filterwarnings("ignore")

class PylonAPIExtractor:
    """Extracts comprehensive API information from pypylon modules"""
    
    def __init__(self, python_executable: str = None):
        self.python_executable = python_executable or sys.executable
    
    def extract_api(self) -> Dict[str, Any]:
        """Extract complete API information from pypylon"""
        
        # Create extraction script
        script = self._generate_extraction_script()
        
        # Set environment for camera emulation
        env = os.environ.copy()
        env["PYLON_CAMEMU"] = "1"
        
        # Run extraction in target environment
        print(f"🔍 Running extraction subprocess...")
        print(f"   Python: {self.python_executable}")
        print(f"   Environment: PYLON_CAMEMU={env.get('PYLON_CAMEMU', 'not set')}")
        
        result = subprocess.run(
            [self.python_executable, "-c", script],
            capture_output=True,
            text=True,
            env=env,
            timeout=300  # 5 minute timeout
        )
        
        print(f"   Return code: {result.returncode}")
        print(f"   STDERR length: {len(result.stderr)}")
        print(f"   STDOUT length: {len(result.stdout)}")
        
        # Show stderr if there's any
        if result.stderr:
            print("📋 STDERR output:")
            for i, line in enumerate(result.stderr.splitlines()[:20]):  # First 20 lines
                print(f"   {i+1:2d}: {line}")
            if len(result.stderr.splitlines()) > 20:
                print(f"   ... and {len(result.stderr.splitlines()) - 20} more lines")
        
        if result.returncode != 0:
            print("❌ Subprocess failed!")
            if result.stdout:
                print("📋 STDOUT output:")
                for i, line in enumerate(result.stdout.splitlines()[:10]):
                    print(f"   {i+1:2d}: {line}")
            raise RuntimeError(f"API extraction subprocess failed with code {result.returncode}\nSTDERR: {result.stderr[:1000]}\nSTDOUT: {result.stdout[:1000]}")
        
        # Try to parse JSON output
        if not result.stdout.strip():
            raise RuntimeError("No output from extraction subprocess")
        
        try:
            # Show first few lines of stdout for debugging
            stdout_lines = result.stdout.splitlines()
            print(f"📋 STDOUT preview (first 5 lines):")
            for i, line in enumerate(stdout_lines[:5]):
                print(f"   {i+1:2d}: {line[:100]}{'...' if len(line) > 100 else ''}")
            
            return json.loads(result.stdout)
        except json.JSONDecodeError as e:
            print("❌ JSON parsing failed!")
            print(f"   Error: {e}")
            print(f"   Position: {e.pos if hasattr(e, 'pos') else 'unknown'}")
            # Show the problematic part of the output
            stdout_preview = result.stdout[:2000] if len(result.stdout) > 2000 else result.stdout
            print(f"📋 Raw output preview:\n{stdout_preview}")
            raise RuntimeError(f"Failed to parse JSON from subprocess output: {e}\nFirst 1000 chars: {result.stdout[:1000]}")
    
    def _generate_extraction_script(self) -> str:
        """Generate Python script for comprehensive API extraction"""
        return '''
import sys
import inspect
import json
import types
import warnings
import platform
import os
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import traceback
import io
import pydoc

# Suppress warnings during introspection
warnings.filterwarnings("ignore")

def get_pydoc_documentation(module_name):
    """Get pydoc documentation for a module"""
    try:
        # Import the module
        module = __import__(module_name)
        
        # For submodules, try to get the actual submodule object
        if "." in module_name:
            parts = module_name.split(".")
            current = module
            for part in parts[1:]:  # Skip the first part (already imported)
                try:
                    current = getattr(current, part)
                except AttributeError:
                    # If we can't get the submodule, fall back to the parent
                    print(f"Warning: Could not access submodule {part} in {module_name}, using parent", file=sys.stderr)
                    break
        
        # Use the reliable stdout capture method that works well
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        try:
            # Get pydoc documentation using help() - this is the most reliable method
            pydoc.help(current)
            doc_output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout
        
        # Check if we got reasonable output and it's not just the parent package
        if len(doc_output) < 50 or (module_name != "pypylon" and "Help on package pypylon" in doc_output):
            print(f"Warning: Got parent package documentation for {module_name}, trying manual extraction", file=sys.stderr)
            
            # Try to manually extract submodule documentation
            try:
                # For submodules, try to get specific documentation
                if "." in module_name:
                    doc_parts = []
                    doc_parts.append(f"Help on module {module_name}")
                    doc_parts.append("=" * (len(module_name) + 15))
                    doc_parts.append("")
                    
                    # Try to get the actual submodule
                    submodule_name = module_name.split(".")[-1]
                    try:
                        submodule = getattr(module, submodule_name)
                        
                        if hasattr(submodule, "__doc__") and submodule.__doc__:
                            doc_parts.append("DESCRIPTION")
                            doc_parts.append("-" * 12)
                            doc_parts.append(submodule.__doc__)
                            doc_parts.append("")
                        
                        # Get all public attributes from the submodule
                        public_attrs = [attr for attr in dir(submodule) if not attr.startswith("_")]
                        
                        if public_attrs:
                            doc_parts.append("PUBLIC ATTRIBUTES")
                            doc_parts.append("-" * 17)
                            for attr_name in sorted(public_attrs):
                                try:
                                    attr = getattr(submodule, attr_name)
                                    attr_type = type(attr).__name__
                                    doc_parts.append(f"{attr_name} ({attr_type})")
                                    
                                    # Get docstring if available
                                    if hasattr(attr, "__doc__") and attr.__doc__:
                                        doc_lines = attr.__doc__.strip().split('\\n')
                                        for line in doc_lines[:3]:  # First 3 lines
                                            doc_parts.append(f"    {line}")
                                        if len(doc_lines) > 3:
                                            doc_parts.append("    ...")
                                except Exception:
                                    doc_parts.append(f"{attr_name} (inaccessible)")
                                doc_parts.append("")
                        
                        doc_output = "\\n".join(doc_parts)
                        print(f"Manual extraction for {module_name}: {len(doc_output)} chars", file=sys.stderr)
                        
                    except AttributeError:
                        # If we can't get the submodule, try to find it in the package
                        print(f"Could not find submodule {submodule_name} in {module_name}", file=sys.stderr)
                        
                        # List what's available in the module
                        doc_parts = []
                        doc_parts.append(f"Help on module {module_name}")
                        doc_parts.append("=" * (len(module_name) + 15))
                        doc_parts.append("")
                        doc_parts.append("NOTE: This module may not be directly accessible.")
                        doc_parts.append("Available attributes in parent module:")
                        doc_parts.append("")
                        
                        public_attrs = [attr for attr in dir(module) if not attr.startswith("_")]
                        for attr_name in sorted(public_attrs):
                            try:
                                attr = getattr(module, attr_name)
                                attr_type = type(attr).__name__
                                doc_parts.append(f"{attr_name} ({attr_type})")
                            except Exception:
                                doc_parts.append(f"{attr_name} (inaccessible)")
                            doc_parts.append("")
                        
                        doc_output = "\\n".join(doc_parts)
                
                else:
                    # For top-level modules, use the original fallback
                    try:
                        doc_output = pydoc.text.document(module)
                    except Exception as fallback_error:
                        print(f"Fallback also failed for {module_name}: {fallback_error}", file=sys.stderr)
                        # Use manual inspection as last resort
                        doc_parts = []
                        doc_parts.append(f"Help on module {module_name}")
                        doc_parts.append("=" * (len(module_name) + 15))
                        doc_parts.append("")
                        
                        if hasattr(module, "__doc__") and module.__doc__:
                            doc_parts.append("DESCRIPTION")
                            doc_parts.append("-" * 12)
                            doc_parts.append(module.__doc__)
                            doc_parts.append("")
                        
                        # Get all public attributes
                        public_attrs = [attr for attr in dir(module) if not attr.startswith("_")]
                        
                        if public_attrs:
                            doc_parts.append("PUBLIC ATTRIBUTES")
                            doc_parts.append("-" * 17)
                            for attr_name in sorted(public_attrs):
                                try:
                                    attr = getattr(module, attr_name)
                                    attr_type = type(attr).__name__
                                    doc_parts.append(f"{attr_name} ({attr_type})")
                                    
                                    # Get docstring if available
                                    if hasattr(attr, "__doc__") and attr.__doc__:
                                        doc_lines = attr.__doc__.strip().split('\\n')
                                        for line in doc_lines[:3]:  # First 3 lines
                                            doc_parts.append(f"    {line}")
                                        if len(doc_lines) > 3:
                                            doc_parts.append("    ...")
                                except Exception:
                                    doc_parts.append(f"{attr_name} (inaccessible)")
                                doc_parts.append("")
                        
                        doc_output = "\\n".join(doc_parts)
                        
            except Exception as manual_error:
                print(f"Manual extraction failed for {module_name}: {manual_error}", file=sys.stderr)
                # Use the original output as fallback
                pass
        
        return {
            "module_name": module_name,
            "documentation": doc_output,
            "doc_length": len(doc_output),
            "doc_lines": doc_output.count('\\n'),
            "success": True
        }
            
    except Exception as e:
        return {
            "module_name": module_name,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "success": False
        }

def safe_getattr(obj, name, default=None):
    """Safely get attribute, handling access errors"""
    try:
        return getattr(obj, name, default)
    except Exception:
        return default

def safe_str(obj, max_length=500):
    """Safely convert object to string with length limit"""
    try:
        s = str(obj)
        if len(s) > max_length:
            return s[:max_length] + "..."
        return s
    except Exception:
        return "<repr_error>"

def safe_repr(obj, max_length=200):
    """Safely get repr of object"""
    try:
        r = repr(obj)
        if len(r) > max_length:
            return r[:max_length] + "..."
        return r
    except Exception:
        return "<repr_error>"

def get_signature_info(func):
    """Extract comprehensive function signature information"""
    try:
        sig = inspect.signature(func)
        
        params = {}
        for name, param in sig.parameters.items():
            param_info = {
                "name": name,
                "kind": param.kind.name,
                "has_default": param.default != param.empty,
                "default_value": safe_str(param.default) if param.default != param.empty else None,
                "default_repr": safe_repr(param.default) if param.default != param.empty else None,
                "has_annotation": param.annotation != param.empty,
                "annotation": safe_str(param.annotation) if param.annotation != param.empty else None
            }
            params[name] = param_info
        
        return {
            "signature_str": str(sig),
            "parameters": params,
            "parameter_count": len(sig.parameters),
            "has_return_annotation": sig.return_annotation != sig.empty,
            "return_annotation": safe_str(sig.return_annotation) if sig.return_annotation != sig.empty else None,
            "callable": True
        }
    except Exception as e:
        return {
            "signature_str": "unavailable",
            "error": str(e),
            "callable": callable(func)
        }

def analyze_function(func, name=None):
    """Analyze a function or method comprehensively"""
    if name is None:
        name = safe_getattr(func, "__name__", "unknown")
    
    info = {
        "name": name,
        "type": "function",
        "doc": safe_getattr(func, "__doc__"),
        "module": safe_getattr(func, "__module__"),
        "qualname": safe_getattr(func, "__qualname__"),
        "file": safe_getattr(safe_getattr(func, "__code__"), "co_filename") if hasattr(func, "__code__") else None,
        "lineno": safe_getattr(safe_getattr(func, "__code__"), "co_firstlineno") if hasattr(func, "__code__") else None,
        "is_builtin": inspect.isbuiltin(func),
        "is_method": inspect.ismethod(func),
        "is_function": inspect.isfunction(func),
        "is_coroutine": inspect.iscoroutinefunction(func),
        "is_generator": inspect.isgeneratorfunction(func),
        "is_async_generator": inspect.isasyncgenfunction(func),
    }
    
    # Add comprehensive signature information
    info.update(get_signature_info(func))
    
    # Add docstring analysis
    if info["doc"]:
        info["doc_length"] = len(info["doc"])
        info["doc_lines"] = info["doc"].count('\\n') + 1
        info["has_parameters_doc"] = "Parameters" in info["doc"] or "Args:" in info["doc"]
        info["has_returns_doc"] = "Returns" in info["doc"] or "Return:" in info["doc"]
        info["has_examples_doc"] = "Example" in info["doc"]
    else:
        info["doc_length"] = 0
        info["doc_lines"] = 0
        info["has_parameters_doc"] = False
        info["has_returns_doc"] = False
        info["has_examples_doc"] = False
    
    return info

def analyze_property(prop, name):
    """Analyze a property"""
    return {
        "name": name,
        "type": "property",
        "doc": safe_getattr(prop, "__doc__"),
        "has_getter": prop.fget is not None,
        "has_setter": prop.fset is not None,
        "has_deleter": prop.fdel is not None,
        "getter_doc": safe_getattr(prop.fget, "__doc__") if prop.fget else None,
        "setter_doc": safe_getattr(prop.fset, "__doc__") if prop.fset else None,
        "deleter_doc": safe_getattr(prop.fdel, "__doc__") if prop.fdel else None
    }

def analyze_class(cls, name=None):
    """Analyze a class and all its members comprehensively"""
    if name is None:
        name = safe_getattr(cls, "__name__", "unknown")
    
    info = {
        "name": name,
        "type": "class",
        "doc": safe_getattr(cls, "__doc__"),
        "module": safe_getattr(cls, "__module__"),
        "qualname": safe_getattr(cls, "__qualname__"),
        "file": safe_getattr(cls, "__file__", None),
        "bases": [safe_getattr(base, "__name__", str(base)) for base in safe_getattr(cls, "__bases__", [])],
        "mro": [safe_getattr(c, "__name__", str(c)) for c in safe_getattr(cls, "__mro__", [])],
        "is_abstract": inspect.isabstract(cls),
        "methods": {},
        "properties": {},
        "class_attributes": {},
        "static_methods": {},
        "class_methods": {},
        "special_methods": {},
        "nested_classes": {}
    }
    
    # Add docstring analysis
    if info["doc"]:
        info["doc_length"] = len(info["doc"])
        info["doc_lines"] = info["doc"].count('\\n') + 1
    else:
        info["doc_length"] = 0
        info["doc_lines"] = 0
    
    # Get all attributes including inherited ones
    all_attrs = set()
    try:
        all_attrs.update(dir(cls))
    except Exception as e:
        print(f"Warning: Could not get dir() for class {name}: {e}", file=sys.stderr)
        return info  # Return early if we can't even get the directory
    
    # Analyze each attribute
    for attr_name in all_attrs:
        try:
            attr = getattr(cls, attr_name)
            
            # Categorize the attribute
            if attr_name.startswith("__") and attr_name.endswith("__"):
                # Special methods
                if callable(attr):
                    info["special_methods"][attr_name] = analyze_function(attr, attr_name)
            elif inspect.ismethod(attr):
                info["methods"][attr_name] = analyze_function(attr, attr_name)
            elif inspect.isfunction(attr):
                if hasattr(attr, "__self__") and attr.__self__ is cls:
                    info["class_methods"][attr_name] = analyze_function(attr, attr_name)
                else:
                    info["methods"][attr_name] = analyze_function(attr, attr_name)
            elif isinstance(attr, staticmethod):
                info["static_methods"][attr_name] = analyze_function(attr.__func__, attr_name)
            elif isinstance(attr, classmethod):
                info["class_methods"][attr_name] = analyze_function(attr.__func__, attr_name)
            elif isinstance(attr, property):
                info["properties"][attr_name] = analyze_property(attr, attr_name)
            elif inspect.isclass(attr):
                # Nested class
                info["nested_classes"][attr_name] = analyze_class(attr, attr_name)
            else:
                # Class attribute/constant
                info["class_attributes"][attr_name] = {
                    "name": attr_name,
                    "type": type(attr).__name__,
                    "value": safe_str(attr, 100),
                    "repr": safe_repr(attr, 100),
                    "is_callable": callable(attr),
                    "value_type": str(type(attr))
                }
        except Exception as e:
            # Record inaccessible attributes
            info["class_attributes"][attr_name] = {
                "name": attr_name,
                "type": "inaccessible",
                "error": str(e),
                "is_callable": False
            }
    
    # Add summary statistics
    info["stats"] = {
        "total_methods": len(info["methods"]),
        "total_properties": len(info["properties"]),
        "total_class_attributes": len(info["class_attributes"]),
        "total_static_methods": len(info["static_methods"]),
        "total_class_methods": len(info["class_methods"]),
        "total_special_methods": len(info["special_methods"]),
        "total_nested_classes": len(info["nested_classes"]),
        "inheritance_depth": len(info["mro"]) - 1  # -1 to exclude the class itself
    }
    
    return info

def analyze_module(module, name=None, depth=0, max_depth=3):
    """Analyze a module and its contents comprehensively"""
    if name is None:
        name = safe_getattr(module, "__name__", "unknown")
    
    print(f"📦 Analyzing module: {name} (depth {depth})", file=sys.stderr)
    
    if depth > max_depth:
        print(f"⚠️  Module {name} too deep (depth {depth} > {max_depth})", file=sys.stderr)
        return {
            "name": name,
            "type": "module_too_deep",
            "depth_exceeded": True
        }
    
    info = {
        "name": name,
        "type": "module",
        "doc": safe_getattr(module, "__doc__"),
        "file": safe_getattr(module, "__file__"),
        "package": safe_getattr(module, "__package__"),
        "version": safe_getattr(module, "__version__", "unknown"),
        "all": safe_getattr(module, "__all__", None),
        "loader": str(safe_getattr(module, "__loader__", None)),
        "spec": str(safe_getattr(module, "__spec__", None)),
        "classes": {},
        "functions": {},
        "constants": {},
        "submodules": {},
        "exceptions": {},
        "variables": {}
    }
    
    # Add docstring analysis
    if info["doc"]:
        info["doc_length"] = len(info["doc"])
        info["doc_lines"] = info["doc"].count('\\n') + 1
    else:
        info["doc_length"] = 0
        info["doc_lines"] = 0
    
    # Get all public attributes (respect __all__ if it exists)
    if info["all"] is not None:
        public_attrs = info["all"]
    else:
        try:
            all_attrs = dir(module)
            public_attrs = [attr for attr in all_attrs if not attr.startswith("_")]
        except Exception as e:
            print(f"Warning: Could not get dir() for module {name}: {e}", file=sys.stderr)
            public_attrs = []
    
    # Analyze each public attribute
    for attr_name in public_attrs:
        try:
            attr = getattr(module, attr_name)
            
            if inspect.ismodule(attr):
                # Submodule
                if attr.__name__.startswith(name + "."):
                    # Internal submodule - analyze recursively
                    info["submodules"][attr_name] = analyze_module(attr, attr_name, depth + 1, max_depth)
                else:
                    # External module reference
                    info["submodules"][attr_name] = {
                        "name": attr_name,
                        "type": "external_module",
                        "module_name": attr.__name__,
                        "file": safe_getattr(attr, "__file__")
                    }
            elif inspect.isclass(attr):
                if issubclass(attr, Exception):
                    info["exceptions"][attr_name] = analyze_class(attr, attr_name)
                else:
                    info["classes"][attr_name] = analyze_class(attr, attr_name)
            elif inspect.isfunction(attr):
                info["functions"][attr_name] = analyze_function(attr, attr_name)
            elif callable(attr):
                # Callable object (might be builtin function, method, etc.)
                info["functions"][attr_name] = analyze_function(attr, attr_name)
            else:
                # Constant, variable, or other object
                info["constants"][attr_name] = {
                    "name": attr_name,
                    "type": type(attr).__name__,
                    "value": safe_str(attr, 200),
                    "repr": safe_repr(attr, 200),
                    "is_callable": callable(attr),
                    "value_type": str(type(attr))
                }
        except Exception as e:
            # Record inaccessible attributes
            info["constants"][attr_name] = {
                "name": attr_name,
                "type": "inaccessible",
                "error": str(e),
                "is_callable": False
            }
    
    # Add summary statistics
    info["stats"] = {
        "total_classes": len(info["classes"]),
        "total_functions": len(info["functions"]),
        "total_constants": len(info["constants"]),
        "total_submodules": len(info["submodules"]),
        "total_exceptions": len(info["exceptions"]),
        "total_public_attrs": len(public_attrs),
        "has_all_attribute": info["all"] is not None,
        "all_attribute_count": len(info["all"]) if info["all"] else 0
    }
    
    print(f"✅ Module {name} analyzed: {info['stats']['total_classes']} classes, {info['stats']['total_functions']} functions", file=sys.stderr)
    return info

def get_system_info():
    """Get comprehensive system and Python environment information"""
    import platform
    import sys
    
    return {
        "python_version": sys.version,
        "python_version_info": {
            "major": sys.version_info.major,
            "minor": sys.version_info.minor,
            "micro": sys.version_info.micro,
            "releaselevel": sys.version_info.releaselevel,
            "serial": sys.version_info.serial
        },
        "platform": platform.platform(),
        "architecture": platform.architecture(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "system": platform.system(),
        "python_executable": sys.executable,
        "python_path": sys.path[:10],  # First 10 entries
        "environment_vars": {
            "PYLON_CAMEMU": os.environ.get("PYLON_CAMEMU"),
            "PYTHONPATH": os.environ.get("PYTHONPATH"),
            "PATH": os.environ.get("PATH", "")[:500]  # Truncate PATH
        }
    }

def extract_pypylon_api():
    """Main extraction function for pypylon API"""
    try:
        print("📊 Creating API data structure...", file=sys.stderr)
        api_data = {
            "metadata": {
                "extraction_time": datetime.now().isoformat(),
                "extractor_version": "2.0.0",
                "extraction_type": "comprehensive",
                "system_info": get_system_info()
            },
            "modules": {},
            "pydoc_documentation": {}
        }
        print("✅ API data structure created", file=sys.stderr)
        
        # Primary modules to analyze
        primary_modules = ["pypylon"]
        
        for module_name in primary_modules:
            try:
                print(f"Importing {module_name}...", file=sys.stderr)
                module = __import__(module_name)
                print(f"Analyzing {module_name}...", file=sys.stderr)
                api_data["modules"][module_name] = analyze_module(module, module_name)
                print(f"Successfully analyzed {module_name}", file=sys.stderr)
                
                # For pypylon, explicitly import and analyze known submodules
                # This ensures consistent analysis regardless of how they're exposed
                if module_name == "pypylon":
                    known_submodules = ["genicam", "pylon", "pylondataprocessing"]
                    for submodule_name in known_submodules:
                        try:
                            print(f"Importing {module_name}.{submodule_name}...", file=sys.stderr)
                            submodule = __import__(f"{module_name}.{submodule_name}", fromlist=[submodule_name])
                            print(f"Analyzing {submodule_name}...", file=sys.stderr)
                            
                            # Add the submodule to the main module's submodules
                            if "submodules" not in api_data["modules"][module_name]:
                                api_data["modules"][module_name]["submodules"] = {}
                            
                            api_data["modules"][module_name]["submodules"][submodule_name] = analyze_module(
                                submodule, submodule_name, depth=1, max_depth=3
                            )
                            print(f"Successfully analyzed {submodule_name}", file=sys.stderr)
                            
                        except ImportError as e:
                            print(f"ImportError for {submodule_name}: {e}", file=sys.stderr)
                            # Add as missing submodule
                            if "submodules" not in api_data["modules"][module_name]:
                                api_data["modules"][module_name]["submodules"] = {}
                            api_data["modules"][module_name]["submodules"][submodule_name] = {
                                "name": submodule_name,
                                "type": "missing_module",
                                "error": str(e),
                                "available": False
                            }
                        except Exception as e:
                            print(f"Error analyzing {submodule_name}: {e}", file=sys.stderr)
                            # Add as error submodule
                            if "submodules" not in api_data["modules"][module_name]:
                                api_data["modules"][module_name]["submodules"] = {}
                            api_data["modules"][module_name]["submodules"][submodule_name] = {
                                "name": submodule_name,
                                "type": "error_module",
                                "error": str(e),
                                "traceback": traceback.format_exc()
                            }
                            
            except ImportError as e:
                print(f"ImportError for {module_name}: {e}", file=sys.stderr)
                api_data["modules"][module_name] = {
                    "name": module_name,
                    "type": "missing_module", 
                    "error": str(e),
                    "available": False
                }
            except Exception as e:
                print(f"Error analyzing {module_name}: {e}", file=sys.stderr)
                api_data["modules"][module_name] = {
                    "name": module_name,
                    "type": "error_module",
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }
        
        # Extract pydoc documentation for key modules
        print("📚 Extracting pydoc documentation...", file=sys.stderr)
        pydoc_modules = ["pypylon.pylon", "pypylon.genicam", "pypylon.pylondataprocessing"]
        
        for module_name in pydoc_modules:
            print(f"📖 Getting pydoc for {module_name}...", file=sys.stderr)
            doc_info = get_pydoc_documentation(module_name)
            api_data["pydoc_documentation"][module_name] = doc_info
            
            if doc_info["success"]:
                print(f"✅ Pydoc extracted for {module_name}: {doc_info['doc_length']} chars, {doc_info['doc_lines']} lines", file=sys.stderr)
                if doc_info.get("fallback_used"):
                    print(f"   ⚠️  Used fallback method for {module_name}", file=sys.stderr)
                # Show first few lines for debugging
                doc_preview = doc_info["documentation"][:500] if len(doc_info["documentation"]) > 500 else doc_info["documentation"]
                print(f"   📄 Preview: {repr(doc_preview)}", file=sys.stderr)
            else:
                print(f"❌ Pydoc failed for {module_name}: {doc_info['error']}", file=sys.stderr)
        
        # Add global statistics
        print("📈 Computing global statistics...", file=sys.stderr)
        total_classes = 0
        total_functions = 0
        total_methods = 0
        total_properties = 0
        
        def count_module_stats(module_data):
            """Recursively count statistics from a module and its submodules"""
            nonlocal total_classes, total_functions, total_methods, total_properties
            
            if isinstance(module_data, dict) and "stats" in module_data:
                total_classes += module_data["stats"].get("total_classes", 0)
                total_functions += module_data["stats"].get("total_functions", 0)
                
                # Count methods and properties from classes
                for class_data in module_data.get("classes", {}).values():
                    if isinstance(class_data, dict) and "stats" in class_data:
                        total_methods += class_data["stats"].get("total_methods", 0)
                        total_properties += class_data["stats"].get("total_properties", 0)
                
                # Recursively count submodules
                for submodule_data in module_data.get("submodules", {}).values():
                    count_module_stats(submodule_data)
        
        for module_name, module_data in api_data["modules"].items():
            count_module_stats(module_data)
        
        api_data["global_stats"] = {
            "total_modules": len([m for m in api_data["modules"].values() if m.get("type") == "module"]),
            "total_classes": total_classes,
            "total_functions": total_functions,
            "total_methods": total_methods,
            "total_properties": total_properties,
            "total_api_items": total_classes + total_functions + total_methods + total_properties
        }
        print(f"✅ Global stats: {total_classes} classes, {total_functions} functions, {total_methods} methods", file=sys.stderr)
        
        return api_data
        
    except Exception as e:
        print(f"❌ Exception in extract_pypylon_api: {e}", file=sys.stderr)
        print(f"   Exception type: {type(e).__name__}", file=sys.stderr)
        return {
            "error": "API extraction failed",
            "message": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }

# Run the extraction
try:
    print("🚀 Starting API extraction...", file=sys.stderr)
    result = extract_pypylon_api()
    
    # Check if result contains an error
    if isinstance(result, dict) and "error" in result:
        print(f"❌ Extraction returned error: {result['error']}", file=sys.stderr)
        print(json.dumps(result, indent=2, default=str))
        sys.exit(1)
    else:
        print("✅ Extraction completed successfully", file=sys.stderr)
        print(json.dumps(result, indent=2, default=str))
        
except Exception as e:
    print(f"❌ Top-level extraction exception: {e}", file=sys.stderr)
    error_result = {
        "error": "Top-level extraction failed",
        "message": str(e),
        "type": type(e).__name__,
        "traceback": traceback.format_exc()
    }
    print(json.dumps(error_result, indent=2, default=str))
    sys.exit(1)
'''

def save_api_dump(api_data: Dict[str, Any], output_file: Path, compress: bool = False) -> None:
    """Save API data to JSON file with integrity verification and documentation files"""
    
    # Add file metadata
    content = json.dumps(api_data, indent=2, sort_keys=True, default=str)
    
    if "metadata" not in api_data:
        api_data["metadata"] = {}
        
    api_data["metadata"]["file_info"] = {
        "filename": output_file.name,
        "size_bytes": len(content.encode()),
        "compressed": compress,
        "checksum": hashlib.sha256(content.encode()).hexdigest()
    }
    
    # Create documentation directory
    docs_dir = output_file.parent / f"{output_file.stem}_docs"
    docs_dir.mkdir(exist_ok=True)
    
    # Save documentation files
    pydoc_data = api_data.get("pydoc_documentation", {})
    doc_files = {}
    
    for module_name, doc_info in pydoc_data.items():
        if doc_info.get("success") and doc_info.get("documentation"):
            # Create safe filename
            safe_name = module_name.replace(".", "_").replace("/", "_")
            doc_file = docs_dir / f"{safe_name}.txt"
            
            try:
                with open(doc_file, 'w', encoding='utf-8') as f:
                    f.write(doc_info["documentation"])
                
                doc_files[module_name] = {
                    "filename": doc_file.name,
                    "path": str(doc_file.relative_to(output_file.parent)),
                    "size_bytes": doc_file.stat().st_size,
                    "lines": doc_info.get("doc_lines", 0)
                }
                print(f"📄 Documentation saved: {doc_file}")
            except Exception as e:
                print(f"⚠️  Failed to save documentation for {module_name}: {e}")
                doc_files[module_name] = {"error": str(e)}
    
    # Add documentation file info to metadata
    api_data["metadata"]["documentation_files"] = doc_files
    
    # Save file
    if compress:
        import gzip
        output_file_gz = output_file.with_suffix('.json.gz')
        with gzip.open(output_file_gz, 'wt', encoding='utf-8') as f:
            json.dump(api_data, f, indent=2, sort_keys=True, default=str)
        print(f"💾 Compressed API dump saved to: {output_file_gz}")
    else:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(api_data, f, indent=2, sort_keys=True, default=str)
        print(f"💾 API dump saved to: {output_file}")
    
    print(f"📚 Documentation files saved to: {docs_dir}")


def create_api_dump(python_executable: str = None, 
                   output_file: str = None,
                   compress: bool = False) -> Path:
    """Create comprehensive API dump from pypylon installation"""
    
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"pypylon_api_{timestamp}.json"
    
    output_path = Path(output_file)
    
    print(f"🔍 Extracting pypylon API from: {python_executable or 'current environment'}")
    print(f"📄 Output: {output_path}")
    
    extractor = PylonAPIExtractor(python_executable)
    api_data = extractor.extract_api()
    
    # Check for extraction errors
    if "error" in api_data:
        raise RuntimeError(f"API extraction failed: {api_data['error']}")
    
    # Add extraction metadata
    if "metadata" not in api_data:
        api_data["metadata"] = {}
    
    api_data["metadata"]["extraction_args"] = {
        "python_executable": python_executable,
        "output_file": str(output_path),
        "compress": compress
    }
    
    save_api_dump(api_data, output_path, compress)
    
    # Print summary statistics
    global_stats = api_data.get("global_stats", {})
    print(f"\n📊 API Analysis Summary:")
    print(f"   📦 Modules: {global_stats.get('total_modules', 0)}")
    print(f"   🏛️  Classes: {global_stats.get('total_classes', 0)}")
    print(f"   🔧 Functions: {global_stats.get('total_functions', 0)}")
    print(f"   ⚙️  Methods: {global_stats.get('total_methods', 0)}")
    print(f"   🏷️  Properties: {global_stats.get('total_properties', 0)}")
    print(f"   📈 Total API items: {global_stats.get('total_api_items', 0)}")
    
    return output_path


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Extract comprehensive pypylon API information",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract from current environment
  python pypylon_api_dumper.py --output pypylon_v4.2.0.json
  
  # Extract from specific Python environment
  python pypylon_api_dumper.py --python-env ~/.pyenv/versions/3.11.0/bin/python --output pypylon_stable.json
  
  # Extract with compression
  python pypylon_api_dumper.py --output pypylon_api.json --compress
  
  # Extract to timestamped file
  python pypylon_api_dumper.py
        """
    )
    
    parser.add_argument(
        "--python-env",
        help="Python executable to use for extraction (default: current environment)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output JSON file path (default: timestamped filename)"
    )
    parser.add_argument(
        "--compress",
        action="store_true",
        help="Compress output with gzip"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    try:
        api_file = create_api_dump(
            python_executable=args.python_env,
            output_file=args.output,
            compress=args.compress
        )
        
        print(f"\n✅ API extraction completed successfully!")
        print(f"📋 Use this file for API compatibility checking")
        
    except Exception as e:
        print(f"❌ Error creating API dump: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 