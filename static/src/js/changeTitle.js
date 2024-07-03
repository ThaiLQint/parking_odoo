/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { WebClient } from "@web/webclient/webclient";

patch(WebClient.prototype, {
  /**
   * @override
   */
  setup() {
    const backendIconEl = document.querySelector("link[rel~='icon']");
    // Save initial backend values.
    backendIconEl.href = "/parking_odoo/static/src/img/logo.ico";
    super.setup();
    this.updateTitle();
  },

  async updateTitle() {
    const title = await this.rpc(
      "/web/dataset/call_kw/ir.config_parameter/get_param",
      {
        model: "ir.config_parameter",
        method: "get_param",
        args: ["change_odoo_theme_header_color.website_title"],
        kwargs: {},
      }
    );

    const logo = await this.rpc(
      "/web/dataset/call_kw/ir.config_parameter/get_param",
      {
        model: "ir.config_parameter",
        method: "get_param",
        args: ["change_odoo_theme_header_color.website_logo_main"],
        kwargs: {},
      }
    );
    this.title.setParts({ zopenerp: title || "" });
    const backendIconEl = document.querySelector("link[rel~='icon']");
    // Save initial backend values.
    backendIconEl.href = `data:image/png;base64,${logo}`;
  },
});
