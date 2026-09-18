"""Controles de estructura, no ejecución ni certificación de AutoCAD."""
from pathlib import Path
import re
import unittest

class LispEstatico(unittest.TestCase):
    def test_lists_and_control_form_structure(self):
        s=(Path(__file__).resolve().parents[1]/'entrega/actualizar_calles.lsp').read_text()
        tokens=re.findall(r';[^\n]*|"(?:\\.|[^"\\])*"|[()]|\'|[^\s()\';]+',s)
        tokens=[t for t in tokens if not t.startswith(';')];pos=0
        def parse():
            nonlocal pos
            t=tokens[pos];pos+=1
            if t=='(':
                result=[]
                while pos<len(tokens) and tokens[pos]!=')':result.append(parse())
                self.assertLess(pos,len(tokens),'Lista sin cierre');pos+=1;return result
            self.assertNotEqual(t,')','Cierre extra')
            if t=="'":return ['quote',parse()]
            return t
        forms=[]
        while pos<len(tokens):forms.append(parse())
        def check(f):
            if not isinstance(f,list) or not f:return
            if f[0]=='if':self.assertIn(len(f),(3,4),'if con argumentos incorrectos')
            if f[0]=='setq':self.assertEqual(len(f)%2,1,'setq incompleto')
            if f[0]=='cond':self.assertTrue(all(isinstance(x,list) for x in f[1:]))
            for child in f:check(child)
        for f in forms:check(f)
        self.assertEqual(sum(f[:2]==['defun','c:ACTUALIZAR_CALLES'] for f in forms),1)
