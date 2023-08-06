# pylint: disable=missing-docstring

from polarion_docstrings.parser import (
    DocstringRecord,
    ErrorRecord,
    ValueRecord,
    get_docstrings_in_file,
    parse_docstring,
    strip_polarion_data,
)

EXPECTED = {
    "tests/data/docstrings_func.py::TestClassFoo::test_in_class_no_docstring": DocstringRecord(
        lineno=7,
        column=4,
        value={},
        nodeid="tests/data/docstrings_func.py::TestClassFoo::test_in_class_no_docstring",
        level="function",
    ),
    "tests/data/docstrings_func.py::TestClassFoo::test_in_class_no_polarion": DocstringRecord(
        lineno=11,
        column=8,
        value={},
        nodeid="tests/data/docstrings_func.py::TestClassFoo::test_in_class_no_polarion",
        level="function",
    ),
    "tests/data/docstrings_func.py::TestClassFoo::test_in_class_polarion": DocstringRecord(
        lineno=17,
        column=8,
        value={
            "assignee": ValueRecord(lineno=1, column=12, value="mkourim"),
            "casecomponent": ValueRecord(lineno=2, column=12, value="nonexistent"),
            "caseimportance": ValueRecord(lineno=3, column=12, value="low"),
            "testSteps": [
                ValueRecord(
                    lineno=6,
                    column=16,
                    value="1. Step with really long description that doesn't fit into one line",
                ),
                ValueRecord(lineno=8, column=16, value="2. Do that"),
            ],
            "expectedResults": [
                ValueRecord(
                    lineno=11,
                    column=16,
                    value="1. Success outcome with really long description that doesn't "
                    "fit into one line",
                ),
                ValueRecord(lineno=13, column=16, value="2. second"),
            ],
            "title": ValueRecord(
                lineno=15,
                column=12,
                value="Some test with really long description that doesn't fit into one line",
            ),
            "setup": ValueRecord(
                lineno=18, column=12, value="Do this:\n- first thing\n- second thing"
            ),
            "teardown": ValueRecord(lineno=22, column=12, value="Tear it down"),
            "caselevel": ValueRecord(lineno=23, column=12, value="level1"),
            "caseautomation": ValueRecord(lineno=24, column=12, value="automated"),
            "linkedWorkItems": ValueRecord(lineno=25, column=12, value=["FOO", "BAR"]),
            "foo": ValueRecord(lineno=26, column=12, value="this is an unknown field"),
            "description": ValueRecord(lineno=27, column=12, value="ignored"),
        },
        nodeid="tests/data/docstrings_func.py::TestClassFoo::test_in_class_polarion",
        level="function",
    ),
    "tests/data/docstrings_func.py::test_annotated_no_docstring": DocstringRecord(
        lineno=51,
        column=0,
        value={},
        nodeid="tests/data/docstrings_func.py::test_annotated_no_docstring",
        level="function",
    ),
    "tests/data/docstrings_func.py::test_standalone_no_docstring": DocstringRecord(
        lineno=55,
        column=0,
        value={},
        nodeid="tests/data/docstrings_func.py::test_standalone_no_docstring",
        level="function",
    ),
    "tests/data/docstrings_func.py::test_annotated_no_polarion": DocstringRecord(
        lineno=61,
        column=4,
        value={},
        nodeid="tests/data/docstrings_func.py::test_annotated_no_polarion",
        level="function",
    ),
    "tests/data/docstrings_func.py::test_annotated_polarion": DocstringRecord(
        lineno=69,
        column=4,
        value={
            "assignee": ValueRecord(lineno=1, column=8, value="mkourim"),
            "initialEstimate": ValueRecord(lineno=2, column=8, value="1/4h"),
            "testSteps": ValueRecord(lineno=3, column=8, value="wrong"),
            "expectedResults": ValueRecord(lineno=6, column=8, value=""),
        },
        nodeid="tests/data/docstrings_func.py::test_annotated_polarion",
        level="function",
    ),
    "tests/data/docstrings_func.py::test_blacklisted": DocstringRecord(
        lineno=82,
        column=4,
        value={"initialEstimate": ValueRecord(lineno=1, column=8, value="1/4h")},
        nodeid="tests/data/docstrings_func.py::test_blacklisted",
        level="function",
    ),
    "tests/data/docstrings_func.py::test_blacklisted_and_whitelisted": DocstringRecord(
        lineno=90,
        column=4,
        value={
            "initialEstimate": ValueRecord(lineno=1, column=8, value="1/4"),
            "_errors_parsing": [
                ErrorRecord(
                    lineno=2, column=12, type="indent", message="Wrong indentation, line ignored"
                )
            ],
        },
        nodeid="tests/data/docstrings_func.py::test_blacklisted_and_whitelisted",
        level="function",
    ),
    "tests/data/docstrings_func.py::test_wrong_steps_indent": DocstringRecord(
        lineno=97,
        column=4,
        value={
            "initialEstimate": ValueRecord(lineno=1, column=8, value="1/4m"),
            "testSteps": [
                ValueRecord(
                    lineno=3,
                    column=12,
                    value="1. Step with really long description that doesn't fit into one line",
                )
            ],
            "_errors_parsing": [
                ErrorRecord(
                    lineno=5, column=15, type="indent", message="Wrong indentation, line ignored"
                )
            ],
        },
        nodeid="tests/data/docstrings_func.py::test_wrong_steps_indent",
        level="function",
    ),
    "tests/data/docstrings_func.py::test_multiline": DocstringRecord(
        lineno=107,
        column=4,
        value={
            "assignee": ValueRecord(lineno=2, column=8, value="mkourim"),
            "initialEstimate": ValueRecord(lineno=3, column=8, value="1/4h"),
            "title": ValueRecord(
                lineno=4, column=8, value="Test multiple tenant quotas simultaneously"
            ),
            "testSteps": [
                ValueRecord(lineno=8, column=12, value="1."),
                ValueRecord(lineno=9, column=12, value="2. Log something"),
            ],
            "expectedResults": [
                ValueRecord(lineno=13, column=12, value="1."),
                ValueRecord(
                    lineno=14,
                    column=12,
                    value='2. <NoMethodError>: <undefined method `service_resources" for '
                    "nil:NilClass> [----] E, [2018-01-06T11:11:20.074019 #13027:e0ffc4] "
                    'ERROR -- :"',
                ),
            ],
            "linkedWorkItems": ValueRecord(lineno=17, column=8, value=["FOO", "BAR", "BAZ"]),
        },
        nodeid="tests/data/docstrings_func.py::test_multiline",
        level="function",
    ),
    "tests/data/docstrings_func.py::test_ignore": DocstringRecord(
        lineno=130,
        column=4,
        value={"ignore": ValueRecord(lineno=1, column=8, value=True)},
        nodeid="tests/data/docstrings_func.py::test_ignore",
        level="function",
    ),
    "tests/data/docstrings_func.py::test_noignore": DocstringRecord(
        lineno=137,
        column=4,
        value={
            "ignore": ValueRecord(lineno=1, column=8, value=False),
            "assignee": ValueRecord(lineno=2, column=8, value="mkourim"),
        },
        nodeid="tests/data/docstrings_func.py::test_noignore",
        level="function",
    ),
}


