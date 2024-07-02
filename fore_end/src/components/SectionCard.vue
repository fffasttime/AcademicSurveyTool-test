<script>
import BibEditDialog from './BibEditDialog.vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';

export default {
    props: {
        section: Object,
    },
    data() {
        return {
            dialog_visible: false
        };
    },
    methods: {
        updateCard() {
            this.$emit("update", this.book);
        },
        removeCard() {
            this.$emit("remove", this.book);
        },
        editCard() {
            this.dialog_visible = true;
        },
    },
    components: { BibEditDialog, DataTable, Column }
};
</script>

<template>
    <Card class="sectionitem">
        <template #title> 
            {{section.title}}
        </template> 
        <template #subtitle> 
            {{section.beginning}}
        </template> 
        <template #content>
            <DataTable :value="section.reference" tableStyle="min-width: 50rem">
                <Column field="key" header="Citation Key"></Column>
                <Column field="title" header="Title"></Column>
            </DataTable>
        </template>

    </Card>
</template>


<style scoped>
Textarea {
  width: 200px;
  resize: none;
}

.content_head {
    font-weight: bold;
}
</style>
