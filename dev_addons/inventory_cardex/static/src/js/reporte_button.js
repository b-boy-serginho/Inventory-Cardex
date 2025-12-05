/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { patch } from "@web/core/utils/patch";

patch(ListController.prototype, {
    setup() {
        super.setup(...arguments);
        if (this.props.resModel === 'stock.move.line') {
            console.log('🔵 Reporte Button: Setup ejecutado para stock.move.line');
            this._addReportButton = this._addReportButton.bind(this);
            this._buttonAdded = false;
            
            // Observador de mutaciones para detectar cuando se agregan botones
            if (typeof MutationObserver !== 'undefined') {
                setTimeout(() => {
                    this._setupMutationObserver();
                }, 1000);
            }
        }
    },

    _setupMutationObserver() {
        const observer = new MutationObserver(() => {
            if (!this._buttonAdded) {
                this._addReportButton();
            }
        });

        // Observar cambios en el body para detectar cuando se carga la vista
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });

        // Detener el observador después de 10 segundos
        setTimeout(() => {
            observer.disconnect();
        }, 10000);
    },

    /**
     * Agregar el botón después de que la vista se monte completamente
     */
    async onWillRender() {
        const result = await super.onWillRender?.call(this, ...arguments);
        if (this.props.resModel === 'stock.move.line') {
            // Usar setTimeout múltiples veces para asegurar que se agregue
            setTimeout(() => {
                this._addReportButton();
            }, 300);
            setTimeout(() => {
                this._addReportButton();
            }, 800);
            setTimeout(() => {
                this._addReportButton();
            }, 1500);
        }
        return result;
    },

    /**
     * También intentar agregar el botón cuando se monta el componente
     */
    onMounted() {
        super.onMounted?.call(this, ...arguments);
        if (this.props.resModel === 'stock.move.line') {
            setTimeout(() => {
                this._addReportButton();
            }, 500);
        }
    },

    _addReportButton() {
        if (this.props.resModel !== 'stock.move.line') {
            return;
        }

        // Buscar el contenedor de botones en diferentes ubicaciones
        let buttonsContainer = null;
        
        // Intentar diferentes selectores
        const selectors = [
            '.o_list_buttons',
            '.o_control_panel .o_list_buttons',
            '.o_action_manager .o_list_buttons',
            '[class*="o_list_buttons"]'
        ];

        for (const selector of selectors) {
            buttonsContainer = document.querySelector(selector);
            if (buttonsContainer) break;
        }

        if (!buttonsContainer) {
            console.warn('No se encontró el contenedor de botones');
            return;
        }

        // Verificar si el botón ya existe
        if (buttonsContainer.querySelector('.btn-reporte-custom')) {
            this._buttonAdded = true;
            return;
        }
        
        console.log('🔵 Reporte Button: Contenedor encontrado, agregando botón...');

        // Crear el botón Reporte
        const reportButton = document.createElement('button');
        reportButton.className = 'btn btn-primary btn-reporte-custom';
        reportButton.type = 'button';
        reportButton.setAttribute('aria-label', 'Reporte');
        reportButton.style.marginLeft = '8px';
        reportButton.innerHTML = '<i class="fa fa-file-text-o"></i> Reporte';
        
        const self = this;
        reportButton.addEventListener('click', async (e) => {
            e.preventDefault();
            e.stopPropagation();
            try {
                // Obtener los IDs de los registros seleccionados
                const recordIds = await self.getSelectedResIds();
                
                if (!recordIds || recordIds.length === 0) {
                    self.env.services.notification.add('Por favor, seleccione al menos un movimiento para generar el reporte.', {
                        type: 'warning',
                        title: 'Sin selección'
                    });
                    return;
                }
                
                const action = {
                    type: 'ir.actions.act_window',
                    res_model: 'reporte.wizard',
                    view_mode: 'form',
                    target: 'new',
                    context: {
                        active_ids: recordIds,
                    },
                };
                await self.actionService.doAction(action);
            } catch (error) {
                console.error('Error al abrir wizard:', error);
            }
        });

        // Buscar el botón Nuevo e insertar después de él
        const createButton = buttonsContainer.querySelector('.o_list_button_add, button[aria-label*="Crear"], button[aria-label*="New"], button[aria-label*="Add"]');
        if (createButton && createButton.parentNode) {
            createButton.parentNode.insertBefore(reportButton, createButton.nextSibling);
        } else {
            // Si no encontramos el botón Nuevo, agregar al final
            buttonsContainer.appendChild(reportButton);
        }
        
        this._buttonAdded = true;
        console.log('✅ Botón Reporte agregado exitosamente');
    },
});

