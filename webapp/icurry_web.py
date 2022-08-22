from flask import Flask, render_template, Markup, session, make_response, request
from random import randint
from subprocess import run, PIPE, TimeoutExpired
from os import path, mkdir, remove, scandir, rmdir
from shutil import rmtree
from base64 import b32encode
from hashlib import md5
from time import time
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

import threading
import re
import xml.etree.ElementTree as ET

app = Flask(__name__)
app.config["SESSION_COOKIE_SAMESITE"] = "Strict"
cache_lock = threading.Lock()
MAX_CACHE_AGE = 60*60
STEP_AMOUNT_MAX = 200 #Maximum of steps allowed for one computation request.
                      #Value set here is used in the entire application

@app.route("/static/<path:path>")
def serve_static():
    return send_from_directory("static", path)

#deliver the main page that contains a form for entering a program
@app.route("/", methods=["GET"])
def main_form():
    prog = ""
    main_exp = ""
    id = request.args.get("id")
    if (id != None) and check_prog_cache(id):
        lines = load_prog(id).splitlines()
        main_exp = lines.pop()[14:]
        prog = "\n".join(lines[:-1])

    # get example-list from examples-directory TODO: recursively scan sub-dirs
    #example_list = []
    with scandir("examples") as entries:
        examples_list = [entry.name[:-6] for entry in entries \
                                    if entry.is_file() and entry.name.endswith(".curry")]
    return render_template("form.html", \
            prog = prog, main_exp = main_exp, examples = examples_list, max_steps = STEP_AMOUNT_MAX)

#deliver a page that shows a cached programs source
@app.route("/source", methods=["GET"])
def display_source():
    id = request.args.get("id")
    if check_prog_cache(id):
        prog = load_prog(id)
        longest_line = max([len(line) for line in prog.splitlines()]) * 10
        win_width = max(350, min(600, longest_line))
        return render_template("program.html", prog = prog, width = win_width)
    else:
        return invalid_id_page("There is no source available for this id.")

@app.route("/example", methods=["POST"])
def serve_example():
    print(request.form)
    with open("examples/" + request.form["example"] + ".curry","r") as ex_file:
        example = ex_file.read();
    return example

