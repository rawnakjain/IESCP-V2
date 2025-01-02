<template>

  <layout-ui>
    <template v-slot:main>
      <div class="container-fluid">
        <div class="row">
          <div class="col-md-12">
            <dashboard-greetings :greeting="greeting"></dashboard-greetings>
            <SearchBar></SearchBar>
            <div class="results" v-if="searchResults.length">
              <div class="top-influencers">
                <h2>Search Results</h2>
              </div>
              <div class="cards">
                <div v-for="influencer in searchResults" :key="influencer.id" class="card"
                     style="width: 18rem;">
                  <img src="#" class="card-img-top" alt="">
                  <div class="card-body">
                    <h5 class="card-title">Name: {{ influencer.username }}</h5>
                    <p class="card-text">Reach: {{ influencer.reach }}</p>
                  </div>
                  <ul class="list-group list-group-flush">
                    <li class="list-group-item">Niche: {{ influencer.niche }}</li>
                    <li class="list-group-item">Category: {{ influencer.category }}</li>
                  </ul>
                  <div class="card-body text-center">
                    <a href="/influencer/ads/create" class="submit-btn"> Request</a>
                  </div>
                </div>
              </div>
              <span @click="clearResults" class="submit-btn">Clear Results</span>
              </div>

            <div class="default" v-else>
              <div class="top-influencers">
                <h2>Top Influencers</h2>
              </div>

              <div class="cards">
                <div v-for="influencer in top10InfluencersByReach" :key="influencer.id" class="card"
                     style="width: 18rem;">
                  <img src="" class="card-img-top" alt="">
                  <div class="card-body">
                    <h5 class="card-title">Name: {{ influencer.username }}</h5>
                    <p class="card-text">Reach: {{ influencer.reach }}</p>
                  </div>
                  <ul class="list-group list-group-flush">
                    <li class="list-group-item">Niche: {{ influencer.niche }}</li>
                    <li class="list-group-item">Category: {{ influencer.category }}</li>
                  </ul>
                  <div class="card-body text-center">
                    <a href="/sponsor/ads/create" class="submit-btn"> Request</a>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </template>
  </layout-ui>

</template>

<script>
import DashboardGreetings from "@/components/DashboardGreetings.vue";
import LayoutUi from "@/components/LayoutUi.vue";
import SearchBar from "@/components/SearchBar.vue";

export default {
  name: "SponsorDashboard",
  components: {SearchBar, DashboardGreetings, LayoutUi},
  computed: {

    greeting() {
      return this.$store.getters.greeting;
    },
    influencers() {
      return this.$store.getters.getInfluencers;
    },
    top10InfluencersByReach() {
      return this.influencers
          .slice()
          .sort((a, b) => b.reach - a.reach)
          .slice(0, 10);
    },
    searchResults() {
      return this.$store.getters.getSearchResults;
    }
  },
  methods:{
    clearResults() {
      this.$store.commit("setSearchResults", []);
    }
  },
  beforeMount() {
    this.$store.dispatch("fetchInfluencers");
  },
}
</script>

<style scoped>

.top-influencers {
  margin: 2rem 0;
}

.top-influencers h2 {
  font-weight: 350;
}

.cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.card {
  margin-bottom: 2rem;
  border: 1px dot-dash #f5f5f5;
  border-radius: 10px;
}

.submit-btn {
  text-decoration: none;
  background-color: #506582;
  width: 30vw;
  color: white;
  padding: 7px;
  border-radius: 5px;
  font-size: 1rem;
  font-family: "Raleway", sans-serif;
  font-weight: bold;
  margin-top: 2rem;
  cursor: pointer;
}


</style>