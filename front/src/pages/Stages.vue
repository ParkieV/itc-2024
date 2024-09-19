<script setup lang="ts">
// @ts-ignore
import { stage1 } from 'src/assets/stages';
import { ref } from 'vue';
const stages = [{ name: 'Тестовый процесс', stage: stage1 }];
const selectedStage = ref();
</script>

<template>
  <q-page>
    <q-select
      outlined
      v-model="selectedStage"
      :options="stages"
      label="Процессы"
      :display-value="`${
        selectedStage?.name ? selectedStage.name : 'Выберите процесс'
      }`"
      :option-label="(item) => (item === null ? 'Null value' : item.name)"
      style="width: 300px"
    />
    <div
      v-if="selectedStage"
      class="shadow-1"
      style="
        border: 2px solid #aaa;
        width: 600px;
        margin-left: auto;
        margin-right: auto;
        border-radius: 10px;
        margin-bottom: 30px;
      "
    >
      <div v-for="stage in selectedStage.stage">
        <p class="q-pa-sm" style="font-size: 20px; font-weight: 600">
          {{ stage.title }}
        </p>
        <p class="q-pa-sm" style="font-size: 16px; font-weight: 400">Этапы:</p>
        <div class="q-ma-sm q-pa-xs shadow-2" style="border-radius: 6px">
          <div v-for="substage in stage.stages">
            <div
              class="q-ma-sm q-pa-xs"
              style="border: 2px solid #aaa; border-radius: 10px"
            >
              <p
                style="
                  margin-top: 10px;
                  margin-bottom: 10px;
                  margin-left: 6px;
                  font-weight: 600;
                "
              >
                {{ substage.title }}
              </p>
              <p style="font-weight: 400">Флаги:</p>
              <q-toggle
                v-for="[key, value] in Object.entries(substage.flags)"
                :label="key"
                :model-value="value"
                disable
                color="amber-10"
              />
              <p style="font-weight: 400">Атрибуты:</p>
              <div class="row" style="gap: 10px">
                <div v-for="attribute in substage.attributes" class="column">
                  <a>{{ attribute.name }}</a>
                  <a>Тип: {{ attribute.type }}</a>
                </div>
              </div>
            </div>
          </div>
        </div>
        <q-separator />
      </div>
    </div>
  </q-page>
</template>
