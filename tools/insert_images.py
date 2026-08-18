"""Insert downloaded images into a subject pearl file.

For each pearl, an **IMAGES:** block is added immediately above the
`Q<id>` source line, listing that pearl's question images then its
explanation images. Idempotent - an existing block is regenerated.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCK = re.compile(r'\n\*\*IMAGES:\*\*\n(?:!\[[^\]]*\]\([^)]*\)\n)+', re.M)


def main(md_path):
    stem = os.path.splitext(os.path.basename(md_path))[0]
    mapping = json.load(open(os.path.join(ROOT, 'tools', 'imgmap-%s.json' % stem), encoding='utf8'))
    txt = open(md_path, encoding='utf8').read()
    txt = BLOCK.sub('\n', txt)

    added = [0]

    def repl(m):
        line = m.group(0)
        ids = re.findall(r'Q([A-Za-z0-9]+)', line)
        pics = []
        for qid in ids:
            for kind, name in mapping.get(qid, []):
                alt = 'question' if kind == 'question' else 'explanation'
                item = '![%s](images/%s)' % (alt, name)
                if item not in pics:
                    pics.append(item)
        if not pics:
            return line
        added[0] += len(pics)
        return '**IMAGES:**\n' + '\n'.join(pics) + '\n\n' + line

    txt = re.sub(r'^`Q[^`]+`\s*$', repl, txt, flags=re.M)
    open(md_path, 'w', encoding='utf8', newline='').write(txt)
    print(stem, '- images inserted:', added[0])


if __name__ == '__main__':
    main(sys.argv[1])
