# Marcovské scripty

Soubor skriptů zpracovávající marc. Spojuje dva úkoly dohromady.

---

## 📂 Přehled

#### Skripty na rozdělení bází 

- `divide_databases_ucla_mrc.py`                → Script který rozdělí souborný ucla marc do jednotlivých bází  
- `save_number_of_records.py`                   → Skript který spočítá kolik je záznamů, nejstarší a nejnovější záznam a velikost databáze vytvořené pomocí divide_databases_ucla_mrc.py  
- `cle_smz_sborniky_casopisy_cle_časopisy.py`   → Skript který spočítá počty monografií, almanachů a časopisů v databázích SMZ, ALKARO a CLE z ucla.

#### Skripty na prolinkování Krameria (Pro Ondřeje)

- `links_kramerius.py`       → Skript který vytahá periodika a linky na krameria 
- `match_clb_and_nk.ipynb`   → Notebook který prolinkuje naše periodika s krameriem (pomocí issn, ale i bez něj (: )

---

## ⚙️ Požadavky

- Python version: `3.x`
- Dependencies:
  - `pymarc`
  - `pandas`
  - `collections`
  - `re`

