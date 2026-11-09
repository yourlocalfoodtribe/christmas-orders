import json, os, html

BASE = r"C:\Users\Tricia\AppData\Local\hermes\cache\scratch\looma"
SITE = os.path.join(BASE, "site")
manifest = json.load(open(os.path.join(SITE, "manifest.json"), encoding="utf-8"))

# customer-facing (brandless) catalogue
ITEMS = [
    # GF section
    {"sku": "LOC3WHOLE", "name": "Vanilla & Raspberry Cake", "gf": True, "price": 119.95, "slice_price": 12.50, "unit": "whole 10-slice cake", "img": "LOC3WHOLE.jpg",
     "desc": "The flagship: vanilla bean mousse with raspberry.GF as labelled by the maker. Their most-loved GF cake.", "altbuy": "Slices cut fresh from the sealed cake on delivery day"},
    {"sku": "LOC6", "name": "Vegan Chocolate Mud Cake", "gf": True, "price": 119.95, "slice_price": 12.50, "unit": "whole 10-slice cake", "img": "LOC6.jpg",
     "desc": "Gluten free, vegan AND dairy free. The one that covers every allergy at the table. 26 five-star reviews of this cake.", "altbuy": "Slices cut fresh from the sealed cake on delivery day"},
    {"sku": "LOC8", "name": "Raffaello Cake", "gf": True, "price": 119.95, "slice_price": 12.50, "unit": "whole cake, pre-cut into 10", "img": "LOC8.jpg",
     "desc": "Coconut and white chocolate, factory pre-cut into 10 so it's dessert-table ready. Sealed original box.", "altbuy": "Slices cut fresh from the sealed cake on delivery day"},
    {"sku": "MHBHBROW03", "name": "Espresso & Hazelnut Brownie", "gf": True, "piece": True, "price": 6.95, "img": "MHBHBROW03.jpg",
     "desc": "Deep, rich, gluten free. Cut from fresh bakery slabs.", "altbuy": None},
    {"sku": "MHBHBROW07", "name": "Triple Choc Brownie", "gf": True, "piece": True, "price": 6.95, "img": "MHBHBROW07.jpg",
     "desc": "Triple chocolate, gluten free. Always the first to go on a platter.", "altbuy": None},
    {"sku": "LOCMINIFRIAND", "name": "Mini Friands", "gf": True, "price": 5.25, "unit": "piece", "img": "LOCMINIFRIAND.jpg",
     "desc": "Almond, lemon, blueberry, strawberry, pistachio and passionfruit. The morning-tea box.", "altbuy": None},
    # Everyone else
    {"sku": "LOC9WHOLE", "name": "Ferrero Rocher Cake", "gf": False, "price": 129.95, "slice_price": 13.50, "unit": "whole 10-slice cake", "img": "LOC9WHOLE.jpg",
     "desc": "The showpiece. Their most reviewed cake of all time, and the Christmas centrepiece.", "altbuy": "Slices cut fresh from the sealed cake on delivery day"},
    {"sku": "LOC7", "name": "Baked Ricotta Cheesecake", "gf": False, "price": 119.95, "unit": "whole 10-slice cake", "img": "LOC7.jpg",
     "desc": "Cinnamon base, soft ricotta centre, crumbly top. A perfect 5.0 from every reviewer.", "altbuy": None},
    {"sku": "LOC1", "name": "New York Cheesecake", "gf": False, "price": 119.95, "unit": "whole 10-slice cake", "img": "LOC1.jpg",
     "desc": "Crumbling biscuit base, creamy white chocolate filling. Another perfect 5.0.", "altbuy": None},
    {"sku": "LOC16WHOLE", "name": "Tiramisu Cake", "gf": False, "price": 119.95, "unit": "whole 10-slice cake", "img": "LOC16WHOLE.jpg",
     "desc": "Coffee, cream, and a light sponge. 'O M G, absolutely divine' per a very recent review.", "altbuy": None},
    # Tarts ($8 each / $39.95 box of 6)
    {"sku": "LOCTA3", "name": "Lemon Tart", "gf": False, "tart": True, "img": "LOCTA3.jpg", "desc": "Zesty, sharp, the palate cleanser of the platter."},
    {"sku": "LOCTA6", "name": "Berry Almond Tart", "gf": False, "tart": True, "img": "LOCTA6.jpg", "desc": "Berries and almond, a perfect 5.0 from every reviewer."},
    {"sku": "LOCTA8", "name": "Caramel Walnut Tart", "gf": False, "tart": True, "img": "LOCTA8.jpg", "desc": "Sticky caramel and walnut. Christmas table material."},
    {"sku": "LOCTA10", "name": "Biscoff Tart", "gf": False, "tart": True, "img": "LOCTA10.jpg", "desc": "Biscoff. No further explanation needed."},
    {"sku": "LOCTA5", "name": "Apple Crumble Tart", "gf": False, "tart": True, "img": "LOCTA5.jpg", "desc": "Warm apple crumble flavours in a little tart."},
    {"sku": "LOCTA9", "name": "Basque Cheesecake Tart", "gf": False, "tart": True, "img": "LOCTA9.jpg", "desc": "Burnt-top Basque cheesecake. Highly recommended by gift buyers."},
    # Platter pieces
    {"sku": "MHBHBROW09", "name": "Nutella Brownie", "gf": False, "piece": True, "price": 7.95, "img": "MHBHBROW09.jpg", "desc": "The indulgent one."},
    {"sku": "MHBHBROW11", "name": "White Choc Macadamia Brownie", "gf": False, "piece": True, "price": 6.95, "img": "MHBHBROW11.jpg", "desc": "Blondie-style, white choc and macadamia."},
    {"sku": "MHBHSLICE01", "name": "Caramel & Macadamia Crumble", "gf": False, "piece": True, "price": 6.75, "img": "MHBHSLICE01.jpg", "desc": "Caramel, macadamia, crumble top. Dangerous."},
]

