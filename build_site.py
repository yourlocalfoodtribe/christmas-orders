import json, os, html

BASE = r"C:\Users\Tricia\AppData\Local\hermes\cache\scratch\looma"
SITE = os.path.join(BASE, "site")
manifest = json.load(open(os.path.join(SITE, "manifest.json"), encoding="utf-8"))

# --- FEATURE FLAGS -------------------------------------------------------
# Tee's one-switch panel: flip any of these to False and rebuild the site to
# turn that feature off. No other edits needed.
FLAGS = {
    "og": True,         # Facebook/messenger link preview card (image + title when the link is shared)
    "hero": True,       # big cake photo banner under the title
    "filters": True,    # All / Gluten free / Vegan / Dairy free chips
    "bottompad": True,  # extra space at the bottom so the floating order bar covers nothing
    "favicon": True,    # little cake icon in the browser tab
    "faq": True,        # quick-answers questions at the bottom
    "snow": True,       # falling snowflakes (Christmas feel) - turn off any time
    "banner": True,     # slim top banner: Monday/Tuesday delivery to North Brisbane
    "visits": True,     # anonymous visitor counter: unique browser IDs pinged to the tally script
}
HERO_IMG = "LOC6WHOLE.jpg"   # hero banner photo - swap the filename to change the picture
FAMILY_PCT = 15              # family discount percent (hidden link ?fam=1 activates it) - set to 0 to disable

# customer-facing (brandless) catalogue
ITEMS = [
    # GF section
    {"sku": "LOC3WHOLE", "name": "Vanilla & Raspberry Cake", "gf": True, "price": 119.95, "slice_price": 12.50, "unit": "whole 10-slice cake", "img": "LOC3WHOLE_LOCAL.jpg",
     "desc": "The flagship: vanilla bean mousse with raspberry.GF as labelled by the maker. Their most-loved GF cake."},
    {"sku": "LOC6", "name": "Vegan Chocolate Mud Cake", "gf": True, "df": True, "vg": True, "price": 119.95, "slice_price": 12.50, "unit": "whole 10-slice cake", "img": "LOC6WHOLE.jpg",
     "desc": "Gluten free, vegan AND dairy free. The one that covers every allergy at the table. 26 five-star reviews of this cake."},
    {"sku": "LOC8", "name": "Raffaello Cake", "gf": True, "price": 119.95, "slice_price": 13.95, "unit": "whole cake, pre-cut into 10", "img": "LOC8.jpg",
     "desc": "Coconut and white chocolate, factory pre-cut into 10 so it's dessert-table ready. Sealed original box."},
    {"sku": "MHBHBROW03", "name": "Espresso & Hazelnut Brownie", "gf": True, "piece": True, "deal4": 25.00, "price": 6.95, "img": "MHBHBROW03.jpg",
     "desc": "Deep, rich, gluten free. Always a crowd favourite on platters."},
    {"sku": "MHBHBROW07", "name": "Triple Choc Brownie", "gf": True, "piece": True, "deal4": 25.00, "price": 6.95, "img": "MHBHBROW07.jpg",
     "desc": "Triple chocolate, gluten free. Always the first to go on a platter.", "altbuy": None},
    {"sku": "LOCMINIFRIAND", "name": "Mini Friands", "gf": True, "price": 5.25, "unit": "piece", "img": "LOCMINIFRIAND.jpg",
     "desc": "Almond, lemon, blueberry, strawberry, pistachio and passionfruit. The morning-tea box.", "altbuy": None},
    {"sku": "LOCMAC7", "name": "Macarons", "gf": True, "piece": True, "deal7": 33.00, "price": 5.00, "img": "MACARONS.jpg",
     "desc": "Assorted French macarons - chocolate, lemon, salted caramel, raspberry & vanilla. Gluten free.", "altbuy": None},
    # Everyone else
    {"sku": "LOC9WHOLE", "name": "Ferrero Rocher Cake", "gf": False, "price": 129.95, "slice_price": 13.50, "unit": "whole 10-slice cake", "img": "LOC9WHOLE.jpg",
     "desc": "The showpiece. Their most reviewed cake of all time, and the Christmas centrepiece."},
    {"sku": "LOC7", "name": "Baked Ricotta Cheesecake", "gf": False, "price": 119.95, "unit": "whole 10-slice cake", "img": "LOC7WHOLE.jpg",
     "desc": "Cinnamon base, soft ricotta centre, crumbly top. A perfect 5.0 from every reviewer.", "altbuy": None},
    {"sku": "LOC1", "name": "New York Cheesecake", "gf": False, "price": 119.95, "unit": "whole 10-slice cake", "img": "LOC1.jpg",
     "desc": "Crumbling biscuit base, creamy white chocolate filling. Another perfect 5.0.", "altbuy": None},
    {"sku": "LOC16WHOLE", "name": "Tiramisu Cake", "gf": False, "price": 119.95, "unit": "whole 10-slice cake", "img": "LOC16WHOLE.jpg",
     "desc": "Coffee, cream, and a light sponge. 'O M G, absolutely divine' per a very recent review.", "altbuy": None},
    # Tarts ($8 each / $39.95 box of 6)
    {"sku": "LOCTA3", "name": "Lemon Tart", "gf": False, "tart": True, "fam": 10, "img": "LOCTA3.jpg", "desc": "Zesty, sharp, the palate cleanser of the platter."},
    {"sku": "LOCTA6", "name": "Berry Almond Tart", "gf": False, "tart": True, "fam": 10, "img": "LOCTA6.jpg", "desc": "Berries and almond, a perfect 5.0 from every reviewer."},
    {"sku": "LOCTA8", "name": "Caramel Walnut Tart", "gf": False, "tart": True, "fam": 10, "img": "LOCTA8.jpg", "desc": "Sticky caramel and walnut. Christmas table material."},
    {"sku": "LOCTA10", "name": "Biscoff Tart", "gf": False, "tart": True, "fam": 10, "img": "LOCTA10.jpg", "desc": "Biscoff. No further explanation needed."},
    {"sku": "LOCTA5", "name": "Apple Crumble Tart", "gf": False, "tart": True, "fam": 10, "img": "LOCTA5.jpg", "desc": "Warm apple crumble flavours in a little tart."},
    {"sku": "LOCTA9", "name": "Basque Cheesecake Tart", "gf": False, "tart": True, "fam": 10, "img": "LOCTA9.jpg", "desc": "Burnt-top Basque cheesecake. Highly recommended by gift buyers."},
    # Platter pieces
    {"sku": "MHBHBROW09", "name": "Nutella Brownie", "gf": False, "piece": True, "deal4": 30.00, "price": 7.95, "img": "MHBHBROW09.jpg", "desc": "The indulgent one."},
    {"sku": "MHBHBROW11", "name": "White Choc Macadamia Brownie", "gf": False, "piece": True, "deal4": 25.00, "price": 6.95, "img": "MHBHBROW11.jpg", "desc": "Blondie-style, white choc and macadamia."},
    {"sku": "MHBHSLICE01", "name": "Caramel & Macadamia Crumble", "gf": False, "piece": True, "deal4": 25.00, "price": 6.75, "img": "MHBHSLICE01.jpg", "desc": "Caramel, macadamia, crumble top. Dangerous."},
    # Bars, balls & bites (all gluten free as labelled by the maker; all dairy free except babycakes)
    {"sku": "MHBHSLICE09", "name": "Fig & Seed Vegan Slice", "gf": True, "df": True, "vg": True, "piece": True, "deal4": 25.00, "price": 6.95, "img": "MHBHSLICE09.jpg",
     "desc": "Dates, figs, sultanas, nuts and seeds baked with maple syrup. Gluten free, dairy free and vegan."},
    {"sku": "MHBHBAR02", "name": "Raw Cacao Bar", "gf": True, "df": True, "vg": True, "piece": True, "deal4": 24.00, "price": 6.50, "img": "MHBHBAR02.jpg",
     "desc": "Dates, almonds, chia and cacao nibs, naturally sweetened. Gluten free, dairy free, vegan."},
    {"sku": "MHBHBAR01", "name": "Raw Breakfast Bar", "gf": True, "df": True, "vg": True, "piece": True, "deal4": 24.00, "price": 6.50, "img": "MHBHBAR01.jpg",
     "desc": "Apricots, cranberries, hazelnuts and seeds with a sharp, not-too-sweet flavour. Gluten free, dairy free, vegan."},
    {"sku": "NBSBCOATPBC", "name": "Peanut Butter & Choc Protein Ball", "gf": True, "df": True, "vg": True, "piece": True, "fam": 20, "deal4": 22.00, "price": 5.95, "img": "NBSBCOATPBC.jpg",
     "desc": "Fudgy chocolate with crunchy peanut pieces. Gluten free, dairy free, vegan."},
    {"sku": "NBSBPB", "name": "Peanut Butter Protein Ball", "gf": True, "df": True, "vg": True, "piece": True, "fam": 20, "deal4": 18.00, "price": 4.95, "img": "NBSBPB.jpg",
     "desc": "Creamy peanut with dates and coconut. Gluten free, dairy free, vegan."},
    {"sku": "NBSBSC", "name": "Salted Caramel Protein Ball", "gf": True, "df": True, "vg": True, "piece": True, "fam": 20, "deal4": 18.00, "price": 4.95, "img": "NBSBSC.jpg",
     "desc": "Almonds, cashews and coconut with a salted caramel hit. Gluten free, dairy free, vegan."},
    {"sku": "MHBHCAKE01", "name": "Babycake (mini cupcake)", "gf": False, "piece": True, "fam": 20, "deal4": 15.00, "price": 4.50, "img": "MHBHCAKE01.jpg",
     "desc": "Mini cupcakes in vanilla and chocolate, piped with buttercream and finished with silver cachous."},
    # Pet treats (kept separate from all human food)
    {"sku": "HGMIX", "name": "Doggie Ice Cream (for dogs!)", "gf": True, "df": True, "pet": True, "piece": True, "fam": 20, "price": 9.95, "was": 11.95, "img": "HGMIX.jpg",
     "desc": "Coconut-milk based frozen treat for dogs, no dairy, no lactose. Flavours: Peanut Butter & Bacon, Strawberry, Carob. Pet treats only, kept separate from all human food. On special for Christmas."},
]

