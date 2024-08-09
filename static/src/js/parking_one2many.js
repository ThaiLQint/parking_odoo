/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ListRenderer } from "@web/views/list/list_renderer";
import {
  X2ManyField,
  x2ManyField,
} from "@web/views/fields/x2many/x2many_field";
import { _t } from "@web/core/l10n/translation";
import { ParkingFormViewDialog } from "./form_view_dialog";
import { EventBus, useSubEnv, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class ParkingSettingList extends ListRenderer {
  /**
   * The purpose of this extension is to allow sections and notes in the one2many list
   * primarily used on Sales Orders and Invoices
   *
   * @override
   */
  async setup() {
    super.setup();
    this.creates = this.props.archInfo.creates.length
      ? this.props.archInfo.creates
      : [{ type: "create", string: _t("Thêm mới") }];
    useSubEnv({
      timeOffBus: new EventBus(),
    });
    this.rpc = useService("rpc");
    this.dialogService = useService("dialog");
    //onWillStart(this.onLoadConfig);
  }

  async onLoadConfig() {
    this.props.list.groups = await this.rpc("/api/load/nsp/config", {
      code: "parking",
    });
  }

  add(params) {
    const self = this;
    if (self.canCreate) {
      var data = self.props.list._parent.data;
      self.props.list._parent.save(data).then((result) => {
        if (result === true) {
          self.props.onAdd(params);
        }
      });
    }
  }
}
ParkingSettingList.template = "parking.ListRenderer";
ParkingSettingList.rowsTemplate = "parking.ListRenderer.Rows";
ParkingSettingList.groupRowTemplate = "parking.ListRenderer.GroupRow";

export class ParkingSettingOne2Many extends X2ManyField {}
ParkingSettingOne2Many.components = {
  ...X2ManyField.components,
  ListRenderer: ParkingSettingList,
};

export const parkingSettingOne2Many = {
  ...x2ManyField,
  component: ParkingSettingOne2Many,
  additionalClasses: [
    ...(x2ManyField.additionalClasses || []),
    "o_field_one2many",
  ],
};
registry
  .category("fields")
  .add("parking_setting_one2many", parkingSettingOne2Many);
