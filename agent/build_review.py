import html,re
import sys,json
WEEK=sys.argv[1]; LABEL=sys.argv[2]
old=open('agent/assets/page_template.html').read()
head=old[:old.index('<div class="wrap"')]
tail=old[old.index('<div class="lb" id="lb"'):]
tail=tail.replace('<p>اضغطي مطولاً على الصورة ثم «حفظ الصورة»</p>','')
RAW=f'https://raw.githubusercontent.com/bdryh9068-boop/dawadom-media./main/posts/{WEEK}/'
H='#جمعية_الدعوة_بأم_الدوم'
P=json.load(open(f'agent/weeks/{WEEK}.json'))
for p in P:
    p.setdefault('st','')
e=html.escape
man=[];allp=[]
for p in P:
    i=p['id']
    if p['type']=='img':
        man.append(f'''<div class="m">
  <a class="mimg" href="{RAW}{i}_story.jpg" data-lb="img/{i}_story.jpg" target="_blank" rel="noopener"><img src="img/{i}_story.jpg" alt="صورة الستوري" loading="lazy"></a>
  <div class="mbody"><div class="mh"><span class="day">{p['day']}</span> <span class="date">{p['date']}</span> · <span class="num">{p['time']}</span></div>
  <div class="plats"><span class="man">سناب</span><span class="man">حالة واتساب</span></div>
  <pre class="cap" id="m-{i}">{e(p['st'])}</pre>
  <div class="mb"><button type="button" data-copy="m-{i}">نسخ النص</button><a class="btn" href="{RAW}{i}_story.jpg" target="_blank" rel="noopener">فتح الصورة لحفظها</a></div></div>
</div>''')
        media=f'''<div class="plats"><span class="auto">إكس · تلقائي</span><span class="man">سناب · يدوي</span><span class="man">حالة واتساب · يدوي</span><span class="tag">{p['tag']}</span></div>
  <div class="imgs"><a href="{RAW}{i}_post.jpg" data-lb="img/{i}_post.jpg" target="_blank" rel="noopener"><img src="img/{i}_post.jpg" alt="تصميم المنشور" loading="lazy"><span>إكس 4:5</span></a><a href="{RAW}{i}_story.jpg" data-lb="img/{i}_story.jpg" target="_blank" rel="noopener"><img src="img/{i}_story.jpg" alt="تصميم الستوري" loading="lazy"><span>ستوري 9:16</span></a></div>'''
        story=f'<h3>نص الستوري</h3><pre class="cap" id="s-{i}">{e(p["st"])}</pre><button type="button" data-copy="s-{i}">نسخ النص</button>'
    else:
        media=f'''<div class="plats"><span class="auto">تيك توك · تلقائي</span><span class="tag">فيديو</span></div>
  <div class="vid"><video controls playsinline preload="none" poster="img/{i}_cover.jpg" src="img/{i}.mp4"></video><a href="{RAW}{i}.mp4" target="_blank" rel="noopener">فتح الفيديو لحفظه</a></div>'''
        story=''
    src=''.join(f'<li>{e(s)}</li>' for s in p['src'])
    allp.append(f'''<article class="post" id="{i}">
  <header><div><span class="day">{p['day']}</span> <span class="date">{p['date']}</span></div><span class="time num">{p['time']}</span></header>
  {media}
  <h3>نص المنشور</h3><pre class="cap" id="c-{i}">{e(p['cap'])}</pre><button type="button" data-copy="c-{i}">نسخ النص</button>
  {story}
  <h3>المصادر</h3><ul class="src">{src}</ul>
</article>''')
body=f'''<div class="wrap" dir="rtl" lang="ar">
  <div><h1>مراجعة منشورات الجمعية</h1><p class="lead">{LABEL} · بانتظار الاعتماد · {len(P)} منشورات · حسابات الجمعية العادية</p></div>
  <section class="manual" id="manual"><h2>للنشر اليدوي: سناب وحالة واتساب</h2>
  {''.join(man)}</section>
  <h2 class="sec">منشورات الأسبوع</h2>
  {''.join(allp)}
</div>
'''
import os; os.makedirs('review',exist_ok=True); open('review/index.html','w').write(head+body+tail)
print(len(head+body+tail))
