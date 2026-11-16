"""Gera os PDFs EM BRANCO dos laudos (formulários preenchíveis) e o modelo do laudo consolidado.

Nenhum dado é preenchido aqui: os campos ficam vazios para serem preenchidos por pessoas reais.
Dependência (somente para gerar): pip install reportlab
Uso:  python docs/laudos/gerar_pdfs.py
Saída: docs/laudos/pdf/formulario-avaliador-1..5.pdf e docs/laudos/pdf/laudo-consolidado-MODELO.pdf
"""
from pathlib import Path

from reportlab.lib.colors import Color, black, HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

OUT = Path(__file__).resolve().parent / "pdf"
W, H = A4
M = 40
CW = W - 2 * M
GREY = HexColor("#667085")
LINE = HexColor("#c9ced6")
BLUE = HexColor("#2f5fd0")

FUNCS = [
    "Dashboard com indicadores",
    "Cadastro, edição, busca e exclusão de clientes",
    "Cadastro, edição e exclusão de serviços (preço e duração)",
    "Criar agendamento",
    "Editar agendamento",
    "Remarcar agendamento",
    "Cancelar agendamento",
    "Bloqueio de horário conflitante",
    "Validação de formulários e mensagens de erro",
    "Uso no celular (layout)",
]
NOTES = ["Facilidade de uso", "Clareza das mensagens", "Aparência/layout", "Desempenho percebido", "Confiança de que a agenda está correta"]
OPTS = ["Sucesso", "Falha", "Parcial", "Não testei"]


class Doc:
    def __init__(self, path: Path, title: str):
        self.c = canvas.Canvas(str(path), pagesize=A4, pageCompression=1)
        self.c.setTitle(title)
        self.c.setAuthor("AgendaPro")
        self.title = title
        self.n = 0
        self.fid = 0
        self.y = 0
        self.new_page()

    # ---- infraestrutura ----
    def new_page(self):
        if self.n:
            self.footer()
            self.c.showPage()
        self.n += 1
        self.y = H - M
        self.c.setFont("Helvetica", 8)
        self.c.setFillColor(GREY)
        self.c.drawString(M, H - 24, self.title)
        self.c.setFillColor(black)
        self.y = H - 46

    def footer(self):
        self.c.setFont("Helvetica", 8)
        self.c.setFillColor(GREY)
        self.c.drawString(M, 22, "AgendaPro - Projeto Integrador Transdisciplinar em Engenharia de Software II")
        self.c.drawRightString(W - M, 22, f"Página {self.n}")
        self.c.setFillColor(black)

    def need(self, h):
        if self.y - h < 40:
            self.new_page()

    def save(self):
        self.footer()
        self.c.save()

    def name(self, prefix="f"):
        self.fid += 1
        return f"{prefix}{self.fid}"

    # ---- elementos ----
    def h1(self, text):
        self.c.setFont("Helvetica-Bold", 16)
        self.c.drawString(M, self.y, text)
        self.y -= 22

    def h2(self, text):
        self.need(40)
        self.y -= 6
        self.c.setFillColor(BLUE)
        self.c.setFont("Helvetica-Bold", 11)
        self.c.drawString(M, self.y, text)
        self.c.setFillColor(black)
        self.c.setStrokeColor(LINE)
        self.c.line(M, self.y - 4, W - M, self.y - 4)
        self.y -= 18

    def para(self, text, size=9, color=black, bold=False):
        font = "Helvetica-Bold" if bold else "Helvetica"
        self.c.setFont(font, size)
        self.c.setFillColor(color)
        for line in simpleSplit(text, font, size, CW):
            self.need(size + 4)
            self.c.drawString(M, self.y, line)
            self.y -= size + 3
        self.c.setFillColor(black)
        self.y -= 2

    def box(self, text, color=HexColor("#fef3f2"), border=HexColor("#b42318")):
        lines = simpleSplit(text, "Helvetica-Bold", 9, CW - 12)
        h = len(lines) * 12 + 10
        self.need(h + 6)
        self.c.setFillColor(color)
        self.c.setStrokeColor(border)
        self.c.rect(M, self.y - h + 4, CW, h, fill=1, stroke=1)
        self.c.setFillColor(black)
        self.c.setFont("Helvetica-Bold", 9)
        yy = self.y - 8
        for ln in lines:
            self.c.drawString(M + 6, yy, ln)
            yy -= 12
        self.y -= h + 6

    def text(self, x, y, w, h, tip="", multiline=False, name=None):
        self.c.acroForm.textfield(
            name=name or self.name(), tooltip=tip, x=x, y=y, width=w, height=h,
            borderStyle="solid", borderColor=LINE, fillColor=Color(1, 1, 1), textColor=black,
            fontName="Helvetica", fontSize=9, forceBorder=True,
            fieldFlags="multiline" if multiline else "",
        )

    def check(self, x, y, size=11, tip=""):
        self.c.acroForm.checkbox(
            name=self.name("c"), tooltip=tip, x=x, y=y, size=size, borderColor=GREY,
            fillColor=Color(1, 1, 1), textColor=black, forceBorder=True, checked=False,
        )

    def labeled(self, label, h=18, w=CW, tip=None, multiline=False):
        """Rótulo acima + campo."""
        self.need(h + 16)
        self.c.setFont("Helvetica", 8)
        self.c.setFillColor(GREY)
        self.c.drawString(M, self.y, label)
        self.c.setFillColor(black)
        self.text(M, self.y - 4 - h, w, h, tip or label, multiline)
        self.y -= h + 16

    def pair(self, l1, l2, h=18):
        self.need(h + 16)
        half = (CW - 10) / 2
        for i, lab in enumerate((l1, l2)):
            x = M + i * (half + 10)
            self.c.setFont("Helvetica", 8)
            self.c.setFillColor(GREY)
            self.c.drawString(x, self.y, lab)
            self.c.setFillColor(black)
            self.text(x, self.y - 4 - h, half, h, lab)
        self.y -= h + 16