def card(it):
    img = "images/" + it["img"]
    gf_badge = '<span class="gf">GF</span>' if it.get("gf") else ""
    name = html.escape(it["name"])
    desc = html.escape(it["desc"])
    if it.get("tart"):
        buttons = (f'<button class="add" data-id="{it["sku"]}-s" data-name="{name} (single)" data-price="8.00" data-img="{img}">Add single $8</button>'
                   f'<button class="add" data-id="{it["sku"]}-b" data-name="{name} box of 6" data-price="39.95" data-img="{img}">Add box of 6 $39.95</button>')
        price_line = '<div class="price">$8 each &nbsp;|&nbsp; $39.95 box of 6</div>'
    elif it.get("piece") or (it.get("gf") and it["price"] < 10):
        pack = f'<button class="add pack" data-id="{it["sku"]}-pack4" data-name="{name} 4-pack" data-price="22.00" data-img="{img}">Add 4 for $22</button>'
        buttons = (f'<button class="add" data-id="{it["sku"]}" data-name="{name}" data-price="{it["price"]:.2f}" data-img="{img}">Add single</button>' + pack)
        price_line = f'<div class="price">${it["price"]:.2f} each</div>'
    else:
        sp = it.get("slice_price")
        slice_btn = f'<button class="add" data-id="{it["sku"]}-slice" data-name="{name} slice" data-price="{sp:.2f}" data-img="{img}">Add a slice ${sp:.2f}</button>' if sp else ""
        buttons = (f'<button class="add" data-id="{it["sku"]}" data-name="{name} ({it["unit"]})" data-price="{it["price"]:.2f}" data-img="{img}">Add whole cake</button>' + slice_btn)
        price_line = f'<div class="price">${it["price"]:.2f} &nbsp;<span class="unit">{it["unit"]}</span></div>'
    alt = f'<div class="altbuy">{html.escape(it["altbuy"])}</div>' if it.get("altbuy") else ""
    return f'''<div class="card">
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
  h2{font-family:Georgia,serif; color:var(--green); font-size:1.5rem; margin:30px 0 6px}
  .sect-sub{color:var(--muted); font-size:.95rem; margin-bottom:14px}
  .gf-note{background:#ecfdf3; border:1px solid #bbe7cc; color:#14532d; padding:10px 14px; border-radius:10px; font-size:.9rem; margin-bottom:16px}
  .grid{display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:16px}
  .card{background:var(--card); border-radius:14px; overflow:hidden; box-shadow:0 2px 10px rgba(20,60,35,.08); display:flex; flex-direction:column}
  .card img{width:100%; aspect-ratio:4/3; object-fit:cover; background:#f0ede6}
  .card-body{padding:12px 14px 14px; display:flex; flex-direction:column; gap:8px; flex:1}
  .cname{font-weight:700; font-size:1.02rem}
  .gf{display:inline-block; background:var(--green2); color:#fff; font-size:.68rem; padding:2px 7px; border-radius:999px; vertical-align:middle; margin-left:6px; letter-spacing:1px}
  .card p{font-size:.86rem; color:var(--muted); flex:1}
  .price{font-weight:700; color:var(--green); font-size:1.05rem}
  .price .unit{font-weight:400; color:var(--muted); font-size:.8rem}
  .btns{display:flex; gap:8px; flex-wrap:wrap}
  button.add{background:var(--green); color:#fff; border:none; padding:9px 14px; border-radius:9px; font-size:.88rem; cursor:pointer; font-weight:600}
  button.add:hover{background:var(--green2)}
  .altbuy{font-size:.78rem; color:var(--gold)}
  .deal{background:#fff7ed; border:1px dashed var(--gold); border-radius:12px; padding:14px 16px; margin-top:16px; font-size:.95rem}
  .delivery{background:var(--green); color:#fff; border-radius:16px; padding:22px; margin-top:34px}
  .delivery h2{color:#fff; margin-top:0}
  .delivery ul{margin:10px 0 0 18px; line-height:1.7; font-size:.95rem}
  .cartbar{position:fixed; left:0; right:0; bottom:0; background:#fff; border-top:3px solid var(--gold); padding:12px 16px; box-shadow:0 -4px 18px rgba(0,0,0,.12); z-index:50}
  .cartbar .inner{max-width:1100px; margin:0 auto; display:flex; align-items:center; gap:12px; flex-wrap:wrap}
  .custfields{display:flex; flex-direction:column; gap:6px; min-width:230px; flex:1}
  .custfields input{padding:9px 12px; border:1.5px solid #d7dcd4; border-radius:9px; font-size:.92rem; width:100%}
  .custfields input:focus{outline:none; border-color:var(--green)}
  #cartSummary{flex:1; min-width:200px; font-size:.95rem}
  #cartSummary b{color:var(--green)}
  #copyOrder{background:var(--red); color:#fff; border:none; padding:12px 22px; border-radius:10px; font-size:1rem; font-weight:700; cursor:pointer}
  #copyOrder:hover{filter:brightness(1.1)}
  .linkbtn{background:none; border:none; color:var(--gold); font-size:.8rem; cursor:pointer; padding:2px 0; text-decoration:underline}
  #cartPanel{background:#fff; border:2px solid var(--green); border-radius:12px; padding:12px; width:100%; max-height:260px; overflow-y:auto; font-size:.88rem}
  #cartPanel .pline{display:flex; align-items:center; gap:8px; padding:6px 0; border-bottom:1px solid #eee}
  #cartPanel .pname{flex:1}
  #cartPanel button.q{width:30px; height:30px; border:1px solid var(--green); background:#fff; color:var(--green); border-radius:7px; cursor:pointer; font-weight:700}
  #cartPanel button.x{border:1px solid var(--red); background:#fff; color:var(--red); border-radius:7px; width:34px; height:30px; cursor:pointer}
  #cartPanel .clearall{background:none; border:none; color:var(--muted); cursor:pointer; text-decoration:underline; font-size:.78rem; margin-top:6px}
  #orderText{display:none; width:100%; margin-top:10px; font-family:monospace; font-size:.8rem; padding:8px}
  .hint{font-size:.78rem; color:var(--muted)}
  footer{max-width:1100px; margin:30px auto 20px; padding:0 16px; color:var(--muted); font-size:.75rem; line-height:1.6}
  @media (max-width:560px){ .grid{grid-template-columns:repeat(auto-fill,minmax(160px,1fr))} }
</style>
</head>
<body>
<header>
  <h1>&#127876; Christmas Cakes &amp; Treats &#127876;</h1>
  <div class="sub">Order by Thursday 5pm &middot; delivered Monday or Tuesday &middot; or free pickup</div>
  <div class="strip">
    <span>&#127873; $12 delivered, FREE over $85</span>
    <span>&#10052; Everything arrives frozen</span>
    <span>&#127856; Cakes keep 5&ndash;7 days in the fridge</span>
    <span>&#127856; Thaw 1 hour before serving</span>
  </div>
</header>
<main>
  <h2>&#127793; Gluten free, the real deal</h2>
  <div class="gf-note">Every item in this section is gluten free as labelled by its maker. Whole cakes come sealed in their original box, already cut into 10 slices. Want individual slices instead? Just say so in your order.</div>
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
  <div class="sect-sub">Cut fresh from bakery slabs.</div>
  <div class="grid">
__PIECE_CARDS__
  </div>
  <div class="deal">&#127873; <b>Any 4 brownie or crumble pieces for $22.</b> Mix and match singles and the discount applies automatically, or use the &quot;Add 4 for $22&quot; button to grab a ready-made four.</div>

  <div class="delivery">
    <h2>&#128666; Delivery &amp; pickup</h2>
    <ul>
      <li><b>$12 delivered to your door</b> &mdash; or <b>free on orders over $85</b></li>
      <li><b>Orders close Thursday 5pm</b> &middot; delivered <b>Monday or Tuesday</b> on our run</li>
      <li><b>Free pickup</b> &mdash; we'll send you the details when you order</li>
      <li>Everything arrives <b>frozen</b>: into the fridge when it reaches you, keeps 5&ndash;7 days, out of the fridge 1 hour before serving</li>
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
      <input id="custAddr" type="text" placeholder="Delivery address (or type PICKUP)" autocomplete="street-address">
    </div>
    <button id="copyOrder">Copy my order</button>
    <textarea id="orderText" rows="6"></textarea>
    <span class="hint">Copy your order, then comment it on our post or send it to us in a message. We'll reply with payment and pickup/delivery details.</span>
  </div>
</div>

<footer>
  Gluten free items are gluten free as labelled by their maker. All items arrive frozen in original packaging (where a cake is pre-cut, it's factory-cut and stays sealed). Keep frozen until needed, refrigerated after thawing, 5&ndash;7 days. Product photos are of the exact items we supply.
</footer>

<script>
var cart = {};
var PIECE_IDS = ["MHBHBROW03","MHBHBROW07","MHBHBROW09","MHBHBROW11","MHBHSLICE01"];
var PIECE_PRICES = {"MHBHBROW03":6.95,"MHBHBROW07":6.95,"MHBHBROW09":7.95,"MHBHBROW11":6.95,"MHBHSLICE01":6.75};

var TALLY_URL = "";  // paste your Apps Script web app URL here once deployed

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
    cart[id] = cart[id] || {name: b.dataset.name, price: parseFloat(b.dataset.price), qty: 0, img: b.dataset.img};
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
  // 4-for-$22 on pieces
  var saved = 0;
  if (pieces >= 4){
    var sets = Math.floor(pieces / 4);
    var fullSum = 0;
    // charge cheapest full price for leftover pieces
    var pieceLinePrices = [];
    keys.forEach(function(k){
      var it = cart[k];
    var isPiece = PIECE_IDS.indexOf(k) >= 0;
      if (isPiece){ for (var q=0; q<it.qty; q++) pieceLinePrices.push(PIECE_PRICES[k] || it.price); }
    });
    pieceLinePrices.sort(function(a,b){ return b - a; });
    var leftovers = pieceLinePrices.slice(0, pieces % 4);
    var leftoverSum = leftovers.reduce(function(a,b){ return a+b; }, 0);
    var piecesFullTotal = pieceLinePrices.reduce(function(a,b){ return a+b; }, 0);
    var piecesDealTotal = sets * 22 + leftoverSum;
    saved = piecesFullTotal - piecesDealTotal;
    subtotal = subtotal - saved;
  }
  var delivery = 0;
  var addr = (document.getElementById("custAddr").value || "").trim();
  var cname = (document.getElementById("custName").value || "").trim();
  var delLabel = "pickup (free)";
  if (subtotal > 0){
    if (addr && addr.toUpperCase() !== "PICKUP"){
      if (subtotal >= 85){ delLabel = "DELIVERY FREE (over $85) to: " + addr; }
      else { delivery = 12; delLabel = "delivery +$12 (free over $85) to: " + addr; }
    } else {
      delLabel = "pickup (free)";
    }
  }
  var total = subtotal + delivery;
  var el = document.getElementById("cartSummary");
  var editBtn = document.getElementById("editCart");
  if (!keys.length){
    el.innerHTML = "Your order is empty &mdash; tick a few things and they'll show here &#127876;";
    editBtn.style.display = "none";
    document.getElementById("cartPanel").style.display = "none";
  } else {
    editBtn.style.display = "inline";
    var txt = lines.map(function(l){ return l.it.qty + "x " + l.it.name + " = " + money(l.it.qty * l.it.unit); }).join(" &middot; ");
    if (saved > 0) txt += " &middot; 4-for-$22 deal saves " + money(saved);
    el.innerHTML = txt + "<br><b>Order: " + money(subtotal) + "</b> &nbsp; " + delLabel + " &nbsp; <b>Total: " + money(total) + "</b>";
  }
  buildOrderText(keys, subtotal, saved, delivery, delLabel, total);
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
  if (saved > 0) h += '<div style="color:var(--green); padding-top:6px">4-for-$22 deal saving you ' + money(saved) + '</div>';
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
  if (saved > 0) t += "(4-for-$22 deal applied, saving " + money(saved) + ")\\n";
  t += "Order total: " + money(subtotal) + "\\n";
  t += "Delivery preference: " + (addr && addr.toUpperCase() !== "PICKUP" ? "DELIVER to " + addr : "PICKUP") + "\\n";
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
</script>
</body>
</html>'''

page = page.replace("__GF_CARDS__", gf_cards).replace("__ELSE_CARDS__", else_cards).replace("__TART_CARDS__", tart_cards).replace("__PIECE_CARDS__", piece_cards)
open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(page)

# preview copy with absolute image paths
prev = page
for sku, m in manifest.items():
    if m["file"]:
        prev = prev.replace("images/" + m["file"], "file:///" + os.path.join(imgdir_abs, m["file"]).replace("\\", "/") if False else "images/" + m["file"])
open(os.path.join(SITE, "preview.html"), "w", encoding="utf-8").write(page)
print("index.html written:", len(page), "chars")
