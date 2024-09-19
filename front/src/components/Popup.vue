<template>
  <transition
    appear
    enter-active-class="animated fadeIn"
    leave-active-class="animated fadeOut"
  >
    <q-card v-show="isPopupShowed" class="popup" flat bordered>
      <q-card-section horizontal>
        <q-card-section class="q-pt-xs">
          <div class="text-overline">Паспорт объекта</div>
          <div class="text-h6 q-mt-sm q-mb-xs">
            <!-- @ts-ignore -->
            {{ object.name }}
          </div>
          <div class="text-caption text-darkgrey">
            {{ object.owner }}
          </div>
          <q-btn
            unelevated
            class="q-mt-md"
            color="primary"
            label="Подробнее"
            align="center"
            @click="openObject"
          />
        </q-card-section>
      </q-card-section>
    </q-card>
  </transition>
</template>
<script setup lang="ts">
// @ts-nocheck
import Feature from 'ol/Feature';
import useMap from 'src/hooks/useMap';
import { useMapStore } from 'src/stores/map';
import { computed, ref, watch } from 'vue';

defineOptions({
  name: 'Popup',
});

const mapStore = useMapStore();
const { map } = useMap();

const object = ref<any>({});
const popupCords = ref([0, 0]);

const isPopupShowed = computed(() => !!mapStore.hoveredObject);

const openObject = () => {
  mapStore.setSelectedObject(mapStore.hoveredObject);
};

watch(isPopupShowed, () => {
  if (mapStore.hoveredObject) {
    popupCords.value = map.value?.getPixelFromCoordinate(
      (mapStore.hoveredObject as any).getGeometry().getCoordinates()
    ) as Array<number>;
    const feature = mapStore.hoveredObject as Feature;
    if (feature.get('type') == 'road') {
      const commonData = feature.get('common-data').fields;

      object.value.name = commonData.find(
        ({ code }) => code == 'FULL_NAME'
      )?.value?.value;

      object.value.owner = commonData

        .find(({ code }) => code == 'ROAD_OWNER')
        ?.value?.value?.at(-1)?.text;
      console.log(commonData);
    } else if (feature.get('type') == 'event') {
      object.value.name = feature.get('name');

      object.value.owner = '';
    }
  }
});
</script>
<style lang="scss" scoped>
.popup {
  position: absolute;
  background-color: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  top: v-bind('(popupCords[1] - 55) + "px"');
  left: v-bind('popupCords[0] + 5 + "px"');
}
</style>
