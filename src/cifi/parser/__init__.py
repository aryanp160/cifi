from typing import Dict, Type
from cifi.parser.base import BaseParser
from cifi.parser.github_actions import GitHubActionsParser
from cifi.parser.pytest_parser import PytestParser
from cifi.parser.jest_parser import JestParser
from cifi.parser.cargo_parser import CargoParser
from cifi.parser.generic_parser import GenericParser

PARSER_REGISTRY: Dict[str, Type[BaseParser]] = {
    "github_actions": GitHubActionsParser,
    "pytest": PytestParser,
    "jest": JestParser,
    "cargo": CargoParser,
    "generic": GenericParser,
}


def get_parser(name_or_content: str, auto_detect: bool = True) -> BaseParser:
    """Retrieve a parser by explicit name or auto-detect based on log heuristics."""
    if name_or_content in PARSER_REGISTRY:
        return PARSER_REGISTRY[name_or_content]()

    if auto_detect:
        if "##[error]" in name_or_content or "##[warning]" in name_or_content:
            return GitHubActionsParser()
        if "FAILED " in name_or_content and "::" in name_or_content:
            return PytestParser()
        if "FAIL " in name_or_content and (".test." in name_or_content or ".spec." in name_or_content or "Test Suites:" in name_or_content or "npm ERR!" in name_or_content):
            return JestParser()
        if "error[E" in name_or_content and "-->" in name_or_content:
            return CargoParser()

    return GenericParser()