def formulario(n: int):
    d = Doc(OUT / f"formulario-avaliador-{n}.pdf", f"Laudo de Avaliação - Avaliador {n} de 5")
    c = d.c
    d.h1(f"Laudo de Avaliação - Avaliador {n} de 5")
    d.para("Sistema avaliado: AgendaPro (MVP acadêmico de agendamentos). Preencha este formulário com SUAS observações reais, depois de usar o sistema. "
           "Use apenas dados fictícios nos testes. Os campos podem ser digitados no leitor de PDF ou impressos e escritos à mão.", 9, GREY)
    d.box("Preenchimento exclusivo do avaliador. A equipe não deve preencher, alterar ou completar as respostas.")

    d.h2("1. Identificação")
    d.labeled("Nome completo do avaliador")
    d.pair("Data da avaliação (dd/mm/aaaa)", "Perfil (empreendedor, estudante, outro)")
    d.pair("Dispositivo (computador / celular / tablet)", "Navegador e versão (se souber)")
    d.pair("Versão testada (commit ou data da demonstração)", "Duração aproximada da avaliação")
    d.need(24)
    c.setFont("Helvetica", 9)
    d.check(M, d.y - 10, tip="Autoriza citar o nome")
    c.drawString(M + 16, d.y - 8, "Autorizo citar meu nome no relatório e no vídeo")
    d.check(M + 300, d.y - 10, tip="Não autoriza citar o nome")
    c.drawString(M + 316, d.y - 8, "Prefiro permanecer anônimo(a)")
    d.y -= 26
    d.para("Campos adicionais exigidos pela instituição (curso, turma, RA, etc.): preencher abaixo SOMENTE se o AVA/professor exigir.", 8, GREY)
    d.labeled("Outros dados exigidos pela instituição (se houver)", 30, multiline=True)

    d.h2("2. Funcionalidades testadas")
    d.para("Marque UMA opção por linha e comente quando quiser. Marque 'Não testei' se não usou.", 8, GREY)
    # cabeçalho da tabela
    cols = [M + 232, M + 280, M + 316, M + 358]  # x dos checkboxes
    c.setFont("Helvetica-Bold", 7)
    for x, o in zip(cols, OPTS):
        c.drawString(x - 4, d.y, o)
    c.drawString(M + 408, d.y, "Comentário")
    d.y -= 10
    for f in FUNCS:
        d.need(28)
        c.setFont("Helvetica", 8.5)
        lines = simpleSplit(f, "Helvetica", 8.5, 220)
        for i, ln in enumerate(lines):
            c.drawString(M, d.y - 8 - i * 10, ln)
        for x, o in zip(cols, OPTS):
            d.check(x, d.y - 11, 11, tip=f"{f}: {o}")
        d.text(M + 408, d.y - 14, CW - 408, 18, f"Comentário: {f}")
        c.setStrokeColor(LINE)
        c.line(M, d.y - 20, W - M, d.y - 20)
        d.y -= 26

    d.h2("3. O que funcionou bem")
    d.labeled("Descreva com suas palavras", 60, multiline=True)

    d.h2("4. Falhas encontradas")
    d.para("Para cada falha: onde ocorreu, passos para reproduzir, o que esperava, o que aconteceu e a gravidade (Baixa, Média, Alta ou Crítica).", 8, GREY)
    for i in (1, 2, 3):
        d.pair(f"Falha {i} - onde ocorreu", f"Falha {i} - gravidade")
        d.labeled(f"Falha {i} - passos para reproduzir", 30, multiline=True)
        d.pair(f"Falha {i} - o que esperava", f"Falha {i} - o que aconteceu", 30)
    d.para("Se houver mais falhas, descreva-as no campo 'Observações adicionais' (seção 8).", 8, GREY)

    d.h2("5. O que você NÃO testou (e por quê)")
    d.labeled("Descreva", 40, multiline=True)

    d.h2("6. Sugestões de melhoria")
    d.labeled("Descreva", 60, multiline=True)

    d.h2("7. Avaliação de qualidade (nota de 1 a 5, sendo 5 = excelente)")
    for label in NOTES:
        d.need(22)
        c.setFont("Helvetica", 9)
        c.drawString(M, d.y - 8, label)
        d.text(M + 300, d.y - 14, 50, 18, f"Nota: {label}")
        d.y -= 24

    d.h2("8. Evidências e observações adicionais")
    d.labeled("Arquivos anexados (capturas de tela, gravações) com legenda curta", 40, multiline=True)
    d.labeled("Observações adicionais", 60, multiline=True)

    d.h2("9. Declaração")
    d.para("Declaro que as respostas acima refletem a minha avaliação real do sistema, feita por mim.", 9)
    d.pair("Nome / rubrica do avaliador", "Data")

    d.h2("10. Tratamento pela equipe (preenchido depois, pela equipe)")
    d.pair("ID(s) no registro de falhas (docs/07-pendencias.md)", "Commit(s) da correção")
    d.labeled("Reteste realizado (data e resultado real)", 22)
    d.save()


