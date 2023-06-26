import os
import pytest
import re


class Payload:
    def __init__(self, payload_path, element_paths):
        self.payload_path = payload_path
        self.element_paths = element_paths


@pytest.fixture
def payload_path():
    return Payload(payload_path)


def test_payload(payload_path):
    p = os.path.split(payload_path)
    assert p in {'json', 'jsonld'}
    # with open(payload_path) as fp:
        # p_elements = v


def pytest_generate_tests(metafunc):
    with open('spdx3/data/Payloads.md') as fp:
        for line in fp.readlines():
            if m := re.match(r'^\s*##\s+(\S+)\s$', line):
                args = [m.group(1), []]
            elif m := re.match(r'^\s*-\s+(\S+)\s*$', line):
                args[1].append(m.group1)

    metafunc.parametrize('payload_path', 'foo')
