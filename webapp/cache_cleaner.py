# Functions for cleaning the cache of the icurry-webapp

# Remove a program and its graph-svgs from cache-storage
def delete_cache_entry(g_name, p_name = ""):
    g_name = secure_filename(g_name)
    p_name = secure_filename(p_name)
    cache_lock.acquire()
    if (path.isdir(f"{WEBAPP_PATH}svgs/{g_name}")):
        rmtree(f"{WEBAPP_PATH}svgs/{g_name}")
    prog_file = f"{WEBAPP_PATH}progs/{p_name}.curry"
    if path.isfile(prog_file):
        remove(prog_file)
    cache_lock.release()

# clear cache-directores of old files recursively
def cleanup_cache(max_age):
    dirs_to_scan = [f"{WEBAPP_PATH}progs", f"{WEBAPP_PATH}svgs"]
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

if __name__ == "__main__":
    cleanup_cache(MAX_CACHE_AGE, True)