#deliver a page that shows a slideshow of a computation's term graphs
@app.route("/slideshow", methods=["POST", "GET", "PUT"])
def build_slideshow():
    #Using a thread here might actually not be that helpful
    threading.Thread(target=cleanup_cache, args=(MAX_CACHE_AGE,)).start()

    # Handle visualization request, render svgs and return request-hash
    if request.method == "POST":
        icurry_args = ["-q", "-m", "icurry_main"]
        prog = "\n".join([line.rstrip() for line in request.form["program"].splitlines()]).strip()
        main_exp = request.form["main_exp"].strip()
        prog_with_main = re.sub("\n\n\n+", "\n\n", prog) + "\n\nicurry_main = " + main_exp
        b32_hash = str(b32encode(md5((prog_with_main).encode("utf-8")).digest()),"utf-8")
        hash = b32_hash.replace("=", "")
        #hash-name for svg-files
        g_hash = "_" + hash
        #hash-name for program-file
        p_hash = "p" + g_hash

        # set icurry cli-parameter for maximum-computation steps
        # and add step-info to hash
        max_steps = int(request.form.get("max_steps"))
        if max_steps is None or max_steps > STEP_AMOUNT_MAX:
            max_steps = STEP_AMOUNT_MAX
        icurry_args.append(f"--maxsteps={max_steps+1}")
        g_hash += f"_{max_steps}"

        # icurry-parameter for maximum termgraph-as-tree depth
        max_depth = request.form.get("max_depth")
        if max_depth is None:
            max_depth = "10"
        icurry_args.append(f"--maxdepth={max_depth}")

        #add i to hash for visualization with node ids
        if (request.form.get("show_ids")):
            g_hash = "i" + g_hash
            icurry_args.append("--shownodeids")

        # icurry-parameter for the type of visualization (graph or tree)
        visualize_type = request.form["visualize_type"]
        if (visualize_type == "graph"):
            g_hash = "g" + g_hash
            icurry_args.append(f"--graphsvg=../svgs/{g_hash}")
        elif (visualize_type == "tree"):
            g_hash = "t" + max_depth + g_hash
            icurry_args.append(f"--treesvg=../svgs/{g_hash}")
        else:
            return ("Invalid visualization type", 400)

        if not check_svg_cache(g_hash):
            with open(f"progs/{p_hash}.curry","w") as prog_file:
                prog_file.write(prog_with_main)
            icurry_args.append(f"progs/{p_hash}.curry")
            print("Running icurry with args: " + str(icurry_args))
            try:
                # As arguments are supplied as individual strings, shell injection is not possible
                comp_proc = run(["icurry"] + icurry_args,\
                    timeout=30, stderr=PIPE, stdout=PIPE, encoding="UTF-8")
            except TimeoutExpired:
                print("Execution Timeout")
                delete_cache_entry(g_hash, p_hash)
                return ("", 508)

            if comp_proc.returncode == 0:
                return (g_hash, 200)
            else:
                print(comp_proc.stderr)
                delete_cache_entry(g_hash, p_hash)
                return (comp_proc.stderr, 400)
        else:
            return (g_hash, 200)

    # display rendered svgs
    elif request.method == "GET":
        g_hash = secure_filename(request.args.get("id"))
        # get start index and make a usable integer out of it
        s_ind = request.args.get("index")
        try:
            s_ind = max(int(s_ind) if (not s_ind is None) else 1, 0)
        except:
            s_ind = 1

        p_hash = "p" + g_hash[g_hash.find('_'):]
        try:
            svgs = load_svgs(g_hash, s_ind)
        except Exception as e:
            print(e)
            delete_cache_entry(g_hash, p_hash)
            return (render_template("error.html", \
                title = "Error while loading svgs", \
                description = "If you supplied your own images:\
                    Make sure they are properly formatted term graph svgs"), \
                500)
        if svgs == []:
            return invalid_id_page("This url is not valid (anymore).")
        else:
            return render_template("slideshow.html", svgs = svgs, len = len(svgs), p_id = p_hash)

    # save pre-rendered svgs and return their id
    elif request.method == "PUT":
        if (request.content_length > pow(2,20)):
            return (f"Content too large, maximum is 1 MB", 400)

        while True:
            id = "u_" + rand_str(26)
            if (not check_svg_prerendered_cache(id)):
                break

        files = [file for file in request.files.getlist("svgs") if re.fullmatch(".+\.svg", file.filename)]
        files.sort(key=lambda x: x.filename)

        if (not path.isdir(f"svgs/{id}")):
            mkdir(f"svgs/{id}")
        ind = 1
        for file in files:
            file.save(f"svgs/{id}/img{ind}.svg")
            ind += 1

        return (id, 200)

# Show the "about" page
@app.route("/about", methods=["GET"])
def info_page():
    return (render_template("info.html", max_steps = STEP_AMOUNT_MAX), 200)


def invalid_id_page(msg):
    return (render_template("error.html", \
        title = "Invalid id or index", \
        description = msg), \
        404) #410 - Gone would also be a possibility


def check_prog_cache(name):
    return path.isfile(f"progs/{name}.curry")

# Load a single program file from cache-storage
def load_prog(name):
    with cache_lock:
        with open(f"progs/{name}.curry","r") as file:
            print(f"loading soure file 'progs/{name}.curry'")
            prog = file.read()
            return prog

# Check if a series of svgs with the exact specified name is in cache
def check_svg_prerendered_cache(name):
    return path.isfile(f"svgs/{name}/img0.svg")

# Check if a series of svgs with the same name and enough rendered images
# is in cache. Does not work for uploaded series.
def check_svg_cache(name):
    short_name, requested_amount = split_hash(name)
    cache_entry = get_svg_entry(short_name)
    if cache_entry is None:
        return False
    else:
        _, entry_length = split_hash(cache_entry)
        if entry_length >= requested_amount:
            return True
        else:
            # if found entry is not long enough, remove it to be replaced
            delete_cache_entry(cache_entry)
            return False

