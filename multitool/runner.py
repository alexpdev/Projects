import json
import os
import sys
from pathlib import Path
from hashlib import sha1

class Words:
    """
    Namespace containing reference documents for gathering data.
    """
    assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

    all_words = json.load(open(os.path.join(assets, "Words_Length.json")))
    word_freq = json.load(open(os.path.join(assets, "Words_Frequency.json")))
    synonyms = json.load(open(os.path.join(assets, "Synonyms.json")))


def sanatize(input):
    """
    Convert input command line arguments into format contained by documents.
    """
    return input.upper()


def ordprint(namespace):
    """
    Convert characters to their ordinal value.
    """
    print(namespace)
    chars = namespace.chars
    result = ', '.join([str(ord(i)) for i in chars])
    print(result)
    return result


def show(output):
    """
    Format the output to show user on console screen.
    """
    sys.stdout.write("Results: ")
    space = max([len(i) for i in output])
    try:
        size = os.get_terminal_size().columns
    except:
        size = 80
    space = space + 1 + len(str(len(output))) + 2
    cols, counter = size // space, 0
    while counter < len(output):
        line = ""
        if len(output) - counter < cols:
            cols = len(output) - counter
        for i in range(cols):
            word = output[counter].ljust(space, " ")
            phrase = f"{str(i).rjust(3, '0')}. {word}  "
            line += phrase
            counter += 1
    return True


def contains(args):
    """
    Check if words exist that contain the partial word within the word.
    """
    if args.start or args.end:
        if args.start:
            return start(args)
        return end(args)
    else:
        output = []
        inp = sanatize(args.val)
        count = -1 if not count else int(count)
        for _, word in enumerate(Words.all_words):
            if count == 0:
                break
            if args.length and len(word) != int(args.length):
                continue
            if len([part for part in inp if part in word]) == len(inp):
                output.append(word)
                count -= 1
        if output:
            show(output)
            return output
    return output


def start(args):
    """
    Check contains but only from the start of the word.
    """
    output = []
    inp = "".join(sanatize(args.start))
    for _, word in enumerate(Words.all_words):
        print(word)
        if word.startswith(inp):
            output.append(word)
            count -= 1
    if output:
        return show()
    return output


def end(args):
    """
    Check contains but only at the end of the word.
    """
    output = []
    inp = "".join(sanatize(args.end))
    count = -1 if not args.length else int(args.length)
    for _, word in enumerate(Words.all_words):
        if word.endswith(inp):
            print(word)
            output.append(word)
            count -= 1
    if output:
        return show(output)
    return output


def binprint(args):
    """
    Return binary representation of decimal digit.
    """
    value = int(args.value)
    result = bin(value)[2:]
    print(result)
    return result


def mergesort(seq, word):
    if len(seq) <= 1:
        return seq
    left = mergesort(seq[: len(seq) // 2], word)
    right = mergesort(seq[len(seq) // 2 :], word)
    i = j = 0
    lst = []
    while i < len(left) and j < len(right):
        if len(left[i]) < len(right[j]):
            lst.append(left[i])
            i += 1
        elif len(left[i]) > len(right[j]):
            lst.append(right[j])
            j += 1
        elif left[i].index(word) < right[j].index(word):
            lst.append(left[i])
            i += 1
        else:
            lst.append(right[j])
            j += 1
    while i < len(left):
        lst.append(left[i])
        i += 1
    while j < len(right):
        lst.append(right[j])
        j += 1
    return lst


def synonyms(args):
    """
    Return Synonyms for the inputed word.
    """
    w = args.word.lower()
    precision = int(args.precision)
    collection = {}
    for entry in Words.synonyms:
        if w in entry["word"]:
            if entry["word"] in collection:
                collection[entry["word"]].extend(entry["synonyms"])
            else:
                collection[entry["word"]] = entry["synonyms"]
    lst = [w]
    if precision != 1:
        lst = mergesort(list(collection.keys()), w)
    m = min(len(lst), precision)
    for item in lst[:m]:
        output = f":{item} \n"
        prev = []
        for syn in collection[item]:
            if syn not in prev:
                prev.append(syn)
                output += f"\t {syn} \n"
        sys.stdout.write(output)
    return output


def utf(args):
    """
    Convert character codes to their utf-8 symbol.
    """
    sys.stdout.write('----------------------\n\n')
    if args.number:
        for num in args.number:
            if args.list:
                sys.stdout.write(f"{num} {chr(int(num))}\n")
            elif args.line:
                sys.stdout.write(f"({num}: {chr(int(num) )}) ")
            else:
                sys.stdout.write(chr(int(num)) + " ")
    elif args.range:
        for i in range(int(args.range[0]), int(args.range[1])):
            if args.list:
                sys.stdout.write(f"{i} {chr(i)}\n")
            elif args.line:
                sys.stdout.write(f"({i}: {chr(i)} ) ")
            else:
                sys.stdout.write(chr(i))
    sys.stdout.write('\n\n----------------------')
    return True


def walk_path(root):
    if root.is_file():
        size = os.path.getsize(root)
        return 1, size
    count, size = 0, 0
    if root.is_dir():
        for item in root.iterdir():
            c1, s1 = walk_path(item)
            count += c1
            size += s1
    return count, size

def dirinfo(nspace):
    path = Path(nspace.path)
    count, size = walk_path(path)
    out = ""
    if nspace.count:
        out += f"{path}| File Count = {count}\n"
    if nspace.size:
        out += f"{path}| Total Size = {size}\n"
    show(out)
    return True

def find_duplicates(nspace):
    path = nspace.dir
    filenames = os.listdir(nspace.dir)
    auto = nspace.auto
    hashes = {}
    for file in filenames:
        full = os.path.join(path, file)
        if os.path.isfile(full):
            digest = sha1(open(full, "rb").read()).digest()
            if digest not in hashes:
                hashes[digest] = full
            else:
                if auto:
                    os.remove(full)
                else:
                    print(f"Found Duplicate {full} <-> {hashes[digest]}")
                    answer = input("Delete (Y/N):  ").lower()
                    if "y" in answer:
                        os.remove(full)
    return
