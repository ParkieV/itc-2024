<template>
  <q-layout view="lHh Lpr lFf">
    <q-header style="height: 50px" elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title> Карта объектов </q-toolbar-title>
        <q-btn square icon="filter_alt" flat @click="toggleFilter" />
        <q-input
          v-model="search"
          label="Поиск"
          filled
          placeholder="Автодорога Р-242"
          dense
          class="q-mr-md q-pb-none"
          color="white"
          standout
          counter
          clearable
        >
          <template v-slot:prepend>
            <q-icon name="search" />
          </template>
        </q-input>
        <div><q-icon name="account_circle"></q-icon> ООО "Дорожные работы"</div>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-list>
        <q-item-label header> Инструменты </q-item-label>

        <EssentialLink
          v-for="link in linksList"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <Sidebar />
    <Filter :opened="isFilterOpened" :filter="filter" />

    <q-page-container class="full-height">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import EssentialLink, {
  EssentialLinkProps,
} from 'components/EssentialLink.vue';
// import { useMapStore } from 'src/stores/map';
import Sidebar from 'src/components/Sidebar.vue';
import Filter from 'src/components/Filter.vue';

defineOptions({
  name: 'MainLayout',
});

const search = ref();
const filter = ref({});

// const mapStore = useMapStore();

const linksList: EssentialLinkProps[] = [
  {
    title: 'Создать событие на карте',
    caption: 'Выберите элемент дороги чтобы создать событие ремонта',
    icon: 'design_services',
    // TODO: вместо ссылок добавить некий флаг в стор, который отображает режим текущего редактирования
  },
  {
    title: 'Создать дорогу',
    caption: 'Создание новой дороги на карте',
    icon: 'add_road',
  },
];

const leftDrawerOpen = ref(false);
const isFilterOpened = ref(false);

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}

const toggleFilter = () => {
  isFilterOpened.value = !isFilterOpened.value;
};
</script>
