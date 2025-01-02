<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-md-7 left-side">
        <div class="form-container">
          <div class="form-heading">
            <h1>Influencer Registration</h1>
          </div>
          <form class="form" @submit.prevent="submitForm">
            <div class="form-group">
              <label for="influencer_username">Influencer Username:</label>
              <input type="text" id="influencer_username" class="inputs form-control shadow-none"
                     name="influencer_username" v-model="form.username"
                     required>
            </div>
            <div class="form-group">
              <label for="Influencer_email">Influencer Email:</label>
              <input type="email" id="Influencer_email" class="inputs form-control shadow-none" name="Influencer_email"
                     v-model="form.email"
                     required>
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
              <input type="text" id="influencer_niche" class="inputs form-control shadow-none" name="influencer_niche"
                     v-model="form.influencer_niche" required>
            </div>

            <div class="form-group">
              <label for="influencer_budget"> Reach (followers)</label>
              <input type="number" id="influencer_reach" class="inputs form-control shadow-none" name="influencer_reach"
                     v-model="form.influencer_reach" required>
            </div>

            <div class="form-group">
              <label for="influencer_password">Password:</label>
              <input type="password" id="influencer_password" class="inputs form-control shadow-none"
                     name="influencer_password"
                     v-model="form.password" required>
            </div>
            <div class="form-group">
              <label for="influencer_password">Confirm Password:</label>
              <input type="password" id="confirm_influencer_password" class="inputs form-control shadow-none"
                     name="confirm_influencer_password" v-model="form.confirm_password" required>
            </div>
            <div class="error" v-if="getStatus.error">
              <p>{{ getStatus.error }}</p>
            </div>
            <button type="submit" class="submit-btn form-control inputs">Register as Influencer</button>
          </form>
        </div>
        <already-link :text="alreadyLink.text" :link="alreadyLink.link"></already-link>
      </div>
      <right-static></right-static>
    </div>
  </div>
</template>


<script>
import RightStatic from "@/components/sign-page/RightStatic.vue";
import AlreadyLink from "@/components/sign-page/AlreadyLink.vue";
import {mapGetters} from "vuex";

export default {
  name: 'GetStarted',
  components: {AlreadyLink, RightStatic,},
  data() {
    return {
      alreadyLink: {"text": "Already have an account? Log in", "link": "/login"},
      success: false,

      form: {
        username: "",
        email: "",
        influencer_category: "Technology",
        influencer_niche: "",
        influencer_reach: "",
        password: "",
        confirm_password: "",
        role: "influencer"
      }
    }
  },
  computed: {
    ...mapGetters(["getStatus"])
  },
  methods: {
    async submitForm() {
      this.$store.dispatch("submitForm", this.form);

      if (this.getStatus.success) {
        this.$router.push("/login");
      }
    }
  }
}
</script>

<style scoped>

.container-fluid {
  height: auto;
}


.left-side {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2em;
  background-color: #f5f5f5;
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

.error {
  margin-bottom: -2rem;
  color: red;
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


@media (max-width: 576px) {
  .left-side {
    padding: 1em;
    margin-bottom: 1em;
    height: 85vh;
  }

  .inputs {
    width: 80vw;
  }


  .form-heading h1 {
    font-size: 1.5rem;
  }
}
</style>
