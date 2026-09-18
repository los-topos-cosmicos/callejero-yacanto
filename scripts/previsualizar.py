#!/usr/bin/env python3
import argparse
import csv
import io
import re
import subprocess
import textwrap
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from comun import RAIZ, LOTE, CONFORMIDAD, cargar, resumen

COLORES={'sin_revisar':'#a5b3bf','propuesta':'#16817b','en_consulta':'#d79420','aprobada':'#345cce'}
ETIQUETAS={'sin_revisar':'Sin revisar','propuesta':'Propuesta','en_consulta':'En consulta','aprobada':'Con conformidad'}
DESTACADO='#e2571e'

def destacadas(data,lotes):
    """Selección manual de lotes completos; no equivale a filas cambiadas."""
    nombres={Path(x).name for x in lotes if x}
    return {k for k,r in data['rows'].items() if r.get('lote') in nombres}

def cambios_desde_git(data,base,raiz=RAIZ):
    """Comparar valores por ID, sin contar reordenamientos como trabajo nuevo.

    Se leen CSV de la base con git show. Nunca se ejecuta código de esa versión.
    El SHA proviene del evento del PR, no de una cadena interpolada en shell.
    """
    if not re.fullmatch(r'[0-9a-fA-F]{40}',base):
        raise ValueError('La base de comparación debe ser un SHA completo de Git (40 caracteres).')
    def git(*args):
        return subprocess.check_output(['git',*args],cwd=raiz).decode('utf-8-sig')
    paths=git('ls-tree','-r','--name-only','-z',base,'--','datos/lotes/').split('\0')
    def filas(path,campos):
        reader=csv.DictReader(io.StringIO(git('show',f'{base}:{path}')),strict=True)
        if reader.fieldnames!=campos:raise ValueError(f'Cabecera incompatible en la base: {path}')
        result={}
        for row in reader:
            if None in row or any(v is None for v in row.values()) or row['id'] in result:
                raise ValueError(f'Filas incompatibles en la base: {path}')
            result[row['id']]=row
        return result
    anteriores={}
    for path in paths:
        if not path or not Path(path).match('lote-*.csv'):continue
        for key,row in filas(path,LOTE).items():
            if key in anteriores:raise ValueError(f'ID repetido en la base: {key}')
            anteriores[key]=row
    conformidades=filas('datos/conformidad.csv',CONFORMIDAD)
    return {key for key,row in data['rows'].items()
            if {c:row[c] for c in LOTE}!=anteriores.get(key)
            or data['approvals'].get(key)!=conformidades.get(key)}

def dibujar(data,dest,destacar=(),*,ids=None):
    s=resumen(data)
    foco=destacadas(data,destacar) if ids is None else set(ids)&data['rows'].keys()
    con_detalle=ids is not None or bool(foco)
    fig,(ax,bar)=plt.subplots(1,2,figsize=(12,7.4 if con_detalle else 6.4),gridspec_kw={'width_ratios':[1.5,1]})
    fig.patch.set_facecolor('white')
    for state,color in COLORES.items():
        points=[data['raw'][k] for k,r in data['rows'].items() if r['estado_final']==state]
        ax.scatter([float(r['x_gk']) for r in points],[float(r['y_gk']) for r in points],s=22,color=color,label=ETIQUETAS[state],alpha=.8)
    if foco:
        points=[data['raw'][k] for k in sorted(foco)]
        ax.scatter([float(r['x_gk']) for r in points],[float(r['y_gk']) for r in points],
                   s=110,facecolors='none',edgecolors=DESTACADO,linewidths=1.6,zorder=5,
                   label='Filas del PR' if ids is not None else 'Lotes seleccionados')
    ax.set_aspect('equal'); ax.ticklabel_format(useOffset=False,style='plain')
    ax.tick_params(axis='x',labelrotation=25,labelsize=8); ax.tick_params(axis='y',labelsize=8)
    ax.set_xlabel('X del dibujo'); ax.set_ylabel('Y del dibujo')
    ax.set_title('Ubicación relativa de los rótulos',loc='left',fontsize=13,pad=15)
    ax.grid(alpha=.15)
    ax.legend(fontsize=8,loc='upper left',bbox_to_anchor=(1.04,1),borderaxespad=0,frameon=False)
    states=list(COLORES)
    bar.barh([ETIQUETAS[x] for x in states],[s[x] for x in states],color=list(COLORES.values()))
    bar.invert_yaxis(); bar.set_xlim(0,s['total']*1.13)
    for i,x in enumerate(states): bar.text(s[x]+3,i,str(s[x]),va='center',fontsize=12)
    bar.set_title(f"{s['total']} calles · {s['rotulos']} rótulos",loc='left',fontsize=13,pad=15)
    for spine in ('top','right'): bar.spines[spine].set_visible(False)
    fig.suptitle('Callejero | avance de revisión',x=.08,ha='left',fontsize=20,fontweight='bold',color='#19324b')
    if ids is not None or foco:
        cantidad='1 fila modificada' if len(foco)==1 else f'{len(foco)} filas modificadas'
        titulo=(f'{cantidad} en el PR' if ids is not None
                else f'{len(foco)} calles de los lotes seleccionados')
        fig.text(.08,.22,titulo,fontsize=11,fontweight='bold',color=DESTACADO)
        nombres=[data['rows'][k]['nombre'] or data['rows'][k]['nombre_crudo'] for k in sorted(foco)]
        muestra=' · '.join(nombres[:5])
        if len(nombres)>5:muestra+=f' · y {len(nombres)-5} más'
        muestra=textwrap.shorten(muestra,width=170,placeholder='…')
        detalle='\n'.join(textwrap.wrap(muestra,width=110)) if muestra else 'No cambiaron filas de calles ni conformidades.'
        fig.text(.08,.185,detalle,fontsize=9,color='#5b6772',va='top')
    fig.text(.08,.07,f"Incluye las {s['fuera_recorte']} calles fuera del recorte anterior; su ubicación requiere revisión.",fontsize=10)
    fig.text(.08,.035,'Esquema de coordenadas del dibujo. No es un mapa georreferenciado ni representa ejes de calles.',fontsize=9,color='#5b6772')
    fig.subplots_adjust(left=.09,right=.95,bottom=.35 if con_detalle else .22,top=.83,wspace=.55)
    dest=Path(dest); dest.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(dest,dpi=150,facecolor='white'); plt.close(fig)

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--salida',type=Path,default=RAIZ/'build/avance.png')
    group=ap.add_mutually_exclusive_group()
    group.add_argument('--destacar',nargs='*',default=[],help='Selección manual de lotes completos.')
    group.add_argument('--base',help='SHA completo de la base del PR; resaltar solo las filas modificadas.')
    args=ap.parse_args();data=cargar()
    ids=cambios_desde_git(data,args.base) if args.base else None
    dibujar(data,args.salida,args.destacar,ids=ids);print(args.salida)
