import json
import hashlib
import random
import itertools

class TemplateDef:
    def __init__(self, name, tags, prompts, thinking, code, generator):
        self.name = name
        self.tags = tags
        self.prompts = prompts
        self.thinking = thinking
        self.code = code
        self.generator = generator

TEMPLATES = []

def register_template(name, tags, prompts, thinking, code, generator):
    TEMPLATES.append(TemplateDef(name, tags, prompts, thinking, code, generator))

# -------- TEMPLATES --------

def object_gen():
    types = ["int", "string", "float", "bool", "char"]
    obj_names = ["User", "Product", "Config", "Server", "Account", "Device", "Message", "Session"]
    field1_names = ["id", "identifier", "uid", "code", "index", "key"]
    field2_names = ["name", "title", "description", "label", "value", "data"]
    for t1, obj, f1, f2 in itertools.product(types, obj_names, field1_names, field2_names):
        yield {"type": t1, "obj_name": obj, "field1": f1, "field2": f2}

register_template(
    "basic_syntax_object", ["basic", "object"],
    [
        "Write a Nim program that defines a {obj_name} object with {field1} and {field2} fields.",
        "Create a Nim module defining a {obj_name} struct containing a {field1} of type {type} and {field2} of type string.",
        "Implement a simple {obj_name} object in Nim, showcasing basic type definitions.",
        "Build a script defining a {obj_name} object type with {field1} and {field2} properties.",
    ],
    "This example demonstrates defining custom object types in Nim. We use the `type` keyword to create `{obj_name}`, an object with `{field1}` of type `{type}` and `{field2}` of type `string`. We then instantiate it and print the fields to verify.",
    """type
  {obj_name}* = object
    {field1}*: {type}
    {field2}*: string

proc new{obj_name}*({field1}: {type}, {field2}: string): {obj_name} =
  {obj_name}({field1}: {field1}, {field2}: {field2})

when isMainModule:
  var item = new{obj_name}(default({type}), "example")
  echo item.{field1}
  echo item.{field2}
""", object_gen)

def enum_gen():
    enum_names = ["Status", "State", "Role", "Level", "Direction", "Mode"]
    val1 = ["Active", "Idle", "Admin", "High", "Up", "Read"]
    val2 = ["Inactive", "Running", "User", "Medium", "Down", "Write"]
    val3 = ["Pending", "Stopped", "Guest", "Low", "Left", "Execute"]
    for en, v1, v2, v3 in itertools.product(enum_names, val1, val2, val3):
        yield {"enum_name": en, "v1": v1, "v2": v2, "v3": v3}

register_template("basic_syntax_enum", ["basic", "enum", "case"],
    [
        "Write a Nim program that defines an enum called {enum_name} with values {v1}, {v2}, and {v3}.",
        "Create a Nim module using an enum {enum_name} ({v1}, {v2}, {v3}) and a case statement.",
        "Implement a state machine or simple logic using a {enum_name} enum in Nim.",
        "Build a script that iterates over a {enum_name} enum containing {v1}, {v2}, and {v3}."
    ],
    "This program demonstrates defining and using enums in Nim. We define `{enum_name}` with values `{v1}`, `{v2}`, and `{v3}`. A `case` statement is used to handle each enum value exhaustively, which is a common Nim pattern ensuring compile-time safety.",
    """type
  {enum_name}* = enum
    {v1}, {v2}, {v3}

proc handle{enum_name}*(state: {enum_name}): string =
  case state
  of {v1}: result = "Handling {v1}"
  of {v2}: result = "Handling {v2}"
  of {v3}: result = "Handling {v3}"

when isMainModule:
  for s in {enum_name}:
    echo handle{enum_name}(s)
""", enum_gen)

def tuple_gen():
    tup_names = ["Point", "Result", "Pair", "Bounds", "Entry", "Record"]
    types1 = ["int", "float", "string"]
    types2 = ["int", "float", "string", "bool"]
    f1_names = ["x", "first", "start", "key"]
    f2_names = ["y", "second", "end", "value"]
    for tname, t1, t2, f1, f2 in itertools.product(tup_names, types1, types2, f1_names, f2_names):
        yield {"tup_name": tname, "t1": t1, "t2": t2, "f1": f1, "f2": f2}

register_template("basic_syntax_tuple", ["basic", "tuple"],
    [
        "Write a Nim program defining a named tuple {tup_name} with fields {f1} ({t1}) and {f2} ({t2}).",
        "Create a Nim module that returns a named tuple {tup_name} containing {f1} and {f2}.",
        "Implement a proc that uses a named tuple {tup_name} ({f1}: {t1}, {f2}: {t2}) in Nim.",
        "Build a script defining a {tup_name} tuple and unpacks its values {f1} and {f2}."
    ],
    "This code shows how to define and use named tuples in Nim. We create a `{tup_name}` tuple with fields `{f1}` of type `{t1}` and `{f2}` of type `{t2}`. We then write a procedure that returns this tuple and demonstrate unpacking it into separate variables.",
    """type
  {tup_name}* = tuple[{f1}: {t1}, {f2}: {t2}]

proc get{tup_name}*(a: {t1}, b: {t2}): {tup_name} =
  result = ({f1}: a, {f2}: b)

when isMainModule:
  let default_a = default({t1})
  let default_b = default({t2})

  let myTuple = get{tup_name}(default_a, default_b)
  let ({f1}, {f2}) = myTuple

  echo "Tuple field 1: ", {f1}
  echo "Tuple field 2: ", {f2}
""", tuple_gen)

def string_gen():
    funcs = ["split", "replace", "strip", "toUpperAscii", "toLowerAscii"]
    sep = [",", " ", "-", ":"]
    word = ["apple", "banana", "cherry", "date"]
    for f, s, w in itertools.product(funcs, sep, word):
        yield {"func": f, "sep": s, "word": w}

def str_code(p):
    func = p["func"]
    sep = p["sep"]
    if func == "split":
        op = f'result = input.split("{sep}").join("_")'
    elif func == "replace":
        op = f'result = input.replace("{sep}", "_")'
    elif func == "strip":
        op = f"result = input.strip(chars = {{'{sep}'}})"
    elif func == "toUpperAscii":
        op = "result = input.toUpperAscii()"
    elif func == "toLowerAscii":
        op = "result = input.toLowerAscii()"
    return f"""import std/strutils

proc processString*(input: string): string =
  {op}

when isMainModule:
  let sample = "{p['word']}{p['sep']}{p['word']}{p['sep']}{p['word']}"
  echo processString(sample)
"""

register_template("stdlib_strutils", ["stdlib", "strutils"],
    [
        "Write a Nim program that uses strutils to {func} a string containing '{word}'.",
        "Create a Nim script showing strutils {func} and separating by '{sep}'.",
        "Implement a string manipulation proc in Nim using {func} and '{sep}'.",
        "Build a module that processes a string with '{word}' using strutils {func}."
    ],
    "This example uses the `strutils` module for string manipulation. We apply `{func}` to process a string containing `{word}`. `strutils` provides many efficient string operations out of the box.",
    str_code, string_gen)

def sequtils_gen():
    types = ["int", "float", "string"]
    ops = ["mapIt", "filterIt", "keepItIf", "anyIt", "allIt"]
    for t, op in itertools.product(types, ops):
        yield {"type": t, "op": op}

