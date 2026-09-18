#!/usr/bin/env python3
"""Publicar una imagen como datos; este script se ejecuta solo desde main.

El PR y su SHA se obtienen de GitHub, nunca del ZIP. No se extrae ni ejecuta
ningún archivo del artefacto. El token solo se envía a api.github.com.
"""
import base64
import io
import json
import os
from pathlib import Path
import re
import struct
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, HTTPRedirectHandler, build_opener, urlopen
import zipfile
import zlib

MAX_BYTES=3_000_000
MARKER='<!-- callejero-vista-previa -->'
BRANCH='ci-previews'

class SinRedireccion(HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):return None

class GitHub:
    def __init__(self,repo,token):
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repo):
            raise ValueError('Repositorio inválido.')
        self.repo=repo;self.token=token
    def api(self,path,method='GET',data=None):
        req=Request('https://api.github.com/repos/'+self.repo+path,
                    data=None if data is None else json.dumps(data).encode(),method=method,
                    headers={'Authorization':'Bearer '+self.token,'Accept':'application/vnd.github+json',
                             'Content-Type':'application/json','X-GitHub-Api-Version':'2026-03-10'})
        # Las descargas redirigen a una URL firmada. No reenviar el token allí.
        try:
            with build_opener(SinRedireccion()).open(req,timeout=30) as r:return json.load(r)
        except HTTPError as e:
            if e.code==302 and path.endswith('/zip'):
                target=e.headers['Location']
                if urlsplit(target).scheme!='https':raise ValueError('Descarga sin HTTPS.')
                with urlopen(target,timeout=30) as r:
                    content=r.read(MAX_BYTES+1)
                if len(content)>MAX_BYTES:raise ValueError('Artefacto demasiado grande.')
                return content
            raise

def png_del_zip(content):
    """Aceptar solo avance.png, con límites y CRC; no extraer rutas al disco."""
    if len(content)>MAX_BYTES:raise ValueError('ZIP demasiado grande.')
    with zipfile.ZipFile(io.BytesIO(content)) as z:
        entries=z.infolist()
        if len(entries)!=1 or entries[0].filename!='avance.png':
            raise ValueError('El artefacto debe contener únicamente avance.png.')
        if entries[0].file_size>MAX_BYTES:raise ValueError('Imagen demasiado grande.')
        png=z.read(entries[0])
    if not png.startswith(b'\x89PNG\r\n\x1a\n'):raise ValueError('La imagen no es PNG.')
    pos=8;types=[]
    while pos<len(png):
        if pos+12>len(png):raise ValueError('PNG truncado.')
        size=struct.unpack('>I',png[pos:pos+4])[0]
        kind=png[pos+4:pos+8];end=pos+8+size
        if end+4>len(png):raise ValueError('PNG truncado.')
        if zlib.crc32(png[pos+4:end])&0xffffffff!=struct.unpack('>I',png[end:end+4])[0]:
            raise ValueError('CRC del PNG incorrecto.')
        if not types:
            if kind!=b'IHDR' or size!=13:raise ValueError('Cabecera PNG inválida.')
            width,height=struct.unpack('>II',png[pos+8:pos+16])
            if not (0<width<=4096 and 0<height<=4096 and width*height<=10_000_000):
                raise ValueError('Dimensiones de imagen inválidas.')
        types.append(kind);pos=end+4
        if kind==b'IEND':
            if size or pos!=len(png):raise ValueError('Final PNG inválido.')
            break
    if not types or types[-1]!=b'IEND' or b'IDAT' not in types:raise ValueError('PNG incompleto.')
    return png

def vigente(pr,repo,sha,default_branch):
    return (pr.get('state')=='open' and pr.get('head',{}).get('sha')==sha
            and (pr.get('head',{}).get('repo') or {}).get('full_name')==repo
            and (pr.get('base',{}).get('repo') or {}).get('full_name')==repo
            and pr.get('base',{}).get('ref')==default_branch)

def asegurar_rama(api):
    try:api('/git/ref/heads/'+BRANCH);return
    except HTTPError as e:
        if e.code!=404:raise
    tree=api('/git/trees','POST',{'tree':[{'path':'README.md','mode':'100644','type':'blob',
               'content':'Imágenes de revisión. Generadas automáticamente; no editar a mano.\n'}]})
    commit=api('/git/commits','POST',{'message':'Iniciar vistas previas','tree':tree['sha'],'parents':[],
                  'author':{'name':'github-actions[bot]','email':'41898282+github-actions[bot]@users.noreply.github.com'}})
    try:api('/git/refs','POST',{'ref':'refs/heads/'+BRANCH,'sha':commit['sha']})
    except HTTPError as e:
        if e.code!=422:raise
        api('/git/ref/heads/'+BRANCH)  # Otro PR pudo crearla mientras tanto.

