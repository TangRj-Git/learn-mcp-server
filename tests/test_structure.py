import ast
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "learn_mcp_server"


def test_feature_modules_do_not_import_server_module():
    feature_files = [
        *SRC.joinpath("data").glob("*.py"),
        *SRC.joinpath("tools").glob("*.py"),
        *SRC.joinpath("resources").glob("*.py"),
        *SRC.joinpath("prompts").glob("*.py"),
    ]

    offenders: list[str] = []
    for path in feature_files:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == "learn_mcp_server.server":
                offenders.append(str(path.relative_to(ROOT)))
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "learn_mcp_server.server":
                        offenders.append(str(path.relative_to(ROOT)))

    assert offenders == []


def test_server_module_is_registration_layer_only():
    server_lines = (SRC / "server.py").read_text(encoding="utf-8").splitlines()

    assert len(server_lines) <= 60


def test_server_module_delegates_registration_to_registry():
    source = (SRC / "server.py").read_text(encoding="utf-8")

    assert "create_server" in source
    assert "register_all" in source
    assert "mcp.tool()(" not in source
    assert "mcp.resource(" not in source
    assert "mcp.prompt()(" not in source


def test_registry_names_and_uris_are_unique():
    from learn_mcp_server import registry

    registered_names = list(registry.REGISTERED_NAMES)
    resource_uris = [uri for _, uri, _ in (*registry.RESOURCES, *registry.RESOURCE_TEMPLATES)]

    assert len(registered_names) == len(set(registered_names))
    assert len(resource_uris) == len(set(resource_uris))


def test_readme_capability_counts_match_registry():
    from learn_mcp_server import registry

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    expected_counts = {
        "Tools": len(registry.TOOLS),
        "Resources": len(registry.RESOURCES),
        "Resource Templates": len(registry.RESOURCE_TEMPLATES),
        "Prompts": len(registry.PROMPTS),
    }

    for label, expected_count in expected_counts.items():
        match = re.search(rf"{re.escape(label)}:\s*(\d+)\s*个", readme)
        assert match is not None, f"README should document {label} count"
        assert int(match.group(1)) == expected_count


def test_package_init_files_export_public_modules():
    init_files = [
        SRC / "data" / "__init__.py",
        SRC / "tools" / "__init__.py",
        SRC / "resources" / "__init__.py",
        SRC / "prompts" / "__init__.py",
        SRC / "utils" / "__init__.py",
    ]

    for path in init_files:
        source = path.read_text(encoding="utf-8")
        assert "__all__" in source, f"{path.relative_to(ROOT)} should define __all__"
