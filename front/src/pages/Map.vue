<template>
  <q-page class="row items-center justify-evenly">
    <div id="map" class="map"></div>
    <Popup />
    <CreateRoadDialog :opened="!!roadFeature" @save="createRoad" />
    <CreateEventDialog
      :opened="placedEventFeatures.length === 2"
      @save="handleCreateEvent"
    />
    <UpdateEventDialog
      :opened="!!eventData"
      :id="eventData?.getId()"
      @save="updateEvent"
    />
    <Chat :opened="showChat" @close="() => (showChat = false)" />
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
        @click="openChat"
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
import UpdateEventDialog from 'src/components/UpdateEventDialog.vue';
import Chat from 'src/components/Chat.vue';

const mapStore = useMapStore();
const { initMap } = useMap();
const { initDrawing } = useDrawing();
const { createPoint } = usePoint();

const map = ref();
const roadFeature = ref();
const eventData = ref(null);
const showChat = ref(false);

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
    getEventsHandler();
  });
};

const createRoad = (data) => {
  console.log(data);
  console.log(roadFeature.value);
};

const updateEvent = (data) => {
  eventData.value = null;
  // TODO: бэкенд)
};

onMounted(() => {
  getRoadsData();
  map.value = initMap('map', [vectorLayer, drawLayer, eventLayer]);
  const event = createPoint(34.59, 53.19, 'Замена дорожного полотна');
  event.setId('e51e25f7-0e6c-4792-bfbd-9c4d693eb4af');
  eventSource.addFeature(event);
  // map.value.getLayers().push(
  //   new VectorLayer({
  //     source: new VectorSource({
  //       features: [
  //         createPoint(34.56, 53.2, 'Объект 1'),
  //         createPoint(34.59, 53.19, 'Замена дорожного полотна'),
  //         createPoint(34.56, 53.1, 'Расширение полосы'),
  //         createPoint(34.68, 53.5, 'Ремонт повреждений'),
  //       ],
  //     }),
  //   })
  // );

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
          if (feature.get('type') === 'event') {
            // event.value = feature.get('id');
            // TODO: достать айди
            eventData.value = feature;
          } else {
            mapStore.setSelectedObject(feature);
          }
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

const openChat = () => {
  showChat.value = !showChat.value;
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

const getEventsHandler = () => {
  // getEvents().then((res) => {
  // res.forEach((object) => {
  //   function closestPointOnLine(multiLineString, point) {
  //     console.log(multiLineString);
  //     return multiLineString.getClosestPoint(point);
  //   }
  //   if (vectorSource.getFeatures().length) {
  //     console.log(object['road_chunk_id'], vectorSource.getFeatures());
  //     const multiLineString = vectorSource.getFeatureById(
  //       object['road_chunk_id']
  //     );
  //     const features = object.properties.boundaries;
  //     proj4.defs(
  //       'EPSG:32633',
  //       '+proj=utm +zone=33 +datum=WGS84 +units=m +no_defs'
  //     );
  //     register(proj4);
  //     // Example UTM coordinates (easting, northing, elevation)
  //     // Transform UTM to WGS84 (EPSG:4326)
  //     const inflatedCoordinates1 = proj4(
  //       'EPSG:32633',
  //       'EPSG:4326',
  //       features[0].flatCoordinates
  //     );
  //     const inflatedCoordinates2 = proj4(
  //       'EPSG:32633',
  //       'EPSG:4326',
  //       features[1].flatCoordinates
  //     );
  //     const point1 = new Feature({
  //       geometry: new Point(fromLonLat(inflatedCoordinates1)),
  //     });
  //     const point2 = new Feature({
  //       geometry: new Point(fromLonLat(inflatedCoordinates2)),
  //     });
  //     const newCoords = [
  //       (inflatedCoordinates1[0] + inflatedCoordinates2[0]) / 2,
  //       (inflatedCoordinates1[1] + inflatedCoordinates2[1]) / 2,
  //     ];
  //     console.log(fromLonLat(inflatedCoordinates1));
  //     // Create a new point feature at the midpoint
  //     const midpointFeature = new Feature(new Point(newCoords));
  //     midpointFeature.set('type', 'event');
  //     midpointFeature.setId(res.id);
  //     eventSource.addFeature(midpointFeature);
  //     point1.setStyle(boundaryStyle);
  //     point1.set('type', 'event-boundary');
  //     eventSource.addFeature(point1);
  //     point2.setStyle(boundaryStyle);
  //     point2.set('type', 'event-boundary');
  //     eventSource.addFeature(point2);
  //     console.log(eventSource.getFeatures());
  //   }
  // });
  // });
};

const handleCreateEvent = (object) => {
  createEvent(
    mapStore.selectedObject.getId(),
    object,
    placedEventFeatures.value.map((feature) => feature.getGeometry())
  );
  placedEventFeatures.value = [];
  mapStore.endEvent();
};
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
