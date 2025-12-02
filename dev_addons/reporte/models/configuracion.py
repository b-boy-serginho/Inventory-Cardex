from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from num2words import num2words


class Configuracion(models.Model):
    _inherit = 'account.move'

    terms_and_conditions = fields.Text(
        'Términos y condiciones')  # Aquí agregamos el campo
    razon_social_micelaneo_id = fields.Many2one(
        comodel_name='res.partner', string='Razón Social', store=True)

    def number_to_word(self, number: float):
        decimal_part = int(round(number % 1, 2) * 100)
        integer_part = int(number)
        # get actual language
        lang = self.env.context.get('lang', 'es_ES')
        return f"{num2words(integer_part, lang=lang)} con {decimal_part}/100 {self.currency_id.symbol}"
    codigo_A1_or_A2 = fields.Char(
        string='Código A1 o A2',
        compute='_compute_codigo_fiscal',
        store=False
    )

    @api.depends('company_id.company_registry')
    def _compute_codigo_fiscal(self):
        for record in self:
            if record.company_id.company_registry == '100':
                record.codigo_A1_or_A2 = "A1"
            elif record.company_id.company_registry == '200':
                record.codigo_A1_or_A2 = "A2"
            else:
                record.codigo_A1_or_A2 = ""

    
    correlativo = fields.Char(
        string='Correlativo',
        store=True,
        readonly=True,
        copy=False,
    )

    def _compute_correlativo(self):
        for record in self:
            if not record.date or not record.journal_id or not record.company_id:
                record.correlativo = ''
                continue

            mes = record.date.strftime('%m')
            start_of_month = record.date.replace(day=1)
            end_of_month = start_of_month + relativedelta(months=1)

            domain = [
                ('date', '>=', start_of_month),
                ('date', '<', end_of_month),
                ('journal_id.type', '=', record.journal_id.type),
                ('company_id', '=', record.company_id.id),
                ('id', '!=', record.id),
                ('correlativo', '!=', False),
            ]

            moves = self.env['account.move'].search(domain)
            numeros_existentes = []
            for m in moves:
                if m.correlativo and '-' in m.correlativo:
                    try:
                        num = int(m.correlativo.split('-')[1])
                        numeros_existentes.append(num)
                    except Exception:
                        pass

            max_num = max(numeros_existentes) if numeros_existentes else 0
            numero = max_num + 1
            secuencia = str(numero).zfill(4)

            record.correlativo = f"{mes}-{secuencia}"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            record._compute_correlativo()
        return records

    def action_post(self):
        res = super().action_post()
        for record in self:
            record._compute_correlativo()
        return res



    # @api.depends('date', 'journal_id', 'journal_id.type', 'company_id')
    # def _compute_mes_secuencia(self):
    #     for record in self:
    #         if record.date and record.journal_id and record.journal_id.type:
    #             mes = record.date.strftime('%m')
    #             start_of_month = record.date.replace(day=1)
    #             end_of_month = start_of_month + relativedelta(months=1)

    #             domain = [
    #                 ('date', '>=', start_of_month),
    #                 ('date', '<', end_of_month),
    #                 ('journal_id.type', '=', record.journal_id.type),
    #                 ('company_id', '=', record.company_id.id),
    #             ]
    #             if record.id:
    #                 domain.append(('id', '!=', record.id))

    #             ultimo_numero = self.env['account.move'].search_count(domain) + 1
    #             secuencial = f"{ultimo_numero:05d}"
    #             record.mes_secuencia = f"-{mes}-{secuencial}"
    #         else:
    #             record.mes_secuencia = ''

    # @api.model_create_multi
    # def create(self, vals_list):
    #     # Crear los asientos contables
    #     records = super(Configuracion, self).create(vals_list)

    #     # Agrupar por mes, diario específico (journal_id.id) y compañía
    #     grouped_records = {}
    #     for record in records:
    #         if record.date and record.journal_id and record.journal_id.id:
    #             mes = record.date.strftime('%m')
    #             key = (mes, record.journal_id.id, record.company_id.id)
    #             if key not in grouped_records:
    #                 grouped_records[key] = []
    #             grouped_records[key].append(record)

    #     # Asignar secuencias únicas por grupo
    #     for key, group in grouped_records.items():
    #         mes, journal_id, company_id = key
    #         start_of_month = group[0].date.replace(day=1)
    #         end_of_month = start_of_month + relativedelta(months=1)

    #         domain = [
    #             ('date', '>=', start_of_month),
    #             ('date', '<', end_of_month),
    #             ('journal_id', '=', journal_id),
    #             ('company_id', '=', company_id),
    #         ]

    #         # Contar ya existentes con ese diario
    #         ultimo_numero = self.env['account.move'].search_count(domain)

    #         for index, record in enumerate(group, start=ultimo_numero + 1):
    #             secuencial = f"{index:05d}"
    #             record.mes_secuencia = f"-{mes}-{secuencial}"

    #     return records

    

    
  

    # @api.depends('date', 'journal_id', 'journal_id.type', 'company_id')
    # def _compute_mes_secuencia(self):
    #     for record in self:
    #         record.mes_secuencia = ''  # Vacío hasta que se publique

    # def action_post(self):
    #     for record in self:
    #         if record.date and record.journal_id and record.journal_id.type:
    #             mes = record.date.strftime('%m')
    #             start_of_month = record.date.replace(day=1)
    #             end_of_month = start_of_month + relativedelta(months=1)

    #             domain = [
    #                 ('date', '>=', start_of_month),
    #                 ('date', '<', end_of_month),
    #                 ('journal_id.type', '=', record.journal_id.type),
    #                 ('company_id', '=', record.company_id.id),
    #                 ('mes_secuencia', '!=', False),
    #                 ('state', '!=', 'draft'),  # ❗ Solo asientos publicados
    #             ]

    #             correlativo = self.env['account.move'].search_count(domain) + 1
    #             secuencial = f"{correlativo:04d}"
    #             record.mes_secuencia = f"{mes}-{secuencial}"

    #     return super(Configuracion, self).action_post()
    

      # mes_secuencia = fields.Char(
    #     string='Mes Secuencia',
    #     compute="_compute_mes_secuencia",
    #     store=True
    # )