"""Estilo editorial compartido para propuesta e informe. Datos escapados como texto."""
from html import escape, unescape
import reportlab
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

FONT_DIR=Path(reportlab.__file__).parent/'fonts'
pdfmetrics.registerFont(TTFont('Callejero',str(FONT_DIR/'Vera.ttf')))
pdfmetrics.registerFont(TTFont('CallejeroBold',str(FONT_DIR/'VeraBd.ttf')))

INK=colors.HexColor('#19324b'); TEAL=colors.HexColor('#167d83'); PALE=colors.HexColor('#edf4f5')
ST=getSampleStyleSheet()
ST.add(ParagraphStyle(name='TitleC',fontName='CallejeroBold',fontSize=27,leading=31,textColor=INK,spaceAfter=16))
ST.add(ParagraphStyle(name='HeadingC',fontName='CallejeroBold',fontSize=15,leading=19,textColor=INK,spaceBefore=14,spaceAfter=8))
ST.add(ParagraphStyle(name='TextC',fontName='Callejero',fontSize=10.1,leading=14.8,spaceAfter=9,textColor=INK))
ST.add(ParagraphStyle(name='SmallC',fontName='Callejero',fontSize=8.4,leading=11.4,textColor=INK,spaceAfter=4))
ST.add(ParagraphStyle(name='KickerC',fontName='CallejeroBold',fontSize=9,leading=12,textColor=TEAL,spaceAfter=9))

def p(text,style='TextC'): return Paragraph(escape(str(text)).replace('\n','<br/>'),ST[style])
def h(text): return p(text,'HeadingC')
def kicker(text): return p(text.upper(),'KickerC')
def table(headers,rows,widths):
    data=[[p(x,'SmallC') for x in headers]]+[[p(x,'SmallC') for x in row] for row in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT'); t.spaceAfter=10
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LINEBELOW',(0,0),(-1,0),.7,TEAL),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#d8e2e8'))]))
    return t

def build(path,story,title):
    path.parent.mkdir(parents=True,exist_ok=True)
    md=[]
    def plain(cell):
        if isinstance(cell,list): return ' '.join(plain(c) for c in cell)
        return cell.getPlainText() if hasattr(cell,'getPlainText') else str(cell)
    for item in story:
        if isinstance(item,Paragraph):
            level={'TitleC':'# ','HeadingC':'## ','KickerC':'### '}.get(item.style.name,'')
            md.append(level+unescape(item.text.replace('<br/>','\n')))
        elif isinstance(item,Table):
            values=[[plain(c).replace('|','/').replace('\n',' ') for c in row] for row in item._cellvalues]
            md.append('\n'.join(['| '+' | '.join(values[0])+' |','| '+' | '.join(['---']*len(values[0]))+' |']+['| '+' | '.join(row)+' |' for row in values[1:]]))
    path.with_suffix('.md').write_text('\n\n'.join(md)+'\n',encoding='utf-8')
    def footer(c,doc):
        c.saveState(); c.setStrokeColor(colors.HexColor('#d8e2e8')); c.line(46,43,A4[0]-46,43)
        c.setFont('Callejero',8); c.setFillColor(INK)
        c.drawString(46,29,'CALLEJERO / '+title); c.drawRightString(A4[0]-46,29,str(doc.page)); c.restoreState()
    SimpleDocTemplate(str(path),pagesize=A4,rightMargin=46,leftMargin=46,topMargin=43,bottomMargin=59,
                      title=title,author='Proyecto callejero · los-topos-cosmicos').build(story,onFirstPage=footer,onLaterPages=footer)
