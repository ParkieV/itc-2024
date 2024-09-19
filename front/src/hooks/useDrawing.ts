import { Map } from 'ol';
import VectorSource from 'ol/source/Vector';
import { Ref, ref } from 'vue';
import { LineString, MultiLineString } from 'ol/geom';
import Draw from 'ol/interaction/Draw';
import Feature from 'ol/Feature';
import { lineStyle } from 'src/assets/style';

const useDrawing = () => {
  const initDrawing = (
    map: Ref<Map>,
    drawSource: VectorSource,
    vectorSource: VectorSource
  ) => {
    const isDrawing = ref(false);
    const drawInteraction = ref();

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && drawInteraction.value) {
        drawInteraction.value.finishDrawing();
      }
    };

    const cancelDrawing = () => {
      isDrawing.value = false;
      drawInteraction.value.finishDrawing();
      drawInteraction.value = null;
      drawSource.clear();
    };

    const toggleDrawingMode = () => {
      if (isDrawing.value) {
        if (drawInteraction.value) {
          drawInteraction.value.finishDrawing();
          map.value.removeInteraction(drawInteraction.value);
          drawInteraction.value = null;
        }

        const features = drawSource.getFeatures();
        if (features.length > 0) {
          const coordinates = features.map((feature) => {
            const geom = feature.getGeometry() as LineString;
            return geom!.getCoordinates();
          });
          const multiLineString = new MultiLineString(coordinates);
          const multiLineFeature = new Feature(multiLineString);
          multiLineFeature.setStyle(lineStyle);
          // здесь создается дорога
          vectorSource.addFeature(multiLineFeature);
          drawSource.clear();
          return multiLineFeature;
        }
      } else {
        drawInteraction.value = new Draw({
          source: drawSource,
          type: 'LineString',
          stopClick: true,
          finishCondition: (event) => false,
        });
        if (map.value) {
          map.value.addInteraction(drawInteraction.value);
        }
      }
      isDrawing.value = !isDrawing.value;
    };
    return { handleKeyDown, toggleDrawingMode, isDrawing, cancelDrawing };
  };
  return { initDrawing };
};

export default useDrawing;