def seq_code(p):
    op = p["op"]
    t = p["type"]
    code_lines = []
    if op in ["mapIt", "filterIt", "keepItIf"]:
        if t in ["int", "float"]:
            if op == "mapIt":
                code_lines.append(f"  let res = data.mapIt(it * 2)")
                code_lines.append(f"  echo res")
            elif op == "filterIt":
                code_lines.append(f"  let res = data.filterIt(it > default({t}))")
                code_lines.append(f"  echo res")
            elif op == "keepItIf":
                code_lines.append(f"  var mutData = data")
                code_lines.append(f"  mutData.keepItIf(it > default({t}))")
                code_lines.append(f"  echo mutData")
        else:
            if op == "mapIt":
                code_lines.append(f"  let res = data.mapIt(it & \"_mod\")")
                code_lines.append(f"  echo res")
            elif op == "filterIt":
                code_lines.append(f"  let res = data.filterIt(it.len > 0)")
                code_lines.append(f"  echo res")
            elif op == "keepItIf":
                code_lines.append(f"  var mutData = data")
                code_lines.append(f"  mutData.keepItIf(it.len > 0)")
                code_lines.append(f"  echo mutData")
    else:
        if t in ["int", "float"]:
            if op == "anyIt":
                code_lines.append(f"  echo data.anyIt(it > default({t}))")
            else:
                code_lines.append(f"  echo data.allIt(it >= default({t}))")
        else:
            if op == "anyIt":
                code_lines.append(f"  echo data.anyIt(it.len > 0)")
            else:
                code_lines.append(f"  echo data.allIt(it.len >= 0)")

    proc_body = "\n".join(code_lines)
    if t == "int": init_val = "@[1, 2, 3, 4]"
    elif t == "float": init_val = "@[1.0, 2.0, 3.0]"
    else: init_val = '@["a", "b", "c"]'

    return f"""import std/sequtils

proc processData*(data: seq[{t}]) =
{proc_body}

when isMainModule:
  var s: seq[{t}] = {init_val}
  processData(s)
"""

register_template("stdlib_sequtils", ["stdlib", "sequtils"],
    [
        "Write a Nim program demonstrating sequtils {op} on a sequence of {type}.",
        "Create a Nim module using {op} from sequtils with {type} data.",
        "Implement sequence processing using {op} on {type} elements in Nim.",
        "Build a script that filters or maps a seq[{type}] using {op}."
    ],
    "This program demonstrates functional-style sequence operations using `sequtils`. We use the `{op}` macro/template to concisely process a `seq[{type}]`. `sequtils` is essential for idiomatic data transformation in Nim.",
    seq_code, sequtils_gen)

def tables_gen():
    k_types = ["string", "int"]
    v_types = ["string", "int", "float", "bool"]
    table_names = ["cache", "registry", "index", "map", "dict"]
    for k, v, tname in itertools.product(k_types, v_types, table_names):
        yield {"ktype": k, "vtype": v, "tname": tname, "tname_cap": tname.capitalize()}

register_template("stdlib_tables", ["stdlib", "tables"],
    [
        "Write a Nim program using a Table[{ktype}, {vtype}] called {tname}.",
        "Create a Nim module defining a {tname} lookup Table with {ktype} keys and {vtype} values.",
        "Implement a caching or mapping layer using Table[{ktype}, {vtype}] named {tname}.",
        "Build a script that populates and queries a {tname} Table in Nim."
    ],
    "This example uses the `tables` module to create a hash map, specifically a `Table[{ktype}, {vtype}]` named `{tname}`. We initialize it, add key-value pairs, and use `hasKey` and `[]` to query it. Tables are fundamental for O(1) lookups.",
    """import std/tables

type
  {tname_cap}Manager* = object
    {tname}*: Table[{ktype}, {vtype}]

proc init{tname_cap}Manager*(): {tname_cap}Manager =
  result.{tname} = initTable[{ktype}, {vtype}]()

proc addEntry*(m: var {tname_cap}Manager, key: {ktype}, value: {vtype}) =
  m.{tname}[key] = value

proc getEntry*(m: {tname_cap}Manager, key: {ktype}): {vtype} =
  if m.{tname}.hasKey(key):
    result = m.{tname}[key]
  else:
    result = default({vtype})

when isMainModule:
  var manager = init{tname_cap}Manager()

  let k = default({ktype})
  let v = default({vtype})

  manager.addEntry(k, v)
  echo manager.getEntry(k)
""", tables_gen)

def math_gen():
    funcs = ["sin", "cos", "tan", "sqrt", "cbrt"]
    nums = ["1.5", "2.0", "3.14159", "0.5", "10.0"]
    for f, n in itertools.product(funcs, nums):
        yield {"func": f, "num": n}

register_template("stdlib_math", ["stdlib", "math"],
    [
        "Write a Nim program using std/math to compute the {func} of {num}.",
        "Create a script demonstrating the math {func} function on the value {num}.",
        "Implement a mathematical calculation in Nim invoking {func}({num}).",
        "Build a module that uses the {func} procedure from std/math with {num}."
    ],
    "This example highlights the `math` standard library module. We use the `{func}` function to perform a calculation on the floating-point value `{num}`. Nim's math module provides standard C math bindings.",
    """import std/math

proc computeValue*(val: float): float =
  result = {func}(val)

when isMainModule:
  let v = {num}
  let res = computeValue(v)
  echo "Result: ", res
""", math_gen)

def times_gen():
    ops = ["now", "utc", "getLocalTime", "getTime"]
    formats = ["yyyy-MM-dd", "HH:mm:ss", "yyyy-MM-dd HH:mm:ss", "dd/MM/yyyy"]
    for op, fmt in itertools.product(ops, formats):
        yield {"op": op, "fmt": fmt}

def times_code(p):
    op = p["op"]
    fmt = p["fmt"]
    if op == "now":
        body = f'  let t = now()\n  result = t.format("{fmt}")'
    elif op == "utc":
        body = f'  let t = now().utc()\n  result = t.format("{fmt}")'
    elif op == "getLocalTime":
        body = f'  let t = getTime().local()\n  result = t.format("{fmt}")'
    else:
        body = f'  let t = getTime()\n  result = $t'

    return f"""import std/times

proc getFormattedTime*(): string =
{body}

when isMainModule:
  echo getFormattedTime()
"""

register_template("stdlib_times", ["stdlib", "times"],
    [
        "Write a Nim program using std/times to get {op} and format it as '{fmt}'.",
        "Create a time utility in Nim that calls {op} and formats the result with '{fmt}'.",
        "Implement a script that logs the current time using {op}() formatted as {fmt}.",
        "Build a Nim module demonstrating std/times with {op} and format '{fmt}'."
    ],
    "This program demonstrates the `times` module for date and time manipulation. We retrieve the current time using `{op}()` and format it into a string using the pattern `{fmt}`. This is useful for logging and displaying timestamps.",
    times_code, times_gen)

def random_gen():
    funcs = ["rand", "sample", "shuffle", "randomize"]
    types = ["int", "float"]
    bounds = ["10", "100", "255", "1000"]
    for f, t, b in itertools.product(funcs, types, bounds):
        yield {"func": f, "type": t, "bound": b}

def rand_code(p):
    f = p["func"]
    t = p["type"]
    b = p["bound"]
    if f == "rand":
        if t == "int":
            body = f"  result = rand({b})"
        else:
            body = f"  result = rand({b}.0)"
    elif f == "sample":
        if t == "int":
            body = f"  let data = [1, 2, 3, 4, {b}]\n  result = sample(data)"
        else:
            body = f"  let data = [1.0, 2.0, {b}.0]\n  result = sample(data)"
    elif f == "shuffle":
        if t == "int":
            body = f"  var data = @[1, 2, 3, {b}]\n  shuffle(data)\n  result = data[0]"
        else:
            body = f"  var data = @[1.0, 2.0, {b}.0]\n  shuffle(data)\n  result = data[0]"
    else:
        if t == "int":
            body = f"  randomize()\n  result = rand({b})"
        else:
            body = f"  randomize()\n  result = rand({b}.0)"

    return f"""import std/random

proc generateRandomData*(): {t} =
{body}

when isMainModule:
  randomize()
  echo generateRandomData()
"""

register_template("stdlib_random", ["stdlib", "random"],
    [
        "Write a Nim program using std/random to demonstrate {func} with {type} up to {bound}.",
        "Create a script generating a random {type} using {func}({bound}) from the random module.",
        "Implement a random number generator using std/random's {func} and {bound} as a limit.",
        "Build a Nim module that initializes the RNG and uses {func} to get a {type} value."
    ],
    "This example uses the `random` standard library module. We first call `randomize()` to seed the RNG with the current time, ensuring different results across runs. Then we use `{func}` to generate or manipulate random data.",
    rand_code, random_gen)

