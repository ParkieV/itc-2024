<template>
  <q-dialog v-model="opened">
    <q-card>
      <q-card-section>
        <div class="text-h6">Создание новой дороги</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <div class="q-pa-md q-pl-none row q-gutter-md">
          <q-input
            class="col-12"
            label="Заказчик строительства"
            v-model="formData.customer"
            outlined
            dense
            flat
          />

          <q-input
            class="col-12"
            label="Исполнитель строительства"
            v-model="formData.contractor"
            outlined
            dense
            flat
          />

          <q-input
            class="col-12"
            label="Описание"
            v-model="formData.description"
            outlined
            dense
            type="textarea"
            flat
          />

          <q-input
            class="col-5"
            label="Дата начала работ"
            v-model="formData.startDate"
            outlined
            dense
            flat
          />

          <q-input
            class="col-5"
            label="Дата окончания работ"
            v-model="formData.endDate"
            outlined
            dense
            flat
          />
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
import { ref, toRefs } from 'vue';

const props = defineProps({
  opened: Boolean,
});

const opened = ref(props.opened);

const emits = defineEmits(['save']);

const formData = ref({
  customer: '',
  contractor: '',
  description: '',
  startDate: '',
  endDate: '',
});
</script>
