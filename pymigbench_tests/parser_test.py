from pymigbench.constants import ProgramElement, Cardinality, Property
from pymigbench.parsers import parse_code_change, parse_migration_file, parse_migration


def test_parse_code_change():
    data = {
        "line": "1:2-4",
        "source_apis": ["foo", "bar"],
        "target_apis": ["foo", "fish"],
        "source_program_elements": ["function call", "function call"],
        "target_program_elements": ["function call", "attribute"],
        "cardinality": "many-to-many",
        "properties": ["element name change", "argument transformation"]
    }

    cc = parse_code_change(data)
    assert cc.line.source.expression == "1"
    assert cc.line.target.expression == "2-4"
    assert cc.source_apis == ["foo", "bar"]
    assert cc.target_apis == ["foo", "fish"]
    assert cc.source_program_elements == [ProgramElement.FUNCTION_CALL, ProgramElement.FUNCTION_CALL]
    assert cc.target_program_elements == [ProgramElement.FUNCTION_CALL, ProgramElement.ATTRIBUTE]
    assert cc.cardinality == Cardinality.MANY_TO_MANY
    assert cc.properties == [Property.ELEMENT_NAME_CHANGE, Property.ARGUMENT_TRANSFORMATION]


def test_parse_migration_file():
    data = {
        "path": "path/to/file",
        "code_changes": [
            {
                "line": "1:2-4",
                "source_apis": ["fizz.foo"],
                "target_apis": ["mazz.foo"],
                "source_program_elements": ["import"],
                "target_program_elements": ["import"],
                "cardinality": "not applicable",
                "properties": []
            },
            {
                "line": "5:5",
                "source_apis": ["foo"],
                "target_apis": ["foo"],
                "source_program_elements": ["decorator"],
                "target_program_elements": ["decorator"],
                "cardinality": "one-to-one",
                "properties": []
            }
        ]
    }

    mf = parse_migration_file(data)
    assert mf.path == "path/to/file"
    assert len(mf.code_changes) == 2
    assert mf.code_changes[0].line.expression == "1:2-4"
    assert mf.code_changes[1].line.expression == "5:5"


def test_parse_migration():
    data = {
        "repo": "this/that",
        "commit": "1234567890abcdef1234567890abcdef12345678",
        "source": "fizz",
        "target": "muzz",
        "domain": "something",
        "files": [
            {
                "path": "path/to/file",
                "code_changes": [
                    {
                        "line": "1:2-4",
                        "source_apis": ["fizz.foo"],
                        "target_apis": ["mazz.foo"],
                        "source_program_elements": ["import"],
                        "target_program_elements": ["import"],
                        "cardinality": "not applicable",
                        "properties": []
                    },
                    {
                        "line": "5:5",
                        "source_apis": ["foo"],
                        "target_apis": ["foo"],
                        "source_program_elements": ["decorator"],
                        "target_program_elements": ["decorator"],
                        "cardinality": "one-to-one",
                        "properties": []
                    }
                ]
            },
            {
                "path": "path/to/another/file",
                "code_changes": [
                    {
                        "line": "1:2-4",
                        "source_apis": ["fizz.foo"],
                        "target_apis": ["mazz.foo"],
                        "source_program_elements": ["import"],
                        "target_program_elements": ["import"],
                        "cardinality": "not applicable",
                        "properties": []
                    }
                ]
            }
        ]
    }

    mig = parse_migration(data)
    assert mig.repo == "this/that"
    assert mig.commit == "1234567890abcdef1234567890abcdef12345678"
    assert mig.source == "fizz"
    assert mig.target == "muzz"
    assert mig.domain == "something"