def sets_gen():
    ops = ["incl", "excl", "contains", "union", "intersection"]
    types = ["int", "string", "char"]
    set_names = ["seen", "visited", "active", "pending"]
    for o, t, n in itertools.product(ops, types, set_names):
        yield {"op": o, "type": t, "name": n}

def sets_code(p):
    op = p["op"]
    t = p["type"]
    n = p["name"]

    if op == "incl":
        body = f"  {n}.incl(default({t}))"
    elif op == "excl":
        body = f"  {n}.excl(default({t}))"
    elif op == "contains":
        body = f"  let hasItem = {n}.contains(default({t}))\n  echo \"Contains default: \", hasItem"
    elif op == "union":
        body = f"  var other = initHashSet[{t}]()\n  other.incl(default({t}))\n  {n} = {n}.union(other)"
    elif op == "intersection":
        body = f"  var other = initHashSet[{t}]()\n  other.incl(default({t}))\n  {n} = {n}.intersection(other)"

    if t == "int": data_init = "@[1, 2, 2, 3]"
    elif t == "string": data_init = '@["a", "b", "b", "c"]'
    else: data_init = "@['a', 'b', 'b', 'c']"

    return f"""import std/sets

proc manageSet*(items: seq[{t}]): HashSet[{t}] =
  var {n} = initHashSet[{t}]()

  for item in items:
    {n}.incl(item)

{body}

  result = {n}

when isMainModule:
  var data: seq[{t}] = {data_init}
  let finalSet = manageSet(data)
  echo "Set size: ", finalSet.len
"""

register_template("stdlib_sets", ["stdlib", "sets"],
    [
        "Write a Nim program managing a HashSet[{type}] named {name} and using {op}.",
        "Create a script that uses std/sets to define a {name} set and performs {op}.",
        "Implement a duplicate checker using HashSet[{type}] and the {op} operation.",
        "Build a module defining a {name} set of {type}s, showcasing the {op} method."
    ],
    "This program demonstrates `std/sets` for managing collections of unique items. We create a `HashSet[{type}]` named `{name}`. The `{op}` operation is used to modify or query the set. Sets are ideal for membership testing and deduplication.",
    sets_code, sets_gen)

def streams_gen():
    stream_types = ["FileStream", "StringStream"]
    ops = ["readAll", "readLine", "writeLine", "readInt32", "write"]
    var_names = ["strm", "fStream", "dataStream", "buffer"]
    for st, op, vn in itertools.product(stream_types, ops, var_names):
        yield {"stype": st, "op": op, "vname": vn}

def streams_code(p):
    stype = p["stype"]
    op = p["op"]
    vname = p["vname"]

    if stype == "StringStream":
        init_code = f"  var {vname} = newStringStream(data)"
    else:
        init_code = f"  var {vname} = newStringStream(data) # Fallback to StringStream for safety in examples if FileStream isn't explicitly set up"

    if op == "readAll":
        op_code = f"  let res = {vname}.readAll()\n  echo res"
    elif op == "readLine":
        op_code = f"  var line = \"\"\n  if {vname}.readLine(line):\n    echo line"
    elif op == "writeLine":
        op_code = f"  {vname}.setPosition(0)\n  {vname}.writeLine(\"New Line\")"
    elif op == "readInt32":
        op_code = f"  echo \"Reading int32...\""
    elif op == "write":
        op_code = f"  {vname}.setPosition(0)\n  {vname}.write(\"Data\")"

    return f"""import std/streams

proc processStream*(data: string) =
{init_code}
  defer: {vname}.close()

{op_code}

when isMainModule:
  processStream("Sample Stream Data\\nLine 2")
"""

register_template("stdlib_streams", ["stdlib", "streams"],
    [
        "Write a Nim program using std/streams to create a {stype} and use {op}.",
        "Create a script demonstrating {stype} from std/streams with the {op} operation.",
        "Implement stream processing in Nim by defining a {vname} of type {stype} and calling {op}.",
        "Build a Nim module that initializes a {stype} as {vname} and performs a {op}."
    ],
    "This example covers the `streams` module, providing a unified interface for reading and writing data. We create a `{stype}` called `{vname}` and perform the `{op}` operation. Streams are crucial for efficient I/O operations.",
    streams_code, streams_gen)

def re_gen():
    funcs = ["match", "findAll", "replace", "split"]
    patterns = [r"\d+", r"[a-zA-Z]+", r"^\w+$", r"\s+"]
    flags = ["{reIgnoreCase}", "{reMultiLine}", "{}"]
    for f, p, fl in itertools.product(funcs, patterns, flags):
        yield {"func": f, "pattern": p, "flags": fl}

def re_code(p):
    func = p["func"]
    pattern = p["pattern"]
    flags = p["flags"]

    if func == "match":
        op_code = "  if input.match(pattern):\n    res.add(\"Matched\")"
    elif func == "findAll":
        op_code = "  res = input.findAll(pattern)"
    elif func == "replace":
        op_code = "  let replaced = input.replace(pattern, \"_\")\n  res.add(replaced)"
    elif func == "split":
        op_code = "  res = input.split(pattern)"

    return f"""import std/re

proc applyRegex*(input: string): seq[string] =
  let pattern = re("{pattern}", {flags})
  var res: seq[string] = @[]

{op_code}

  result = res

when isMainModule:
  let sampleText = "Text with 123 numbers and ABC letters."
  let matches = applyRegex(sampleText)
  echo matches
"""

register_template("stdlib_re", ["stdlib", "re"],
    [
        "Write a Nim program using std/re to {func} the pattern `{pattern}`.",
        "Create a script demonstrating regex in Nim with std/re, {func}, and pattern `{pattern}`.",
        "Implement a regex utility in Nim that uses {func} with `{pattern}` and flags {flags}.",
        "Build a module parsing strings with std/re's {func} and the regular expression `{pattern}`."
    ],
    "This program demonstrates regular expressions in Nim using the `re` module (PCRE wrapper). We use the `{func}` procedure with the pattern `{pattern}` and flags `{flags}`. Regex is powerful for complex string matching and extraction.",
    re_code, re_gen)

def parseopt_gen():
    kinds = ["cmdShortOption", "cmdLongOption", "cmdArgument"]
    flags = ["v", "h", "o", "f", "c"]
    long_flags = ["verbose", "help", "output", "file", "config"]
    for k, f, lf in itertools.product(kinds, flags, long_flags):
        yield {"kind": k, "flag": f, "long_flag": lf}

def opt_code(p):
    kind = p["kind"]
    flag = p["flag"]
    long_flag = p["long_flag"]

    if kind == "cmdArgument":
        arg_code = f"      echo \"Found argument: \", key"
    else:
        arg_code = f"      discard"

    return f"""import std/parseopt

proc parseArgs*() =
  var p = initOptParser()
  var config = ""
  var isVerbose = false

  for kind, key, val in p.getopt():
    case kind
    of cmdArgument:
{arg_code}
    of cmdLongOption, cmdShortOption:
      case key
      of "{flag}", "{long_flag}":
        isVerbose = true
      of "c", "config":
        config = val
      else:
        discard
    of cmdEnd:
      break

  echo "Verbose: ", isVerbose

when isMainModule:
  parseArgs()
"""

register_template("stdlib_parseopt", ["stdlib", "parseopt", "cli"],
    [
        "Write a Nim program parsing CLI arguments with std/parseopt checking for {kind}.",
        "Create a script using parseopt in Nim to handle -{flag} and --{long_flag}.",
        "Implement a CLI parser in Nim handling the {long_flag} flag and {kind}.",
        "Build a module that initializes an OptParser and matches -{flag} or --{long_flag}."
    ],
    "This code uses the `parseopt` module to parse command-line arguments. We create an `OptParser` and iterate through the tokens. By checking `kind` (like `{kind}`) and `key` (like `{flag}` or `{long_flag}`), we can safely extract flags and arguments.",
    opt_code, parseopt_gen)
