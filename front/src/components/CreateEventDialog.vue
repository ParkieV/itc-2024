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
          <q-select
            class="col-12"
            v-model="selectedStage"
            :options="stages"
            label="Процессы"
            :display-value="`${
              selectedStage?.name ? selectedStage.name : 'Выберите процесс'
            }`"
            :option-label="(item) => (item === null ? 'Null value' : item.name)"
            outlined
            dense
            flat
          />
          <div v-if="selectedStage" style="width: 100%">
            <div
              v-for="(stage, index) in selectedStage.stage"
              class="q-pa-sm q-mb-md"
              style="border: 2px solid #aaa; border-radius: 10px"
            >
              <div class="row justify-between">
                <p
                  class="q-px-sm q-pt-sm"
                  style="font-size: 20px; font-weight: 600"
                >
                  {{ stage.title }}
                </p>
                <q-toggle
                  :model-value="stage.disabled"
                  @update:model-value="
                    (newValue) => {
                      handleToggle1(newValue, index);
                    }
                  "
                />
              </div>
              <q-separator />
              <div
                v-for="(substage, subIndex) in stage.stages"
                class="q-pa-sm"
                style="border-radius: 10px; margin-bottom: 8px"
              >
                <div class="row justify-between">
                  <p
                    style="
                      margin-top: 10px;
                      margin-bottom: 10px;
                      margin-left: 6px;
                      font-weight: 400;
                      font-size: 14px;
                    "
                  >
                    {{ substage.title }}
                  </p>
                  <q-toggle
                    :model-value="substage.disabled"
                    @update:model-value="
                      (newValue) => {
                        handleToggle2(newValue, index, subIndex);
                      }
                    "
                  />
                </div>

                <div
                  v-for="(attribute, subSubIndex) in substage.attributes"
                  style="margin-top: 10px"
                >
                  <q-input
                    v-if="attribute.type == 'text'"
                    class="col-12"
                    :label="attribute.name"
                    v-model="
                      formData[index].stages[subIndex].attributes[subSubIndex]
                        .value
                    "
                    :disable="stage.disabled || substage.disabled"
                    outlined
                    dense
                    flat
                  />
                  <q-uploader
                    v-else
                    hide-upload-btn
                    @added="
                      ($event) =>
                        processFiles($event, index, subIndex, subSubIndex)
                    "
                    :disable="stage.disabled || substage.disabled"
                    :label="attribute.name"
                    multiple
                    accept="image/*"
                  />
                  <q-separator style="margin-top: 10px" />
                </div>
                <q-separator />
              </div>
            </div>
          </div>
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
import { computed, ref, watch } from 'vue';
import { stage1 } from 'src/assets/stages';

const handleToggle1 = (newVal, index) => {
  formData.value[index].disabled = newVal;
};

const handleToggle2 = (newVal, index, index2) => {
  formData.value[index].stages[index2].disabled = newVal;
};

const stages = [{ name: 'Тестовый процесс', stage: stage1 }];
const selectedStage = ref();

const props = defineProps<{
  opened: boolean;
}>();

const isOpened = computed(() => props.opened);

const emits = defineEmits(['save']);

const processFiles = (files, index, index2, index3) => {
  files.forEach((file) => {
    const reader = new FileReader();
    formData.value[index].stages[index2].attributes[index3].value = [];
    reader.onload = (e) => {
      formData.value[index].stages[index2].attributes[index3].value.push(
        e.target.result
      );
    };
    reader.readAsDataURL(file);
  });
};

const formData = ref({});

watch(selectedStage, () => {
  const newData = selectedStage.value.stage;
  newData.forEach((stage) => {
    stage.disabled = false;
    stage.stages.forEach((subStage) => {
      subStage.disabled = false;
    });
  });
  console.log(newData);
  formData.value = newData;
});

watch(
  formData,
  () => {
    console.log('allo');
    let disableNext = false;
    formData.value.forEach((stage) => {
      if (disableNext) {
        stage.disabled = true;
      }
      if (stage.disabled) {
        disableNext = true;
      }
      stage.stages.forEach((subStage) => {
        if (stage.disabled) {
          subStage.disabled = true;
        }
      });
    });
  },
  { deep: true }
);
</script>