def card(it):
    img = "images/" + it["img"]
    gf_badge = ('<span class="gf">GF</span> ' if it.get("gf") else "") + ('<span class="df">DF</span>' if it.get("df") else "") + ('<span class="vg">VG</span>' if it.get("vg") else "") + ('<span class="pet">FOR DOGS ONLY</span>' if it.get("pet") else "")
    name = html.escape(it["name"])
    desc = html.escape(it["desc"])
    if it.get("tart"):
        tfam = it.get("fam", 15)
        buttons = (f'<button class="add" data-id="{it["sku"]}-s" data-name="{name} (single)" data-price="8.50" data-img="{img}" data-fam="{tfam}">Add single $8.50</button>'
                   f'<button class="add" data-id="{it["sku"]}-b" data-name="{name} box of 6" data-price="44.95" data-img="{img}" data-fam="10">Add box of 6 $44.95</button>')
        price_line = '<div class="price">$8.50 each &nbsp;|&nbsp; $44.95 box of 6</div>'
    elif it.get("piece") or (it.get("gf") and it["price"] < 10):
        if it.get("pet"):
            was = f'<span style="text-decoration:line-through; color:var(--muted); font-weight:400">${it["was"]:.2f}</span> &nbsp;' if it.get("was") else ""
            buttons = f'<button class="add" data-id="{it["sku"]}" data-name="{name}" data-price="{it["price"]:.2f}" data-img="{img}" data-fam="{it.get("fam", 15)}">Add a tub</button>'
            price_line = f'<div class="price">{was}<span style="color:var(--red)">${it["price"]:.2f}</span> per tub &nbsp;<span class="unit">single serve</span></div>'
        else:
            dp = it.get("deal4") or (18.00 if it["sku"] == "LOCMINIFRIAND" else 22.00)
            if it.get("deal7"):
                pk_n, pk_id, dp = 7, f'{it["sku"]}-pack7', it["deal7"]
            else:
                pk_n, pk_id = 4, f'{it["sku"]}-pack4'
            pack = f'<button class="add pack" data-id="{pk_id}" data-name="{name} {pk_n}-pack" data-price="{dp:.2f}" data-img="{img}" data-fam="{it.get("fam", 15)}">Add {pk_n} for ${dp:.2f}</button>'
            buttons = (f'<button class="add" data-id="{it["sku"]}" data-name="{name}" data-price="{it["price"]:.2f}" data-img="{img}" data-fam="{it.get("fam", 15)}">Add single</button>' + pack)
            price_line = f'<div class="price">${it["price"]:.2f} each &nbsp;|&nbsp; ${dp:.2f} for {pk_n}</div>'
    else:
        sp = it.get("slice_price")
        slice_btn = f'<button class="add" data-id="{it["sku"]}-slice" data-name="{name} slice" data-price="{sp:.2f}" data-img="{img}" data-fam="{it.get("fam", 15)}">Add a slice ${sp:.2f}</button>' if sp else ""
        buttons = (f'<button class="add" data-id="{it["sku"]}" data-name="{name} ({it["unit"]})" data-price="{it["price"]:.2f}" data-img="{img}" data-fam="{it.get("fam", 15)}">Add whole cake</button>' + slice_btn)
        price_line = f'<div class="price">${it["price"]:.2f} &nbsp;<span class="unit">{it["unit"]}</span></div>'
    alt = f'<div class="altbuy">{html.escape(it["altbuy"])}</div>' if it.get("altbuy") else ""
    tags = "".join(" " + t for t in ("gf", "df", "vg", "pet") if it.get(t))
    return f'''<div class="card" data-tags="{tags}">
      <img src="{img}" alt="{name}" loading="lazy" onerror="this.style.display='none'">
      <div class="card-body">
        <div class="cname">{name} {gf_badge}</div>
        <p>{desc}</p>
        {price_line}
        <div class="btns">{buttons}</div>
        {alt}
      </div>
    </div>'''

gf_cards = "\n".join(card(i) for i in ITEMS if i.get("gf"))
else_cards = "\n".join(card(i) for i in ITEMS if not i.get("gf") and not i.get("tart") and not i.get("piece"))
tart_cards = "\n".join(card(i) for i in ITEMS if i.get("tart"))
piece_cards = "\n".join(card(i) for i in ITEMS if i.get("piece"))

