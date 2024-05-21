from odoo import models, fields, api

class AddActionModel(models.Model):
    _name = 'add.action.model'

    color_ids = fields.One2many('product.color.values',
                    inverse_name='color_id',  
                    index=True,
                    string="Color list")
    
    name        = fields.Char(string='Tên màu', index=True)
    html_color  = fields.Char('Mã màu',  required=True)
    
    @api.model
    def save_method(self):
        # Logic to save the form can be defined here
        return True
    
    def open_popup_action(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Popup Form',
            'view_mode': 'form',
            'res_model': 'product.color.main',
            'target': 'new',
            'context': self.env.context,
        }
