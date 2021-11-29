# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 16:40:25 2021

@author: catal
"""

from browser import document, prompt, html, alert
from browser.local_storage import storage
import json, base64
import yarn_selector_web as ysw

def load_data():
    data = storage.get("b64data")
    if data:
        return json.loads(data)
    else:
        storage["b64data"] = json.dumps({})
        return {}

def base64_compute(evt):
    value = document["text-src"].value
    if not value:
        alert("You need to enter a value")
        return
    if value in b64_map:
        alert(f"'{value}' already exists: '{b64_map[value]}'")
        return
    b64data = str(ysw.suggestYarn(value)[:50])  # TODO modified
    b64_map[value] = b64data
    storage["b64data"] = json.dumps(b64_map)
    display_map()

def clear_map(evt):
    b64_map.clear()
    storage["b64data"] = json.dumps({})
    document["b64-display"].clear()

def display_map():
    if not b64_map:
        return
    table = html.TABLE(Class="pure-table")
    table <= html.THEAD(html.TR(html.TH("Text") + html.TH("Base64")))
    table <= (html.TR(html.TD(key) + html.TD(b64_map[key])) for key in b64_map)
    base64_display = document["b64-display"]
    base64_display.clear()
    base64_display <= table
    document["text-src"].value = ""

b64_map = load_data()
display_map()
document["submit"].bind("click", base64_compute)
document["clear-btn"].bind("click", clear_map)