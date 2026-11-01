import asyncio,os,json
from playwright.async_api import async_playwright
TEAL="#105C63";DARK="#0B4248";GOLD="#B9A050";GREEN="#5A8F3C"
import sys
WEEK=sys.argv[1]
posts=[p for p in json.load(open(f'agent/weeks/{WEEK}.json')) if p.get('type')!='vid']
def post_html(p):
    tag=p['tag']; 
    if p['kind']=='project':
        inner=f'''<div class="k" style="font-size:66px;color:{TEAL};line-height:1.3">{p['title']}</div>
<div style="font-size:34px;line-height:1.75;color:#16292B">{p['body']}</div>
<div style="margin-top:16px;background:#E9EDEF;border-radius:18px;padding:22px;text-align:center;font-size:34px;font-weight:700;color:{GREEN}">{p['cta']}</div>'''
    else:
        lead=f'<div class="n" style="font-size:40px;color:{GREEN};font-weight:700">{p["lead"]}</div>' if p.get('lead') else ''
        inner=f'''{lead}<div class="n" style="font-size:{p.get('fs',50)}px;line-height:1.85;color:#16292B">{p['text']}</div>
<div style="font-size:30px;color:#6B7B7D;font-weight:600">{p['ref']}</div>'''
    return f'''<html><head><meta charset=utf-8><style>
*{{margin:0;box-sizing:border-box}}body{{width:1080px;height:1350px;position:relative;direction:rtl;font-family:'IBM Plex Sans Arabic'}}
.k{{font-family:'Reem Kufi';font-weight:700}}.n{{font-family:'Amiri'}}
</style></head><body><img src="base_post.jpg" style="position:absolute;inset:0;width:1080px;height:1350px">
<div style="position:absolute;left:80px;right:80px;top:430px">
<div style="width:100%;min-height:510px;background:#fff;border-radius:28px;padding:0 42px 46px 42px;display:flex;flex-direction:column;gap:18px">
<div style="align-self:flex-start;margin-right:-30px;background:#949C9E;color:#fff;font-size:36px;padding:8px 30px;margin-top:12px">{tag}</div>
{inner}</div></div></body></html>'''
def pillars():
    xs=[83,197,312,426,540,655,769,884,998];tops=[1100,980,930,980,930,930,980,930,1100]
    return ''.join(f'<div style="position:absolute;left:{x-37}px;top:{t}px;width:75px;height:{1750-t}px;border-radius:38px;background:#164B51"></div>' for x,t in zip(xs,tops))
def story_html(p):
    return f'''<html><head><meta charset=utf-8><style>
*{{margin:0;box-sizing:border-box}}body{{width:1080px;height:1920px;position:relative;direction:rtl;font-family:'IBM Plex Sans Arabic';background:{DARK};overflow:hidden}}
.k{{font-family:'Reem Kufi';font-weight:700}}.n{{font-family:'Amiri'}}
</style></head><body>{pillars()}
<img src="story_top.png" style="position:absolute;top:0;left:0;width:1080px">
<img src="story_foot.png" style="position:absolute;bottom:0;left:0;width:1080px">
<div style="position:absolute;top:330px;left:0;right:0;display:flex;flex-direction:column;align-items:center;gap:40px">
<div style="background:{GOLD};color:{DARK};font-weight:700;font-size:36px;padding:8px 34px;border-radius:999px">{p['pill']}</div>
<div class="k" style="font-size:66px;color:#D9C68A">{p['stitle']}</div></div>
<div style="position:absolute;top:760px;left:90px;right:90px;text-align:center;display:flex;flex-direction:column;gap:30px">
<div class="n" style="font-size:{p.get('sfs',60)}px;line-height:1.75;color:#fff">{p['stext']}</div>
<div style="font-size:32px;color:#D9C68A">{p.get('sref','')}</div></div>
</body></html>'''
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(); pg=await b.new_page()
        base='file://'+os.path.abspath('agent/assets')+'/'
        for p in posts:
            for kind,w,h,fn in [('post',1080,1350,post_html),('story',1080,1920,story_html)]:
                open('agent/assets/t.html','w').write(fn(p)); await pg.set_viewport_size({'width':w,'height':h})
                await pg.goto(base+'t.html'); await pg.wait_for_timeout(250)
                await pg.screenshot(path=f"posts/{WEEK}/{p['id']}_{kind}.jpg",type='jpeg',quality=92)
        await b.close()
os.makedirs(f'posts/{WEEK}',exist_ok=True); asyncio.run(main())