def consolidado():
    d = Doc(OUT / "laudo-consolidado-MODELO.pdf", "Laudo de Qualidade Consolidado - AgendaPro (MODELO)")
    c = d.c
    d.h1("Laudo de Qualidade Consolidado - AgendaPro")
    d.box("MODELO EM BRANCO - AGUARDANDO DADOS REAIS DOS 5 AVALIADORES. Não preencher com dados simulados. "
          "Só concluir após receber os cinco formulários preenchidos pelos próprios avaliadores.")

    d.h2("1. Identificação do projeto")
    d.pair("Projeto", "Disciplina")
    d.pair("Integrantes da equipe", "Professor(a)")
    d.pair("Repositório (URL)", "Versão / commit avaliado")
    d.labeled("Outros campos exigidos pelo AVA (preencher somente se confirmados)", 30, multiline=True)

    d.h2("2. Avaliadores (um por linha; copiar dos formulários recebidos)")
    heads = ["Nº", "Nome (se autorizado)", "Data", "Dispositivo/navegador", "Autoriza nome?"]
    xs = [M, M + 24, M + 190, M + 250, M + 430]
    ws = [22, 164, 58, 178, CW - 430]
    c.setFont("Helvetica-Bold", 8)
    for x, h in zip(xs, heads):
        c.drawString(x, d.y, h)
    d.y -= 6
    for i in range(1, 6):
        d.need(24)
        c.setFont("Helvetica", 9)
        c.drawString(xs[0] + 6, d.y - 14, str(i))
        for x, w, h in zip(xs[1:], ws[1:], heads[1:]):
            d.text(x, d.y - 20, w, 18, f"Avaliador {i}: {h}")
        d.y -= 24
    d.y -= 4

    d.h2("3. Resultado por funcionalidade e avaliador")
    d.para("Legenda: S = sucesso, F = falha, P = parcial, NT = não testou. Copiar fielmente dos formulários.", 8, GREY)
    c.setFont("Helvetica-Bold", 8)
    for i in range(5):
        c.drawString(M + 262 + i * 34, d.y, f"Av.{i + 1}")
    c.drawString(M + 440, d.y, "Observação")
    d.y -= 8
    for f in FUNCS:
        d.need(24)
        c.setFont("Helvetica", 8.5)
        for k, ln in enumerate(simpleSplit(f, "Helvetica", 8.5, 250)):
            c.drawString(M, d.y - 11 - k * 10, ln)
        for i in range(5):
            d.text(M + 262 + i * 34, d.y - 20, 30, 18, f"{f} - avaliador {i + 1}")
        d.text(M + 440, d.y - 20, CW - 440, 18, f"Observação: {f}")
        d.y -= 24

    d.h2("4. Falhas consolidadas")
    d.para("Uma linha por falha distinta relatada; indicar quais avaliadores a relataram.", 8, GREY)
    h4 = ["ID", "Descrição", "Avaliadores", "Gravidade", "Situação (corrigida/pendente)", "Commit"]
    x4 = [M, M + 28, M + 190, M + 250, M + 300, M + 430]
    w4 = [26, 160, 58, 48, 128, CW - 430]
    c.setFont("Helvetica-Bold", 7.5)
    for x, h in zip(x4, h4):
        c.drawString(x, d.y, h)
    d.y -= 6
    for r in range(1, 7):
        d.need(24)
        for x, w, h in zip(x4, w4, h4):
            d.text(x, d.y - 20, w, 18, f"Falha {r}: {h}")
        d.y -= 24

    d.h2("5. Notas de qualidade (1 a 5) - copiar e calcular a média real")
    for lab in NOTES:
        d.need(22)
        c.setFont("Helvetica", 8.5)
        c.drawString(M, d.y - 10, lab)
        for i in range(5):
            d.text(M + 222 + i * 40, d.y - 16, 36, 18, f"{lab} - avaliador {i + 1}")
        d.text(M + 430, d.y - 16, 60, 18, f"Média: {lab}")
        d.y -= 24
    c.setFont("Helvetica", 7.5)
    c.setFillColor(GREY)
    c.drawString(M + 222, d.y + 4, "Av.1      Av.2      Av.3      Av.4      Av.5                       Média")
    c.setFillColor(black)
    d.y -= 6

    d.h2("6. Principais sugestões recebidas")
    d.labeled("Resumo fiel das sugestões (indicar quais foram implementadas)", 70, multiline=True)

    d.h2("7. Análise de qualidade")
    d.labeled("Pontos fortes observados pelos avaliadores", 50, multiline=True)
    d.labeled("Pontos fracos e riscos observados", 50, multiline=True)
    d.labeled("Correções realizadas após a avaliação (com referência ao commit) e reteste", 50, multiline=True)

    d.h2("8. Conclusão da equipe")
    d.labeled("Conclusão baseada apenas nos resultados reais acima", 60, multiline=True)
    d.pair("Local e data", "Assinatura/identificação da equipe")
    d.save()


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for i in range(1, 6):
        formulario(i)
    consolidado()
    print("PDFs gerados em", OUT)
