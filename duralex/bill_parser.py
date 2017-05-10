# -*- coding=utf-8 -*-
"""
Original code by RegardsCitoyen (https://github.com/RegardsCitoyens) for the-law-factory-parser
(https://github.com/regardscitoyens/the-law-factory-parser).
"""

import sys, re, html5lib
from bs4 import BeautifulSoup

from alinea_parser import word_to_number, month_to_number

bister = u'(un|duo|tre|bis|qua|quin[tqu]*|sex|sept|octo?|novo?|non|dec|vic|ter|ies)+'

ORDER = ''

# Warning changing parenthesis in this regexp has multiple consequences throughout the code
section_titles = u"((chap|t)itre|volume|livre|tome|(sous-)?section)"

re_definitif = re.compile(ur'<p[^>]*align[=:\s\-]*center"?>\(?<(b|strong)>\(?texte d[^f]*finitif\)?</(b|strong)>\)?</p>', re.I)

clean_texte_regexps = [
    (re.compile(ur'[\n\t\r\s]+'), ' '),
    (re.compile(ur'(<t[rdh][^>]*>) ?<p [^>]*> ?'), r'\1'),
    (re.compile(ur' ?</p> ?(</t[rdh]>)'), r'\1'),
    (re.compile(ur'(>%s\s*[\dIVXLCDM]+(<sup>[eE][rR]?</sup>)?)\s+-\s+([^<]*?)\s*</p>' % section_titles.upper()), r'\1</p><p><b>\6</b></p>'),
]

re_clean_title_legif = re.compile("[\s|]*l[eé]gifrance(.gouv.fr)?$", re.I)
clean_legifrance_regexps = [
    (re.compile(ur'[\n\t\r\s]+'), ' '),
    (re.compile(ur'<a[^>]*>\s*En savoir plus sur ce[^<]*</a>', re.I), ''),
    (re.compile(ur'<a/?[^>]*>', re.I), ''),
    (re.compile(ur'\s*<br/>\s*', re.I), '</p><p>'),
    (re.compile(ur'<div[^>]*class="titreSection[^>]*>\s*(%s\s+[\dIVXLCDM]+e?r?)\s*:\s*([^<]*?)\s*</div>' % section_titles, re.I), r'<p>\1</p><p><b>\5</b></p>'),
    (re.compile(ur'<div[^>]*class="titreArt[^>]*>(.*?)\s*</div>', re.I), r'<p><b>\1</b></p>'),
]

# Convert from roman numbers
re_mat_romans = re.compile(ur"[IVXCLDM]+", re.I)
romans_map = zip(
    (1000,  900, 500, 400 , 100,  90 , 50 ,  40 , 10 ,   9 ,  5 ,  4  ,  1),
    ( u'M', u'CM', u'D', u'CD', u'C', u'XC', u'L', u'XL', u'X', u'IX', u'V', u'IV', u'I')
)

def romans(n):
    n = n.upper()
    i = res = 0
    for d, r in romans_map:
        while n[i:i + len(r)] == r:
            res += d
            i += len(r)
    return res

upcase_accents = u"ÇÀÂÄÉÈÊËÎÏÔÖÙÛÜ"
locase_accents = u"çàâäéèêëîïôöùûü"


def real_lower(text):
    for a in upcase_accents:
        text = text.replace(a, locase_accents[upcase_accents.find(a)])
    return text.lower()


def lower_but_first(text):
    return text[0].upper() + real_lower(text[1:])


re_fullupcase = re.compile(ur"^([\W0-9]*)([A-Z%s][\W0-9A-Z%s]*)$" % (upcase_accents, upcase_accents), re.U)


def clean_full_upcase(text):
    mat = re_fullupcase.match(text)
    if mat:
        text = mat.group(1) + lower_but_first(mat.group(2))
    return text

