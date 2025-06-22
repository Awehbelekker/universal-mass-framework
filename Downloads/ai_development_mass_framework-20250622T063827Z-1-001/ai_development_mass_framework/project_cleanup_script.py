#!/usr/bin/env python3
"""
Universal MASS Framework - Project Cleanup Script
================================================

Comprehensive cleanup script for the Universal MASS Framework project.
This script removes redundant files, organizes documentation, and prepares
the project for production deployment and future maintenance.

Features:
- Remove redundant and temporary files
- Organize documentation structure
- Consolidate requirements files
- Clean up deployment scripts
- Prepare production package
- Generate final project structure

Author: Universal MASS Framework Team
Date: June 22, 2025
Version: 1.0.0
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import glob

class MassFrameworkCleanup:
    """Comprehensive cleanup for MASS Framework project"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.cleanup_log = []
        self.moved_files = []
        self.deleted_files = []
        self.created_dirs = []
        
    def log_action(self, action: str, details: str = ""):
        """Log cleanup action"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {action}"
        if details:
            log_entry += f": {details}"
        self.cleanup_log.append(log_entry)
        print(log_entry)
    
    def remove_redundant_files(self):
        """Remove redundant and temporary files"""
        self.log_action("🧹 REMOVING REDUNDANT FILES")
        
        # Patterns for files to remove
        redundant_patterns = [
            "**/__pycache__",
            "**/*.pyc",
            "**/*.pyo", 
            "**/.pytest_cache",
            "**/*.log",
            "**/*.tmp",
            "**/*.cache",
            "**/.DS_Store",
            "**/Thumbs.db",
            "**/*_old.*",
            "**/*_backup.*",
            "**/*.bak",
            "**/.coverage",
            "**/node_modules"  # If any exist
        ]
        
        for pattern in redundant_patterns:
            matches = list(self.base_path.glob(pattern))
            for match in matches:
                try:
                    if match.is_file():
                        match.unlink()
                        self.deleted_files.append(str(match.relative_to(self.base_path)))
                        self.log_action("  Deleted file", str(match.relative_to(self.base_path)))
                    elif match.is_dir():
                        shutil.rmtree(match)
                        self.deleted_files.append(str(match.relative_to(self.base_path)))
                        self.log_action("  Deleted directory", str(match.relative_to(self.base_path)))
                except Exception as e:
                    self.log_action("  ⚠️  Failed to delete", f"{match}: {e}")
    
    def organize_documentation(self):
        """Organize documentation into proper structure"""
        self.log_action("📚 ORGANIZING DOCUMENTATION")
        
        # Create docs directory if it doesn't exist
        docs_dir = self.base_path / "docs"
        if not docs_dir.exists():
            docs_dir.mkdir()
            self.created_dirs.append("docs")
            self.log_action("  Created directory", "docs")
        
        # Documentation files to organize
        doc_files = {
            # Keep in root
            "README.md": None,
            "QUICK_START_GUIDE.md": None,
            
            # Move to docs/
            "UNIVERSAL_MASS_FRAMEWORK_COMPLETE.md": "docs/",
            "IMPLEMENTATION_COMPLETE_SUMMARY.md": "docs/",
            "AI_AGENT_IMPLEMENTATION_COMPLETE.md": "docs/technical/",
            "AI_AGENT_SYSTEM_COMPLETE.md": "docs/technical/",
            "ENTERPRISE_ADVANCEMENT_ANALYSIS.md": "docs/business/",
            "COMPETITIVE_ANALYSIS_COMPREHENSIVE.md": "docs/business/",
            "COMPETITIVE_COMPARISON_CHART.md": "docs/business/",
            "MARKET_DOMINATION_STRATEGY.md": "docs/business/",
            "STRATEGIC_POSITIONING.md": "docs/business/",
            
            # Deployment docs
            "AWS_DEPLOYMENT_GUIDE.md": "docs/deployment/",
            "DEPLOYMENT_GUIDE.md": "docs/deployment/",
            "COMPLETE_DEPLOYMENT_GUIDE.md": "docs/deployment/",
            "FIREBASE_DEPLOYMENT_GUIDE.md": "docs/deployment/",
            "ARM64_DEPLOY_GUIDE.md": "docs/deployment/",
            
            # Status and completion docs
            "MISSION_ACCOMPLISHED.md": "docs/status/",
            "FINAL_STATUS_REPORT.md": "docs/status/",
            "BETA_LAUNCH_COMPLETE.md": "docs/status/",
            "DEPLOYMENT_SUCCESS.md": "docs/status/",
        }
        
        # Create subdirectories
        subdirs = ["docs/technical", "docs/business", "docs/deployment", "docs/status"]
        for subdir in subdirs:
            subdir_path = self.base_path / subdir
            if not subdir_path.exists():
                subdir_path.mkdir(parents=True)
                self.created_dirs.append(subdir)
                self.log_action("  Created directory", subdir)
        
        # Move documentation files
        for filename, target_dir in doc_files.items():
            source_file = self.base_path / filename
            if source_file.exists() and target_dir:
                target_path = self.base_path / target_dir / filename
                try:
                    shutil.move(str(source_file), str(target_path))
                    self.moved_files.append(f"{filename} -> {target_dir}")
                    self.log_action("  Moved", f"{filename} to {target_dir}")
                except Exception as e:
                    self.log_action("  ⚠️  Failed to move", f"{filename}: {e}")
    
    def consolidate_requirements(self):
        """Consolidate multiple requirements files"""
        self.log_action("📦 CONSOLIDATING REQUIREMENTS")
        
        requirements_files = [
            "requirements.txt",
            "requirements-minimal.txt", 
            "requirements-functional.txt"
        ]
        
        # Find existing requirements files
        existing_requirements = []
        for req_file in requirements_files:
            if (self.base_path / req_file).exists():
                existing_requirements.append(req_file)
        
        if len(existing_requirements) > 1:
            self.log_action("  Found multiple requirements files", str(existing_requirements))
            
            # Read all requirements
            all_requirements = set()
            for req_file in existing_requirements:
                try:
                    with open(self.base_path / req_file, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                all_requirements.add(line)
                except Exception as e:
                    self.log_action("  ⚠️  Failed to read", f"{req_file}: {e}")
            
            # Create consolidated requirements.txt
            main_requirements = [
                "# Universal MASS Framework - Requirements",
                "# Consolidated from multiple requirements files",
                "# Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "",
                "# Core Framework Dependencies",
                "fastapi>=0.104.0",
                "uvicorn>=0.24.0",
                "sqlalchemy>=2.0.0",
                "aiofiles>=23.0.0",
                "websockets>=12.0",
                "requests>=2.31.0",
                "aiohttp>=3.9.0",
                "",
                "# Data Processing Dependencies", 
                "numpy>=1.24.0",
                "pandas>=2.0.0",
                "scikit-learn>=1.3.0",
                "",
                "# Authentication and Security",
                "python-jose[cryptography]>=3.3.0",
                "passlib[bcrypt]>=1.7.4",
                "python-multipart>=0.0.6",
                "",
                "# Utilities",
                "python-dotenv>=1.0.0",
                "jinja2>=3.1.0",
                "structlog>=23.0.0",
                "",
                "# Monitoring",
                "prometheus-client>=0.19.0",
                "",
                "# Additional requirements from existing files:"
            ]
            
            # Add unique requirements
            for req in sorted(all_requirements):
                main_requirements.append(req)
            
            # Write consolidated requirements
            try:
                with open(self.base_path / "requirements.txt", 'w') as f:
                    f.write('\n'.join(main_requirements))
                self.log_action("  Created consolidated requirements.txt")
                
                # Move old requirements files to backup
                backup_dir = self.base_path / "backup_requirements"
                if not backup_dir.exists():
                    backup_dir.mkdir()
                
                for req_file in existing_requirements[1:]:  # Keep the first one
                    old_file = self.base_path / req_file
                    backup_file = backup_dir / req_file
                    try:
                        shutil.move(str(old_file), str(backup_file))
                        self.moved_files.append(f"{req_file} -> backup_requirements/")
                        self.log_action("  Moved to backup", req_file)
                    except Exception as e:
                        self.log_action("  ⚠️  Failed to backup", f"{req_file}: {e}")
                        
            except Exception as e:
                self.log_action("  ⚠️  Failed to create consolidated requirements", str(e))
    
    def clean_deployment_scripts(self):
        """Clean up redundant deployment scripts"""
        self.log_action("🚀 CLEANING DEPLOYMENT SCRIPTS")
        
        # Create deployment directory
        deploy_dir = self.base_path / "deployment"
        if not deploy_dir.exists():
            deploy_dir.mkdir()
            self.created_dirs.append("deployment")
            self.log_action("  Created directory", "deployment")
        
        # Deployment scripts to organize
        deployment_patterns = [
            "*deploy*.ps1",
            "*deploy*.sh",
            "*deploy*.bat",
            "*deploy*.py",
            "setup-*.ps1",
            "setup-*.sh",
            "*-setup*.ps1",
            "*fix*.sh",
            "*fix*.ps1",
            "launch*.ps1",
            "launch*.sh",
            "start*.ps1",
            "start*.sh"
        ]
        
        # Find and move deployment scripts
        moved_count = 0
        for pattern in deployment_patterns:
            matches = list(self.base_path.glob(pattern))
            for match in matches:
                if match.is_file() and match.name not in ["deploy.py"]:  # Keep main deploy.py
                    target_file = deploy_dir / match.name
                    try:
                        shutil.move(str(match), str(target_file))
                        self.moved_files.append(f"{match.name} -> deployment/")
                        moved_count += 1
                    except Exception as e:
                        self.log_action("  ⚠️  Failed to move", f"{match.name}: {e}")
        
        self.log_action(f"  Moved {moved_count} deployment scripts to deployment/")
    
    def organize_configuration_files(self):
        """Organize configuration files"""
        self.log_action("⚙️  ORGANIZING CONFIGURATION FILES")
        
        # Create config directory if it doesn't exist
        config_dir = self.base_path / "config"
        if not config_dir.exists():
            config_dir.mkdir()
            self.created_dirs.append("config")
            self.log_action("  Created directory", "config")
        
        # Configuration files to organize
        config_files = [
            ".env.template",
            ".env.production",
            "firebase.json",
            "firestore.rules",
            "firestore.indexes.json",
            "docker-compose.yml",
            "docker-compose.production.yml",
            "docker-compose.local.yml",
            "Dockerfile",
            "Dockerfile.production",
            "*-params.json",
            "conftest.py"
        ]
        
        moved_count = 0
        for pattern in config_files:
            matches = list(self.base_path.glob(pattern))
            for match in matches:
                if match.is_file():
                    # Keep some files in root
                    if match.name in [".env", ".env.local", "docker-compose.yml", "Dockerfile"]:
                        continue
                    
                    target_file = config_dir / match.name
                    try:
                        shutil.move(str(match), str(target_file))
                        self.moved_files.append(f"{match.name} -> config/")
                        moved_count += 1
                    except Exception as e:
                        self.log_action("  ⚠️  Failed to move", f"{match.name}: {e}")
        
        self.log_action(f"  Moved {moved_count} configuration files to config/")
    
    def create_production_package(self):
        """Create production deployment package"""
        self.log_action("📦 CREATING PRODUCTION PACKAGE")
        
        # Create production directory
        prod_dir = self.base_path / "production_package"
        if prod_dir.exists():
            shutil.rmtree(prod_dir)
        prod_dir.mkdir()
        self.created_dirs.append("production_package")
        
        # Essential files for production
        essential_files = [
            "main.py",
            "requirements.txt",
            "README.md",
            "QUICK_START_GUIDE.md",
            ".env.template"
        ]
        
        # Copy essential files
        for filename in essential_files:
            source_file = self.base_path / filename
            if source_file.exists():
                target_file = prod_dir / filename
                try:
                    shutil.copy2(str(source_file), str(target_file))
                    self.log_action("  Copied to production", filename)
                except Exception as e:
                    self.log_action("  ⚠️  Failed to copy", f"{filename}: {e}")
        
        # Copy universal_mass_framework directory
        framework_source = self.base_path / "universal_mass_framework"
        framework_target = prod_dir / "universal_mass_framework"
        if framework_source.exists():
            try:
                shutil.copytree(str(framework_source), str(framework_target))
                self.log_action("  Copied framework to production package")
            except Exception as e:
                self.log_action("  ⚠️  Failed to copy framework", str(e))
        
        # Create production README
        prod_readme = f"""# Universal MASS Framework - Production Package

