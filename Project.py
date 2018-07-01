"""
Find differences in file contents.
"""

IDENTICAL = -1

def singleline_diff(line1, line2):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
    Output:
      Returns the index where the first difference between
      line1 and line2 occurs.
      Returns IDENTICAL if the two lines are the same.
    """
    len1 = len(line1)
    len2 = len(line2)
    if len1 < len2: 
        for index in range(len1):
            if line1[index] != line2[index]:
                return index
        return len1 
    elif len1 > len2:
        for index in range(len2):
            if line1[index] != line2[index]:
                return index
        return len2
    else:
        for index in range(len1):
            if line1[index] != line2[index]:
                return index   
    return IDENTICAL


def singleline_diff_format(line1, line2, idx):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
      idx   - index at which to indicate difference
    Output:
      Returns a three line formatted string showing the location
      of the first difference between line1 and line2.
    """
    new1 = line1.find("\n")
    new2 = line2.find("\n")
    if new1 != -1 or new2 != -1:
        return ""
    len1 = len(line1)
    len2 = len(line2)
    if len1 < len2:
        if idx < 0 or idx > len1:
            return ""
    else:
        if idx < 0 or idx > len2:
            return ""
    second = "" 
    for index in range(idx + 1):
        if index == idx:
            second += "^"
            break
        else:
            second += "="
    return line1 + "\n" + second + "\n" + line2 + "\n"

def multiline_diff(lines1, lines2):
    """
    Inputs:
      lines1 - list of single line strings
      lines2 - list of single line strings
    Output:
      Returns a tuple containing the line number (starting from 0) and
      the index in that line where the first difference between lines1
      and lines2 occurs.
      Returns (IDENTICAL, IDENTICAL) if the two lists are the same.
    """
    len1 = len(lines1)
    len2 = len(lines2) 
    if len1 < len2:
        for index in range(len1):
            diff = singleline_diff(lines1[index], lines2[index])
            if diff != IDENTICAL:
                return (index, diff)
        return (len1, 0)
    elif len1 > len2:
        for index in range(len2):
            diff = singleline_diff(lines1[index], lines2[index])
            if diff != IDENTICAL:
                return (index, diff)
        return (len2, 0)
    else:
        for index in range(len1):
            diff = singleline_diff(lines1[index], lines2[index])
            if diff != IDENTICAL:
                return (index, diff)
    return (IDENTICAL, IDENTICAL)


def get_file_lines(filename):
    """
    Inputs:
      filename - name of file to read
    Output:
      Returns a list of lines from the file named filename.  Each
      line will be a single line string with no newline ('\n') or
      return ('\r') characters.
      If the file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
   
    openfile = open(filename, "rt")
    data = openfile.read()
    if data == "":
        openfile.close()
        return []
    lines = data.split("\n")
    len1 = len(lines)
    openfile.close()
    if len1 == 1 and lines != []:
        return lines
    lines.pop()
    return lines


def file_diff_format(filename1, filename2):
    """
    Inputs:
      filename1 - name of first file
      filename2 - name of second file
    Output:
      Returns a four line string showing the location of the first
      difference between the two files named by the inputs.
    """
    lst1 = get_file_lines(filename1)
    lst2 = get_file_lines(filename2)
    (line, index) = multiline_diff(lst1, lst2)
    if (line == IDENTICAL) and (index == IDENTICAL):
        return "No differences\n"
    len1 = len(lst1)
    len2 = len(lst2)
    if len1 == 0 and len2 != 0:
        line2 = lst2[line]
        fmat = singleline_diff_format("", line2, index)
        return "Line " + str(line) + ":\n" + fmat
    elif len1 != 0 and len2 == 0:
        line1 = lst1[line]
        fmat = singleline_diff_format(line1, "", index)
        return "Line " + str(line) + ":\n" + fmat  
    else:
        line1 = lst1[line]
        line2 = lst2[line]
        fmat = singleline_diff_format(line1, line2, index)
        return "Line " + str(line) + ":\n" + fmat
