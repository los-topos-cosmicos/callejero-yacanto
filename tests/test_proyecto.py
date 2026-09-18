"""Regresiones que protegen aprobación, formato, integridad y exportación."""
import csv
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from comun import cargar, resumen, DatosInvalidos, leer_csv, escribir_csv, LOTE, CONFORMIDAD, geojson
from generar_entrega import generar, cambios, archivo_cad

class Proyecto(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)/'repo'
        for name in ('datos','config','entrega','docs'):
            shutil.copytree(ROOT/name,self.root/name)
    def tearDown(self): self.tmp.cleanup()
    def update(self,key,**fields):
        for path in (self.root/'datos/lotes').glob('*.csv'):
            rows=leer_csv(path)
            if any(r['id']==key for r in rows):
                for r in rows:
                    if r['id']==key:r.update(fields)
                escribir_csv(path,rows,LOTE);return
        raise AssertionError(key)
    def propose(self):
        key=next(k for k,r in cargar(self.root)['rows'].items() if r['nombre_crudo']=='Av Jose Marrero')
        self.update(key,nombre='Av. José Marrero',tipo='avenida',homenaje='persona',estado='propuesta',
                    nota='Caso sintético de prueba de abreviatura y acento; no es conformidad real.',fuente='Fixture de test')
        return key
    def approve(self,key,**overrides):
        row=cargar(self.root)['rows'][key]
        a=dict(id=key,nombre_crudo=row['nombre_crudo'],nombre_aprobado=row['nombre'],fecha='2026-09-18',referencia='TEST-SINTETICO')
        a.update(overrides);escribir_csv(self.root/'datos/conformidad.csv',[a],CONFORMIDAD)
    def test_baseline_counts_and_no_approval(self):
        data=cargar(self.root);s=resumen(data)
        # 251 calles y 1102 rótulos salen de la extracción: no cambian con el avance.
        self.assertEqual((s['total'],s['rotulos']),(251,1102))
        # Sin conformidad registrada no hay nada aprobado, esté como esté el avance.
        self.assertEqual(s['aprobada'],0)
        self.assertEqual(cambios(data,True),[])
    def test_unapproved_changes_never_enter_approved_payload(self):
        # Se mide el incremento, no el total: los lotes avanzan con el trabajo.
        antes=len(cambios(cargar(self.root),False))
        self.propose();data=cargar(self.root)
        self.assertEqual(cambios(data,True),[])
        self.assertEqual(len(cambios(data,False))-antes,9)
    def test_exact_approved_accent_reaches_all_9_handles(self):
        key=self.propose();self.approve(key);data=cargar(self.root)
        changes=cambios(data,True);self.assertEqual(len(changes),9)
        dest=Path(self.tmp.name)/'salida';generar(self.root,dest,con_pdf=False)
        for name,encoding in [('actualizaciones_aprobadas_utf8.txt','utf-8'),('actualizaciones_aprobadas_cp1252.txt','cp1252')]:
            b=(dest/name).read_bytes();self.assertIn(b'\r\n',b)
            self.assertEqual(b.decode(encoding).count('Av. José Marrero'),9)
        self.assertTrue((dest/'actualizaciones_aprobadas_cp1252.txt').read_bytes().startswith(b'# CALLEJERO|1|AUXILIAR_CP1252'))
    def test_changed_name_invalidates_conformity(self):
        key=self.propose();self.approve(key);self.update(key,nombre='Av. José Marrero Norte')
        with self.assertRaisesRegex(DatosInvalidos,'texto exacto'):cargar(self.root)
    def test_approval_needs_real_shape_date_reference_and_uniqueness(self):
        key=self.propose()
        for overrides in ({'fecha':'18/09/2026'},{'referencia':''},{'nombre_crudo':'otro'}):
            escribir_csv(self.root/'datos/conformidad.csv',[],CONFORMIDAD)
            self.approve(key,**overrides)
            with self.assertRaises(DatosInvalidos):cargar(self.root)
        escribir_csv(self.root/'datos/conformidad.csv',[],CONFORMIDAD);self.approve(key)
        rows=leer_csv(self.root/'datos/conformidad.csv');escribir_csv(self.root/'datos/conformidad.csv',rows*2,CONFORMIDAD)
        with self.assertRaisesRegex(DatosInvalidos,'duplicada'):cargar(self.root)
    def test_approval_cannot_be_typed_in_lot(self):
        self.update('006',estado='aprobada')
        with self.assertRaisesRegex(DatosInvalidos,'se deriva'):cargar(self.root)
    def test_dangerous_names_are_rejected(self):
        for name in ('Alma|fuerte','Alma\\Pfu','{Almafuerte}','Alma%fu','Ōcho','Alma\nfu','Alma\u200bfu'):
            with self.subTest(name=name):
                self.update('006',nombre=name)
                with self.assertRaises(DatosInvalidos):cargar(self.root)
    def test_header_whitespace_and_short_rows_are_rejected(self):
        p=self.root/'datos/lotes/lote-02.csv';old=p.read_text()
        p.write_text(old.replace('id,',' id,',1))
        with self.assertRaisesRegex(DatosInvalidos,'cabecera exacta'):cargar(self.root)
        p.write_text(old+'999,foo\n')
        with self.assertRaisesRegex(DatosInvalidos,'columnas'):cargar(self.root)
    def test_leading_zero_id_is_not_silently_repaired(self):
        self.update('008',id='8')
        with self.assertRaisesRegex(DatosInvalidos,'ID desconocido'):cargar(self.root)
    def test_queries_require_a_question_and_no_name(self):
        self.update('008',nota='')
        with self.assertRaisesRegex(DatosInvalidos,'pregunta'):cargar(self.root)
        self.update('008',nota='¿Cuál Alsina?',nombre='Adolfo Alsina')
        with self.assertRaisesRegex(DatosInvalidos,'nombre vacío'):cargar(self.root)
    def test_source_required_and_csv_commas_supported(self):
        self.update('006',fuente='')
        with self.assertRaisesRegex(DatosInvalidos,'fuente'):cargar(self.root)
        self.update('006',fuente='Rótulo recibido, referente por confirmar',nota='Nota con comas, y símbolos < > & sin HTML ejecutable')
        self.assertEqual(cargar(self.root)['rows']['006']['fuente'],'Rótulo recibido, referente por confirmar')
    def test_base_integrity_detects_edit(self):
        p=self.root/'datos/crudo/etiquetas.csv';p.write_bytes(p.read_bytes()+b'\n')
        with self.assertRaisesRegex(DatosInvalidos,'cambió el archivo base'):cargar(self.root)
    def test_geojson_has_no_unverified_geometries_and_keeps_39(self):
        g=geojson(cargar(self.root));self.assertEqual(len(g['features']),251)
        self.assertTrue(all(r['geometry'] is None for r in g['features']))
        self.assertEqual(sum(r['properties']['dentro_recorte']=='no' for r in g['features']),39)
    def test_invalid_input_leaves_existing_delivery_untouched(self):
        dest=Path(self.tmp.name)/'salida';dest.mkdir();(dest/'keep').write_text('original')
        self.update('006',nombre='Alma|fuerte')
        with self.assertRaises(DatosInvalidos):generar(self.root,dest,con_pdf=False)
        self.assertEqual((dest/'keep').read_text(),'original')
        self.assertEqual(len(list(dest.iterdir())),1)
    def test_generator_refuses_to_replace_a_previous_delivery(self):
        dest=Path(self.tmp.name)/'salida';generar(self.root,dest,con_pdf=False)
        with self.assertRaisesRegex(ValueError,'ya existe'):generar(self.root,dest,con_pdf=False)
    def test_delivery_rebuilt_from_current_data_and_hashes_match(self):
        self.update('008',nota='Pregunta más precisa para el docente')
        dest=Path(self.tmp.name)/'salida';generar(self.root,dest,con_pdf=False)
        self.assertIn('Pregunta más precisa',(dest/'consultas_pendientes.csv').read_text())
        from comun import sha256
        m=json.loads((dest/'manifest.json').read_text())
        self.assertTrue(all(sha256(dest/name)==digest for name,digest in m['salidas_sha256'].items()))
    @unittest.skipUnless(importlib.util.find_spec('ezdxf'),'Instalar requirements-extraccion.txt para probar el extractor')
    def test_synthetic_extraction_preserves_mtext_format_and_does_not_overwrite(self):
        import ezdxf
        from extraer import extraer
        doc=ezdxf.new('R2018');doc.layers.new('NOMBRE CALLES')
        doc.modelspace().add_mtext(r'{\C1;Águila Mora}',dxfattribs={'layer':'NOMBRE CALLES'})
        doc.modelspace().add_text('Calle de prueba',dxfattribs={'layer':'NOMBRE CALLES'})
        path=Path(self.tmp.name)/'test.dxf';doc.saveas(path);out=Path(self.tmp.name)/'extraccion'
        m=extraer(path,out);self.assertEqual(m['rotulos'],2)
        rows=leer_csv(out/'rotulos_extraidos.csv')
        self.assertTrue(any(r['texto_original']==r'{\C1;Águila Mora}' and r['texto_plano']=='Águila Mora' for r in rows))
        with self.assertRaises(ValueError):extraer(path,out)

if __name__=='__main__':unittest.main()
