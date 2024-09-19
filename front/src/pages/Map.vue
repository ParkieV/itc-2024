<template>
  <q-page class="row items-center justify-evenly">
    <div id="map" class="map"></div>
    <Popup />
    <CreateRoadDialog :opened="!!roadFeature" @save="createRoad" />
    <CreateEventDialog
      :opened="placedEventFeatures.length === 2"
      @save="createRoad"
    />
    <q-fab
      v-if="!isDrawing && !isStartingEvent"
      class="absolute fab"
      color="purple"
      icon="keyboard_arrow_up"
      direction="up"
    >
      <q-fab-action
        external-label
        label-position="left"
        label="Создание объекта дороги"
        color="primary"
        icon="draw"
        @click="toggleDrawingMode"
      />
      <q-fab-action
        external-label
        label-position="left"
        label="Чат-бот"
        color="secondary"
        icon="forum"
      />
    </q-fab>
    <template v-else>
      <q-btn
        class="absolute-bottom-right q-ma-md"
        round
        color="negative"
        icon="cancel"
        style="margin-bottom: 80px"
        @click="
          () => (isStartingEvent ? handlerDiscardEvent() : cancelDrawing())
        "
        ><q-tooltip
          :offset="[10, 10]"
          class="overflow-hidden"
          self="center left"
          anchor="center right"
        >
          <p style="margin: 0; font-size: 16px; text-align: center">
            Отменить создание
          </p>
        </q-tooltip>
      </q-btn>
      <q-btn
        v-if="!isStartingEvent"
        class="absolute-bottom-right q-ma-md"
        round
        color="primary"
        icon="save"
        @click="
          () => {
            roadFeature = toggleDrawingMode();
          }
        "
      >
        <q-tooltip
          :offset="[10, 10]"
          class="overflow-hidden"
          self="center left"
          anchor="center right"
        >
          <p style="margin: 0; font-size: 16px; text-align: center">
            Сохранить объект дороги
          </p>
        </q-tooltip>
      </q-btn>
    </template>
  </q-page>
</template>
<script setup>
import { onBeforeUnmount, onMounted, ref, computed, watch } from 'vue';
import 'ol/ol.css';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import useMap from 'src/hooks/useMap';
import usePoint from 'src/hooks/usePoint';
import useDrawing from 'src/hooks/useDrawing';
import GeoJSON from 'ol/format/GeoJSON';
import { Style, Stroke } from 'ol/style';
import { useMapStore } from 'src/stores/map';
import Popup from 'src/components/Popup.vue';
import getRoads from 'src/api/getRoads';
import Feature from 'ol/Feature';
import { MultiLineString } from 'ol/geom';
import { lineStyle, boundaryStyle } from 'src/assets/style';
import Point from 'ol/geom/Point';
import CreateRoadDialog from 'src/components/CreateRoadDialog.vue';
import CreateEventDialog from 'src/components/CreateEventDialog.vue';
import getEventsInfo from 'src/api/getEventsInfo';

const mapStore = useMapStore();
const { initMap } = useMap();
const { initDrawing } = useDrawing();
const { createPoint } = usePoint();

const map = ref();
const roadFeature = ref();

const drawSource = new VectorSource({ wrapX: false });
const drawLayer = new VectorLayer({
  source: drawSource,
});

const vectorSource = new VectorSource({ wrapX: false });
const vectorLayer = new VectorLayer({
  source: vectorSource,
});

const eventSource = new VectorSource({ wrapX: false });
const eventLayer = new VectorLayer({
  source: eventSource,
});

const movingEventFeature = ref(new Feature(new Point([0, 0]))); // точка, летающая вдоль дороги, которую выбрали для основы ивента
const placedEventFeatures = ref([]); // хранит все точки, поставленные в режиме создания ивента как баундерис

const { toggleDrawingMode, handleKeyDown, isDrawing, cancelDrawing } =
  initDrawing(map, drawSource, vectorSource);

