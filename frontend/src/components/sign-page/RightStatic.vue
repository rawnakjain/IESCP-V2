<template>

  <div class="col-md-5 right-side">
    <div class="heading">
      <h1 class="white-font text-light">Connect.</h1>
      <h1 class="white-font text-light"> Collaborate. </h1>
      <h1 class="white-font text-light"> Amplify.</h1>
    </div>
    <div class="description white-font">
      <p>Launch successful influencer <br> campaigns and elevate your brand.</p>
    </div>
    <div class="join-us">
      <div class="join-us-img"><img src="@/assets/join-us.svg" alt=""></div>
      <div class="join-us-text white-font"> <router-link to="/register"><p>Join Us.</p></router-link></div>
    </div>
  </div>

</template>


<script>
export default {
  name:'RightStatic'
}
</script>

<style>

.right-side {
  display: flex;
  flex-direction: column;
  justify-content: center;
  //align-items: center;
  padding-left: 3.5em;
  height: 100vh;
  background: linear-gradient(to right, #2C3646, #506582);
}


.right-side div {
  margin-top: 0.9em;
}

.heading h1 {
  font-size: 3.5rem;
  font-weight: 800;
  color: #ffffff;
}


.description p {
  font-size: 1.5rem;
  font-weight: 500;
  color: #ffffff;
}


.join-us {
  display: flex;
  flex-direction: row;
}


.join-us p {
  font-size: 1.4rem;
  font-weight: 700;
  color: #ffffff;
  margin-top: 0.3rem;
  margin-left: 1rem;
}


.join-us-text a{
  color: #39465B;
  text-decoration: none;
}

@media (max-width: 576px) {



  .right-side .description, .join-us {
    display: none;
  }


  .right-side .heading h1 {
    font-size: 1rem;
  }


  .right-side {
    height: 13vh;
    padding: 0;
    margin: 0;
    //position: relative;
  }


  .heading {
    display: flex;
    justify-content: space-evenly;
    align-items: flex-start;
  }

  .heading h1{
    margin-top: -1rem;
  }
}
</style>
