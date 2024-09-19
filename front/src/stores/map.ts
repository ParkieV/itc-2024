import { defineStore } from 'pinia';

export const useMapStore = defineStore('map', {
  state: () => ({
    hoveredObject: null,
    selectedObject: null,
    startingEvent: false,
    isDrawing: false,
  }),
  actions: {
    setHoveredObject(hoveredObject: any) {
      if (!this.isDrawing) {
        this.hoveredObject = hoveredObject;
      }
    },

    clearHoveredObject() {
      this.hoveredObject = null;
    },

    setSelectedObject(selectedObject: any) {
      if (!this.isDrawing) {
        this.selectedObject = selectedObject;
        this.clearHoveredObject();
      }
    },

    clearSelectedObject() {
      this.selectedObject = null;
    },

    getSelectedObject() {
      return this.selectedObject;
    },

    startEvent() {
      this.startingEvent = true;
    },

    endEvent() {
      this.startingEvent = false;
    },

    toggleDrawing(value: boolean) {
      this.isDrawing = value;
    },
  },
});
