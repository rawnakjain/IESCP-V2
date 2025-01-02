<template>
  <layout-ui>
    <template v-slot:main>
      <div class="container-fluid">
        <div class="row">
          <DashboardHeading title="Profile Page"></DashboardHeading>
        </div>
        <div class="row">
          <div class="col-md-12 content">
            <div class="form-container" v-if="form.role==='influencer'">
              <form class="form" @submit.prevent="updateUserDetails">
                <div class="form-group">
                  <label for="influencer_username">Influencer Username:</label>
                  <input type="text" id="influencer_username" class="inputs form-control shadow-none"
                         name="influencer_username" v-model="form.username"
                         required disabled>
                </div>
                <div class="form-group">
                  <label for="Influencer_email">Influencer Email:</label>
                  <input type="email" id="Influencer_email" class="inputs form-control shadow-none"
                         name="Influencer_email"
                         v-model="form.email"
                         required disabled>
                </div>
                <div class="form-group">
                  <label for="influencer_company">Category</label>
                  <select name="influencer_category" id="influencer_category" class="inputs form-control shadow-none"
                          v-model="form.influencer_category" required>
                    <option value="Fashion">Fashion</option>
                    <option value="Food">Food</option>
                    <option value="Travel">Travel</option>
                    <option value="Fitness">Fitness</option>
                    <option value="Lifestyle">Lifestyle</option>
                    <option value="Beauty">Beauty</option>
                    <option value="Parenting">Parenting</option>
                    <option value="Health">Health</option>
                    <option value="Technology">Technology</option>
                    <option value="Gaming">Gaming</option>
                    <option value="Sports">Sports</option>
                    <option value="Music">Music</option>
                    <option value="Entertainment">Entertainment</option>
                    <option value="Education">Education</option>
                    <option value="Finance">Finance</option>
                    <option value="Automobile">Automobile</option>
                    <option value="Pets">Pets</option>
                    <option value="Books">Books</option>
                    <option value="Art">Art</option>
                    <option value="Photography">Photography</option>
                    <option value="Politics">Politics</option>
                    <option value="Science">Science</option>
                    <option value="Environment">Environment</option>
                    <option value="Social Causes">Social Causes</option>
                    <option value="Others">Others</option>
                  </select>
                  <!-- <input type="text" id="influencer_category" class="inputs" name="influencer_category" required> -->
                </div>

                <div class="form-group">
                  <label for="influencer_niche"> Niche </label>
                  <input type="text" id="influencer_niche" class="inputs form-control shadow-none"
                         name="influencer_niche"
                         v-model="form.influencer_niche" required>
                </div>

                <div class="form-group">
                  <label for="influencer_budget"> Reach (followers)</label>
                  <input type="number" id="influencer_reach" class="inputs form-control shadow-none"
                         name="influencer_reach"
                         v-model="form.influencer_reach" required>
                </div>

                <div class="form-group">
                  <label for="influencer_password">New Password (optional)</label>
                  <input type="password" id="influencer_password" class="inputs form-control shadow-none"
                         name="influencer_password"
                         v-model="form.password">
                </div>
                <div class="form-group">
                  {{ message }}
                </div>
                <button type="submit" class="submit-btn form-control inputs">Update Profile</button>
              </form>
            </div>

            <div class="form-container" v-else-if="form.role==='sponsor'">
              <button @click="downloadReport" class="download-btn"> Download Your Report </button> <span v-if="getCeleryWaiting">waiting...</span>
              <form class="form" @submit.prevent="updateUserDetails">
                <div class="form-group">
                  <label for="sponsor_username">Sponsor Username:</label>
                  <input type="text" id="sponsor_username" class="inputs form-control shadow-none"
                         name="sponsor_username"
                         v-model="form.username" disabled required>
                </div>
                <div class="form-group">
                  <label for="sponsor_email">Sponsor Email:</label>
                  <input type="email" id="sponsor_email" class="inputs form-control shadow-none" name="sponsor_email"
                         v-model="form.email" disabled required>
                </div>

                <div class="form-group">
                  <label for="sponsor_company">Sponsor Company:</label>
                  <input type="text" id="sponsor_company" class="inputs form-control shadow-none" name="sponsor_company"
                         v-model="form.sponsor_company" required>
                </div>
                <div class="form-group">
                  <label for="sponsor_industry">Sponsor Industry</label>
                  <select name="sponsor_industry" id="sponsor_industry" class="inputs form-control shadow-none"
                          v-model="form.sponsor_industry" required>
                    <option value="Fashion">Fashion</option>
                    <option value="Food">Food</option>
                    <option value="Travel">Travel</option>
                    <option value="Fitness">Fitness</option>
                    <option value="Lifestyle">Lifestyle</option>
                    <option value="Beauty">Beauty</option>
                    <option value="Parenting">Parenting</option>
                    <option value="Health">Health</option>
                    <option value="Technology">Technology</option>
                    <option value="Gaming">Gaming</option>
                    <option value="Sports">Sports</option>
                    <option value="Music">Music</option>
                    <option value="Entertainment">Entertainment</option>
                    <option value="Education">Education</option>
                    <option value="Finance">Finance</option>
                    <option value="Automobile">Automobile</option>
                    <option value="Pets">Pets</option>
                    <option value="Books">Books</option>
                    <option value="Art">Art</option>
                    <option value="Photography">Photography</option>
                    <option value="Politics">Politics</option>
                    <option value="Science">Science</option>
                    <option value="Environment">Environment</option>
                    <option value="Social Causes">Social Causes</option>
                    <option value="Others">Others</option>
                  </select>
                  <!-- <input type="text" id="influencer_category" class="inputs form-control" name="influencer_category" required> -->
                </div>

                <div class="form-group">
                  <label for="sponsor_budget">Sponsor Budget:</label>
                  <input type="number" id="sponsor_budget" class="inputs form-control shadow-none" name="sponsor_budget"
                         v-model="form.sponsor_budget" required>
                </div>

                <div class="form-group">
                  <label for="sponsor_password">Password:</label>
                  <input type="password" id="sponsor_password" class="inputs form-control shadow-none"
                         name="sponsor_password" v-model="form.password" required>
                </div>
                <div class="form-group">
                  {{ message }}
                </div>
                <button type="submit" class="submit-btn form-control inputs">Update Profile</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </template>
  </layout-ui>
