/** @odoo-module **/
import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";
import { ListRenderer } from "@web/views/list/list_renderer";
import { useService } from "@web/core/utils/hooks";
import { onMounted, onWillUpdateProps, onWillStart } from "@odoo/owl";

class NspBranchListController extends ListController {
  setup() {
    super.setup();
    this.rpc = useService("rpc");
    this.onLoadConfig();
  }
  async onLoadConfig() {
    this.records = await this.rpc("/api/load/nsp/config/view", {
      code: "parking",
    });
    if (this.records.message === "Success") {
      this.records = this.records.records;
    }
  }
}
NspBranchListController.template = "parking_odoo.setting_nsp_list_view";

export class SettingNspListRenderer extends ListRenderer {
  setup() {
    super.setup();
    onMounted(() => {
      var acc = document.getElementsByClassName("accordion");
      var i;

      for (i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function () {
          this.classList.toggle("accordion-active");
          var panel = this.nextElementSibling;
          if (panel.style.maxHeight) {
            panel.style.maxHeight = null;
          } else {
            panel.style.maxHeight = panel.scrollHeight + "px";
          }
        });
      }
    });
    onWillUpdateProps(async (nextProps) => {});
  }
  toggleGroup(group) {
    console.log(group);
    group.toggle();
  }

  onCellKeydown(ev, group = null, record = null) {
    console.log(group);
    console.log(record);
    if (this.props.list.model.useSampleModel) {
      return;
    }

    const hotkey = getActiveHotkey(ev);

    if (ev.target.tagName === "TEXTAREA" && hotkey === "enter") {
      return;
    }

    const closestCell = ev.target.closest("td, th");

    if (this.toggleFocusInsideCell(hotkey, closestCell)) {
      return;
    }

    const handled = this.props.list.editedRecord
      ? this.onCellKeydownEditMode(hotkey, closestCell, group, record)
      : this.onCellKeydownReadOnlyMode(hotkey, closestCell, group, record); // record is supposed to be not null here

    if (handled) {
      this.lastCreatingAction = false;
      this.tableRef.el
        .querySelector("tbody")
        .classList.add("o_keyboard_navigation");
      ev.preventDefault();
      ev.stopPropagation();
    }
  }
}
SettingNspListRenderer.template = "parking.ListRenderer";
SettingNspListRenderer.rowsTemplate = "parking.ListRenderer.Rows";
SettingNspListRenderer.recordRowTemplate = "parking.ListRenderer.RecordRow";
SettingNspListRenderer.groupRowTemplate = "parking.ListRenderer.GroupRow";
export const nspBranchListView = {
  ...listView,
  Controller: NspBranchListController,
  Renderer: SettingNspListRenderer,
};

registry.category("views").add("nsp_branch_list_view", nspBranchListView);
