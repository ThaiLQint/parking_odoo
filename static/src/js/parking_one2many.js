/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ListRenderer } from "@web/views/list/list_renderer";
import {
  X2ManyField,
  x2ManyField,
} from "@web/views/fields/x2many/x2many_field";
import { _t } from "@web/core/l10n/translation";
import { ParkingFormViewDialog } from "./form_view_dialog";
import { EventBus, useSubEnv } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class ParkingSettingList extends ListRenderer {
  /**
   * The purpose of this extension is to allow sections and notes in the one2many list
   * primarily used on Sales Orders and Invoices
   *
   * @override
   */
  setup() {
    super.setup();
    this.creates = this.props.archInfo.creates.length
      ? this.props.archInfo.creates
      : [{ type: "create", string: _t("Thêm mới") }];
    useSubEnv({
      timeOffBus: new EventBus(),
    });
    this.dialogService = useService("dialog");
  }

  add(params) {
    const self = this;
    if (self.canCreate) {
      //this.props.onAdd(params);
      console.log(self);
      var data = self.props.list._parent.data;
      var resModel = self.props.list._config.resModel;
      var context = {};
      self.props.list._parent.save(data).then((result) => {
        console.log(result);
        var data = self.props.list._parent.data;
        var title = "";
        if (result === true) {
          context = {
            form_view_ref:
              "parking_odoo." + resModel.replace(".", "_") + "_view_form",
          };
          if (resModel === "setting.nsp.office") {
            context = { ...context, default_parking_id: data.id };
            title = "Tạo văn phòng bảo vệ";
          } else if (
            resModel  === "setting.nsp.lane.in" ||
            resModel === "setting.nsp.lane.out"
          ) {
            context = { ...context, default_office_id: data.id };
            title =
              "Tạo cổng " + (resModel === "setting.nsp.lane.in" ? "vào" : "ra");
          } else if (resModel === "setting.nsp.parking") {
            context = { ...context, default_branch_id: data.id };
            title = "Tạo bãi xe";
          }
          const onDialogClosed = () => {
            self.env.model.load();
            self.env.timeOffBus.trigger("update_dashboard");
          };
          self.env.model.dialog.add(ParkingFormViewDialog, {
            title: _t(title),
            resModel: resModel,
            context: context,
            onRecordSaved: () => onDialogClosed(),
            onRecordDeleted: (record) => self.deleteRecord(record),
          });
        }
      });
    }
  }
}
ParkingSettingList.template = "parking.SettingListRenderer";

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
