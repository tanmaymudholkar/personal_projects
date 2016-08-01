#!/usr/bin/env python

from __future__ import print_function, division
import re, sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument("wallfile_name", help="name of file containing raw wall text")
args = parser.parse_args()
wallfile = open(args.wallfile_name)

max_multiple_of_3 = 12

def parse_line(line):
    if (re.match(r' *$', line)):
        return ["empty", 0, line]
    if (re.match(r'---\+\+', line)):
        return ["new_day", 0, line[6:]]
    for multiple_of_three in range(1, 1+max_multiple_of_3//3):
        if(re.match(r' {%d}\*'%(3*multiple_of_three), line)):
            return ["spaces", 3*multiple_of_three, line[2+3*multiple_of_three:]]
    print ("Error encountered! Unidentified line: %s"%(line))
    sys.exit()
    
if __name__=="__main__":
    loop_level=0
    output_string=""
    for line in wallfile:
        parsed_line = parse_line(line)
        if (parsed_line[0]=="empty"):
            continue
        if (parsed_line[0]=="new_day"):
            while (loop_level > 0):
                output_string += r"""\end{itemize}
                """
                loop_level += -1
            
            output_string += r"""\end{frame}

            \begin{frame}
            \frametitle{"""
            output_string += parsed_line[2]
            output_string += r"""}
            """
        elif (parsed_line[0]=="spaces"):
            new_loop_level = parsed_line[1]//3
            if (new_loop_level > loop_level):
                output_string += r"""\begin{itemize}
                """
            if (new_loop_level < loop_level):
                output_string += r"""\end{itemize}
                """
            loop_level = new_loop_level
            output_string += r"\item %s"%(parsed_line[2])

        # print ("Type: %s   If spaces then number of spaces: %d    Line: %s"%(parsed_line[0], parsed_line[1], parsed_line[2]))
    print ("Output string is:\n%s"%(output_string))
