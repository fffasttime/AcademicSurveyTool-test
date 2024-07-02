<script>
import Textarea from 'primevue/textarea';

export default {
    props: {
        book: Object,
    },
    components: { Textarea }
};
</script>

<template>
<div class="flex_col_wrapper">
<div>
<span class="content_head">Citation Key: &nbsp;&nbsp;</span>
<InputText v-model="book.key"/>
</div>
<span class="content_head">Title: </span>
<InputText v-model="book.title" style="width: 100%;"/>
<span class="content_head">Relation: </span>
<Textarea v-model="book.relation" autoResize style="width: 100%;"/>
<span class="content_head">Suggestion: </span>
<Textarea v-model="book.suggestion" autoResize style="width: 100%;"/>
<span class="content_head">Relevence rating: {{book.rating}}</span>
<Rating v-model="book.rating" :cancel="false" :stars="9"/>
</div>
</template>

<style scoped>
.flex_col_wrapper{
    display: flex;
    flex-direction: column;
    gap: 15px;
}
.content_head {
    font-weight: bold;
}
</style>