re_clean_premier = re.compile(ur'((PREM)?)(1|I)ER?')
re_clean_bister = re.compile(ur'([IXV\d]+e?r?)\s+(%s)' % bister, re.I)
re_clean_subsec_space = re.compile(ur'^("?[IVX0-9]{1,4}(\s+[a-z]+)?(\s+[A-Z]{1,4})?)\s*([\.°\-]+)\s*([^\s\)])', re.I)
re_clean_subsec_space2 = re.compile(ur'^("?[IVX0-9]{1,4})\s*([a-z]*)\s*([A-H]{1,4})([\.°\-])', re.I)
re_clean_punc_space = re.compile(u'([°«»:;,\.!\?\]\)%€&\$])([^\s\)\.,\d"])')
re_clean_spaces = re.compile(ur'(\s|\xc2\xa0|\xa0)+')
re_clean_coord = re.compile(ur'^["\(]*(pour)?\s*coordination[\)\s\.]*$', re.I)
# Clean html and special chars
lower_inner_title = lambda x: x.group(1)+lower_but_first(x.group(3))+" "
html_replace = [
    (re_clean_spaces, " "),
    (re.compile(ur"−"), "-"),
    (re.compile(ur" "), " "),
    (re.compile(ur"<!--.*?-->", re.I), ""),
    # (re.compile(ur"</?br/?>[«\"\s]+", re.I), " "),
    (re.compile(ur'(«\s+|\s+»)'), '"'),
    (re.compile(ur'(«|»|“|”|„|‟|❝|❞|＂|〟|〞|〝)'), '"'),
    (re.compile(ur"(’|＇|’|ߴ|՚|ʼ|❛|❜)"), "'"),
    (re.compile(ur"(‒|–|—|―|⁓|‑|‐|⁃|⏤)"), "-"),
    (re.compile(ur"(</?\w+)[^>]*>"), r"\1>"),
    (re.compile(ur"(</?)em>", re.I), r"\1i>"),
    (re.compile(ur"(</?)strong>", re.I), r"\1b>"),
    (re.compile(ur"<(![^>]*|/?(p|span))>", re.I), ""),
    (re.compile(ur"\s*\n+\s*"), " "),
    (re.compile(ur"<[^>]*></[^>]*>"), ""),
    (re.compile(ur"^<b><i>", re.I), "<i><b>"),
    (re.compile(ur"</b>(\s*)<b>", re.I), r"\1"),
    (re.compile(ur"</?sup>", re.I), ""),
    (re.compile(ur"^((<[bi]>)*)\((S|AN)[12]\)\s*", re.I), r"\1"),
    (re.compile(ur"^(<b>Article\s*)\d+\s*<s>\s*", re.I), r"\1"),
    (re.compile(ur"<s>(.*)</s>", re.I), ""),
    (re.compile(ur"</?s>", re.I), ""),
    (re.compile(ur"\s*</?img>\s*", re.I), ""),
    (re.compile(ur"œ([A-Z])"), r"OE\1"),
    (re.compile(ur"œ\s*", re.I), "oe"),
    (re.compile(ur'^((<[^>]*>)*")%s ' % section_titles, re.I), lower_inner_title),
    (re.compile(ur' pr..?liminaire', re.I), ' préliminaire'),
    (re.compile(ur'<strike>[^<]*</strike>', re.I), ''),
    (re.compile(ur'^<a>(\w)', re.I), r"\1"),
]


def clean_html(t):
    for regex, repl in html_replace:
        t = regex.sub(repl, t)
    return t.strip()

re_clean_et = re.compile(ur'(,|\s+et)\s+', re.I)

def cleanup(dic):
    # Clean empty articles with only "Supprimé" as text
    if not dic:
        return
    if 'alineas' in dic:
        if len(dic['alineas']) == 1 and dic['alineas']['001'].startswith("(Supprimé)"):
            dic['statut'] = "supprimé"
            dic['alineas'] = {'001': ''}
        elif dic['statut'].startswith('conforme') and not len(dic['alineas']):
            dic['alineas'] = {'001': '(Non modifié)'}
        multiples = re_clean_et.sub(',', dic['titre']).split(',')
        if len(multiples) > 1:
            for d in multiples:
                new = dict(dic)
                new['titre'] = d
            return new

    return dic

def save_text(txt):
    if "done" not in txt:
        return cleanup(txt)
    txt["done"] = True
    return txt

