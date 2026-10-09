"""Verificación de Fase 4 y copia limpia del contenido destinado a Git."""
from pathlib import Path
import argparse
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'wrangler/04_MODELADO'))
from eduanalytics_modelado import core
from eduanalytics_modelado.verificacion import verificar,verificar_copia_limpia,manifiesto

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--copia-limpia',action='store_true')
    p.add_argument('--manifest',action='store_true')
    args=p.parse_args()
    d=core.experimento_actual()
    result=verificar_copia_limpia(d) if args.copia_limpia else verificar(d)
    if args.manifest: manifiesto(d)
    print(json.dumps(result,ensure_ascii=False,indent=2))
