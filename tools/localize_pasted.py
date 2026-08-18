"""Copy MarkText-pasted images into images/ and rewrite
the absolute C:/Users/... paths to relative images/ paths."""
import os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMGDIR = os.path.join(ROOT, 'images')
PAT = re.compile(r'(?:file:///)?[A-Za-z]:/Users/[^)\s]*?/marktext/images/([^)\s]+)')


def main(md_path):
    os.makedirs(IMGDIR, exist_ok=True)
    txt = open(md_path, encoding='utf8').read()
    moved, missing = 0, []

    def repl(m):
        nonlocal moved
        src = m.group(0).replace('file:///', '')
        name = m.group(1)
        dest = os.path.join(IMGDIR, name)
        if not os.path.exists(dest):
            if not os.path.exists(src):
                missing.append(src)
                return m.group(0)
            shutil.copy2(src, dest)
        moved += 1
        return 'images/' + name

    txt = PAT.sub(repl, txt)
    open(md_path, 'w', encoding='utf8', newline='').write(txt)
    print(os.path.basename(md_path), '- localized:', moved, '| missing:', len(missing))
    for p in missing:
        print('  MISSING', p)


if __name__ == '__main__':
    main(sys.argv[1])
