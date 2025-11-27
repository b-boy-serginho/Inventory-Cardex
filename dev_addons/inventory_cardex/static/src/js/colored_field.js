/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ListRenderer } from "@web/views/list/list_renderer";

// Función helper para aplicar colores a las celdas
function applyColorsToQtyCells(rootElement) {
    if (!rootElement) return;

    // Buscar todas las celdas de incoming_qty
    const incomingCells = rootElement.querySelectorAll('[name="incoming_qty"]');
    incomingCells.forEach(cell => {
        // Obtener el valor, manejando tanto el formato con coma como con punto
        const text = cell.textContent.trim().replace(',', '.');
        const value = parseFloat(text) || 0;

        if (value !== 0) {
            cell.style.color = '#00b050';
            cell.style.fontWeight = 'bold';
            cell.style.textAlign = 'center';
        } else {
            cell.style.color = '';
            cell.style.fontWeight = '';
            cell.style.textAlign = 'center';
        }
    });

    // Buscar todas las celdas de outgoing_qty
    const outgoingCells = rootElement.querySelectorAll('[name="outgoing_qty"]');
    outgoingCells.forEach(cell => {
        // Obtener el valor, manejando tanto el formato con coma como con punto
        const text = cell.textContent.trim().replace(',', '.');
        const value = parseFloat(text) || 0;

        if (value !== 0) {
            cell.style.color = '#ff0000';
            cell.style.fontWeight = 'bold';
            cell.style.textAlign = 'center';
        } else {
            cell.style.color = '';
            cell.style.fontWeight = '';
            cell.style.textAlign = 'center';
        }
    });

    // ========== CAMPOS DE COMPRA - COLOR VERDE (#00b050) ==========
    const purchaseFields = [
        'purchase_product_qty', 'purchase_price_unit', 'purchase_price_subtotal',
        'purchase_price_tax', 'purchase_price_total', 'purchase_order_id',
        'purchase_product_name', 'purchase_state', 'has_purchase'
    ];
    
    purchaseFields.forEach(fieldName => {
        const cells = rootElement.querySelectorAll(`[name="${fieldName}"]`);
        cells.forEach(cell => {
            // Verificar si purchase_product_qty > 0 en la misma fila
            const row = cell.closest('tr');
            if (row) {
                const qtyCell = row.querySelector('[name="purchase_product_qty"]');
                if (qtyCell) {
                    const qtyText = qtyCell.textContent.trim().replace(/[^\d.,-]/g, '').replace(',', '.');
                    const qtyValue = parseFloat(qtyText) || 0;
                    
                    if (qtyValue > 0) {
                        cell.style.color = '#00b050';
                        cell.style.fontWeight = 'bold';
                        // Aplicar color a todos los elementos dentro de la celda
                        const innerElements = cell.querySelectorAll('*');
                        innerElements.forEach(el => {
                            el.style.color = '#00b050';
                            el.style.fontWeight = 'bold';
                        });
                    } else {
                        cell.style.color = '';
                        cell.style.fontWeight = '';
                        const innerElements = cell.querySelectorAll('*');
                        innerElements.forEach(el => {
                            el.style.color = '';
                            el.style.fontWeight = '';
                        });
                    }
                }
            }
        });
    });

    // ========== CAMPOS DE VENTA - COLOR ROJO (#ff0000) ==========
    const saleFields = [
        'sale_product_uom_qty', 'sale_price_unit', 'sale_price_subtotal',
        'sale_price_tax', 'sale_price_total', 'sale_order_id',
        'sale_product_name', 'sale_state', 'has_sale'
    ];
    
    saleFields.forEach(fieldName => {
        const cells = rootElement.querySelectorAll(`[name="${fieldName}"]`);
        cells.forEach(cell => {
            // Verificar si sale_product_uom_qty > 0 en la misma fila
            const row = cell.closest('tr');
            if (row) {
                const qtyCell = row.querySelector('[name="sale_product_uom_qty"]');
                if (qtyCell) {
                    const qtyText = qtyCell.textContent.trim().replace(/[^\d.,-]/g, '').replace(',', '.');
                    const qtyValue = parseFloat(qtyText) || 0;
                    
                    if (qtyValue > 0) {
                        cell.style.color = '#ff0000';
                        cell.style.fontWeight = 'bold';
                        // Aplicar color a todos los elementos dentro de la celda
                        const innerElements = cell.querySelectorAll('*');
                        innerElements.forEach(el => {
                            el.style.color = '#ff0000';
                            el.style.fontWeight = 'bold';
                        });
                    } else {
                        cell.style.color = '';
                        cell.style.fontWeight = '';
                        const innerElements = cell.querySelectorAll('*');
                        innerElements.forEach(el => {
                            el.style.color = '';
                            el.style.fontWeight = '';
                        });
                    }
                }
            }
        });
    });
}

// Patch del ListRenderer
patch(ListRenderer.prototype, {
    setup() {
        super.setup();

        // Usar setTimeout para aplicar después del renderizado
        setTimeout(() => {
            applyColorsToQtyCells(this.rootRef?.el);
        }, 100);

        // Observar cambios en el DOM
        if (typeof MutationObserver !== 'undefined') {
            const observer = new MutationObserver(() => {
                applyColorsToQtyCells(this.rootRef?.el);
            });

            setTimeout(() => {
                if (this.rootRef?.el) {
                    observer.observe(this.rootRef.el, {
                        childList: true,
                        subtree: true
                    });
                }
            }, 200);
        }
    }
});

// También aplicar cuando se carga la página
if (typeof window !== 'undefined') {
    window.addEventListener('load', () => {
        setInterval(() => {
            applyColorsToQtyCells(document.body);
        }, 1000);
    });
}
