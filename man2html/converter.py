#!/usr/bin/python3

import re

class Converter:
    def __init__(self, man_text, stylesheet_name):
        self.html_parser = HTMLGenerator()
        self.man_text = man_text
        self.html_text = ""
        self.html_header = ""
        self.html_body = ""
        self.stylesheet_name = stylesheet_name

    def gen_html(self):
        return """
<!DOCTYPE html>
<html>
<head>
    %s
    <link rel="stylesheet" type="text/css" href="%s">
</head>
<body>
%s
</body>
</html>""" % (self.html_header, self.stylesheet_name, self.html_body)

    def convert(self):
        try:
            lines = self.man_text
            if lines[0].strip()[0] != "'" and lines[0].strip()[0] != ".":
                raise Exception("Error: file is not a man file")
            text = "".join(lines)
            #print(text)
            self.html_header = self.get_header(lines)
            self.parse_sections(self.get_sections(text))
            self.html_text = self.gen_html()
            self.handle_other_tags()
        except:
            print("Error: file is not a man file")
        return self.html_text

    def handle_other_tags(self):
        self.html_text = self.html_text.replace('\\fB', '<b>')
        self.html_text = self.html_text.replace('\\fI', '<i>')
        self.html_text = self.html_text.replace('\\fP', '</b></i>')
        self.html_text = self.html_text.replace('\\fR', '</b>')
        self.html_text = self.html_text.replace('\\&', '&nbsp;' * 2)
        self.html_text = self.html_text.replace(r'\\', '\\')
        self.html_text = self.html_text.replace('\\e', '/')
        self.html_text = self.html_text.replace('\\-', '- ')


    def get_header(self, file):
        title_pattern = re.compile(
            r'\.TH (?P<page_name>.*?) '
            r'(?P<par>[0-9\-])(?P<date>(.*? |".*?"))'
            r'(?P<source>(".*"|.*? )) (?P<docs>(".*"|.*))')
        title = ""
        for v in file:
            if re.match(title_pattern, v):
                line = re.search(title_pattern, v)

                header = line.group(1)
                partition = line.group(2)
                date = line.group(3)
                source = line.group(4)
                docs = line.group(5)

                html_head = "<title>{}</title>".format(header)

                html_main_header = self.html_parser.generate_main_header(
                    header,
                    partition,
                    date,
                    source,
                    docs)

                title = "%s%s" % (
                    html_head,
                    html_main_header)
                break
        return title

    def get_sections(self, sections):
        section_pattern = re.compile(
            r'(?<!.SH&\.\\\") (?P<section_name>.*?)\n'
            r'(?P<section>.*?)\n.SH',
            re.MULTILINE + re.DOTALL)
        result = re.findall(section_pattern, sections)
        try:
            result[0] = (result[0][0][4:], result[0][1])
        except:
            pass
        return result

    def parse_sections(self, all_sections):
        for section in all_sections:
            self.html_body += self.html_parser.section_start(section[0])
            self.parse_text(section[1])
            self.html_body += self.html_parser.section_end()

    def parse_text(self, text):
        for line in text.split("\n"):
            try:
                self.html_body += self.html_parser.parse_line(line)
            except:
                print(line)

