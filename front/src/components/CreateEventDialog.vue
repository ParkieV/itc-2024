<template>
  <q-dialog v-model="isOpened">
    <q-card>
      <q-card-section>
        <div class="text-h6">Создание объекта реконструкции</div>
      </q-card-section>
      <q-card-section class="q-pt-none">
        <div class="q-pa-md q-pl-none row q-gutter-md">
          <q-select
            class="col-12"
            label="Основание выполнения работ"
            :options="[
              'Постановление Правительства РФ от 31 августа 2023 года №1410',
              'Государственная программа «Безопасные и качественные дороги»',
            ]"
            v-model="formData.basis"
            outlined
            dense
            flat
          />
          <div class="text-subtitle1">Планирование госзакупок</div>
          <q-select
            class="col-12"
            label="Вид торгов"
            :options="['44-ФЗ', '223-ФЗ']"
            v-model="formData.law"
            outlined
            dense
            flat
          />
          <q-input
            class="col-12"
            label="Ссылка на электронную торговую площадку"
            v-model="formData.link"
            outlined
            dense
            flat
          />
          <q-input
            class="col-12"
            label="Заказчик"
            v-model="formData.customer"
            outlined
            dense
            flat
          />
          <q-input
            class="col-12"
            label="Подрядчик"
            v-model="formData.contractor"
            outlined
            dense
            flat
          />
          <div class="text-subtitle1">Проектирование</div>
          <q-toggle
            class="col-12"
            label="Проект объекта разработан"
            v-model="formData.isDesigned"
          />
          <template v-if="!formData.isDesigned">
            <q-input
              class="col-12"
              label="Подрядчик проекта"
              v-model="formData.designContractor"
              outlined
              dense
              flat
            />
            <q-uploader
              url="http://localhost:4444/upload"
              class="col-12"
              label="Проектная документация"
              flat
              outlined
              dense
            />
          </template>
        </div>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn
          flat
          label="Сохранить"
          color="primary"
          v-close-popup
          @click="emits('save', formData)"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>
<script setup lang="ts">
import { ref } from 'vue';

const props = defineProps({
  opened: Boolean,
});

const isOpened = ref(true);

const emits = defineEmits(['save']);

const formData = ref({
  basis: '',
  customer: '',
  law: '',
  link: '',
  isDesigned: false,
  designContractor: '',
  contractor: '',
});
</script>
