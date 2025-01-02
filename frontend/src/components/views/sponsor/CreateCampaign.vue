<template>
  <layout-ui>
    <template v-slot:main>
      <div class="row">
        <DashboardHeading title="Create Campaign"></DashboardHeading>
      </div>
      <div class="form-container">
        <div class="row">
          <div class="col-md-6 content">
            <form>
              <div class="form-group">
                <label for="name">Name</label>
                <input type="text" class="form-control shadow-none" id="name" v-model="campaign.name" required>
              </div>
              <div class="form-group">
                <label for="description">Description</label>
                <textarea class="form-control shadow-none" id="description" v-model="campaign.description"></textarea>
              </div>
              <div class="form-group">
                <label for="category">Category</label>
                <input type="text" class="form-control shadow-none" id="category" v-model="campaign.category" required>
              </div>
              <div class="form-group">
                <label for="start_date">Start Date</label>
                <input type="date" class="form-control shadow-none" id="start_date" v-model="campaign.start_date">
              </div>
              <div class="form-group">
                <label for="end_date">End Date</label>
                <input type="date" class="form-control shadow-none" id="end_date" v-model="campaign.end_date">
              </div>
              <div class="form-group">
                <label for="budget">Budget</label>
                <input type="number" class="form-control shadow-none" id="budget" v-model="campaign.budget" required>
              </div>
              <div class="form-group">
                <label for="visibility">Visibility</label>
                <select class="form-control shadow-none" id="visibility" v-model="campaign.visibility" required>
                  <option value="Public">Public</option>
                  <option value="Private">Private</option>
                </select>
              </div>
              <div class="form-group">
                <label for="goals">Goals</label>
                <textarea class="form-control shadow-none" id="goals" v-model="campaign.goals"></textarea>
              </div>
            </form>
          </div>
          <div class="col-md-6 content">
            <div class="form-group shadow-none">
              <label for="guidelines" class=" mt-2">Guidelines</label>
              <textarea class="form-control shadow-none" id="guidelines" v-model="campaign.guidelines"></textarea>
            </div>
            <div class="button-container">
              <button type="submit" @click="createCampaign" class="submit-btn text-center">Create Campaign</button>
              </div>
          </div>
        </div>
      </div>
    </template>
  </layout-ui>
</template>

<script>
import DashboardHeading from "@/components/DashboardHeading.vue";
import LayoutUi from "@/components/LayoutUi.vue";

export default {
  components: {LayoutUi, DashboardHeading},
  data() {
    return {
      campaign: {
        name: "",
        description: "",
        category: "",
        start_date: "",
        end_date: "",
        budget: "",
        visibility: "Public",
        goals: "",
        guidelines: "",
        is_flagged: false
      },
    }
  },
  computed:{
    success() {
      return this.$store.getters.getStatus.success;
    }
  },
    methods: {
    createCampaign() {
      this.$store.dispatch("createCampaign", this.campaign);
      if (this.success) {
        this.$router.push("/sponsor/campaigns");
        this.$store.commit("setSuccess", false);
      }
    },
  },
}
</script>

<style scoped>

.form-container {
  padding: 1rem;
  border: 1px solid #E0E0E0;
  border-radius: 5px;
  margin: 1rem;
}


form .form-group {
  margin-top: 1em;
}


input, textarea, select {
  width: 30vw;
  padding: 0.5em;
  border-radius: 0.5em;
  border: 1px solid #39465B;
  font-size: 1rem;
  font-family: "Raleway", sans-serif;
  font-weight: 500;
}

input:focus, textarea:focus, select:focus {
  outline: none;
  box-shadow: none; /* Remove the default blue shadow */
  border-color: #39465B; /* Optional: Add your own border color */
}


.error {
  margin-bottom: -2rem;
  color: red;
  font-size: 1rem;
  font-family: "Raleway", sans-serif;
  font-weight: 500;
}

.submit-btn {
  background-color: #506582;
  width: 30vw;
  color: white;
  padding: 8px;
  border-radius: 5px;
  font-size: 1.2rem;
  font-family: "Raleway", sans-serif;
  font-weight: bold;
  margin-top: 2rem;
}

</style>