const getRoadsData = () => {
  getRoads().then((res) => {
    res.map(({ geodata, id, ...obj }) => {
      const commonData = obj['common-data'];
      const allCoordinates = geodata.map(
        ({ geometry }) => geometry.coordinates
      )[0];
      const multiLineString = new MultiLineString(allCoordinates);

      const feature = new Feature({
        geometry: multiLineString,
        ...commonData,
      });

      feature.setId(id);
      feature.setStyle(lineStyle);
      feature.set('common-data', commonData);
      feature.set('type', 'road');
      vectorSource.addFeature(feature);
    });
  });
};

const createRoad = (data) => {
  console.log(data);
  console.log(roadFeature.value);
};

onMounted(() => {
  getRoadsData();
  map.value = initMap('map', [vectorLayer, drawLayer, eventLayer]);
  map.value.getLayers().push(
    new VectorLayer({
      source: new VectorSource({
        features: [
          createPoint(34.56, 53.2, 'Объект 1'),
          createPoint(34.59, 53.19, 'Замена дорожного полотна'),
          createPoint(34.56, 53.1, 'Расширение полосы'),
          createPoint(34.68, 53.5, 'Ремонт повреждений'),
        ],
      }),
    })
  );

  map.value.on('click', (event) => {
    if (map.value) {
      if (isStartingEvent.value) {
        const finalPosition = movingEventFeature.value
          .getGeometry()
          .getCoordinates();
        console.log('Feature placed at:', finalPosition);
        const finalFeature = movingEventFeature.value.clone();
        finalFeature.set('type', 'event-boundary'); // !!!
        finalFeature.setStyle(boundaryStyle);
        eventSource.addFeature(finalFeature);
        placedEventFeatures.value.push(finalFeature);
        console.log(placedEventFeatures.value);
      } else {
        const feature = map.value.forEachFeatureAtPixel(
          event.pixel,
          (feature) => {
            return feature;
          }
        );

        if (feature) {
          mapStore.setSelectedObject(feature);
        }
      }
    }
  });

  map.value.on('pointermove', (e) => {
    if (map.value) {
      if (isStartingEvent.value) {
        const multiLineString = mapStore.selectedObject;
        const coordinate = e.coordinate;
        const closestPoint = multiLineString
          .getGeometry()
          .getClosestPoint(coordinate);
        movingEventFeature.value.getGeometry().setCoordinates(closestPoint);
      } else {
        const feature = map.value?.forEachFeatureAtPixel(
          e.pixel,
          function (feature, layer) {
            // TODO: исключить из обработки новую feature
            return feature;
          }
        );
        if (feature) {
          mapStore.setHoveredObject(feature);
        } else {
          mapStore.clearHoveredObject();
        }
      }
    }
  });

  window.addEventListener('keydown', handleKeyDown);
});

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeyDown);
});

const isStartingEvent = computed(() => mapStore.startingEvent);

watch(isStartingEvent, () => {
  // вошли в режим создания ивента
  if (isStartingEvent.value) {
    eventSource.addFeature(movingEventFeature.value);
  }
});

const handlerCreateEvent = () => {
  movingEventFeature.value = new Feature(new Point([0, 0]));
  // TODO: сохранение на бэк
  // placedEventFeatures.value = [];
  // mapStore.endEvent();
};

const handlerDiscardEvent = () => {
  movingEventFeature.value = new Feature(new Point([0, 0]));
  placedEventFeatures.value.forEach((feature) => {
    console.log(feature);
    eventSource.removeFeature(feature);
  });
  placedEventFeatures.value = [];
  mapStore.endEvent();
};

watch(
  placedEventFeatures,
  () => {
    // если поставил две баундерис, то создаем автоматически
    if (placedEventFeatures.value.length == 2) {
      handlerCreateEvent();
    }
  },
  { deep: true }
);

watch(isDrawing, () => {
  mapStore.toggleDrawing(isDrawing.value);
});

onMounted(async () => {
  const data = await getEventsInfo();
  console.log(data);
});
</script>

<style lang="scss" scoped>
.map {
  position: absolute;
  top: -50px;
  width: 100%;
  height: 100vh;
}

:deep {
  .ol-attribution {
    display: none;
  }
}

.fab {
  bottom: 20px;
  right: 20px;
}
</style>
