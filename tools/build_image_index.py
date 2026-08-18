"""Build Q<id> -> [image urls] index from the two bookmark source JSONs."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _urls(v):
    out = []
    for i in v or []:
        u = i if isinstance(i, str) else (i.get('url') or i.get('src') or '')
        if u:
            out.append(u)
    return out

def build():
    idx = {}
    d = json.load(open(os.path.join(ROOT, 'source/all_bookmarks_converted.json'), encoding='utf8'))
    for q in d['questions']:
        q_i = _urls(q.get('question_images'))
        e_i = _urls(q.get('explanation_images'))
        if q_i or e_i:
            idx[str(q['id'])] = {'question': q_i, 'explanation': e_i}

    d2 = json.load(open(os.path.join(ROOT, 'source/my-bookmarks-2026-08-14.json'), encoding='utf8'))
    qs = d2['questions'] if isinstance(d2, dict) else d2
    for x in qs:
        q = x['question']
        q_i = _urls(q.get('images'))
        e_i = _urls(q.get('explanationImages'))
        if q_i or e_i:
            idx.setdefault(str(x['id']), {'question': q_i, 'explanation': e_i})
    return idx

if __name__ == '__main__':
    idx = build()
    json.dump(idx, open(os.path.join(ROOT, 'tools/image_index.json'), 'w'), indent=1)
    print(len(idx), 'questions with images')
