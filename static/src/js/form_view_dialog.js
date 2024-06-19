/** @odoo-module **/
import { FormViewDialog } from "@web/views/view_dialogs/form_view_dialog";

export class ParkingFormViewDialog extends FormViewDialog {
  setup() {
    super.setup();
    this.viewProps = Object.assign(this.viewProps, {
      onCancelLeave: () => {
        this.props.close();
      },
      onLeaveUpdated: () => {
        this.props.onRecordSaved();
        console.log("hello");
        this.props.close();
      },
      onRecordDeleted: (record) => {
        this.props.onRecordDeleted(record);
      },
      saveRecord: async (record, { saveAndNew }) => {
        const saved = await record.save({ reload: false });
        if (saved) {
          await this.props.onRecordSaved(record);
          if (saveAndNew) {
            const context = Object.assign({}, this.props.context);
            Object.keys(context).forEach((k) => {
              if (k.startsWith("default_")) {
                delete context[k];
              }
            });
            await record.model.load({ resId: false, context });
          } else {
            this.props.close();
          }
        }
        return saved;
      },
    });
  }
}
ParkingFormViewDialog.props = {
  ...ParkingFormViewDialog.props,
  onRecordDeleted: Function,
  onLeaveCancelled: Function,
};