page = '''<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
__FAVICON__
__OG__
<title>Christmas Cakes &amp; Treats</title>
<style>
  :root{
    --green:#14532d; --green2:#1a6b38; --cream:#fdf9f3; --card:#ffffff;
    --gold:#b7791f; --red:#b91c1c; --ink:#243029; --muted:#6b7a70;
  }
  *{box-sizing:border-box; margin:0; padding:0}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; background:var(--cream); color:var(--ink); padding-bottom:110px}
  header{background:var(--green); color:#fff; text-align:center; padding:38px 16px 30px}
  header h1{font-family:Georgia,'Times New Roman',serif; font-size:clamp(1.7rem,4.5vw,2.6rem); letter-spacing:.5px}
  header .sub{margin-top:8px; font-size:1rem; color:#d9f2e2}
  .strip{display:flex; flex-wrap:wrap; gap:8px; justify-content:center; margin-top:18px; font-size:.85rem}
  .strip span{background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.25); padding:6px 12px; border-radius:999px}
  main{max-width:1100px; margin:0 auto; padding:26px 16px}
  h2{font-family:Georgia,serif; color:var(--green); font-size:clamp(1.7rem,3.5vw,2.3rem); margin:34px 0 10px}
  .sect-sub{color:var(--muted); font-size:.95rem; margin-bottom:14px}
  .gf-note{background:#ecfdf3; border:1px solid #bbe7cc; color:#14532d; padding:10px 14px; border-radius:10px; font-size:.9rem; margin-bottom:16px}
  .grid{display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:16px}
  .card{background:var(--card); border-radius:14px; overflow:hidden; box-shadow:0 2px 10px rgba(20,60,35,.08); display:flex; flex-direction:column}
  .card img{width:100%; aspect-ratio:4/3; object-fit:cover; background:#f0ede6}
  .card-body{padding:12px 14px 14px; display:flex; flex-direction:column; gap:8px; flex:1}
  .cname{font-weight:700; font-size:1.02rem}
  .gf{display:inline-block; background:var(--green2); color:#fff; font-size:.68rem; padding:2px 7px; border-radius:999px; vertical-align:middle; margin-left:6px; letter-spacing:1px}
  .df{display:inline-block; background:var(--gold); color:#fff; font-size:.68rem; padding:2px 7px; border-radius:999px; vertical-align:middle; margin-left:6px; letter-spacing:1px}
  .pet{display:inline-block; background:var(--red); color:#fff; font-size:.68rem; padding:2px 7px; border-radius:999px; vertical-align:middle; margin-left:6px; letter-spacing:1px}
  .vg{display:inline-block; background:#c79a00; color:#fff; font-size:.68rem; padding:2px 7px; border-radius:999px; vertical-align:middle; margin-left:6px; letter-spacing:1px}
  .card p{font-size:.86rem; color:var(--muted); flex:1}
  .price{font-weight:700; color:var(--green); font-size:1.05rem}
  .price .unit{font-weight:400; color:var(--muted); font-size:.8rem}
  .btns{display:flex; gap:8px; flex-wrap:wrap}
  button.add{background:var(--green); color:#fff; border:none; padding:9px 14px; border-radius:9px; font-size:.88rem; cursor:pointer; font-weight:600}
  button.add:hover{background:var(--green2)}
  .altbuy{font-size:.78rem; color:var(--gold)}
  .deal{background:#fff7ed; border:1px dashed var(--gold); border-radius:12px; padding:14px 16px; margin-top:16px; font-size:.95rem}
  .boxbuilder{background:#fff; border:2px solid var(--green); border-radius:16px; padding:20px; margin-top:24px}
  .boxbuilder h2{margin-top:0}
  .boxgrid{display:grid; grid-template-columns:repeat(auto-fill,minmax(230px,1fr)); gap:8px; margin:14px 0}
  .bitem{display:flex; align-items:center; justify-content:space-between; gap:6px; background:var(--cream); border:1px solid #e2ddd2; border-radius:10px; padding:6px 8px; font-size:.82rem}
  .bitem-gf{background:#f2faf5; border-color:#bbe7cc}
  .bthumb{width:42px; height:32px; object-fit:cover; border-radius:6px; flex-shrink:0; background:#f0ede6}
  .bname{flex:1; cursor:pointer}
  .bname:hover{text-decoration:underline}
  .card{scroll-margin-top:12px}
  @keyframes flashhl{0%{box-shadow:0 0 0 5px var(--gold)}100%{box-shadow:none}}
  .card.flash{animation:flashhl 1.8s ease-out}
  .bctrl{display:flex; align-items:center; gap:6px}
  .bctrl .q{width:26px; height:26px; border:1px solid var(--green); background:#fff; color:var(--green); border-radius:7px; cursor:pointer; font-weight:700; padding:0}
  .bctrl .bqty{min-width:18px; text-align:center; font-weight:700}
  .boxsummary{font-size:1rem; margin:12px 0}
  #addBox{background:var(--green); color:#fff; border:none; padding:12px 22px; border-radius:10px; font-size:1rem; font-weight:700; cursor:pointer}
  #addBox:disabled{background:#c9cfc9; cursor:not-allowed}
  .delivery{background:var(--green); color:#fff; border-radius:16px; padding:22px; margin-top:34px}
  .delivery h2{color:#fff; margin-top:0}
  .delivery ul{margin:10px 0 0 18px; line-height:1.7; font-size:.95rem}
  .cartbar{position:fixed; left:0; right:0; bottom:0; background:#fff; border-top:2px solid var(--gold); padding:7px 12px; box-shadow:0 -2px 10px rgba(0,0,0,.10); z-index:50}
  .cartbar .inner{max-width:1100px; margin:0 auto; display:flex; align-items:center; gap:10px; flex-wrap:wrap}
  .custfields{display:flex; flex-direction:row; gap:6px; min-width:0; flex:1 1 300px}
  .custfields input{padding:6px 9px; border:1.5px solid #d7dcd4; border-radius:8px; font-size:.85rem; width:100%; min-width:0}
  .custfields input:focus{outline:none; border-color:var(--green)}
  #cartSummary{flex:1; min-width:180px; font-size:.85rem}
  #cartSummary b{color:var(--green)}
  #copyOrder{background:var(--red); color:#fff; border:none; padding:8px 14px; border-radius:8px; font-size:.85rem; font-weight:700; cursor:pointer}
  #copyOrder:hover{filter:brightness(1.1)}
  .linkbtn{background:none; border:none; color:var(--gold); font-size:.8rem; cursor:pointer; padding:2px 0; text-decoration:underline}
  #cartPanel{background:#fff; border:2px solid var(--green); border-radius:12px; padding:12px; width:100%; max-height:260px; overflow-y:auto; font-size:.88rem}
  #cartPanel .pline{display:flex; align-items:center; gap:8px; padding:6px 0; border-bottom:1px solid #eee}
  #cartPanel .pname{flex:1}
  #cartPanel button.q{width:30px; height:30px; border:1px solid var(--green); background:#fff; color:var(--green); border-radius:7px; cursor:pointer; font-weight:700}
  #cartPanel button.x{border:1px solid var(--red); background:#fff; color:var(--red); border-radius:7px; width:34px; height:30px; cursor:pointer}
  #cartPanel .clearall{background:none; border:none; color:var(--muted); cursor:pointer; text-decoration:underline; font-size:.78rem; margin-top:6px}
  #orderText{display:none; width:100%; margin-top:10px; font-family:monospace; font-size:.8rem; padding:8px}
  .hint{font-size:.78rem; color:var(--ink)}
  #payPalBtn{background:none; border:none; padding:0; cursor:pointer}
  #payPalBtn img{height:34px; display:block}
  #payPalBtn:hover{filter:brightness(1.05)}
  #payIdBtn{background:#0a7d4e; color:#fff; border:none; padding:8px 14px; border-radius:8px; font-size:.85rem; font-weight:700; cursor:pointer}
  #payIdBtn:hover{filter:brightness(1.1)}
  footer{max-width:1100px; margin:30px auto 70px; padding:0 16px; color:var(--muted); font-size:.75rem; line-height:1.6}
  @media (max-width:560px){ .grid{grid-template-columns:repeat(auto-fill,minmax(160px,1fr))} }
  body.bottompad{padding-bottom:180px}
  .hero{display:block; width:100%; max-width:1100px; height:320px; object-fit:cover; object-position:center 35%; margin:0 auto}
  @media (max-width:560px){ .hero{height:200px} }
  .filters{max-width:1100px; margin:14px auto 0; padding:0 16px; display:flex; gap:8px; flex-wrap:wrap}
  .chip{border:1.5px solid var(--green); background:#fff; color:var(--green); border-radius:999px; padding:8px 18px; font-size:.88rem; font-weight:700; cursor:pointer}
  .chip.active{background:var(--green); color:#fff}
  .card.hide{display:none}
  .faq{max-width:1100px; margin:36px auto 0; padding:0 16px}
  .faq h2{margin-bottom:10px}
  .faq details{background:var(--cream); border:1px solid #e2ddd2; border-radius:12px; padding:12px 16px; margin-bottom:8px}
  .faq summary{cursor:pointer; font-weight:700; font-size:.95rem}
  .faq details p{margin:8px 0 0; font-size:.9rem; color:var(--ink); line-height:1.55}
  .topbanner{background:#1a7a3c; color:#fff; text-align:center; font-weight:800; font-size:1.02rem; padding:10px 12px; letter-spacing:.02em}
  .topbanner span{color:#ffe08a}
__SNOWCSS__
</style>
</head>
<body class="__BP__">
__BANNER__
<header>
  <h1>&#127876; Christmas Cakes &amp; Treats &#127876;</h1>
  <div class="sub">Order by Thursday 5pm &middot; delivered Monday or Tuesday &middot; or free pickup</div>
  <div class="strip">
    <span>&#127873; $12 delivered, FREE over $85</span>
    <span>&#10052; Order by Thursday 5pm for Monday/Tuesday delivery</span>
    <span>&#127856; Thaw 1 hour before serving</span>
  </div>
</header>
__HERO__
__FILTERS__
<main>
  <h2>&#127793; Gluten free, the real deal</h2>
  <div class="grid">
__GF_CARDS__
  </div>

  <h2>&#127856; For everyone else</h2>
  <div class="sect-sub">The showpieces. These are the cakes people write five-star reviews about.</div>
  <div class="grid">
__ELSE_CARDS__
  </div>

  <h2>&#127850; Mini tarts</h2>
  <div class="sect-sub">Buy singles for a mixed platter, or grab a sealed box of 6.</div>
  <div class="grid">
__TART_CARDS__
  </div>

  <h2>&#127854; Sweet platter bits</h2>
  <div class="sect-sub">Individual treats, perfect for platters and lunch boxes.</div>
  <div class="grid">
__PIECE_CARDS__
  </div>
  <div class="boxbuilder">
    <h2>&#127873; Build your own box</h2>
    <div class="sect-sub">Pick any 4, 6 or 10 pieces, mixed however you like &mdash; that's the premium way. $0.50 off every piece.</div>
    <div class="boxgrid" id="boxItems"></div>
    <div class="boxsummary" id="boxSummary">Pick 4, 6 or 10 pieces to start your box.</div>
    <button id="addBox" disabled>Add box to order</button>
  </div>

  <div class="delivery">
    <h2>&#128666; Delivery &amp; pickup</h2>
    <ul>
      <li><b>$12 delivered to your door</b> &mdash; or <b>free on orders over $85</b></li>
      <li><b>Free delivery for registered Fruit &amp; Veg members</b> &mdash; on the Tuesday run. Type <b>MEMBER</b> then your street at checkout</li>
      <li><b>Orders close Thursday 5pm</b> &middot; delivered <b>Monday or Tuesday</b> on our run</li>
      <li><b>Free pickup from Taigum Square</b> &mdash; we'll send you the details when you order</li>
      <li><b>We deliver to:</b> Nundah, Wavell Heights, Chermside, Boondall, Virginia, Geebung, Zillmere, Taigum, Fitzgibbon, Bracken Ridge, Deagon, Sandgate, Shorncliffe, Brighton, Aspley &amp; Carseldine</li>
      <li><b>PayID button</b> in the order bar at checkout</li>
      <li>Everything arrives <b>frozen or refrigerated</b>: into the fridge when it reaches you, keeps 5&ndash;7 days, out of the fridge 1 hour before serving</li>
    </ul>
  </div>
</main>

<div class="cartbar">
  <div class="inner">
    <div>
      <div id="cartSummary">Your order is empty &mdash; tick a few things and they'll show here &#127876;</div>
      <button id="editCart" style="display:none" class="linkbtn">&#9998; View / change your order</button>
    </div>
    <div id="cartPanel" style="display:none"></div>
    <div class="custfields">
      <input id="custName" type="text" placeholder="Your name" autocomplete="name">
      <input id="custAddr" type="text" placeholder="Delivery address (or PICKUP / MEMBER + your street)" autocomplete="street-address">
    </div>
    <button id="copyOrder">Copy my order</button>
    <button id="payIdBtn">Copy PayID</button>
    <button id="payPalBtn" type="button"><img src="https://www.paypalobjects.com/webstatic/en_US/i/buttons/checkout-logo-large.png" alt="Check out with PayPal or card" title="Pay by card or PayPal"></button>
    <textarea id="orderText" rows="3"></textarea>
    <span class="hint">Pay by card or PayPal, or tap <b>Copy PayID</b> to pay free via PayID.</span>
  </div>
</div>

<div id="payModal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,.55); z-index:100; align-items:center; justify-content:center; padding:16px">
  <div style="background:#fff; border-radius:16px; max-width:540px; width:100%; padding:22px; max-height:80vh; overflow-y:auto">
    <h3 style="margin-top:0">Thank you &mdash; your payment went through &#127881;</h3>
    <p style="font-size:.95rem; line-height:1.55">One last thing so we know exactly what to bring you: <b>send us your order</b>. Copy it below and comment it on our post, send it to us in Messenger, or email it.</p>
    <pre id="pmText" style="background:var(--cream); border:1px solid #e2ddd2; border-radius:10px; padding:10px; font-family:monospace; font-size:.8rem; max-height:200px; overflow:auto; white-space:pre-wrap"></pre>
    <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:12px">
      <button id="pmCopy" style="background:var(--red); color:#fff; border:none; padding:10px 16px; border-radius:9px; font-size:.9rem; font-weight:700; cursor:pointer">Copy my order</button>
      <a id="pmMail" style="background:var(--green); color:#fff; padding:10px 16px; border-radius:9px; font-size:.9rem; font-weight:700; text-decoration:none">Email my order</a>
      <button onclick="document.getElementById('payModal').style.display='none'" style="background:none; border:1px solid var(--muted); color:var(--muted); padding:10px 14px; border-radius:9px; font-size:.9rem; cursor:pointer">Close</button>
    </div>
  </div>
</div>
<div id="payBanner" style="display:none; position:fixed; top:0; left:0; right:0; background:var(--red); color:#fff; padding:8px 14px; font-size:.88rem; z-index:90; text-align:center">
  You paid by PayPal but we have not received your order yet &mdash; <a href="#" onclick="payModalOpen(); return false" style="color:#fff; font-weight:700; text-decoration:underline">send us your order</a>
</div>
__FAQ__

<footer>
  Gluten free items are gluten free as labelled by their maker. All items arrive frozen or refrigerated in original packaging. Keep refrigerated after thawing, 5&ndash;7 days. Product photos are of the exact items we supply.
</footer>

<script>
var cart = {};
var PIECE_IDS = ["MHBHBROW03","MHBHBROW07","MHBHBROW09","MHBHBROW11","MHBHSLICE01"];
var PIECE_PRICES = {"MHBHBROW03":6.95,"MHBHBROW07":6.95,"MHBHBROW09":7.95,"MHBHBROW11":6.95,"MHBHSLICE01":6.75};
var FRIAND_IDS = ["LOCMINIFRIAND"];
var FRIAND_PRICES = {"LOCMINIFRIAND":5.25};

var TALLY_URL = "https://script.google.com/macros/s/AKfycbzlDlCVP0uprvSfGLG1kxItBQLXt4Xz9ZSP3E338JxaXQ2ymYT6gVKY2ygs-gDRPZcW/exec";
__VISITS__

function money(n){ return "$" + n.toFixed(2); }

function bump(id, delta){
  if (!cart[id]) return;
  cart[id].qty += delta;
  if (cart[id].qty <= 0) delete cart[id];
  render();
}
function removeLine(id){ delete cart[id]; render(); }
function clearAll(){ cart = {}; render(); }

document.querySelectorAll("button.add").forEach(function(b){
  b.addEventListener("click", function(){
    var id = b.dataset.id;
    cart[id] = cart[id] || {name: b.dataset.name, price: parseFloat(b.dataset.price), qty: 0, img: b.dataset.img, fam: parseFloat(b.dataset.fam || "15")};
    cart[id].qty++;
    render();
  });
});

function render(){
  var keys = Object.keys(cart).filter(function(k){ return cart[k].qty > 0; });
  var lines = [];
  var subtotal = 0, pieces = 0, fullPricePieces = 0;
  keys.forEach(function(k){
    var it = cart[k];
    var unit = it.price;
    var isPiece = PIECE_IDS.indexOf(k) >= 0 || k.indexOf("MHBHBROW") === 0 || k === "MHBHSLICE01";
    if (isPiece) { pieces += it.qty; }
    subtotal += unit * it.qty;
    lines.push({k:k, it:it, unit:unit});
  });
  // no auto mix-and-match discount — mixing happens in the box builder
  var saved = 0;
  var delivery = 0;
  var addr = (document.getElementById("custAddr").value || "").trim();
  var cname = (document.getElementById("custName").value || "").trim();
  var delLabel = "pickup (free)";
  var famPct = 15; // per-line tiers override this (fam field on each line)
  var famOff = 0;
  var famActive = false;
  try { famActive = localStorage.getItem("ylft_fam") === "1"; } catch(e){}
  if (famActive && subtotal > 0){
    keys.forEach(function(k){
      var it = cart[k];
      famOff += (it.famOff !== undefined) ? it.famOff : (it.price * it.qty * (it.fam === undefined ? 15 : it.fam) / 100);
    });
    famOff = Math.round(famOff * 100) / 100;
  }
  var itemsTotal = Math.max(0, subtotal - famOff);
  window.__famOff = famOff;
  if (subtotal > 0){
    var aU = addr.toUpperCase();
    var isMember = aU.indexOf("MEMBER") === 0;
    var memberAddr = isMember ? addr.slice(6).replace(/^[\s,:-]+/, "").trim() : "";
    if (isMember){
      if (memberAddr){ delLabel = "FREE delivery - Fruit & Veg member (Tuesday run) to: " + memberAddr; }
      else { delLabel = "MEMBER delivery - add your street after MEMBER"; }
    } else if (addr && aU !== "PICKUP"){
      if (itemsTotal >= 85){ delLabel = "DELIVERY FREE (over $85) to: " + addr; }
      else { delivery = 12; delLabel = "delivery +$12 (free over $85) to: " + addr; }
    } else {
      delLabel = "pickup (free)";
    }
  }
  var total = itemsTotal + delivery;
  window.__total = total;
  var DELIVERY_SUBURBS = ["nundah","wavell heights","chermside","boondall","virginia","geebung","zillmere","taigum","fitzgibbon","bracken ridge","deagon","sandgate","shorncliffe","brighton","aspley","carseldine"];
  var addrKnown = !addr || aU.indexOf("MEMBER") === 0 || aU === "PICKUP" || DELIVERY_SUBURBS.some(function(s){ return addr.toLowerCase().indexOf(s) > -1; });
  window.__addrKnown = addrKnown;
  window.__payFee = (total > 0) ? Math.round((total * 0.026 + 0.30) * 100) / 100 : 0;
  window.__shortSummary = ((cname ? "for " + cname + ": " : "") + lines.map(function(l){ return l.it.qty + "x " + l.it.name; }).join("; ")).slice(0, 100);
  var el = document.getElementById("cartSummary");
  var editBtn = document.getElementById("editCart");
  if (!keys.length){
    el.innerHTML = "Your order is empty &mdash; tick a few things and they'll show here &#127876;";
    editBtn.style.display = "none";
    document.getElementById("cartPanel").style.display = "none";
  } else {
    editBtn.style.display = "inline";
    var txt = lines.map(function(l){ return l.it.qty + "x " + l.it.name + " = " + money(l.unit * l.it.qty); }).join(" &middot; ");
    el.innerHTML = txt + "<br><b>Order: " + money(itemsTotal) + "</b>" + (famOff > 0 ? ' <span style="color:var(--green); font-size:.85rem">&#127872; family discount &minus;' + money(famOff) + '</span>' : "")
      + " &nbsp; " + delLabel + " &nbsp; <b>Total: " + money(total) + "</b>"
      + (keys.some(function(k){ return cart[k].name.indexOf("(for dogs!)") > -1; }) ? '<br><span style="font-size:.85rem; color:var(--red)">&#128021; Doggie treats are packed separately from all human treats.</span>' : "")
      + (window.__payFee > 0 ? '<br><span style="font-size:.85rem">Paying by card or PayPal adds ' + money(window.__payFee) + ' processing fee &mdash; <b>free with PayID</b></span>' : "")
      + (!addrKnown && subtotal > 0 ? '<br><span style="font-size:.85rem; color:var(--red)">&#9888; Your address does not look like one of our delivery suburbs (see Quick answers). We will confirm before the run &mdash; or type PICKUP for free pickup from Taigum Square.</span>' : "");
  }
  buildOrderText(keys, itemsTotal, saved, delivery, delLabel, total);
  renderPanel(keys, saved);
}

function renderPanel(keys, saved){
  var p = document.getElementById("cartPanel");
  if (p.style.display === "none") return;
  var h = "";
  keys.forEach(function(k){
    var it = cart[k];
    h += '<div class="pline"><span class="pname">' + it.qty + ' &times; ' + it.name + '</span>'
      + '<button class="q" onclick="bump(\\'' + k + '\\',-1)">&minus;</button>'
      + '<button class="q" onclick="bump(\\'' + k + '\\',1)">+</button>'
      + '<button class="x" onclick="removeLine(\\'' + k + '\\')" title="Remove">&times;</button></div>';
  });
  h += '<button class="clearall" onclick="clearAll()">Remove everything</button>';
  p.innerHTML = h;
}

document.getElementById("editCart").addEventListener("click", function(){
  var p = document.getElementById("cartPanel");
  p.style.display = (p.style.display === "none") ? "block" : "none";
  render();
});

function buildOrderText(keys, subtotal, saved, delivery, delLabel, total){
  var cname = (document.getElementById("custName").value || "").trim();
  var addr = (document.getElementById("custAddr").value || "").trim();
  var t = "CHRISTMAS ORDER\\n";
  if (cname) t += "Name: " + cname + "\\n";
  if (addr) t += "Delivery address: " + addr + "\\n";
  keys.forEach(function(k){
    var it = cart[k];
    t += "- " + it.qty + " x " + it.name + " (" + money(it.price) + " each)\\n";
  });
  if (window.__payFee > 0) {
    t += "Card/PayPal payment adds " + money(window.__payFee) + " processing fee (free with PayID)\\n";
    t += "Card/PayPal total: " + money(window.__total + window.__payFee) + "\\n";
  }
  if (window.__famOff > 0){
    t += "Family discount applied: -" + money(window.__famOff) + "\\n";
  }
  t += "Order total: " + money(subtotal) + "\\n";
  var aU2 = (addr || "").toUpperCase();
  var pref;
  if (aU2.indexOf("MEMBER") === 0){
    var mAddr = addr.slice(6).replace(/^[\s,:-]+/, "").trim();
    pref = mAddr ? ("DELIVER to " + mAddr + " (Fruit & Veg member - free Tuesday run)") : "MEMBER delivery (street address missing)";
  } else if (addr && aU2 !== "PICKUP"){ pref = "DELIVER to " + addr; }
  else { pref = "PICKUP"; }
  t += "Delivery preference: " + pref + "\\n";
  t += "Total with delivery: " + money(total) + "\\n";
  var ta = document.getElementById("orderText");
  ta.value = t;
  window.__orderText = t;
}

document.getElementById("copyOrder").addEventListener("click", function(){
  var ta = document.getElementById("orderText");
  ta.style.display = "block";
  ta.value = window.__orderText || "";
  ta.select();
  try { document.execCommand("copy"); } catch(e){}
  if (navigator.clipboard && window.__orderText){ navigator.clipboard.writeText(window.__orderText).catch(function(){}); }
  // background tally for admin (fires when TALLY_URL is set)
  if (TALLY_URL && window.__orderText){
    try {
      fetch(TALLY_URL, {method:"POST", mode:"no-cors", headers:{"Content-Type":"text/plain;charset=utf-8"}, body: window.__orderText}).catch(function(){});
    } catch(e){}
  }
  this.textContent = "Copied! Paste it to us";
  var btn = this;
  setTimeout(function(){ btn.textContent = "Copy my order"; }, 2500);
});

document.getElementById("payIdBtn").addEventListener("click", function(){
  if (navigator.clipboard){ navigator.clipboard.writeText("yourfoodtribe@gmail.com").catch(function(){}); }
  this.textContent = "PayID copied! Pay in your bank app";
  var btn = this;
  setTimeout(function(){ btn.textContent = "Copy PayID"; }, 2500);
});

document.getElementById("payPalBtn").addEventListener("click", function(){
  var keys = Object.keys(cart).filter(function(k){ return cart[k].qty > 0; });
  if (!keys.length){ alert("Add some treats to your order first!"); return; }
  // log the full order to the tally sheet BEFORE they leave for PayPal
  if (TALLY_URL && window.__orderText){
    try {
      fetch(TALLY_URL, {method:"POST", mode:"no-cors", headers:{"Content-Type":"text/plain;charset=utf-8"}, body: window.__orderText}).catch(function(){});
    } catch(e){}
  }
  try { localStorage.setItem("ylft_pending_order", JSON.stringify({txt: window.__orderText, ts: Date.now()})); } catch(e){}
  // copy the order text so they can paste it to us after paying
  var ta = document.getElementById("orderText");
  ta.style.display = "block";
  ta.value = window.__orderText || "";
  ta.select();
  try { document.execCommand("copy"); } catch(e){}
  if (navigator.clipboard && window.__orderText){ navigator.clipboard.writeText(window.__orderText).catch(function(){}); }
  var form = document.createElement("form");
  form.method = "POST";
  form.action = "https://www.paypal.com/cgi-bin/webscr";
  form.target = "_blank";
  var fields = {
    cmd: "_xclick",
    business: "yourfoodtribe@gmail.com",
    item_name: ("Christmas order: " + window.__shortSummary),
    amount: (window.__total + window.__payFee).toFixed(2),
    currency_code: "AUD",
    no_shipping: "2",
    rm: "1",
    return: "https://yourlocalfoodtribe.github.io/christmas-orders/",
    charset: "utf-8"
  };
  for (var f in fields){
    var inp = document.createElement("input");
    inp.type = "hidden";
    inp.name = f;
    inp.value = fields[f];
    form.appendChild(inp);
  }
  document.body.appendChild(form);
  form.submit();
});

// ---- Build your own box ----
var BOX_PIECES = [
  {n:"Vanilla & Raspberry Slice", p:12.00, gf:1, img:"LOC3WHOLE_LOCAL.jpg"},
  {n:"Vegan Chocolate Mud Slice", p:12.00, gf:1, df:1, vg:1, img:"LOC6WHOLE.jpg"},
  {n:"Raffaello Slice", p:13.95, gf:1, img:"LOC8.jpg"},
  {n:"Espresso & Hazelnut Brownie", p:6.95, gf:1, img:"MHBHBROW03.jpg"},
  {n:"Triple Choc Brownie", p:6.95, gf:1, img:"MHBHBROW07.jpg"},
  {n:"Mini Friands", p:5.25, gf:1, img:"LOCMINIFRIAND.jpg"},
  {n:"Macarons", p:5.00, gf:1, img:"MACARONS.jpg"},
  {n:"Raw Cacao Bar", p:6.50, gf:1, df:1, vg:1, img:"MHBHBAR02.jpg"},
  {n:"Raw Breakfast Bar", p:6.50, gf:1, df:1, vg:1, img:"MHBHBAR01.jpg"},
  {n:"Peanut Butter & Choc Protein Ball", p:5.95, gf:1, df:1, fam:20, vg:1, img:"NBSBCOATPBC.jpg"},
  {n:"Peanut Butter Protein Ball", p:4.95, gf:1, df:1, fam:20, vg:1, img:"NBSBPB.jpg"},
  {n:"Salted Caramel Protein Ball", p:4.95, gf:1, df:1, fam:20, vg:1, img:"NBSBSC.jpg"},
  {n:"Fig & Seed Vegan Slice", p:6.95, gf:1, df:1, vg:1, img:"MHBHSLICE09.jpg"},
  {n:"Doggie Ice Cream (for dogs!)", p:9.95, gf:1, df:1, fam:20, pet:1, img:"HGMIX.jpg"},
  {n:"Ferrero Rocher Slice", p:13.00, gf:0, img:"LOC9WHOLE.jpg"},
  {n:"Baked Ricotta Slice", p:12.00, gf:0, img:"LOC7WHOLE.jpg"},
  {n:"New York Cheesecake Slice", p:12.00, gf:0, img:"LOC1.jpg"},
  {n:"Tiramisu Slice", p:12.00, gf:0, img:"LOC16WHOLE.jpg"},
  {n:"Nutella Brownie", p:7.95, gf:0, img:"MHBHBROW09.jpg"},
  {n:"White Choc Macadamia Brownie", p:6.95, gf:0, img:"MHBHBROW11.jpg"},
  {n:"Caramel & Macadamia Crumble", p:6.75, gf:0, img:"MHBHSLICE01.jpg"},
  {n:"Lemon Tart", p:8.50, fam:10, gf:0, img:"LOCTA3.jpg"},
  {n:"Berry Almond Tart", p:8.50, fam:10, gf:0, img:"LOCTA6.jpg"},
  {n:"Caramel Walnut Tart", p:8.50, fam:10, gf:0, img:"LOCTA8.jpg"},
  {n:"Biscoff Tart", p:8.50, fam:10, gf:0, img:"LOCTA10.jpg"},
  {n:"Apple Crumble Tart", p:8.50, fam:10, gf:0, img:"LOCTA5.jpg"},
  {n:"Basque Cheesecake Tart", p:8.50, fam:10, gf:0, img:"LOCTA9.jpg"},
  {n:"Babycake (mixed flavours)", fam:20, p:4.50, gf:0, img:"MHBHCAKE01.jpg"}
];
var boxQty = {};

function boxInit(){
  var g = document.getElementById("boxItems");
  var h = "";
  BOX_PIECES.forEach(function(b, i){
    var badges = (b.gf ? ' <span class="gf">GF</span>' : '') + (b.df ? ' <span class="df">DF</span>' : '') + (b.vg ? ' <span class="vg">VG</span>' : '') + (b.pet ? ' <span class="pet">DOGS</span>' : '');
    h += '<div class="bitem' + (b.gf ? ' bitem-gf' : '') + '">'
      + '<img class="bthumb" src="images/' + b.img + '" loading="lazy">'
      + '<span class="bname" title="Click to see this one up top" data-q="' + b.n + '" onclick="scrollCard(this.dataset.q)">' + b.n + badges + '</span>'
      + '<span class="bctrl"><button class="q" onclick="boxBump(' + i + ',-1)">&minus;</button>'
      + '<span class="bqty" id="bqty' + i + '">0</span>'
      + '<button class="q" onclick="boxBump(' + i + ',1)">+</button></span>'
      + '</div>';
  });
  g.innerHTML = h;
}

function boxBump(i, d){
  boxQty[i] = Math.max(0, (boxQty[i] || 0) + d);
  document.getElementById("bqty" + i).textContent = boxQty[i];
  boxRender();
document.getElementById("addBox").onclick = boxAdd;\ndocument.getElementById(\"addBox\").onclick = boxAdd;
}

function boxTotals(){
  var total = 0, full = 0, contents = [];
  BOX_PIECES.forEach(function(b, i){
    var q = boxQty[i] || 0;
    total += q; full += q * b.p;
    if (q > 0) contents.push(q + "x " + b.n);
  });
  var disc = 0.50 * total;
  var price = Math.ceil(full - disc);
  return {total: total, full: full, disc: full - price, price: price, contents: contents};
}

function boxRender(){
  var t = boxTotals();
  var s = document.getElementById("boxSummary");
  var btn = document.getElementById("addBox");
  if (t.total === 0){
    s.textContent = "Pick 4, 6 or 10 pieces to start your box.";
    btn.disabled = true;
    return;
  }
  var ok = (t.total === 4 || t.total === 6 || t.total === 10);
  var petInBox = BOX_PIECES.some(function(b, i){ return b.pet && (boxQty[i] || 0) > 0; });
  var petNote = petInBox ? '<div style="font-size:.78rem; color:var(--red); margin-top:4px">Doggie treats are packed separately from all human treats.</div>' : '';
  var hint = ok ? "" : (t.total < 4 ? " &mdash; pick " + (4 - t.total) + " more for a box of 4" : " &mdash; pick exactly 4, 6 or 10 pieces");
  s.innerHTML = "Pieces: " + t.total + " &nbsp; Full: $" + t.full.toFixed(2)
    + " &nbsp; Save: $" + t.disc.toFixed(2)
    + " &nbsp; <b>Box price: $" + t.price.toFixed(2) + "</b>" + hint + petNote;
  btn.disabled = !ok;
}

function scrollCard(name){
  var q = name.replace(/ \(.*?\)$/g, "").replace(/ Slice$/, "").trim();
  var cards = document.querySelectorAll(".card");
  for (var i = 0; i < cards.length; i++){
    if (cards[i].textContent.indexOf(q) > -1){
      var c = cards[i];
      var y0 = window.scrollY;
      try { c.scrollIntoView({behavior:"smooth", block:"start"}); } catch(e){}
      setTimeout(function(){
        if (Math.abs(window.scrollY - y0) < 5){ c.scrollIntoView({block:"start"}); }
      }, 500);
      var old = document.querySelectorAll(".card.flash");
      for (var j = 0; j < old.length; j++){ old[j].classList.remove("flash"); }
      void c.offsetWidth;
      c.classList.add("flash");
      return;
    }
  }
}

function boxAdd(){
  var t = boxTotals();
  if (t.total !== 4 && t.total !== 6 && t.total !== 10) return;
  var id = "custombox-" + Date.now();
  var name = "Your Box of " + t.total + " (" + t.contents.join(", ") + ")";
  cart[id] = {name: name, price: t.price, qty: 1, img: "", fam: 10};
  boxQty = {};
  BOX_PIECES.forEach(function(b, i){
    var e = document.getElementById("bqty" + i);
    if (e) e.textContent = "0";
  });
  boxRender();
document.getElementById("addBox").onclick = boxAdd;\ndocument.getElementById(\"addBox\").onclick = boxAdd;
  render();
}

boxInit();

function payModalOpen(){
  var p = null;
  try { p = JSON.parse(localStorage.getItem("ylft_pending_order") || "null"); } catch(e){}
  if (!p || !p.txt) return;
  document.getElementById("pmText").textContent = p.txt;
  document.getElementById("pmMail").href = "mailto:yourfoodtribe@gmail.com?subject=" + encodeURIComponent("My Christmas order") + "&body=" + encodeURIComponent(p.txt);
  document.getElementById("payModal").style.display = "flex";
}
document.getElementById("pmCopy").addEventListener("click", function(){
  var txt = document.getElementById("pmText").textContent;
  if (navigator.clipboard){ navigator.clipboard.writeText(txt).catch(function(){}); }
  this.textContent = "Copied! Now paste it to us";
  var btn = this;
  setTimeout(function(){ btn.textContent = "Copy my order"; }, 2500);
});
(function(){
  var s = location.search;
  var back = s.indexOf("token=") > -1 || s.indexOf("PayerID") > -1;
  var p = null;
  try { p = JSON.parse(localStorage.getItem("ylft_pending_order") || "null"); } catch(e){}
  if (back && p && p.txt){
    payModalOpen();
    try { localStorage.removeItem("ylft_pending_order"); } catch(e){}
  } else if (p && p.txt && (Date.now() - (p.ts || 0)) < 86400000){
    document.getElementById("payBanner").style.display = "block";
  }
})();
(function(){
  // hidden family discount - activated only by ?fam=1 in the link
  var s = location.search.toLowerCase();
  if (s.indexOf("fam=") > -1){
    try { localStorage.setItem("ylft_fam", "1"); } catch(e){}
  }
  if (s.indexOf("fam=0") > -1){
    try { localStorage.removeItem("ylft_fam"); } catch(e){}
  }
})();
(function(){
  var bar = document.getElementById("filters");
  if (!bar) return;
  var box = document.querySelector(".boxbuilder");
  function apply(f){
    bar.querySelectorAll(".chip").forEach(function(x){ x.classList.toggle("active", x.dataset.f === f); });
    document.querySelectorAll("main .card").forEach(function(cd){
      var tags = (cd.dataset.tags || "").split(" ");
      var vis = true;
      if (f === "else") vis = tags.indexOf("gf") === -1;
      else if (f === "box") vis = false;
      else if (f !== "all") vis = tags.indexOf(f) > -1;
      cd.classList.toggle("hide", !vis);
    });
    document.querySelectorAll("main .grid").forEach(function(g){
      var vis = g.querySelectorAll(".card:not(.hide)").length;
      g.style.display = vis ? "" : "none";
      var el = g.previousElementSibling;
      while (el && (el.tagName === "H2" || (el.classList && (el.classList.contains("sect-sub") || el.classList.contains("gf-note"))))){
        el.style.display = vis ? "" : "none";
        el = el.previousElementSibling;
      }
    });
    if (box) box.style.display = (f === "all" || f === "box") ? "" : "none";
  }
  bar.querySelectorAll(".chip").forEach(function(c){
    c.addEventListener("click", function(){ apply(c.dataset.f); });
  });
})();
boxRender();
document.getElementById("addBox").onclick = boxAdd;\ndocument.getElementById(\"addBox\").onclick = boxAdd;
__SNOWJS__
</script>
</body>
</html>'''

