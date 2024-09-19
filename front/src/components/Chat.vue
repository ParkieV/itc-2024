<template>
  <transition
    enter-active-class="animated fadeIn"
    leave-active-class="animated fadeOut"
  >
    <div v-if="opened" class="chat q-pa-md">
      <div class="row justify-between">
        <div class="text-h6">Умный чат-бот 🤖</div>
        <q-btn round dense flat icon="close" @click="$emit('close')" />
      </div>
      <q-separator class="q-my-md" />
      <q-chat-message
        v-for="message in messages"
        :key="message"
        :text="[message.text]"
        :sent="message.sent"
      />
      <q-input outlined v-model="message" label="Сообщение">
        <template v-slot:after>
          <q-btn round dense flat icon="send" @click="sendMessage" />
        </template>
      </q-input>
    </div>
  </transition>
</template>
<script setup lang="ts">
// @ts-nocheck
import axios from 'axios';
import { onMounted, Ref, ref } from 'vue';

const props = defineProps<{
  opened: boolean;
}>();

const emits = defineEmits(['close']);

const messages = ref([]);
const message = ref('');

const sendMessage = async () => {
  // @ts-ignore
  messages.value.push({
    text: message.value,
    sent: true,
  });
  const query = message.value;
  message.value = '';

  const answer = await axios.post(
    'http://5.42.83.81:8000/getAnswer',
    {
      description: query,
    },
    {
      headers: {
        authorization:
          'TQ1JLdWGA1TCPm2x1mUqkOccCcwT//4a87n+Tqx4eGzSmHM5LmuxJT11mIR5IBoP5LDakUIelGHorz7L',
        accept: 'application/json',
        'Content-Type': 'application/json',
      },
    }
  );
  messages.value.push({
    text: answer.data.answer,
    sent: false,
  });
};
</script>
<style lang="scss" scoped>
.chat {
  z-index: 1000;
  position: absolute;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  bottom: 20px;
  left: 20px;
  max-width: 500px;
}
</style>
