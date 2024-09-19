<template>
  <transition
    enter-active-class="animated fadeIn"
    leave-active-class="animated fadeOut"
  >
    <q-card v-if="opened" class="filter q-pa-lg">
      <div class="text-h6">Фильтр</div>
      <div class="row q-pt-md q-pr-lg q-gutter-md">
        <q-input
          label="Начало работ"
          v-model="filter.startDate"
          class="col-12"
          outlined
          dense
          flat
        />
        <q-input
          label="Окончание работ"
          v-model="filter.endDate"
          class="col-12"
          outlined
          dense
          flat
        />
        <q-badge color="secondary">
          Процент готовности: {{ filter.percentage }}% (от 0 до 100)
        </q-badge>
        <q-slider
          v-model="filter.percentage"
          :min="0"
          :max="100"
          color="green"
        />
        <q-select
          label="Регион"
          v-model="filter.region"
          class="col-12"
          :options="[
            'Центральный федеральный округ',
            'Северо-Западный федеральный округ',
            'Южный федеральный округ',
            'Северо-Кавказский федеральный округ',
            'Приволжский федеральный округ',
            'Уральский федеральный округ',
            'Сибирский федеральный округ',
            'Дальневосточный федеральный округ',
          ]"
          outlined
          dense
          flat
        />
      </div>
    </q-card>
  </transition>
</template>
<script setup lang="ts">
import { toRefs } from 'vue';

const props = defineProps<{
  opened: boolean;
  filter: any;
}>();

const { filter, opened } = toRefs(props);
</script>
<style lang="scss" scoped>
.filter {
  position: absolute;
  top: 60px;
  right: 20px;
  background-color: #fff;
  z-index: 1000;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}
</style>
