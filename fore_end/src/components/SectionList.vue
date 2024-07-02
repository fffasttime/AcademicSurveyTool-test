
<template>
    <div class="page">
        <!-- <Button label="Stats" @click="stats_visible=true"/>
        <Dialog v-model:visible="stats_visible" modal header="Header" :style="{ width: '50rem' }">
            <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            </p>
        </Dialog> -->
        <Fieldset legend = "Overview">
          <div class="p-card p-component">
          <div class="p-card-body">
            <h2>A survey of hardware error fault tolerance for deep learning</h2>
          </div>
          </div>
            <DataTable :value="sections" tableStyle="min-width: 50rem">
                <Column field="title" header="Section Title"></Column>
                <Column field="beginning" header="Section Description"></Column>
            </DataTable>
        </Fieldset>
        <div class="line_panel_wrapper">
        <section-card
            v-for="(section, index) in sections"
            :key="index"
            :section="section"
            @remove="removeCard(index)"
            @update="updateCard(index, $event)"
        />
        <div class="sectionitem">
            <Button @click="addCard" label="Add Item" icon="pi pi-plus" style="justify-self: center;" />
        </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import SectionCard from "./SectionCard.vue";
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Fieldset from 'primevue/fieldset';

export default {
components: {
  SectionCard, DataTable, Column, Fieldset
},
data() {
    return {
    sections: [
        { section: "importance", beginning: "Toward a AI based a academic survey", reference: [{key:"key",title:"title"}]},
    ],
    stats_visible: false,
    };
},
created() {
    this.fetchSections();
},
methods: {
    async fetchSections() {
      try {
        // Replace the URL with your actual backend API endpoint
        const response = await axios.get("http://localhost:5000/sections");
        this.sections = response.data;
      } catch (error) {
        console.error("Error fetching sections:", error);
      }
    },
    addCard() {
    this.sections.push({key:"new", title: "New title", author: "author 1" });
    },
    removeCard(index) {
    this.sections.splice(index, 1);
    },
    updateCard(index, updatedSection) {
      this.$set(this.sections, index, updatedSection);
    },
},
};
</script>

<style scoped>
.tile_panel_wrapper {
  display: flex;
  flex-direction: row;
  align-items: center;
  width: 100%;
  flex-wrap: wrap;
  gap: 15px;
}
.line_panel_wrapper {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.sectionitem{
  min-width: 340px;
  flex: 1 1 0;
  display: grid;
}
.page{
  display: flex;
  flex-direction: column;
  gap: 15px;
}
</style>