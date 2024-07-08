import logging
from odoo import models, _, fields
import uuid
from odoo.exceptions import UserError
import json
import requests

_logger = logging.getLogger(__name__)


class ActionsServer(models.Model):
    _inherit = 'ir.actions.server'
    id_device = fields.Char(string="Id Device", store=True)

    def create(self, vals):
        """ Create a contextual action for each server action. """
        new_record = super(ActionsServer, self).create(vals)
        return new_record

    # def _run_action_webhook(self, eval_context=None):
    #     """Send a post request with a read of the selected field on active_id."""
    #     record = self.env[self.model_id.model].browse(
    #         self._context.get('active_id'))
    #     url = self.webhook_url
    #     if not record:
    #         return
    #     if not url:
    #         raise UserError(
    #             _("I'll be happy to send a webhook for you, but you really need to give me a URL to reach out to..."))
    #     vals = {
    #         '_model': self.model_id.model,
    #         '_id': record.id,
    #         '_action': f'{self.name}(#{self.id})',
    #     }
    #     if self.webhook_field_ids:
    #         # you might think we could use the default json serializer of the requests library
    #         # but it will fail on many fields, e.g. datetime, date or binary
    #         # so we use the json.dumps serializer instead with the str() function as default
    #         vals.update(record.read(
    #             self.webhook_field_ids.mapped('name'), load=None)[0])
    #     json_values = json.dumps(vals, sort_keys=True, default=str)
    #     _logger.info("Webhook call to %s", url)
    #     _logger.debug("POST JSON data for webhook call: %s", json_values)
    #     try:
    #         # 'send and forget' strategy, and avoid locking the user if the webhook
    #         # is slow or non-functional (we still allow for a 1s timeout so that
    #         # if we get a proper error response code like 400, 404 or 500 we can log)
    #         response = requests.post(url, data=json_values, headers={
    #                                  'Content-Type': 'application/json'}, timeout=1)
    #         response.raise_for_status()
    #     except requests.exceptions.ReadTimeout:
    #         _logger.warning("Webhook call timed out after 1s - it may or may not have failed. "
    #                         "If this happens often, it may be a sign that the system you're "
    #                         "trying to reach is slow or non-functional.")
    #     except requests.exceptions.RequestException as e:
    #         _logger.warning("Webhook call failed: %s", e)
    #     except Exception as e:  # noqa: BLE001
    #         raise UserError(
    #             _("Wow, your webhook call failed with a really unusual error: %s", e)) from e