page = page.replace("__GF_CARDS__", gf_cards).replace("__ELSE_CARDS__", else_cards).replace("__TART_CARDS__", tart_cards).replace("__PIECE_CARDS__", piece_cards)

# --- feature-flagged blocks ---------------------------------------------
og_tags = ""
if FLAGS["og"]:
    og_tags = (
        '<meta property="og:title" content="Christmas Cakes &amp; Treats - order now">\n'
        '<meta property="og:description" content="Gluten free cakes, brownies, protein balls and more. Order by Thursday 5pm - delivered Monday or Tuesday, or free pickup. $12 delivered, free over $85.">\n'
        '<meta property="og:image" content="https://yourlocalfoodtribe.github.io/christmas-orders/images/LOC6WHOLE.jpg">\n'
        '<meta property="og:image:width" content="1200">\n'
        '<meta property="og:image:height" content="900">\n'
        '<meta property="og:type" content="website">\n'
        '<meta name="twitter:card" content="summary_large_image">'
    )
favicon = ""
if FLAGS["favicon"]:
    favicon = "<link rel=\"icon\" href=\"data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>\\U0001F382</text></svg>\">"
hero = ""
if FLAGS["hero"]:
    hero = f'<img class="hero" src="images/{HERO_IMG}" alt="Rich chocolate celebration cake">'