def test_parser(source_file):
    docstrings = get_docstrings_in_file(source_file)
    assert docstrings == EXPECTED


def test_strip_1():
    docstring = """
    FOO
    BAR

    Polarion:
        initialEstimate: 1/4h
        title: >

        testSteps:
        expectedResults:
            1.
            2. >
               <NoMethodError>: <undefined method `service_resources" for

    BAZ
    """
    stripped = strip_polarion_data(docstring)
    assert stripped == "    FOO\n    BAR\n\n    BAZ"


def test_strip_2():
    docstring = """
    FOO

    BAR
    Polarion:
        testSteps:
        expectedResults:
            1.
            2. >
               <NoMethodError>: <undefined method `service_resources" for

    BAZ
    """
    stripped = strip_polarion_data(docstring)
    assert stripped == "    FOO\n\n    BAR\n    BAZ"


def test_linked_items_1():
    docstring = """
    Polarion:
        expectedResults:
            1. >
               something
        linkedWorkItems: >
            foo, bar,
            baz
    """
    expected = {
        "expectedResults": [ValueRecord(lineno=2, column=12, value="1. something")],
        "linkedWorkItems": ValueRecord(lineno=4, column=8, value=["foo", "bar", "baz"]),
    }
    parsed = parse_docstring(docstring)
    assert parsed == expected


