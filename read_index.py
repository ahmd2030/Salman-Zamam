
try:
    with open('index.html', 'r', encoding='utf-8') as f: content = f.read()
except:
    with open('index.html', 'r', encoding='utf-16') as f: content = f.read()

target = 'id="new-car-section"'
start = content.find(target)
if start != -1:
    print(content[start:start+400])
else:
    print('Not found')
