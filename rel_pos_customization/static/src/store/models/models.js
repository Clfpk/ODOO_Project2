/** @odoo-module */

import {
   Order,
   Orderline,
   Payment
} from "@point_of_sale/app/store/models";
import {
   patch
} from "@web/core/utils/patch";
import {
    formatFloat,
    roundDecimals as round_di,
    roundPrecision as round_pr,
    floatIsZero,
} from "@web/core/utils/numbers";
import { renderToElement } from "@web/core/utils/render";

// New orders are now associated with the current table, if any.
patch(Order.prototype, {
   export_for_printing() {
     var service_total = 0;
     var lines = this.orderlines;
     for(let line=0 ; line<lines.length; line++){if(lines[line].product.detailed_type == 'service'){service_total += lines[line].price}}
     debugger;
      return {
         ...super.export_for_printing(...arguments),
         service_charge: service_total,
         current_order: this.pos.get_order(),
      };
   },
   async printChanges(cancelled) {
      let orderChange = this.changesToOrder(cancelled);
      let isPrintSuccessful = true;
      const d = new Date();
      let hours = "" + d.getHours();
      hours = hours.length < 2 ? "0" + hours : hours;
      let minutes = "" + d.getMinutes();
      minutes = minutes.length < 2 ? "0" + minutes : minutes;
      var current_order_date = this.pos.get_order().date_order;
      for (const printer of this.pos.unwatched.printers) {
         const changes = this._getPrintingCategoriesChanges(
            printer.config.product_categories_ids,
            orderChange
         );
         if (changes["new"].length > 0 || changes["cancelled"].length > 0) {
            const printingChanges = {
               new: changes["new"],
               cancelled: changes["cancelled"],
               table_name: this.pos.config.module_pos_restaurant ?
                  this.getTable().name :
                  false,
               floor_name: this.pos.config.module_pos_restaurant ?
                  this.getTable().floor.name :
                  false,
               name: this.name || "unknown order",
               time: {
                  hours,
                  minutes,
               },
            };
            if (current_order_date.c) {
               let date_obj = current_order_date.c;
               printingChanges['date_order'] = date_obj.day + '-' + date_obj.month + '-' + date_obj.year + ':' + date_obj.hour + ':' + date_obj.minute + ':' + date_obj.second
            }
            const receipt = renderToElement("point_of_sale.OrderChangeReceipt", {
               changes: printingChanges,
            });
            const result = await printer.printReceipt(receipt);
            if (!result.successful) {
               isPrintSuccessful = false;
            }
         }
      }

      return isPrintSuccessful;
   },

   async add_product(product, options) {
        if (
            this.pos.doNotAllowRefundAndSales() &&
            this._isRefundOrder() &&
            (!options.quantity || options.quantity > 0)
        ) {
            this.pos.env.services.popup.add(ErrorPopup, {
                title: _t("Refund and Sales not allowed"),
                body: _t("It is not allowed to mix refunds and sales"),
            });
            return;
        }
        if (this._printed) {
            // when adding product with a barcode while being in receipt screen
            this.pos.removeOrder(this);
            return this.pos.add_new_order().add_product(product, options);
        }
        this.assert_editable();
        options = options || {};
        const quantity = options.quantity ? options.quantity : 1;
        const line = new Orderline(
            { env: this.env },
            { pos: this.pos, order: this, product: product, quantity: quantity }
        );
        this.fix_tax_included_price(line);

        this.set_orderline_options(line, options);
        line.set_full_product_name();
        var to_merge_orderline;
        for (var i = 0; i < this.orderlines.length; i++) {
            if (this.orderlines.at(i).can_be_merged_with(line) && options.merge !== false) {
                to_merge_orderline = this.orderlines.at(i);
            }
        }
        if (to_merge_orderline) {
            to_merge_orderline.merge(line);
            this.select_orderline(to_merge_orderline);
        } else {
            this.add_orderline(line);
            this.select_orderline(this.get_last_orderline());
        }

        if (options.draftPackLotLines) {
            this.selected_orderline.setPackLotLines({ ...options.draftPackLotLines, setQuantity: options.quantity === undefined });
        }

        if (options.comboLines?.length) {
            line.price = line.product.lst_price
            await this.addComboLines(line, options);
            // Make sure the combo parent is selected.
            this.select_orderline(line);
        }
         const defaultDiscount = 0.10; // 10%
        line.set_discount(defaultDiscount);

    },

   compute_child_lines(comboParentProduct, comboLines, pricelist) {
        const combolines = [];
        const parentLstPrice = comboParentProduct.get_price(pricelist, 1);
        const originalTotal = comboLines.reduce((acc, comboLine) => {
            const originalPrice = this.pos.db.combo_by_id[comboLine.combo_id[0]].base_price;
            return acc + originalPrice;
        }, 0);

        let remainingTotal = parentLstPrice;

        for (const comboLine of comboLines) {
            const combo = this.pos.db.combo_by_id[comboLine.combo_id[0]];
            let priceUnit = round_di(
                (combo.base_price * parentLstPrice) / originalTotal,
                this.pos.dp["Product Price"]
            );
            remainingTotal -= priceUnit;
            if (comboLine == comboLines[comboLines.length - 1]) {
                priceUnit += remainingTotal;
            }
            const attribute_value_ids = comboLine.configuration?.attribute_value_ids;
            const attributesPriceExtra = (attribute_value_ids ?? [])
                .map((id) => this.pos.db.attribute_value_by_id[id]?.price_extra || 0)
                .reduce((acc, price) => acc + price, 0);
            var totalPriceExtra = priceUnit + attributesPriceExtra + comboLine.combo_price;
            totalPriceExtra = comboLine.combo_price;
            combolines.push({ comboLine: comboLine, price: totalPriceExtra, attribute_value_ids });
        }
        return combolines;
    }

});

patch(Orderline.prototype, {
    getDisplayData() {
        return {
             ...super.getDisplayData(...arguments),
             type:this.product.detailed_type,
             InternalNote:this.getNote(),
             qty: parseInt(this.get_quantity_str()).toFixed(2),
        };
    },
});






