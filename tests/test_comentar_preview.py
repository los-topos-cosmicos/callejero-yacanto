"""Publicación probada con una API simulada: estas pruebas nunca envían nada."""
from copy import deepcopy
import io
from pathlib import Path
import struct
import sys
import unittest
from unittest.mock import patch
import zipfile
import zlib

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from comentar_preview import comentar, png_del_zip, MAX_BYTES, MARKER, publicar_png

REPO='los-topos-cosmicos/callejero-yacanto';SHA='a'*40
def png():
    def chunk(kind,data):return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
    return (b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',1,1,8,2,0,0,0))
            +chunk(b'IDAT',zlib.compress(b'\x00\xff\xff\xff'))+chunk(b'IEND',b''))
def archive(filename='avance.png',image=None):
    result=io.BytesIO()
    with zipfile.ZipFile(result,'w',zipfile.ZIP_DEFLATED) as z:z.writestr(filename,png() if image is None else image)
    return result.getvalue()
def event():
    return {'repository':{'full_name':REPO,'default_branch':'main'},'workflow_run':{
        'event':'pull_request','head_repository':{'full_name':REPO},'path':'.github/workflows/validar.yml',
        'head_sha':SHA,'id':42,'run_attempt':1,'pull_requests':[{'number':7}],'conclusion':'success'}}

class FakeGitHub:
    repo=REPO
    def __init__(self):
        self.pr={'number':7,'state':'open','head':{'sha':SHA,'repo':{'full_name':REPO}},
                 'base':{'ref':'main','repo':{'full_name':REPO}}}
        self.writes=[];self.archive=archive();self.comments=[]
    def api(self,path,method='GET',data=None):
        if method!='GET':self.writes.append((path,method,data));return {}
        if path=='/pulls/7':return self.pr
        if path=='/actions/runs/42/artifacts?per_page=100':
            return {'artifacts':[{'name':'vista-pr-'+SHA,'id':12,'expired':False,'size_in_bytes':len(self.archive)}]}
        if path=='/actions/artifacts/12/zip':return self.archive
        if path=='/issues/7/comments?per_page=100&page=1':return self.comments
        raise AssertionError('Llamada inesperada: '+path)

class PublicarVista(unittest.TestCase):
    def test_zip_acepta_solo_el_png_y_no_rutas_ni_scripts(self):
        self.assertEqual(png_del_zip(archive()),png())
        for bad in (archive('../avance.png'),archive('script.py'),archive(image=b'print(1)'),
                    archive(image=png()+b'contenido extra'),archive(image=b'x'*(MAX_BYTES+1))):
            with self.assertRaises(ValueError):png_del_zip(bad)
    def test_no_comenta_forks_commits_viejos_pr_cerrados_o_workflow_ajeno(self):
        for field in ('fork','old','closed','path','target'):
            with self.subTest(field=field):
                api=FakeGitHub();e=event()
                if field=='fork':e['workflow_run']['head_repository']['full_name']='otro/fork'
                elif field=='old':api.pr['head']['sha']='b'*40
                elif field=='closed':api.pr['state']='closed'
                elif field=='target':api.pr['base']['ref']='otra-rama'
                else:e['workflow_run']['path']='.github/workflows/otro.yml'
                with patch('comentar_preview.publicar_png') as publish:comentar(api,e);publish.assert_not_called()
                self.assertEqual(api.writes,[])
    def test_exito_publica_la_imagen_y_actualiza_el_mismo_comentario(self):
        api=FakeGitHub();api.comments=[{'id':99,'user':{'login':'github-actions[bot]','type':'Bot'},'body':MARKER+' viejo'}]
        with patch('comentar_preview.publicar_png',return_value='https://example.invalid/avance.png') as publish:
            comentar(api,event());publish.assert_called_once_with(api,png(),7,SHA,42,1)
        path,method,data=api.writes[0]
        self.assertEqual((path,method),('/issues/comments/99','PATCH'))
        self.assertIn('Círculo naranja',data['body']);self.assertIn(SHA[:7],data['body'])
    def test_fallo_actualiza_el_aviso_sin_publicar_una_imagen_anterior(self):
        api=FakeGitHub();e=event();e['workflow_run']['conclusion']='failure'
        with patch('comentar_preview.publicar_png') as publish:comentar(api,e);publish.assert_not_called()
        self.assertIn('no tiene una vista validada',api.writes[0][2]['body'])
        self.assertNotIn('![',api.writes[0][2]['body'])
    def test_artefacto_inesperado_no_publica_ni_comenta(self):
        api=FakeGitHub();api.archive=archive('../../scripts/comentar_preview.py')
        with patch('comentar_preview.publicar_png') as publish:
            with self.assertRaises(ValueError):comentar(api,event())
            publish.assert_not_called()
        self.assertEqual(api.writes,[])
    def test_publicacion_escribe_solo_el_png_y_devuelve_url_de_commit(self):
        class ImagenAPI:
            repo=REPO
            def __init__(self):self.writes=[]
            def api(self,path,method='GET',data=None):
                if method=='GET':return {'sha':'d'*40}
                self.writes.append((path,method,deepcopy(data)));return {'commit':{'sha':'e'*40}}
        api=ImagenAPI();url=publicar_png(api,png(),7,SHA,42,1)
        self.assertEqual(len(api.writes),1)
        self.assertEqual(api.writes[0][1],'PUT');self.assertEqual(api.writes[0][2]['branch'],'ci-previews')
        self.assertIn('/contents/pr-7/',api.writes[0][0]);self.assertIn('/'+'e'*40+'/',url)

if __name__=='__main__':unittest.main()
