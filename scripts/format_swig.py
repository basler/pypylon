#! /bin/env python3
import re
import sys
import subprocess
import tempfile
import argparse
from dataclasses import dataclass
from enum import Enum, auto
from typing import List

class CodeType(Enum):
    CPP = auto()
    PYTHON = auto()
    SWIG = auto()
    PYTHON_INLINE = auto()  # For inline Python code

@dataclass
class CodeSection:
    type: CodeType
    content: str
    start_line: int
    end_line: int
    directive: str = ""

def format_cpp(code: str, debug: bool = False) -> str:
    """Format C++ code using clang-format with an explicit style."""
    if debug:
        print("[DEBUG] Formatting C++ code with clang-format:\n", code)
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.cpp') as tmp:
        tmp.write(code)
        tmp.flush()
        try:
            # Specify a style for clarity; you can change 'llvm' to 'google', etc.
            result = subprocess.run(
                ['clang-format', '--style=llvm', tmp.name],
                capture_output=True,
                text=True,
                check=True
            )
            if debug:
                print("[DEBUG] clang-format output:\n", result.stdout)
            return result.stdout
        except subprocess.CalledProcessError as e:
            if debug:
                print("[DEBUG] clang-format failed. Returning original code.")
                print("[DEBUG] Error:", e.stderr)
            return code

def format_python(code: str, debug: bool = False) -> str:
    """Format Python code using black."""
    if debug:
        print("[DEBUG] Formatting Python code with black:\n", code)
    try:
        result = subprocess.run(
            ['black', '-', '-q'],
            input=code,
            capture_output=True,
            text=True,
            check=True
        )
        if debug:
            print("[DEBUG] black output:\n", result.stdout)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if debug:
            print("[DEBUG] black formatting failed. Returning original code.")
            print("[DEBUG] Error:", e.stderr)
        return code

def parse_swig_file(content: str, debug: bool = False) -> List[CodeSection]:
    """Parse SWIG interface file into sections."""
    lines = content.split('\n')
    sections = []
    current_type = CodeType.SWIG
    current_content = []
    start_line = 0
    current_directive = ""
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped_line = line.strip()
        
        # Handle inline %pythoncode
        if '%pythoncode' in stripped_line and '%{' not in stripped_line:
            if current_content:
                sections.append(CodeSection(
                    type=current_type,
                    content='\n'.join(current_content),
                    start_line=start_line,
                    end_line=i-1,
                    directive=current_directive
                ))
            
            # Add the inline Python code as its own section
            sections.append(CodeSection(
                type=CodeType.PYTHON_INLINE,
                content=line,
                start_line=i,
                end_line=i,
                directive=""
            ))
            
            current_content = []
            start_line = i + 1
            i += 1
            continue
        
        # Check for C++ sections
        elif stripped_line.startswith('%{'):
            if current_content:
                sections.append(CodeSection(
                    type=current_type,
                    content='\n'.join(current_content),
                    start_line=start_line,
                    end_line=i-1,
                    directive=current_directive
                ))
            current_type = CodeType.CPP
            current_content = [line]
            start_line = i
            current_directive = line
        
        # Check for Python block sections
        elif stripped_line.startswith('%pythoncode') and '%{' in stripped_line:
            if current_content:
                sections.append(CodeSection(
                    type=current_type,
                    content='\n'.join(current_content),
                    start_line=start_line,
                    end_line=i-1,
                    directive=current_directive
                ))
            current_type = CodeType.PYTHON
            current_content = [line]
            start_line = i
            current_directive = line
        
        elif stripped_line == '%}' and (current_type == CodeType.CPP or current_type == CodeType.PYTHON):
            current_content.append(line)
            sections.append(CodeSection(
                type=current_type,
                content='\n'.join(current_content),
                start_line=start_line,
                end_line=i,
                directive=current_directive
            ))
            current_type = CodeType.SWIG
            current_content = []
            start_line = i + 1
            current_directive = ""
            
        else:
            current_content.append(line)
        
        i += 1
    
    # Add final section
    if current_content:
        sections.append(CodeSection(
            type=current_type,
            content='\n'.join(current_content),
            start_line=start_line,
            end_line=len(lines)-1,
            directive=current_directive
        ))
    
    if debug:
        for sec in sections:
            print(f"[DEBUG] Section from line {sec.start_line} to {sec.end_line}, type={sec.type}, directive={sec.directive}")
    
    return sections

def format_section(section: CodeSection, debug: bool = False) -> str:
    """Format a single section of code."""
    if debug:
        print(f"[DEBUG] Formatting section (type={section.type}). Lines {section.start_line}-{section.end_line}")
    if section.type == CodeType.CPP:
        lines = section.content.split('\n')
        # Remove the %{ ... %} wrapper to format only the C++ inside
        inner_code = '\n'.join(lines[1:-1])
        formatted_inner = format_cpp(inner_code, debug=debug)
        return f"{lines[0]}\n{formatted_inner.rstrip()}\n{lines[-1]}"
    elif section.type == CodeType.PYTHON:
        lines = section.content.split('\n')
        # Remove the %pythoncode %{ ... %} wrapper to format only the Python inside
        inner_code = '\n'.join(lines[1:-1])
        formatted_inner = format_python(inner_code, debug=debug)
        return f"{lines[0]}\n{formatted_inner.rstrip()}\n{lines[-1]}"
    elif section.type == CodeType.PYTHON_INLINE:
        # For inline Python code, preserve exactly as is
        return section.content
    else:
        # SWIG or unknown sections remain unchanged
        return section.content

def format_swig_file(filepath: str, in_place: bool = False, create_backup: bool = True, debug: bool = False) -> str:
    """Format a SWIG interface file.
    
    Args:
        filepath: Path to the SWIG interface file
        in_place: If True, modify the file in place.
        create_backup: If True, create a .bak backup of the original file.
        debug: If True, print debugging information to stdout.
    
    Returns:
        The formatted content as a string.
    """
    if debug:
        print(f"[DEBUG] Reading from {filepath}")
    with open(filepath, 'r') as f:
        content = f.read()
    
    sections = parse_swig_file(content, debug=debug)
    formatted_sections = [format_section(section, debug=debug) for section in sections]
    formatted_content = '\n'.join(formatted_sections)
    
    if debug:
        print("[DEBUG] Finished formatting. Checking in_place option...")
    if in_place:
        if create_backup:
            backup_path = filepath + '.bak'
            if debug:
                print(f"[DEBUG] Creating backup at {backup_path}")
            with open(backup_path, 'w') as f:
                f.write(content)
        
        if debug:
            print(f"[DEBUG] Writing changes back to {filepath}")
        with open(filepath, 'w') as f:
            f.write(formatted_content)
    
    return formatted_content

def main():
    parser = argparse.ArgumentParser(description='Format SWIG interface files.')
    parser.add_argument('file', help='The SWIG interface file to format')
    parser.add_argument('-i', '--in-place', action='store_true',
                        help='Modify the file in place (creates a .bak backup by default)')
    parser.add_argument('--no-backup', action='store_true',
                        help='Do not create backup files when using --in-place')
    parser.add_argument('--debug', action='store_true',
                        help='Print debug information')
    
    args = parser.parse_args()
    
    try:
        formatted = format_swig_file(
            args.file,
            in_place=args.in_place,
            create_backup=not args.no_backup,
            debug=args.debug
        )
        if args.in_place:
            print(f"Formatted {args.file}")
        else:
            print(formatted)
    except Exception as e:
        print(f"Error formatting file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