def test_linked_items_2():
    docstring = """
    Polarion:
        linkedWorkItems: foo,bar , baz
    """
    expected = {"linkedWorkItems": ValueRecord(lineno=1, column=8, value=["foo", "bar", "baz"])}
    parsed = parse_docstring(docstring)
    assert parsed == expected


def test_linked_items_3():
    docstring = """
    Polarion:
        linkedWorkItems: foo
            bar
            baz
    """
    expected = {"linkedWorkItems": ValueRecord(lineno=1, column=8, value=["foo", "bar", "baz"])}
    parsed = parse_docstring(docstring)
    assert parsed == expected


def test_linked_items_4():
    docstring = """
    Polarion:
        linkedWorkItems:
            foo
            bar
            baz
    """
    expected = {"linkedWorkItems": ValueRecord(lineno=1, column=8, value=["foo", "bar", "baz"])}
    parsed = parse_docstring(docstring)
    assert parsed == expected


def test_multiline_1():
    docstring = """
    Polarion:
        testSteps:
            1. >
               FOO
            2. >
               BAR
        expectedResults:
            1. >
               BAR
            2. >
               FOO
        title: >
            Test multiple tenant
            quotas simultaneously
    """
    expected = {
        "testSteps": [
            ValueRecord(lineno=2, column=12, value="1. FOO"),
            ValueRecord(lineno=4, column=12, value="2. BAR"),
        ],
        "expectedResults": [
            ValueRecord(lineno=7, column=12, value="1. BAR"),
            ValueRecord(lineno=9, column=12, value="2. FOO"),
        ],
        "title": ValueRecord(
            lineno=11, column=8, value="Test multiple tenant quotas simultaneously"
        ),
    }
    parsed = parse_docstring(docstring)
    assert parsed == expected


def test_multiline_2():
    docstring = """
    Polarion:
        testSteps:
            1.
               FOO
            2.
               BAR
        expectedResults:
            1.
               BAR
            2.
               FOO
        title:
            Test multiple tenant
            quotas simultaneously
    """
    expected = {
        "testSteps": [
            ValueRecord(lineno=2, column=12, value="1. FOO"),
            ValueRecord(lineno=4, column=12, value="2. BAR"),
        ],
        "expectedResults": [
            ValueRecord(lineno=7, column=12, value="1. BAR"),
            ValueRecord(lineno=9, column=12, value="2. FOO"),
        ],
        "title": ValueRecord(
            lineno=11, column=8, value="Test multiple tenant quotas simultaneously"
        ),
    }
    parsed = parse_docstring(docstring)
    assert parsed == expected


def test_multiline_3():
    docstring = """
    Polarion:
        testSteps:
            1. >
               FOO: BAR
            2. >
               BAR: BAZ
    """
    expected = {
        "testSteps": [
            ValueRecord(lineno=2, column=12, value="1. FOO: BAR"),
            ValueRecord(lineno=4, column=12, value="2. BAR: BAZ"),
        ]
    }
    parsed = parse_docstring(docstring)
    assert parsed == expected
