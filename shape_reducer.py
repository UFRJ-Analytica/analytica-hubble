import os, json, glob
from copy import deepcopy

import shapely.geometry as sgeom
from shapely.ops import transform as shp_transform
import pyproj

SRC_DIR = "./flui_app/data_manager/geojson"               # de onde vêm os seus .json
DST_DIR = "./flui_app/data_manager/geojson_simplified"    # para onde vamos salvar simplificados
os.makedirs(DST_DIR, exist_ok=True)

# tolerância de simplificação em METROS (ajuste: 200–800 m)
TOLERANCE_M = 400

# Projeções p/ converter graus->metros->graus (tolerância em m faz sentido)
proj_to_3857 = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True).transform
proj_fr_3857 = pyproj.Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True).transform

# Quais propriedades manter (enxuga payload)
KEEP_PROPS = {'id','name','nome','NM_MUN','CD_MUN','cd_mun','SIGLA_UF','UF','uf'}

def _round_coords(obj, ndigits=5):
    """Arredonda coordenadas para reduzir ainda mais o tamanho do arquivo."""
    if isinstance(obj, list):
        return [_round_coords(x, ndigits) for x in obj]
    if isinstance(obj, float):
        return round(obj, ndigits)
    return obj

def simplify_feature(feat, tol_m=TOLERANCE_M):
    """Simplifica a geometria do Feature e encolhe propriedades."""
    out = {'type': 'Feature', 'properties': {}, 'geometry': None}

    # 1) propriedades mínimas
    props_in = feat.get('properties', {}) or {}
    props = {k: props_in[k] for k in props_in.keys() if k in KEEP_PROPS}
    # garanta UF maiúsculo se existir
    if 'uf' in props and 'UF' not in props:
        props['UF'] = str(props['uf']).upper()
    out['properties'] = props

    # 2) id (string)
    fid = feat.get('id', None)
    if fid is None:
        # tenta código municipal
        for k in ('CD_MUN','cd_mun','id'):
            if k in props_in:
                fid = str(props_in[k]); break
    if fid is not None:
        out['id'] = str(fid)

    # 3) geometria -> 3857 -> simplify -> 4326
    geom_in = feat.get('geometry', None)
    if geom_in is None:
        return out
    geom = sgeom.shape(geom_in)
    # repara invalidez simples
    if not geom.is_valid:
        geom = geom.buffer(0)

    geom_m = shp_transform(proj_to_3857, geom)
    geom_s = geom_m.simplify(tol_m, preserve_topology=True)
    geom_s = shp_transform(proj_fr_3857, geom_s)

    out['geometry'] = json.loads(json.dumps(sgeom.mapping(geom_s)))
    # 4) arredonda coords
    out['geometry']['coordinates'] = _round_coords(out['geometry']['coordinates'], 5)
    return out

def simplify_state_file(src_path, dst_path, tol_m=TOLERANCE_M):
    with open(src_path, "r", encoding="utf-8") as f:
        gj = json.load(f)
    feats = gj.get('features', [])
    out_feats = []
    for ft in feats:
        out_feats.append(simplify_feature(ft, tol_m=tol_m))
    out_gj = {'type': 'FeatureCollection', 'features': out_feats}
    # remova bbox/crs se houver
    for k in ('bbox','crs'):
        if k in out_gj:
            del out_gj[k]
    with open(dst_path, "w", encoding="utf-8") as f:
        json.dump(out_gj, f, ensure_ascii=False)

# === roda para todos os estados ===
src_files = sorted(glob.glob(os.path.join(SRC_DIR, "geojs-BR??-mun.json")))
print(f"Encontrados {len(src_files)} arquivos de estados.")
for src in src_files:
    uf = os.path.basename(src).split("-")[1][2:4]  # 'BRXX'
    dst = os.path.join(DST_DIR, f"geojs-BR{uf}-mun.json")
    print(f"Simplificando {os.path.basename(src)} -> {os.path.basename(dst)} (tol={TOLERANCE_M} m)")
    simplify_state_file(src, dst, tol_m=TOLERANCE_M)

print("✔ Simplificação concluída.")
