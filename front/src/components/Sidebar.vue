<template>
  <transition
    appear
    enter-active-class="animated fadeIn"
    leave-active-class="animated fadeOut"
  >
    <div class="sidebar" v-if="isSidebarShowed">
      <div class="row">
        <q-btn
          flat
          icon="close"
          @click="() => mapStore.clearSelectedObject()"
        />
        <div
          v-if="keys['common-info']?.value?.['Наименование']"
          class="q-mt-xs q-mb-xs"
          style="
            /* очень горьким опытом я узнал, как делать ограничение на строки в ксс. Спасибо кс****жи */
            display: -webkit-box;
            -webkit-line-clamp: 1;
            -webkit-box-orient: vertical;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 80%;
            font-size: 16px;
          "
        >
          {{ keys['common-info'].value['Наименование'] }}
        </div>
      </div>
      <div
        class="column q-mv-sm"
        style="gap: 15px; align-self: center; width: 80%; margin-left: 10%"
      >
        <q-btn
          label="Запланировать ремонтные работы"
          color="primary"
          @click="handlerStartEvent"
        />
        <q-btn label="Запросить аналитику по всей дороге" color="secondary" />
      </div>

      <div
        class="column q-pa-md q-pt-md no-wrap"
        style="max-height: 70vh; overflow-y: scroll; overflow-x: hidden"
      >
        <q-expansion-item
          v-for="[key, object] in Object.entries(keys)"
          :key="object.name"
          expand-separator
          :icon="object.icon"
          :label="object.name"
        >
          <q-card>
            <q-card-section>
              <div v-if="key == 'common-info'">
                <div
                  v-for="[key, value] in Object.entries(object.value)"
                  :key="key"
                >
                  <p
                    style="
                      display: flex;
                      flex-direction: row;
                      justify-content: space-between;
                      flex-wrap: wrap;
                      margin-top: 6px;
                      margin-bottom: 6px;
                    "
                  >
                    <a>{{ key }}</a>
                    <a>{{ value }}</a>
                  </p>
                  <q-separator></q-separator>
                </div>
              </div>
              <q-virtual-scroll
                v-else
                type="table"
                style="max-height: 70vh"
                :virtual-scroll-item-size="48"
                :virtual-scroll-sticky-size-start="48"
                :virtual-scroll-sticky-size-end="32"
                :items="object.value"
              >
                <template v-slot:before>
                  <thead class="text-left" v-if="object.value?.[0]">
                    <tr>
                      <th
                        v-for="[col, colName] in Object.entries(
                          object.value?.[0]
                        )"
                        :key="'1--' + colName"
                      >
                        {{ col }}
                      </th>
                    </tr>
                  </thead>
                </template>

                <template v-slot="{ item: row, index }">
                  <tr :key="index">
                    <td v-for="(item, index2) in row" :key="index + '-' + item">
                      {{ row[index2] }}
                    </td>
                  </tr>
                </template>
              </q-virtual-scroll>
            </q-card-section>
          </q-card>
        </q-expansion-item>
      </div>
    </div>
  </transition>
</template>
<script setup lang="ts">
// @ts-nocheck
import { useMapStore } from 'src/stores/map';
import { computed, onMounted, ref, watch } from 'vue';
import getRoadInfo from 'src/api/getRoadInfo';
import Feature from 'ol/Feature';

const mapStore = useMapStore();

const isSidebarShowed = computed(
  () => !!mapStore.selectedObject && !mapStore.startingEvent
);

const handlerStartEvent = () => {
  if (mapStore.startingEvent) {
    mapStore.endEvent();
  } else {
    mapStore.startEvent();
  }
};

