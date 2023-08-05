import shutil
import pprint


class QuitPaginateException(Exception):
    pass


class PaginationError(Exception):
    pass


class LineNumbers:
    """
    Prepend line numbers to a string.
    """

    def __init__(self, start: int = 0):
        """
        Take a string '<x>' and return an string prefixed by a line number
        of the form '<start> : <x>'. Where start is greater than one. if start
        is 0 (zero) then LineNumbers just returns the input string unaltered.

        :param start:
        """
        self._line_number = start

    @property
    def line_numbers(self):
        return self._line_numbers

    @line_numbers.setter
    def line_number(self, line_number: int):
        """
        :type line_number: int
        """
        self._line_number = line_number

    @staticmethod
    def prefix(number):
        """

        :param number: If None return an empty prefix
        :return: a prefix string
        """
        if number:
            return f'{number:<3}: '
        else:
            return ""

    def line_number(self, s):
        """
        Take a string and return a prefixed string and the new string size
        :param s: string to have a prefix added
        :return: (size, prefixed string)
        """
        if self._line_number:
            p = LineNumbers.prefix(self._line_number)
            x = f"{p}{s}"
            return len(p), x

        else:
            return 0, s


class Pager:
    """
    Provide paginating services allow content to be paginated
    using shutil to determine screen dimensions
    """

    def __init__(self,
                 paginate: bool = True,
                 paginate_prompt: str = "Hit Return to continue (q or quit to exit)",
                 output_filename: str = None,
                 line_numbers: bool = True):
        """

        :param paginate: paginate at terminal boundaries
        :param output_filename: send output to file as well
        :param line_number: if 0 no line numbers are emitted. If 1 or more
        start line_numbers from that point and auto increment with
        line_number function.

        """
        self._paginate = paginate
        self._output_filename = output_filename
        self._output_file = None
        self._line_numbers = line_numbers
        self._paginate_prompt = paginate_prompt

        assert type(paginate_prompt) is str

    @property
    def line_numbers(self):
        return self._line_numbers

    @staticmethod
    def prefix(number):
        return LineNumbers.prefix(number)

    def line_to_paragraph(self, line: str, width: int = 80, line_number: int = 0) -> list:
        """
        Take a line and split into separate lines at width boundaries
        also if self.line_numbers > 0 then add the defined line number prefix
        to each line.

        :param line: A string of input
        :param width: the size of the terminal in columns
        :param line_number: Start incrementing line numbers from this number.
        :return: A list of strings split at width boundaries from line
        """
        lines: list = []
        prefix = self.prefix(line_number)
        prefix_size = len(prefix)

        while prefix_size + len(line) > width:

            if prefix_size < width:
                segment: str = prefix + line[0:width - prefix_size]
                lines.append(segment)
                line: str = line[width - prefix_size:]

                if line_number:
                    line_number = line_number + 1
                    prefix = self.prefix(line_number)
                    prefix_size = len(prefix)
            else:
                segment: str = self.prefix(line_number)[0:width]
                lines.append(segment)
                line: str = ""

        if len(line) > 0:
            lines.append(self.prefix(line_number) + line)

        return lines

    def paginate_lines(self, lines: list):
        """
        Outputs lines to a terminal. It uses
        `shutil.get_terminal_size` to determine the height of the terminal.
        It expects an iterator that returns a line at a time and those lines
        should be terminated by a valid newline sequence.

        Behaviour is controlled by a number of external class properties.

        `paginate` : Is on by default and triggers pagination. Without `paginate`
        all output is written straight to the screen.

        `output_file` : By assigning a name to this property we can ensure that
        all output is sent to the corresponding file. Prompts are not output.

        `pretty_print` : If this is set (default is on) then all output is
        pretty printed with `pprint`. If it is off then the output is just
        written to the screen.


        :param lines:
        :return: paginated output
        """
        try:
            if self._output_filename:
                self._output_file = open(self._output_filename, "a+")

            output_lines = []
            prompt_lines = []
            overflow_lines = []
            if self._line_numbers:
                line_number = 1
            else:
                line_number = 0

            for l in lines:
                # a line can be less than terminal width  - line number width. Just output it.
                # a line can be more than terminal width - line number width. Output the line number
                # and the line[0:terminal_width - line_number_width].
                if self._output_file:
                    self._output_file.write(f"{l}\n")
                    self._output_file.flush()

                if self._paginate:
                    terminal_columns, terminal_lines = shutil.get_terminal_size(fallback=(80, 24))
                    if terminal_lines < 2:
                        raise PaginationError("Only 1 display line for output, I need at least two")

                    # is the pagination prompt wider than the screen? If it is then we need to
                    # fold it into a number of lines. This will be subtracted from the available
                    # vertical display real estate.
                    # We calculate the prompt size first so we know how many lines are left from
                    # program output. Probably not a good idea to make your prompt longer than
                    # 80 columns.
                    prompt_lines = self.line_to_paragraph(self._paginate_prompt,
                                                          terminal_columns)  # No line numbers

                    multi_line = overflow_lines + self.line_to_paragraph(l, terminal_columns, line_number)
                    overflow_lines = []
                    # print(f"{multi_line}")
                    line_number = line_number + len(multi_line)
                    buffer_length = len(output_lines) + len(multi_line)
                    terminal_lines = terminal_lines - len(prompt_lines)  # leave room to output prompt

                    if buffer_length < terminal_lines:
                        output_lines.extend(multi_line)
                        continue
                    if buffer_length == terminal_lines:
                        output_lines.extend(multi_line)
                    elif buffer_length > terminal_lines:
                        overflow = buffer_length - terminal_lines
                        output_lines.extend(multi_line[0:overflow])
                        overflow_lines = multi_line[overflow:]

                    for data in output_lines:
                        print(f"{data}")

                    #
                    # Output potentially multi-line prompt string.
                    #
                    for i, line_counter in enumerate(prompt_lines, 1):
                        if i == len(prompt_lines):
                            print(f"{line_counter}", end="")
                        else:
                            print(f"{line_counter}")
                    user_input = input()
                    if user_input.lower().strip() in ["q", "quit", "exit"]:
                        raise QuitPaginateException
                    output_lines = []
                else:
                    for line in multi_line:
                        print(f"{line}")
            # if self._paginate:
            #         user_input = input()
            #         if user_input.lower().strip() in ["q", "quit", "exit"]:
            #             raise QuitPaginateException

            for i in output_lines:
                print(f"{i}")

        except QuitPaginateException:
            pass

        except KeyboardInterrupt:
            print("ctrl-C...")
        finally:
            if self._output_file:
                self._output_file.close()

    def doc_to_lines(self, doc, format_func=None):
        """
        Generator that converts a doc to a sequence of lines.
        :param doc: A dictionary
        :param format_func: customisable formatter defaults to pformat
        :return: a generator yielding a line at a time
        """
        if format_func:
            for l in format_func(doc).splitlines():
                yield l
        elif self.pretty_print:
            for l in pprint.pformat(doc).splitlines():
                yield l
        else:
            for l in str(doc).splitlines():
                yield l
