from datetime import datetime
import pandas as pd
from fpdf import FPDF

pd.options.mode.chained_assignment = None  # default='warn'


class PDF(FPDF):
    def header(self):
        # Logo
        self.image(r"img_ae_logo_c_230.png", 10, 8, 33)
        # Arial bold 15
        self.set_font('Times', 'B', 20)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Concrete Test Report Summary', 0, 0, 'C')
        self.cell(80)
        self.set_font('Times', '', 11)
        self.cell(0, 4, 'Arun Kishore', 0, 1, 'R')
        self.cell(0, 4, datetime.now().strftime('%B %d, %Y'), 0, 0, 'R')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Times', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def draw_table(self, header, data, cell_width, heading='', subheading=''):
        """Draws a table in PDF based on provided input

        Args:
            pdf (<FPDF class>): _description_
            header (tuple): A tuple with header row values
            data (Array of Arrays): Array with table data
            cell_width (Array): Array of int with col widths
            heading (str, optional): Table Title. Defaults to ''.
            subheading (str, optional): Table subtitle. Defaults to ''.
        """
        #print(header)
        #print(data)
        effective_page_width = self.w - 2*self.l_margin
        cell_offset = (effective_page_width - sum(cell_width))/2

        if heading != '':
            self.set_font('Times', 'B', 14)
            self.cell(w=0, h=5, txt=heading, ln=1, align='C')

        if subheading != '':
            self.set_font('Times', 'I', 10)
            self.cell(w=0, h=4, txt=subheading, ln=1, align='C')

        if cell_offset > 0:
            self.cell(cell_offset)

        self.set_font('Times', 'B', 10)
        for i, datum in enumerate(header):
            self.cell(cell_width[i], self.font_size * 1.5, datum, border=1,align='C')
        self.ln(self.font_size * 1.5)

        self.set_font('Times', '', 10)
        for row in data:
            if cell_offset > 0:
                self.cell(cell_offset)
            for i, datum in enumerate(row):
                self.cell(cell_width[i], self.font_size * 1.5, str(datum), border=1,align='C')
            self.ln(self.font_size * 1.5)
        self.ln(self.font_size * 1.5)
    
