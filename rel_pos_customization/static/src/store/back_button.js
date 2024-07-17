/** @odoo-module */

import { BackButton } from "@point_of_sale/app/navbar/back_button/back_button";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { TipScreen } from "@pos_restaurant/app/tip_screen/tip_screen";
import { patch } from "@web/core/utils/patch";

patch(BackButton.prototype, {
//   async onClick() {
//      if (this.pos.mainScreen.component && this.pos.config.module_pos_restaurant) {
//         if (
//            (this.pos.mainScreen.component === ProductScreen &&
//               this.pos.mobile_pane == "right") ||
//            this.pos.mainScreen.component === TipScreen
//         ) {
//            this.pos.showScreen("FloorScreen", {
//               floor: this.floor
//            });
//         } else {
//            super.onClick(...arguments);
//         }
//         if (this.pos.get_order().get_orderlines().length == 0) {
//            const orderOnTable = this.pos.orders.filter(
//               (o) => o.tableId === this.pos.table.id && o.finalized === false
//            );
//            for (const order of orderOnTable) {
//               this.pos.removeOrder(order);
//            }
//         }
//         return;
//      }
//      super.onClick(...arguments);
//   },
})