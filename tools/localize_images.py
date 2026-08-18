"""Localize every image referenced by a markdown file into <md_dir>/images/.

Handles:
  * MarkText absolute paths (C:/Users/.../marktext/images/...), plain or file:///
  * remote http(s) images (downloaded so GitHub keeps rendering them)
Filenames are sanitized to [A-Za-z0-9._-] so GitHub link targets stay valid.
Content-hash dedup; idempotent - existing files are reused, not re-fetched.
"""
import os, re, sys, shutil, hashlib, urllib.parse, urllib.request

UA = {'User-Agent': 'Mozilla/5.0'}
EXT_OK = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg'}
LOCAL = re.compile(r'(?:file:///)?[A-Za-z]:/[^\s"\')]*?/marktext/images/([^"\s]+)')
REMOTE = re.compile(r'https?://[^\s"\')]+')


def sanitize(name):
    return re.sub(r'[^A-Za-z0-9._-]+', '-', name).strip('-')


def split_trailing_parens(name):
    """Give back any ')' that belongs to the enclosing markdown link, not the name."""
    tail = ''
    while name.endswith(')') and name.count('(') < name.count(')'):
        name, tail = name[:-1], ')' + tail
    return name, tail


def main(md_path):
    md_dir = os.path.dirname(os.path.abspath(md_path))
    imgdir = os.path.join(md_dir, 'images')
    os.makedirs(imgdir, exist_ok=True)
    by_hash = {}
    for fn in os.listdir(imgdir):
        p = os.path.join(imgdir, fn)
        if os.path.isfile(p):
            by_hash[hashlib.sha256(open(p, 'rb').read()).hexdigest()] = fn

    txt = open(md_path, encoding='utf8').read()
    stats = {'local': 0, 'remote': 0}
    problems = []

    def store(data, name):
        h = hashlib.sha256(data).hexdigest()
        if h in by_hash:
            return by_hash[h]
        base, ext = os.path.splitext(sanitize(name))
        if ext.lower() not in EXT_OK:
            ext = '.jpg'
        base = base[:100] or 'image'
        name = base + ext
        n = 1
        while os.path.exists(os.path.join(imgdir, name)):
            name = f'{base}-{n}{ext}'
            n += 1
        open(os.path.join(imgdir, name), 'wb').write(data)
        by_hash[h] = name
        return name

    def repl_local(m):
        raw = m.group(1)
        name, tail = split_trailing_parens(raw)
        src = m.group(0).replace('file:///', '')
        src = src[:len(src) - len(tail)] if tail else src
        if not os.path.exists(src):
            problems.append('MISSING ' + src)
            return m.group(0)
        stats['local'] += 1
        return 'images/' + store(open(src, 'rb').read(), name) + tail

    def repl_remote(m):
        url, tail = split_trailing_parens(m.group(0))
        path = urllib.parse.urlparse(url).path
        if os.path.splitext(path)[1].lower() not in EXT_OK and 'iu/?u=' not in url:
            return m.group(0)          # not an image link - leave alone
        try:
            data = urllib.request.urlopen(
                urllib.request.Request(url, headers=UA), timeout=45).read()
        except Exception as e:
            problems.append(f'FAILED {url} ({e})')
            return m.group(0)
        name = os.path.basename(urllib.parse.unquote(path)) or 'remote'
        if 'iu/?u=' in url:            # duckduckgo proxy - real name is in the query
            inner = urllib.parse.parse_qs(urllib.parse.urlparse(url).query).get('u', [''])[0]
            name = os.path.basename(urllib.parse.urlparse(inner).path) or name
        stats['remote'] += 1
        return 'images/' + store(data, name) + tail

    txt = LOCAL.sub(repl_local, txt)
    # only rewrite remote URLs sitting in an image position
    def img_scan(m):
        return m.group(0)[:m.start(1) - m.start(0)] + REMOTE.sub(repl_remote, m.group(1)) + \
               m.group(0)[m.end(1) - m.start(0):]
    txt = re.sub(r'!\[[^\]]*\]\((\s*[^)\s]+)', img_scan, txt)
    txt = re.sub(r'(<img[^>]*\bsrc=")([^"]+)', lambda m: m.group(1) + REMOTE.sub(repl_remote, m.group(2)), txt)

    open(md_path, 'w', encoding='utf8', newline='').write(txt)
    print(f'{md_path}: local={stats["local"]} remote={stats["remote"]}')
    for p in problems:
        print('  ' + p)


if __name__ == '__main__':
    for a in sys.argv[1:]:
        main(a)