class HTMLGenerator:

    def __init__(self):
        self.tag_functions = {
            "B": self.bold,
            "I": self.italic,
            "BI": self.bi,
            "BR": self.br,
            "IB": self.ib,
            "IR": self.ir,
            "RI": self.ri,
            "LP": self.pp,
            "P": self.pp,
            "PP": self.pp,
            "RS": self.rs,
            "RE": self.re,
            "TP": self.tp,
            "SS": self.ss
            }
        self.dt_written = False
        self.dt_needed = False
        self.br_needed = False
        self.str_length = 0
        self.rs_tabs = 0
        self.ss_tabs = 0
        self.two_fonts_pattern = re.compile(
            r'^\.(?P<tag>(BI|BR|IB|IR|RB|RI))'
            r'(?P<par1>(".*"|.*? ))(?P<par2>(".*"|.*))')
        self.no_parameters_pattern = re.compile(
            r'^\.(?P<tag>(LP|P|PP|RE|RS|TP))'r'.*')
        self.one_parameter_pattern = re.compile(
            r'^\.(?P<tag>(B|I|SS)) (?P<par1>(\".*\"|.*))')
        self.comment_pattern = re.compile(r'^\.\\\".*')
        self.tags_to_skip_pattern = re.compile(
            r'^\.(?P<tag>(TH|ad|bp|br|ce|de|ds|el|ie|if|fi|ft|hy|'
            r'ig|in|na|ne|nf|nh|nr|ps|so|sp|ti|t|.|))')
        self.inline_tags_pattern = re.compile(r'')

    def section_start(self, header):
        return "<h1>" + header + "</h1><p><pre>"

    def section_end(self):
        self.rs_tabs = 0
        self.dt_written = False
        self.dt_needed = False
        self.br_needed = False
        self.ss_tabs = 0
        self.str_length = 0
        return "</pre>"

    def generate_main_header(self, header, partition, date, source, docs):
        return """
    <h1>{0}</h1><br>
    <i>
        Partition: {1}<br>
        Date: {2}<br>
        Source: {3}<br>
        Documentation: {4}
    </i>""".format(header, partition, date, source, docs)

    def add_tabs(self, text):
        if self.br_needed:
            return text + " "
        elif not self.dt_written and self.dt_needed:
            self.dt_written = True
            self.str_length = 0
            return "\n{}{}\n".format(
                "\t" * (self.rs_tabs + self.ss_tabs), text)
        elif self.dt_written and self.dt_needed:
            return "{}{}".format(
                "\t" * (self.rs_tabs + self.ss_tabs + 1), text)
        else:
            return "{}{}".format(
                "\t" * (self.rs_tabs + self.ss_tabs), text)

    def bold(self, text):
        return self.add_tabs("<b>{}</b> ".format(text))

    def italic(self, text):
        return "<i>{}</i> ".format(text)

    def bi(self, text1, text2):
        return "<b>{}</b><i>{}</i>".format(text1, text2)

    def br(self, text1, text2):
        return "<b>{}</b>{}".format(text1, text2)

    def ib(self, text1, text2):
        return "<i>{}</i><b>{}</b>".format(text1, text2)

    def ir(self, text1, text2):
        return "<i>{}</i>{}".format(text1, text2)

    def rb(self, text1, text2):
        return "{}<b>{}</b>".format(text1, text2)

    def ri(self, text1, text2):
        return "{}<i>{}</i>".format(text1, text2)

    def pp(self):
        self.dt_needed = False
        self.str_length = 0
        return "<p>"

    def rs(self):
        self.rs_tabs += 1
        return ""

    def re(self):
        self.rs_tabs -= 1
        return ""

    def tp(self):
        self.dt_written = False
        self.dt_needed = True
        self.br_needed = True
        self.str_length = 0
        return ""

    def ss(self, text):
        if self.ss_tabs == 0:
            self.ss_tabs += 1
        return "   {}".format(text)

    def parse_line(self, text):
        if re.match(self.two_fonts_pattern, text):
            self.br_needed = False
            parsed_text = re.search(self.two_fonts_pattern, text)
            tag = parsed_text.group(1)
            par1 = parsed_text.group(3)
            par2 = parsed_text.group(5)
            return self.add_tabs(self.tag_functions[tag](par1, par2))
        elif re.match(self.no_parameters_pattern, text):
            self.br_needed = False
            tag = re.search(self.no_parameters_pattern, text).group(1)
            return self.tag_functions[tag]()
        elif re.match(self.one_parameter_pattern, text):
            self.br_needed = False
            parsed_text = re.search(self.one_parameter_pattern, text)
            tag = parsed_text.group(1)
            par1 = parsed_text.group(3)
            if tag != "SS":
                return self.add_tabs(self.tag_functions[tag](par1))
            else:
                return self.tag_functions[tag](par1)
        elif re.match(self.comment_pattern, text) \
                or re.match(self.tags_to_skip_pattern, text):
            return ""
        else:
            if self.br_needed or len(text) + self.str_length > 70:
                return "\n{}".format(self.add_tabs(text))
            else:
                self.br_needed = True
                self.str_length += len(text)
                return self.add_tabs(text)
