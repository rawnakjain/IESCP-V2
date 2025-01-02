<template>
  <layout-ui>
    <template v-slot:main>
      <div class="container-fluid">
        <div class="row">
          <div class="col-md-12">
            <dashboard-heading :title="`Campaign ${campaign.name}`"></dashboard-heading>
          </div>
        </div>
        <div class="row">
          <div class="col-md-12 card-center">
            <div class="card-container">
              <div class="card-bod">
                <div class="part1">
                <p class="card-p">Name: {{campaign.name}}</p>
                <p class="card-p">Category: {{campaign.category}}</p>
                <p class="card-p">Budget: {{campaign.budget}}</p>
                <p class="card-p">Goals: {{campaign.goals}}</p>
                </div>
                <div class="part2">
                <p class="card-p">Description: {{campaign.description}}</p>
                <p class="card-p">Visibility: {{campaign.visibility}}</p>
                <p class="card-p">Starting: {{campaign.start_date}}</p>
                <p class="card-p">Ending: {{campaign.end_date}}</p>
                </div>
                <div class="part3">
                <p class="card-p">Guidelines: {{campaign.guidelines}}</p>
                </div>
                <div class="part4">
                   <button class="btns"> <router-link :to="`/sponsor/campaigns/update/${campaign.id}`">Update</router-link></button>
                  <button class="btns"><router-link to="/sponsor/ads/create" >Create Ad</router-link></button>
                  <button class="btns"><router-link :to="`/sponsor/ads-list/${campaign.id}`">Show Ads</router-link></button>
                  <button  @click="deleteCampaign(campaign.id)" class="btns">Delete</button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="row">
        </div>
      </div>
    </template>
  </layout-ui>
</template>
<script>
import LayoutUi from "@/components/LayoutUi.vue";
import DashboardHeading from "@/components/DashboardHeading.vue";

export default {
  name: "ViewCampaign",
  components: {LayoutUi, DashboardHeading},
  computed: {
    campaignId() {
      return this.$route.params.id;
    },
    campaign() {
      return this.$store.getters.getCampaign;
    },
    success() {
      return this.$store.getters.getStatus.success;
    }
  },
  methods: {
    deleteCampaign(id) {
      this.$store.dispatch("deleteSponsorCampaign", id);
      if(this.success){
        this.$router.push("/sponsor/campaigns");
        this.$store.commit("setSuccess", false);
      }
    },
  },
    async beforeMount() {
      await this.$store.dispatch("fetchCampaign", this.campaignId);
    },
}
</script>


<style scoped>

.card-center{
  display: flex;
  justify-content: center;
  align-items: center;
}

.card-container {
  display: flex;
  flex-direction: column;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 1rem;
  margin: 1rem 0;
  background-color: #fff;
  width:80vw;
  //height:50vh;
  border: 2px solid #506582;
}

.part1, .part2, .part3, .part4{
  display:flex;
  flex-direction:row;
  justify-content: space-around;
  margin-bottom:20px;
  border-bottom: 2px solid #f5f5f5;

}

.card-p{
  font-size: 1.1rem;
  font-weight: 600;
  color: #506582;
}

.part4 a, button{
  text-decoration: none;
  color: white;
  background-color: #506582;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  margin: 0.5rem;
  font-weight: 600;
}

button p{
  font-weight: 600;
}
</style>