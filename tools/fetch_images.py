"""Download images for the Q ids cited in a subject pearl file.

Files land in bookmark-pearls/images/, named <qid>-<q|e><n>.<ext>.
Content-hash dedup: identical bytes reuse the first-seen filename.
Idempotent - already-present files are skipped.
"""
import json, os, re, sys, hashlib, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMGDIR = os.path.join(ROOT, 'bookmark-pearls', 'images')
IDX = json.load(open(os.path.join(ROOT, 'tools/image_index.json'), encoding='utf8'))

EXT_OK = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
UA = {'User-Agent': 'Mozilla/5.0'}


def ext_of(url):
    e = os.path.splitext(url.split('?')[0])[1].lower()
    # dailyrounds embeds dimensions: ...x600x564.JPEG
    return e if e in EXT_OK else '.jpg'


def qids_in(path):
    txt = open(path, encoding='utf8').read()
    ids = []
    for line in re.findall(r'^`(Q[^`]+)`\s*$', txt, re.M):
        ids += re.findall(r'Q([A-Za-z0-9]+)', line)
    return ids


def main(md_path):
    os.makedirs(IMGDIR, exist_ok=True)
    by_hash = {}
    for fn in os.listdir(IMGDIR):
        p = os.path.join(IMGDIR, fn)
        if os.path.isfile(p):
            by_hash[hashlib.sha256(open(p, 'rb').read()).hexdigest()] = fn

    mapping, fails = {}, []
    for qid in qids_in(md_path):
        entry = IDX.get(qid)
        if not entry:
            continue
        got = []
        for kind, key in (('q', 'question'), ('e', 'explanation')):
            for n, url in enumerate(entry[key], 1):
                name = f'{qid}-{kind}{n}{ext_of(url)}'
                dest = os.path.join(IMGDIR, name)
                if os.path.exists(dest):
                    got.append((key, name))
                    continue
                try:
                    req = urllib.request.Request(url, headers=UA)
                    data = urllib.request.urlopen(req, timeout=30).read()
                except Exception as e:
                    fails.append((qid, url, str(e)))
                    continue
                h = hashlib.sha256(data).hexdigest()
                if h in by_hash:
                    got.append((key, by_hash[h]))
                    continue
                open(dest, 'wb').write(data)
                by_hash[h] = name
                got.append((key, name))
        if got:
            mapping[qid] = got

    out = os.path.join(ROOT, 'tools', 'imgmap-%s.json' %
                       os.path.splitext(os.path.basename(md_path))[0])
    json.dump(mapping, open(out, 'w'), indent=1)
    print('questions with images:', len(mapping),
          '| files:', sum(len(v) for v in mapping.values()),
          '| failed:', len(fails))
    for f in fails[:10]:
        print('  FAIL', f)


if __name__ == '__main__':
    main(sys.argv[1])