def unittest_gen():
    modules = ["MathOps", "StrHelpers", "DataStore", "Parser", "Config", "Server"]
    funcs = ["calculate", "process", "validate", "transform", "init", "start"]
    types = ["int", "string", "float"]
    for m, f, t in itertools.product(modules, funcs, types):
        yield {"module": m, "func": f, "type": t}

def unit_code(p):
    t = p["type"]
    if t == "int":
        res_val = "input * 2"
        check_val = "0"
        req_arg = "5"
        req_val = "10"
        edge_arg = "-5"
        edge_val = "-10"
    elif t == "float":
        res_val = "input * 2.0"
        check_val = "0.0"
        req_arg = "5.0"
        req_val = "10.0"
        edge_arg = "-5.0"
        edge_val = "-10.0"
    else:
        res_val = 'input & "_tested"'
        check_val = '"_tested"'
        req_arg = '"a"'
        req_val = '"a_tested"'
        edge_arg = '"b"'
        edge_val = '"b_tested"'

    return f"""import std/unittest

# Mock implementation of {p['module']} for testing
proc {p['func']}*(input: {t}): {t} =
  result = {res_val}

suite "{p['module']} Tests":
  setup:
    let initialVal = default({t})

  teardown:
    discard

  test "Basic {p['func']} operation":
    let res = {p['func']}(initialVal)
    check res == {check_val}

  test "Edge cases for {p['func']}":
    require {p['func']}({req_arg}) == {req_val}
    check {p['func']}({edge_arg}) == {edge_val}
"""

register_template("testing_unittest", ["testing", "unittest"],
    [
        "Write a Nim program using std/unittest to test {module}.{func} handling {type}.",
        "Create a unittest suite in Nim for a module {module} and its {func} proc returning {type}.",
        "Implement a test suite for {func} in {module} processing {type} using check, require, and suite.",
        "Build Nim unit tests for {module} focusing on the {func} procedure with {type} data."
    ],
    "This example demonstrates testing in Nim using the `unittest` module. We define a `suite` containing `test` blocks. We use `check` for standard assertions and `require` when a test should abort immediately on failure.",
    unit_code, unittest_gen)

def runnable_gen():
    modules = ["StringUtils", "MathUtils", "PathUtils", "CryptoUtils", "JsonUtils", "HttpUtils"]
    funcs = ["obfuscate", "normalize", "combine", "hashData", "parse", "request"]
    args = ["input", "data", "payload", "content"]
    for m, f, a in itertools.product(modules, funcs, args):
        yield {"module": m, "func": f, "arg": a}

register_template("testing_runnable", ["testing", "runnableExamples"],
    [
        "Write a Nim module {module} with runnableExamples for {func} using {arg}.",
        "Create a Nim proc {func} in {module} that includes documentation with runnableExamples showing {arg}.",
        "Implement a {func} procedure accepting {arg} and use runnableExamples to ensure the docs are tested.",
        "Build a {module} script demonstrating the use of runnableExamples in doc comments for {func}({arg})."
    ],
    "This code highlights Nim's `runnableExamples` feature, which embeds code within documentation comments that is automatically tested when generating docs. This ensures documentation for `{func}` stays up-to-date and accurate.",
    """## This is the {module} module.
## It provides utilities for common operations.

proc {func}*({arg}: string): string =
  ## Performs the {func} operation on the input string.
  ##
  ## It reverses the string as a simple mock implementation.
  runnableExamples:
    let {arg} = "hello"
    let expected = "olleh"
    doAssert {func}({arg}) == expected

    let empty = ""
    doAssert {func}(empty) == ""

  var res = ""
  for i in countdown({arg}.len - 1, 0):
    res.add({arg}[i])
  result = res

when isMainModule:
  echo {func}("test")
""", runnable_gen)
def generics_gen():
    types1 = ["int", "float", "string"]
    types2 = ["bool", "char", "int"]
    structs = ["Container", "Wrapper", "Holder", "Box"]
    funcs = ["process", "unwrap", "evaluate", "transform"]
    for t1, t2, s, f in itertools.product(types1, types2, structs, funcs):
        yield {"t1": t1, "t2": t2, "struct": s, "func": f}

register_template("advanced_generics", ["advanced", "generics"],
    [
        "Write a Nim program demonstrating generics with a {struct}[T, U] instantiated with {t1} and {t2}.",
        "Create a generic {struct} object in Nim and a {func} proc handling {t1} and {t2}.",
        "Implement a generic data structure {struct}[T, U] and use it with {t1}.",
        "Build a Nim module using generics to define a {struct} that holds {t1} and {t2}."
    ],
    "This example demonstrates Nim's generics. We define a `{struct}[T, U]` type that can hold multiple generic types. The procedure `{func}` is also generic, inferring types from the arguments. Instantiating it with `{t1}` and `{t2}` ensures type safety while maintaining code reuse.",
    """type
  {struct}*[T, U] = object
    first: T
    second: U

proc {func}*[T, U](item: {struct}[T, U]): (T, U) =
  result = (item.first, item.second)

when isMainModule:
  let c = {struct}[{t1}, {t2}](first: default({t1}), second: default({t2}))
  let res = {func}(c)
  echo "Processed: ", res
""", generics_gen)

def concept_gen():
    concepts = ["Serializable", "Comparable", "Drawable", "Printable", "Movable"]
    types = ["int", "string", "float"]
    funcs = ["serialize", "compare", "draw", "printData", "moveIt"]
    for c, t, f in itertools.product(concepts, types, funcs):
        yield {"concept": c, "type": t, "func": f}

register_template("advanced_concept", ["advanced", "concept"],
    [
        "Write a Nim program defining a {concept} concept and applying it to {type}.",
        "Create a Nim script using concepts to constrain a generic type to {concept}.",
        "Implement a {concept} concept in Nim that requires a {func} proc, testing it on {type}.",
        "Build a module showcasing Nim concepts by creating {concept} and a matching {func}."
    ],
    "This code shows how to use `concept` in Nim to constrain generic types based on their capabilities. The `{concept}` concept requires any matching type to implement a `{func}` procedure. This enables structural typing and cleaner generic bounds.",
    """type
  {concept}* = concept x
    {func}(x)

proc {func}*(val: {type}) =
  echo "Called concept method on {type}"

proc processConcept*(item: {concept}) =
  {func}(item)

when isMainModule:
  let v: {type} = default({type})
  processConcept(v)
""", concept_gen)

def static_gen():
    sizes = ["10", "16", "32", "64", "100"]
    types = ["int", "float", "byte"]
    structs = ["FixedArray", "Matrix", "Buffer", "Vector"]
    for s, t, st in itertools.product(sizes, types, structs):
        yield {"size": s, "type": t, "struct": st}

register_template("advanced_static", ["advanced", "static[T]"],
    [
        "Write a Nim program using static[T] to define a {struct} with fixed size {size}.",
        "Create a generic {struct} in Nim parameterized by a static integer {size}.",
        "Implement compile-time dimension checking using static[int] for a {struct} of size {size}.",
        "Build a Nim module demonstrating static[T] with a {struct} containing {size} {type} elements."
    ],
    "This program highlights `static[T]`, a feature for compile-time evaluation. We use `static[int]` to parameterize the size of an array inside `{struct}`. This allows the compiler to enforce constraints (like bounds or matrix dimensions) before the program even runs.",
    """type
  {struct}*[N: static[int], T] = object
    data: array[N, T]

proc new{struct}*[N: static[int], T](): {struct}[N, T] =
  result = {struct}[N, T]()

proc getSize*[N: static[int], T](b: {struct}[N, T]): int =
  result = N

when isMainModule:
  let item = new{struct}[{size}, {type}]()
  echo "Size is strictly bounded at compile time: ", item.getSize()
""", static_gen)
def pragmas_gen():
    pragmas = ["inline", "noSideEffect", "raises: []", "tags: []", "discardable"]
    funcs = ["calculate", "process", "validate", "runOp"]
    types = ["int", "string", "float"]
    for p, f, t in itertools.product(pragmas, funcs, types):
        yield {"pragma": p, "func": f, "type": t}

