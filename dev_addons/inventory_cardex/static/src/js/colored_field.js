/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class ColoredQtyField extends Component {
    static template = "inventory_cardex.ColoredQtyField";
    static props = {
        ...standardFieldProps,
    };

    get formattedValue() {
        const value = this.props.record.data[this.props.name];
        return Math.round(value || 0);
    }

    get colorStyle() {
        const value = this.props.record.data[this.props.name];
        const fieldName = this.props.name;

        if (value > 0) {
            // Verde para incoming_qty, rojo para outgoing_qty
            const color = fieldName === 'incoming_qty' ? '#00b050' : '#ff0000';
            return `color: ${color}; font-weight: bold; text-align: center;`;
        }
        return "color: inherit; text-align: center;";
    }
}

registry.category("fields").add("colored_qty", ColoredQtyField);
