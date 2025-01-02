<template>
  <div class="search">
      <select v-if="form.role==='sponsor'" class="search-options" v-model="form.option">
        <option value="influencer_username">Name</option>
        <option value="reach">Reach</option>
        <option value="category">Category</option>
        <option value="niche">Niche</option>
      </select>
      <select v-if="form.role==='influencer'" class="search-options" v-model="form.option">
        <option value="campaign_name">Name</option>
        <option value="budget">Budget</option>
        <option value="category">Category</option>
      </select>
      <input type="search" placeholder="Search.." class="inputs form-control shadow-none" v-model="form.searchQuery">
      <div class="search-btn" @click="search">
       <i class="fas fa-search"></i>
      </div>
  </div>

</template>

<script>
export default {
  name: "SearchBar",
  data() {
    return {
      form: {
        searchQuery: "",
        role: "",
        option: "category"
      }
    }
  },
  methods: {
    search() {
      this.$store.dispatch("search", this.form);
    }
  },
  created() {
    this.form.role = JSON.parse(localStorage.getItem("role"));
  },
}
</script>

<style scoped>

.inputs {
  width: 30vw;
  padding: 0.5em;
  border-radius: 0.5em;
  font-size: 1.15rem;
  font-family: "Raleway", sans-serif;
  font-weight: 500;
}

.search {
  margin: 2rem 0;
  display: flex;
  justify-content: center;
}

.search-options {
  margin-right: 1rem;
  width: 10vw;
  padding: 0.5em;
  border-radius: 0.5em;
  font-size: 1.15rem;
  font-family: "Raleway", sans-serif;
  font-weight: 300;
  background-color: white;
}

.search-btn {
  margin-left: 1rem;
  background-color: #506582;
  color: white;
  padding: 0.5em 1em;
  border-radius: 0.5em;
  font-size: 1.15rem;
  font-family: "Raleway", sans-serif;
  font-weight: 500;
  cursor: pointer;
}
</style>