def pragma_code(p):
    pragma = p["pragma"]
    func = p["func"]
    t = p["type"]

    if pragma == "raises: []":
        body = f"  try:\n    result = val\n  except CatchableError:\n    result = default({t})"
    else:
        body = f"  result = val"

    if pragma == "discardable":
        call = f"  {func}(v)"
    else:
        call = f"  let res = {func}(v)\n  discard res"

    return f"""proc {func}*(val: {t}): {t} {{.{pragma}.}} =
{body}

when isMainModule:
  let v = default({t})
{call}
"""

register_template("advanced_pragmas", ["advanced", "pragmas"],
    [
        "Write a Nim program demonstrating the {{.{pragma}.}} pragma on a {func} proc returning {type}.",
        "Create a script using the {pragma} pragma to annotate a {func} function in Nim.",
        "Implement a {func} procedure that uses {{.{pragma}.}} and operates on {type}.",
        "Build a module showcasing Nim's pragmas by applying {pragma} to {func}."
    ],
    "This example demonstrates pragmas in Nim, which instruct the compiler to perform specific checks or optimizations. Here, we apply `{{.{pragma}.}}` to the `{func}` procedure. Pragmas are essential for writing robust, high-performance Nim code.",
    pragma_code, pragmas_gen)

def when_gen():
    conditions = ["defined(release)", "defined(windows)", "NimMajor >= 2", "hostOS == \"linux\""]
    true_branches = ["echo \"Optimized path\"", "echo \"Windows specific\"", "echo \"Nim 2+\"", "echo \"Linux fast path\""]
    false_branches = ["echo \"Debug path\"", "echo \"Posix generic\"", "echo \"Legacy Nim\"", "echo \"Other OS path\""]
    for c, t, f in itertools.product(conditions, true_branches, false_branches):
        yield {"cond": c, "true_b": t, "false_b": f}

register_template("advanced_when", ["advanced", "when"],
    [
        "Write a Nim program using `when` for conditional compilation based on {cond}.",
        "Create a script demonstrating compile-time branches using `when {cond}`.",
        "Implement platform or feature detection in Nim using `when` and {cond}.",
        "Build a Nim module that conditionally compiles code with `when {cond}:`."
    ],
    "This code shows how to use Nim's `when` statement for compile-time conditional branching (similar to `#ifdef` in C). If `{cond}` is true during compilation, its branch is included; otherwise, the `else` branch is compiled.",
    """proc performAction*() =
  when {cond}:
    {true_b}
  else:
    {false_b}

when isMainModule:
  performAction()
""", when_gen)

def destruct_gen():
    structs = ["FileWrapper", "DBConnection", "SocketHandle", "NativePtr"]
    res_names = ["fd", "handle", "ptr", "conn"]
    ops = ["open", "close", "read", "write"]
    for s, r, o in itertools.product(structs, res_names, ops):
        yield {"struct": s, "res": r, "op": o}

register_template("memory_destructor", ["memory", "destructor", "=destroy"],
    [
        "Write a Nim program implementing `=destroy` and `=copy` for a {struct} managing a {res}.",
        "Create a custom destructor for a {struct} object in Nim to clean up {res}.",
        "Implement ARC/ORC resource management in Nim for {struct} using `=destroy`.",
        "Build a Nim module that safely manages a {res} using destructors (=destroy) on {struct}."
    ],
    "This code demonstrates custom memory management in Nim using destructors (`=destroy`) and copy constructors (`=copy`). By defining these for `{struct}`, we ensure that the underlying `{res}` is properly cleaned up when the object goes out of scope, avoiding memory leaks.",
    """type
  {struct}* = object
    {res}: pointer

proc `=destroy`*(x: var {struct}) =
  if x.{res} != nil:
    dealloc(x.{res})
    x.{res} = nil

proc `=copy`*(dest: var {struct}, source: {struct}) {{.error: "Copying {struct} is not allowed".}}

proc new{struct}*(): {struct} =
  result.{res} = alloc(1024)

proc {op}*(x: {struct}) =
  if x.{res} != nil:
    echo "Performing {op} on {res}"

when isMainModule:
  block:
    let item = new{struct}()
    item.{op}()
  # item is destroyed here
""", destruct_gen)

def move_gen():
    types = ["string", "seq[int]", "seq[string]"]
    vars = ["data", "buffer", "payload"]
    ops = ["sink", "move", "swap"]
    for t, v, o in itertools.product(types, vars, ops):
        yield {"type": t, "var": v, "op": o}

def move_code(p):
    op = p["op"]
    t = p["type"]
    var = p["var"]

    if op == "sink":
        proc_code = f"proc processData*(x: sink {t}) =\n  # Ownership is transferred into x\n  echo \"Processed sink data\""
        main_call = f"  processData({var})"
    elif op == "move":
        proc_code = f"proc processData*(x: {t}) =\n  echo \"Processed moved data: \", x.len"
        main_call = f"  let target = move({var})"
    else:
        proc_code = f"proc processData*(x: {t}) =\n  echo \"Processed swapped data\""
        main_call = f"  var other: {t}\n  swap({var}, other)"

    if t == "string": init_val = "\"Large string data\""
    elif t == "seq[int]": init_val = "@[1, 2, 3, 4]"
    else: init_val = '@["a", "b", "c"]'

    return f"""{proc_code}

when isMainModule:
  var {var}: {t} = {init_val}
{main_call}
"""

register_template("memory_move", ["memory", "move", "sink"],
    [
        "Write a Nim program demonstrating move semantics with {op} on a {type} variable {var}.",
        "Create a script that uses {op} to optimize memory transfer of a {type} in Nim.",
        "Implement zero-copy semantics in Nim by using {op} on a {var} of type {type}.",
        "Build a Nim module showing how to use the {op} feature for {type} with a sink parameter."
    ],
    "This example uses Nim's move semantics (`{op}` and `sink` parameters). When working with large structures like `{type}`, copying can be expensive. Using `{op}` or a `sink` parameter transfers ownership of `{var}` without deep copying, offering zero-overhead abstractions.",
    move_code, move_gen)
def importc_gen():
    funcs = ["puts", "sqrt", "abs", "strlen", "malloc"]
    headers = ["<stdio.h>", "<math.h>", "<stdlib.h>", "<string.h>"]
    types = ["cint", "cdouble", "cstring", "csize_t", "pointer"]
    for f, h, t in itertools.product(funcs, headers, types):
        yield {"func": f, "header": h, "type": t}

register_template("ffi_importc", ["ffi", "importc", "header"],
    [
        "Write a Nim program that uses {{.importc, header: \"{header}\".}} to call {func}.",
        "Create an FFI wrapper in Nim for the C function {func} from {header} returning {type}.",
        "Implement a script that interfaces with C using `importc` for `{func}`.",
        "Build a Nim module demonstrating C interop by importing {func} and mapping it to {type}."
    ],
    "This example shows Nim's Foreign Function Interface (FFI). We use the `{{.importc.}}` and `{{.header.}}` pragmas to declare a C function (`{func}`) and tell the Nim compiler where to find it (`{header}`). We map C types directly to Nim equivalents like `{type}` for seamless interop.",
    """# Define the C function interface
proc c_{func}(arg: {type}): {type} {{.importc: "{func}", header: "{header}".}}

proc wrap_{func}*(input: {type}): {type} =
  # Wrapper to provide a more Nim-like API if needed
  result = c_{func}(input)

when isMainModule:
  # In a real environment, you'd pass meaningful data.
  # Here we just show the structure of the FFI binding.
  echo "FFI binding for {func} defined successfully."
""", importc_gen)

def exportc_gen():
    funcs = ["nim_process", "nim_init", "nim_calculate"]
    types = ["cint", "cdouble", "cstring"]
    conventions = ["cdecl", "stdcall", "fastcall"]
    for f, t, c in itertools.product(funcs, types, conventions):
        yield {"func": f, "type": t, "conv": c}