blank_none = lambda x: x if x else ""
re_cl_html = re.compile(ur"<[^>]+>")
re_cl_html_except_tables = re.compile(ur"</?[^t/][^>]*>", re.I)
re_fix_missing_table = re.compile(ur'(<td>\W*)$', re.I)
cl_html_except_tables = lambda x: re_fix_missing_table.sub(r'\1</td></tr></tbody></table>', re_cl_html_except_tables.sub('', x)).strip().replace('> ', '>').replace(' <', '<').replace('<td><tr>', '<td></td></tr><tr>')
re_cl_par  = re.compile(ur"[()]")
re_cl_uno  = re.compile(ur"(premie?r?|unique?)", re.I)
re_cl_sec_uno = re.compile(ur"^[Ii1][eE][rR]?")
re_mat_sec = re.compile(ur"%s(\s+(.+)e?r?)" % section_titles, re.I)
re_mat_n = re.compile(ur"((pr..?)?limin|unique|premier|[IVX\d]+)", re.I)
re_mat_art = re.compile(ur"articles?\s*([^(]*)(\([^)]*\))?$", re.I)
re_mat_ppl = re.compile(ur"(<b>)?pro.* loi", re.I)
re_mat_tco = re.compile(ur"\s*<b>\s*(ANNEXE[^:]*:\s*|\d+\)\s+)?TEXTES?\s*(ADOPTÉS?\s*PAR|DE)\s*LA\s*COMMISSION.*</b>\s*$")
re_mat_exp = re.compile(ur"(<b>)?expos[eéÉ]", re.I)
re_mat_end = re.compile(ur"((<i>)?Délibéré en|(<i>)?NB[\s:<]+|(<b>)?RAPPORT ANNEX|Fait à .*, le|\s*©|\s*N.?B.?\s*:|(</?i>)*<a>[1*]</a>\s*(</?i>)*\(\)(</?i>)*|<i>\(1\)\s*Nota[\s:]+|<a>\*</a>\s*(<i>)?1)", re.I)
re_mat_ann = re.compile(ur"\s*<b>\s*ANNEXES?[\s<]+")
re_mat_dots = re.compile(ur"^(<i>)?[.…]+(</i>)?$")
re_mat_st = re.compile(ur"(<i>|\()+\s*(conform|non[\s\-]*modif|suppr|nouveau).{0,10}$", re.I)
re_mat_new = re.compile(ur"\s*\(\s*nouveau\s*\)\s*", re.I)
re_mat_texte = re.compile(ur'\(texte (modifié|élaboré|d(u|e l))', re.I)
re_mat_single_char = re.compile(ur'^\s*[LMN]\s*$')
re_clean_idx_spaces = re.compile(ur'^([IVXLCDM0-9]+)\s*\.\s*')
re_clean_art_spaces = re.compile(ur'^\s*("?)\s+')
re_clean_art_spaces2 = re.compile(ur'\s+\.\s*-\s+')
re_clean_conf = re.compile(ur"\((conforme|non[\s-]*modifi..?)s?\)", re.I)
re_clean_supr = re.compile(ur'\((dispositions?\s*d..?clar..?es?\s*irrecevable.*article 4.*Constitution.*|(maintien de la )?suppr(ession|im..?s?)(\s*(conforme|maintenue|par la commission mixte paritaire))*)\)["\s]*$', re.I)
re_echec_hemi = re.compile(ur"L('Assemblée nationale|e Sénat) (a rejeté|n'a pas adopté)[, ]+", re.I)
re_echec_hemi2 = re.compile(ur"de loi a été rejetée par l('Assemblée nationale|e Sénat)\.$", re.I)
re_echec_com = re.compile(ur" la commission .*(effet est d'entraîner le rejet|demande de rejeter|a rejeté|n'a pas adopté)[dleau\s]*(projet|proposition|texte)[.\s]", re.I)
re_echec_cmp = re.compile(ur" (a conclu à l'échec de ses travaux|(ne|pas) .*parven(u[es]?|ir) à (élaborer )?un texte commun)", re.I)
re_rap_mult = re.compile(ur'[\s<>/ai]*N[°\s]*\d+\s*(,|et)\s*[N°\s]*\d+', re.I)
re_src_mult = re.compile(ur'^- L(?:A PROPOSITION|E PROJET) DE LOI n°\s*(\d+)\D')
re_clean_mult_1 = re.compile(ur'\s*et\s*', re.I)
re_clean_mult_2 = re.compile(ur'[^,\d]', re.I)
re_clean_footer_notes = re.compile(ur"[\.\s]*\(*\d*\([\d\*]+[\)\d\*\.\s]*$")
re_sep_text = re.compile(ur'\s*<b>\s*(article|%s)\s*(I|uniqu|pr..?limina|1|prem)[ier]*\s*</b>\s*$' % section_titles, re.I)
re_stars = re.compile(ur'^[\s*_]+$')
re_art_uni = re.compile(ur'\s*article\s*unique\s*$', re.I)
re_all_caps = re.compile(ur'[A-Z' + upcase_accents + ur' ]+')
section = {"type": "section", "id": ""}

