import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.platypus import Table


class EOB:
    """
    EOB loosely based on AETNA example found here:
    https://ctmirror.org/2014/09/02/what-is-this-form-the-explanation-of-benefits/
    """

    #----------------------------------------------------------------------
    def __init__(self, pdf_file):
        """"""
        self.canvas = canvas.Canvas(pdf_file, pagesize=letter)
        self.styles = getSampleStyleSheet()
        self.width, self.height = letter

    #----------------------------------------------------------------------
    def coord(self, x, y, unit=1):
        x, y = x * unit, self.height -  y * unit
        return x, y

    #----------------------------------------------------------------------
    def create_header(self):
        """"""
        ptext = '<font size=10><b>Statement Date: {}' \
            '</b></font>'.format('01/01/2017')
        p = Paragraph(ptext, self.styles["Normal"])
        p.wrapOn(self.canvas, self.width, self.height)
        p.drawOn(self.canvas, *self.coord(145, 14, mm))

        ptext = '''<font size=10>
        <b>Member:</b> {member}<br/>
        <b>Member ID:</b> {member_id}<br/>
        <b>Group #:</b> {group_num}<br/>
        <b>Group name:</b> {group_name}<br/>
        </font>
        '''.format(member='MIKE D',
                   member_id='X123456',
                   group_num=789456-1235,
                   group_name='PYTHON CORP'
                   )
        p = Paragraph(ptext, self.styles["Normal"])
        p.wrapOn(self.canvas, self.width, self.height)
        p.drawOn(self.canvas, *self.coord(145, 35, mm))

    #----------------------------------------------------------------------
    def create_bold_text(self, text, size=8):
        """"""
        return Paragraph('''<font size={size}><b>
        {text}</b></font>
        '''.format(size=size, text=text),
           self.styles['Normal'])

    #----------------------------------------------------------------------
    def create_payment_summary(self):
        """"""
        ptext = '<font size=26>Your payment summary</font>'
        p = Paragraph(ptext, self.styles["Normal"])
        p.wrapOn(self.canvas, self.width, self.height)
        p.drawOn(self.canvas, *self.coord(15, 47, mm))

        colWidths = [75, 125, 50, 125, 50, 150]
        plan_title = Paragraph(
            '<font size=8>Your plan paid</font>',
            self.styles["Normal"])
        owe_title = Paragraph(
            '<font size=8>You owe or already paid</font>',
            self.styles["Normal"])

        data = [['', '', '', plan_title, '', owe_title],
                [self.create_bold_text('Patient'),
                 self.create_bold_text('Provider'),
                 self.create_bold_text('Amount'),
                 self.create_bold_text('Sent to'),
                 self.create_bold_text('Date'),
                 self.create_bold_text('Amount'),
                 ]]
        table = Table(data, colWidths=colWidths)
        table.wrapOn(self.canvas, self.width, self.height)
        table.drawOn(self.canvas, 20, 600)

    #----------------------------------------------------------------------
    def create_claims(self):
        """"""
        pass

    #----------------------------------------------------------------------
    def save(self):
        """"""
        self.canvas.save()


#----------------------------------------------------------------------
def main(pdf_file):
    """"""
    eob = EOB(pdf_file)
    eob.create_header()
    eob.create_payment_summary()
    eob.create_claims()
    eob.save()


if __name__ == '__main__':
    pdf_file = "eob.pdf"
    main(pdf_file)