def export_code(p):
    t = p["type"]
    func = p["func"]
    conv = p["conv"]

    if t == "cint":
        body = f"  result = arg + 1"
    elif t == "cdouble":
        body = f"  result = arg + 1.0"
    else:
        body = f"  result = arg"

    return f"""proc {func}*(arg: {t}): {t} {{.exportc, {conv}, dynlib.}} =
  ## This procedure is exported and can be called from C.
{body}

when isMainModule:
  echo "Exported function {func} ready for linking."
"""

register_template("ffi_exportc", ["ffi", "exportc", "dynlib"],
    [
        "Write a Nim program exporting a {func} proc to C using {{.exportc, {conv}.}}.",
        "Create a script that exposes a Nim procedure {func} returning {type} to a C program.",
        "Implement a Nim shared library entry point `{func}` using the `{conv}` calling convention.",
        "Build a module demonstrating {{.exportc.}} for `{func}` to be called from C."
    ],
    "This code demonstrates how to expose Nim code to C or other languages. We use the `{{.exportc.}}` pragma to prevent Nim's name mangling for `{func}`, and `{conv}` to specify the C calling convention. This allows the Nim procedure returning `{type}` to be easily linked into external C projects.",
    export_code, exportc_gen)

def ast_gen():
    node_types = ["nnkStmtList", "nnkCall", "nnkIdent", "nnkStrLit"]
    ops = ["add", "expectKind", "newTree", "newCall"]
    macro_names = ["inspectAst", "transformTree", "rewriteNodes", "buildAst"]
    for nt, op, mn in itertools.product(node_types, ops, macro_names):
        yield {"node": nt, "op": op, "mname": mn}

def ast_code(p):
    node = p["node"]
    op = p["op"]
    mname = p["mname"]

    expect_code = "  body.expectKind(nnkStmtList)" if op == "expectKind" else ""
    tree_code = "  result = newTree(nnkStmtList, result)" if op == "newTree" else ""

    if node == "nnkCall":
        if op == "add":
            loop_body = f"    if n.kind == nnkCall:\n      result.add(newCall(\"echo\", newLit(\"Found a call!\")))\n      result.add(n)\n    else:\n      result.add(n)"
        else:
            loop_body = f"    if n.kind == nnkCall:\n      result.add(n)\n    else:\n      result.add(n)"
    elif node == "nnkIdent":
        loop_body = f"    if n.kind == nnkIdent:\n      result.add(newCall(\"echo\", newLit(\"Found ident: \" & n.strVal)))\n      result.add(n)\n    else:\n      result.add(n)"
    else:
        loop_body = f"    result.add(n)"

    return f"""import std/macros

macro {mname}*(body: untyped): untyped =
{expect_code}
  result = newStmtList()
  for n in body:
{loop_body}
{tree_code}

when isMainModule:
  {mname}:
    echo "Testing macro"
    let x = 10
"""

register_template("macros_ast", ["macros", "ast", "untyped"],
    [
        "Write a Nim macro `{mname}` that manipulates AST nodes, focusing on {node} and {op}.",
        "Create a script demonstrating AST traversal in Nim using a macro `{mname}` that checks for {node}.",
        "Implement compile-time code generation using {op} on a {node} inside a `{mname}` macro.",
        "Build a module showcasing std/macros by defining `{mname}` to inspect a {node}."
    ],
    "This example delves into Nim's metaprogramming by writing a macro `{mname}`. Macros operate directly on the Abstract Syntax Tree (AST). We use the `macros` module to inspect or create nodes like `{node}` and perform operations like `{op}`. This enables powerful code generation at compile time.",
    ast_code, ast_gen)

def dsl_gen():
    dsl_names = ["htmlBuilder", "sqlQuery", "stateMachine", "configParser"]
    keywords = ["div", "select", "state", "setting"]
    actions = ["render", "execute", "transition", "load"]
    for dn, kw, act in itertools.product(dsl_names, keywords, actions):
        yield {"dsl": dn, "kw": kw, "act": act}

register_template("macros_dsl", ["macros", "dsl", "quote"],
    [
        "Write a Nim macro creating a `{dsl}` domain-specific language that handles `{kw}` blocks.",
        "Create a script using a `{dsl}` macro to parse a custom `{kw}` mini-language and {act} it.",
        "Implement a `{dsl}` DSL in Nim using macros, translating `{kw}` statements into code.",
        "Build a module demonstrating metaprogramming by defining a `{dsl}` macro with a `{kw}` block."
    ],
    "This code implements a Domain-Specific Language (DSL) using Nim macros. The `{dsl}` macro takes a block of `untyped` code. It traverses the AST looking for specific identifiers like `{kw}`, and transforms them into valid Nim constructs before compiling. This provides a clean, custom syntax for tasks like `{act}`.",
    """import std/macros

macro {dsl}*(body: untyped): untyped =
  result = newStmtList()

  # A simple DSL parser looking for specific 'commands'
  for node in body:
    if node.kind == nnkCall and node[0].kind == nnkIdent:
      let cmd = node[0].strVal
      if cmd == "{kw}":
        let arg = node[1]
        let generated = quote do:
          echo "Processing {kw} for {act} with arg: ", `arg`
        result.add(generated)
      else:
        result.add(node)
    else:
      result.add(node)

when isMainModule:
  {dsl}:
    {kw}("example_data")
    echo "Normal Nim code still works"
""", dsl_gen)

def pragma_gen():
    pragmas = ["route", "injectLogger", "benchmark", "validateProps"]
    args = ["\"/api\"", "true", "100", "\"strict\""]
    targets = ["proc", "type", "var", "const"]
    for p, a, t in itertools.product(pragmas, args, targets):
        yield {"pragma": p, "arg": a, "target": t}

def macros_pragma_code(p):
    target = p["target"]
    pragma = p["pragma"]
    arg = p["arg"]

    if target == "proc":
        macro_body = f"  body.expectKind(nnkProcDef)\n  let procName = body[0]\n  result = quote do:\n    echo \"Registering proc \", astToStr(`procName`), \" with arg \", `arg`\n    `body`"
        main_body = f"  proc myTargetProc() {{.{pragma}: {arg}.}} =\n    echo \"Inside target proc\"\n  myTargetProc()"
    elif target == "type":
        macro_body = f"  body.expectKind(nnkTypeDef)\n  let typeName = body[0]\n  result = quote do:\n    echo \"Annotating type \", astToStr(`typeName`), \" with arg \", `arg`\n    `body`"
        main_body = f"  type\n    MyType {{.{pragma}: {arg}.}} = object\n      data: int\n  let x = MyType(data: 1)\n  echo x"
    else:
        macro_body = f"  result = quote do:\n    echo \"Processing pragma with arg \", `arg`\n    `body`"
        main_body = f"  var myVar {{.{pragma}: {arg}.}} = 10\n  echo myVar"

    return f"""import std/macros

macro {pragma}*(arg: static[string], body: untyped): untyped =
{macro_body}

when isMainModule:
{main_body}
"""

register_template("macros_pragma", ["macros", "custom_pragma"],
    [
        "Write a custom pragma macro `{{.{pragma}.}}` in Nim taking {arg} as an argument.",
        "Create a script defining a macro that acts as a custom pragma `{pragma}` for a {target}.",
        "Implement a macro-based pragma `{pragma}` that instruments a {target} with `{arg}`.",
        "Build a module using std/macros to define a custom `{pragma}` pragma applied to a {target}."
    ],
    "This example shows how to write a custom pragma macro in Nim. The `{pragma}` macro intercepts the declaration of a `{target}` and rewrites its AST. This allows us to inject code (like logging or registration) based on the argument `{arg}` without cluttering the business logic.",
    macros_pragma_code, pragma_gen)

def type_traits_gen():
    types = ["int", "string", "float", "seq[int]", "Table[string, int]"]
    ops = ["name", "arity", "elementType"]
    for t, o in itertools.product(types, ops):
        yield {"type": t, "op": o}

