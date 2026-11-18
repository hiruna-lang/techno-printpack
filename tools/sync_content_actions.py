"""Apply the shared content-action pass without rebuilding independent page edits."""
from pathlib import Path
import re,sys
from content_actions import refine_actions

ROOT=Path(__file__).resolve().parents[1]
PAGES=['index','about','products','capabilities','industries','quality','quotation','contact','farm/index']
STYLE='<link rel="stylesheet" href="assets/css/content-actions.css">'
check='--check' in sys.argv
for name in PAGES:
    path=ROOT/f'{name}.html';before=path.read_text(encoding='utf-8')
    page='farm' if name=='farm/index' else name
    match=re.search(r'(<main\b[^>]*>)(.*?)(</main>)',before,re.S)
    assert match,name
    content=refine_actions(page,match[2])
    after=before[:match.start(2)]+content+before[match.end(2):]
    if page!='farm' and STYLE not in after:
        anchor='<link rel="stylesheet" href="assets/css/navigation.css">'
        assert anchor in after,name
        after=after.replace(anchor,STYLE+anchor,1)
    if check:assert before==after,f'Content actions out of sync: {name}'
    elif before!=after:path.write_text(after,encoding='utf-8')
print(('Checked' if check else 'Updated')+' content actions on eight company pages and the Farm page.')
