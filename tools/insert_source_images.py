"""Attach the source CDN images to every pearl that cites a question id.

An **IMAGES:** block is (re)generated directly above each `Q...` citation
line, listing that question's images as remote CDN links - nothing is
downloaded. The local images/ folder is reserved for hand-pasted images.
"""
import json, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = json.load(open(os.path.join(ROOT, 'tools/image_index.json'), encoding='utf8'))
BLOCK = re.compile(r'\n\*\*IMAGES:\*\*\n(?:!\[[^\]]*\]\([^)]*\)\n)+', re.M)
CITE = re.compile(r'^`Q?[A-Z0-9][^`]*`\s*$', re.M)
QID = re.compile(r'\b(?:Q)?([A-Z]{1,2}\d{3,}|\d{3,})\b')

# the raw S3 bucket blocks public reads; its CDN front serves the same paths
HOST_FIX = ('cerebellum-web-static.s3.amazonaws.com', 'media.cerebellumacademy.com')
# assets that no longer resolve (404 / private) - skipped so no broken image renders
DEAD = (
    'https://pub-8c30f7a873214da0837b787a0c529b95.r2.dev/634ec2697b6a1faa66b2ed43f525324.webp',
    'trello.com/',
)


def main(paths):
    grand = 0
    for md in paths:
        txt = open(md, encoding='utf8').read()
        txt = BLOCK.sub('\n', txt)          # drop any previous block
        added = [0]

        def repl(m):
            line = m.group(0)
            pics = []
            for qid in QID.findall(line):
                entry = IDX.get(qid)
                if not entry:
                    continue
                for kind in ('question', 'explanation'):
                    for url in entry[kind]:
                        url = url.replace(*HOST_FIX)
                        if any(d in url for d in DEAD):
                            continue
                        item = '![%s](%s)' % (kind, url)
                        if item not in pics:
                            pics.append(item)
            if not pics:
                return line
            added[0] += len(pics)
            return '**IMAGES:**\n' + '\n'.join(pics) + '\n\n' + line

        txt = CITE.sub(repl, txt)
        open(md, 'w', encoding='utf8', newline='').write(txt)
        grand += added[0]
        print('%-24s images linked: %d' % (os.path.basename(md), added[0]))
    print('total:', grand)


if __name__ == '__main__':
    main(sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT, '*.md'))))