# Check if a series of svgs with the same name is in cache
# and return its name with length of the series
def get_svg_entry(short_name):
    with scandir("svgs") as cache_entries:
        for entry in cache_entries:
            if(entry.is_dir() and entry.name.startswith(short_name)):
                return entry.name
    return None


def split_hash(hash):
    last_underscore = hash.rindex("_")
    requested_amount = int(hash[last_underscore+1:])
    short_name = hash[:last_underscore]
    return short_name, requested_amount


# Remove a program and its graph-svgs from cache-storage
def delete_cache_entry(g_name, p_name = ""):
    g_name = secure_filename(g_name)
    p_name = secure_filename(p_name)
    cache_lock.acquire()
    if (path.isdir(f"svgs/{g_name}")):
        rmtree(f"svgs/{g_name}")
    prog_file = f"progs/{p_name}.curry"
    if path.isfile(prog_file):
        remove(prog_file)
    cache_lock.release()

# clear cache-directores of old files recursively
def cleanup_cache(max_age):
    dirs_to_scan = ["progs", "svgs"]
    with cache_lock:
        for dir in dirs_to_scan:
            cleanup_dir(dir, max_age)

# clean a directory of old files recursively
# return True if dir is empty after cleanup
def cleanup_dir(dir, max_age):
    curr_time = time()
    is_dir_empty = True
    with scandir(dir) as entries:
        for entry in entries:
            if entry.is_file() and (curr_time - entry.stat().st_atime) > max_age:
                remove(entry.path)
            elif entry.is_dir():
                if (cleanup_dir(entry, max_age)):
                    rmdir(entry)
                else:
                    is_dir_empty = False
            else:
                is_dir_empty = False
    return is_dir_empty

# Load a computation's svgs from storage
def load_svgs(name, ind):
    requested_amount = float('inf')
    if not name.startswith("u_"):
        name, requested_amount = split_hash(name)

    name = get_svg_entry(name)
    print(f"loading image series '{name}' with {requested_amount} images")

    svgs = []
    with cache_lock:
        while ind <= requested_amount:
            currFile = f"svgs/{name}/img{ind}.svg" #acually look for the right dir
            if path.isfile(currFile):
                svgs.append(ET.parse(currFile))
                ind += 1
            else:
                break
    process_svgs(svgs)

    svgstrs = list(map(lambda svg: Markup(ET.tostring(svg.getroot(), encoding="unicode", method="html")), svgs))

    return svgstrs

# Add mouseenter and mouseleave events to a list of svgs to enable sharing-highlighting
# This method is mutating
def process_svgs(svgs):
    for i,graph in enumerate(svgs):
        nodes = graph.getroot().findall("{http://www.w3.org/2000/svg}g")
        for el in nodes:
            nodeClass = el.get("class")
            # TODO: check that the class is actually nodeX
            if nodeClass != None:
                nodeId = re.findall("[0-9]+", nodeClass)[0]
                el.set("class", f"node{nodeId} graph{i}")
                el.set("onmouseenter", f"nodeEntered({nodeId},{i})")
                el.set("onmouseleave", f"nodeExited({nodeId},{i})")


def rand_str(length):
    str = ""
    for _ in range(length):
        # Consider only letters
        str += (chr(randint(65, 65 + 26 - 1)))
    return str

# Setup: create necessary directories if they don't exist
def create_dirs():
    if not path.isdir("svgs"):
        mkdir("svgs")
    if not path.isdir("progs"):
        mkdir("progs")


# Setup: Set parameters in files
def apply_parameters():
    with open("static/script-form.js", "r") as formscript:
        formscript_lines = formscript.readlines()
    formscript_lines[0] = f"const MAX_STEPS = {STEP_AMOUNT_MAX};\n"
    with open("static/script-form.js", "w") as formscript:
        formscript.writelines(formscript_lines)


if __name__ == "__main__":
    create_dirs()
    apply_parameters()
    cleanup_cache(MAX_CACHE_AGE)
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    app.run(debug=True, host=("localhost"))
