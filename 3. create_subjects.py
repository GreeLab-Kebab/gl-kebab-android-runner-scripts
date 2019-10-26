#!/usr/bin/python
import os
import sys
import glob2

JS_TO_INJECT = "<script>window.addEventListener('load', function() {console.log('load time: '+(performance.timing.responseEnd - performance.timing.navigationStart) + 'ms');}, false);</script>"

def is_non_empty(x):
    return len(x) != 0

def starts_with(x, c):
    return x[0] == c

def read_lines_from_file(file):
    with open(file, 'r') as f:
        return f.readlines()

def write_lines_to_file(file, lines):
    with open(file, 'w') as f:
        f.writelines(lines)

def main(subjects_dir, candidates_dir, treatments):
    os.system('rm -r %s; cp -r %s %s'%(subjects_dir, candidates_dir, subjects_dir))

    assert(os.path.exists(candidates_dir))
    assert(os.path.exists(subjects_dir))

    subjects = list(
        filter(lambda x: is_non_empty(x) and not starts_with(x, '.'), os.listdir(subjects_dir))
    )
    for subject in subjects:
        for treatment in treatments:
            index_location = locate_index(
                os.path.join(subjects_dir, subject),
                treatment
            )

            index_lines = read_lines_from_file(index_location)
            index_lines.reverse()
            
            ok = False
            for i, line in enumerate(index_lines):
                if "</body>" in line.lower():
                    j = line.lower().index('</body>')
                    index_lines[i] = line[:j] + JS_TO_INJECT + line[j:]
                    ok = True
                    break
            
            assert(ok)

            index_lines.reverse()
            write_lines_to_file(index_location, index_lines)
            print("injected -> ", index_location)



def locate_index(subject_dir, treatment):
    result = glob2.glob(os.path.join(subject_dir, "**", treatment, "index.html"))
    
    if len(result) == 1: 
        return result[0]

    result = glob2.glob(os.path.join(subject_dir, "**", treatment, "*.html"))
    assert(len(result) == 1)

    return result[0]


if __name__ == '__main__':
    if len(sys.argv) == 1:
        subjects_dir = 'Subjects' 
        candidates_dir = 'Candidates'
        treatments = ['0', '1', '2', '3']
    elif len(sys.argv) == 4:
        subjects_dir = sys.argv[1]
        candidates_dir = sys.argv[2]
        treatments = sys.argv[3].split(',')
    else:
        print("Invalid arguments")
        exit(1)

    main(subjects_dir, candidates_dir, treatments)