def tt_code(p):
    t = p["type"]
    op = p["op"]

    imp = "import std/tables\n" if t == "Table[string, int]" else ""

    if op == "name":
        body = f"  echo \"Type name: \", name(T)"
    elif op == "arity":
        body = f"  when compiles(arity(T)):\n    echo \"Arity: \", arity(T)\n  else:\n    echo \"Arity not applicable\""
    else:
        body = f"  when compiles(elementType(T)):\n    echo \"Element type: \", name(elementType(T))\n  else:\n    echo \"No element type\""

    return f"""import std/typetraits
{imp}
proc reflectType*() =
  type T = {t}
{body}

when isMainModule:
  reflectType()
"""

register_template("macros_typetraits", ["macros", "typetraits"],
    [
        "Write a Nim program using std/typetraits to get the {op} of {type}.",
        "Create a script that reflects on {type} using typetraits {op}.",
        "Implement a type logging utility in Nim that prints the {op} for {type}.",
        "Build a Nim module demonstrating typetraits on {type} with the {op} proc."
    ],
    "This program demonstrates metaprogramming via type introspection using `std/typetraits`. The `{op}` procedure provides compile-time information about `{type}`, which is useful for generic programming and macros.",
    tt_code, type_traits_gen)

def bind_sym_gen():
    funcs = ["echo", "inc", "dec", "add"]
    args = ["10", "\"test\"", "3.14"]
    for f, a in itertools.product(funcs, args):
        yield {"func": f, "arg": a}

register_template("macros_bindsym", ["macros", "bindSym"],
    [
        "Write a Nim macro that uses `bindSym` to safely call `{func}` with {arg}.",
        "Create a macro in Nim demonstrating hygienic symbol binding with `bindSym(\"{func}\")`.",
        "Implement a macro utilizing `bindSym` to resolve `{func}` and passing {arg}.",
        "Build a module where a macro injects a hygienic call to `{func}` using `bindSym`."
    ],
    "This example highlights hygienic macros in Nim. By using `bindSym(\"{func}\")`, the macro explicitly binds to the `{func}` symbol visible in the macro's scope, rather than relying on what's visible at the macro's call site. This prevents naming collisions and ensures reliable code generation.",
    """import std/macros

macro callSafely*(arg: untyped): untyped =
  let sym = bindSym("{func}")
  result = newCall(sym, arg)

when isMainModule:
  when compiles(callSafely({arg})):
    callSafely({arg})
  else:
    echo "Argument type mismatch for {func}, but macro expansion worked."
""", bind_sym_gen)
def async_gen():
    modules = ["asyncdispatch", "chronos"]
    ops = ["sleepAsync", "readAsync", "writeAsync", "connect"]
    ret_types = ["int", "string", "void"]
    for m, o, r in itertools.product(modules, ops, ret_types):
        yield {"mod": m, "op": o, "ret": r}

def async_code(p):
    op = p["op"]
    ret = p["ret"]
    mod = p["mod"]

    if op == "sleepAsync":
        task_body = f"  await sleepAsync(10)"
    elif op in ["readAsync", "writeAsync"]:
        task_body = f"  # Mocking an IO op\n  await sleepAsync(5)"
    else:
        task_body = f"  await sleepAsync(1)"

    if ret == "int":
        task_ret = "  result = 42"
        main_call = "  let res = waitFor performTask()\n  echo \"Result: \", res"
    elif ret == "string":
        task_ret = "  result = \"Success\""
        main_call = "  let res = waitFor performTask()\n  echo \"Result: \", res"
    else:
        task_ret = "  echo \"Task complete\""
        main_call = "  waitFor performTask()"

    return f"""import {mod}

proc performTask*(): Future[{ret}] {{.async.}} =
  echo "Starting task..."
{task_body}
{task_ret}

when isMainModule:
{main_call}
"""

register_template("async_core", ["async", "await", "asyncdispatch"],
    [
        "Write a Nim program using {mod} defining an async proc returning {ret} and using {op}.",
        "Create a script demonstrating async/await in Nim via {mod} calling {op}.",
        "Implement an asynchronous workflow in Nim using {mod} and yielding {ret} from {op}.",
        "Build a module that uses `{{.async.}}` with {mod} to perform {op} non-blocking."
    ],
    "This example uses the `{mod}` module for asynchronous programming in Nim. We define a procedure with the `{{.async.}}` pragma. The `await` keyword is used to yield control back to the event loop while waiting for `{op}` to complete. This is crucial for I/O-bound tasks.",
    async_code, async_gen)

def http_gen():
    methods = ["getContent", "postContent", "request"]
    urls = ["\"http://example.com\"", "\"https://api.github.com\"", "\"http://localhost:8080\""]
    async_flags = ["true", "false"]
    for m, u, a in itertools.product(methods, urls, async_flags):
        yield {"method": m, "url": u, "is_async": a}

def http_code(p):
    is_async = p["is_async"]
    method = p["method"]
    url = p["url"]

    if is_async == "true":
        imp = "import std/asyncdispatch"
        proc_def = "proc fetchData*(): Future[string] {.async.} ="
        client = "var client = newAsyncHttpClient()"
        if method == "getContent":
            req = f"  result = await client.getContent({url})"
        elif method == "postContent":
            req = f"  result = await client.postContent({url}, body=\"data\")"
        else:
            req = f"  let resp = await client.request({url})\n  result = await resp.body"
        main_call = "    let data = waitFor fetchData()\n    echo \"Fetched async length: \", data.len"
    else:
        imp = ""
        proc_def = "proc fetchData*(): string ="
        client = "var client = newHttpClient()"
        if method == "getContent":
            req = f"  result = client.getContent({url})"
        elif method == "postContent":
            req = f"  result = client.postContent({url}, body=\"data\")"
        else:
            req = f"  let resp = client.request({url})\n  result = resp.body"
        main_call = "    let data = fetchData()\n    echo \"Fetched sync length: \", data.len"

    return f"""import std/httpclient
{imp}

{proc_def}
  {client}
  defer: client.close()
{req}

when isMainModule:
  try:
{main_call}
  except HttpRequestError, OSError:
    echo "Network error occurred, which is expected in a disconnected environment."
"""

register_template("async_http", ["async", "httpclient", "networking"],
    [
        "Write a Nim program using std/httpclient to make a {method} request to {url}.",
        "Create an HTTP client in Nim that fetches data from {url} using {method}.",
        "Implement a script that calls {method} on {url} (async: {is_async}) using httpclient.",
        "Build a module demonstrating std/httpclient making a request to {url}."
    ],
    "This code demonstrates making network requests using `std/httpclient`. Based on the configuration (`async: {is_async}`), we instantiate either an `HttpClient` or an `AsyncHttpClient`. We then perform a `{method}` request to `{url}` and read the response.",
    http_code, http_gen)

def async_streams_gen():
    modes = ["fmRead", "fmWrite"]
    files = ["\"test.txt\"", "\"data.bin\"", "\"log.txt\""]
    ops = ["readAll", "write"]
    for m, f, o in itertools.product(modes, files, ops):
        yield {"mode": m, "file": f, "op": o}

def ast_streams_code(p):
    mode = p["mode"]
    file = p["file"]
    op = p["op"]

    if mode == "fmRead":
        if op == "readAll":
            op_code = f"      let data = await file.readAll()\n      echo \"Read \", data.len, \" bytes\""
        else:
            op_code = f"      echo \"Operation skipped\""
        body = f"  try:\n    var file = openAsync({file}, fmRead)\n    defer: file.close()\n{op_code}\n  except OSError:\n    echo \"File access error\""
    else:
        if op == "write":
            op_code = f"      await file.write(\"Async data\")"
        else:
            op_code = f"      echo \"Operation skipped\""
        body = f"  try:\n    var file = openAsync({file}, fmWrite)\n    defer: file.close()\n{op_code}\n  except OSError:\n    echo \"File access error\""

    return f"""import std/asyncdispatch
import std/asyncfile

proc processFile*(): Future[void] {{.async.}} =
{body}

when isMainModule:
  waitFor processFile()
"""

