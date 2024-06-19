/** @odoo-module **/
import { registry } from "@web/core/registry";
import { formView } from "@web/views/form/form_view";
import { FormController } from "@web/views/form/form_controller";
import { FormRenderer } from "@web/views/form/form_renderer";
import { useService } from "@web/core/utils/hooks";
import {
  onMounted,
  onWillUpdateProps,
  useState,
  EventBus,
  useSubEnv,
} from "@odoo/owl";
import { FormViewDialog } from "@web/views/view_dialogs/form_view_dialog";

class NspBranchFormController extends FormController {
  setup() {
    super.setup();
    useSubEnv({
      timeOffBus: new EventBus(),
    });
    console.log(this.model);

    this.dialogService = useService("dialog");
  }
  save(params){
    console.log("save")
    super.save(params)
  }
  // addParkingId() {
  //   self = this;
  //   self.dialogService.add(FormViewDialog, {
  //     title: "Tạo mới bãi xe",
  //     resModel: "setting.nsp.parking",
  //     context: {
  //       form_view_ref: "parking_odoo.setting_nsp_parking_view_form",
  //       default_branch_id: self.model.root.data.id,
  //     },
  //     onRecordSaved: (record) => {
  //       console.log(record);
  //       self.model.load();
  //       self.env.timeOffBus.trigger("update_dashboard");
  //       //   saveButtonClicked(params = {}) {
  //       //     return executeButtonCallback(this.ui.activeElement, () => this.save(params));
  //       // }
  //     },
  //   });
  // }
  // save(params) {
  //   console.log(params);
  //   super.save(params);
  // }
}
NspBranchFormController.template = "parking_odoo.setting_nsp_form_view";

export class SettingNspFormRenderer extends FormRenderer {
  setup() {
    super.setup();
    onMounted(() => {});
    onWillUpdateProps(async (nextProps) => {});
  }
}
export const nspBranchFormView = {
  ...formView,
  Controller: NspBranchFormController,
  Renderer: SettingNspFormRenderer,
};

registry.category("views").add("nsp_branch_form_view", nspBranchFormView);
