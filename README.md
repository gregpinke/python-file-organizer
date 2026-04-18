# Python File Organizer

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Tests](https://img.shields.io/badge/tests-pytest-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A command-line Python tool that automatically organizes messy folders into clean category-based structures using configurable rules.

---

## Features

- Organize files by extension
- Configurable JSON rule system
- Automatic creation of category folders
- Duplicate-safe renaming
- Dry-run mode
- Recursive scanning
- Summary report generation
- Command-line interface
- Automated pytest test suite

---

## System Workflow

Input Directory  
↓  
File Scanner  
↓  
Extension Detection  
↓  
Rule Matching  
(JSON configuration)  
↓  
Category Folder Creation  
↓  
File Relocation  
↓  
Optional Report Generation  

Dry-run mode allows previewing changes before applying them.

---

## Project Impact

Large folders quickly become disorganized due to mixed file types from downloads, exports, and project files.

This tool automates file organization by:

- classifying files using configurable rules
- creating consistent directory structures
- preventing duplicate naming conflicts
- generating reports of automated actions

The result is a repeatable workflow for maintaining clean project directories.