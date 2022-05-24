import inspect

from IPython.core.magic import Magics, magics_class, line_magic

@magics_class
class TestMagics(Magics):
    test_path = None

    @line_magic
    def set_test_path(self, line):
        self.test_path = Path(line).resolve()

    @line_magic
    def print_test_path(self, line):
        print(self.test_path)

    @line_magic
    def add_test(self, line):
        """        
        Caveats
        * no imports are added, so you'll likely need to include some of those for the
          test to work
        * if testing the same function more than once, you'll need to rename the tests,
          as they'll all be `test_{func_name}`
        * If you use an existing variable as an argument, extracting the test case will
          only work if that variable can be recreated by evaluating its repr, i.e. if
          `var == eval(repr(var))`.
        * `line` may be evaluated fully or partially more than once while generating the
          test case (so only use pure functions)
        """
        assert line.endswith(")")

        func_name, arg_str = line[:-1].split("(", 1)
        args = eval(arg_str)
        func = self.shell.user_ns[func_name]
        sig = inspect.signature(func)
        param_names = list(sig.parameters.keys())
        expected = repr(eval(line))

        indent = " " * 4
        lines = [
            f"def test_{func_name}():",
            *[f"{indent}{n} = {repr(arg)}" for n, arg in zip(param_names, args)],
            f"{indent}result = {func_name}({', '.join(param_names)})",
            f"{indent}expected = {expected}",
            f"{indent}assert result == expected",
            "", # so we get a trailing newline
        ]
        print_test = False
        test = "\n".join(lines)
        if print_test:
            print(test)
        with open(self.test_path, "a") as f:
            f.write(test)
        return expected

get_ipython().register_magics(TestMagics)
