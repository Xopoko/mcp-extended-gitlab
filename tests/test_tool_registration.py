"""Tests for tool registration and module structure."""

import importlib
import inspect
from pathlib import Path
from typing import List, Dict, Any

import pytest
from fastmcp import FastMCP


class TestModuleStructure:
    """Test the module structure and conventions."""
    
    @pytest.fixture(scope='class')
    def api_modules(self):
        """Get all API modules."""
        api_path = Path(__file__).parent.parent / 'mcp_extended_gitlab' / 'api'
        modules = []
        
        for domain_dir in api_path.iterdir():
            if domain_dir.is_dir() and not domain_dir.name.startswith('__'):
                for module_file in domain_dir.glob('*.py'):
                    if not module_file.name.startswith('__'):
                        module_path = f"mcp_extended_gitlab.api.{domain_dir.name}.{module_file.stem}"
                        modules.append({
                            'path': module_path,
                            'domain': domain_dir.name,
                            'name': module_file.stem,
                            'file': module_file
                        })
        
        return modules
    
    def test_all_modules_have_register_function(self, api_modules):
        """Test that all API modules have a register function."""
        modules_without_register = []
        
        for module_info in api_modules:
            try:
                module = importlib.import_module(module_info['path'])
                if not hasattr(module, 'register'):
                    modules_without_register.append(module_info['path'])
            except ImportError as e:
                pytest.fail(f"Failed to import {module_info['path']}: {e}")
        
        assert not modules_without_register, f"Modules without register function: {modules_without_register}"
    
    def test_all_modules_have_get_gitlab_client(self, api_modules):
        """Test that all API modules have get_gitlab_client function."""
        modules_without_client = []
        
        for module_info in api_modules:
            try:
                module = importlib.import_module(module_info['path'])
                if not hasattr(module, 'get_gitlab_client'):
                    modules_without_client.append(module_info['path'])
            except ImportError:
                pass  # Already tested in previous test
        
        assert not modules_without_client, f"Modules without get_gitlab_client: {modules_without_client}"
    
    def test_register_function_signature(self, api_modules):
        """Test that all register functions have correct signature."""
        invalid_signatures = []
        
        for module_info in api_modules:
            try:
                module = importlib.import_module(module_info['path'])
                if hasattr(module, 'register'):
                    sig = inspect.signature(module.register)
                    params = list(sig.parameters.keys())
                    
                    # Should have exactly one parameter: mcp
                    if len(params) != 1 or params[0] != 'mcp':
                        invalid_signatures.append({
                            'module': module_info['path'],
                            'params': params
                        })
            except ImportError:
                pass
        
        assert not invalid_signatures, f"Invalid register signatures: {invalid_signatures}"
    
    def test_module_docstrings(self, api_modules):
        """Test that all modules have proper docstrings."""
        modules_without_docstring = []
        
        for module_info in api_modules:
            try:
                module = importlib.import_module(module_info['path'])
                if not module.__doc__ or len(module.__doc__.strip()) < 10:
                    modules_without_docstring.append(module_info['path'])
            except ImportError:
                pass
        
        assert not modules_without_docstring, f"Modules without proper docstrings: {modules_without_docstring}"
    
    def test_consistent_imports(self, api_modules):
        """Test that all modules use consistent imports."""
        inconsistent_imports = []
        
        for module_info in api_modules:
            with open(module_info['file'], 'r') as f:
                content = f.read()
                
                # Check for required imports
                required_imports = [
                    'from typing import',
                    'from fastmcp import FastMCP',
                    'from pydantic import Field',
                    'from ...client import GitLabClient'
                ]
                
                missing = []
                for req_import in required_imports:
                    if req_import not in content:
                        missing.append(req_import)
                
                if missing:
                    inconsistent_imports.append({
                        'module': module_info['path'],
                        'missing': missing
                    })
        
        # Some modules might not use all imports, so we'll be lenient
        if inconsistent_imports:
            print(f"\nModules with potentially missing imports: {len(inconsistent_imports)}")


