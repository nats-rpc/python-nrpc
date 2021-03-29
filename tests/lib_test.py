import pytest
import nrpc
import nrpc.lib

import contextlib

try:
    ExitStack = contextlib.ExitStack
except AttributeError:

    def _exit_stack():
        yield

    ExitStack = contextlib.contextmanager(_exit_stack)

test_parse_subject_data = [
    ("", 0, "foo", 0, 0, "foo.bar", [], [], [], "bar", "protobuf", None),
    ("", 0, "foo", 0, 0, "foo.bar.protobuf", [], [], [], "bar", "protobuf", None),
    ("", 0, "foo", 0, 0, "foo.bar.json", [], [], [], "bar", "json", None),
    (
        "",
        0,
        "foo",
        0,
        0,
        "foo.bar.json.protobuf",
        [],
        [],
        [],
        "bar",
        "",
        (nrpc.lib.InvalidSubject, "subject tail is too long"),
    ),
    ("demo", 0, "foo", 0, 0, "demo.foo.bar", [], [], [], "bar", "protobuf", None),
    ("demo", 0, "foo", 0, 0, "demo.foo.bar.json", [], [], [], "bar", "json", None),
    (
        "demo",
        0,
        "foo",
        0,
        0,
        "foo.bar.json",
        [],
        [],
        [],
        "",
        "",
        (nrpc.lib.InvalidSubject, "subject should start with demo"),
    ),
    (
        "demo",
        2,
        "foo",
        0,
        0,
        "demo.p1.p2.foo.bar.json",
        ["p1", "p2"],
        [],
        [],
        "bar",
        "json",
        None,
    ),
    (
        "demo",
        2,
        "foo",
        1,
        0,
        "demo.p1.p2.foo.sp1.bar.json",
        ["p1", "p2"],
        ["sp1"],
        [],
        "bar",
        "json",
        None,
    ),
    (
        "demo.pkg",
        1,
        "nested.svc",
        1,
        0,
        "demo.pkg.p1.nested.svc.sp1.bar",
        ["p1"],
        ["sp1"],
        [],
        "bar",
        "protobuf",
        None,
    ),
]


@pytest.mark.parametrize(
    "pkg_subject,pkg_params_count,svc_subject,svc_params_count,"
    "mt_params_count,subject,"
    "e_pkg_params,e_svc_params,e_mt_params,e_mt_name,e_encoding,e_error",
    test_parse_subject_data,
)
def test_parse_subject(
    pkg_subject,
    pkg_params_count,
    svc_subject,
    svc_params_count,
    mt_params_count,
    subject,
    e_pkg_params,
    e_svc_params,
    e_mt_params,
    e_mt_name,
    e_encoding,
    e_error,
):
    if e_error:
        ctx = pytest.raises(e_error[0], match=e_error[1])
    else:
        ctx = ExitStack()

    with ctx:
        pkg_params, svc_params, mt_name, tail = nrpc.parse_subject(
            pkg_subject, pkg_params_count, svc_subject, svc_params_count, subject
        )
        assert pkg_params == e_pkg_params
        assert svc_params == e_svc_params
        assert mt_name == e_mt_name

        mt_params, encoding = nrpc.parse_subject_tail(mt_params_count, tail)
        assert mt_params == e_mt_params
        assert encoding == e_encoding
