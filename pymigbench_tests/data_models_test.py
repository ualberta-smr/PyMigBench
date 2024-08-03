from pymigbench.code_change import CodeChange
from pymigbench.constants import ProgramElement, Cardinality, Property
from pymigbench.line_replacement import LineReplacement
from pymigbench.migration import Migration
from pymigbench.migration_file import MigrationFile

cc1 = CodeChange(
    LineReplacement.from_expression("1:1"),
    ["fizz.foo"], ["muzz.fish"],
    [ProgramElement.IMPORT], [ProgramElement.IMPORT],
    Cardinality.NOT_APPLICABLE, []
)
cc2 = CodeChange(
    LineReplacement.from_expression("5:3"),
    ["foo"], ["fish"],
    [ProgramElement.ATTRIBUTE], [ProgramElement.ATTRIBUTE],
    Cardinality.ONE_TO_ONE, [Property.ELEMENT_NAME_CHANGE]
)
file = MigrationFile("path/to/file", [cc1, cc2])
mig = Migration(
    repo="this/that", commit="1234567890abcdef1234567890abcdef12345678", source="fizz", target="muzz",
    files=[file], domain="something"
)


def test_code_change():
    cc3 = CodeChange(
        line=LineReplacement.from_expression("1:"),
        source_apis=["boo"], target_apis=[],
        source_program_elements=[ProgramElement.FUNCTION_CALL], target_program_elements=[],
        cardinality=Cardinality.ONE_TO_ZERO,
        properties=[]
    )

    cc4 = CodeChange(
        line=LineReplacement.from_expression(":7"),
        source_apis=[], target_apis=["foo"],
        source_program_elements=[], target_program_elements=[ProgramElement.FUNCTION_CALL],
        cardinality=Cardinality.ZERO_TO_ONE,
        properties=[]
    )
    assert cc1.file == file
    assert cc2.file == file

    assert cc1.id() == "fizz__muzz__this/that__12345678__path/to/file__1:1__0"
    assert cc2.id() == "fizz__muzz__this/that__12345678__path/to/file__5:3__1"

    assert cc1.index == 0
    assert cc2.index == 1

    assert cc1.id_in_file() == "1:1__0"

    assert cc1.is_import() is True
    assert cc2.is_import() is False
    assert cc3.is_import() is False
    assert cc4.is_import() is False

    assert cc1.is_addition_only() is False
    assert cc2.is_addition_only() is False
    assert cc3.is_addition_only() is False
    assert cc4.is_addition_only() is True

    assert cc1.is_removal_only() is False
    assert cc2.is_removal_only() is False
    assert cc3.is_removal_only() is True
    assert cc4.is_removal_only() is False

    assert cc1.can_have_properties() is False
    assert cc2.can_have_properties() is True
    assert cc3.can_have_properties() is False
    assert cc4.can_have_properties() is False

    # assert len(mig.files) == 2
    # assert mig.commit_url == "https://github.com/this/that/commit/12345678"
    # assert mig.short_commit() == "12345678"
    # assert mig.id() == "fizz__muzz__this/that__12345678"
    # assert mig.pair_id == "fizz__muzz"


def test_migration_file():
    assert file.id() == "fizz__muzz__this/that__12345678__path/to/file"
    assert file.api_ccs() == [cc2]
    assert file.code_changes == [cc1, cc2]


def test_migration():
    assert mig.id() == "fizz__muzz__this/that__12345678"
    assert mig.files == [file]
    assert mig.commit_url == "https://github.com/this/that/commit/12345678"
    assert mig.short_commit() == "12345678"
    assert mig.id() == "fizz__muzz__this/that__12345678"
    assert mig.pair_id == "fizz__muzz"
    assert mig.code_changes() == [cc1, cc2]
