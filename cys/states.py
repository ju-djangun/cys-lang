from abc import ABC, abstractmethod

from alt import AbstractLineTreeManager, Node


class LineContext:
    _state = None
    line_tree = None

    def __init__(self, state, tree_manager: AbstractLineTreeManager) -> None:
        """
        LineContext has State() for starting, tree_manager to create line tree.
        """
        self.set_line_context(state)
        self.line_tree = tree_manager

    def set_line_context(self, state) -> None:
        """
        LineContext setter for State Pattern.
        """
        self._state = state
        self._state.linecontext = self
        self._state.line_tree = self.line_tree

    def is_last_colon(self, line: str) -> bool:
        if line[-1] == r":":
            return True
        else:
            return False

    def is_not_comment(self, line: str) -> bool:
        not_comment_flag = True
        striped_line: str = line.lstrip()
        if striped_line[0] == "#":
            not_comment_flag = False
        return not_comment_flag

    def line_validate(self, code_line: str):
        """
        For checking codeline validation.
        """
        if len(code_line) == 0 or len(code_line.strip()) == 0:
            return False
        else:
            return self.is_not_comment(code_line)

    def get_indent_depth(self, line: str, indent_size: int) -> int:
        tab_2_space_line: str = line.replace("\t", " ")
        striped_line: str = line.lstrip()
        indented_space: int = len(tab_2_space_line) - len(striped_line)
        indent_depth: int = indented_space // indent_size
        return indent_depth

    def extract_line(self, line: str, line_no: int):
        if self.line_validate(line):
            indent_depth = self.get_indent_depth(line, 4)  # todo : indent size
            is_last_colon = self.is_last_colon(line)
            line_data = {
                "line_no": line_no,
                "indent_depth": indent_depth,
                "is_last_colon": is_last_colon,
                }
            return line_data
        else:
            False

    def insert_line(self, line, line_no):
        """
        Insert new codeline in syntax tree.
        > self.line_tree.node_cursor = ?
        method chaining unable.
        required info : s or e, depth, 
        """
        line_data = self.extract_line(line, line_no)
        if line_data:
            self._state.move_state(line_data)
            new_node = self.line_tree.create_node(
                f"{self._state.node_type}_{line_no}",
                self._state.clean_codeline(line),
                line_data,
            )
            parent = self._state.find_parent(line_data)
            # 부모 노드 찾기. 기본은 노드 커서.
            self.line_tree.node_cursor = parent
            self.line_tree.node_cursor = self._state.find_node_cursor(new_node)
            # E는 기존 커서, S는 자기 자신을 커서로 설정.
            self.line_tree.adopt_node(new_node, parent)


class State(ABC):
    """
    상태 전이는 전부 state 쪽에 몰아넣지만, 그 입력값이나 연산 로직은 context에 몰아넣기.
    """
    line_tree = None
    node_type: str = ""

    @property
    def linecontext(self) -> LineContext:
        return self._linecontext

    @linecontext.setter
    def linecontext(self, linecontext: LineContext) -> None:
        self._linecontext = linecontext

    @abstractmethod
    def move_state(self, line_data):
        pass

    @abstractmethod
    def find_node_cursor(self, new_node):
        pass

    @abstractmethod
    def clean_codeline(self, line):
        pass

    def find_parent(self, line_data) -> Node:
        # depth로 pedgree tracing
        new_node_indent: int = line_data['indent_depth']
        cursor_indent: int = self.line_tree.get_cursor_indent()
        pedi_list = self.line_tree.get_cursor_pedigree()
        if cursor_indent + 1 >= new_node_indent:
            return pedi_list[cursor_indent + 1 - new_node_indent]
        else:
            self.linecontext.set_line_context(Wrong())
            return self.line_tree.node_cursor


class Begin(State):
    """
    Already has root node. For pre-processing or config
    """
    node_type = "B"

    def move_state(self, line_data):
        if line_data["is_last_colon"]:
            self.linecontext.set_line_context(Statement())
        else:
            self.linecontext.set_line_context(Expression())

    def find_node_cursor(self, new_node):
        """
        In ALTreeManager __init__.
        """
        pass

    def clean_codeline(self, line):
        return line


class Expression(State):
    node_type = "E"

    def move_state(self, line_data):
        if line_data["is_last_colon"]:
            self.linecontext.set_line_context(Statement())
    
    def find_node_cursor(self, new_node):
        """
        return parent node
        """
        return self.line_tree.node_cursor # self

    def clean_codeline(self, line):
        return line


class Statement(State):
    node_type = "S"

    def move_state(self, line_data):
        if not line_data["is_last_colon"]:
            self.linecontext.set_line_context(Expression())

    def find_node_cursor(self, new_node):
        """
        return self
        """
        return new_node

    def clean_codeline(self, line):
        cleaned_line = line.rstrip().rstrip(":")
        return cleaned_line


class Wrong(State):
    node_type = "W"

    def move_state(self, line_data):
        print(
            f"Error: line {line_data['line_no']} has undefined state.\n\n " + \
            "Error code -> {line_data['line']}"
            )

    def find_node_cursor(self, new_node):
        """
        return self
        """
        return new_node

    def clean_codeline(self, line):
        pass