register_template("async_file", ["async", "asyncfile"],
    [
        "Write a Nim program using std/asyncfile to {op} a file {file} async.",
        "Create an async script reading/writing {file} in mode {mode} via asyncfile.",
        "Implement non-blocking file I/O for {file} using std/asyncfile and {op}.",
        "Build a module demonstrating asynchronous file access on {file}."
    ],
    "This example uses `std/asyncfile` for asynchronous file operations. We open the file `{file}` in `{mode}` mode. Then we perform `{op}` asynchronously, using `await`. This is vital for high-performance servers where blocking disk I/O would stall the event loop.",
    ast_streams_code, async_streams_gen)

def async_gen_more():
    modules = ["asyncdispatch", "chronos"]
    ops = ["sleepAsync", "readAsync", "writeAsync", "connect"]
    ret_types = ["int", "string", "void"]
    loops = ["1", "5", "10", "20"]
    for m, o, r, l in itertools.product(modules, ops, ret_types, loops):
        yield {"mod": m, "op": o, "ret": r, "loop": l}

def async_more_code(p):
    op = p["op"]
    ret = p["ret"]
    mod = p["mod"]
    loop = p["loop"]

    if op == "sleepAsync":
        task_body = f"    await sleepAsync(10)"
    elif op in ["readAsync", "writeAsync"]:
        task_body = f"    # Mock IO\n    await sleepAsync(5)"
    else:
        task_body = f"    await sleepAsync(1)"

    if ret == "int":
        task_ret = "  result = 42"
    elif ret == "string":
        task_ret = "  result = \"Done looping\""
    else:
        task_ret = "  echo \"Task complete\""

    return f"""import {mod}

proc runLoop*(): Future[{ret}] {{.async.}} =
  for i in 1..{loop}:
{task_body}
{task_ret}

when isMainModule:
  discard waitFor runLoop()
"""

register_template("async_loop", ["async", "await", "loop", "asyncdispatch"],
    [
        "Write a Nim program looping {loop} times in an async proc with {mod} returning {ret} and using {op}.",
        "Create a script demonstrating async loops in Nim via {mod} calling {op} {loop} times.",
        "Implement a recurring async task in Nim using {mod} and yielding {ret} from {op} ({loop} iterations)."
    ],
    "This example uses the `{mod}` module for a looping asynchronous task. We define a procedure with the `{{.async.}}` pragma and loop `{loop}` times. The `await` keyword yields control back to the event loop on each iteration. This is a common pattern for background workers.",
    async_more_code, async_gen_more)
def multi_gen():
    files = ["data.json", "config.json", "settings.json", "input.json", "output.json"]
    dirs = ["/tmp", "/var/lib", "/opt/app", "~/.config", "./data"]
    types = ["int", "string", "float", "bool"]
    funcs = ["sqrt", "sin", "cos", "tan", "cbrt"]
    for f, d, t, fu in itertools.product(files, dirs, types, funcs):
        yield {"file": f, "dir": d, "type": t, "func": fu}

register_template("stdlib_multi5", ["stdlib", "os", "json", "strutils", "math", "times"],
    [
        "Write a Nim program combining os, json, strutils, math, and times to process {file}.",
        "Create a script using 5 stdlib modules to parse {file} in {dir}.",
        "Implement a data processor reading {file} and applying math functions using multiple stdlibs.",
        "Build a Nim module demonstrating os, json, strutils, math, and times working together."
    ],
    "This code combines five standard library modules: `os` (for path manipulation), `json` (for parsing), `strutils` (for string handling), `math` (for calculations), and `times` (for timestamping). Combining modules is common in real-world scripts for data processing and configuration management.",
    """import std/os
import std/json
import std/strutils
import std/math
import std/times

proc processComplexData*(baseDir, filename: string) =
  let fullPath = baseDir / filename
  let startTime = now()

  if fileExists(fullPath):
    let raw = readFile(fullPath).strip()
    try:
      let parsed = parseJson(raw)
      echo "Parsed JSON: ", parsed
    except JsonParsingError:
      echo "Failed to parse"

  let dummyCalc = {func}(144.0)
  echo "Calculation: ", dummyCalc
  echo "Elapsed time: ", now() - startTime

when isMainModule:
  processComplexData("{dir}", "{file}")
""", multi_gen)

def multi2_gen():
    files = ["data.csv", "log.csv", "users.csv", "metrics.csv", "report.csv"]
    dirs = ["/tmp", "/var/log", "/opt/data", "~/downloads", "./out"]
    funcs = ["split", "replace", "strip", "toUpperAscii"]
    times_ops = ["now()", "now().utc()", "getTime().local()", "getTime()"]
    for f, d, fu, to in itertools.product(files, dirs, funcs, times_ops):
        yield {"file": f, "dir": d, "func": fu, "top": to}

def multi2_code(p):
    top = p["top"]
    func = p["func"]
    file = p["file"]
    dir = p["dir"]

    if func == "split":
        op_code = f"            echo col.split(\",\")"
    elif func == "replace":
        op_code = f"            echo col.replace(\"a\", \"b\")"
    elif func == "strip":
        op_code = f"            echo col.strip()"
    else:
        op_code = f"            echo col.toUpperAscii()"

    return f"""import std/os
import std/parsecsv
import std/strutils
import std/streams
import std/times

proc processCSV*(baseDir, filename: string) =
  let fullPath = baseDir / filename
  let startTime = {top}

  if fileExists(fullPath):
    var strm = newFileStream(fullPath, fmRead)
    if strm != nil:
      var parser: CsvParser
      open(parser, strm, filename)
      while readRow(parser):
        for col in parser.row:
{op_code}
      close(parser)

  # We just convert both to string to avoid math operations on `Time` and `DateTime`
  echo "Elapsed: Done at ", {top}

when isMainModule:
  processCSV("{dir}", "{file}")
"""

register_template("stdlib_multi_csv", ["stdlib", "os", "parsecsv", "strutils", "streams", "times"],
    [
        "Write a Nim program combining os, parsecsv, strutils, streams, and times to process {file}.",
        "Create a script using 5 stdlib modules to parse CSV {file} in {dir}.",
        "Implement a CSV processor reading {file} and applying string formatting using multiple stdlibs.",
        "Build a Nim module demonstrating os, parsecsv, strutils, streams, and times."
    ],
    "This example uses `os`, `parsecsv`, `strutils`, `streams`, and `times` together. We locate a CSV file with `os`, read it using `streams` and `parsecsv`, format the data with `strutils`, and measure the processing time using `times`. Integrating these modules covers typical data ingestion tasks.",
    multi2_code, multi2_gen)

def generate_examples(target_total=3000):
    seen_codes = set()
    examples = []

    if not TEMPLATES:
        print("No templates found.")
        return examples

    perms_per_template = 3000

    for t in TEMPLATES:
        perms = list(t.generator())
        random.shuffle(perms)

        target_per_t = max(250, (target_total // len(TEMPLATES)) * 10)
        if "async" in t.name:
             target_per_t *= 3
        if "multi" in t.name or "os_json_strutils" in t.name:
             target_per_t *= 3

        for p in perms[:target_per_t]:
            prompt_fmt = random.choice(t.prompts)
            prompt = prompt_fmt.format(**p)
            thinking = t.thinking.format(**p)

            if callable(t.code):
                code = t.code(p)
            else:
                code = t.code.format(**p)

            if code not in seen_codes:
                seen_codes.add(code)
                examples.append({
                    "prompt": prompt,
                    "thinking": thinking,
                    "nim_code": code,
                    "tags": t.tags
                })
    return examples

if __name__ == "__main__":
    examples = generate_examples(3000)
    print(f"Generated {len(examples)} examples.")
    with open("nim_training_data.jsonl", "w") as f:
        for ex in examples:
            out = {
                "prompt": ex["prompt"],
                "thinking": ex["thinking"],
                "nim_code": ex["nim_code"]
            }
            f.write(json.dumps(out) + "\n")
