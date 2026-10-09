"""Entrada reproducible Fase 4. 'entrenar' y 'comparar' nunca evalúan prueba."""
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'wrangler/04_MODELADO'))
from eduanalytics_modelado import core


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('etapa', choices=['preparar', 'entrenar', 'comparar', 'finalizar',
                                         'verificar', 'notebooks', 'informe', 'reproducir-final'])
    parser.add_argument('--modelo', choices=['todos', 'dummy']+core.MODELOS, default='todos')
    parser.add_argument('--escenario', choices=['principal', 'reducido', 'ambos'], default='principal')
    parser.add_argument('--incluir-prueba', action='store_true', help='Autoriza ejecutar notebook 06 tras selección congelada.')
    parser.add_argument('--desde', choices=['raiz', 'carpetas'], default='raiz')
    args = parser.parse_args()
    if args.etapa == 'preparar':
        print(core.preparar().relative_to(ROOT))
        return
    directory = core.experimento_actual()
    if args.etapa == 'entrenar':
        scenarios = core.ESCENARIOS if args.escenario == 'ambos' else [args.escenario]
        models = core.MODELOS if args.modelo == 'todos' else [args.modelo]
        if args.modelo == 'todos' and 'principal' in scenarios:
            core.entrenar('dummy', directory=directory)
        for s in scenarios:
            for n in models:
                core.entrenar(n, s, directory)
    elif args.etapa == 'comparar':
        print(json.dumps(core.comparar(directory), ensure_ascii=False, indent=2))
    elif args.etapa == 'finalizar':
        print(json.dumps(core.finalizar(directory), ensure_ascii=False, indent=2))
    elif args.etapa == 'informe':
        from eduanalytics_modelado.academico import generar_informe
        generar_informe(directory)
    elif args.etapa in ['verificar', 'reproducir-final']:
        from eduanalytics_modelado.verificacion import verificar, reproducir_final
        result = verificar(directory) if args.etapa == 'verificar' else reproducir_final(directory)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        from eduanalytics_modelado.verificacion import ejecutar_notebooks
        ejecutar_notebooks(directory, args.desde, args.incluir_prueba)


if __name__ == '__main__':
    main()
