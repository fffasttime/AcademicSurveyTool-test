
<template>
    <div class="bib_page">
        <Button label="Stats" @click="stats_visible=true"/>
        <Dialog v-model:visible="stats_visible" modal header="Header" :style="{ width: '50rem' }">
            <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            </p>
        </Dialog>
        <div class="bib_panel_wrapper">
        <book-card
            v-for="(book, index) in books"
            :key="index"
            :book="book"
            @remove="removeCard(index)"
            @update="updateCard(index, $event)"
        />
        <div class="bibitem">
            <Button @click="addCard" label="Add Item" icon="pi pi-plus" style="justify-self: center;" />
        </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import BookCard from "./BookCard.vue";

export default {
components: {
    BookCard,
},
data() {
    return {
    books: [
        { key: "huang2023", title: "Toward a AI based a academic survey", author: "Author 1, Author 2" },
    ],
    stats_visible: false,
    };
},
created() {
    this.fetchBooks();
},
methods: {
    async fetchBooks() {
      try {
        // Replace the URL with your actual backend API endpoint
        const response = await axios.get("http://localhost:5000/books");
        this.books = response.data;
      } catch (error) {
        console.error("Error fetching books:", error);
      }
    },
    addCard() {
    this.books.push({key:"new", title: "New title", author: "author 1" });
    },
    removeCard(index) {
    this.books.splice(index, 1);
    },
    updateCard(index, updatedBook) {
      this.$set(this.books, index, updatedBook);
    },
},
};
</script>

<style scoped>
.bib_panel_wrapper {
  display: flex;
  flex-direction: row;
  align-items: center;
  width: 100%;
  flex-wrap: wrap;
  gap: 15px;
}
.bibitem{
  min-width: 340px;
  flex: 1 1 0;
  display: grid;
}
.bib_page{
  display: flex;
  flex-direction: column;
  gap: 15px;
}
</style>