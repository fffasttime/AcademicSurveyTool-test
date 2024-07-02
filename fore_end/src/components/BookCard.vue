<script>
import BibEditDialog from './BibEditDialog.vue';

export default {
    props: {
        book: Object,
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
    components: { BibEditDialog }
};
</script>

<template>
    <Card class="bibitem">
        <template #title> 
            <Button @click="editCard()" severity="info" icon="pi pi-pencil" rounded outlined />
            <Dialog v-model:visible="dialog_visible" modal maximizable style="width: 1080px;">
                <template #header>
                Edit Citation
                </template>
                <BibEditDialog :book="book"/>
                <template #footer>
                    <Button @click="removeCard" label="Delete Item" severity="danger" icon="pi pi-trash" />
                    <Button label="Cancel" severity="secondary"  icon="pi pi-times"/>
                    <Button @click="updateCard" label="Save" severity="success" icon="pi pi-check" />
                </template>
            </Dialog>
            {{book.key}}
        </template> 
        <template #subtitle> 
            {{book.title}}
        </template> 
        <template #content>
            <p>
            <span class="content_head">Authors: </span>
            <em>{{book.author}}</em>
            </p>
            <p>
            <Tag value="AI" />
            <span class="content_head"> Relation: </span>
            {{book.relation}}
            </p>
            <p>
            <Tag value="AI" />
            <span class="content_head"> Suggestion: </span>
            {{book.suggestion}}
            </p>
            <p>
            <Tag value="AI" />
            <span class="content_head"> Relevence rating: </span>
            {{book.rating}}
            </p>
            <p>
            <Rating v-model="book.rating" readonly :cancel="false" :stars="9" st/>
            </p>
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