def publicar_png(client,png,number,sha,run_id,attempt):
    api=client.api;asegurar_rama(api)
    path=f'pr-{number}/{sha}-{run_id}-{attempt}.png'
    for _ in range(3):
        data={'message':f'Vista previa del PR #{number} ({sha[:7]})','branch':BRANCH,
              'content':base64.b64encode(png).decode()}
        try:data['sha']=api('/contents/'+path+'?ref='+BRANCH)['sha']
        except HTTPError as e:
            if e.code!=404:raise
        try:result=api('/contents/'+path,'PUT',data);break
        except HTTPError as e:
            if e.code not in (409,422):raise
    else:raise RuntimeError('No se pudo guardar la imagen; reejecutar este workflow.')
    # URL de un commit inmutable: ni caché vieja ni imagen de otra versión.
    return f"https://raw.githubusercontent.com/{client.repo}/{result['commit']['sha']}/{path}"

def comentar(client,event):
    run=event['workflow_run'];repo=client.repo;default=event['repository']['default_branch']
    if (event['repository']['full_name']!=repo or run.get('event')!='pull_request'
        or (run.get('head_repository') or {}).get('full_name')!=repo
        or run.get('path','').split('@')[0]!='.github/workflows/validar.yml'):
        return 'Evento fuera del alcance; no se publicó nada.'
    sha=run['head_sha'];run_id=run['id'];attempt=run.get('run_attempt',1)
    if not re.fullmatch(r'[0-9a-f]{40}',sha) or type(run_id)!=int or run_id<=0 or type(attempt)!=int or attempt<=0:
        raise ValueError('Identificación de ejecución inválida.')
    api=client.api
    candidates=run.get('pull_requests') or api(f'/commits/{sha}/pulls?per_page=100')
    current=[]
    for candidate in candidates:
        number=candidate['number']
        if type(number)!=int or number<=0:raise ValueError('Número de PR inválido.')
        pr=api(f'/pulls/{number}')
        if vigente(pr,repo,sha,default):current.append(pr)
    if len(current)!=1:return 'PR cerrado, ambiguo o con una versión más nueva; no se publicó nada.'
    number=current[0]['number'];url=f'https://github.com/{repo}/actions/runs/{run_id}'
    body=f'{MARKER}\n### Vista de la revisión\n\nVersión `{sha[:7]}`. [Ver controles y archivos]({url}).\n\n'
    if run.get('conclusion')=='success':
        artifacts=api(f'/actions/runs/{run_id}/artifacts?per_page=100')['artifacts']
        selected=[a for a in artifacts if a['name']==f'vista-pr-{sha}' and not a['expired']]
        if len(selected)!=1:raise ValueError('Falta el artefacto único de esta versión.')
        artifact=selected[0]
        if artifact['size_in_bytes']>MAX_BYTES:raise ValueError('Artefacto demasiado grande.')
        png=png_del_zip(api(f"/actions/artifacts/{int(artifact['id'])}/zip"))
        image_url=publicar_png(client,png,number,sha,run_id,attempt)
        body+=(f'![Avance de revisión del callejero]({image_url})\n\n'
               '**Círculo naranja:** fila modificada en este PR, incluso si solo cambió su nota o fuente. '
               'El color interior conserva su estado: verde, propuesta; ámbar, consulta; '
               'azul, conformidad municipal; gris, sin revisar.\n\n'
               'El gráfico incluye los ejemplos del lote 01. Un control correcto comprueba las reglas; '
               'el supervisor todavía revisa las fuentes y las preguntas. Incorporar el PR no aprueba un nombre.')
    else:
        body+=('**Esta versión no tiene una vista validada.** Abrí el enlace de controles, '
               'leé el primer error y corregilo desde Codespaces. Después hacé otro commit y push '
               'en la misma rama. El resultado anterior no representa estos cambios.')
    # Evitar que una ejecución lenta sustituya la vista de un commit más nuevo.
    if not vigente(api(f'/pulls/{number}'),repo,sha,default):return 'El PR cambió durante la preparación; se omitió el comentario.'
    previous=None;page=1
    while True:
        comments=api(f'/issues/{number}/comments?per_page=100&page={page}')
        previous=next((c for c in comments if c['user']['login']=='github-actions[bot]'
                       and c['user']['type']=='Bot' and c.get('body','').startswith(MARKER)),previous)
        if len(comments)<100:break
        page+=1
    if previous:api(f"/issues/comments/{previous['id']}",'PATCH',{'body':body})
    else:api(f'/issues/{number}/comments','POST',{'body':body})
    return f'Comentario actualizado para el PR #{number}, versión {sha[:7]}.'

if __name__=='__main__':
    event=json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
    print(comentar(GitHub(os.environ['GITHUB_REPOSITORY'],os.environ['GH_TOKEN']),event))