banner = ""
if FLAGS["banner"]:
    banner = '<div class="topbanner">&#127877; Delivered <span>Monday or Tuesday</span> &mdash; all across North Brisbane &#128666;</div>'
filters = ""
if FLAGS["filters"]:
    filters = (
        '<div class="filters" id="filters">'
        '<button class="chip active" data-f="all">All</button>'
        '<button class="chip" data-f="gf">Gluten free</button>'
        '<button class="chip" data-f="else">Everyone Else</button>'
        '<button class="chip" data-f="box">Build Your Own Box</button>'
        '<button class="chip" data-f="vg">Vegan</button>'
        '<button class="chip" data-f="df">Dairy free</button>'
        '</div>'
    )
faq = ""
if FLAGS["faq"]:
    faq = (
        '<div class="faq" id="faq">'
        '<h2>&#10067; Quick answers</h2>'
        '<details><summary>How far do you deliver?</summary><p>We deliver to Nundah, Wavell Heights, Chermside, Boondall, Virginia, Geebung, Zillmere, Taigum, Fitzgibbon, Bracken Ridge, Deagon, Sandgate, Shorncliffe, Brighton, Aspley and Carseldine. Not on the list? Send us a message and we will see what we can do.</p></details>'
        '<details><summary>How does everything arrive?</summary><p>Everything arrives Frozen or Refrigerated, in its original sealed packaging. Into the fridge when it reaches you - it keeps 5-7 days there. Take cakes out about an hour before serving. Not eating it yet? It lasts 6 months in the freezer.</p></details>'
        '<details><summary>Can I pick up instead?</summary><p>Yes - free pickup from Taigum Square. Type PICKUP in the address box at checkout and we will send you the pickup details.</p></details>'
        '<details><summary>How do I pay?</summary><p>PayID (yourfoodtribe@gmail.com) is free, or pay by card or PayPal at checkout.</p></details>'
        '<details><summary>What if something is not right?</summary><p>Message us straight away and we will sort it out.</p></details>'
        '</div>'
    )