const keys = {
  'common-info': { name: 'Общая информация', value: [], icon: 'perm_identity' },
  'road-owners': {
    name: 'Собственник (балансодержатель)',
    value: [],
    icon: 'perm_identity',
  },
  'operating-organizations': {
    name: 'Эксплуатирующая организация',
    value: [],
    icon: 'perm_identity',
  },
  regulations: {
    name: 'Нормативно-правовые документы',
    value: [],
    icon: 'perm_identity',
  },
  'backbone-network': {
    name: 'Участки, входяшие в опорную сеть',
    value: [],
    icon: 'perm_identity',
  },
  'start-exploraion': {
    name: 'Дата ввода в эксплуатацию',
    value: [],
    icon: 'perm_identity',
  },
  'paid-section-of-the-road': {
    name: 'Участки, используемые на платной основе',
    value: [],
    icon: 'perm_identity',
  },
  'dangerous-sections': {
    name: 'Места концентрации дорожно-транспортных происшествий (аварийно-опасные участки)',
    value: [],
    icon: 'perm_identity',
  },
  'cross-subjects': {
    name: 'Прохождение дороги по территории субъектов Российской Федерации',
    value: [],
    icon: 'perm_identity',
  },
  'climatic-zones': {
    name: 'Дорожно-климатическая зона',
    value: [],
    icon: 'perm_identity',
  },
  'terrain-types': {
    name: 'Тип местности по условиям увлажнения',
    value: [],
    icon: 'perm_identity',
  },
  'max-speeds': {
    name: 'Максимальная разрешенная скорость',
    value: [],
    icon: 'perm_identity',
  },
  'axle-loads': { name: 'Нагрузка на ось', value: [], icon: 'perm_identity' },
  'traffic-intensities': {
    name: 'Среднесуточная интенсивность и состав движения',
    value: [],
    icon: 'perm_identity',
  },
  categories: {
    name: 'Техническая категория',
    value: [],
    icon: 'perm_identity',
  },
  'road-class': { name: 'Класс', value: [], icon: 'perm_identity' },
  'number-of-lanes': {
    name: 'Число полос движения',
    value: [],
    icon: 'perm_identity',
  },
  'roadway-width': {
    name: 'Ширина основной проезжей части дороги',
    value: [],
    icon: 'perm_identity',
  },
  'earthen-canvas-width': {
    name: 'Земляное полотно',
    value: [],
    icon: 'perm_identity',
  },
  'type-of-coatings': {
    name: 'Тип дорожной одежды и вид покрытия',
    value: [],
    icon: 'perm_identity',
  },
};

watch(isSidebarShowed, () => {
  // поверь мне наслово эта хуйня работает. Я не смогу откоментить это. Для ивентов сделаем свою обработку данных. Либо вообще отдельный сайдбар, ибо я слабо представляю куда там делать таблицы
  if (mapStore.selectedObject) {
    const feature = mapStore.getSelectedObject() as unknown as Feature;
    // ебнуться вот это я выдал!
    getRoadInfo(feature.getId() as string).then((res) => {
      Object.entries(res).forEach(([key, value]: [any, any]) => {
        if (key != 'id' && key != 'geodata' && key != 'events') {
          if (value.data) {
            const tableData = value.data;
            keys[key].value = tableData.map(
              ({
                isNew,
                isDeleted,
                hash,
                id,
                dateStart,
                dateFinish,
                hasGeometry,
                children,
                ...obj
              }) => {
                const row = {};
                Object.entries(obj).forEach(([rowKey, rowValue]) => {
                  let resValue = '';
                  if (Array.isArray(rowValue.value)) {
                    resValue = rowValue.value
                      .map(({ text }) => text)
                      .join(', ');
                  } else {
                    resValue = rowValue.value;
                  }
                  row[rowKey] = resValue ?? '-';
                  if (row[rowKey] == '') {
                    row[rowKey] == '-';
                  }
                });
                return row;
              }
            );
          } else if (value.fields) {
            const tableData = {};
            value.fields.forEach(({ title, value }) => {
              let res = '';
              if (Array.isArray(value.value)) {
                res = value.value?.[-1]?.text;
              } else {
                res = value.value;
              }
              tableData[title] = res ?? '-';
            });
            console.log(tableData);
            keys[key].value = tableData;
          }
        }
      });
    });
  }
});
</script>
<style lang="scss" scoped>
.sidebar {
  position: absolute;
  background-color: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  padding: 10px;
  right: 0;
  top: 100px;
  z-index: 1000;
  max-width: 500px;
}
</style>
