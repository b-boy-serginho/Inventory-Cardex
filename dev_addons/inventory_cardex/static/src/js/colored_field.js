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
