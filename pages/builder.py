# Builder.py v1.0.1
# Build all files in a directory by adding content to templates.
# Requires Python 3.x

# THE FORMAT
# To avoid conflicting with standard HTML, metadata is stored in standard HTML comments:
#   <!-- $command -->
# There can be a maximum of ONE command per line; later commands will be ignored.
# Commands should be included on their own line, because the line containing the command
# will be removed from the output.
# There are two kinds of files: templates and pages; each has its own set of commands.
# Essentially, templates include sections from the pages by inserting the contents
# of the section wherever the include was.

# Page commands:
#  Use these before any section tags; don't put them twice:
#   $template <file>    -- Use a template out of the templates directory
#   $output <directory> -- Copy this file into a different directory (instead of '../');
#                          the directory must exist or an error will occur! Please note
#                          that the path is relative to the location of this file.
#
#   $begin              -- Ends the 'header', begins the content. If not included,
#                          you will probably experience errors!
#  Available after the header:
#   $section <name>     -- Use the content between this tag and an $endsection to
#                          replace a section placeholder in the layout. Nesting is
#                          not allowed!
#   $endsection         -- End a section. There must be one of these for every
#                          $section tag.
#
# If a template is not used, the file will be copied as-is. Otherwise, if there is
# any text outside a section, IT WILL BE REMOVED FROM THE OUTPUT! Unused
# sections are not added to the output either.

# Template commands:
#   $include <name> -- Replace this tag with the contents of a section defined in
#                      the page.
#   $req-include <name> -- Same as $include, but raises a ParseException if the
#                          section is not defined.

# Templates are also run through the page parser, so that you can apply super-templates
# to them. This also means that they require the $begin command before the content!

import os
import os.path
import glob
import time
import sys

verbose = False

if len(sys.argv) > 1:
    if sys.argv[1] == '-v' or sys.argv[1] == '--verbose':
        verbose = True

def printv(v):
    if verbose:
        print(v)

template_dir = "templates/"

class ParseException(Exception):
    pass

class Parser:
    def parse(self, command):
        pass
    def parseLine(self, line):
        pass
    def end(self):
        pass

class PageParser(Parser):

    def __init__(self, default_outdir):
        self.header = True
        self.section = None
        self.template = None
        self.sections = {}
        self.outdir = default_outdir

    def parse(self, command):
        cmd = command.split(" ")
        if cmd[0] == "template":
            if not self.header:
                raise ParseException("Template command outside header!")
            if self.template:
                raise ParseException("Template already set!")
            if len(cmd) < 2:
                raise ParseException("Not enough arguments for template");
            printv("Using template file " + cmd[1])
            self.template = template_dir + cmd[1]
        elif cmd[0] == "output":
            if not self.header:
                raise ParseException("Output command outside header!")
            if len(cmd) < 2:
                raise ParseException("Not enough arguments for output")
            printv("Using output directory " + cmd[1])
            self.outdir = cmd[1]
        elif cmd[0] == "begin":
            if not self.header:
                raise ParseException("Multiple begin commands!")
            printv("Begin content")
            self.header = False
        elif cmd[0] == "section":
            if self.header:
                raise ParseException("Cannot start section in header!")
            if self.section:
                raise ParseException("Cannot nest sections!")
            if len(cmd) < 2:
                raise ParseException("Not enough arguments for section")
            printv("Start section " + cmd[1])
            section_name = cmd[1]
            if section_name in self.sections:
                raise ParseException("Duplicate section name " + section_name)
            self.section = section_name
            self.sections[section_name] = []
        elif cmd[0] == "endsection":
            if self.header:
                raise ParseException("Cannot end section in header!")
            if not self.section:
                raise ParseException("No section to end!")
            printv("End section " + self.section)
            self.section = None
        else:
            return 1
        return 0

    def parseLine(self, line):
        if self.section:
            self.sections[self.section].append(line);

    def end(self):
        if self.header:
            raise ParseException("Reached end of file; no begin command found!")
        if self.section:
            raise ParseException("Reached end of file; could not find end of section " + self.section)

class TemplateParser(Parser):
    def __init__(self, sections, outfile):
        self.sections = sections
        self.outfile = outfile

    def addsection(self, section):
        for line in section:
            self.outfile.write(line)

    def parse(self, command):
        cmd = command.split(" ")
        if cmd[0] == "include":
            if len(cmd) < 2:
                raise ParseException("Not enough arguments for include")
            if cmd[1] in self.sections:
                printv("Inserting section " + cmd[1])
                self.addsection(self.sections[cmd[1]])
            else:
                return 1 # Keep missing includes
        elif cmd[0] == "req-include":
            if len(cmd) < 2:
                raise ParseException("Not enough arguments for req-include")
            if cmd[1] in self.sections:
                printv("Inserting section " + cmd[1])
                self.addsection(self.sections[cmd[1]])
            else:
                raise ParseException("Undefined section: '" + cmd[1] + "'")
        else:
            return 1
        return 0

    def parseLine(self, line):
        self.outfile.write(line)

class Copier(Parser):
    def __init__(self, outfile):
        self.outfile = outfile

    def parse(self, command):
        cmd = command.split(" ")
        if cmd[0] == "include" or cmd[0] == "req-include":
            return 1
        return 0

    def parseLine(self, line):
        self.outfile.write(line)

def parse(filename, parser):
    with open(filename, "r") as f:
        for line in f:
            if '<!--' in line and '-->' in line:
                start = line.find('<!--') + 4
                end = line.find("-->") - 1
                content = line[start:end].strip()
                if content.startswith('$'):
                    content = content[1:]
                    # print("Parsing '" + content + "'")
                    missingno = parser.parse(content)
                    if missingno:
                        parser.parseLine(line) # Don't remove unknown commands
                else:
                    parser.parseLine(line)
            else:
                parser.parseLine(line)
        parser.end()

def parse_page(filename, default_outdir=".."):
    print("Parsing page " + filename)
    page_parser = PageParser(default_outdir)
    parse(filename, page_parser) # Fill it up with data
    return page_parser

def write_page(filename, page_parser):
    # Open up an output file for the template parser (write a tmp file in case of errors)
    with open(page_parser.outdir + "/" + filename + ".partial", "w") as outfile:
        printv("Parsing template and writing output")
        if not page_parser.template:
            printv("No template; copying file as-is")
            copier = Copier(outfile)
            parse(filename, copier)
        else:
            template_parser = TemplateParser(page_parser.sections, outfile)
            parse("generated/" + page_parser.template, template_parser)
    targetname = page_parser.outdir + "/" + filename
    print("Updating " + targetname)
    if (os.path.exists(targetname)):
        os.remove(targetname)
    os.rename(targetname + ".partial", targetname)

def parse_template(filename):
    printv("Parsing template requirement " + filename)
    pp = parse_page(filename, "generated")
    if pp.template:
        if pp.template == filename:
            raise ParseException("Infinite recursion is not allowed")
        else:
            parse_template(pp.template)
    write_page(filename, pp)

def main():
    printv("Scanning directory for HTML files")
    for file in glob.glob("*.html"):
        page_parser = parse_page(file)
        if page_parser.template:
            parse_template(page_parser.template) # Generate required templates
        write_page(file, page_parser)

start = time.perf_counter()
main()
end = time.perf_counter()
elapsed = end - start
print("Done! (%.4f s)" % elapsed);