</template>

<script>
import LayoutUi from "@/components/LayoutUi.vue";
import DashboardHeading from "@/components/DashboardHeading.vue";
import {mapGetters} from "vuex";

export default {
  name: "ProfilePage",
  components: {DashboardHeading, LayoutUi},
  data() {
    return {
      form: {
        username: "",
        email: "",
        password: "",
        role: "",
        influencer_category: "",
        influencer_niche: "",
        influencer_reach: "",
        sponsor_company:"",
        sponsor_industry:"",
        sponsor_budget:"",
      },
      message: "",
    }
  },
  computed: {
    ...mapGetters(["getStatus", "getAuth", "getCeleryWaiting"]),
    username() {
      return localStorage.getItem('username');
    },
    user_id() {
      return localStorage.getItem('user_id');
    }
  },
  methods: {
    async updateUserDetails() {
      const response = await this.$store.dispatch("updateUserDetails", this.form);
      this.message = response.message
    },
    async downloadReport() {
      await this.$store.dispatch("downloadReport", this.user_id);
    }
  },
  async beforeMount() {
    this.form = await this.$store.dispatch("fetchProfile", this.username);
  }
}
</script>


<style scoped>

.container-fluid {
  height: auto;
}

.form-heading h1 {
  color: #454545;
  font-family: "Raleway", sans-serif;
  font-optical-sizing: auto;
  font-weight: bolder;
  font-size: 2rem;
}

.form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}


.form .form-group {
  margin-top: 1em;
}


.inputs {
  width: 30vw;
  padding: 0.5em;
  border-radius: 0.5em;
  border: 1px solid #000000;
  font-size: 1rem;
  font-family: "Raleway", sans-serif;
  font-weight: 500;
}

.submit-btn {
  background: linear-gradient(to right, #2C3646, #506582);
  color: white;
  padding: 8px;
  border-radius: 5px;
  font-size: 1.2rem;
  font-family: "Raleway", sans-serif;
  font-weight: bold;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.download-btn{
  background: linear-gradient(to right, #2C3646, #506582);
  color: white;
  padding: 8px;
  border-radius: 5px;
  font-size: 1.2rem;
  font-family: "Raleway", sans-serif;
  font-weight: bold;
}

</style>