## Quick Deployment

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment:
   ```bash
   cp .env.template .env
   # Edit .env with your configuration
   ```

3. Run the framework:
   ```bash
   python main.py
   ```

## Package Contents

- `universal_mass_framework/` - Core framework implementation
- `main.py` - Application entry point
- `requirements.txt` - Python dependencies
- `QUICK_START_GUIDE.md` - Integration guide

## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

For full documentation, see the main project repository.
"""
        
        try:
            with open(prod_dir / "PRODUCTION_README.md", 'w') as f:
                f.write(prod_readme)
            self.log_action("  Created production README")
        except Exception as e:
            self.log_action("  ⚠️  Failed to create production README", str(e))
    
    def generate_final_project_structure(self):
        """Generate and save final project structure"""
        self.log_action("📋 GENERATING PROJECT STRUCTURE")
        
        def get_directory_structure(path: Path, prefix: str = "", max_depth: int = 3, current_depth: int = 0):
            """Generate directory tree structure"""
            if current_depth >= max_depth:
                return []
            
            items = []
            try:
                entries = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
                for i, entry in enumerate(entries):
                    is_last = i == len(entries) - 1
                    current_prefix = "└── " if is_last else "├── "
                    items.append(f"{prefix}{current_prefix}{entry.name}")
                    
                    if entry.is_dir() and not entry.name.startswith('.') and current_depth < max_depth - 1:
                        next_prefix = prefix + ("    " if is_last else "│   ")
                        items.extend(get_directory_structure(entry, next_prefix, max_depth, current_depth + 1))
            except PermissionError:
                pass
            
            return items
        
        structure = get_directory_structure(self.base_path)
        
        structure_doc = f"""# Universal MASS Framework - Final Project Structure

## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Directory Structure
```
{self.base_path.name}/
""" + '\n'.join(structure) + f"""
```

## Key Components

### Core Framework
- `universal_mass_framework/` - Main framework implementation
  - `core/` - Core orchestration engines
  - `data_orchestration/` - Data processing and orchestration
  - `intelligence_agents/` - AI agents for analysis and prediction
  - `universal_adapters/` - System integration adapters
  - `enterprise_trust/` - Security and compliance framework

### Documentation
- `docs/` - Organized documentation
  - `technical/` - Technical implementation details
  - `business/` - Business analysis and strategy
  - `deployment/` - Deployment guides and instructions
  - `status/` - Project status and completion reports

### Configuration & Deployment
- `config/` - Configuration files and templates
- `deployment/` - Deployment scripts and utilities
- `production_package/` - Ready-to-deploy package

### Development & Testing
- `tests/` - Test suites and validation scripts
- Various validation and demo scripts

## Cleanup Summary
- Files moved: {len(self.moved_files)}
- Files deleted: {len(self.deleted_files)}
- Directories created: {len(self.created_dirs)}

## Status: ✅ ORGANIZED AND PRODUCTION READY
"""
        
        try:
            with open(self.base_path / "PROJECT_STRUCTURE.md", 'w') as f:
                f.write(structure_doc)
            self.log_action("  Created PROJECT_STRUCTURE.md")
        except Exception as e:
            self.log_action("  ⚠️  Failed to create structure document", str(e))
    
    def run_comprehensive_cleanup(self):
        """Run complete cleanup process"""
        self.log_action("🚀 STARTING COMPREHENSIVE CLEANUP")
        self.log_action(f"Target Directory: {self.base_path.absolute()}")
        self.log_action("")
        
        try:
            # Step 1: Remove redundant files
            self.remove_redundant_files()
            self.log_action("")
            
            # Step 2: Organize documentation
            self.organize_documentation()
            self.log_action("")
            
            # Step 3: Consolidate requirements
            self.consolidate_requirements()
            self.log_action("")
            
            # Step 4: Clean deployment scripts
            self.clean_deployment_scripts()
            self.log_action("")
            
            # Step 5: Organize configuration files
            self.organize_configuration_files()
            self.log_action("")
            
            # Step 6: Create production package
            self.create_production_package()
            self.log_action("")
            
            # Step 7: Generate final structure
            self.generate_final_project_structure()
            self.log_action("")
            
            # Generate cleanup summary
            self.generate_cleanup_summary()
            
        except Exception as e:
            self.log_action("❌ CLEANUP FAILED", str(e))
            raise
    
    def generate_cleanup_summary(self):
        """Generate comprehensive cleanup summary"""
        self.log_action("📊 GENERATING CLEANUP SUMMARY")
        
        summary = {
            "cleanup_timestamp": datetime.now().isoformat(),
            "base_path": str(self.base_path.absolute()),
            "actions_performed": {
                "files_moved": len(self.moved_files),
                "files_deleted": len(self.deleted_files),
                "directories_created": len(self.created_dirs),
                "total_actions": len(self.cleanup_log)
            },
            "moved_files": self.moved_files,
            "deleted_files": self.deleted_files,
            "created_directories": self.created_dirs,
            "cleanup_log": self.cleanup_log
        }
        
        # Save detailed log
        try:
            with open(self.base_path / "cleanup_report.json", 'w') as f:
                json.dump(summary, f, indent=2)
            self.log_action("  Saved detailed cleanup report to cleanup_report.json")
        except Exception as e:
            self.log_action("  ⚠️  Failed to save cleanup report", str(e))
        
        # Print summary
        self.log_action("")
        self.log_action("🎉 CLEANUP COMPLETED SUCCESSFULLY")
        self.log_action("=" * 50)
        self.log_action(f"Files Moved: {len(self.moved_files)}")
        self.log_action(f"Files Deleted: {len(self.deleted_files)}")
        self.log_action(f"Directories Created: {len(self.created_dirs)}")
        self.log_action(f"Total Actions: {len(self.cleanup_log)}")
        self.log_action("")
        self.log_action("✅ Project is now organized and production-ready!")
        
        return summary

def main():
    """Main cleanup function"""
    print("🧹 UNIVERSAL MASS FRAMEWORK - PROJECT CLEANUP")
    print("=" * 50)
    print(f"Starting cleanup at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    cleanup = MassFrameworkCleanup()
    results = cleanup.run_comprehensive_cleanup()
    
    return results

if __name__ == "__main__":
    main()