def parse_bill(string, url):
    section_id = ""
    curtext = -1
    srclst = []
    article = None
    read = art_num = ali_num = 0
    indextext = -1

    definitif = re_definitif.search(string) is not None
    soup = BeautifulSoup(string, "html5lib")

    texte = {
        "type": "projet de loi",
        "definitive": definitif,
        "articles": [],
        "url": url,
        "expose": ""
    }
    expose = False

    if url:
        url = re.sub(r"^.*/http", "http", url)
        url = re.sub(r"%3A", ":", re.sub(r"%2F", "/", url))
        # Generate Senat or AN ID from URL
        if "legifrance.gouv.fr" in url:
            m = re.search(r"cidTexte=(JORFTEXT\d+)(\D|$)", url, re.I)
            texte["id"] = ORDER + m.group(1)
        elif re.search(r"assemblee-?nationale", url, re.I):
            m = re.search(r"/(\d+)/.+/(ta)?[\w\-]*(\d{4})[\.\-]", url, re.I)
            numero = int(m.group(3))
            texte["id"] = ORDER+"A" + m.group(1) + "-"
            if m.group(2) is not None:
                texte["id"] += m.group(2)
            texte["id"] += str(numero)
        else:
            m = re.search(r"(ta|l)?s?(\d\d)-(\d{1,3})\d?\.", url, re.I)
            if m is None:
                m = re.search(r"/(-)?20(\d+)-\d+/(\d+).html", url, re.I)
            numero = int(m.group(3))
            texte["id"] = ORDER+"S" + m.group(2) + "-"
            if m.group(1) is not None:
                texte["id"] += m.group(1)
            texte["id"] += "%03d" % numero

    is_html = string.find('<html>') == 0 or string.find('<?xml version="1.0" encoding="UTF-8"?>') == 0
    lines = soup.body.find_all('p') if is_html else string.split(u'\n')

    if is_html:
        texte["type"] = (re_clean_title_legif.sub('', soup.title.string.strip()) if soup.title else "").lower()

    for line in lines:
        line = clean_html(line.text if is_html else line)

        if re_stars.match(line):
            continue

        match = re.compile(ur'^N°\D+(\d+)$', re.MULTILINE).search(line)
        if match:
            texte['id'] = int(match.group(1))

        match = re.compile(ur'^(.*) LÉGISLATURE$', re.MULTILINE).search(line)
        if match:
            texte['legislature'] = word_to_number(match.group(1))

        match = re.compile(ur'Enregistré à la Présidence (du |de l\')(.*) le (\d+) (\w+) (\d{4})').search(line)
        if match:
            texte['date'] = match.group(5) + '-' + str(month_to_number(match.group(4))) + '-' + match.group(3)
            texte['place'] = match.group(2).lower()

        if line == 'PROPOSITION DE LOI':
            texte['type'] = line.lower()

        if 'description' not in texte and line in [u'PROPOSITION DE LOI', u'PROJET DE LOI']:
            texte['description'] = line.lower()
            read = 3
            continue
        if read == 3:
            if real_lower(line).startswith(u'transmise par') or real_lower(line).startswith(u'présentée par'):
                read = 0
            else:
                if re_all_caps.match(line):
                    line = real_lower(line)
                line = line.replace(',', '')
                if line:
                    texte['description'] += ' ' + line
            continue

        if line == "<b>RAPPORT</b>" or line == "Mesdames, Messieurs,":
            read = -1
        if (srclst or indextext != -1) and re_sep_text.match(line):
            curtext += 1
            art_num = 0
        srcl = re_src_mult.search(line)
        cl_line = re_cl_html.sub("", line).strip()
        if srcl and read < 1:
            srclst.append(int(srcl.group(1)))
            continue
        elif re_rap_mult.match(line):
            line = cl_line
            line = re_clean_mult_1.sub(",", line)
            line = re_clean_mult_2.sub("", line)
            cl_line = re_cl_html.sub("", line).strip()
            for n_t in line.split(','):
                indextext += 1
                if int(n_t) == numero:
                    break
        elif re_mat_ppl.match(line) or re_mat_tco.match(line):
            read = 0
            texte = save_text(texte)
        elif re_mat_exp.match(line):
            read = -1 # Deactivate description lecture
            expose = True
        elif re_echec_cmp.search(cl_line) or re_echec_com.search(cl_line) or re_echec_hemi.match(cl_line) or re_echec_hemi2.search(cl_line):
            texte = save_text(texte)
            cleanup({"type": "echec", "texte": cl_line})
            break
        elif read == -1 or (indextext != -1 and curtext != indextext):
            continue

        # Identify section zones
        m = re_mat_sec.match(line)
        if m:
            read = 1 # Activate titles lecture
            section["type_section"] = real_lower(m.group(1))
            section_typ = m.group(1).upper()[0]
            if m.group(3) is not None:
                section_typ += "S"

            if " LIMINAIRE" in line:
                section_num = "L"
            else:
                section_num = re_cl_uno.sub('1', re_cl_sec_uno.sub('1', re_cl_html.sub('', m.group(5).strip())).strip())
                section_num = re_clean_bister.sub(lambda m: m.group(1)+" "+real_lower(m.group(2)), section_num)
                section_num = re_mat_new.sub('', section_num).strip()
                m2 = re_mat_romans.match(section_num)
                if m2:
                    rest = section_num.replace(m2.group(0), '')
                    section_num = romans(m2.group(0))
                    if rest: section_num = str(section_num) + rest
            # Get parent section id to build current section id
            section_par = re.sub(r""+section_typ+"[\dL].*$", "", section["id"])
            section["id"] = section_par + section_typ + str(section_num)

        # Identify titles and new article zones
        elif (not expose and re_mat_end.match(line)) or (read == 2 and re_mat_ann.match(line)):
            break
        elif re.match(r"(<i>)?<b>", line) or re_art_uni.match(line) or re.match(r"^Articles? ", line):
            line = cl_line
            # Read a new article
            if re_mat_art.match(line):
                if article is not None:
                    texte = save_text(texte)
                    cleanup(article)
                read = 2 # Activate alineas lecture
                expose = False
                art_num += 1
                ali_num = 0
                article = {"type": "article", "order": art_num, "alineas": {}, "statut": "none"}
                texte['articles'].append(article)
                if srclst:
                    article["source_text"] = srclst[curtext]
                m = re_mat_art.match(line)
                article["titre"] = re_cl_uno.sub("1er", re_cl_sec_uno.sub("1er", m.group(1).strip())).strip(" -'")
                if m.group(2) is not None:
                    article["statut"] = re_cl_par.sub("", real_lower(m.group(2))).strip()
                if section["id"] != "":
                    article["section"] = section["id"]
            # Read a section's title
            elif read == 1:
                texte = save_text(texte)
                section["titre"] = lower_but_first(line)
                if article is not None:
                    cleanup(article)
                    article = None
                cleanup(section)
                read = 0

        # Read articles with alineas
        if read == 2 and not m:
            # Find extra status information
            if ali_num == 0 and re_mat_st.match(line):
                article["statut"] = re_cl_html.sub("", re_cl_par.sub("", real_lower(line)).strip())
                continue
            if re_mat_dots.match(line):
                continue
            if "<table>" in line:
                cl_line = cl_html_except_tables(line)
            line = re_clean_art_spaces2.sub('. - ', re_clean_art_spaces.sub(r'\1', re_clean_idx_spaces.sub(r'\1. ', re_mat_new.sub(" ", cl_line).strip())))
            # Clean low/upcase issues with BIS TER etc.
            line = line.replace("oeUVRE", "OEUVRE")
            line = clean_full_upcase(line)
            line = re_clean_premier.sub(lambda m: (real_lower(m.group(0)) if m.group(1) else "")+m.group(3)+"er", line)
            line = re_clean_bister.sub(lambda m: m.group(1)+" "+real_lower(m.group(2)), line)
            # Clean different versions of same comment.
            line = re_clean_supr.sub('(Supprimé)', line)
            line = re_clean_conf.sub('(Non modifié)', line)
            line = re_clean_coord.sub('', line)
            line = re_clean_subsec_space.sub(r'\1\4 \5', line)
            line = re_clean_subsec_space2.sub(r'\1 \2 \3\4', line)
            line = re_clean_punc_space.sub(r'\1 \2', line)#.encode('utf-8')
            line = re_clean_spaces.sub(' ', line)
            line = re_mat_sec.sub(lambda x: lower_but_first(x.group(1))+x.group(4) if re_mat_n.match(x.group(4)) else x.group(0), line)
            line = re_clean_footer_notes.sub(".", line)
            # Clean comments (Texte du Sénat), (Texte de la Commission), ...
            if ali_num == 0 and re_mat_texte.match(line):
                continue
            line = re_mat_single_char.sub("", line)
            line = line.strip()
            if line:
                ali_num += 1
                # match alinea numbering in the form of "(ali_num) actual alinea content goes here..."
                m = re.compile(ur"^\((\d)\) (.*)$", re.MULTILINE).match(line)
                if m:
                    ali_num = int(m.group(1))
                    line = m.group(2)
                article["alineas"]["%03d" % ali_num] = line
        else:
            #metas
            continue

    # save_text(texte)
    cleanup(texte)

    return texte