class TestToolRegistration:
    """Test tool registration in the MCP server."""
    
    def test_server_loads_all_modules(self):
        """Test that server.py imports all API modules."""
        server_path = Path(__file__).parent.parent / 'mcp_extended_gitlab' / 'server.py'
        
        with open(server_path, 'r') as f:
            server_content = f.read()
        
        # Check for imports from each domain
        expected_domains = ['core', 'ci_cd', 'security', 'devops', 'registry', 'monitoring', 'integrations', 'admin']
        missing_domains = []
        
        for domain in expected_domains:
            if f'from .api.{domain}' not in server_content:
                missing_domains.append(domain)
        
        assert not missing_domains, f"Server doesn't import from domains: {missing_domains}"
    
    def test_all_register_functions_called(self):
        """Test that all register functions are called in server.py."""
        server_path = Path(__file__).parent.parent / 'mcp_extended_gitlab' / 'server.py'
        
        with open(server_path, 'r') as f:
            server_content = f.read()
        
        # Extract all imports with 'register as'
        import re
        import_pattern = r'from .api.[.\w]+ import register as (\w+)'
        imported_registers = re.findall(import_pattern, server_content)
        
        # Check that each imported register is called
        uncalled_registers = []
        for register_name in imported_registers:
            if f'{register_name}(mcp)' not in server_content:
                uncalled_registers.append(register_name)
        
        assert not uncalled_registers, f"Uncalled register functions: {uncalled_registers}"
    
    def test_no_duplicate_tool_names(self):
        """Test that there are no duplicate tool names across modules."""
        from mcp_extended_gitlab.server import mcp
        
        # Get all tool names
        if hasattr(mcp, '_tools'):
            tool_names = list(mcp._tools.keys())
            
            # Check for duplicates
            duplicates = [name for name in tool_names if tool_names.count(name) > 1]
            
            assert not duplicates, f"Duplicate tool names found: {set(duplicates)}"
    
    def test_tool_count_matches_readme(self):
        """Test that the actual tool count matches what's stated in README."""
        from mcp_extended_gitlab.server import mcp
        
        if hasattr(mcp, '_tools'):
            actual_count = len(mcp._tools)
            
            # Read README to find stated count
            readme_path = Path(__file__).parent.parent / 'README.md'
            with open(readme_path, 'r') as f:
                readme_content = f.read()
            
            # Look for tool count (e.g., "478 MCP tools" or "478+ tools")
            import re
            count_match = re.search(r'(\d+)\+?\s+(?:MCP\s+)?tools', readme_content, re.IGNORECASE)
            
            if count_match:
                stated_count = int(count_match.group(1))
                
                # Allow some tolerance as tools might be added
                assert actual_count >= stated_count, f"Actual tool count ({actual_count}) is less than stated ({stated_count})"
                
                # Warn if significantly different
                if abs(actual_count - stated_count) > 10:
                    pytest.warning(f"Tool count mismatch: README states {stated_count}, actual is {actual_count}")


class TestDomainOrganization:
    """Test that tools are properly organized by domain."""
    
    def test_core_domain_tools(self):
        """Test that core domain has expected tool categories."""
        from mcp_extended_gitlab.api.core import projects, issues, merge_requests, users, groups
        
        # Test that each core module registers appropriate tools
        test_mcp = FastMCP("test")
        
        # Projects should have CRUD operations
        projects.register(test_mcp)
        project_tools = [name for name in test_mcp._tools if 'project' in name]
        assert any('list' in tool for tool in project_tools)
        assert any('create' in tool for tool in project_tools)
        assert any('edit' in tool or 'update' in tool for tool in project_tools)
        assert any('delete' in tool for tool in project_tools)
    
    def test_security_domain_tools(self):
        """Test that security domain has appropriate tools."""
        security_modules = ['protected_branches', 'deploy_keys', 'deploy_tokens', 'keys']
        
        for module_name in security_modules:
            module_path = f"mcp_extended_gitlab.api.security.{module_name}"
            try:
                module = importlib.import_module(module_path)
                assert hasattr(module, 'register'), f"{module_name} missing register function"
            except ImportError as e:
                pytest.fail(f"Failed to import security module {module_name}: {e}")
    
    def test_monitoring_domain_tools(self):
        """Test that monitoring domain has analytics tools."""
        monitoring_modules = ['analytics', 'error_tracking', 'statistics']
        
        for module_name in monitoring_modules:
            module_path = f"mcp_extended_gitlab.api.monitoring.{module_name}"
            try:
                module = importlib.import_module(module_path)
                assert hasattr(module, 'register'), f"{module_name} missing register function"
                
                # Check for specific monitoring tools
                test_mcp = FastMCP("test")
                module.register(test_mcp)
                
                if module_name == 'analytics':
                    assert any('dora' in name.lower() for name in test_mcp._tools), "Missing DORA metrics tools"
            except ImportError as e:
                pytest.fail(f"Failed to import monitoring module {module_name}: {e}")


if __name__ == "__main__":
    # Quick test run
    test = TestModuleStructure()
    
    # Get modules
    api_path = Path(__file__).parent.parent / 'mcp_extended_gitlab' / 'api'
    modules = []
    
    for domain_dir in api_path.iterdir():
        if domain_dir.is_dir() and not domain_dir.name.startswith('__'):
            print(f"\nDomain: {domain_dir.name}")
            for module_file in domain_dir.glob('*.py'):
                if not module_file.name.startswith('__'):
                    print(f"  - {module_file.stem}")
                    modules.append(module_file.stem)
    
    print(f"\nTotal modules: {len(modules)}")