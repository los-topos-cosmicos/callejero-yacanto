#!/usr/bin/env python3
import argparse
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from comun import RAIZ, cargar, resumen

COLORES={'sin_revisar':'#a5b3bf','propuesta':'#16817b','en_consulta':'#d79420','aprobada':'#345cce'}
ETIQUETAS={'sin_revisar':'Sin revisar','propuesta':'Propuesta','en_consulta':'En consulta','aprobada':'Con conformidad'}

def dibujar(data,dest):
    s=resumen(data)
    fig,(ax,bar)=plt.subplots(1,2,figsize=(12,6.4),gridspec_kw={'width_ratios':[1.5,1]})
    fig.patch.set_facecolor('white')
    for state,color in COLORES.items():
        points=[data['raw'][k] for k,r in data['rows'].items() if r['estado_final']==state]
        ax.scatter([float(r['x_gk']) for r in points],[float(r['y_gk']) for r in points],s=22,color=color,label=ETIQUETAS[state],alpha=.8)
    ax.set_aspect('equal'); ax.ticklabel_format(useOffset=False,style='plain')
    ax.tick_params(axis='x',labelrotation=25,labelsize=8); ax.tick_params(axis='y',labelsize=8)
    ax.set_xlabel('X del dibujo'); ax.set_ylabel('Y del dibujo')
    ax.set_title('Ubicación relativa de los rótulos',loc='left',fontsize=13,pad=15)
    ax.grid(alpha=.15); ax.legend(fontsize=8,loc='upper right')
    states=list(COLORES)
    bar.barh([ETIQUETAS[x] for x in states],[s[x] for x in states],color=list(COLORES.values()))
    bar.invert_yaxis(); bar.set_xlim(0,s['total']*1.13)
    for i,x in enumerate(states): bar.text(s[x]+3,i,str(s[x]),va='center',fontsize=12)
    bar.set_title(f"{s['total']} calles · {s['rotulos']} rótulos",loc='left',fontsize=13,pad=15)
    for spine in ('top','right'): bar.spines[spine].set_visible(False)
    fig.suptitle('Callejero | avance de revisión',x=.08,ha='left',fontsize=20,fontweight='bold',color='#19324b')
    fig.text(.08,.07,f"Incluye las {s['fuera_recorte']} calles fuera del recorte anterior; su ubicación requiere revisión.",fontsize=10)
    fig.text(.08,.035,'Esquema de coordenadas del dibujo. No es un mapa georreferenciado ni representa ejes de calles.',fontsize=9,color='#5b6772')
    fig.subplots_adjust(left=.09,right=.95,bottom=.22,top=.83,wspace=.55)
    dest=Path(dest); dest.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(dest,dpi=150,facecolor='white'); plt.close(fig)

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--salida',type=Path,default=RAIZ/'build/avance.png')
    args=ap.parse_args(); dibujar(cargar(),args.salida); print(args.salida)