bp = "bottompad" if FLAGS["bottompad"] else ""
visits_js = ""
if FLAGS["visits"]:
    visits_js = (
        'var VISITS_URL = "";   // anonymous visit counter: paste the Apps Script /exec URL here once the visit-aware doPost is deployed\n'
        'function sendVisit(){\n'
        '  try {\n'
        '    if (!VISITS_URL) return;\n'
        '    var vid = null;\n'
        '    try { vid = localStorage.getItem("gfc_vid"); } catch(e){}\n'
        '    if (!vid) {\n'
        '      vid = "v" + Date.now().toString(36) + Math.random().toString(36).slice(2, 10);\n'
        '      try { localStorage.setItem("gfc_vid", vid); } catch(e){}\n'
        '    }\n'
        '    window.__visitId = vid;\n'
        '    var ref = document.referrer || "";\n'
        '    if (ref.length > 100) ref = ref.slice(0, 100);\n'
        '    fetch(VISITS_URL, {method:"POST", mode:"no-cors", headers:{"Content-Type":"text/plain;charset=utf-8"}, body:"VISIT|" + vid + "|" + ref}).catch(function(){});\n'
        '  } catch(e){}\n'
        '}\n'
        'sendVisit();\n'
    )
snowcss = ""
snowjs = ""
if FLAGS["snow"]:
    snowcss = (
        ".snow{position:fixed; top:-40px; z-index:60; pointer-events:none; color:#fff;"
        " text-shadow:0 0 4px rgba(120,160,200,.4); animation:snowfall linear infinite}\n"
        "@keyframes snowfall{0%{transform:translate(0,-5vh) rotate(0deg)}100%{transform:translate(6vw,112vh) rotate(260deg)}}\n"
        "@media (prefers-reduced-motion: reduce){ .snow{display:none} }"
    )
    snowjs = (
        "(function(){\n"
        "  for (var i = 0; i < 28; i++){\n"
        "    var s = document.createElement(\"div\");\n"
        "    s.className = \"snow\";\n"
        "    s.textContent = \"\\u2744\";\n"
        "    s.style.left = (Math.random() * 100) + \"vw\";\n"
        "    s.style.animationDuration = (8 + Math.random() * 10) + \"s\";\n"
        "    s.style.animationDelay = (-Math.random() * 14) + \"s\";\n"
        "    s.style.fontSize = (10 + Math.random() * 14) + \"px\";\n"
        "    s.style.opacity = (0.45 + Math.random() * 0.5).toFixed(2);\n"
        "    document.body.appendChild(s);\n"
        "  }\n"
        "})();"
    )
page = (page.replace("__OG__", og_tags)
            .replace("__FAVICON__", favicon)
            .replace("__BANNER__", banner)
            .replace("__HERO__", hero)
            .replace("__FILTERS__", filters)
            .replace("__FAQ__", faq)
            .replace("__SNOWCSS__", snowcss)
            .replace("__SNOWJS__", snowjs)
            .replace("__VISITS__", visits_js)
            .replace("__BP__", bp))
open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(page)

# preview copy with absolute image paths
prev = page
for sku, m in manifest.items():
    if m["file"]:
        prev = prev.replace("images/" + m["file"], "file:///" + os.path.join(imgdir_abs, m["file"]).replace("\\", "/") if False else "images/" + m["file"])
open(os.path.join(SITE, "preview.html"), "w", encoding="utf-8").write(page)
print("index.html written:", len(page), "chars")
