;;; CALLEJERO - UTF-8, AutoCAD 2021+ con LISPSYS 1 o 2.
;;; NO EJECUTADO EN AUTOCAD por el autor de este paquete.
;;; Probar con el operador en una COPIA antes de considerar uso institucional.
;;; Solo TEXT/MTEXT planos, capa NOMBRE CALLES, espacio modelo.
;;; No guarda el DWG. La simulacion es la opcion predeterminada.

(defun cal:split (s / pos start result)
  (setq start 1 pos 1 result nil)
  (while (<= pos (strlen s))
    (if (= (substr s pos 1) "|")
      (progn (setq result (cons (substr s start (- pos start)) result))
             (setq start (1+ pos))))
    (setq pos (1+ pos)))
  (reverse (cons (substr s start) result)))

(defun cal:plain (s / i ok n ch)
  (setq i 1 ok (and s (> (strlen s) 0) (<= (strlen s) 200)))
  (if ok
    (progn
      (if (or (= (substr s 1 1) " ") (= (substr s (strlen s) 1) " ")) (setq ok nil))
      (while (<= i (strlen s))
        (setq ch (substr s i 1) n (ascii ch))
        (if (or (< n 32) (= n 127) (member ch '("|" "\\" "{" "}" "%"))) (setq ok nil))
        (setq i (1+ i)))))
  ok)

(defun cal:hex (s / i ok)
  (setq i 1 ok (> (strlen s) 0))
  (while (<= i (strlen s))
    (if (not (wcmatch (substr (strcase s) i 1) "[0-9A-F]")) (setq ok nil))
    (setq i (1+ i)))
  ok)

(defun cal:log (s)
  (if cal:logfile (write-line s cal:logfile))
  (princ (strcat "\n" s)))

(defun cal:close ()
  (if cal:input (progn (close cal:input) (setq cal:input nil)))
  (if cal:undo (progn (command-s "._UNDO" "_End") (setq cal:undo nil)))
  (if cal:logfile (progn (close cal:logfile) (setq cal:logfile nil)))
  (setq *error* cal:old-error))

(defun cal:error (msg)
  (cal:log (strcat "INTERRUMPIDO: " msg))
  (cal:log "Puede haber cambios parciales. No guardar; revisar el registro y usar U si se inicio el grupo UNDO.")
  (cal:close)
  (princ))

(defun cal:check (row / en ed layer flags actual)
  (setq en (handent (car row)))
  (if en (setq ed (entget en)))
  (cond
    ((not en) "FALTA_HANDLE")
    ((not (member (cdr (assoc 0 ed)) '("TEXT" "MTEXT"))) "TIPO_NO_ADMITIDO")
    ((/= (cdr (assoc 8 ed)) "NOMBRE CALLES") "OTRA_CAPA")
    ((not (equal (cdr (assoc 410 ed)) "Model")) "FUERA_DE_MODELO")
    ((assoc 3 ed) "MTEXT_FRAGMENTADO_REVISION_MANUAL")
    ((not (cal:plain (cdr (assoc 1 ed)))) "FORMATO_REVISION_MANUAL")
    (T
      (setq layer (tblsearch "LAYER" "NOMBRE CALLES") flags (cdr (assoc 70 layer)))
      (setq actual (cdr (assoc 1 ed)))
      (cond
        ((/= 0 (logand 4 flags)) "CAPA_BLOQUEADA")
        ((= actual (caddr row)) "YA_ACTUALIZADO")
        ((/= actual (cadr row)) "TEXTO_NO_COINCIDE")
        (T "LISTO")))))

(defun c:ACTUALIZAR_CALLES (/ path mode header line fields rows seen invalid count
                           logpath suffix row status ready skipped done failed en ed result again)
  (setq cal:old-error *error* *error* cal:error cal:input nil cal:logfile nil cal:undo nil)
  (cond
    ((< (atof (getvar "ACADVER")) 24.0)
      (princ "\nSe requiere AutoCAD 2021+ con lectura UTF-8 explicita.") (cal:close))
    ((= (getvar "LISPSYS") 0)
      (princ "\nLISPSYS debe ser 1 o 2; su cambio requiere reiniciar AutoCAD. Consultar al operador.") (cal:close))
    ((not (setq path (getfiled "Archivo de cambios UTF-8" "" "txt" 0))) (cal:close))
    (T
      (setq cal:input (open path "r" "utf8"))
      (if (not cal:input) (progn (princ "\nNo se pudo abrir el archivo.") (cal:close))
        (progn
          (setq header (read-line cal:input) rows nil seen nil invalid nil)
          (if (not (member header '("# CALLEJERO|1|APROBADAS" "# CALLEJERO|1|SIMULACION")))
            (setq invalid T))
          (while (setq line (read-line cal:input))
            (if (and (/= line "") (/= (substr line 1 1) "#"))
              (progn
                (setq fields (cal:split line))
                (if (or (/= (length fields) 3)
                        (not (cal:hex (car fields)))
                        (not (cal:plain (cadr fields)))
                        (not (cal:plain (caddr fields)))
                        (member (strcase (car fields)) seen))
                  (setq invalid T)
                  (progn
                    (setq seen (cons (strcase (car fields)) seen))
                    (setq rows (cons fields rows)))))))
          (close cal:input) (setq cal:input nil rows (reverse rows))
          (cond
            (invalid (princ "\nArchivo invalido: cabecera, duplicado, formato o renglon incorrecto. CERO cambios.") (cal:close))
            ((not rows) (princ "\nArchivo sin cambios autorizados. CERO cambios.") (cal:close))
            (T
              (initget "Simular Aplicar")
              (setq mode (getkword "\nModo [Simular/Aplicar] <Simular>: "))
              (if (not mode) (setq mode "Simular"))
              (if (and (= mode "Aplicar") (/= header "# CALLEJERO|1|APROBADAS"))
                (progn (princ "\nEste archivo solo admite Simular.") (setq mode nil)))
              (if (= mode "Aplicar")
                (progn
                  (initget "Copia Salir")
                  (if (/= (getkword "\nConfirmar copia de prueba y conformidad revisada [Copia/Salir] <Salir>: ") "Copia")
                    (setq mode nil))))
              (if (not mode) (cal:close)
                (progn
                  (setq suffix 0 logpath (strcat path ".log"))
                  (while (findfile logpath)
                    (setq suffix (1+ suffix) logpath (strcat path "." (itoa suffix) ".log")))
                  (setq cal:logfile (open logpath "w" "utf8"))
                  (if (not cal:logfile)
                    (progn (princ "\nNo se puede crear el registro. CERO cambios.") (cal:close))
                    (progn
                      (cal:log (strcat "DIBUJO: " (getvar "DWGPREFIX") (getvar "DWGNAME")))
                      (cal:log (strcat "MODO: " mode))
                      (setq ready nil skipped 0 again 0 done 0 failed 0)
                      (foreach row rows
                        (setq status (cal:check row))
                        (cal:log (strcat (car row) "|" status))
                        (cond ((= status "LISTO") (setq ready (cons row ready)))
                              ((= status "YA_ACTUALIZADO") (setq again (1+ again)))
                              (T (setq skipped (1+ skipped)))))
                      ;; Cualquier discrepancia aborta Aplicar antes de la primera escritura.
                      (if (and (= mode "Aplicar") (> skipped 0))
                        (cal:log "ABORTADO: resolver discrepancias y regenerar el paquete. CERO cambios.")
                        (if (and (= mode "Aplicar") ready)
                          (if (or (= 0 (logand 1 (getvar "UNDOCTL")))
                                  (/= 0 (logand 8 (getvar "UNDOCTL"))))
                            (cal:log "ABORTADO: UNDO desactivado o grupo existente. CERO cambios.")
                            (progn
                              (command-s "._UNDO" "_Begin") (setq cal:undo T)
                              (foreach row (reverse ready)
                                (if (= failed 0)
                                  (progn
                                    ;; Revalidar inmediatamente antes de cada escritura.
                                    (setq status (cal:check row))
                                    (if (/= status "LISTO")
                                      (progn (setq failed (1+ failed)) (cal:log (strcat (car row) "|FALLO|" status)))
                                      (progn
                                        (setq en (handent (car row)) ed (entget en))
                                        (setq result (entmod (subst (cons 1 (caddr row)) (assoc 1 ed) ed)))
                                        (if (and result (= (cdr (assoc 1 (entget en))) (caddr row)))
                                          (progn (entupd en) (setq done (1+ done)) (cal:log (strcat (car row) "|CAMBIADO")))
                                          (progn (setq failed (1+ failed)) (cal:log (strcat (car row) "|FALLO_ENTMOD")))))))))
                              (command-s "._UNDO" "_End") (setq cal:undo nil)))))
                      (cal:log (strcat "RESUMEN|listos=" (itoa (length ready)) "|ya_actualizados=" (itoa again)
                                       "|discrepancias=" (itoa skipped) "|cambiados=" (itoa done) "|fallos=" (itoa failed)))
                      (if (> failed 0) (cal:log "Hay cambios parciales posibles. No guardar; revisar y usar U para deshacer el grupo."))
                      (cal:log "No se guardo el DWG automaticamente. Revisar el plano y el registro.")
                      (cal:close)))))))))))
  (princ))

(princ "\nCargado ACTUALIZAR_CALLES. Prueba en copia obligatoria; Enter elige Simular.")
(princ)
