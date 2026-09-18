#!/usr/bin/env python3
import json
import sys
from comun import RAIZ, DatosInvalidos, cargar, resumen

def main():
    out=RAIZ/'build'; out.mkdir(exist_ok=True)
    try:
        info={'valido':True,'resumen':resumen(cargar()),'errores':[]}; code=0
    except (DatosInvalidos,ValueError,OSError) as e:
        info={'valido':False,'errores':str(e).splitlines()}; code=1
    (out/'validacion.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(info,ensure_ascii=False,indent=2)); return code

if __name__=='__main__': sys.exit(main())
