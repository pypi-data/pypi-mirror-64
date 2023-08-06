import re
from typing import Dict, Pattern, Union


class CommitStyle:
    TYPES: Dict[str, str]
    TYPE_REGEX: Pattern
    BREAK_REGEX: Pattern

    def parse_commit(self, commit: "Commit") -> Dict[str, Union[str, bool]]:
        raise NotImplementedError


class BasicStyle(CommitStyle):
    TYPES: Dict[str, str] = {
        "add": "Added",
        "fix": "Fixed",
        "change": "Changed",
        "remove": "Removed",
        "merge": "Merged",
        "doc": "Documented",
    }

    TYPE_REGEX: Pattern = re.compile(r"^(?P<type>(%s))" % "|".join(TYPES.keys()), re.I)
    BREAK_REGEX: Pattern = re.compile(r"^break(s|ing changes?)?[ :].+$", re.I | re.MULTILINE)

    def parse_commit(self, commit: "Commit") -> Dict[str, Union[str, bool]]:
        commit_type = self.parse_type(commit.subject)
        message = "\n".join([commit.subject] + commit.body)
        is_major = self.is_major(message)
        is_minor = not is_major and self.is_minor(commit_type)
        is_patch = not any((is_major, is_minor))

        return dict(type=commit_type, is_major=is_major, is_minor=is_minor, is_patch=is_patch)

    def parse_type(self, commit_subject: str) -> str:
        type_match = self.TYPE_REGEX.match(commit_subject)
        if type_match:
            return self.TYPES.get(type_match.groupdict().get("type").lower())
        return ""

    def is_minor(self, commit_type: str) -> bool:
        return commit_type == self.TYPES["add"]

    def is_major(self, commit_message: str) -> bool:
        return bool(self.BREAK_REGEX.search(commit_message))


class AngularStyle(CommitStyle):
    TYPES: Dict[str, str] = {
        # 'build': 'Build',
        # 'ci': 'CI',
        "perf": "Performance Improvements",
        "feat": "Features",
        "fix": "Bug Fixes",
        "revert": "Reverts",
        # 'docs': 'Docs',
        # 'style': '',
        "refactor": "Code Refactoring",
        # 'test': '',
        # 'chore': '',
    }
    SUBJECT_REGEX: Pattern = re.compile(
        r"^(?P<type>(%s))(?:\((?P<scope>.+)\))?: (?P<subject>.+)$" % ("|".join(TYPES.keys()))
    )
    BREAK_REGEX: Pattern = re.compile(r"^break(s|ing changes?)?[ :].+$", re.I | re.MULTILINE)

    def parse_commit(self, commit: "Commit") -> Dict[str, Union[str, bool]]:
        subject = self.parse_subject(commit.subject)
        message = "\n".join([commit.subject] + commit.body)
        is_major = self.is_major(message)
        is_minor = not is_major and self.is_minor(subject["type"])
        is_patch = not any((is_major, is_minor))

        return dict(
            type=subject["type"],
            scope=subject["scope"],
            subject=subject["subject"],
            is_major=is_major,
            is_minor=is_minor,
            is_patch=is_patch,
        )

    def parse_subject(self, commit_subject: str) -> Dict[str, str]:
        subject_match = self.SUBJECT_REGEX.match(commit_subject)
        if subject_match:
            dct = subject_match.groupdict()
            dct["type"] = self.TYPES[dct["type"]]
            return dct
        return {"type": "", "scope": "", "subject": commit_subject}

    def is_minor(self, commit_type: str) -> bool:
        return commit_type == self.TYPES["feat"]

    def is_major(self, commit_message: str) -> bool:
        return bool(self.BREAK_REGEX.search(commit_message))


class AtomStyle(CommitStyle):
    TYPES: Dict[str, str] = {
        ":art:": "",  # when improving the format/structure of the code
        ":racehorse:": "",  # when improving performance
        ":non-potable_water:": "",  # when plugging memory leaks
        ":memo:": "",  # when writing docs
        ":penguin:": "",  # when fixing something on Linux
        ":apple:": "",  # when fixing something on Mac OS
        ":checkered_flag:": "",  # when fixing something on Windows
        ":bug:": "",  # when fixing a bug
        ":fire:": "",  # when removing code or files
        ":green_heart:": "",  # when fixing the CI build
        ":white_check_mark:": "",  # when adding tests
        ":lock:": "",  # when dealing with security
        ":arrow_up:": "",  # when upgrading dependencies
        ":arrow_down:": "",  # when downgrading dependencies
        ":shirt:": "",  # when removing linter warnings
    }
